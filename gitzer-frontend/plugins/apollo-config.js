export default (context) => {
  return {
    httpEndpoint: process.env.BACKEND_URL || 'http://0.0.0.0:8000/graphql/',
  }
}