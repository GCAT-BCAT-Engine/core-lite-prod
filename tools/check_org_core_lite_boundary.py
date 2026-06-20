#!/usr/bin/env python3
"""Validate the GCAT-BCAT org core-lite ingestion boundary scaffold."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "docs/ORG_CORE_LITE_INGESTION_BOUNDARY.md": [
        "org: GCAT-BCAT-Engine",
        "repo: core-lite-prod",
        "goal: org-level ingestion and continuation alignment",
        "state: boundary_scaffold_ready",
        "role: org_core_lite_ingestion_engine",
        "origin_repository",
        "destination_repository",
        "event_hash",
        "bundle_hash",
        "receipt_hash",
        "routing_decision",
        "retention_status",
        "master_record_pointer_required: true",
        "This document is not an activation receipt.",
    ],
    "docs/ORG_CORE_LITE_SELF_MANAGEMENT_STATUS.md": [
        "repo_state: scaffold_ready",
        "activation_state: pending_validator_and_workflow_alignment",
        "tools/check_org_core_lite_boundary.py",
        "tools/check_org_core_lite_activation.py",
        "github/workflows/org-core-lite-validation.yml",
        "This status is not an activation receipt.",
    ],
}


def main() -> int:
    for rel_path, terms in CHECKS.items():
        path = ROOT / rel_path
        if not path.exists():
            print(f"org core-lite boundary check failed: missing {rel_path}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8")
        missing = [term for term in terms if term not in text]
        if missing:
            print(f"org core-lite boundary check failed: {rel_path}", file=sys.stderr)
            for term in missing:
                print(f"missing: {term}", file=sys.stderr)
            return 1

    print("valid: org core-lite boundary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
