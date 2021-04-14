<template>
  <div>
    <FontAwesomeIcon
      :icon="['fas', 'times']"
      :class="classes"
    ></FontAwesomeIcon>
  </div>
</template>

<script>
export default {
  props: {
    classes: {
      type: String,
      default: 'h-8 w-8',
    },
  },
}
</script>
