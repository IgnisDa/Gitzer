<template>
  <div class="min-h-screen w-full flex flex-col">
    <!-- <client-only>
      <div v-if="loading">Loading your repository...</div>
    </client-only> -->
    <div class="container mx-auto">
      <div class="flex flex-wrap overflow-hidden">
        <div
          class="max-h-96 w-full md:w-1/3 overflow-auto border-l border-b border-black relative"
        >
          <div class="text-center bg-yellow-200 sticky top-0">
            Untracked Files
          </div>
          <div>
            <div v-if="untrackedFiles.length !== 0">
              <div
                v-for="(file, index) in untrackedFiles"
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
                    @click="
                      stageFileAction({
                        filename: file.name,
                        directory: $route.query.directory,
                      })
                    "
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
            <div v-if="modifiedFiles.length !== 0">
              <div
                v-for="(file, index) in modifiedFiles"
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
                    @click="
                      stageFileAction({
                        filename: file.name,
                        directory: $route.query.directory,
                      })
                    "
                  >
                    <FontAwesomeIcon class="h-7" :icon="['fas', 'plus']" />
                  </button>
                  <button
                    class="mx-1 shadow-inner rounded-full p-1"
                    @click="
                      discardFileChangeAction({
                        filename: file.name,
                        directory: $route.query.directory,
                      })
                    "
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
            <div v-if="stagedFiles.length !== 0">
              <div
                v-for="(file, index) in stagedFiles"
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
                    @click="
                      unstageFileAction({
                        filename: file.name,
                        directory: $route.query.directory,
                      })
                    "
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
    <div>
      <CommitMessageForm />
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

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
  data: () => ({
    loading: 0,
  }),
  head: () => ({
    title: 'Status',
  }),
  computed: {
    ...mapState({
      stagedFiles: (state) => state.repository.stagedFiles,
      modifiedFiles: (state) => state.repository.modifiedFiles,
      untrackedFiles: (state) => state.repository.untrackedFiles,
    }),
  },
  mounted() {
    this.fetchStatusAction({ directory: this.$route.query.directory })
    this.interval = setInterval(
      function () {
        this.fetchStatusAction({ directory: this.$route.query.directory })
      }.bind(this),
      10000
    )
  },
  beforeDestroy() {
    clearInterval(this.interval)
  },
  methods: {
    ...mapActions({
      fetchStatusAction: 'repository/fetchStatus',
      stageFileAction: 'repository/stageFile',
      unstageFileAction: 'repository/unstageFile',
      discardFileChangeAction: 'repository/discardFileChange',
    }),
  },
}
</script>
