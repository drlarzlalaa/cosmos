-- COSMOS schema. Phase 1 added users; Phase 2 adds sources (the
-- research-library's data-ingestion records). Later phases add more
-- tables here as their own modules land - see ROADMAP.md.

CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT NOT NULL UNIQUE,
    display_name  TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL
);

-- A research-library entry. evidence_status is the platform's core
-- epistemic promise (see CONTRIBUTING.md): every source is tagged as
-- one of 'established' / 'open_question' / 'speculative', enforced in
-- data-ingestion/ingestion.py, not just asserted in prose.
CREATE TABLE IF NOT EXISTS sources (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT NOT NULL,
    url             TEXT,
    authors         TEXT,
    abstract        TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    submitted_by    INTEGER NOT NULL REFERENCES users(id),
    created_at      TEXT NOT NULL
);
