<template>
  <div class="flex-grow">
    <form class="m-4" @submit.prevent="commitChange(formData)">
      <div
        class="text-3xl text-center font-serif text-blue-500 bg-black p-5 rounded-3xl ring ring-green-600"
      >
        Commit
      </div>

      <div
        class="flex text-sm sm:text-base md:text-lg flex-wrap mt-4 font-mono"
      >
        <div class="w-3/5 flex flex-col">
          <div class="mx-2 text-purple-200">Type of commit*:</div>
          <select
            v-model="formData.commitType"
            class="m-3 ring ring-purple-600 rounded-lg"
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
          <div class="m-3 flex">
            <input
              v-model="formData.commitScope"
              type="text"
              class="w-1/2 ring ring-purple-600 rounded-lg"
              name="scope"
            />
            <button
              type="button"
              class="w-1/2 ml-2 bg-purple-900 ring ring-purple-600 rounded-lg"
              @click="setScope()"
            >
              Automatic Scope
            </button>
          </div>
          <div class="mx-2 text-purple-200">Summary of commit*:</div>
          <input
            v-model="formData.commitSummary"
            type="text"
            class="m-3 ring ring-purple-600 rounded-lg"
            name="summary"
            required
          />
        </div>
        <div class="flex flex-col w-2/5">
          <div class="mx-2 text-purple-200">Additional information:</div>
          <textarea
            v-model="formData.commitInfo"
            class="h-full resize-none m-3 ring ring-purple-600 rounded-lg"
            type="text"
            name="commit-info"
          />
        </div>
        <button
          class="w-full mx-2 bg-purple-900 ring ring-purple-600 rounded-lg"
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
      commitType: 'fix',
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
      performCommitAction: 'repository/commitChange',
    }),
    setScope() {
      this.formData.commitScope = this.commitScopeGetter
    },
    commitChange(formData) {
      let commitMessage = `${formData.commitType}`
      if (formData.commitScope) {
        commitMessage += `(${formData.commitScope})`
      }
      commitMessage += `: ${formData.commitSummary}`
      if (formData.commitInfo) {
        commitMessage += `\n\n${formData.commitInfo}`
      }
      this.performCommitAction({
        commitMessage,
        directory: this.$route.query.directory,
      })
    },
  },
}
</script>
