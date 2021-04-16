<template>
  <div
    class="flex w-full h-screen from-indigo-900 bg-gradient-to-b to-gray-800"
  >
    <div class="flex flex-col w-full h-full mx-auto 2xl:w-4/5">
      <div
        class="flex flex-wrap justify-center flex-grow overflow-hidden files--area"
      >
        <record-untracked-column></record-untracked-column>
        <record-modified-column></record-modified-column>
        <record-staged-column></record-staged-column>
      </div>
      <div class="flex-none my-3 md:mb-14 md:mt-8">
        <git-actions></git-actions>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import GitActions from '../components/GitActions.vue'

export default {
  components: { GitActions },
  head: () => ({
    title: 'Status',
  }),
  mounted() {
    this.fetchStatusAction({ directory: this.$route.query.directory })
    this.interval = setInterval(
      function () {
        this.fetchStatusAction({ directory: this.$route.query.directory })
      }.bind(this),
      10000
    )
  },
  beforeDestroy() {
    clearInterval(this.interval)
  },
  methods: {
    ...mapActions({
      fetchStatusAction: 'repository/fetchStatus',
    }),
  },
}
</script>

<style lang="scss">
.files--area {
  ::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    border-radius: 10px;
  }

  ::-webkit-scrollbar {
    width: 12px;
  }

  ::-webkit-scrollbar-thumb {
    border-radius: 10px;
    -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    background-color: #ee2828;
  }
  .files-enter-active,
  .files-leave-active {
    transition: all 1s;
  }
  .files-enter,
  .files-leave-to {
    opacity: 0;
    transform: translateX(-30px);
  }
  .files-move {
    transition: transform 1s;
  }
}
</style>
