import json
import os
import warnings
from collections import defaultdict
from datetime import date
from typing import List, Optional, Union

warnings.filterwarnings(action='ignore', category=FutureWarning) # setting ignore as a parameter and further adding category

import numpy as np
import pandas as pd
from app.books import books, ratings, users
from app.recommender import recommender
from elasticsearch import Elasticsearch
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

Recommender = recommender.Recommender
elasticsearch_url = os.environ['ES_URL'] 
es = Elasticsearch(elasticsearch_url)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ErrorMessage(BaseModel):
    description: str

@dataclass
class Book:
    bookId: str
    title: str
    author: Optional[str]
    publisher: Optional[str]
    year: Optional[int]
    cover: Optional[str]

@dataclass
class BookDetails:
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

@dataclass
class User:
    userId: str
    age: int
    country: str
    favoriteAuthor: Optional[str]
    favoritePublisher: Optional[str]
    favorites: Optional[List[int]]

@dataclass
class Rating:
    userId: str
    bookId: str
    rating: int

@dataclass
class Favorite:
    userId: str
    bookId: str

allFavorites = defaultdict(list)
newUsers = {}
newUserIds = []
allRatings = pd.DataFrame(ratings.ratings, columns=['userId', 'bookId', 'rating'])

allBooks = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/books/BX-Books-cleaned-final.csv', sep=";",  na_filter=False, encoding="latin1", escapechar='\\')
usersample = User(1, 23, 'Austria', 'JRR Tolkien', "Ravensburger", [1,7])
recsystem = Recommender()
searches = {}

@app.get("/")
async def read_root():
    return {"Hello": "Woadfrld"}

def takescore(elem):
    return elem[1]


def boost(recommendations, favs, searches, user):
    withind = list()
    for i, book in enumerate(recommendations):
        boostscore = 0
        for fav in favs:
            fb = books.bookshash[fav]
            if(fb.author == book.author or fb.publisher == book.publisher):
                boostscore += 200
        for search in searches:
            if(search in book.author or search in book.title or search in book.excerpt):
                boostscore += 200
        
        if book.author == user.favoriteAuthor or book.publisher == user.favoritePublisher:
            boostscore += 200

        withind.append([book, i+boostscore])
    withind.sort(key=takescore, reverse=True)
    return list(map(lambda x: x[0], withind))


@app.get("/recommend")
async def recommend(user_id: Optional[int] = Query(None, alias="userId"), item_id: Optional[str] = Query(None, alias="itemId"), number_of_items: Optional[int] = Query(10, alias="numberOfItems")) -> List[Book]:
    print(user_id, item_id, number_of_items)
    global allRatings
    global newUsers
    global searches

    if(user_id != None):
        try:
            result = []
            recs = []
            userSearches = []
            if user_id in searches.keys():
                userSearches = searches[user_id]

            if user_id in newUsers.keys():
                user = newUsers[user_id]
                user_ratings = allRatings.loc[allRatings["userId"] == str(user_id)]
                user_ratings_isbns = user_ratings.loc[user_ratings["rating"] > 2.0]["bookId"].tolist()
                
                if(len(user_ratings_isbns) >= 5):
                    print("cold start recommend")
                    recs = recsystem.cold_start_recommend(age=user.age, country=user.country, has_rated_items=user_ratings_isbns, n_items=number_of_items)
                else:
                    np.random.shuffle(books.booksMLPopular)
                    return books.booksMLPopular[:number_of_items]
            else:
                print("get for user recommend")
                recs = recsystem.get_for_user(user_id=user_id, n_items=number_of_items)

            user_data = None
            if user_id  in newUsers.keys():
                user_data = newUsers[user_id]
            else:
                user_data = users.usershash[str(user_id)]

            for rec in recs:
                result.append(books.bookshash[rec])
            result = boost(result,allFavorites[str(user_id)],userSearches, user_data)
            return result
        except Exception as error:
            print("big fail", error)

    if(item_id != None):
        try:
            result = []
            recs = recsystem.get_similar_items(item_id=item_id, n_items=number_of_items)
            for rec in recs:
                result.append(books.bookshash[rec])
            
            print("rec similar items")
            return result
        except Exception as error:
            print("big fail", error)
    

    print("fallback ml popular recommend")
    np.random.shuffle(books.booksMLPopular)
    return books.booksMLPopular[:number_of_items]

@app.get("/recommendItems", response_model=List[str])
async def recommend_items(
    age: Optional[int] = Query(None, alias="age", ge=5, le=100),
    user_id: Optional[int] = Query(None, alias="userId"),
    location_country: Optional[str] = Query(None, alias="locationCountry"),
    location_state: Optional[str] = Query(None, alias="locationState", deprecated=True),
    location_city: Optional[str] = Query(None, alias="locationCity", deprecated=True),
    item_id: Optional[str] = Query(None, alias="itemId"),
    number_of_items: Optional[int] = Query(10, alias="numberOfItems"),
) -> List[int]:

    recommendations = []
    if(user_id != None or item_id != None):
        print("self /recommend")
        recommendations = await recommend(user_id=user_id, item_id=item_id, number_of_items=number_of_items)

    elif((age <= 100 and age >= 5) and location_country != None):
        print("cold start recommend")
        recs = recsystem.cold_start_recommend(age=age, country=location_country, n_items=number_of_items)
        for rec in recs:
            recommendations.append(books.bookshash[rec])
    else:
        print("baseline recommend")
        recommendations = books.booksMLPopular[:number_of_items]

    print(recommendations, "recs")
    return list(map(lambda x: x.bookId, recommendations))


