<template>
  <div
    class="flex items-center px-2 py-4 space-x-4 font-mono rounded-lg shadow-lg"
  >
    <div
      class="flex-none text-xl text-green-500 font-rock"
      :title="`Change type: ${getChangeType}`"
      :class="[getChangeTypeColor]"
    >
      {{ file.changeType }}
    </div>
    <div class="flex flex-col flex-grow">
      <div class="tracking-tighter text-gray-100 lg:text-lg">
        {{ filename }}
      </div>
      <div
        v-if="fileRoot !== null"
        class="ml-3 text-xs font-bold font-rock text-warm-gray-300"
      >
        {{ fileRoot }}
      </div>
    </div>
    <div class="flex-none">
      <slot name="file-actions"></slot>
    </div>
  </div>
</template>

<script>
import { getFileRoot, getFilename, getChangeTypeColor } from '../../utils.js'

export default {
  props: {
    file: {
      required: true,
      type: Object,
    },
  },
  data: () => ({
    filename: '',
    fileRoot: '',
  }),
  computed: {
    getChangeType() {
      if (this.file.changeType === 'U') {
        return 'Untracked'
      } else if (this.file.changeType === 'D') {
        return 'Deleted'
      } else if (this.file.changeType === 'M') {
        return 'Modified'
      }
      return ''
    },
    getChangeTypeColor() {
      return getChangeTypeColor(this.file.changeType)
    },
  },
  mounted() {
    this.filename = this.getFilename()
    this.fileRoot = this.getFileRoot()
  },
  methods: {
    getFilename() {
      return getFilename(this.file.name)
    },
    getFileRoot() {
      return getFileRoot(this.file.name)
    },
  },
}
</script>
