<template>
  <div class="flex justify-around items-center text-lime-100">
    <NuxtLink :to="{ name: 'index' }" title="Home">
      <FontAwesomeIcon
        class="h-12 hover:text-red-600 transition duration-300 ease-in-out"
        :icon="['fas', 'home']"
      />
    </NuxtLink>
    <button
      class="appearance-none focus:outline-none"
      title="Refresh status"
      @click="fetchStatusAction({ directory: $route.query.directory })"
    >
      <FontAwesomeIcon
        class="h-12 hover:text-red-600 transition duration-300 ease-in-out"
        :icon="['fas', 'sync']"
      />
    </button>
    <button
      class="appearance-none focus:outline-none"
      :title="`Push '${branch}' branch to 'origin'`"
      @click="pushToOriginAction({ directory: $route.query.directory })"
    >
      <FontAwesomeIcon
        class="h-12 hover:text-red-600 transition duration-300 ease-in-out"
        :icon="['fas', 'arrow-up']"
      />
    </button>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  computed: {
    ...mapState({
      branch: (state) => state.repository.branch,
    }),
  },
  methods: {
    ...mapActions({
      fetchStatusAction: 'repository/fetchStatus',
      pushToOriginAction: 'repository/pushToOrigin',
    }),
  },
}
</script>
