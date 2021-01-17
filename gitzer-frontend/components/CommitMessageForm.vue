<template>
  <form
    class="bg-green-200 container mx-auto h-64"
    @submit.prevent="submitCommit()"
  >
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
    <input v-model="formData.commitScope" type="text" name="scope" required />
    <input
      v-model="formData.commitSummary"
      type="text"
      name="summary"
      required
    />
    <input
      v-model="formData.commitInfo"
      type="text"
      name="commit-info"
      required
    />
    <button type="submit">Commit</button>
  </form>
</template>

<script>
export default {
  data: () => ({
    formData: {
      commitType: 'fix',
      commitScope: 'views.py',
      commitSummary: 'summary for this change',
      commitInfo: 'this is a complete info of the change',
    },
  }),
  methods: {
    submitCommit() {
      this.$emit('commit-change', this.formData)
    },
  },
}
</script>
