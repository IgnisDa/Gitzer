<template>
  <div
    class="flex w-full min-h-screen from-indigo-900 bg-gradient-to-b to-gray-800"
  >
    <div class="container flex flex-col mx-auto">
      <div class="flex flex-grow">
        <div class="flex flex-wrap flex-grow my-auto">
          <div
            class="relative w-full p-2 overflow-x-hidden overflow-y-auto rounded-lg md:w-1/3 max-h-80"
          >
            <div class="px-1 shadow-lg">
              <div
                class="sticky top-0 flex items-center justify-between p-3 font-serif text-3xl text-blue-500 bg-black rounded-3xl ring ring-green-600"
              >
                <div>Untracked Files</div>
                <button
                  title="Stage All Files"
                  class="p-1 mx-1 rounded-full shadow-inner"
                  @click="
                    stageAllUntrackedFilesAction({
                      directory: $route.query.directory,
                    })
                  "
                >
                  <FontAwesomeIcon
                    class="text-yellow-400 h-7"
                    :icon="['fas', 'plus']"
                  />
                </button>
              </div>
              <div v-if="untrackedFiles.length !== 0">
                <transition-group tag="div" name="files">
                  <div
                    v-for="(file, index) in untrackedFiles"
                    :key="index + 0"
                    class="flex justify-between p-2 my-1 transition duration-200 hover:bg-indigo-900 rounded-xl"
                    :class="index % 2 ? 'bg-gray-900' : 'bg-gray-700'"
                  >
                    <div class="flex items-center justify-between">
                      <div
                        class="mr-2 font-extrabold text-green-500"
                        title="Change type: Untracked"
                      >
                        {{ file.changeType }}
                      </div>
                      <div class="ml-2 font-mono justify-items-center">
                        <div class="text-white">
                          {{ file.name | getFilename }}
                        </div>
                        <div class="ml-2 text-sm text-gray-300">
                          {{ file.name | getFileRoot }}
                        </div>
                      </div>
                    </div>
                    <div class="flex items-center">
                      <button
                        class="p-1 mx-1 rounded-full shadow-inner"
                        title="Stage File"
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
              <div v-else class="flex text-white h-28">
                <FontAwesomeIcon
                  class="h-20 m-auto"
                  :icon="['fas', 'folder-open']"
                />
              </div>
            </div>
          </div>
          <div
            class="relative w-full p-2 overflow-x-hidden overflow-y-auto rounded-lg md:w-1/3 max-h-80"
          >
            <div class="px-1 shadow-lg">
              <div
                class="sticky top-0 flex items-center justify-between p-3 font-serif text-3xl text-blue-500 bg-black rounded-3xl ring ring-green-600"
              >
                <div>Modified Files</div>
                <div>
                  <button
                    title="Stage All Files"
                    class="p-1 mx-1 rounded-full shadow-inner"
                    @click="
                      stageAllModifiedFilesAction({
                        directory: $route.query.directory,
                      })
                    "
                  >
                    <FontAwesomeIcon
                      class="text-yellow-400 h-7"
                      :icon="['fas', 'plus']"
                    />
                  </button>
                  <button
                    class="p-1 mx-1 rounded-full shadow-inner"
                    title="Discard All Modified Files"
                    @click="
                      discardAllModifiedFilesAction({
                        directory: $route.query.directory,
                      })
                    "
                  >
                    <FontAwesomeIcon
                      class="text-yellow-400 h-7"
                      :icon="['fas', 'trash']"
                    />
                  </button>
                </div>
              </div>
              <div v-if="modifiedFiles.length !== 0">
                <transition-group tag="div" name="files">
                  <div
                    v-for="(file, index) in modifiedFiles"
                    :key="index + 0"
                    class="flex justify-between p-2 my-1 transition duration-200 hover:bg-indigo-900 rounded-xl"
                    :class="index % 2 ? 'bg-gray-900' : 'bg-gray-700'"
                  >
                    <div class="flex items-center justify-between">
                      <div
                        class="mr-2 font-extrabold"
                        :class="changeTypeColor(file.changeType)"
                        :title="changeTypeTitle(file.changeType)"
                      >
                        {{ file.changeType }}
                      </div>
                      <div class="ml-2 font-mono justify-items-center">
                        <div class="text-white">
                          {{ file.name | getFilename }}
                        </div>
                        <div class="ml-2 text-sm text-gray-300">
                          {{ file.name | getFileRoot }}
                        </div>
                      </div>
                    </div>
                    <div class="flex items-center">
                      <button
                        title="Stage Changes"
                        class="p-1 mx-1 rounded-full shadow-inner"
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
                        class="p-1 mx-1 rounded-full shadow-inner"
                        title="Discard Changes"
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
                </transition-group>
              </div>
              <div v-else class="flex text-white h-28">
                <FontAwesomeIcon
                  class="h-20 m-auto"
                  :icon="['fas', 'folder-open']"
                />
              </div>
            </div>
          </div>
          <div
            class="relative w-full p-2 overflow-x-hidden overflow-y-auto rounded-lg md:w-1/3 max-h-80"
          >
            <div class="px-1 shadow-lg">
              <div
                class="sticky top-0 flex items-center justify-between p-3 font-serif text-3xl text-blue-500 bg-black rounded-3xl ring ring-green-600"
              >
                <div>Staged Files</div>
                <button
                  class="p-1 mx-1 rounded-full shadow-inner"
                  title="Unstage All Changes"
                  @click="
                    unstageAllStagedFilesAction({
                      directory: $route.query.directory,
                    })
                  "
                >
                  <FontAwesomeIcon
                    class="text-yellow-400 h-7"
                    :icon="['fas', 'minus']"
                  />
                </button>
              </div>
              <div v-if="stagedFiles.length !== 0">
                <transition-group tag="div" name="files">
                  <div
                    v-for="(file, index) in stagedFiles"
                    :key="index + 1"
                    class="flex justify-between p-2 my-1 transition duration-200 hover:bg-indigo-900 rounded-xl"
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
                        class="p-1 mx-1 rounded-full shadow-inner"
                        title="Unstage File"
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
                </transition-group>
              </div>
              <div v-else class="flex text-white h-28">
                <FontAwesomeIcon
                  class="h-20 m-auto"
                  :icon="['fas', 'folder-open']"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex flex-none">
        <CommitMessageForm />
      </div>
      <div class="flex-none my-3 md:mb-14 md:mt-8">
        <git-actions></git-actions>
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
    try {
      this.fetchStatusAction({ directory: this.$route.query.directory })
    } catch {
      this.$addAlert({
        severity: 'danger',
        messageHeading: 'Illegal path',
        messageBody:
          'The directory you requested is not a valid git repository',
        active: true,
      })
      this.$router.push({ name: 'index' })
      return
    } finally {
      this.interval = setInterval(
        function () {
          this.fetchStatusAction({ directory: this.$route.query.directory })
        }.bind(this),
        10000
      )
    }
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
    changeTypeTitle(changeType) {
      if (changeType === 'D') {
        return 'Change type: Deleted'
      } else {
        return 'Change type: Modified'
      }
    },
    changeTypeColor(changeType) {
      if (changeType === 'D') {
        return 'text-pink-600'
      } else {
        return 'text-blue-400'
      }
    },
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
.files-enter-active,
.files-leave-active {
  transition: all 1s;
}
.files-enter,
.files-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
.files-move {
  transition: transform 1s;
}
</style>
