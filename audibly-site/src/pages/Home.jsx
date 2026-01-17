import { Link } from 'react-router-dom'
import { FloatingLeaves, Wave, Circle, Butterfly, Leaf } from '../components/Decorations'
import '../styles/Home.css'

function Home() {
  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <FloatingLeaves className="hero-leaves" />
        <Circle className="hero-circle-1" size={400} />
        <Circle className="hero-circle-2" size={300} />

        <div className="container">
          <div className="hero-content">
            <span className="hero-badge">Workplace Accessibility Solution</span>
            <h1 className="hero-title">
              Equal Access to <span className="gradient-text">Every Meeting</span>
            </h1>
            <p className="hero-subtitle">
              Audibly ensures deaf and hard-of-hearing employees can fully participate
              in meetings, presentations, and daily workplace communication. Real-time
              captions, ASL recognition, and translation—integrated seamlessly into your workflow.
            </p>
            <div className="hero-actions">
              <Link to="/download" className="btn btn-primary btn-lg">
                Request a Demo
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </Link>
              <Link to="/features" className="btn btn-outline btn-lg">
                See How It Works
              </Link>
            </div>
            <div className="hero-stats">
              <div className="stat">
                <span className="stat-number">15%</span>
                <span className="stat-label">of global workforce has hearing loss</span>
              </div>
              <div className="stat">
                <span className="stat-number">76%</span>
                <span className="stat-label">report workplace communication barriers</span>
              </div>
              <div className="stat">
                <span className="stat-number">$0</span>
                <span className="stat-label">Cost to deploy</span>
              </div>
            </div>
          </div>

          <div className="hero-visual">
            <div className="hero-mockup">
              <div className="mockup-window">
                <div className="mockup-header">
                  <span className="dot red"></span>
                  <span className="dot yellow"></span>
                  <span className="dot green"></span>
                </div>
                <div className="mockup-content">
                  <div className="caption-demo">
                    <div className="speaker-badge">Manager</div>
                    <p className="caption-text">Let's review the Q4 projections and discuss the timeline for the product launch...</p>
                  </div>
                  <div className="asl-indicator">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                      <rect x="3" y="11" width="18" height="11" rx="2"/>
                    </svg>
                    <span>ASL Input Active</span>
                  </div>
                </div>
              </div>
              <Butterfly className="mockup-butterfly" size={50} />
            </div>
          </div>
        </div>

        <Wave className="hero-wave" />
      </section>

      {/* Problem Section */}
      <section className="section problem-section">
        <div className="container">
          <div className="section-header">
            <span className="section-badge">The Workplace Reality</span>
            <h2 className="section-title">Meetings Aren't Accessible by Default</h2>
            <p className="section-subtitle">
              Employees with hearing loss face daily barriers that limit their contributions and career growth.
            </p>
          </div>

          <div className="problem-grid">
            <div className="problem-card">
              <div className="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="3" width="20" height="14" rx="2"/>
                  <path d="M8 21h8M12 17v4"/>
                </svg>
              </div>
              <h3>Video Calls Without Captions</h3>
              <p>
                Most video conferencing platforms offer limited or inaccurate auto-captions.
                Employees miss critical information, action items, and context—leading to
                mistakes and exclusion from key decisions.
              </p>
            </div>

            <div className="problem-card">
              <div className="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
              </div>
              <h3>In-Person Meeting Barriers</h3>
              <p>
                Conference rooms, team huddles, and impromptu discussions happen without
                interpretation services. Deaf employees are forced to rely on incomplete
                notes or ask colleagues to repeat themselves.
              </p>
            </div>

            <div className="problem-card">
              <div className="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 20V10"/>
                  <path d="M18 20V4"/>
                  <path d="M6 20v-4"/>
                </svg>
              </div>
              <h3>Career Advancement Gap</h3>
              <p>
                When communication tools fail, employees with hearing loss are overlooked
                for promotions, excluded from leadership conversations, and
                underrepresented in senior roles.
              </p>
            </div>
          </div>
        </div>
        <Leaf className="problem-leaf-1" size={80} />
        <Leaf className="problem-leaf-2" size={60} flip />
      </section>

      {/* Solution Section */}
      <section className="section section-alt solution-section">
        <Wave className="section-wave-top" flip />
        <Circle className="solution-circle" size={500} />

        <div className="container">
          <div className="solution-content">
            <div className="solution-text">
              <span className="section-badge">The Solution</span>
              <h2 className="section-title left-align">Workplace Accessibility, Automated</h2>
              <p className="solution-lead">
                Audibly runs in the background on Windows workstations, providing instant
                accessibility for any audio or video content—no IT infrastructure changes required.
              </p>

              <div className="solution-steps">
                <div className="solution-step">
                  <div className="step-number">1</div>
                  <div className="step-content">
                    <h4>Capture System Audio</h4>
                    <p>Automatically transcribes audio from Zoom, Teams, Slack, or any application with high accuracy.</p>
                  </div>
                </div>

                <div className="solution-step">
                  <div className="step-number">2</div>
                  <div className="step-content">
                    <h4>Recognize ASL Input</h4>
                    <p>Employees who sign can contribute to meetings—Audibly translates ASL gestures to text in real-time.</p>
                  </div>
                </div>

                <div className="solution-step">
                  <div className="step-number">3</div>
                  <div className="step-content">
                    <h4>Display Professional Captions</h4>
                    <p>Clean, customizable overlay that doesn't interfere with your work. Position it anywhere on screen.</p>
                  </div>
                </div>
              </div>

              <p className="solution-footer">
                Zero configuration. No subscription fees. Deploy to individual workstations in minutes.
              </p>
            </div>

            <div className="solution-visual">
              <div className="feature-cards-stack">
                <div className="feature-mini-card">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                  </svg>
                  <span>Speech-to-Text</span>
                </div>
                <div className="feature-mini-card">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    <rect x="3" y="11" width="18" height="11" rx="2"/>
                  </svg>
                  <span>ASL Recognition</span>
                </div>
                <div className="feature-mini-card">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 8l6 6M4 14l6-6 2-3M2 5h12M7 2h1"/>
                    <path d="M22 22l-5-10-5 10M14 18h6"/>
                  </svg>
                  <span>Multi-Language</span>
                </div>
              </div>
              <Butterfly className="solution-butterfly" size={60} />
            </div>
          </div>
        </div>

        <Wave className="section-wave-bottom" />
      </section>

      {/* CTA Section */}
      <section className="section cta-section">
        <div className="container">
          <Butterfly className="cta-butterfly-1" size={40} />
          <Butterfly className="cta-butterfly-2" size={55} />

          <div className="cta-content">
            <h2>Make Your Workplace Accessible</h2>
            <p>Give every employee the tools to contribute fully.</p>
            <Link to="/download" className="btn btn-white btn-lg">
              Get Audibly for Your Team
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7,10 12,15 17,10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home
