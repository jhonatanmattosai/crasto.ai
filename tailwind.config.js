/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html'],
  theme: {
    extend: {
      animation: {
        shimmer: 'shimmer 2.5s linear infinite',
        synapse: 'synapse 8s linear infinite',
      },
      keyframes: {
        shimmer: {
          '0%': { transform: 'translateX(-150%)' },
          '100%': { transform: 'translateX(150%)' },
        },
        synapse: {
          '0%': { transform: 'translateX(-100%)', opacity: 0 },
          '10%': { opacity: 0.5 },
          '90%': { opacity: 0.5 },
          '100%': { transform: 'translateX(200%)', opacity: 0 },
        },
      },
    },
  },
  plugins: [],
}
