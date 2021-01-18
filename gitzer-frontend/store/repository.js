import performCommitMutation from '~/apollo/mutations/performCommit.gql'
import statusQuery from '~/apollo/queries/status.gql'

export const state = () => ({
  stagedFiles: [],
  modifiedFiles: [],
  untrackedFiles: [],
})

export const mutations = {
  addStagedFile(state, filename) {
    state.stagedFiles.push(filename)
  },
  setStagedFiles(state, files) {
    state.stagedFiles = files
  },
  removeStagedFile(state, filename) {
    const index = state.stagedFiles.indexOf(filename)
    state.stagedFiles.splice(index, 1)
  },
  addModifiedFile(state, filename) {
    state.modifiedFiles.push(filename)
  },
  setModifiedFiles(state, files) {
    state.modifiedFiles = files
  },
  removeModifiedFile(state, filename) {
    const index = state.modifiedFiles.indexOf(filename)
    state.modifiedFiles.splice(index, 1)
  },
  addUntrackedFile(state, filename) {
    state.untrackedFiles.push(filename)
  },
  setUntrackedFiles(state, files) {
    state.untrackedFiles = files
  },
  removeUntrackedFile(state, filename) {
    const index = state.untrackedFiles.indexOf(filename)
    state.untrackedFiles.splice(index, 1)
  },
}

export const actions = {
  async fetchStatus({ commit }, payload) {
    const apolloClient = this.app.apolloProvider.defaultClient
    const { data } = await apolloClient.query({
      query: statusQuery,
      variables: { directory: payload.directory },
    })
    commit('setStagedFiles', data.status.stagedFiles)
    commit('setModifiedFiles', data.status.modifiedFiles)
    commit('setUntrackedFiles', data.status.untrackedFiles)
  },
  async commitChange({ dispatch, commit }, payload) {
    const apolloClient = this.app.apolloProvider.defaultClient
    await apolloClient
      .mutate({
        mutation: performCommitMutation,
        variables: {
          message: payload.commitMessage,
          directory: payload.directory,
        },
      })
      .then((result) => {
        this.refetchStatus()
      })
      .catch((err) => {
        console.log(err)
      })
  },
}
