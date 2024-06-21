import { Book } from './Book'

export type User = {
  userId: string
  age: number
  country: string
  favoriteAuthor?: string
  favoritePublisher?: string
  favorites?: Book[]
}
