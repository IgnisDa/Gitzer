<template>
  <div class="min-h-screen bg-gray-900 flex w-full">
    <div class="text-white mx-auto flex flex-col container">
      <div class="flex flex-col font-mono h-1/2 items-center">
        <div class="my-auto max-w-4xl shadow-lg p-3 border border-gray-800">
          <div
            class="text-6xl md:text-9xl font-semibold transition duration-500 ease-in"
            :class="existence.exists ? 'text-green-400' : 'text-red-500'"
          >
            Gitzer.
          </div>
          <div class="p-3 items-center mt-6">
            <div class="w-full">
              <form
                class="flex flex-wrap items-center w-full relative"
                @submit.prevent="submitForm()"
              >
                <input
                  ref="directory"
                  v-model="directory"
                  type="text"
                  class="flex-shrink text-black font-serif font-thin flex-grow leading-normal w-px flex-1 border h-10 border-grey-light rounded rounded-r-none px-3 relative"
                  placeholder="Repository"
                />
              </form>
            </div>
            <div class="mx-2 mt-2 text-gray-200">
              Path to a local git repository
            </div>
          </div>
        </div>
      </div>
      <div class="text-center h-1/2">
        <div class="max-w-4xl mx-auto">
          <div class="mx-auto flex">
            <NuxtLink
              :event="existence.exists ? 'click' : ''"
              :to="{ name: 'status', query: { directory: directory } }"
              class="mx-auto"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                class="h-24 w-24 fill-current rounded-full mx-auto transition ease-out duration-500"
                :class="
                  existence.exists === true
                    ? 'text-purple-600 hover:text-pink-600 cursor-pointer'
                    : 'text-black cursor-default'
                "
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </NuxtLink>
          </div>
          <div class="text-xl">
            {{ existence.message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import existenceQuery from '~/apollo/queries/existence.gql'
import presentWorkingDirectoryQuery from '~/apollo/queries/presentWorkingDirectory.gql'

export default {
  data: () => ({
    directory: '',
    existence: false,
  }),
  head() {
    return { title: 'Gitzer' }
  },
  watch: {
    directory() {
      this.$apollo
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
  mounted() {
    this.presentWorkingDirectory()
    this.focusInput()
  },
  methods: {
    focusInput() {
      this.$refs.directory.focus()
    },
    async presentWorkingDirectory() {
      await this.$apollo
        .query({
          query: presentWorkingDirectoryQuery,
        })
        .then((data) => {
          this.directory = data.data.presentWorkingDirectory
        })
        .catch((error) => {
          this.existence = error
        })
    },
    submitForm() {
      if (this.existence) {
        this.$router.push({
          name: 'status',
          query: { directory: this.directory },
        })
      }
    },
  },
}
</script>
