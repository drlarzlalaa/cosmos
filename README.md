# COSMOS

**Universal Law Discovery System.**

COSMOS is an open-source research platform that investigates the
fundamental principles of the universe through scientific research,
mathematical modelling, AI, simulations, and philosophical inquiry —
while trying hard never to blur the line between what's actually known
and what's merely hoped for.

Its defining feature is keeping three things clearly separated, in the
code and in every finding it produces:

- **Established knowledge** — supported by strong, reproducible evidence.
- **Open scientific questions** — researchable, but not yet resolved.
- **Speculative hypotheses** — ideas with no evidential support yet.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full planned structure
(frontend, backend, eight research engines, an AI intelligence layer,
a knowledge graph, and the validation pipeline that keeps discoveries
honest) and [ROADMAP.md](ROADMAP.md) for the build order.

## Status: Phase 2 of 8 (core), plus one early Phase 3 slice

This is a young project. What's real today:

- Accounts: register / log in, password hashing (PBKDF2), signed
  session tokens — all stdlib, no third-party auth library.
- A research library: add a source (title, abstract, optional
  url/authors) tagged `established` / `open_question` / `speculative`
  — enforced server-side, not just asserted in this README — and
  search it (`backend/search-service`, pure-Python token scoring, no
  SQLite FTS5 dependency).
- A physics engine calculator (`engines/physics-engine/gravity`):
  closed-form Newtonian gravity — force, escape velocity, orbital
  period, potential energy — tried live at `/physics-explorer/`. Built
  early, out of strict roadmap order, to prove the engine → API →
  frontend pipeline works end to end with a real engine. It's one
  calculation module, not "the physics engine done" — see
  [ROADMAP.md](ROADMAP.md).
- Provenance for engine output (`data-platform/data-provenance`): a
  signed-in user can save a gravity result as a finding, but the
  server always recomputes it first — a client's claimed result is
  never trusted or stored, only the inputs that produced it.
- A small API gateway (`backend/api-gateway`) serving both the JSON
  API and the static frontend.
- A sqlite-backed `storage/relational-database`.
- A frontend shell: sign-in/registration, a dashboard, a settings
  page, the research library's search/browse/add UI, and the physics
  explorer.

Everything else in `ARCHITECTURE.md` — the rest of the eight research
engines, the AI intelligence layer, the knowledge graph, simulation,
discovery reporting, and most of `data-platform` beyond basic
ingestion — exists
in this repo only as a scaffolded directory with a placeholder
`README.md` naming its purpose and the phase it's planned for. Nothing
there is implemented yet; don't take the directory tree as a claim
that it is.

## Quickstart

Requires Python 3.9+ and nothing else (no `pip install` needed —
everything here is standard library).

```sh
python3 run.py
# COSMOS Phase 2 gateway listening on http://127.0.0.1:8080/
# -> open http://127.0.0.1:8080/login/ to register or sign in
```

## Running the tests

```sh
python3 -m unittest discover -s tests -v
```

## Repository layout

The top-level directories mirror [ARCHITECTURE.md](ARCHITECTURE.md)
exactly — `frontend/`, `backend/`, `engines/`, `scientific-methods/`,
`intelligence/`, `simulation/`, `data-platform/`, `knowledge-graph/`,
`storage/`, `discovery/`, `infrastructure/`, `testing/` — plus:

- `run.py` — starts the Phase 1 API gateway.
- `tools/generate_scaffold.py` — (re-)generates placeholder READMEs for
  every module that doesn't have real content yet.
- `tools/cosmos_paths.py` — the `sys.path` wiring that lets Python
  import the hyphenated module directories (see
  [CONTRIBUTING.md](CONTRIBUTING.md) for why they're hyphenated).
- `tests/` — stdlib `unittest` tests for everything implemented so far.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — the epistemic ground rule
(tag every claim as established / open question / speculative) matters
more than the code style guide.

## License

MIT — see [LICENSE](LICENSE).
