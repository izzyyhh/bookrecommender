# Dependencies.

import os
import random
from collections import Counter

import pandas as pd

# Load Data.

books = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/BX-Books-cleaned-final.csv', sep=";",  na_filter=False, encoding="latin1", escapechar='\\')
ratings = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/BX-Book-Ratings-cleaned.csv', sep=";", converters = {'user': int, 'ISBN': str, 'rating': float}, encoding="CP1252")

# ----------------------------------
## Most Popular Books
# ----------------------------------

# sorting on basis of frequency of elements
sortedRatings = [item for items, c in Counter(ratings['isbn']).most_common()
                                      for item in [items] * c]

sortedRatings = list(dict.fromkeys(sortedRatings))

# get the average of the Ratings per Book
def getAverage(allRatings):
    sumOfRating = 0
    countRatings = 0
    for isbn in allRatings:
        rating = int(ratings.loc[[isbn]]["rating"])
        if rating > 0:
            countRatings += 1
            sumOfRating += rating
    return (sumOfRating / countRatings)

bestRatedBooks = []
for book in sortedRatings[:200]:
    allRatings = [i for i, x in enumerate(ratings["isbn"]) if x == book]
    average = getAverage(allRatings)
    bestRatedBooks.append({'isbn': book, 'averageRating': average})

# sort the average Ratings (best to least)
def get_rating(element):
    return element['averageRating']

bestRatedBooks.sort(key=get_rating, reverse=True)

def get_isbn(element):
    return element['isbn']

# Top n Books
mostPopularBooks = []
for entry in bestRatedBooks[:50]:
    mostPopularBooks.append(entry['isbn'])


# ----------------------------------
## Least Popular Books
# ----------------------------------

leastPopularBooks = list(set(books['ISBN']) - set(ratings['isbn']))
leastPopularBooks = random.sample(leastPopularBooks, 15)

# ----------------------------------
# Merge most and least Popular Books
# ----------------------------------

firstRecommendations =  leastPopularBooks + mostPopularBooks
random.shuffle(firstRecommendations)

for isbn in range(len(firstRecommendations)):
    if len(firstRecommendations[isbn]) == 9:
        firstRecommendations[isbn] = '0' + firstRecommendations[isbn]
    elif len(firstRecommendations[isbn]) == 8:
        firstRecommendations[isbn] = '00' + firstRecommendations[isbn]

# Save Books in MostPopular.csv file
books = pd.merge(pd.DataFrame(firstRecommendations, columns=['ISBN']), books)
books.to_csv("./backend/app/books/MostLeastPopular.csv", index=False)