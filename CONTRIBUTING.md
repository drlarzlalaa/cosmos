# Contributing to COSMOS

COSMOS is an open-source attempt to build a research platform that
investigates the laws of nature without blurring the line between
what's actually known and what's merely hoped for. That line is the
thing to protect in every contribution.

## The one rule that matters most

Every claim, hypothesis, or finding introduced into the platform (in
code, docs, or data) must be tagged as one of:

- **Established** — supported by strong, reproducible evidence. Cite it.
- **Open question** — a real, researchable problem with no settled answer yet.
- **Speculative** — an idea with no evidential support yet.

Never present a speculative idea as established, and never let a
module's output imply more confidence than its evidence supports. This
applies everywhere, but especially in `engines/`, `knowledge-graph/`,
and `discovery/`, once those phases land.

## Scope discipline

Build in the order laid out in [ROADMAP.md](ROADMAP.md). A PR that
jumps ahead of the current phase (e.g. wiring up `engines/physics-engine`
before Phase 3 starts) is a good conversation to have in an issue
first, not a surprise in a PR.

## Code conventions

- Stdlib-first. The build/CI environment this project started on has
  no `pip`, so `backend/` and `storage/` have zero third-party
  dependencies by design — keep it that way unless a later phase
  (e.g. a real vector database, a numerical library for the physics
  engine) genuinely needs one. If you add a dependency, say why in
  the PR description.
- Module directory names match [ARCHITECTURE.md](ARCHITECTURE.md)
  exactly, including the hyphens. Python can't import a hyphenated
  directory as a package, so cross-module code adds the directory to
  `sys.path` via `tools/cosmos_paths.py` and imports the (hyphen-free)
  `.py` file by its bare module name — see `run.py` for the pattern.
- No comments that restate what the code does; comments explain a
  non-obvious why.

## Running it locally

```sh
python3 run.py
# -> http://127.0.0.1:8080/login/
```

## Running the tests

```sh
python3 -m unittest discover -s tests -v
```

Every new module should ship with `unittest`-based tests in `tests/`,
following the existing files as the pattern (no pytest - it isn't
installed in CI either).

## Re-running the scaffold

`tools/generate_scaffold.py` only ever writes a placeholder `README.md`
into a module directory that doesn't already have one — it never
overwrites real code or a README you've written by hand. Run it after
adding a new module to ARCHITECTURE.md's tree.
