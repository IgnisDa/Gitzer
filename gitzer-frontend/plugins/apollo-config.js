export default (context) => {
  return {
    httpEndpoint:
      context.$config.backendUrl || 'http://127.0.0.1:8534/graphql/',
  }
}
