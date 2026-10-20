-- COSMOS Phase 1 schema: accounts only. Research data (hypotheses,
-- observations, experiments, ...) lands here in later phases per
-- ARCHITECTURE.md / ROADMAP.md, not yet.

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
