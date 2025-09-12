import React, { useEffect, useState } from 'react';

// Theme toggle: switches a 'dark' class on <html> and persists preference.
export default function ThemeToggle({ className = '' }) {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    // Determine initial theme: localStorage > system preference
    const stored = localStorage.getItem('theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const dark = stored ? stored === 'dark' : prefersDark;
    setIsDark(dark);
    document.documentElement.classList.toggle('dark', dark);
  }, []);

  const toggle = () => {
    const next = !isDark;
    setIsDark(next);
    document.documentElement.classList.toggle('dark', next);
    localStorage.setItem('theme', next ? 'dark' : 'light');
  };

  return (
    <button
      type="button"
      onClick={toggle}
      className={`inline-flex items-center justify-center p-2 rounded-md text-ink dark:text-white hover:bg-ink/5 dark:hover:bg-white/10 ${className}`}
      aria-label={isDark ? 'Switch to light theme' : 'Switch to dark theme'}
      title={isDark ? 'Switch to light theme' : 'Switch to dark theme'}
    >
      {isDark ? (
        // Sun icon (when in dark mode, offer to switch to light). Uses brand gradient.
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-5 w-5">
          <defs>
            <linearGradient id="bijouGrad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#e11d48" />
              <stop offset="50%" stopColor="#eab308" />
              <stop offset="100%" stopColor="#0f766e" />
            </linearGradient>
          </defs>
          <circle cx="12" cy="12" r="4" fill="url(#bijouGrad)" />
          <g stroke="url(#bijouGrad)" strokeWidth="1.8" fill="none" strokeLinecap="round">
            <path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />
          </g>
        </svg>
      ) : (
        // Moon icon (when in light mode, offer to switch to dark). Uses brand gradient.
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-5 w-5">
          <defs>
            <linearGradient id="bijouGrad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#e11d48" />
              <stop offset="50%" stopColor="#eab308" />
              <stop offset="100%" stopColor="#0f766e" />
            </linearGradient>
          </defs>
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="url(#bijouGrad)" />
        </svg>
      )}
    </button>
  );
}
