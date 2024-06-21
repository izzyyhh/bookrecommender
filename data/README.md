# Bookommender - Data

## User

Contains the users. Note that user IDs (`User-ID`) have been anonymized and map to integers. Demographic data is provided (`Location`, `Age`) if available. Otherwise, these fields contain NULL-values.

## Books

Books are identified by their respective ISBN. Invalid ISBNs have already been removed from the dataset. Moreover, some content-based information is given (`Book-Title`, `Book-Author`, `Year-Of-Publication`, `Publisher`), obtained from Amazon Web Services. Note that in case of several authors, only the first is provided. URLs linking to cover images are also given, appearing in three different flavours (`Image-URL-S`, `Image-URL-M`, `Image-URL-L`), i.e., small, medium, large. These URLs point to the Amazon web site.

## Ratings

Contains the book rating information. Ratings (`Book-Rating`) are either explicit, expressed on a scale from 1-10 (higher values denoting higher appreciation), or implicit, expressed by 0

## Cleaning Data

Code: [clean-data.ipynb](./clean-data.ipynb)

### Users

From 278858 to 167723 users.

- Remove all user where age is Null
- Remove all user where 5 > age > 100: [BX-User-cleaned.ipynb](./BX-User-cleaned.csv)

Final user data cleaned is: [BX-User-cleaned.csv](./BX-User-cleaned.csv)

### Books

From 271379 to 228643 (cleaned) to 228144 (cleaned-final) books.

1. Merge books with same title and author and same year: [BX-Books-cleaned-tmp.ipynb](./BX-Books-cleaned-tmp.csv)
2. Merge books with same title and author to latest year: [BX-Books-cleaned.ipynb](./BX-Books-cleaned.csv)
3. Remove bad characters from Title, Author and Publisher & merge books with same title and author to latest year: [BX-Books-cleaned-final.csv](./BX-Books-cleaned-final.csv)
4. Remove bad characters from Title, Author, Publisher
5. Set Publication Year to between 1800-2025, otherwise average year.
6. Clean Excerpt and Tags [BX-Books-cleaned-final-tags.csv](./BX-Books-cleaned-final-tags.csv)

Final book data cleaned and extended is: [BX-Books-cleaned-final-tags.csv](./BX-Books-cleaned-final-tags.csv)

### Ratings

From 1048574 to 656293 ratings (without 0: 235563).

1. Remove all ratings where user is not found: [BX-Book-Ratings-cleaned-tmp.csv](./BX-Book-Ratings-cleaned-tmp.csv)
2. Change isbn for books where isbn is not found because merged to another isbn in book cleaning: [./BX-Book-Ratings-cleaned.csv](BX-Book-Ratings-cleaned-final.csv)
3. Remove all 0 values (0 is implicit feedback): [BX-Book-Ratings-cleaned-without-0.csv](BX-Book-Ratings-cleaned-final-without-0.csv)

Final rating data cleaned is: [BX-Book-Ratings-cleaned.csv](BX-Book-Ratings-cleaned-final.csv)

## Extending Book Data

Code: [extend-data.ipynb](./extend-data.ipynb)

- Library used: **OpenLibrary** https://openlibrary.org/
- Extend book data with **Excerpt**, **Number of Pages**, **Tags** (Subjects), **Published Places**
  - Excerpt (string or empty string if not found)
  - Number Of Pages (Number or 0 if not found)
  - Publish Places (array of strings or empty array if not found)
  - Tags (array of strings or empty array if not found)
- [BX-Books-extended.csv](./BX-Books-extended.csv) is based on [BX-Books-cleaned.csv](./BX-Books-cleaned.csv)
- Final book data cleaned and extended is: [BX-Books-cleaned-final.csv](./BX-Books-cleaned-final.csv)
