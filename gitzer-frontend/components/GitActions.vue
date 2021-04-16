<template>
  <div class="flex items-center justify-around text-lime-100">
    <NuxtLink :to="{ name: 'index' }" title="Home" class="text-[12px]">
      <IgIcon
        name="home"
        class="w-8 h-8 transition duration-300 ease-in-out lg:h-14 lg:w-14 md:h-12 md:w-12 sm:h-10 sm:w-10 hover:text-red-600 text-lime-200"
        no-size
        no-color
      ></IgIcon>
    </NuxtLink>
    <button
      class="appearance-none focus:outline-none"
      title="Refresh status"
      @click="fetchStatusAction({ directory: $route.query.directory })"
    >
      <IgIcon
        name="refresh-cw"
        class="w-8 h-8 transition duration-300 ease-in-out lg:h-14 lg:w-14 md:h-12 md:w-12 sm:h-10 sm:w-10 hover:text-red-600 text-lime-200"
        no-size
        no-color
      ></IgIcon>
    </button>
    <button
      class="appearance-none focus:outline-none"
      :title="`Push '${branch}' branch to 'origin'`"
      @click="pushToOrigin()"
    >
      <IgIcon
        name="chevrons-up"
        class="w-8 h-8 transition duration-300 ease-in-out lg:h-14 lg:w-14 md:h-12 md:w-12 sm:h-10 sm:w-10 hover:text-red-600 text-lime-200"
        :class="{ 'animate-bounce': loading }"
        no-size
        no-color
      ></IgIcon>
    </button>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  data: () => ({
    loading: false,
  }),
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
    async pushToOrigin() {
      this.loading = true
      await this.pushToOriginAction({ directory: this.$route.query.directory })
      this.loading = false
    },
  },
}
</script>
