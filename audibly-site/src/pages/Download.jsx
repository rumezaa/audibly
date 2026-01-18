import { Wave, Butterfly, Leaf, Circle } from '../components/Decorations'
import '../styles/Download.css'

function Download() {
  return (
    <div className="download-page">
      {/* Page Header */}
      <section className="page-header">
        <Circle className="header-circle" size={350} />
        <Leaf className="header-leaf" size={60} />

        <div className="container">
          <span className="section-badge">Get Audibly</span>
          <h1>Download Audibly</h1>
          <p>Get started in minutes with our simple installation.</p>
        </div>

        <Wave className="header-wave" />
      </section>

      {/* Download Hero */}
      <section className="section download-hero-section">
        <div className="container">
          <div className="download-card">
            <div className="download-card-content">
              <div className="platform-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M0 3.449L9.75 2.1v9.451H0m10.949-9.602L24 0v11.4H10.949M0 12.6h9.75v9.451L0 20.699M10.949 12.6H24V24l-12.9-1.801"/>
                </svg>
              </div>

              <div className="download-info">
                <h2>Audibly for Windows</h2>
                <span className="version-badge">Version 1.0.0</span>
                <p>
                  A lightweight Windows application that provides real-time captions,
                  ASL recognition, and translation. Runs in your system tray and works
                  with any application.
                </p>

                <div className="requirements">
                  <h4>System Requirements</h4>
                  <ul>
                    <li>Windows 10 or Windows 11</li>
                    <li>4 GB RAM minimum</li>
                    <li>Webcam (for ASL recognition)</li>
                    <li>Internet connection (for initial setup)</li>
                  </ul>
                </div>

                <a href="https://google.com" className="btn btn-primary btn-lg download-btn" target="_blank" rel="noopener noreferrer">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7,10 12,15 17,10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  Download for Windows
                </a>
                <p className="download-note">Free download. No account required.</p>
              </div>
            </div>

            <Butterfly className="download-butterfly" size={55} />
          </div>
        </div>
      </section>

      {/* Installation Steps */}
      <section className="section section-alt">
        <Wave className="section-wave-top" flip />
        <Circle className="install-circle" size={400} />

        <div className="container">
          <div className="section-header">
            <span className="section-badge">Setup</span>
            <h2 className="section-title">Installation Guide</h2>
          </div>

          <div className="install-steps">
            <div className="install-step">
              <div className="step-icon">
                <span>1</span>
              </div>
              <div className="step-content">
                <h3>Download the Installer</h3>
                <p>Click the download button above to get the Audibly installer. The file is small and downloads quickly.</p>
              </div>
            </div>

            <div className="install-step">
              <div className="step-icon">
                <span>2</span>
              </div>
              <div className="step-content">
                <h3>Run the Setup</h3>
                <p>Double-click the downloaded file and follow the on-screen instructions. No administrator privileges required.</p>
              </div>
            </div>

            <div className="install-step">
              <div className="step-icon">
                <span>3</span>
              </div>
              <div className="step-content">
                <h3>Grant Permissions</h3>
                <p>Allow Audibly to access your microphone and camera when prompted for speech recognition and ASL detection.</p>
              </div>
            </div>

            <div className="install-step">
              <div className="step-icon">
                <span>4</span>
              </div>
              <div className="step-content">
                <h3>Start Using Audibly</h3>
                <p>Look for the Audibly icon in your system tray. Click it to open settings and adjust preferences.</p>
              </div>
            </div>
          </div>
        </div>

        <Wave className="section-wave-bottom" />
      </section>

      {/* Quick Tips */}
      <section className="section">
        <div className="container">
          <div className="section-header">
            <span className="section-badge">Tips</span>
            <h2 className="section-title">Quick Start Tips</h2>
          </div>

          <div className="tips-grid">
            <div className="tip-card">
              <div className="tip-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="3" width="20" height="14" rx="2"/>
                  <path d="M8 21h8M12 17v4"/>
                </svg>
              </div>
              <h3>Enable Captions</h3>
              <p>Right-click the system tray icon and select "Show Captions" to display the overlay.</p>
            </div>

            <div className="tip-card">
              <div className="tip-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M5 3l14 9-14 9V3z"/>
                </svg>
              </div>
              <h3>Adjust Position</h3>
              <p>Drag the caption window anywhere on screen. It stays on top of other windows.</p>
            </div>

            <div className="tip-card">
              <div className="tip-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-2.82 1.17V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1.08-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0-.33-2.82H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1.08 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 2.82-.33V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1.08 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0 .33 2.82H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1.08z"/>
                </svg>
              </div>
              <h3>Change Settings</h3>
              <p>Customize font size, colors, and enable/disable specific features from the settings menu.</p>
            </div>

            <div className="tip-card">
              <div className="tip-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="4" width="20" height="16" rx="2"/>
                  <path d="M6 8h.01M10 8h.01M6 12h12M6 16h8"/>
                </svg>
              </div>
              <h3>Keyboard Shortcut</h3>
              <p>Use Ctrl+Shift+A to quickly toggle captions on and off without clicking.</p>
            </div>
          </div>
        </div>

        <Leaf className="tips-leaf" size={70} flip />
      </section>

      {/* FAQ */}
      <section className="section section-alt">
        <Wave className="section-wave-top" flip />

        <div className="container">
          <div className="section-header">
            <span className="section-badge">Help</span>
            <h2 className="section-title">Frequently Asked Questions</h2>
          </div>

          <div className="faq-list">
            <div className="faq-item">
              <h3>Is Audibly free?</h3>
              <p>Yes, Audibly is completely free to use. There are no subscriptions, premium tiers, or hidden costs.</p>
            </div>

            <div className="faq-item">
              <h3>Does Audibly work offline?</h3>
              <p>Core features work offline after the initial setup. Some advanced features may require an internet connection.</p>
            </div>

            <div className="faq-item">
              <h3>Is my data private?</h3>
              <p>Absolutely. All audio and video processing happens locally on your computer. We don't collect or transmit your conversations.</p>
            </div>

            <div className="faq-item">
              <h3>Can I use Audibly with Zoom, Teams, etc?</h3>
              <p>Yes! Audibly works with any application that plays audio or uses your webcam, including all major video conferencing tools.</p>
            </div>
          </div>
        </div>

        <Butterfly className="faq-butterfly" size={45} />
        <Wave className="section-wave-bottom" />
      </section>
    </div>
  )
}

export default Download
