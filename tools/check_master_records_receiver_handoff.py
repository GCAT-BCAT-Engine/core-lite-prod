from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
handoff = ROOT / "docs" / "MASTER_RECORDS_RECEIVER_HANDOFF.md"
schema = ROOT / "schemas" / "master-record-pointer-update.schema.json"
pointer = ROOT / "data" / "master-record-pointer-update.example.json"
sha_pattern = re.compile(r"^sha256:[a-f0-9]{64}$")
ok = True
for path in [handoff, schema, pointer]:
    if not path.exists():
        print(f"missing: {path.relative_to(ROOT)}")
        ok = False
if handoff.exists():
    text = handoff.read_text(encoding="utf-8")
    for term in ["receiver_org: master-records", "state: receiver_handoff_scaffold_ready", "receiver_installation_confirmed: false"]:
        if term not in text:
            print(f"missing handoff term: {term}")
            ok = False
if schema.exists():
    data = json.loads(schema.read_text(encoding="utf-8"))
    ok = ok and data.get("title") == "Master Record Pointer Update"
if pointer.exists():
    data = json.loads(pointer.read_text(encoding="utf-8"))
    ok = ok and data.get("schema") == "stegverse.org_core_lite.master_record_pointer_update.v1"
    ok = ok and str(data.get("master_record_pointer", "")).startswith("master-records/dist/")
    ok = ok and str(data.get("pointer_update_path", "")).startswith("master-records/dist/")
    ok = ok and sha_pattern.match(str(data.get("event_hash", ""))) is not None
    ok = ok and sha_pattern.match(str(data.get("receipt_hash", ""))) is not None
print("valid: master records receiver handoff" if ok else "master records receiver handoff check failed")
raise SystemExit(0 if ok else 1)
