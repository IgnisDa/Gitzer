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
