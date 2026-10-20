"""Phase 2: data-ingestion. Takes in research-library entries
("sources") and enforces the one rule CONTRIBUTING.md asks every
contributor to follow by hand - every source is tagged established,
open_question, or speculative, not left to imply more confidence than
it has. Backed by storage/relational-database.
"""
import sqlite3
import time

EVIDENCE_STATUSES = ("established", "open_question", "speculative")


class IngestionError(Exception):
    pass


class SourceStore:
    def __init__(self, conn):
        self.conn = conn

    def create_source(self, title, abstract, evidence_status, submitted_by,
                       url=None, authors=None):
        title = title.strip()
        abstract = abstract.strip()
        if not title:
            raise IngestionError("title is required")
        if not abstract:
            raise IngestionError("abstract is required")
        if evidence_status not in EVIDENCE_STATUSES:
            raise IngestionError(
                "evidence_status must be one of %s" % ", ".join(EVIDENCE_STATUSES))
        try:
            cur = self.conn.execute(
                "INSERT INTO sources (title, url, authors, abstract, evidence_status, "
                "submitted_by, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (title, (url or "").strip() or None, (authors or "").strip() or None,
                 abstract, evidence_status, submitted_by, _now_iso()),
            )
        except sqlite3.IntegrityError:
            raise IngestionError("unknown submitting user")
        self.conn.commit()
        return self.get_by_id(cur.lastrowid)

    def get_by_id(self, source_id):
        row = self.conn.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()
        return _row_to_dict(row) if row else None

    def list_all(self):
        # id DESC as a tiebreaker: created_at has only second resolution,
        # so two inserts within the same second would otherwise sort
        # arbitrarily instead of newest-first.
        rows = self.conn.execute("SELECT * FROM sources ORDER BY created_at DESC, id DESC").fetchall()
        return [_row_to_dict(row) for row in rows]


def _row_to_dict(row):
    return {
        "id": row["id"], "title": row["title"], "url": row["url"],
        "authors": row["authors"], "abstract": row["abstract"],
        "evidence_status": row["evidence_status"], "submitted_by": row["submitted_by"],
        "created_at": row["created_at"],
    }


def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
