<template>
  <column-base title="Modified Files">
    <template #column-commands>
      <column-button
        title="Stage All Files"
        icon="plus"
        @click.native="
          stageAllModifiedFilesAction({
            directory: $route.query.directory,
          })
        "
      >
      </column-button>
      <column-button
        title="Discard All Modified Files"
        icon="trash"
        @click.native="
          discardAllModifiedFilesAction({
            directory: $route.query.directory,
          })
        "
      >
      </column-button>
    </template>
    <template #body>
      <column-files-collection type="modifiedFiles"></column-files-collection>
    </template>
  </column-base>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  methods: {
    ...mapActions({
      discardAllModifiedFilesAction: 'repository/discardAllModifiedFiles',
      stageAllModifiedFilesAction: 'repository/stageAllModifiedFiles',
    }),
  },
}
</script>
