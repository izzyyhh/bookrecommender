import { useNavigate } from 'react-router-dom'
import {
  API_URL,
  FAVORITES_ENDPOINT,
  REMOVE_FAVORITE_ENDPOINT,
} from '../../contants/contants'
import { useStore } from '../../store'
import RatingStars from '../RatingStars'

import './BookItem.css'

export default function BookItem({ book, rating, isFavorite }: any) {
  const { user, favorites, removeFavorite, addFavorite } = useStore()
  const navigate = useNavigate()
  const toggleFavorite = () => {
    if (!book) return

    const endPoint = !isFavorite ? FAVORITES_ENDPOINT : REMOVE_FAVORITE_ENDPOINT

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

  return (
    <div className="box flex flex-col justify-center pl-2 pr-2">
      <div
        onClick={() => navigate(`/detail/${book.bookId}`)}
        className="cursor-pointer"
      >
        <p className="mr-8 text-left font-bold whitespace-nowrap truncate">
          {book.title}
        </p>
        <p className="author">
          {book.author} - {book.year}
        </p>
      </div>
      <img
        onClick={toggleFavorite}
        className="heartIcon"
        src={isFavorite ? 'heartFill.svg' : 'heartOutline.svg'}
        alt="Heart Icon"
      ></img>
      <img className="coverIcon mt-2" src={book.cover} alt={book.title}></img>
      <RatingStars rating={rating} book={book} />
    </div>
  )
}
