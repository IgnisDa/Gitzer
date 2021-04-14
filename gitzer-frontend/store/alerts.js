export const state = () => ({
  alerts: [],
})

export const getters = {
  activeAlerts(state) {
    const alerts = state.alerts.filter((alert) => {
      return alert.active
    })
    return alerts
  },
}

export const mutations = {
  addAlert(state, alertObj) {
    // add an alert to the vuex store
    state.alerts.push(alertObj)
  },
  disableAlert(state, id) {
    // sets the active state of a `id`th alert to `false`
    const index = state.alerts.findIndex((alert) => alert.id === id)
    state.alerts[index].active = false
  },
}

export const actions = {
  addAlert({ commit, state }, payload) {
    // append an alert to the vuex store, along with it's correct `id`
    const id = state.alerts.length
    payload = { ...payload, id }
    commit('addAlert', payload)
  },
  disableAlert({ commit }, payload) {
    commit('disableAlert', payload)
  },
}
