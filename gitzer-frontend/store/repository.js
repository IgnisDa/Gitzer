import performCommitMutation from '~/apollo/mutations/performCommit.gql'
import statusQuery from '~/apollo/queries/status.gql'
import discardFileChangeMutation from '~/apollo/mutations/discardFileChange.gql'
import stageFileMutation from '~/apollo/mutations/stageFile.gql'
import unstageFileMutation from '~/apollo/mutations/unstageFile.gql'

export const state = () => ({
  stagedFiles: [],
  modifiedFiles: [],
  untrackedFiles: [],
})

export const getters = {
  commitScope: (state) => {
    const files = []
    for (const file of state.stagedFiles) {
      const array = file.name.split('/')
      files.push(array[array.length - 1])
    }
    return files.join(', ')
  },
}

export const mutations = {
  setStagedFiles(state, files) {
    state.stagedFiles = files
  },
  setModifiedFiles(state, files) {
    state.modifiedFiles = files
  },
  setUntrackedFiles(state, files) {
    state.untrackedFiles = files
  },
}

export const actions = {
  async fetchStatus({ commit }, payload) {
    const apolloClient = this.app.apolloProvider.defaultClient
    const { data } = await apolloClient.query({
      query: statusQuery,
      variables: { directory: payload.directory },
      // we set the fetchPolicy to 'network-only' to ensure that apollo always
      // fetches data from the backend. This ensures that our list of files
      // does not become stale
      fetchPolicy: 'network-only',
    })
    commit('setStagedFiles', data.status.stagedFiles)
    commit('setModifiedFiles', data.status.modifiedFiles)
    commit('setUntrackedFiles', data.status.untrackedFiles)
  },
  stageFile({ dispatch }, payload) {
    const apolloClient = this.app.apolloProvider.defaultClient
    apolloClient
      .mutate({
        mutation: stageFileMutation,
        variables: {
          data: {
            filename: payload.filename,
            directory: payload.directory,
          },
        },
      })
      .then(() => {
        dispatch('fetchStatus', { directory: payload.directory })
      })
      .catch((err) => {
        alert(err)
      })
  },
  unstageFile({ dispatch }, payload) {
    const apolloClient = this.app.apolloProvider.defaultClient
    apolloClient
      .mutate({
        mutation: unstageFileMutation,
        variables: {
          data: {
            filename: payload.filename,
            directory: payload.directory,
          },
        },
      })
      .then(() => {
        dispatch('fetchStatus', { directory: payload.directory })
      })
      .catch((err) => {
        alert(err)
      })
  },
  async discardFileChange({ dispatch }, payload) {
    const apolloClient = this.app.apolloProvider.defaultClient
    await apolloClient
      .mutate({
        mutation: discardFileChangeMutation,
        variables: {
          data: {
            filename: payload.filename,
            directory: payload.directory,
          },
        },
      })
      .then(() => {
        dispatch('fetchStatus', { directory: payload.directory })
      })
      .catch((err) => {
        alert(err)
      })
  },
  async commitChange({ dispatch }, payload) {
    const apolloClient = this.app.apolloProvider.defaultClient
    await apolloClient
      .mutate({
        mutation: performCommitMutation,
        variables: {
          message: payload.commitMessage,
          directory: payload.directory,
        },
      })
      .then(() => {
        dispatch('fetchStatus', { directory: payload.directory })
      })
      .catch((err) => {
        alert(err)
      })
  },
}
