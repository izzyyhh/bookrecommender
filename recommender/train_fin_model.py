import pickle
from datetime import datetime
from typing import List

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

user_converter = {
    'User-ID': int,
    'Age': int,
    'City': str,
    'State': str,
    'Country': str
}

book_converter = {
    'ISBN': str,
    'Book-Title': str,
    'Book-Author': str,
    'Year-Of-Publication': int,
    'Publisher': str,
    'Image-URL-S': str,
    'Image-URL-M': str,
    'Image-URL-L': str,
}

tags_converter = {
    'Tags': str,
    'Count': int
}

ext_books_converter = {
    'ISBN': str,
    'Tags': str
}

ratings = get_dataframe(filepath = '../data/BX-Book-Ratings-cleaned.csv', converter = rating_converter)
users = get_dataframe(filepath = '../data/BX-User-cleaned.csv', converter = user_converter)
books = get_dataframe(filepath = '../data/BX-Books-cleaned.csv', converter = book_converter)
tags = get_dataframe(filepath = "./trained_models/data/tags_sorted.csv", converter = tags_converter )
extended_books = get_dataframe(filepath = '../data/BX-Books-extended.csv', converter = ext_books_converter)[["ISBN", "Tags"]]

u = users[users["User-ID"].isin(ratings['user'])]

print(u.head())

d = pickle.dumps(u)
f = open("known_users", "wb")
f.write(d)


mean_rating = ratings.loc[ratings['rating'] > 0]['rating'].mean()
mean_rating_per_user = ratings.loc[ratings['rating'] > 0].select_dtypes(include=['int64', 'float64']).groupby('user').mean()

user_features: DataFrame = pickle.load(open("user_features", "rb"))
book_features: DataFrame = pickle.load(open("book_features", "rb"))

weights = []

for i, row in ratings.iterrows():
    if row.rating == 0:
        weights.append(1)
    elif row.rating >= mean_rating_per_user.loc[row.user].item():
        weights.append(2)
    else:
        weights.append(0)

user_ids = ratings["user"].unique()
book_ids = ratings["isbn"].unique()

user_features = user_features[user_features["User-ID"].isin(ratings['user'])]
book_features = book_features[book_features["ISBN"].isin(ratings['isbn'])]

user_features.loc[:,"Age"] /= user_features["Age"].max()
book_features.loc[:,"bf_1"] /= book_features['bf_1'].max()


print("training")
model = RankFM(factors=50, loss='warp', max_samples=100, alpha=0.01, sigma=0.1, learning_rate=0.10, learning_schedule='invscaling')
model.fit(interactions=ratings[["user", "isbn"]], epochs=50, sample_weight=np.array(weights), user_features=user_features, item_features=book_features, verbose=True)

print("saving model")
pickled_model = pickle.dumps(model) 
f = open("final", "wb")
f.write(pickled_model)
print("saved model")
