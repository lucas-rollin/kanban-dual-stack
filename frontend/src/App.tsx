import { useState } from 'react'
import { Routes, Route, Link } from 'react-router'; 

const Home = () => <h3 className='text-accent'>Home Page!</h3>;
const About = () => <h3 className='text-secondary'>About Page?</h3>;

function App() {
  
  // Setup Django and FastAPI endpoint tests
  const [result, setResult] = useState<String>('No data fetched yet.');

  const endpoints = {
    django: new URL('http://127.0.0.1:8000/users/'),
    fastapi: new URL('http://127.0.0.1:8001/users/')
  }

  async function testEndpoint(endpoint: URL) {
    try {
      const res = await fetch(endpoint);

      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status} ${res.statusText}`);
      }
      const text = await res.text();
      setResult(text);
    } catch (error) {
      console.error(error);

      setResult(error instanceof Error? error.message: String(error))
    }

  }

  return (
    <>
      <main className='flex flex-col justify-center items-center h-dvh'>

        <h2 className='text-xl mb-12'>Test Backend Connection</h2>
        <section className='flex flex-col justify-center items-center gap-4'>
          <div className='space-x-4'>
            <button 
              onClick={() => testEndpoint(endpoints.django)}
              className='btn btn-primary'>
              Fetch Django
            </button>
            <button 
              onClick={() => testEndpoint(endpoints.fastapi)}
              className='btn btn-primary'>
              Fetch FastAPI
            </button>
          </div>
          <pre>
            {result}
          </pre>
        </section>

        <h2 className='text-xl mb-12 mt-32'>Test React Router</h2>
        <section className='space-y-4'>
          <nav>
            <Link className='link link-accent' to="/">Home</Link> | <Link className='link link-secondary' to="/about">About</Link>
          </nav>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </section>
      </main>
    </>
  )
}

export default App
