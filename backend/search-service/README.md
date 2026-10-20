# search-service

Part of [`backend`](../README.md) in the COSMOS platform.

**Status:** Phase 2 of 8 — implemented.

Pure-Python token scoring over `data-platform/data-ingestion`'s
sources (`search.py`'s `search_sources()`) — title matches rank above
abstract-only matches, with an optional `evidence_status` filter.
Deliberately not SQLite FTS5: that's a compile-time SQLite feature,
and this repo would rather stay portable across whatever Python/SQLite
build is in use than depend on it silently being present everywhere.

Exposed via `backend/api-gateway`'s `GET /api/sources?q=...`. Tests:
`tests/test_search.py`.
