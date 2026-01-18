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
            <span className="hero-badge">Eliminating Access Bias in the Workplace</span>
            <h1 className="hero-title">
              Every Voice Heard in <span className="gradient-text">Every Meeting</span>
            </h1>
            <p className="hero-subtitle">
              Access bias excludes 15% of the workforce from full meeting participation.
              Audibly removes that barrier—providing real-time captions, ASL recognition,
              and translation so every employee can contribute equally, regardless of
              how they hear or communicate.
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
                <span className="stat-number">430M</span>
                <span className="stat-label">people globally face hearing-related access bias</span>
              </div>
              <div className="stat">
                <span className="stat-number">76%</span>
                <span className="stat-label">feel excluded from workplace meetings</span>
              </div>
              <div className="stat">
                <span className="stat-number">100%</span>
                <span className="stat-label">meeting inclusion with Audibly</span>
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
            <span className="section-badge">The Access Bias Problem</span>
            <h2 className="section-title">Meetings Create Systemic Exclusion</h2>
            <p className="section-subtitle">
              When meetings aren't accessible, organizations inadvertently create bias against employees
              with hearing differences—limiting their contributions, visibility, and career advancement.
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
              <h3>Virtual Meeting Exclusion</h3>
              <p>
                Video conferencing auto-captions are unreliable. Employees miss critical
                decisions, action items, and strategic discussions—creating an uneven
                playing field where some voices matter less than others.
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
              <h3>Conference Room Bias</h3>
              <p>
                In-person meetings, team huddles, and boardroom discussions happen
                without accommodation. Employees with hearing differences are systematically
                excluded from the conversations that shape company direction.
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
              <h3>Leadership Pipeline Bias</h3>
              <p>
                Access barriers compound over time. Employees who can't fully participate
                in meetings are passed over for promotions, excluded from leadership
                opportunities, and remain underrepresented at every level.
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
              <span className="section-badge">Removing the Bias</span>
              <h2 className="section-title left-align">Equal Meeting Participation, Automated</h2>
              <p className="solution-lead">
                Audibly eliminates access bias by running silently on Windows workstations,
                ensuring every employee can fully participate in any meeting—virtual or in-person—
                without requiring IT infrastructure changes or special accommodations.
              </p>

              <div className="solution-steps">
                <div className="solution-step">
                  <div className="step-number">1</div>
                  <div className="step-content">
                    <h4>Capture Meeting Audio</h4>
                    <p>Instantly transcribes Zoom, Teams, Meet, or any conferencing platform with enterprise-grade accuracy.</p>
                  </div>
                </div>

                <div className="solution-step">
                  <div className="step-number">2</div>
                  <div className="step-content">
                    <h4>Enable Two-Way Participation</h4>
                    <p>ASL users can contribute equally—Audibly translates sign language to text so their voice is part of the meeting.</p>
                  </div>
                </div>

                <div className="solution-step">
                  <div className="step-number">3</div>
                  <div className="step-content">
                    <h4>Professional Meeting Overlay</h4>
                    <p>Non-intrusive captions that integrate seamlessly with your meeting workflow. Enterprise-ready from day one.</p>
                  </div>
                </div>
              </div>

              <p className="solution-footer">
                Zero configuration. No IT overhead. Deploy organization-wide and create an inclusive meeting culture.
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
            <h2>Eliminate Access Bias in Your Organization</h2>
            <p>Create meetings where every employee can contribute equally.</p>
            <Link to="/download" className="btn btn-white btn-lg">
              Deploy Audibly Enterprise
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
