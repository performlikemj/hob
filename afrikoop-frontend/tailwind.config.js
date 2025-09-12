/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Bodoni Moda"', 'serif'],
        sans: ['"Noto Sans JP"', 'Poppins', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        // Custom colours inspired by ballroom aesthetics
        primary: '#e11d48', // vibrant magenta/rose
        secondary: '#0f766e', // deep teal/jade
        accent: '#eab308', // golden yellow
        ink: '#111827', // near-black for text
        paper: '#ffffff',
      },
    },
  },
  plugins: [],
};
