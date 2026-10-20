"""Phase 2: search-service. Pure-Python token scoring over
data-ingestion's sources, deliberately not SQLite FTS5 - that's a
compile-time SQLite feature and this repo would rather stay portable
across whatever Python/SQLite build CI (or a contributor) happens to
have than depend on it silently being present everywhere.
"""
import re

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text):
    return _TOKEN_RE.findall((text or "").lower())


def _score(source, query_tokens):
    title_tokens = _tokenize(source["title"])
    abstract_tokens = _tokenize(source["abstract"])
    score = 0
    for qt in query_tokens:
        if qt in title_tokens:
            score += 3
        elif any(qt in t for t in title_tokens):
            score += 2
        if qt in abstract_tokens:
            score += 1
    return score


def search_sources(sources, query="", evidence_status=None, limit=20):
    """sources: a list of dicts as returned by SourceStore.list_all()."""
    filtered = [s for s in sources if evidence_status is None or s["evidence_status"] == evidence_status]
    query = (query or "").strip()
    if not query:
        return filtered[:limit]
    query_tokens = _tokenize(query)
    scored = ((_score(s, query_tokens), s) for s in filtered)
    ranked = sorted((pair for pair in scored if pair[0] > 0), key=lambda pair: -pair[0])
    return [s for _, s in ranked][:limit]
