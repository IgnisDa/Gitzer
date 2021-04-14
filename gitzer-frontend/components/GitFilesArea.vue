<template>
  <div class="w-full md:w-1/3">
    <div>{{ title }}</div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      required: true,
      type: String,
    },
  },
}
</script>
