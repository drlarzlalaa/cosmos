"""data-platform/data-provenance: saves a result an engine actually
computed, not a claim a user typed in. The caller (backend/api-gateway)
is responsible for recomputing the result server-side via the named
engine before calling record_finding() - this module never trusts a
result value handed to it, it only stores one.
"""
import json
import sqlite3
import time


class ProvenanceError(Exception):
    pass


class ProvenanceStore:
    def __init__(self, conn):
        self.conn = conn

    def record_finding(self, engine, calculation, inputs, result, unit, formula,
                        evidence_status, submitted_by):
        try:
            cur = self.conn.execute(
                "INSERT INTO computed_findings (engine, calculation, inputs_json, result, "
                "unit, formula, evidence_status, submitted_by, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (engine, calculation, json.dumps(inputs, sort_keys=True), result, unit,
                 formula, evidence_status, submitted_by, _now_iso()),
            )
        except sqlite3.IntegrityError:
            raise ProvenanceError("unknown submitting user")
        self.conn.commit()
        return self.get_by_id(cur.lastrowid)

    def get_by_id(self, finding_id):
        row = self.conn.execute(
            "SELECT * FROM computed_findings WHERE id = ?", (finding_id,)).fetchone()
        return _row_to_dict(row) if row else None

    def list_all(self, engine=None):
        if engine:
            rows = self.conn.execute(
                "SELECT * FROM computed_findings WHERE engine = ? "
                "ORDER BY created_at DESC, id DESC", (engine,)).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM computed_findings ORDER BY created_at DESC, id DESC").fetchall()
        return [_row_to_dict(row) for row in rows]


def _row_to_dict(row):
    return {
        "id": row["id"], "engine": row["engine"], "calculation": row["calculation"],
        "inputs": json.loads(row["inputs_json"]), "result": row["result"],
        "unit": row["unit"], "formula": row["formula"],
        "evidence_status": row["evidence_status"], "submitted_by": row["submitted_by"],
        "created_at": row["created_at"],
    }


def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
