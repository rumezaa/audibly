import '../styles/Decorations.css'

export function Butterfly({ className = '', size = 40 }) {
  return (
    <svg
      className={`decoration butterfly ${className}`}
      width={size}
      height={size}
      viewBox="0 0 60 60"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M30 15c-8-12-25-8-25 8 0 12 15 22 25 32 10-10 25-20 25-32 0-16-17-20-25-8z"
        fill="currentColor"
        opacity="0.15"
      />
      <path
        d="M30 25c-5-8-15-5-15 5 0 8 10 14 15 20 5-6 15-12 15-20 0-10-10-13-15-5z"
        fill="currentColor"
        opacity="0.25"
      />
      <ellipse cx="30" cy="35" rx="2" ry="12" fill="currentColor" opacity="0.4"/>
    </svg>
  )
}

export function Leaf({ className = '', size = 50, flip = false }) {
  return (
    <svg
      className={`decoration leaf ${className}`}
      width={size}
      height={size}
      viewBox="0 0 60 60"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ transform: flip ? 'scaleX(-1)' : 'none' }}
    >
      <path
        d="M10 50C10 25 25 10 50 10c-5 15-15 25-25 30-5 3-10 8-15 10z"
        fill="currentColor"
        opacity="0.12"
      />
      <path
        d="M15 45c5-20 15-30 35-35-5 12-12 22-22 28-4 2-8 5-13 7z"
        fill="currentColor"
        opacity="0.08"
      />
      <path
        d="M12 48c10-15 20-25 38-38"
        stroke="currentColor"
        strokeWidth="1"
        opacity="0.15"
      />
    </svg>
  )
}

export function FloatingLeaves({ className = '' }) {
  return (
    <div className={`floating-leaves ${className}`}>
      <Leaf className="float-1" size={60} />
      <Leaf className="float-2" size={45} flip />
      <Leaf className="float-3" size={55} />
      <Butterfly className="float-4" size={35} />
      <Leaf className="float-5" size={40} flip />
      <Butterfly className="float-6" size={45} />
    </div>
  )
}

export function Wave({ className = '', flip = false }) {
  return (
    <svg
      className={`wave ${className}`}
      viewBox="0 0 1440 120"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      preserveAspectRatio="none"
      style={{ transform: flip ? 'rotate(180deg)' : 'none' }}
    >
      <path
        d="M0 60c240-40 480 40 720 0s480-40 720 0v60H0z"
        fill="currentColor"
      />
    </svg>
  )
}

export function Circle({ className = '', size = 200 }) {
  return (
    <div
      className={`decoration-circle ${className}`}
      style={{ width: size, height: size }}
    />
  )
}
