/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html"],
  theme: {
    container: {
      padding: {
        DEFAULT: "2rem",
        sm: '2.5vw',
        lg: '5vw',
        xl: '10vw',
        '2xl': '12.5vw',
      },
      screens: {
        sm: '900px',
        lg: '1080px',
        xl: '1380px',
        '2xl': '1600px',
      }
    },
    extend: {},
  },
  plugins: [],
}

