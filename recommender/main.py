import pickle
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None
from data_reader import get_dataframe
from rankfm.evaluation import (discounted_cumulative_gain, diversity, hit_rate,
                               precision, recall, reciprocal_rank)
from rankfm.rankfm import RankFM
from sklearn.model_selection import train_test_split

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
tags = get_dataframe(filepath = "tags_sorted.csv", converter = tags_converter )
extended_books = get_dataframe(filepath = '../data/BX-Books-extended.csv', converter = ext_books_converter)[["ISBN", "Tags"]]

tags = tags.loc[tags['Count'] >= 50]

"""
analyze ratings and choose how to train with it
according to docs of data, ratings with value 0 are considered as implicit fb
those ratings are weighted higher than bad ratings
+ the ratings with higher than average rating value have higher weights
to calculate average rating value, 0-values are not taken into account

then users with at least 10 ratings/fb are selected to ensure better splitting
in train and test (min 8 r/fb in train and min 2 r/fb in test)
"""

mean_rating = ratings.loc[ratings['rating'] > 0]['rating'].mean()
mean_rating_per_user = ratings.loc[ratings['rating'] > 0].select_dtypes(include=['int64', 'float64']).groupby('user').mean()
# good_ratings_and_implicit_fb = ratings.loc[(ratings['rating'] > mean_rating) | (ratings['rating'] == 0)]

print("mean rating where rating > 0: {}".format(mean_rating))

unique_users_count = ratings.user.nunique()
unique_books_count = ratings.isbn.nunique()
sparsity = 1 - (len(ratings) / (unique_users_count * unique_books_count))

print("sparsity of uncleaned rating matrix: {}".format(sparsity))

ratings_with_u_min10r = ratings.groupby('user').filter(lambda r: r['rating'].count() >= 10)
# shuffled_ratings = ratings_with_u_min10r.sample(frac=1)

unique_users_count = ratings_with_u_min10r.user.nunique()
unique_books_count = ratings_with_u_min10r.isbn.nunique()
sparsity = 1 - (len(ratings_with_u_min10r) / (unique_users_count * unique_books_count))

print("sparsity of cleaned rating matrix with: {}".format(sparsity))
print("length of uncleaned rating matrix with: {}".format(len(ratings)))
print("length of cleaned rating matrix with: {}".format(len(ratings_with_u_min10r)))

"""
building user features and book features as data frames
need to encode columns correctly if needed (dummy or one hot)

example features:
    user features   => Age, Country
    book features   => Year-Of-Publication (age in months)

different feature sets are tested and models for each pair of sets is pickled and saved
these different models are evaluated later
"""
user_features = pd.get_dummies(data = users, columns = ['Country'], prefix = ['uf_2']).drop(columns = ['City', 'State'])
book_features = pickle.load(open("book_features", "rb"))



# book_features = books.drop(columns = ['Book-Title', 'Book-Author', 'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L'])
# book_features['Year-Of-Publication'] = book_features['Year-Of-Publication'].apply(lambda y: (datetime.now().year - y) * 12)
# book_features = book_features.rename(columns={'Year-Of-Publication': 'bf_1'})


# print("adding tags as book features")
# tag_cols = tags["Tags"].values
# tags_frame = pd.DataFrame(columns=tag_cols)
# book_features = pd.concat([book_features, tags_frame], axis=1).fillna(0)
# count = 0
# for i, b in extended_books.iterrows():
#     for j, t in tags.iterrows():
#         tag = t["Tags"]
#         if t["Tags"] in b["Tags"] :
#             b[tag] = 1

# book_feature_file = open("book_features", "wb")
# b_features_dump = pickle.dumps(book_features)
# book_feature_file.write(b_features_dump)
# print("saved book features")

print("user features shape {}".format(user_features.shape))
print("book features shape {}".format(book_features.shape))

"""
splitting
in 80/20, we ensure that there are enough users in train and test set with stratitfy
after split, reduce set of user and book features, select only feature rows for existing books and users in train set
"""

user_ids = ratings_with_u_min10r['user'].unique()
book_isbns = ratings_with_u_min10r['isbn'].unique()

