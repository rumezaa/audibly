# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Run Commands

```bash
npm install     # Install dependencies
npm run dev     # Start development server (Vite)
npm run build   # Build for production
npm run preview # Preview production build
```

The development server runs at `http://localhost:5173`.

## Architecture

React + Vite single-page application for the Audibly accessibility product website.

**Entry Points:**
- `index.html` - HTML shell that loads React
- `src/main.jsx` - React app initialization with BrowserRouter
- `src/App.jsx` - Main component with route definitions

**Routing:** React Router v6 with four routes:
- `/` → Home (hero, problem, solution sections)
- `/features` → Features page (ASL, speech-to-text, translation)
- `/download` → Download and installation guide
- `/about` → Design philosophy and team

**Components (`src/components/`):**
- `Navbar.jsx` - Fixed horizontal navigation with mobile toggle
- `Footer.jsx` - Site footer with navigation and branding
- `Decorations.jsx` - SVG decorative elements (Butterfly, Leaf, Wave, Circle, FloatingLeaves)

**Styling (`src/styles/`):**
- `index.css` - CSS variables, reset, global styles
- Component-specific CSS files imported by each component

## Design System

**Color Scheme (CSS variables in `index.css`):**
- Primary: `#1e3a5f` (dark navy)
- Secondary: `#7dd3fc` (light blue)
- Tertiary: `#fb7185` (grapefruit/coral)

**Gradients:**
- `--gradient-primary` - Navy gradient
- `--gradient-secondary` - Light blue gradient
- `--gradient-tertiary` - Grapefruit gradient
- `--gradient-mixed` - Blue to grapefruit blend

**Decorative Elements:**
- Butterflies and leaves as floating SVG decorations
- Wave dividers between sections
- Gradient circles as background accents

## Constraints

- No backend, authentication, or analytics
- Must work on desktop and mobile
- Accessibility-first: keyboard navigation, screen reader support, reduced motion
