<template>
  <div
    v-if="$store.state.repository[type].length === 0"
    class="flex items-center justify-center"
  >
    <div class="flex items-center space-x-3">
      <IgIcon
        name="x-octagon"
        class="text-purple-200"
        size="xl"
        no-color
      ></IgIcon>
      <div class="font-extrabold text-center text-white uppercase">
        **Cricket Noise**
      </div>
      <IgIcon
        name="x-octagon"
        class="text-purple-200"
        size="xl"
        no-color
      ></IgIcon>
    </div>
  </div>
  <div v-else class="flex flex-col space-y-0.5">
    <div v-for="(file, index) in $store.state.repository[type]" :key="index">
      <column-file-isolated
        :file="file"
        class="bg-opacity-95"
        :class="index % 2 == 0 ? 'bg-gray-800' : 'bg-warm-gray-800'"
      >
        <template #file-actions>
          <div v-if="type === 'untrackedFiles'" class="flex items-center">
            <column-button
              icon="plus"
              title="Stage this file"
              class="text-rose-600"
              no-color
              @click.native="
                stageFileAction({
                  filename: file.name,
                  directory: $route.query.directory,
                })
              "
            ></column-button>
          </div>
          <div v-else-if="type === 'modifiedFiles'" class="flex items-center">
            <column-button
              icon="plus"
              title="Stage changes"
              class="text-rose-600"
              no-color
              @click.native="
                stageFileAction({
                  filename: file.name,
                  directory: $route.query.directory,
                })
              "
            ></column-button>
            <column-button
              icon="trash"
              title="Discard changes"
              class="text-rose-600"
              no-color
              @click.native="
                discardFileChangeAction({
                  filename: file.name,
                  directory: $route.query.directory,
                })
              "
            ></column-button>
          </div>
          <div v-else class="flex items-center">
            <column-button
              icon="minus"
              title="Unstage file"
              class="text-rose-600"
              no-color
              @click.native="
                unstageFileAction({
                  filename: file.name,
                  directory: $route.query.directory,
                })
              "
            ></column-button>
          </div>
        </template>
      </column-file-isolated>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  props: {
    type: {
      required: true,
      type: String,
    },
  },
  methods: {
    ...mapActions({
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
