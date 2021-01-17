<template>
  <div class="min-h-screen w-full flex">
    <!-- <client-only>
      <div v-if="loading">Loading your repository...</div>
    </client-only> -->
    <div v-if="status" class="container mx-auto">
      <div class="flex flex-wrap overflow-hidden">
        <div
          class="max-h-96 w-full md:w-1/3 overflow-auto border-l border-b border-black relative"
        >
          <div class="text-center bg-yellow-200 sticky top-0">
            Untracked Files
          </div>
          <div>
            <div v-if="status.untrackedFiles.length !== 0">
              <div
                v-for="(file, index) in status.untrackedFiles"
                :key="index"
                class="p-2 flex justify-between"
                :class="index % 2 ? 'bg-blue-200' : 'bg-blue-300'"
              >
                <div>
                  <div>
                    {{ file.name | getFilename }}
                  </div>
                  <div class="ml-2 text-sm">
                    {{ file.name | getFileRoot }}
                  </div>
                </div>
                <div class="flex items-center">
                  <button
                    class="mx-1 shadow-inner rounded-full p-1"
                    @click="stageFile(file.name)"
                  >
                    <FontAwesomeIcon class="h-7" :icon="['fas', 'plus']" />
                  </button>
                </div>
              </div>
            </div>
            <div v-else>No files</div>
          </div>
        </div>

        <div
          class="max-h-96 w-full md:w-1/3 overflow-auto border-l border-b border-black relative"
        >
          <div class="text-center bg-yellow-200 sticky top-0">
            Modified Files
          </div>
          <div>
            <div v-if="status.modifiedFiles.length !== 0">
              <div
                v-for="(file, index) in status.modifiedFiles"
                :key="index"
                class="p-2 flex justify-between"
                :class="index % 2 ? 'bg-blue-200' : 'bg-blue-300'"
              >
                <div>
                  <div>
                    {{ file.name | getFilename }}
                  </div>
                  <div class="ml-2 text-sm">
                    {{ file.name | getFileRoot }}
                  </div>
                </div>
                <div class="flex items-center">
                  <button
                    class="mx-1 shadow-inner rounded-full p-1"
                    @click="stageFile(file.name)"
                  >
                    <FontAwesomeIcon class="h-7" :icon="['fas', 'plus']" />
                  </button>
                  <button
                    class="mx-1 shadow-inner rounded-full p-1"
                    @click="discardFileChange(file.name)"
                  >
                    <FontAwesomeIcon class="h-7" :icon="['fas', 'trash']" />
                  </button>
                </div>
              </div>
            </div>
            <div v-else>No files</div>
          </div>
        </div>

        <div
          class="max-h-96 w-full md:w-1/3 overflow-auto border-l border-r border-b border-black relative"
        >
          <div class="text-center bg-yellow-200 sticky top-0">Staged Files</div>
          <div>
            <div v-if="status.stagedFiles.length !== 0">
              <div
                v-for="(file, index) in status.stagedFiles"
                :key="index"
                class="p-2 flex justify-between"
                :class="index % 2 ? 'bg-blue-200' : 'bg-blue-300'"
              >
                <div>
                  <div>
                    {{ file.name | getFilename }}
                  </div>
                  <div class="ml-2 text-sm">
                    {{ file.name | getFileRoot }}
                  </div>
                </div>
                <div class="flex items-center">
                  <button
                    class="mx-1 shadow-inner rounded-full p-1"
                    @click="unstageFile(file.name)"
                  >
                    <FontAwesomeIcon class="h-7" :icon="['fas', 'minus']" />
                  </button>
                </div>
              </div>
            </div>
            <div v-else>No files</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import statusQuery from '~/apollo/queries/status.gql'
import stageFileMutation from '~/apollo/mutations/stageFile.gql'
import unstageFileMutation from '~/apollo/mutations/unstageFile.gql'
import discardFileChangeMutation from '~/apollo/mutations/discardFileChange.gql'

export default {
  filters: {
    getFilename(filename) {
      const array = filename.split('/')
      return array[array.length - 1]
    },
    getFileRoot(filename) {
      const array = filename.split('/')
      return array.slice(0, array.length - 1).join('/')
    },
  },
  data: () => ({ loading: 0 }),
  head: () => ({
    title: 'Status',
  }),
  methods: {
    refetchStatus() {
      this.$apollo.queries.status.refetch()
    },
    discardFileChange(filename) {
      this.$apollo
        .mutate({
          mutation: discardFileChangeMutation,
          variables: {
            data: {
              filename,
              directory: this.$route.query.directory,
            },
          },
        })
        .then((result) => {
          this.refetchStatus()
        })
        .catch((err) => {
          console.log(err)
        })
    },
    stageFile(filename) {
      this.$apollo
        .mutate({
          mutation: stageFileMutation,
          variables: {
            data: {
              filename,
              directory: this.$route.query.directory,
            },
          },
        })
        .then((result) => {
          this.refetchStatus()
        })
        .catch((err) => {
          console.log(err)
        })
    },
    unstageFile(filename) {
      this.$apollo
        .mutate({
          mutation: unstageFileMutation,
          variables: {
            data: {
              filename,
              directory: this.$route.query.directory,
            },
          },
        })
        .then((result) => {
          this.refetchStatus()
        })
        .catch((err) => {
          console.log(err)
        })
    },
  },
  apollo: {
    $loadingKey: 'loading',
    status: {
      query: statusQuery,
      variables() {
        return { directory: this.$route.query.directory }
      },
      error(error) {
        this.status = error
      },
      prefetch: false,
      pollInterval: 10000,
    },
  },
}
</script>
