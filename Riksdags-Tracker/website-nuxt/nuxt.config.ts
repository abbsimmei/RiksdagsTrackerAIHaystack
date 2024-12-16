// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@nuxt/content', '@nuxt/image'],
  // buildModules: [
  //   '@nuxt/image',
  // ],
  image: {
    // Image configurations, like domains
  },
  ssr: true,
  css: [
    '~/assets/css/multiselect.css',  // Add your global CSS file here
  ],
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
    }
  }
  
})