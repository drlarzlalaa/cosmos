# data-ingestion

Part of [`data-platform`](../README.md) in the COSMOS platform.

**Status:** Phase 2 of 8 — implemented.

Takes in research-library entries ("sources": a title, abstract,
optional URL/authors, and a required `evidence_status` of
`established` / `open_question` / `speculative`) and enforces that tag
server-side — see `ingestion.py`'s `SourceStore`. Backed by the
`sources` table in [`storage/relational-database`](../../storage/relational-database/).

Exposed via `backend/api-gateway`'s `/api/sources` endpoints and
browsable at `/research-library/`. Tests: `tests/test_ingestion.py`.
