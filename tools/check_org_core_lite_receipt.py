#!/usr/bin/env python3
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "receipts" / "org-core-lite-continuation-receipt.example.json"
WRITER = ROOT / "tools" / "write_org_core_lite_receipt.py"
SHA_PATTERN = re.compile(r"^sha256:[a-f0-9]{64}$")
REQUIRED = [
    "schema", "org", "event_id", "event_hash", "event_record_digest", "routing_matrix_digest",
    "origin_repository", "destination_repository", "routing_decision", "retention_status",
    "requires_destination_confirmation", "requires_master_record_pointer", "master_record_pointer",
    "activation_state", "non_claim"
]

def fail(message: str) -> int:
    print(f"org core-lite receipt check failed: {message}", file=sys.stderr)
    return 1

def main() -> int:
    if not WRITER.exists():
        return fail("missing receipt writer")
    if not RECEIPT.exists():
        return fail("missing receipt example")
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))
    for key in REQUIRED:
        if key not in data:
            return fail(f"missing {key}")
    if data["schema"] != "stegverse.org_core_lite.continuation_receipt.v1":
        return fail("invalid schema")
    if data["org"] != "GCAT-BCAT-Engine":
        return fail("invalid org")
    if data["activation_state"] != "non_activating_continuation_receipt":
        return fail("invalid activation_state")
    for key in ["event_hash", "event_record_digest", "routing_matrix_digest"]:
        if not SHA_PATTERN.match(str(data[key])):
            return fail(f"invalid {key}")
    if "not a downstream installation receipt" not in data["non_claim"]:
        return fail("missing downstream non-claim")
    if "not" not in data["non_claim"] or "activation receipt" not in data["non_claim"]:
        return fail("missing activation non-claim")
    print("valid: org core-lite continuation receipt")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
