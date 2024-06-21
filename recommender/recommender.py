import pickle
from multiprocessing import Process, Queue
from typing import List, TypedDict

import numpy as np
import pandas as pd
from data_reader import get_dataframe
from pandas import DataFrame
from rankfm.rankfm import RankFM


class Recommender:
    _model_file = open("trained_models/final", "rb")
    _users_file = open("known_users", "rb")
    _user_converter = {
        'User-ID': int,
        'Age': int,
        'City': str,
        'State': str,
        'Country': str
    }


    def __init__(self):
        self.model: RankFM = pickle.load(self._model_file)
        self._users: DataFrame = pickle.load(self._users_file)
    
    def get_for_user(self, user_id: int, n_items: int = 10, filter_previous=False):
        recs = self.model.recommend([user_id], n_items, filter_previous).loc[user_id]
        rec_array = []
        for rec in recs:
            rec_array.append(rec)
        
        return rec_array

    def get_similar_items(self, item_id: str, n_items: int = 10):
        return self.model.similar_items(item_id, n_items)


    def get_similar_users(self, user_id: int, n_items: int = 10):
        return self.model.similar_users(user_id, n_items)
    
    def cold_start_similar_users(self, age: int, country: str):
        age_tolerance = 5

        same_country_users = self._users.loc[self._users["Country"] == country]

        if len(same_country_users) == 0:
            return self._similar_age(self._users, age, age_tolerance)
        else: 
            return self._similar_age(same_country_users, age, age_tolerance)


    def _similar_age(self, filtered_users: DataFrame, age: int,  age_tolerance: int):
        while len(filtered_users.loc[abs((self._users["Age"] - age)) <= age_tolerance]) == 0:
            age_tolerance = age_tolerance * 1.5

        return filtered_users.loc[abs((self._users["Age"] - age)) <= age_tolerance]

    def cold_start_recommend(self, age: int, country: str, has_rated_items: List[str] = [], n_items: int = 10):
        similar_users = self.cold_start_similar_users(age, country)["User-ID"].values[:400]
        rec_candidates_by_users = []
        
        if(len(similar_users) < 10):
            rec_candidates_by_users.append(self.model.recommend(similar_users, n_items=n_items).values.flatten())
        else:
            n_processes = 4
            user_recs_queue = Queue()
            chunk_size = len(similar_users) // n_processes
            users_chunks = [similar_users[i:i + chunk_size] for i in range(0, len(similar_users), chunk_size)]
            tasks = []

            for chunk in users_chunks:
                tasks.append({"target": rec_in_process, "kwargs": {"chunk": chunk, "model": self.model, "queue": user_recs_queue}})
            
            run_in_parallel(tasks)
            rec_candidates_by_users = user_recs_queue.get()

        rec_candidates_by_items = []

        for item in has_rated_items:
            try:
                rec_candidates_by_items = np.append(rec_candidates_by_items, self.model.similar_items(item))
            except:
                continue
        
        all_recs = np.append(rec_candidates_by_users, rec_candidates_by_items)
        np.random.shuffle(all_recs)
        return list(set(all_recs))[:n_items]

    class UserFeature(TypedDict):
        user_id: int
        country: str
        age: int

    class Interaction(TypedDict):
        user_id: int
        item_id: str
        rating: float
    
    class ItemFeatures(TypedDict):
        isbn: str
        publication_year: int

    def incremential_fit(self, interactions: List[Interaction] = None, user_features: List[UserFeature] = None):
        interaction_data = []
        user_data = []

        for i in interactions:
            interaction_data.append([i["user_id"], i["item_id"], i["rating"]])

        interactions_frame = pd.DataFrame(interaction_data, columns=["user_id", "item_id", "rating"])

        """
        rankfm/rankfm.py line 157, _init_interactions macht probleme
        self.interactions['user_id'] = self.interactions['user_id'].map(self.user_to_index).astype(np.int32)
        """
        self.model = self.model.fit_partial(interactions_frame[["user_id", "item_id"]], epochs=1, verbose=True)



def rec_in_process(chunk, model: RankFM, queue: Queue):
    queue.put(model.recommend(chunk, n_items=10).values.flatten())

def run_in_parallel(tasks):
    ps = []
    for task in tasks:
        p = Process(target=task["target"], kwargs=task["kwargs"])
        p.start()
        ps.append(p)

    for p in ps:
        p.join()