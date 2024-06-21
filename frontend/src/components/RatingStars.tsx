import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import {
  API_URL,
  RATINGS_ENDPOINT,
  RECOMMEND_ENDPOINT,
} from '../contants/contants'
import { useStore } from '../store'
import { Book } from '../types/Book'
import './BookItem/BookItem.css'

export default function RatingStars({ rating, book }: any) {
  const [val, setVal] = useState(0)
  const {
    user,
    setRatings,
    ratings,
    setBooks,
    setIsLoading,
    isLoading,
    setShouldRefetch,
  } = useStore()

  const location = useLocation()

  useEffect(() => {
    if (rating != undefined) {
      setVal(rating.rating)
    } else {
      setVal(0)
    }
  }, [rating])

  const rate = (newrating: any) => {
    fetch(`${API_URL}/${RATINGS_ENDPOINT}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        bookId: book.bookId,
        userId: user?.userId,
        rating: newrating,
      }),
    })
      .then(r => r.json())
      .then(r => {
        setVal(newrating)

        setRatings(r)
        localStorage.setItem('ratings', JSON.stringify(r))

        // do not block ui by immediately refetching all book recommendations
        if (location.pathname.includes('detail')) {
          setShouldRefetch(true)
          return
        }

        if (ratings.length >= 4 && user?.userId) {
          const url = new URL(`${API_URL}/${RECOMMEND_ENDPOINT}/`)
          url.searchParams.set('userId', user.userId)
          url.searchParams.set('numberOfItems', '80')

          if (!isLoading) {
            setShouldRefetch(false)
            setTimeout(() => setIsLoading(true), 500)

            fetch(url.toString())
              .then(r => r.json())
              .then(b => {
                setBooks(b as Book[])
                setIsLoading(false)
              })
          }
        }
      })
  }
  return (
    <div className="flex justify-center mt-2 max-w-fit self-center">
      {Array.from(Array(10)).map((e, i) => {
        if (i < val)
          return (
            <img
              key={i}
              className="starIcon cursor-pointer"
              src="/starFill.svg"
              onClick={e => rate(i + 1)}
            ></img>
          )
        return (
          <img
            key={i}
            className="starIcon cursor-pointer"
            src="/starOutline.svg"
            onClick={e => rate(i + 1)}
          ></img>
        )
      })}
    </div>
  )
}
