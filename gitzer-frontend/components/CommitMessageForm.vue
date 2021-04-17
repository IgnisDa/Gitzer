<template>
  <div class="flex-grow">
    <hotkeys @submitForm="commitChange()"></hotkeys>
    <form class="m-4" @submit.prevent="commitChange()">
      <div
        class="p-5 font-serif text-3xl text-center text-blue-500 bg-black rounded-3xl ring ring-green-600"
      >
        Commit
      </div>

      <div
        class="flex flex-wrap mt-4 font-mono text-sm sm:text-base md:text-lg"
      >
        <div class="flex flex-col w-3/5">
          <div class="mx-2 text-purple-200">Type of commit*:</div>
          <select
            v-model="formData.commitType"
            class="m-3 rounded-lg ring ring-purple-600"
          >
            <option value="">Choose</option>
            <option>fix</option>
            <option>feat</option>
            <option>docs</option>
            <option>style</option>
            <option>refactor</option>
            <option>perf</option>
            <option>test</option>
            <option>build</option>
            <option>ci</option>
          </select>
          <div class="mx-2 text-purple-200">Scope of commit*:</div>
          <div class="flex m-3">
            <input
              v-model="formData.commitScope"
              type="text"
              class="w-1/2 rounded-lg ring ring-purple-600"
              name="scope"
            />
            <button
              type="button"
              class="w-1/2 ml-2 bg-purple-900 rounded-lg ring ring-purple-600"
              @click="setScope()"
            >
              Automatic Scope
            </button>
          </div>
          <div class="mx-2 text-purple-200">Summary of commit*:</div>
          <input
            v-model="formData.commitSummary"
            type="text"
            class="m-3 rounded-lg ring ring-purple-600"
            name="summary"
            required
          />
        </div>
        <div class="flex flex-col w-2/5">
          <div class="mx-2 text-purple-200">Additional information:</div>
          <textarea
            v-model="formData.commitInfo"
            class="h-full m-3 rounded-lg resize-none ring ring-purple-600"
            type="text"
            name="commit-info"
          />
        </div>
        <button
          class="w-full mx-2 bg-purple-900 rounded-lg ring ring-purple-600"
          type="submit"
        >
          Commit
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  data: () => ({
    formData: {
      commitType: 'feat',
      commitScope: '',
      commitSummary: '',
      commitInfo: '',
    },
  }),
  computed: {
    ...mapGetters({
      commitScopeGetter: 'repository/commitScope',
    }),
  },
  methods: {
    ...mapActions({
      performCommitAction: 'repository/performCommit',
    }),
    resetCommit() {
      this.formData.commitType = 'feat'
      this.formData.commitScope = ''
      this.formData.commitSummary = ''
      this.formData.commitInfo = ''
    },
    setScope() {
      this.formData.commitScope = this.commitScopeGetter
    },
    commitChange() {
      const formData = this.formData
      let commitMessage = `${formData.commitType}`
      if (formData.commitScope) {
        commitMessage += `(${formData.commitScope})`
      }
      commitMessage += `: ${formData.commitSummary}`
      if (formData.commitInfo) {
        commitMessage += `\n\n${formData.commitInfo}`
      }
      // console.log(commitMessage)
      this.performCommitAction({
        commitMessage,
        directory: this.$route.query.directory,
      }).then(() => {
        this.resetCommit()
      })
    },
  },
}
</script>
