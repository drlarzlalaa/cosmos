import os
import tempfile
import unittest

import conftest_paths  # noqa: F401
import db
import ingestion
import users


class SourceStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.conn = db.get_connection(os.path.join(self.tmp_dir, "test.db"))
        self.user = users.UserStore(self.conn).create_user(
            "researcher@example.com", "password123", "Researcher")
        self.store = ingestion.SourceStore(self.conn)

    def test_create_and_fetch(self):
        source = self.store.create_source(
            title="General relativity predicts light bending",
            abstract="Starlight bends near the sun, measured during a solar eclipse.",
            evidence_status="established", submitted_by=self.user["id"],
            url="https://example.org/paper", authors="Eddington",
        )
        fetched = self.store.get_by_id(source["id"])
        self.assertEqual(fetched["title"], source["title"])
        self.assertEqual(fetched["evidence_status"], "established")

    def test_rejects_unknown_evidence_status(self):
        with self.assertRaises(ingestion.IngestionError):
            self.store.create_source(
                title="X", abstract="Y", evidence_status="definitely-true",
                submitted_by=self.user["id"],
            )

    def test_requires_title_and_abstract(self):
        with self.assertRaises(ingestion.IngestionError):
            self.store.create_source(
                title="   ", abstract="Y", evidence_status="speculative",
                submitted_by=self.user["id"],
            )
        with self.assertRaises(ingestion.IngestionError):
            self.store.create_source(
                title="X", abstract="   ", evidence_status="speculative",
                submitted_by=self.user["id"],
            )

    def test_rejects_unknown_user(self):
        with self.assertRaises(ingestion.IngestionError):
            self.store.create_source(
                title="X", abstract="Y", evidence_status="speculative",
                submitted_by=999999,
            )

    def test_list_all_orders_newest_first(self):
        first = self.store.create_source(
            title="First", abstract="A", evidence_status="open_question",
            submitted_by=self.user["id"])
        second = self.store.create_source(
            title="Second", abstract="B", evidence_status="open_question",
            submitted_by=self.user["id"])
        listed = self.store.list_all()
        self.assertEqual([s["id"] for s in listed][:2], [second["id"], first["id"]])


if __name__ == "__main__":
    unittest.main()
