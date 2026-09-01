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
        copal: {
          black: '#0B0D0F',
          white: '#FFFFFF',
          green: '#15A34A',
          'green-light': '#22C55E',
          'green-dark': '#138A3E',
          gray: {
            50: '#F8F9FA',
            100: '#F1F3F5',
            200: '#E9ECEF',
            300: '#DEE2E6',
            400: '#ADB5BD',
            500: '#6C757D',
            600: '#495057',
            700: '#343A40',
            800: '#212529',
            900: '#0B0D0F',
          },
        },
      },
      fontFamily: {
        'suez': ['"Suez One"', 'serif'],
        'roboto': ['"Roboto"', 'sans-serif'],
        'space-grotesk': ['"Space Grotesk"', 'sans-serif'],
        'dm-sans': ['"DM Sans"', 'sans-serif'],
        'ibm-plex-mono': ['"IBM Plex Mono"', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '6px',
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
    },
  },
  plugins: [],
}
