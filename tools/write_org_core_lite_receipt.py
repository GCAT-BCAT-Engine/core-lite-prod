#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENT = ROOT / "examples" / "org-core-lite-event-record.example.json"
MATRIX = ROOT / "data" / "org-core-lite-routing-matrix.json"
OUT_DIR = ROOT / "receipts"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(data: dict) -> str:
    raw = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def route_for(event: dict, matrix: dict) -> dict:
    for route in matrix.get("routes", []):
        if route.get("event_type") == event.get("event_type"):
            return route
    raise SystemExit(f"no route for event_type: {event.get('event_type')}")


def main() -> int:
    event = load(EVENT)
    matrix = load(MATRIX)
    route = route_for(event, matrix)
    payload = {
        "schema": "stegverse.org_core_lite.continuation_receipt.v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "org": "GCAT-BCAT-Engine",
        "event_id": event["event_id"],
        "event_hash": event["event_hash"],
        "event_record_digest": digest(event),
        "routing_matrix_digest": digest(matrix),
        "origin_repository": event["origin_repository"],
        "destination_repository": event["destination_repository"],
        "routing_decision": route["routing_decision"],
        "retention_status": route["retention_status"],
        "requires_destination_confirmation": route["requires_destination_confirmation"],
        "requires_master_record_pointer": route["requires_master_record_pointer"],
        "master_record_pointer": event["master_record_pointer"],
        "activation_state": "non_activating_continuation_receipt",
        "non_claim": "This receipt is not a downstream installation receipt or repository activation receipt."
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "org-core-lite-continuation-receipt.example.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote: {out.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
