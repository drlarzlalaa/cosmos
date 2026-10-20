import unittest

import conftest_paths  # noqa: F401
import search


def _source(id, title, abstract, evidence_status="established"):
    return {"id": id, "title": title, "abstract": abstract, "evidence_status": evidence_status}


SOURCES = [
    _source(1, "Gravitational lensing confirms general relativity", "Light bends around massive bodies."),
    _source(2, "Quantum tunneling in superconductors", "Particles cross barriers classically forbidden.", "open_question"),
    _source(3, "A speculative theory of consciousness", "Not yet supported by evidence.", "speculative"),
]


class SearchTests(unittest.TestCase):
    def test_empty_query_returns_all_within_limit(self):
        results = search.search_sources(SOURCES, query="")
        self.assertEqual(len(results), 3)

    def test_title_match_ranks_above_abstract_only_match(self):
        results = search.search_sources(SOURCES, query="quantum")
        self.assertEqual(results[0]["id"], 2)

    def test_no_match_returns_empty(self):
        results = search.search_sources(SOURCES, query="zzzznomatch")
        self.assertEqual(results, [])

    def test_evidence_status_filter(self):
        results = search.search_sources(SOURCES, query="", evidence_status="speculative")
        self.assertEqual([s["id"] for s in results], [3])

    def test_limit(self):
        results = search.search_sources(SOURCES, query="", limit=1)
        self.assertEqual(len(results), 1)

    def test_multi_word_query_matches_relevant_source(self):
        results = search.search_sources(SOURCES, query="general relativity")
        self.assertEqual(results[0]["id"], 1)


if __name__ == "__main__":
    unittest.main()
