#!/usr/bin/env python3
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "org-core-lite-event-record.schema.json"
EXAMPLES = ROOT / "examples"
SHA_PATTERN = re.compile(r"^sha256:[a-f0-9]{64}$")
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REQUIRED = ["schema", "org", "event_id", "event_type", "origin_repository", "destination_repository", "event_hash", "bundle_hash", "receipt_hash", "state_before_hash", "state_after_hash", "routing_decision", "retention_status", "master_record_pointer"]
EVENT_TYPES = {"bundle_received", "bundle_validated", "bundle_routed", "install_confirmed", "quarantine", "superseded", "deprecated_destination"}
ROUTING_DECISIONS = {"route", "retain_pending", "quarantine", "reject", "supersede", "deprecate_destination"}
RETENTION_STATUSES = {"pointer_only", "active_pending_custody", "quarantine", "superseded_pending_retention", "explicit_local_distribution"}

def fail(message: str) -> int:
    print(f"org core-lite event record validation failed: {message}", file=sys.stderr)
    return 1

def validate_record(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in REQUIRED:
        if key not in data:
            return fail(f"{path}: missing {key}")
    if data["schema"] != "stegverse.org_core_lite.event_record.v1":
        return fail(f"{path}: invalid schema")
    if data["org"] != "GCAT-BCAT-Engine":
        return fail(f"{path}: invalid org")
    if data["event_type"] not in EVENT_TYPES:
        return fail(f"{path}: invalid event_type")
    if data["routing_decision"] not in ROUTING_DECISIONS:
        return fail(f"{path}: invalid routing_decision")
    if data["retention_status"] not in RETENTION_STATUSES:
        return fail(f"{path}: invalid retention_status")
    for key in ["origin_repository", "destination_repository"]:
        if not REPO_PATTERN.match(str(data[key])):
            return fail(f"{path}: invalid {key}")
    for key in ["event_hash", "bundle_hash", "receipt_hash", "state_before_hash", "state_after_hash"]:
        if not SHA_PATTERN.match(str(data[key])):
            return fail(f"{path}: invalid {key}")
    if not str(data["master_record_pointer"]).strip():
        return fail(f"{path}: missing master_record_pointer")
    print(f"valid: {path.relative_to(ROOT)}")
    return 0

def main() -> int:
    if not SCHEMA.exists():
        return fail("missing event record schema")
    paths = sorted(EXAMPLES.glob("org-core-lite-event-record*.json"))
    if not paths:
        return fail("no org core-lite event record examples found")
    for path in paths:
        result = validate_record(path)
        if result != 0:
            return result
    print("valid: org core-lite event records")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
