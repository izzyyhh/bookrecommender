import { useEffect } from 'react'
import BookItem from '../../components/BookItem/BookItem'
import LoadingSpinner from '../../components/LoadingSpinner'
import {
  API_URL,
  FAVORITES_ENDPOINT,
  RATINGS_ENDPOINT,
  RECOMMEND_ENDPOINT,
} from '../../contants/contants'
import { useStore } from '../../store'
import { Book } from '../../types/Book'
import { Rating } from '../../types/Rating'
import { User } from '../../types/User'

export default function Home() {
  const {
    setUser,
    user,
    books,
    setBooks,
    favorites,
    setFavorites,
    ratings,
    setRatings,
    setSearchQuery,
    setSearchResults,
    searchResults,
    searchQuery,
    setIsLoading,
    isLoading,
    shouldRefetch,
    setShouldRefetch,
  } = useStore()

  useEffect(() => {
    const lsUser = JSON.parse(localStorage.getItem('user') || '')
    setUser(lsUser as User)

    const url = new URL(`${API_URL}/${RECOMMEND_ENDPOINT}/`)
    url.searchParams.set('userId', lsUser.userId)
    url.searchParams.set('numberOfItems', '80')

    if (books.length == 0) {
      if (!isLoading) {
        setIsLoading(true)

        fetch(url.toString())
          .then(r => r.json())
          .then(b => {
            setBooks(b as Book[])
            setIsLoading(false)
          })
      }
    }
  }, [])

  useEffect(() => {
    if (!user) return
    const url = new URL(`${API_URL}/${RECOMMEND_ENDPOINT}/`)
    url.searchParams.set('userId', user?.userId)
    url.searchParams.set('numberOfItems', '80')

    if (shouldRefetch && !isLoading) {
      setIsLoading(true)

      fetch(url.toString())
        .then(r => r.json())
        .then(b => {
          setBooks(b as Book[])
          setIsLoading(false)
          setShouldRefetch(false)
        })
    }
  }, [shouldRefetch])

  useEffect(() => {
    if (user?.userId && favorites.length == 0) {
      getFavorites()
    }
    if (user?.userId && ratings.length == 0) {
      getRatings()
    }
  }, [user])

  const getRatings = () => {
    fetch(`${API_URL}/${RATINGS_ENDPOINT}/${user?.userId}`)
      .then(r => r.json())
      .then(b => {
        b.forEach((item: { userId: any }) => {
          delete item.userId
        })
        localStorage.setItem('ratings', JSON.stringify(b))
        setRatings(b)
      })
  }

  const getFavorites = () => {
    fetch(`${API_URL}/${FAVORITES_ENDPOINT}/${user?.userId}`)
      .then(r => r.json())
      .then(b => {
        localStorage.setItem('favorites', JSON.stringify(b))
        setFavorites(b as Book[])
      })
  }

  const resetSearch = () => {
    setSearchResults([])
    setSearchQuery('')
  }

  return (
    <main className="w-full mt-16 pt-4 pl-8 pr-8 flex-col justify-start max-w-screen-2xl">
      {isLoading && <LoadingSpinner />}

      <>
        {searchQuery.length > 0 && (
          <div className="mb-4 flex-col justify-start">
            <div className="mb-4 flex flex-row justify-start gap-8 items-center">
              <h2 className="text-2xl text-left w-fit m-w-fit mr-0 font-bold">{`Search results for '${searchQuery}'`}</h2>
              <button
                className=" bg-primary text-white font-medium text-xs leading-tight uppercase rounded-full shadow-md "
                onClick={resetSearch}
              >
                Clear Search
              </button>
            </div>
            {searchResults.length > 0 ? (
              <div className="flex flex-row flex-wrap justify-between">
                {searchResults.map((element: Book) => (
                  <BookItem
                    key={element.bookId}
                    book={element}
                    rating={ratings.find(
                      (r: Rating) => r.bookId == element.bookId
                    )}
                    isFavorite={
                      favorites.findIndex(
                        (fav: Book) => fav.bookId == element.bookId
                      ) >= 0
                    }
                  />
                ))}
              </div>
            ) : (
              <div className="text-xl text-left mb-8 mt-2 ml-4">
                No matching books found.
              </div>
            )}
          </div>
        )}

        <div className="flex flex-col justify-center">
          <h2 className="text-2xl text-left font-bold">Recommended for you</h2>
          <div className="flex flex-row flex-wrap justify-between">
            {books.map((element: Book) => (
              <BookItem
                key={element.bookId}
                book={element}
                rating={ratings.find((r: Rating) => r.bookId == element.bookId)}
                isFavorite={
                  favorites.findIndex(
                    (fav: Book) => fav.bookId == element.bookId
                  ) >= 0
                }
              />
            ))}
          </div>
        </div>
      </>
    </main>
  )
}