@app.get("/search", response_model=List[Book])
async def search(
    searchTerm: Optional[str] = Query(None, alias="searchTerm"),
    userId: Optional[int] = Query(None, alias="userId")
) -> Union[List[Book], ErrorMessage]:

    if(searchTerm == None):
        raise HTTPException(status_code=404, detail="Search string empty.")

    if(not(searchTerm.strip())):
        raise HTTPException(status_code=404, detail="Search string empty.")

    results = es.search(index="books", size=30, query={"multi_match": {
      "fields":  [ "excerpt^3", "title^5", "author^1" ],
      "query":     searchTerm.strip(),
      "fuzziness": "2.0" 
    }})
    
    nr_results = results.body["hits"]["total"]["value"]

    if nr_results == 0:
        return ErrorMessage(description="No matching books found.")

    hits = results.body["hits"]["hits"]
    books_result = []

    for book in hits:
        book_s = book["_source"]
        books_result.append(Book(book_s["isbn"], book_s["title"], book_s["author"], book_s["publisher"], int(book_s["year"]), book_s["cover"] ))
        print(book["_source"]["title"])
    if userId in searches.keys():
        searches[userId].append(searchTerm)
    else:
        searches[userId] = [searchTerm]
    return books_result[:12]

@app.post("/user", response_model=User)
async def new_user(body: User) -> User:
    global newUserIds
    global newUsers

    newid = 0
    if len(newUserIds) == 0:
        newid = users.maxuid+1
    else:
        newid = newUserIds[len(newUserIds)-1]+1

    body.userId = newid
    newUserIds.append(newid)
    print(f"\"{newid}\";\"{body.age}\";\"\";\"\";\"{body.country}\"")
    newUsers[newid] = body
    return body

@app.get("/user/{user_id}", response_model=User)
async def get_existing_user(
    user_id: str = Path(..., alias="user_id")
) -> User:
    for user in users.users:
        if user.userId == user_id:
            return user
    if int(user_id) in newUsers.keys():
        return newUsers[user_id]
    
    raise HTTPException("User not found.")

@app.get("/books/{book_id}", response_model=BookDetails)
async def book_detail(book_id: str = Path(..., alias="book_id")) -> BookDetails:

    if len(str(book_id)) == 9:
        book_id = '0' + str(book_id)
    elif len(str(book_id)) == 8:
        book_id = '00' + str(book_id)
    
    return list(filter(lambda book: book.bookId == book_id, books.books))[0]

@app.get("/ratings/{user_id}", response_model=List[Rating])
async def get_ratings(user_id: str = Path(..., alias="user_id")) -> List[Rating]:
    global allRatings

    if(allRatings.empty == False):
        ratings = pd.DataFrame()
        ratings = allRatings.loc[allRatings["userId"] == str(user_id)]
        ratings = list(map(lambda x: Rating(x[0], x[1], x[2]), ratings.values.tolist()))
        return ratings
    return []

@app.post("/ratings")
async def rate_book(body: Rating) -> List[Rating]:
    global allRatings

    newRow = {'userId': body.userId, 'bookId': body.bookId, 'rating': body.rating}

    ratings =  allRatings.loc[allRatings["userId"] == body.userId]
    if body.bookId in ratings["bookId"].values:
        index = ratings.index[ratings["bookId"] == body.bookId].tolist()
        allRatings.at[index[0], "rating"] = [body.rating]
    else:
        allRatings = allRatings.append(newRow, ignore_index=True)

    ratings = allRatings.loc[allRatings["userId"] == body.userId]
    
    return list(map(lambda x: Rating(x[0], x[1], x[2]), ratings.values.tolist()))


@app.get("/favorites/{user_id}", response_model=List[Book])
async def get_favorites(user_id: str = Path(..., alias="user_id")) -> List[Book]:
    favorites = []

    if user_id in allFavorites:
        user_favorites = allFavorites[user_id]
        favorites = list(filter(lambda book: book.bookId in user_favorites , books.books))
    
    return favorites

@app.post("/favorites/")
async def add_favorites(body: Favorite) -> List[Book]:
    allFavorites[body.userId].append(body.bookId)
    return list(filter(lambda book: book.bookId in allFavorites[body.userId] , books.books))

@app.post("/removefavorite")
async def deleteFavorite(body: Favorite)  -> List[Book]:
    allFavorites[body.userId].remove(body.bookId)
    return list(filter(lambda book: book.bookId in allFavorites[body.userId] , books.books))