export default (context) => {
  return {
    httpEndpoint: context.$config.backendUrl,
  }
}
