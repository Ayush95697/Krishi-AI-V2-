/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'canvas-sand': '#F4EFE6',
        'monsoon-blue': '#1F3A44',
        'earthen-clay': '#8B3F2B',
        'turmeric-gold': '#D3901B',
        'harvest-green': '#2D5E37',
        'surface-paper': '#FAF9F6',
      },
      fontFamily: {
        serif: ['Karma', 'serif'],
        sans: ['Hind', 'sans-serif'],
        data: ['"Work Sans"', 'sans-serif'],
      }
    },
  },
  plugins: [],
}