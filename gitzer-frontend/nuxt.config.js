export default {
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: 'gitzer-frontend',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content:
          'The frontend of Gitzer - a web based client for simple git operations',
      },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: ['~/assets/css/main.css'],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    '~/plugins/fontawesome.js',
    '~/plugins/ignisnents.js',
    { src: '~/plugins/hotkeys.js', mode: 'client' },
  ],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    // https://go.nuxtjs.dev/stylelint
    '@nuxtjs/stylelint-module',
    // https://go.nuxtjs.dev/tailwindcss
    '@nuxtjs/tailwindcss',
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    '@nuxtjs/apollo',
    // https://google-fonts.nuxtjs.org/
    '@nuxtjs/google-fonts',
  ],

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {},

  // Added later
  server: {
    port: '3000',
    host: '0.0.0.0',
  },
  telemetry: false,
  watchers: {
    webpack: {
      aggregateTimeout: 300,
      poll: 1000,
    },
  },
  googleFonts: {
    families: {
      'Josefin+Sans': [500],
      Sacramento: true,
      'RocknRoll One': [400],
    },
  },
  publicRuntimeConfig: {
    backendUrl:
      process.env.VUE_APP_BACKEND_URL || 'http://127.0.0.1:8534/graphql/',
  },
  target: 'static',
  apollo: {
    clientConfigs: {
      default: '~/plugins/apollo-config.js',
    },
  },
}
