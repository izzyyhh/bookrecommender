import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import FavoriteItem from '../components/FavoriteItem'
import { API_URL, FAVORITES_ENDPOINT } from '../contants/contants'
import '../index.css'
import { useStore } from '../store'
import { Book } from '../types/Book'
import { User } from '../types/User'

export default function Favorites() {
  const { favorites, setFavorites, user, setUser } = useStore()

  const navigate = useNavigate()

  useEffect(() => {
    if (!user) {
      const lsUser = localStorage.getItem('user')

      if (!lsUser) {
        navigate('/')
        return
      }
      setUser(JSON.parse(lsUser) as User)
    }
  }, [])

  useEffect(() => {
    if (user?.userId) {
      getFavorites()
    }
  }, [user])

  function getFavorites() {
    fetch(`${API_URL}/${FAVORITES_ENDPOINT}/${user?.userId}`)
      .then(r => r.json())
      .then(b => {
        localStorage.setItem('favorites', JSON.stringify(b))
        setFavorites(b as Book[])
      })
  }

  return (
    <div className="mt-20 mb-10 ml-8">
      <h2 className="text-2xl text-left">Your Favorites</h2>
      <div className="flex flex-row flex-wrap gap-4">
        {favorites.length > 0 ? (
          favorites.map((element: Book) => (
            <FavoriteItem
              key={element.bookId}
              book={element}
              favorite={
                favorites.findIndex(
                  (fav: Book) => fav.bookId == element.bookId
                ) >= 0
              }
              getFavorites={getFavorites}
            />
          ))
        ) : (
          <div className="text-md mt-4 text-left">
            You do not have any favorites yet. Press the heart icon on a book
            you like.
          </div>
        )}
      </div>
    </div>
  )
}
