import { Link } from 'react-router-dom'
import { Wave, Butterfly, Leaf, Circle } from '../components/Decorations'
import '../styles/Features.css'

function Features() {
  return (
    <div className="features-page">
      {/* Page Header */}
      <section className="page-header">
        <Circle className="header-circle" size={300} />
        <Butterfly className="header-butterfly" size={45} />

        <div className="container">
          <span className="section-badge">Enterprise Features</span>
          <h1>Built for the Modern Workplace</h1>
          <p>Professional-grade accessibility tools that integrate with your existing workflow.</p>
        </div>

        <Wave className="header-wave" />
      </section>

      {/* ASL Recognition */}
      <section className="section feature-section">
        <div className="container">
          <div className="feature-row">
            <div className="feature-content">
              <span className="feature-tag">Inclusive Communication</span>
              <h2>ASL Recognition for Meetings</h2>
              <p>
                Employees who use American Sign Language can actively participate in meetings
                without an interpreter present. Audibly's computer vision technology recognizes
                ASL gestures and converts them to text, enabling two-way communication in
                real-time.
              </p>
              <ul className="feature-list">
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Works with standard webcams—no specialized hardware
                </li>
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Supports common workplace vocabulary and phrases
                </li>
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Sub-second latency for natural conversation flow
                </li>
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Compatible with Zoom, Teams, Meet, and more
                </li>
              </ul>
            </div>
            <div className="feature-visual">
              <div className="feature-icon-wrapper gradient-blue">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <circle cx="12" cy="16" r="1"/>
                </svg>
              </div>
              <Leaf className="feature-leaf" size={70} />
            </div>
          </div>
        </div>
      </section>

      {/* Speech-to-Text */}
      <section className="section section-alt feature-section">
        <Wave className="section-wave-top" flip />

        <div className="container">
          <div className="feature-row reverse">
            <div className="feature-content">
              <span className="feature-tag">Real-Time Transcription</span>
              <h2>Accurate Speech-to-Text</h2>
              <p>
                Audibly captures audio from any application on your workstation and transcribes
                it with enterprise-grade accuracy. Meeting discussions, training videos, webinars—
                everything becomes accessible.
              </p>
              <ul className="feature-list">
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  System-wide audio capture across all applications
                </li>
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Speaker identification for multi-person meetings
                </li>
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Industry terminology and proper noun recognition
                </li>
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Automatic punctuation and formatting
                </li>
              </ul>
            </div>
            <div className="feature-visual">
              <div className="feature-icon-wrapper gradient-grapefruit">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                  <line x1="12" y1="19" x2="12" y2="23"/>
                  <line x1="8" y1="23" x2="16" y2="23"/>
                </svg>
              </div>
              <Butterfly className="feature-butterfly" size={50} />
            </div>
          </div>
        </div>

        <Wave className="section-wave-bottom" />
      </section>

      {/* Translation */}
      <section className="section feature-section">
        <div className="container">
          <div className="feature-row">
            <div className="feature-content">
              <span className="feature-tag">Global Teams</span>
              <h2>Multi-Language Support</h2>
              <p>
                For organizations with international teams, Audibly can translate captions
                into the employee's preferred language. Reduce language barriers and ensure
                consistent understanding across your global workforce.
              </p>
              <ul className="feature-list">
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Support for major business languages
                </li>
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Real-time translation with minimal delay
                </li>
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Preserves technical terminology and context
                </li>
                <li>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Configurable per-user language preferences
                </li>
              </ul>
            </div>
            <div className="feature-visual">
              <div className="feature-icon-wrapper gradient-mixed">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path d="M5 8l6 6M4 14l6-6 2-3M2 5h12M7 2h1"/>
                  <path d="M22 22l-5-10-5 10M14 18h6"/>
                </svg>
              </div>
              <Leaf className="feature-leaf-2" size={55} flip />
            </div>
          </div>
        </div>
      </section>

      {/* More Features Grid */}
      <section className="section section-alt">
        <Wave className="section-wave-top" flip />
        <Circle className="features-grid-circle" size={400} />

        <div className="container">
          <div className="section-header">
            <span className="section-badge">Enterprise Ready</span>
            <h2 className="section-title">Designed for Business</h2>
          </div>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="3" width="20" height="14" rx="2"/>
                  <line x1="8" y1="21" x2="16" y2="21"/>
                  <line x1="12" y1="17" x2="12" y2="21"/>
                </svg>
              </div>
              <h3>Non-Intrusive Overlay</h3>
              <p>Professional caption display that doesn't interfere with presentations or workflows.</p>
            </div>

            <div className="feature-card">
              <div className="feature-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
              </div>
              <h3>IT-Friendly Deployment</h3>
              <p>Simple installation with no infrastructure changes. Runs on individual workstations.</p>
            </div>

            <div className="feature-card">
              <div className="feature-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
              </div>
              <h3>Low Latency</h3>
              <p>Captions appear in under 200ms, keeping conversations natural and productive.</p>
            </div>

            <div className="feature-card">
              <div className="feature-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
              </div>
              <h3>Data Privacy</h3>
              <p>All processing happens locally. No audio or transcripts leave the employee's device.</p>
            </div>
          </div>
        </div>

        <Wave className="section-wave-bottom" />
      </section>

      {/* CTA */}
      <section className="section cta-section">
        <div className="container">
          <Butterfly className="cta-butterfly" size={50} />
          <div className="cta-content">
            <h2>Ready to Enable Your Workforce?</h2>
            <p>Deploy Audibly and ensure every employee can participate fully.</p>
            <Link to="/download" className="btn btn-white btn-lg">
              Get Started
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Features
