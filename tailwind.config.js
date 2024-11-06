/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#8c3800",
        secondary: "#ff7f27",
        border: "#99d9ea",
        black: "#000000",
        dark: "#3b3b3b",
        light: "#7f7f7f",
      },
    },
  },
  plugins: [],
}