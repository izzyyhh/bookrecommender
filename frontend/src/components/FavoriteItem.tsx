import { useEffect, useState } from 'react'
import {
  API_URL,
  FAVORITES_ENDPOINT,
  REMOVE_FAVORITE_ENDPOINT,
} from '../contants/contants'
import { useStore } from '../store'

export default function favoriteItem({ book, favorite, getFavorites }: any) {
  let [isFavorite, setIsFavorite] = useState<boolean>(favorite)
  const { user, setFavorites } = useStore()

  useEffect(() => {
    setIsFavorite(favorite)
  }, [favorite])

  function handleClickFavorite(e: any) {
    if (!isFavorite) {
      fetch(`${API_URL}/${FAVORITES_ENDPOINT}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: user?.userId,
          bookId: book.bookId,
        }),
      })
        .then(r => r.json())
        .then(r => {
          setIsFavorite(true)
          setFavorites(r)
          localStorage.setItem('favorites', JSON.stringify(r))
        })
    } else {
      fetch(`${API_URL}/${REMOVE_FAVORITE_ENDPOINT}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: user?.userId,
          bookId: book.bookId,
        }),
      })
        .then(r => r.json())
        .then(r => {
          setIsFavorite(false)
          setFavorites(r)
          localStorage.setItem('favorites', JSON.stringify(r))
        })
    }
  }
  return (
    <div className="box flex flex-col justify-center pl-2 pr-2">
      <a href={`/detail/` + book.bookId}>
        <p className="text-left font-bold whitespace-nowrap truncate">
          {book.title}
        </p>
        <p className="author">
          {book.author} - {book.year}
        </p>
      </a>

      <img className="coverIcon mt-2" src={book.cover}></img>
      <img
        onClick={handleClickFavorite}
        className="mt-2 mb-1 self-center"
        src={isFavorite ? 'heartFill.svg' : 'heartOutline.svg'}
      ></img>
    </div>
  )
}
