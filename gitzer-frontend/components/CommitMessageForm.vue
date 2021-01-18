<template>
  <div class="flex-grow">
    <form class="m-4" @submit.prevent="commitChange(formData)">
      <div
        class="text-3xl text-center font-serif text-blue-800 bg-black p-5 rounded-3xl"
      >
        Commit
      </div>

      <div class="flex text-sm sm:text-base md:text-lg flex-wrap">
        <div class="w-3/5 flex flex-col">
          <div class="mx-2 text-blue-600">Type of commit*:</div>
          <select v-model="formData.commitType" class="m-2">
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
          <div class="mx-2 text-blue-600">Scope of commit*:</div>
          <div class="m-2 flex">
            <input
              v-model="formData.commitScope"
              type="text"
              class="w-1/2"
              name="scope"
              required
            />
            <button
              type="button"
              class="w-1/2 ml-2 bg-purple-900"
              @click="setScope()"
            >
              Automatic Scope
            </button>
          </div>
          <div class="mx-2 text-blue-600">Summary of commit*:</div>
          <input
            v-model="formData.commitSummary"
            type="text"
            class="m-2"
            name="summary"
            required
          />
        </div>
        <div class="flex flex-col w-2/5">
          <div class="mx-2 text-blue-600">Additional information:</div>
          <textarea
            v-model="formData.commitInfo"
            class="h-full resize-none m-2"
            type="text"
            name="commit-info"
          />
        </div>
        <button class="w-full mx-2 bg-purple-900" type="submit">Commit</button>
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
      commitChangeAction: 'repository/commitChange',
    }),
    setScope() {
      this.formData.commitScope = this.commitScopeGetter
    },
    commitChange(formData) {
      let commitMessage = `${formData.commitType}(${formData.commitScope}): ${formData.commitSummary}`
      if (formData.commitInfo) {
        commitMessage += `\n\n${formData.commitInfo}`
      }
      this.commitChangeAction({
        commitMessage,
        directory: this.$route.query.directory,
      })
    },
  },
}
</script>
