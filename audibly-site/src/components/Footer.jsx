import { Link } from 'react-router-dom'
import '../styles/Footer.css'

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-decoration">
        <svg className="footer-leaf footer-leaf-1" viewBox="0 0 60 60" fill="none">
          <path d="M30 5C15 5 5 20 5 35c0 10 8 20 25 20 5-15 5-35 0-50z" fill="currentColor" opacity="0.1"/>
        </svg>
        <svg className="footer-leaf footer-leaf-2" viewBox="0 0 60 60" fill="none">
          <path d="M30 5C15 5 5 20 5 35c0 10 8 20 25 20 5-15 5-35 0-50z" fill="currentColor" opacity="0.1"/>
        </svg>
      </div>

      <div className="container">
        <div className="footer-content">
          <div className="footer-brand">
            <Link to="/" className="footer-logo">
              <svg className="logo-icon" viewBox="0 0 40 40" fill="none">
                <circle cx="20" cy="20" r="18" stroke="currentColor" strokeWidth="2"/>
                <path d="M20 8C13.373 8 8 13.373 8 20s5.373 12 12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                <path d="M20 12c-4.418 0-8 3.582-8 8s3.582 8 8 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                <circle cx="20" cy="20" r="3" fill="currentColor"/>
              </svg>
              <span>Audibly</span>
            </Link>
            <p>Eliminating access bias in workplace meetings through inclusive technology.</p>
          </div>

          <nav className="footer-nav">
            <div className="footer-nav-group">
              <h4>Product</h4>
              <Link to="/features">Features</Link>
              <Link to="/download">Download</Link>
            </div>
            <div className="footer-nav-group">
              <h4>Company</h4>
              <Link to="/about">About Us</Link>
              <Link to="/about#team">Team</Link>
            </div>
          </nav>
        </div>

        <div className="footer-bottom">
          <p>Built for <strong>HackTheBias 2026</strong></p>
          <p>Creating meeting equity for every organization.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
