<template>
  <div class="min-h-screen container">
    <client-only>
      <div v-if="loading">Loading your repository...</div>
    </client-only>
    <button class="bg-green-300" @click="$apollo.queries.status.refetch()">
      Refetch
    </button>
    <div v-if="status" class="container">
      <div class="flex flex-wrap overflow-hidden">
        <div class="h-100 w-full md:w-1/3 overflow-hidden">
          <div>Untracked Files</div>
          <div>
            <div v-if="status.untrackedFiles.length">
              <div v-for="(file, index) in status.untrackedFiles" :key="index">
                {{ file.name }}
              </div>
            </div>
            <div v-else>No files</div>
          </div>
        </div>

        <div class="h-100 w-full md:w-1/3 overflow-hidden">
          <div>Modified Files</div>
          <div>
            <div v-if="status.untrackedFiles.length">
              <div v-for="(file, index) in status.modifiedFiles" :key="index">
                {{ file.name }}
              </div>
            </div>
            <div v-else>No files</div>
          </div>
        </div>

        <div class="h-100 w-full md:w-1/3 overflow-hidden">
          <div>Staged Files</div>
          <div>
            <div v-if="status.stagedFiles.length !== 0">
              <div v-for="(file, index) in status.stagedFiles" :key="index">
                {{ file.name }}
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
import statusQuery from '~/apollo/status.gql'

export default {
  data: () => ({ loading: 0 }),
  head: () => ({
    title: 'Status',
  }),
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
    },
  },
}
</script>
