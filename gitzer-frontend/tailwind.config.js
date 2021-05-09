const ignisnents = require('ignisnents/dist/tailwind-preset.js')

module.exports = {
  mode: 'jit',
  presets: [ignisnents],
  purge: {
    content: [
      'components/**/*.vue',
      'layouts/**/*.vue',
      'pages/**/*.vue',
      'plugins/**/*.js',
      'nuxt.config.js',
      'node_modules/ignisnents/src/components/**/*.vue',
      '*.js',
    ],
  },
  darkMode: false,
  theme: {
    extend: {
      animation: {
        'spin-slow': 'spin 2.5s linear infinite',
      },
      fontFamily: {
        display: ['Josefin Sans', 'sans-serif'],
        rock: ['RocknRoll One', 'sans-serif'],
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [require('tailwindcss-debug-screens')],
}
