<template>
  <div class="min-h-screen bg-gray-900 flex w-full">
    <div class="text-white mx-auto flex flex-col container">
      <div class="flex flex-col font-mono h-1/2 items-center">
        <div class="my-auto max-w-4xl shadow-lg p-3 border border-gray-800">
          <div
            class="text-6xl md:text-9xl font-semibold"
            :class="
              existence.exists === true
                ? 'text-successful'
                : 'text-unsuccessful'
            "
          >
            Gitzer.
          </div>
          <div class="p-3 items-center mt-6">
            <div class="w-full">
              <form
                class="flex flex-wrap items-center w-full relative"
                @submit.prevent="checkRepository()"
              >
                <input
                  v-model="directory"
                  type="text"
                  class="flex-shrink text-black font-serif font-thin flex-grow leading-normal w-px flex-1 border h-10 border-grey-light rounded rounded-r-none px-3 relative"
                  placeholder="Repository"
                />
                <button type="submit" class="flex -mr-px">
                  <span
                    class="flex items-center leading-normal bg-grey-lighter rounded rounded-l-none border border-l-0 border-grey-light px-3 whitespace-no-wrap text-grey-dark text-sm"
                    ><svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      class="h-8 w-8 fill-current text-white"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </span>
                </button>
              </form>
            </div>
            <div class="mx-2 mt-2 text-gray-200">
              Path to a local git repository
            </div>
          </div>
        </div>
      </div>
      <div class="flex text-center h-1/2">
        <div class="mx-auto max-w-4xl text-3xl text-yellow-400">
          {{ existence.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import existenceQuery from '~/apollo/existence.gql'

export default {
  data: () => ({
    directory: '..',
    existence: false,
  }),
  head() {
    return { title: 'Gitzer' }
  },
  mounted() {
    this.checkRepository()
  },
  methods: {
    async checkRepository() {
      await this.$apollo
        .query({
          query: existenceQuery,
          variables: {
            directory: this.directory,
          },
        })
        .then((data) => {
          this.existence = data.data.existence
        })
        .catch((error) => {
          this.existence = error
        })
    },
  },
}
</script>

<style>
.text-successful {
  @apply text-green-400;
}
.text-unsuccessful {
  @apply text-red-500;
}
</style>
