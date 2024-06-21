import pickle

from data_reader import get_dataframe
from rankfm.rankfm import RankFM

from recommender import Recommender

# print("I love Python")
# rating_converter = {
#     'user': int,
#     'isbn': str,
#     'rating': float
# }

# ratings = get_dataframe(filepath = '../data/BX-Book-Ratings-cleaned.csv', converter = rating_converter)
# mean_rating = ratings.loc[ratings['rating'] > 0]['rating'].mean()
# mean_rating_per_user = ratings.loc[ratings['rating'] > 0].select_dtypes(include=['int64', 'float64']).groupby('user').mean()
# good_ratings_and_implicit_fb = ratings.loc[(ratings['rating'] > mean_rating) | (ratings['rating'] == 0)]
# ratings_with_u_min10r = good_ratings_and_implicit_fb.groupby('user').filter(lambda r: r['rating'].count() > 10)
# shuffled_ratings = ratings_with_u_min10r.sample(frac=1)


# model = pickle.load(open("v0_0_and_oavg_without_features", "rb"))

# recs = pickle.load(open("v0_10_recs_user", "rb"))

# first_pairs = shuffled_ratings[['user', 'isbn']].head()
# first_users = shuffled_ratings.head()['user'].unique()


# preds = model.predict(pairs = first_pairs, cold_start = 'nan')
# recs = model.recommend(first_users, n_items=10)

recommender = Recommender()
if __name__ == '__main__':
    recs = recommender.cold_start_recommend(20,"germany", n_items=10)
    print(recs)

# recs = recommender.get_for_user(99)
# sim_items = recommender.get_similar_items("0971880107")
# print(recommender.get_similar_users(115392))



