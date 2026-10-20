import unittest

import conftest_paths  # noqa: F401
import gravity

EARTH_MASS_KG = 5.972e24
EARTH_RADIUS_M = 6.371e6
SUN_MASS_KG = 1.989e30
AU_M = 1.496e11


class GravityTests(unittest.TestCase):
    def test_force_matches_known_value(self):
        # Two 1000 kg masses 1 m apart: F = G*1000*1000/1 = G*1e6
        f = gravity.gravitational_force(1000, 1000, 1)
        self.assertAlmostEqual(f, gravity.G * 1e6, places=6)

    def test_earth_escape_velocity_matches_known_value(self):
        # Textbook value: ~11.2 km/s
        v = gravity.escape_velocity(EARTH_MASS_KG, EARTH_RADIUS_M)
        self.assertAlmostEqual(v / 1000, 11.2, delta=0.05)

    def test_earth_orbital_period_matches_one_year(self):
        # Earth around the Sun: ~365.25 days
        seconds = gravity.orbital_period(AU_M, SUN_MASS_KG)
        days = seconds / 86400
        self.assertAlmostEqual(days, 365.25, delta=2)

    def test_potential_energy_is_negative_and_symmetric(self):
        u = gravity.gravitational_potential_energy(1000, 1000, 1)
        self.assertLess(u, 0)
        self.assertAlmostEqual(u, -gravity.G * 1e6, places=6)

    def test_rejects_non_positive_inputs(self):
        for bad in (0, -5, "not-a-number"):
            with self.assertRaises(gravity.GravityError):
                gravity.gravitational_force(bad, 1000, 1)

    def test_compute_dispatches_by_name(self):
        out = gravity.compute("force", {"mass1_kg": 1000, "mass2_kg": 1000, "distance_m": 1})
        self.assertEqual(out["evidence_status"], "established")
        self.assertAlmostEqual(out["result"], gravity.G * 1e6, places=6)
        self.assertEqual(out["unit"], "newtons")

    def test_compute_rejects_unknown_calculation(self):
        with self.assertRaises(gravity.GravityError):
            gravity.compute("teleportation", {})

    def test_compute_rejects_missing_input(self):
        with self.assertRaises(gravity.GravityError):
            gravity.compute("force", {"mass1_kg": 1000})


if __name__ == "__main__":
    unittest.main()
