# Bookommender

## Team

- Lena Ebner
- Ismail Halili
- Stefan Maier
- Tabea Schaeffer

## Content

- [Frontend](./frontend)
- [Backend](./backend)
- [Data](./data)
- [Data Exploration](./data-exploration)
- [Recommender](./recommender)
- [Konzept](./concept)
- [Evaluation](./evaluation/)

You can find more detailed information to each directory in the `README.md` of each directory.

## Get Started

- run `yarn start:docker`
- to setup elasticsearch run everything in `./backend/elasticsearch_setup.ipynb` once (necessary for search)

## Features

- Login
  - as new User
  - as existing User (e.g. 276762)
- Book Overview with recommended Books
  - Most and Least Popular for Cold Start Problem
  - Recommendations user-based
- Book Details
  - also contains additional book data from extending it via OpenLibrary
  - Recommendations item-based
- Favorites
- Book Ratings
- Search for a specific book
  - uses Elatiscsearch

## Endpoint /recommendItems

Provide either:

- **userId**: uses the FM recommend method
- **itemId**: uses the FM similiarItems method
- **age (>=5, <=100) and locationCountry**: uses similar users and FM recommendations
- **fallback**: returns items from our most and least popular baseline

Endpoint Swagger UI: http://localhost:8055/docs#/default/recommend_items_recommendItems_get

Supported Users: all users ids from the `BX-Book-Ratings-cleaned.csv` are supported.

## Evaluation

The Evaluation can be found [Evaluation](./evaluation/) directory.

## Recommender

Can be found in [Recommender](./recommender/recommender.py)
