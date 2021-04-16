<template>
  <button
    class="p-1 mx-1 transition transform border-2 border-dotted rounded-lg border-warm-gray-900 hover:shadow-2xl hover:scale-110"
    :title="title"
    :class="{ 'text-warm-gray-800 hover:text-black': !noColor }"
  >
    <IgIcon size="lg" no-color :name="icon"></IgIcon>
  </button>
</template>

<script>
export default {
  props: {
    icon: {
      required: true,
      type: String,
    },
    title: {
      type: String,
      default: 'Perform Action',
    },
    noColor: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
