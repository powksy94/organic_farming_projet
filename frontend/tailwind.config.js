/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        agri: {
          50:  '#f0f9f3',
          100: '#d8f3dc',
          500: '#2d6a4f',
          600: '#1b4332',
          700: '#0d2818'
        }
      }
    },
  },
  plugins: [],
}
