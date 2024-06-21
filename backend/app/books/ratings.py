import os
from datetime import date
from typing import List, Optional, Union

import pandas as pd
from pydantic.dataclasses import dataclass

ratings = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/BX-Book-Ratings-cleaned.csv', sep=';', converters = {'user': int, 'isbn': str, 'rating': float} , encoding="CP1252")
grouped = ratings.groupby('user')

@dataclass
class Rating:
    userId: str
    bookId: str
    rating: int

ratings = list(map(lambda x: Rating(x[0], x[1], x[2]), ratings.values.tolist()))

user_ratings = {}
for user, g_rate in grouped:
    vals = list(map(lambda x: [x[1], x[2]],g_rate.values.tolist()))
    user_ratings[user] = vals


