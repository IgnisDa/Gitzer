<template>
  <div class="hidden">
    <span v-hotkey="keymap"></span>
  </div>
</template>

<script>
export default {
  data() {
    return {
      show: true,
    }
  },
  computed: {
    keymap() {
      return {
        'ctrl+enter': this.commit,
      }
    },
  },
  methods: {
    commit() {
      this.$emit('submitForm')
    },
  },
}
</script>
