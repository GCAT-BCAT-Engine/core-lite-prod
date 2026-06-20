#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "org-core-lite-routing-matrix.json"
EVENT_TYPES = {"bundle_received", "bundle_validated", "bundle_routed", "install_confirmed", "quarantine", "superseded", "deprecated_destination"}
ROUTING_DECISIONS = {"route", "retain_pending", "quarantine", "reject", "supersede", "deprecate_destination"}
RETENTION_STATUSES = {"pointer_only", "active_pending_custody", "quarantine", "superseded_pending_retention", "explicit_local_distribution"}

def fail(message: str) -> int:
    print(f"org core-lite routing matrix check failed: {message}", file=sys.stderr)
    return 1

def main() -> int:
    if not MATRIX.exists():
        return fail("missing routing matrix")
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    if data.get("schema") != "stegverse.org_core_lite.routing_matrix.v1":
        return fail("invalid schema")
    if data.get("org") != "GCAT-BCAT-Engine":
        return fail("invalid org")
    routes = data.get("routes")
    if not isinstance(routes, list) or not routes:
        return fail("routes must be a non-empty list")
    seen = set()
    for index, route in enumerate(routes):
        event_type = route.get("event_type")
        routing_decision = route.get("routing_decision")
        retention_status = route.get("retention_status")
        if event_type not in EVENT_TYPES:
            return fail(f"route {index}: invalid event_type")
        if routing_decision not in ROUTING_DECISIONS:
            return fail(f"route {index}: invalid routing_decision")
        if retention_status not in RETENTION_STATUSES:
            return fail(f"route {index}: invalid retention_status")
        if route.get("requires_master_record_pointer") is not True:
            return fail(f"route {index}: missing master-record pointer requirement")
        seen.add(event_type)
    missing = sorted(EVENT_TYPES - seen)
    if missing:
        return fail("missing routes: " + ", ".join(missing))
    print("valid: org core-lite routing matrix")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
