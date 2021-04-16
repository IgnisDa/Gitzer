<template>
  <column-base title="Untracked Files">
    <template #column-commands>
      <column-button
        title="Stage All Files"
        icon="plus"
        @click.native="
          stageAllUntrackedFilesAction({
            directory: $route.query.directory,
          })
        "
      >
      </column-button>
    </template>
    <template #body>
      <column-files-collection type="untrackedFiles"></column-files-collection>
    </template>
  </column-base>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  methods: {
    ...mapActions({
      stageAllUntrackedFilesAction: 'repository/stageAllUntrackedFiles',
    }),
  },
}
</script>
