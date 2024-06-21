import { useEffect, useRef } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { API_URL, SEARCH_ENDPOINT } from '../../contants/contants'
import { useStore } from '../../store'
import { Book } from '../../types/Book'
import './Header.css'

export default function Header() {
  const { setSearchResults, setSearchQuery, searchQuery, user } = useStore()
  const inputRef: any = useRef(null)

  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    if (searchQuery == '' && inputRef.current) {
      inputRef.current.value = ''
    }
  }, [searchQuery])

  const handleKeyDown = (event: any) => {
    if (event.key === 'Enter') {
      if (event.target.value.trim() != '') {
        search(event.target.value.trim())
      } else {
        resetSearch()
      }
    }
  }

  const handleClick = () => {
    if (inputRef.current.value.trim() != '') {
      search(inputRef.current.value.trim())
    } else {
      resetSearch()
    }
  }

  const resetSearch = () => {
    setSearchQuery('')
    setSearchResults([])
  }

  const search = (queryString: string) => {
    setSearchQuery(queryString)

    if (location.pathname != '/home') {
      navigate('/home')
    }

    let url = new URL(`${API_URL}/${SEARCH_ENDPOINT}`)
    url.searchParams.set('searchTerm', queryString)
    if (user) {
      url.searchParams.set('userId', user.userId)
    }
    fetch(url.toString(), {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(r => r.json())
      .then(r => {
        setSearchResults(r as Book[])
      })
  }

  return (
    <header className="header z-50">
      <div className="leftWrapper">
        <div onClick={() => navigate('/home')} className="cursor-pointer">
          <img src="/Bookommender_Logo.png" className="imgLogo"></img>
        </div>
        {user && (
          <div
            onClick={() => navigate('/home')}
            className={`link ${
              location.pathname == '/home' && 'active'
            } cursor-pointer`}
          >
            ALL
          </div>
        )}

        {user && (
          <div
            onClick={() => navigate('/favorites')}
            className={`link ${
              location.pathname == '/favorites' && 'active'
            } cursor-pointer`}
          >
            FAVS
          </div>
        )}
      </div>
      <div className="rightWrapper">
        {user && (
          <div className="searchWrapper">
            <img
              onClick={handleClick}
              src="/iconSearch.svg"
              className="iconSearch"
            ></img>
            <input
              type="text"
              defaultValue={searchQuery}
              ref={inputRef}
              onKeyDown={handleKeyDown}
              className="placeholder:italic placeholder:text-slate-400 block bg-white w-full border border-slate-300 rounded-md py-2 pl-3 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1 md:text-md"
              placeholder="Search for anything..."
              name="search"
            ></input>
          </div>
        )}
        {user && (
          <a href="/">
            <img src="/iconUser.svg" className="iconUser"></img>
          </a>
        )}
      </div>
    </header>
  )
}
