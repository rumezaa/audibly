# Audibly Website

A React website for Audibly, a Windows application providing real-time accessibility features including ASL recognition, speech-to-text, and translation.

Built for **HackTheBias 2026**.

## Quick Start

```bash
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## Project Structure

```
AudiblySite/
├── public/
│   └── favicon.svg
├── src/
│   ├── components/
│   │   ├── Decorations.jsx   # SVG butterflies, leaves, waves
│   │   ├── Footer.jsx
│   │   └── Navbar.jsx
│   ├── pages/
│   │   ├── About.jsx         # Design process, team
│   │   ├── Download.jsx      # Installation guide
│   │   ├── Features.jsx      # Feature details
│   │   └── Home.jsx          # Landing page
│   ├── styles/
│   │   ├── index.css         # Variables, reset, globals
│   │   ├── Navbar.css
│   │   ├── Footer.css
│   │   ├── Decorations.css
│   │   ├── Home.css
│   │   ├── Features.css
│   │   ├── Download.css
│   │   └── About.css
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── vite.config.js
└── package.json
```

## Tech Stack

- React 18
- React Router 6
- Vite
- CSS (no preprocessor)

## Design

- **Primary:** Dark navy (#1e3a5f)
- **Secondary:** Light blue (#7dd3fc)
- **Tertiary:** Grapefruit (#fb7185)
- Decorative SVG butterflies and leaves
- Responsive for desktop and mobile
