//eval precision recall
//keywords -> jacard alle bücher vom user in einen Datensatz komprimieren, alle item similarities in zu jedem item 10 meist similarities speichern in dict
//most-popular ->

import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authors } from '../contants/authors'
import { API_URL, USER_ENDPOINT } from '../contants/contants'
import { countries } from '../contants/countries'
import { publishers } from '../contants/publishers'
import { useStore } from '../store'
import { User } from '../types/User'

export default function Login() {
  const navigate = useNavigate()
  const { setUser, user } = useStore()

  const [fakeId, setFakeId] = useState<number>()
  const [age, setAge] = useState<number>()
  const [country, setCountry] = useState<string>()
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const [fakeErrorMsg, setFakeErrorMsg] = useState<string | null>(null)
  const [author, setAuthor] = useState<any>(null)
  const [publisher, setPublisher] = useState<any>(null)

  useEffect(() => {
    let storageUser = localStorage.getItem('user')
    if (storageUser) {
      const { age, country, favoriteAuthor, favoritePublisher, userId } =
        JSON.parse(storageUser)

      const lsUser = {
        userId,
        age,
        country,
        favoriteAuthor,
        favoritePublisher,
      }

      setUser(lsUser)
    }
  }, [])

  const fakeUser = () => {
    if (fakeId) {
      console.log('fake')
      setFakeErrorMsg(null)
      fetch(`${API_URL}/${USER_ENDPOINT}/${fakeId}`)
        .then(r => r.json())
        .then(r => {
          localStorage.setItem('user', JSON.stringify(r))
          setUser(r as User)
          navigate('/home')
        })
        .catch(error => {
          console.log(error)
          setFakeErrorMsg(
            'Fake ID not preset in users. Try another one instead.'
          )
        })
    }
  }

  const Logout = () => {
    localStorage.removeItem('user')
    localStorage.setItem('favorites', JSON.stringify([]))
    localStorage.setItem('ratings', JSON.stringify([]))
    setUser(undefined)
  }

  const trySubmit = () => {
    if (!(age && age >= 5 && age <= 100)) {
      setErrorMsg('Age not valid: must be between 5 and 100')
      return
    }

    if (!country) {
      setErrorMsg('Country not valid: country must be selected')
      return
    }

    fetch(`${API_URL}/${USER_ENDPOINT}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        age,
        country,
        userId: 0,
        favoriteAuthor: author,
        favoritePublisher: publisher,
        favorites: [],
      }),
    })
      .then(r => r.json())
      .then(r => {
        localStorage.setItem('user', JSON.stringify(r))
        setUser(r as User)
        navigate('/home')
      })
  }

  if (user) {
    return (
      <main className="w-full pl-8 pr-8 flex-col justify-center items-center ">
        <div className="w-[60vw] mt-24 center ">
          <h2 className="text-3xl mb-8 text-left">Profile</h2>
          <div className="ml-4 mb-4">
            <p>Age: {user?.age}</p>
            <p>
              {`Country: 
              ${
                user.country.toUpperCase().slice(0, 1) +
                user.country.toLowerCase().slice(1)
              }`}
            </p>

            {user?.favoriteAuthor && (
              <p>Favourite Author:{user?.favoriteAuthor} </p>
            )}
            {user?.favoritePublisher && (
              <p>Favourite Publisher:{user?.favoritePublisher} </p>
            )}
          </div>
          <button className="bigbutton mb-3 mt-3" onClick={Logout}>
            Logout
          </button>
        </div>
      </main>
    )
  }
  return (
    <main className="w-full pl-8 pr-8 flex-col justify-start items-center ">
      <div className="w-[60vw] mt-24 ">
        <h2 className="text-4xl mb-16 text-left">Welcome</h2>
        <form className="flex flex-col gap-3 mb-8 ml-2">
          <div className="grid grid-cols-2 grid-flow-row grid-cols-[6fr_3fr] items-center max-w-screen-md">
            <label>Enter your age:*</label>
            <input
              defaultValue={age}
              onChange={(e: any) => setAge(parseInt(e.target.value))}
              className="inputfield w-30 px-3 py-1 placeholder-gray-400 rounded-sm "
              name="age"
              type="number"
              min="5"
              max="100"
            ></input>
          </div>

          <div className="grid grid-cols-2 grid-flow-row grid-cols-[6fr_3fr] items-center max-w-screen-md">
            <label>Enter your country:*</label>
            <select
              id="country"
              className="inputfield w-full px-3 py-1 rounded-sm hover:bg-slate-200 focus:bg-slate-200 active:bg-slate-100"
              onChange={e => setCountry(e.target.value)}
            >
              <option value="">Choose a country</option>
              {countries
                .sort((a, b) => {
                  if (a < b) return -1
                  else return 1
                })
                .map(country => (
                  <option key={country} value={country} title={country}>
                    {country.toUpperCase().slice(0, 1) +
                      country.toLowerCase().slice(1, 20)}
                  </option>
                ))}
            </select>
          </div>
          <div className="grid grid-cols-2 grid-flow-row grid-cols-[6fr_3fr] items-center max-w-screen-md">
            <label>Enter your favourite author:</label>
            <select
              id="author"
              className="inputfield w-full px-3 py-1 rounded-sm hover:bg-slate-200 focus:bg-slate-200 active:bg-slate-100"
              onChange={e => setAuthor(e.target.value)}
            >
              <option>Choose an author</option>
              {authors.map(author => (
                <option key={author} value={author} title={author}>
                  {author.slice(0, 20)}
                </option>
              ))}
            </select>
          </div>
          <div className="grid grid-cols-2 grid-flow-row grid-cols-[6fr_3fr] items-center max-w-screen-md">
            <label>Enter your favourite publisher:</label>
            <select
              id="publisher"
              className="inputfield w-full px-3 py-1 rounded-sm hover:bg-slate-200 focus:bg-slate-200 active:bg-slate-100"
              defaultValue="publisher"
              onChange={e => setPublisher(e.target.value)}
            >
              <option>Choose a publisher</option>
              {publishers.map(publisher => (
                <option key={publisher} value={publisher} title={publisher}>
                  {publisher.slice(0, 20)}
                </option>
              ))}
            </select>
          </div>
          {errorMsg && (
            <div className="text-md text-left text-red-500 ">{errorMsg}</div>
          )}
        </form>

        <button className="bigbutton ml-2" onClick={trySubmit}>
          Login
        </button>
      </div>
      <div className="w-[60vw] mt-24 mx-auto center ml-2">
        <h3 className="text-2xl text-left">Fake User</h3>
        <form className="flex flex-col gap-3  mt-4 mb-4">
          <div className="grid grid-cols-2 grid-flow-row grid-cols-[6fr_3fr] items-center max-w-screen-md">
            <label>Enter your UserId:</label>
            <input
              min="1"
              onChange={(e: any) => setFakeId(parseInt(e.target.value))}
              className="inputfield w-30 px-3 py-1 placeholder-gray-400 rounded-sm "
              name="age"
              type="number"
            ></input>
          </div>
          {fakeErrorMsg && (
            <div className="text-md text-left text-red-500 ">
              {fakeErrorMsg}
            </div>
          )}
        </form>
        <button className="bigbutton" onClick={fakeUser}>
          Login as fake user
        </button>
      </div>
    </main>
  )
}
