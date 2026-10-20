# gravity

Part of [`engines/physics-engine`](../README.md) in the COSMOS platform.

**Status:** implemented early, out of strict roadmap order (this
module is nominally Phase 3; see ROADMAP.md's "early Phase 3 slice"
for why).

Closed-form Newtonian gravity - Newton's law of universal gravitation
and Kepler's third law (two-body, test-particle approximation).
Everything here is textbook, established physics: no hypothesis
testing, no discovery. `compute()` dispatches by calculation name
(`force`, `escape_velocity`, `orbital_period`, `potential_energy`) and
every result is tagged `evidence_status: "established"`.

Exposed via `backend/api-gateway`'s `GET`/`POST /api/engines/gravity`
and tried live at `/physics-explorer/`. Tests: `tests/test_gravity.py`
(checked against known values - Earth's escape velocity, Earth's
orbital period).
