<template>
  <column-base title="Staged Files">
    <template #column-commands>
      <column-button
        title="Unstage All Changes"
        icon="minus"
        @click.native="
          unstageAllStagedFilesAction({
            directory: $route.query.directory,
          })
        "
      >
      </column-button>
    </template>
    <template #body>
      <column-files-collection type="stagedFiles"></column-files-collection>
    </template>
  </column-base>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  methods: {
    ...mapActions({
      unstageAllStagedFilesAction: 'repository/unstageAllStagedFiles',
    }),
  },
}
</script>
