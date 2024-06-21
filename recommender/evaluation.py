import pickle

import numpy as np
import pandas as pd
from pandas import DataFrame

pd.options.mode.chained_assignment = None
from data_reader import get_dataframe
from rankfm.evaluation import (discounted_cumulative_gain, diversity, hit_rate,
                               precision, recall, reciprocal_rank)
from rankfm.rankfm import RankFM

rating_converter = {
    'user': int,
    'isbn': str,
    'rating': float
}

ratings = get_dataframe(filepath = '../data/BX-Book-Ratings-cleaned.csv', converter = rating_converter)
mean_rating = ratings.loc[ratings['rating'] > 0]['rating'].mean()
mean_rating_per_user = ratings.loc[ratings['rating'] > 0].select_dtypes(include=['int64', 'float64']).groupby('user').mean()

def good_ratings_and_implicit_filter(group):
    avg_rating = group['rating'].mean()
    
    return group.loc[(group['rating'] >= avg_rating) | (group['rating'].eq(0))]

def precision_at_k(model: RankFM, test_set: DataFrame, k=10):
    """
    Calculates mean precision at k recommendations.

    -- Important Definitions --
    True Positives: Recommended and interaction between user and book exists and rating is good or it is implicit feedback (rating = 0)
    False Positives: Recommended and interaction between user and book does not exist or if exists, rating is bad
    Good Rating: Above User Average Rating and NOT 0
    Implicit fb: Rating = 0
    Bad Rating: Below User Average Rating and NOT 0
    """
    test_set = test_set.groupby('user').apply(good_ratings_and_implicit_filter).reset_index(drop=True)
    interactions_per_user = test_set.groupby('user')['isbn'].apply(set)
    test_users = test_set['user'].unique()
    all_precisions = []

    for user in test_users:
        gt_books: set = interactions_per_user[user] # user item pairs to be predicted

        if len(gt_books) >= k:
            recommended_books = set(model.recommend([user], n_items=k, filter_previous=True).loc[user])
            all_precisions.append(len(recommended_books & gt_books) / k)
        else:
            recommended_books = set(model.recommend([user], n_items=len(gt_books)).loc[user])
            all_precisions.append(len(recommended_books & gt_books) / len(gt_books))

    return np.mean(all_precisions)


def recall_at_k(model: RankFM, test_set: DataFrame, k=10):
    """
    Calculates mean recall at k recommendations.

    -- Important Definitions --
    False Negatives: Not Recommended but should have, bc has good rating or implicit fb
    """
    test_set = test_set.groupby('user').apply(good_ratings_and_implicit_filter).reset_index(drop=True)
    interactions_per_user = test_set.groupby('user')['isbn'].apply(set)
    test_users = test_set['user'].unique()
    recs: DataFrame = model.recommend(users=test_users, n_items=k,filter_previous=True, cold_start='nan')
    user_in_recs = recs.index.values

    all_recalls = []

    for user in user_in_recs:
        recommended_books = set(recs.loc[user])
        gt_books = interactions_per_user[user]

        all_recalls.append(len(recommended_books & gt_books) / len(gt_books))
    
    return np.mean(all_recalls)

model: RankFM = pickle.load(open("lab2_all_ratings_with_binary_weights", "rb"))
test_set: DataFrame = pickle.load(open("lab2_test_set", "rb"))
train_set: DataFrame = pickle.load(open("lab2_train_set", "rb"))

print(precision_at_k(model, test_set, 10))
print(recall_at_k(model, test_set, 10))

