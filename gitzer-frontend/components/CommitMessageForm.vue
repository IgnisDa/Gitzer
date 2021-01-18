<template>
  <form class="container mx-auto h-64" @submit.prevent="commitChange(formData)">
    <div>Commit</div>
    <select v-model="formData.commitType">
      <option value="">Please select one</option>
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
    <input
      v-model="formData.commitScope"
      class="w-full"
      type="text"
      name="scope"
      required
    />
    <input
      v-model="formData.commitSummary"
      type="text"
      name="summary"
      required
    />
    <input v-model="formData.commitInfo" type="text" name="commit-info" />
    <button type="submit">Commit</button>
    {{ commitScopeGetter }}
    <button @click="setScope()">Set Scope</button>
  </form>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  data: () => ({
    formData: {
      commitType: 'fix',
      commitScope: 'views.py',
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
