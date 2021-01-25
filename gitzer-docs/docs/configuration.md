---
id: configuration
title: Configuration
---

Gitzer reads the following environment variables for its configuration:

1. `GITZER_FRONTEND_HOST`: The host to use to launch the frontend server. Defaults
   to `"127.0.0.1"`.
2. `GITZER_BACKEND_HOST`: The host to use to launch the backend server. Defaults
   to `"127.0.0.1"`.
3. `GITZER_DONT_START_BROWSER`: If set to `"1"`, Gitzer will not attempt to start a
   new browser session when started. Useful when it is being used in a remote
   development environment.
