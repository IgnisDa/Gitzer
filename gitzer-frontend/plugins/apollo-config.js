export default (context) => {
  return {
    httpEndpoint: process.env.BACKEND_URL || 'http://127.0.0.1:8534/graphql/',
  }
}
