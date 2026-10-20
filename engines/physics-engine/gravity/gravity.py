"""engines/physics-engine/gravity: closed-form Newtonian gravity.
Everything here is textbook, established physics (Newton's law of
gravitation and Kepler's third law under the two-body, test-particle
approximation) - no hypothesis testing, no discovery, nothing
speculative. That's deliberate: this is the first real research engine
in the platform, so it's the right place to prove the engine ->
API -> frontend pipeline works before anything here claims to compute
something uncertain. Hypothesis testing lives in Phase 4
(scientific-methods); discovery lives in Phase 7.
"""
import math

G = 6.6743e-11  # CODATA 2018 Newtonian constant of gravitation, m^3 kg^-1 s^-2


class GravityError(Exception):
    pass


def _positive(name, value):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
        raise GravityError("%s must be a positive number" % name)
    return float(value)


def gravitational_force(mass1_kg, mass2_kg, distance_m):
    """Newton's law of universal gravitation: F = G*m1*m2 / r^2."""
    m1 = _positive("mass1_kg", mass1_kg)
    m2 = _positive("mass2_kg", mass2_kg)
    r = _positive("distance_m", distance_m)
    return G * m1 * m2 / r ** 2


def escape_velocity(mass_kg, radius_m):
    """v = sqrt(2*G*M / r) - speed needed to escape a body's gravity
    from its surface, ignoring atmospheric drag."""
    m = _positive("mass_kg", mass_kg)
    r = _positive("radius_m", radius_m)
    return math.sqrt(2 * G * m / r)


def orbital_period(semi_major_axis_m, central_mass_kg):
    """Kepler's third law (two-body, orbiting mass negligible next to
    the central mass): T = 2*pi*sqrt(a^3 / (G*M))."""
    a = _positive("semi_major_axis_m", semi_major_axis_m)
    m = _positive("central_mass_kg", central_mass_kg)
    return 2 * math.pi * math.sqrt(a ** 3 / (G * m))


def gravitational_potential_energy(mass1_kg, mass2_kg, distance_m):
    """U = -G*m1*m2 / r (negative: bound system, zero at infinite separation)."""
    m1 = _positive("mass1_kg", mass1_kg)
    m2 = _positive("mass2_kg", mass2_kg)
    r = _positive("distance_m", distance_m)
    return -G * m1 * m2 / r


CALCULATIONS = {
    "force": {
        "fn": gravitational_force,
        "params": ["mass1_kg", "mass2_kg", "distance_m"],
        "unit": "newtons",
        "formula": "F = G * m1 * m2 / r^2",
    },
    "escape_velocity": {
        "fn": escape_velocity,
        "params": ["mass_kg", "radius_m"],
        "unit": "meters/second",
        "formula": "v = sqrt(2 * G * M / r)",
    },
    "orbital_period": {
        "fn": orbital_period,
        "params": ["semi_major_axis_m", "central_mass_kg"],
        "unit": "seconds",
        "formula": "T = 2 * pi * sqrt(a^3 / (G * M))",
    },
    "potential_energy": {
        "fn": gravitational_potential_energy,
        "params": ["mass1_kg", "mass2_kg", "distance_m"],
        "unit": "joules",
        "formula": "U = -G * m1 * m2 / r",
    },
}


def compute(calculation, inputs):
    """inputs: a dict with (at least) the keys CALCULATIONS[calculation]['params'].
    Returns {"result", "unit", "formula", "evidence_status"}. Raises
    GravityError on an unknown calculation or missing/invalid input."""
    spec = CALCULATIONS.get(calculation)
    if spec is None:
        raise GravityError("unknown calculation: %s (expected one of %s)" %
                            (calculation, ", ".join(CALCULATIONS)))
    try:
        args = [inputs[p] for p in spec["params"]]
    except KeyError as exc:
        raise GravityError("missing required input: %s" % exc.args[0])
    result = spec["fn"](*args)
    return {
        "result": result,
        "unit": spec["unit"],
        "formula": spec["formula"],
        "evidence_status": "established",
    }
