# Dependencies.

import os
from typing import List, Optional

import pandas as pd
from pydantic.dataclasses import dataclass


@dataclass
class Book:
    bookId: str
    title: str
    author: Optional[str]
    publisher: Optional[str]
    year: Optional[int]
    cover: Optional[str]
    excerpt: Optional[str]
    pages: Optional[int]
    publishedPlaces: Optional[List[str]]
    tags: Optional[List[str]]



# Load Data.
books = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/BX-Books-cleaned-final.csv', sep=";",  na_filter=False, encoding="latin1", escapechar='\\')
books = list(map(lambda x: Book(x[0], x[1], x[2], x[4], x[3], x[7], x[8], x[9], x[10].strip('\'][\'').split('\', \''), x[11].strip('\'][\'').split('\', \'')), books.values.tolist()))

booksMLPopular = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/MostLeastPopular.csv', sep=",", encoding="CP1252")
booksMLPopular = list(map(lambda x: Book(x[0], x[1], x[2], x[4], x[3], x[7], x[8], x[9], x[10].strip('\'][\'').split('\', \''), x[11].strip('\'][\'').split('\', \'')), booksMLPopular.values.tolist()))

bookshash = {}
for book in books:
    bookshash[book.bookId] = book