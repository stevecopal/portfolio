/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './portfolio/templates/**/*.html',
    './portfolio/static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        black: '#000000',
        white: '#ffffff',
      },
      fontFamily: {
        'space-grotesk': ['Space Grotesk', 'sans-serif'],
        'dm-sans': ['DM Sans', 'sans-serif'],
        'ibm-plex-mono': ['IBM Plex Mono', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '0px',
        'sm': '2px',
        'md': '4px',
      }
    },
  },
  plugins: [],
}