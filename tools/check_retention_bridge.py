from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
retention_map = ROOT / "data" / "master-records-retention-map.json"
confirmation_file = ROOT / "examples" / "downstream-install-confirmation.example.json"
sha_pattern = re.compile(r"^sha256:[a-f0-9]{64}$")
retention_statuses = {"pointer_only", "active_pending_custody", "quarantine", "superseded_pending_retention", "explicit_local_distribution"}
install_states = {"pending_confirmation", "installed", "superseded", "destination_deprecated", "quarantined"}

ok = True
if retention_map.exists():
    data = json.loads(retention_map.read_text(encoding="utf-8"))
    ok = ok and data.get("schema") == "stegverse.org_core_lite.master_records_retention_map.v1"
    ok = ok and data.get("master_records_org") == "master-records"
    seen = {rule.get("retention_status") for rule in data.get("retention_rules", [])}
    ok = ok and retention_statuses.issubset(seen)
    for rule in data.get("retention_rules", []):
        ok = ok and rule.get("requires_master_record_pointer") is True
        ok = ok and rule.get("requires_receipt_hash") is True
else:
    ok = False

if confirmation_file.exists():
    confirmation = json.loads(confirmation_file.read_text(encoding="utf-8"))
    ok = ok and confirmation.get("schema") == "stegverse.org_core_lite.downstream_install_confirmation.v1"
    ok = ok and confirmation.get("install_state") in install_states
    ok = ok and sha_pattern.match(str(confirmation.get("event_hash", ""))) is not None
    ok = ok and sha_pattern.match(str(confirmation.get("receipt_hash", ""))) is not None
    ok = ok and str(confirmation.get("master_record_pointer", "")).startswith("master-records/dist/")
else:
    ok = False

print("valid: retention bridge" if ok else "retention bridge check failed")
raise SystemExit(0 if ok else 1)
