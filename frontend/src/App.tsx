import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import './App.css'
import Header from './components/Header/Header'
import BookDetail from './pages/BookDetail/BookDetail'
import Favorites from './pages/Favorites'
import Home from './pages/Home/Home'
import Login from './pages/Login'

function App() {
  return (
    <div className="w-full m-w-full min-h-screen overflow-x-hidden ">
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="home" element={<Home />} />
          <Route path="/detail/:bookId" element={<BookDetail />} />
          <Route path="/favorites" element={<Favorites />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
