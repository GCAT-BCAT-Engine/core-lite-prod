#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECKS = {
    "docs/ORG_CORE_LITE_SELF_MANAGED_COMPLETION.md": [
        "repo_build_state: self_managed_completion_ready",
        "activation_state: self_managed_validation_ready",
        "event_record_validation: ready",
        "routing_matrix_validation: ready",
        "continuation_receipt_validation: ready",
        "retention_bridge_validation: ready",
        "downstream_confirmation_writer_validation: ready",
        "master_record_pointer_update_example: ready",
        "workflow_trigger_expansion: pending_hardening",
        "self_managed_completion: ready",
        "thread_archive_ready: true",
    ],
    "docs/ORG_CORE_LITE_INGESTION_BOUNDARY.md": [
        "state: self_managed_completion_ready",
        "Self-Managed Completion",
        "activation runner validates self-managed completion",
        "thread_archive_ready: true",
    ],
    "docs/ORG_CORE_LITE_SELF_MANAGEMENT_STATUS.md": [
        "repo_state: self_managed_completion_ready",
        "activation_state: self_managed_validation_ready",
        "receipt_writer_alignment: ready",
        "self_managed_completion: ready",
    ],
    "tools/check_org_core_lite_activation.py": [
        "tools/check_org_core_lite_boundary.py",
        "tools/validate_org_core_lite_event_record.py",
        "tools/check_org_core_lite_routing_matrix.py",
        "tools/check_org_core_lite_receipt.py",
        "tools/check_org_core_lite_self_managed_completion.py",
        "tools/check_retention_bridge.py",
        "tools/check_downstream_confirmation_writer.py",
    ],
    "tools/check_downstream_confirmation_writer.py": [
        "downstream-install-confirmation.generated.example.json",
        "master-record-pointer-update.example.json",
        "valid: downstream confirmation writer",
    ],
    "README.md": [
        "state: downstream_confirmation_write_path_ready",
        "tools/check_org_core_lite_self_managed_completion.py",
        "tools/check_downstream_confirmation_writer.py",
        "valid: downstream confirmation writer",
        "Workflow trigger expansion for downstream writer artifacts remains the next hardening item",
    ],
}


def main() -> int:
    for rel_path, terms in CHECKS.items():
        path = ROOT / rel_path
        if not path.exists():
            print(f"org core-lite self-managed completion check failed: missing {rel_path}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8")
        missing = [term for term in terms if term not in text]
        if missing:
            print(f"org core-lite self-managed completion check failed: {rel_path}", file=sys.stderr)
            for term in missing:
                print(f"missing: {term}", file=sys.stderr)
            return 1
    print("valid: org core-lite self-managed completion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
