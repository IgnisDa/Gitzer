<template>
  <div class="w-full p-3 md:w-1/2 lg:w-1/3 h-1/3 md:h-1/2 lg:h-full">
    <div class="flex flex-col w-full h-full">
      <div
        class="flex items-center justify-between flex-none px-3 py-2 border-2 border-gray-900 border-dashed rounded-lg bg-lime-600"
      >
        <div class="flex-grow text-xl uppercase font-rock">{{ title }}</div>
        <div class="flex-none">
          <slot name="column-commands"></slot>
        </div>
      </div>
      <div class="flex-grow mx-2 mt-2 overflow-auto">
        <slot name="body"></slot>
      </div>
    </div>
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
