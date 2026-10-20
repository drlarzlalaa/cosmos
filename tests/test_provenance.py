import os
import tempfile
import unittest

import conftest_paths  # noqa: F401
import db
import provenance
import users


class ProvenanceStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.conn = db.get_connection(os.path.join(self.tmp_dir, "test.db"))
        self.user = users.UserStore(self.conn).create_user(
            "researcher@example.com", "password123", "Researcher")
        self.store = provenance.ProvenanceStore(self.conn)

    def test_record_and_fetch_round_trips_inputs(self):
        finding = self.store.record_finding(
            engine="physics-engine/gravity", calculation="escape_velocity",
            inputs={"mass_kg": 5.972e24, "radius_m": 6.371e6},
            result=11185.97789184991, unit="meters/second",
            formula="v = sqrt(2 * G * M / r)", evidence_status="established",
            submitted_by=self.user["id"],
        )
        fetched = self.store.get_by_id(finding["id"])
        self.assertEqual(fetched["inputs"], {"mass_kg": 5.972e24, "radius_m": 6.371e6})
        self.assertEqual(fetched["result"], 11185.97789184991)
        self.assertEqual(fetched["evidence_status"], "established")

    def test_rejects_unknown_user(self):
        with self.assertRaises(provenance.ProvenanceError):
            self.store.record_finding(
                engine="physics-engine/gravity", calculation="force", inputs={},
                result=1.0, unit="newtons", formula="F = ...",
                evidence_status="established", submitted_by=999999,
            )

    def test_list_all_filters_by_engine(self):
        self.store.record_finding(
            engine="physics-engine/gravity", calculation="force", inputs={},
            result=1.0, unit="newtons", formula="F = ...",
            evidence_status="established", submitted_by=self.user["id"],
        )
        self.store.record_finding(
            engine="other-engine/x", calculation="y", inputs={},
            result=2.0, unit="", formula="", evidence_status="established",
            submitted_by=self.user["id"],
        )
        gravity_only = self.store.list_all(engine="physics-engine/gravity")
        self.assertEqual(len(gravity_only), 1)
        self.assertEqual(gravity_only[0]["engine"], "physics-engine/gravity")

        all_findings = self.store.list_all()
        self.assertEqual(len(all_findings), 2)


if __name__ == "__main__":
    unittest.main()
