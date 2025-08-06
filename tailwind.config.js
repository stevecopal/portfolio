/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Chemin vers tes templates Django
    './monportfolio/**/*.py', // Inclut les fichiers Python pour les templates dynamiques
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}