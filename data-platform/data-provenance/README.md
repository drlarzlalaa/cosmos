# data-provenance

Part of [`data-platform`](../README.md) in the COSMOS platform.

**Status:** implemented (alongside the `engines/physics-engine/gravity`
slice - both out of strict roadmap order, together).

Saves a result an engine actually computed, not a user's claim about
one. `provenance.py`'s `ProvenanceStore.record_finding()` only ever
stores a `result` the caller (`backend/api-gateway`) got back from
re-running the named engine's `compute()` server-side - the client's
own request can't set the stored result, only the `engine`,
`calculation`, and `inputs` that get recomputed. Backed by the
`computed_findings` table in
[`storage/relational-database`](../../storage/relational-database/).

Exposed via `backend/api-gateway`'s `/api/findings` endpoints; tried
live at `/physics-explorer/`'s "Save as a provenance-tracked finding"
button. Tests: `tests/test_provenance.py` (including the API-level
check that a client-supplied `result` is ignored in favor of the
server's own recomputation).
