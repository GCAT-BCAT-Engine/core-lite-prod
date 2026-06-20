from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
writer = ROOT / "tools" / "write_downstream_confirmation.py"
receipt = ROOT / "receipts" / "downstream-install-confirmation.generated.example.json"
pointer = ROOT / "data" / "master-record-pointer-update.example.json"
sha_pattern = re.compile(r"^sha256:[a-f0-9]{64}$")
ok = True
for path in [writer, receipt, pointer]:
    if not path.exists():
        print(f"missing: {path.relative_to(ROOT)}")
        ok = False
if receipt.exists():
    data = json.loads(receipt.read_text(encoding="utf-8"))
    ok = ok and data.get("schema") == "stegverse.org_core_lite.downstream_install_confirmation.v1"
    ok = ok and data.get("install_state") == "pending_confirmation"
    ok = ok and data.get("installed") is False
    ok = ok and str(data.get("pointer_update_path", "")).startswith("master-records/dist/")
    ok = ok and sha_pattern.match(str(data.get("event_hash", ""))) is not None
    ok = ok and sha_pattern.match(str(data.get("receipt_hash", ""))) is not None
if pointer.exists():
    data = json.loads(pointer.read_text(encoding="utf-8"))
    ok = ok and data.get("schema") == "stegverse.org_core_lite.master_record_pointer_update.v1"
    ok = ok and data.get("custody_state") == "pending_destination_confirmation"
    ok = ok and str(data.get("master_record_pointer", "")).startswith("master-records/dist/")
    ok = ok and str(data.get("pointer_update_path", "")).startswith("master-records/dist/")
print("valid: downstream confirmation writer" if ok else "downstream confirmation writer check failed")
raise SystemExit(0 if ok else 1)
