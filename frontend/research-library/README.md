# research-library

Part of [`frontend`](../README.md) in the COSMOS platform.

**Status:** Phase 2 of 8 — implemented.

Search and browse `data-platform/data-ingestion`'s sources
(`backend/search-service` under the hood), each shown with a colored
badge for its `evidence_status`. Signed-in users get a form to add a
new source; signed-out visitors get a sign-in prompt instead. Plain
HTML/JS, no build step - same pattern as `frontend/login` and
`frontend/dashboard`.
