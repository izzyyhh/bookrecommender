export type Book = {
  bookId: string
  title: string
  publisher: string
  author: string
  cover: string
  year: number
  excerpt?: string
  tags?: string[]
  publishedPlaces?: string[]
  pages?: number
}
