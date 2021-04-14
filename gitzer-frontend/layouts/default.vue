<template>
  <div
    class="flex max-w-full antialiased h-screen"
    :class="mode !== 'production' ? 'debug-screens' : ''"
  >
    <alert></alert>
    <Nuxt keep-alive />
  </div>
</template>

<script>
export default {
  data: () => ({
    mode: process.env.NODE_ENV,
  }),
}
</script>