train_set, test_set = train_test_split(ratings_with_u_min10r, test_size = 0.2, stratify=ratings_with_u_min10r['user'])
train_set.to_pickle("train_set")
test_set.to_pickle("test_set")

weights = []
train_set = train_set.reset_index()
test_set = test_set.reset_index()

for i, row in train_set.iterrows():
    if row.rating == 0:
        weights.append(1)
    elif row.rating >= mean_rating_per_user.loc[row.user].item():
        weights.append(1)
    else:
        weights.append(0)

weights = np.array(weights)
train_set = train_set[["user", "isbn"]]
test_set = test_set[["user", "isbn"]]

print("train set shape {}".format(train_set.shape))
print("test set shape {}".format(test_set.shape))
print("rating matrix shape {}".format(ratings_with_u_min10r.shape))

train_user_features = user_features[user_features["User-ID"].isin(train_set['user'])]
train_user_features.loc[:,"Age"] /= train_user_features["Age"].max()
train_book_features = book_features[book_features["ISBN"].isin(train_set['isbn'])]
train_book_features.loc[:,"bf_1"] /= train_book_features['bf_1'].max()

"""
sample weights
for each good interaction we set weight 1 
and for each bad interaction weight 0

definition of good interaction:
implicit fb, rating = 0
OR
good rating, rating between 1-10 AND over user average rating
"""
model = RankFM(factors=50, loss='warp', max_samples=100, alpha=0.01, sigma=0.1, learning_rate=0.10, learning_schedule='invscaling')
model.fit(interactions=train_set, epochs=50, sample_weight=weights, user_features=train_user_features, item_features=train_book_features, verbose=True) # item_features sample_weight=sample_weight,

print("saving model")
pickled_model = pickle.dumps(model) 
f = open("model_with_extended_book_features", "wb")
f.write(pickled_model)
print("saved model")



















"""
we want all items to be included in the training 
create dummy user and create interactions for that user with every item and append to set
"""
# print("dummy")
# dummy_user = 92625
# dummy_interactions = []
# all_isbns = books["ISBN"].unique()
# print("books num")
# print(len(all_isbns))

# dummy_weights = []

# for isbn in all_isbns[:len(all_isbns)]:

#     if isbn not in train_book_features["ISBN"].values:
#         dummy_interactions.append([dummy_user, isbn])
#         dummy_weights.append(0)

# dummy_interactions = pd.DataFrame(dummy_interactions, columns=["user", "isbn"])
# new_users = pd.DataFrame({"User-ID": dummy_user, "Age": 23}, index=[0])

# n_new_books = 5000

# print(train_user_features.head())
# train_user_features = pd.concat([train_user_features, new_users], ignore_index=True)
# train_user_features = train_user_features.reset_index().fillna(0).drop(columns=['index'])
# all_books_set = pd.concat([train_set, dummy_interactions[:n_new_books]], ignore_index=True)
# all_books_set.reset_index()

# print(dummy_interactions.shape)
# print(dummy_interactions.head())
# print(weights.shape)

# all_books_features_limited = book_features[book_features["ISBN"].isin(all_books_set['isbn'])]
# model.fit(interactions=all_books_set, epochs=50, sample_weight=np.append(weights, dummy_weights[:n_new_books]), user_features=train_user_features, item_features=all_books_features_limited, verbose=True) # item_features sample_weight=sample_weight,

# # print(model.recommend([dummy_user]))

# print("save")
# pickled_model = pickle.dumps(model) 
# f = open("all_books_not_in_limited_5k", "wb")
# f.write(pickled_model)
# print("written")

# print(model.similar_users(dummy_user))

# print("partial fit")
# saved_model: RankFM = pickle.load(open("2", "rb"))
# # saved_model.fit_partial(t_set[:10], sample_weight=weights[:10], verbose=True)

# print(saved_model.similar_users(dummy_user))

# recs = saved_model.recommend([1])
# print(recs)










# precision = precision(model, test_set, k=10)
# recall = recall(model, test_set, k=10)


# print("precision {}".format(precision))
# print("recall {}".format(recall))

# recommendations = model.recommend(user_ids, n_items=10)
# recommendations.to_pickle("lab2_recommendations_10pu")