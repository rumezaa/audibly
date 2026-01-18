import { Link } from 'react-router-dom'
import { Wave, Butterfly, Leaf, Circle } from '../components/Decorations'
import '../styles/About.css'

function About() {
  return (
    <div className="about-page">
      {/* Page Header */}
      <section className="page-header">
        <Circle className="header-circle" size={350} />
        <Butterfly className="header-butterfly" size={50} />

        <div className="container">
          <span className="section-badge">Our Mission</span>
          <h1>Eliminating Access Bias in the Workplace</h1>
          <p>Building technology that creates truly inclusive meeting cultures.</p>
        </div>

        <Wave className="header-wave" />
      </section>

      {/* Design Philosophy */}
      <section className="section">
        <div className="container">
          <div className="philosophy-intro">
            <h2>Designing for Workplace Equity</h2>
            <p className="lead">
              Access bias happens when workplace tools and practices systematically exclude
              certain employees. Every design decision in Audibly aims to <strong>eliminate
              these barriers</strong>—so meetings become spaces where everyone contributes equally.
            </p>
          </div>

          <div className="principles-grid">
            <div className="principle-card">
              <div className="principle-icon gradient-blue">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12,6 12,12 16,14"/>
                </svg>
              </div>
              <h3>Immediate Inclusion</h3>
              <p>
                Bias removal shouldn't require IT tickets or manager approval.
                Audibly works the moment an employee needs it—because access delayed
                is access denied.
              </p>
            </div>

            <div className="principle-card">
              <div className="principle-icon gradient-teal">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
              </div>
              <h3>Equity by Design</h3>
              <p>
                Rather than retrofitting inclusion, we built it into the foundation.
                Every employee gets the same quality meeting experience—no special
                requests, no stigma, no second-class participation.
              </p>
            </div>

            <div className="principle-card">
              <div className="principle-icon gradient-mixed">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
              </div>
              <h3>Confidential by Default</h3>
              <p>
                Meeting content stays on the employee's device—never transmitted
                to external servers. Board discussions, HR conversations, and
                strategic planning remain private.
              </p>
            </div>

            <div className="principle-card">
              <div className="principle-icon gradient-blue">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="3" width="18" height="18" rx="2"/>
                  <path d="M9 9h.01M15 9h.01M9 15h6"/>
                </svg>
              </div>
              <h3>Professional Integration</h3>
              <p>
                Audibly integrates seamlessly into corporate workflows—no disruptive
                overlays or attention-grabbing interfaces. It's enterprise software
                that respects the professional environment.
              </p>
            </div>
          </div>
        </div>

        <Leaf className="philosophy-leaf" size={80} />
      </section>

      {/* Process Timeline */}
      <section className="section section-alt">
        <Wave className="section-wave-top" flip />
        <Circle className="process-circle" size={450} />

        <div className="container">
          <div className="section-header">
            <span className="section-badge">Process</span>
            <h2 className="section-title">How We Built It</h2>
          </div>

          <div className="timeline">
            <div className="timeline-item">
              <div className="timeline-marker">
                <span>1</span>
              </div>
              <div className="timeline-content">
                <h3>Research</h3>
                <p>
                  We started by listening. Conversations with deaf and hard-of-hearing
                  individuals, non-native speakers, and accessibility advocates shaped
                  our understanding of real needs.
                </p>
              </div>
            </div>

            <div className="timeline-item">
              <div className="timeline-marker">
                <span>2</span>
              </div>
              <div className="timeline-content">
                <h3>Prototype</h3>
                <p>
                  Early prototypes focused on core functionality: can we capture audio
                  accurately? Can we recognize ASL reliably? We built ugly tools that
                  worked before beautiful tools that didn't.
                </p>
              </div>
            </div>

            <div className="timeline-item">
              <div className="timeline-marker">
                <span>3</span>
              </div>
              <div className="timeline-content">
                <h3>Test</h3>
                <p>
                  Real users tested every feature with real workflows. We watched,
                  took notes, and iterated. Assumptions we held dear were often wrong;
                  user behavior taught us what actually mattered.
                </p>
              </div>
            </div>

            <div className="timeline-item">
              <div className="timeline-marker">
                <span>4</span>
              </div>
              <div className="timeline-content">
                <h3>Refine</h3>
                <p>
                  The final product reflects hundreds of small improvements. Faster
                  response times, clearer captions, better defaults. Polish isn't
                  vanity—it's respect for users' time.
                </p>
              </div>
            </div>
          </div>
        </div>

        <Butterfly className="timeline-butterfly" size={50} />
        <Wave className="section-wave-bottom" />
      </section>

      {/* Team Section */}
      <section className="section" id="team">
        <div className="container">
          <div className="section-header">
            <span className="section-badge">Team</span>
            <h2 className="section-title">The People Behind Audibly</h2>
            <p className="section-subtitle">
              Built during HackTheBias 2026 by a team committed to eliminating workplace access bias.
            </p>
          </div>

          <div className="team-grid">
            <div className="team-card">
              <div className="team-avatar gradient-blue">
                <span>TM</span>
              </div>
              <h3>Team Member 1</h3>
              <span className="team-role">Lead Developer</span>
              <p>Core application architecture and real-time audio processing.</p>
            </div>

            <div className="team-card">
              <div className="team-avatar gradient-teal">
                <span>TM</span>
              </div>
              <h3>Team Member 2</h3>
              <span className="team-role">ML Engineer</span>
              <p>ASL recognition system and speech-to-text integration.</p>
            </div>

            <div className="team-card">
              <div className="team-avatar gradient-mixed">
                <span>TM</span>
              </div>
              <h3>Team Member 3</h3>
              <span className="team-role">UX Designer</span>
              <p>Interface design with accessibility and usability at the forefront.</p>
            </div>

            <div className="team-card">
              <div className="team-avatar gradient-blue">
                <span>TM</span>
              </div>
              <h3>Team Member 4</h3>
              <span className="team-role">Frontend Developer</span>
              <p>Website and application user interface development.</p>
            </div>
          </div>
        </div>

        <Leaf className="team-leaf-1" size={65} />
        <Leaf className="team-leaf-2" size={50} flip />
      </section>

      {/* Mission Statement */}
      <section className="section section-alt mission-section">
        <Wave className="section-wave-top" flip />

        <div className="container">
          <div className="mission-content">
            <Butterfly className="mission-butterfly-1" size={40} />
            <Butterfly className="mission-butterfly-2" size={55} />

            <h2>Our Commitment</h2>
            <blockquote>
              "Access bias in meetings isn't just an inconvenience—it's a systemic barrier
              that limits careers, silences perspectives, and costs organizations their
              best ideas. We're building technology that removes these barriers entirely,
              creating workplaces where every employee can participate, contribute, and advance."
            </blockquote>
          </div>
        </div>

        <Wave className="section-wave-bottom" />
      </section>

      {/* CTA */}
      <section className="section cta-section">
        <div className="container">
          <div className="cta-content">
            <h2>Join the Movement Against Access Bias</h2>
            <p>Transform your organization's meeting culture today.</p>
            <Link to="/download" className="btn btn-white btn-lg">
              Get Audibly for Your Organization
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default About
