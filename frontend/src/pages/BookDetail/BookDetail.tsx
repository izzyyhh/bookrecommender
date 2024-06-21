import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import RatingStars from '../../components/RatingStars'
import {
  API_URL,
  BOOKS_ENDPOINT,
  FAVORITES_ENDPOINT,
  RECOMMEND_ENDPOINT,
  REMOVE_FAVORITE_ENDPOINT,
} from '../../contants/contants'
import '../../index.css'
import { useStore } from '../../store'
import { Book } from '../../types/Book'
import { Rating } from '../../types/Rating'
import { User } from '../../types/User'
import './BookDetail.css'

export default function BookDetail() {
  const navigate = useNavigate()
  const params = useParams()
  const {
    setUser,
    user,
    similarBooks,
    setSimilarBooks,
    favorites,
    removeFavorite,
    setFavorites,
    addFavorite,
    setRatings,
    ratings,
  } = useStore()

  const [book, setBook] = useState<Book>()
  const [rating, setRating] = useState<Rating | undefined>()
  const { bookId } = params

  useEffect(() => {
    if (!user) {
      const lsUser = localStorage.getItem('user')

      if (!lsUser) {
        navigate('/')
        return
      }
      setUser(JSON.parse(lsUser) as User)
    }

    if (bookId) {
      fetchSimilarBooks(bookId)
      fetchBook(bookId)
      const rating = ratings.find((e: any) => e.bookId == bookId)
      setRating(rating)
    }
  }, [bookId])

  useEffect(() => {
    const favs = JSON.parse(localStorage.getItem('favorites') || '[]') || []
    setFavorites(favs)

    const user_ratings =
      JSON.parse(localStorage.getItem('ratings') || '[]') || []
    setRatings(user_ratings)
  }, [])

  useEffect(() => {
    const rating = ratings.find((e: any) => e.bookId == bookId)
    setRating(rating)
  }, [ratings])

  useEffect(() => {
    if (user?.userId) {
      getFavorites()
    }
  }, [user])

  const changeBook = (bookId: string) => {
    navigate(`/detail/${bookId}`)
  }

  const fetchBook = (bookId: string) => {
    fetch(`${API_URL}/${BOOKS_ENDPOINT}/${bookId}`)
      .then(r => r.json())
      .then(b => {
        setBook(b as Book)
      })
  }

  const fetchSimilarBooks = (bookId: string) => {
    let url = new URL(`${API_URL}/${RECOMMEND_ENDPOINT}/`)
    if (bookId) {
      url.searchParams.set('itemId', bookId)
    }

    fetch(url.toString())
      .then(r => r.json())
      .then(b => {
        setSimilarBooks(b)
      })
  }

  function getFavorites() {
    fetch(`${API_URL}/${FAVORITES_ENDPOINT}/${user?.userId}`)
      .then(r => r.json())
      .then(b => {
        localStorage.setItem('favorites', JSON.stringify(b))
        setFavorites(b as Book[])
      })
  }

  const toggleFavorite = () => {
    if (!book) return

    const endPoint = !favorites.find((e: Book) => e.bookId == book?.bookId)
      ? FAVORITES_ENDPOINT
      : REMOVE_FAVORITE_ENDPOINT

    fetch(`${API_URL}/${endPoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId: user?.userId,
        bookId: book?.bookId,
      }),
    })
      .then(r => r.json())
      .then(r => {
        endPoint == FAVORITES_ENDPOINT
          ? addFavorite(book)
          : removeFavorite(book.bookId)

        localStorage.setItem('favorites', JSON.stringify(favorites))
      })
  }

  const recommendedBooks: Book[] = similarBooks.slice(0, 8)

  return (
    <main className="pt-20 pb-10 w-full max-w-full min-w-full">
      <div className="grid grid-cols-2 grid-flow-row grid-cols-[5fr_3fr] gap-x-2">
        <div className="">
          <img
            onClick={() => navigate(-1)}
            className="backArrow mt-5 ml-10"
            src="/arrowBack.svg"
          ></img>
          <div className="mt-2 ml-20 pl-10 flex flex-col">
            <h2 className="text-2xl font-bold max-w-xl">{book?.title}</h2>
            <div className="mt-2">
              <RatingStars rating={rating} book={book} />
            </div>
            <div className="flex flex-row items-center gap-6 justify-between max-w-xl">
              <div>
                <p className="text-left text-xl mt-4">Author: {book?.author}</p>
                <p className="text-xl max-w-xl mt-1">
                  Publisher: {book?.publisher}
                </p>
                {!!book?.pages && book.pages > 0 && (
                  <p className="text-xl max-w-xl mt-1">Pages: {book?.pages}</p>
                )}
              </div>
              <button
                type="button"
                className="px-6 py-2.5 mr-20 bg-primary text-white font-medium text-xs leading-tight uppercase rounded-full shadow-md "
                onClick={toggleFavorite}
              >
                {favorites.find(
                  (e: { bookId: string | undefined }) =>
                    e.bookId == book?.bookId
                )
                  ? 'Unfavorite'
                  : 'Favorit'}
              </button>
            </div>
            <div className="flex flex-row justify-start w-full">
              <img className="h-auto w-72 mt-4" src={book?.cover} />
            </div>
            <p className="text-l max-w-xl mt-2 mb-2">{book?.excerpt}</p>
            {!!book?.tags &&
              book?.tags.length > 0 &&
              book?.tags[0].length > 0 && (
                <div className="w-3/5">
                  <div className="flex flex-row flex-wrap justify-start gap-1">
                    {book.tags.slice(0, 15).map(tag => (
                      <span className="mt-1 px-3 py-1 rounded-full text-gray-500 bg-gray-200 font-semibold text-xs flex align-center w-max cursor-pointer active:bg-gray-300">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
          </div>
        </div>
        <div className="mt-2">
          <h2 className="text-lg text-left font-semibold">
            Recommended for you
          </h2>
          <div className="flex flex-col mt-2 ml-2">
            {recommendedBooks.map((element: Book) => (
              <div
                key={element.bookId}
                onClick={() => changeBook(element.bookId)}
                className="flex flex-row items-center m-3 cursor-pointer"
              >
                <div className="w-14">
                  <img
                    className="max-w-full h-full w-full"
                    src={element.cover}
                  ></img>
                </div>
                <div className="ml-5 text-left">
                  <p className="bookTitleWidth text-md break-words text-black max-w-xs ">
                    {element.title}
                  </p>
                  <p className="flex-nowrap text-black text-xs">
                    {element.author} - {element.year}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  )
}
