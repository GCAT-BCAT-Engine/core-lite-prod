#!/usr/bin/env python3
"""Run the org core-lite validation sequence."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COMMANDS = [
    [sys.executable, "tools/check_org_core_lite_boundary.py"],
    [sys.executable, "tools/validate_org_core_lite_event_record.py"],
    [sys.executable, "tools/check_org_core_lite_routing_matrix.py"],
    [sys.executable, "tools/check_org_core_lite_receipt.py"],
    [sys.executable, "tools/check_org_core_lite_self_managed_completion.py"],
    [sys.executable, "tools/check_retention_bridge.py"],
    [sys.executable, "tools/check_downstream_confirmation_writer.py"],
]


def main() -> int:
    for command in COMMANDS:
        print(f"running: {' '.join(command)}")
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode != 0:
            print(f"org core-lite activation validation failed: {' '.join(command)}")
            return result.returncode
    print("valid: org core-lite activation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
