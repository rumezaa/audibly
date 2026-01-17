import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import '../styles/Navbar.css'

function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const location = useLocation()

  const isActive = (path) => location.pathname === path

  return (
    <header className="navbar">
      <nav className="navbar-container">
        <Link to="/" className="navbar-logo">
          <svg className="logo-icon" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="20" r="18" stroke="currentColor" strokeWidth="2"/>
            <path d="M20 8C13.373 8 8 13.373 8 20s5.373 12 12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <path d="M20 12c-4.418 0-8 3.582-8 8s3.582 8 8 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <circle cx="20" cy="20" r="3" fill="currentColor"/>
          </svg>
          <span>Audibly</span>
        </Link>

        <button
          className={`navbar-toggle ${isOpen ? 'active' : ''}`}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle navigation"
          aria-expanded={isOpen}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <ul className={`navbar-menu ${isOpen ? 'active' : ''}`}>
          <li>
            <Link
              to="/"
              className={`navbar-link ${isActive('/') ? 'active' : ''}`}
              onClick={() => setIsOpen(false)}
            >
              Home
            </Link>
          </li>
          <li>
            <Link
              to="/features"
              className={`navbar-link ${isActive('/features') ? 'active' : ''}`}
              onClick={() => setIsOpen(false)}
            >
              Features
            </Link>
          </li>
          <li>
            <Link
              to="/download"
              className={`navbar-link ${isActive('/download') ? 'active' : ''}`}
              onClick={() => setIsOpen(false)}
            >
              Download
            </Link>
          </li>
          <li>
            <Link
              to="/about"
              className={`navbar-link ${isActive('/about') ? 'active' : ''}`}
              onClick={() => setIsOpen(false)}
            >
              About
            </Link>
          </li>
          <li className="navbar-cta">
            <Link
              to="/download"
              className="btn btn-primary btn-sm"
              onClick={() => setIsOpen(false)}
            >
              Get Started
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  )
}

export default Navbar
