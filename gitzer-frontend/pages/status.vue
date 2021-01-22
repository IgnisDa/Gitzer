<template>
  <div
    class="min-h-screen flex w-full from-indigo-900 bg-gradient-to-b to-gray-800"
  >
    <div class="container mx-auto flex flex-col">
      <div class="flex-grow flex">
        <div class="flex flex-wrap flex-grow my-auto">
          <div
            class="w-full md:w-1/3 rounded-lg p-2 max-h-80 overflow-y-auto overflow-x-hidden relative"
          >
            <div class="px-1 shadow-lg">
              <div
                class="text-3xl flex justify-between items-center font-serif text-blue-500 sticky top-0 bg-black p-3 rounded-3xl ring ring-green-600"
              >
                <div>Untracked Files</div>
                <button
                  class="mx-1 shadow-inner rounded-full p-1"
                  @click="
                    stageAllUntrackedFilesAction({
                      directory: $route.query.directory,
                    })
                  "
                >
                  <FontAwesomeIcon
                    class="h-7 text-yellow-400"
                    :icon="['fas', 'plus']"
                  />
                </button>
              </div>
              <div v-if="untrackedFiles.length !== 0">
                <transition-group tag="div" name="untracked-files">
                  <div
                    v-for="(file, index) in untrackedFiles"
                    :key="index + 0"
                    class="p-2 flex justify-between my-1 hover:bg-indigo-900 rounded-xl transition duration-200"
                    :class="index % 2 ? 'bg-gray-900' : 'bg-gray-700'"
                  >
                    <div class="font-mono justify-items-center">
                      <div class="text-white">
                        {{ file.name | getFilename }}
                      </div>
                      <div class="ml-2 text-sm text-gray-300">
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
                </transition-group>
              </div>
              <div v-else class="h-28 flex text-white">
                <FontAwesomeIcon
                  class="h-20 m-auto"
                  :icon="['fas', 'folder-open']"
                />
              </div>
            </div>
          </div>
          <div
            class="w-full md:w-1/3 rounded-lg p-2 max-h-80 overflow-y-auto overflow-x-hidden relative"
          >
            <div class="px-1 shadow-lg">
              <div
                class="text-3xl flex justify-between items-center font-serif text-blue-500 sticky top-0 bg-black p-3 rounded-3xl ring ring-green-600"
              >
                <div>Modified Files</div>
                <div>
                  <button
                    class="mx-1 shadow-inner rounded-full p-1"
                    @click="
                      stageAllModifiedFilesAction({
                        directory: $route.query.directory,
                      })
                    "
                  >
                    <FontAwesomeIcon
                      class="h-7 text-yellow-400"
                      :icon="['fas', 'plus']"
                    />
                  </button>
                  <button
                    class="mx-1 shadow-inner rounded-full p-1"
                    @click="
                      discardAllModifiedFilesAction({
                        directory: $route.query.directory,
                      })
                    "
                  >
                    <FontAwesomeIcon
                      class="h-7 text-yellow-400"
                      :icon="['fas', 'trash']"
                    />
                  </button>
                </div>
              </div>
              <div v-if="modifiedFiles.length !== 0">
                <div
                  v-for="(file, index) in modifiedFiles"
                  :key="index"
                  class="p-2 flex justify-between my-1 hover:bg-indigo-900 rounded-xl transition duration-200"
                  :class="index % 2 ? 'bg-gray-900' : 'bg-gray-700'"
                >
                  <div class="font-mono justify-items-center">
                    <div class="text-white">
                      {{ file.name | getFilename }}
                    </div>
                    <div class="ml-2 text-sm text-gray-300">
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
              <div v-else class="h-28 flex text-white">
                <FontAwesomeIcon
                  class="h-20 m-auto"
                  :icon="['fas', 'folder-open']"
                />
              </div>
            </div>
          </div>
          <div
            class="w-full md:w-1/3 rounded-lg p-2 max-h-80 overflow-y-auto overflow-x-hidden relative"
          >
            <div class="px-1 shadow-lg">
              <div
                class="text-3xl flex justify-between items-center font-serif text-blue-500 sticky top-0 bg-black p-3 rounded-3xl ring ring-green-600"
              >
                <div>Staged Files</div>
                <button
                  class="mx-1 shadow-inner rounded-full p-1"
                  @click="
                    unstageAllStagedFilesAction({
                      directory: $route.query.directory,
                    })
                  "
                >
                  <FontAwesomeIcon
                    class="h-7 text-yellow-400"
                    :icon="['fas', 'minus']"
                  />
                </button>
              </div>
              <div v-if="stagedFiles.length !== 0">
                <div
                  v-for="(file, index) in stagedFiles"
                  :key="index"
                  class="p-2 flex justify-between my-1 hover:bg-indigo-900 rounded-xl transition duration-200"
                  :class="index % 2 ? 'bg-gray-900' : 'bg-gray-700'"
                >
                  <div class="font-mono justify-items-center">
                    <div class="text-white">
                      {{ file.name | getFilename }}
                    </div>
                    <div class="ml-2 text-sm text-gray-300">
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
              <div v-else class="h-28 flex text-white">
                <FontAwesomeIcon
                  class="h-20 m-auto"
                  :icon="['fas', 'folder-open']"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex flex-wrap my-auto flex-">
        <CommitMessageForm />
      </div>
      <div class="flex flex-grow text-pink-600">
        <NuxtLink :to="{ name: 'index' }" class="m-auto">
          <FontAwesomeIcon
            class="h-12 hover:text-gray-50 transition duration-150 ease-in-out"
            :icon="['fas', 'home']"
          />
        </NuxtLink>
        <button
          class="m-auto"
          @click="fetchStatusAction({ directory: $route.query.directory })"
        >
          <FontAwesomeIcon
            class="h-12 hover:text-gray-50 transition duration-150 ease-in-out"
            :icon="['fas', 'sync']"
          />
        </button>
      </div>
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
      stageAllUntrackedFilesAction: 'repository/stageAllUntrackedFiles',
      stageAllModifiedFilesAction: 'repository/stageAllModifiedFiles',
      discardAllModifiedFilesAction: 'repository/discardAllModifiedFiles',
      unstageAllStagedFilesAction: 'repository/unstageAllStagedFiles',
    }),
  },
}
</script>

<style scoped>
::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
}

::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #ee2828;
}
.untracked-files-enter-active,
.untracked-files-leave-active {
  transition: all 1s;
}
.untracked-files-enter,
.untracked-files-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
.untracked-files-move {
  transition: transform 1s;
}
</style>
