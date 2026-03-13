/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        coffee: {
          light: '#FAF9F6',
          dark: '#2C1B18',
          accent: '#C67C4E',
        }
      }
    },
  },
  plugins: [],
}