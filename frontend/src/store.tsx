import create from 'zustand'
import { Book } from './types/Book'
import { Rating } from './types/Rating'
import { User } from './types/User'

interface BookommenderState {
  books: Book[]
  similarBooks: Book[]
  user?: User
  favorites: Book[]
  ratings: Rating[]
  searchQuery: string
  searchResults: Book[]
  isLoading: boolean
  shouldRefetch: boolean
  addFavorite: (book: Book) => void
  removeFavorite: (id: string) => void
  setUser: (user?: User) => void
  setBooks: (books: Book[]) => void
  setSimilarBooks: (books: Book[]) => void
  setSearchQuery: (query: string) => void
  setFavorites: (favs: Book[]) => void
  setRatings: (ratings: Rating[]) => void
  setSearchResults: (results: Book[]) => void
  setIsLoading: (value: boolean) => void
  setShouldRefetch: (value: boolean) => void
}

export const useStore = create<BookommenderState>(set => ({
  // initial state
  books: [],
  similarBooks: [],
  searchResults: [],
  user: undefined,
  favorites: [],
  searchQuery: '',
  ratings: [],
  isLoading: false,
  shouldRefetch: false,
  // methods for manipulating state
  setUser: (newUser?: User) => {
    set(_ => ({
      user: newUser,
    }))
  },
  setBooks: (books: Book[]) => {
    set(_ => ({
      books: books,
    }))
  },
  setSimilarBooks: (books: Book[]) => {
    set(_ => ({
      similarBooks: books,
    }))
  },
  setFavorites: (favs: Book[]) => {
    set(_ => ({
      favorites: favs,
    }))
  },
  setSearchQuery: (query: string) => {
    set(_ => ({
      searchQuery: query,
    }))
  },
  setRatings: (ratings: Rating[]) => {
    set(_ => ({
      ratings: ratings,
    }))
  },
  addRating: (rating: Rating) => {
    set(state => ({
      ratings: [...state.ratings, rating],
    }))
  },
  removeRating: (rating: Rating) => {
    set(state => ({
      ratings: state.ratings.filter(r => rating !== r),
    }))
  },
  setSearchResults: (results: Book[]) => {
    set(_ => ({
      searchResults: results,
    }))
  },
  addFavorite: (book: Book) => {
    set(state => ({
      favorites: [...state.favorites, book],
    }))
  },
  removeFavorite: id => {
    set(state => ({
      favorites: state.favorites.filter(book => book.bookId !== id),
    }))
  },
  setIsLoading: (value: boolean) => {
    set(_ => ({
      isLoading: value,
    }))
  },
  setShouldRefetch: (value: boolean) => {
    set(_ => ({
      shouldRefetch: value,
    }))
  },
}))
