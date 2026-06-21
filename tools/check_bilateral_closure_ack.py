from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
doc = ROOT / "docs" / "BILATERAL_HANDOFF_CLOSURE_ACK.md"
ack = ROOT / "receipts" / "bilateral-closure-ack.example.json"
source_ack = ROOT / "receipts" / "master-records-publication-ack.example.json"
sha_pattern = re.compile(r"^sha256:[a-f0-9]{64}$")
ok = True
for path in [doc, ack, source_ack]:
    if not path.exists():
        print(f"missing: {path.relative_to(ROOT)}")
        ok = False
if doc.exists():
    text = doc.read_text(encoding="utf-8")
    for term in ["state: bilateral_closure_acknowledgement_ready", "target_repo: master-records/telemetry", "status_record_only: true"]:
        if term not in text:
            print(f"missing doc term: {term}")
            ok = False
if ack.exists():
    data = json.loads(ack.read_text(encoding="utf-8"))
    ok = ok and data.get("schema") == "stegverse.org_core_lite.bilateral_closure_ack.v1"
    ok = ok and data.get("source_repository") == "GCAT-BCAT-Engine/core-lite-prod"
    ok = ok and data.get("target_repository") == "master-records/telemetry"
    ok = ok and data.get("acknowledgement_state") == "bilateral_closure_acknowledged"
    ok = ok and str(data.get("master_record_pointer", "")).startswith("master-records/dist/")
    ok = ok and sha_pattern.match(str(data.get("event_hash", ""))) is not None
    ok = ok and data.get("status_record_only") is True
    ok = ok and data.get("source_activation_claim") is False
    ok = ok and data.get("downstream_install_claim") is False
    ok = ok and data.get("full_retention_claim") is False
if source_ack.exists():
    data = json.loads(source_ack.read_text(encoding="utf-8"))
    ok = ok and data.get("target_repository") == "master-records/telemetry"
    ok = ok and data.get("source_repository") == "GCAT-BCAT-Engine/core-lite-prod"
print("valid: bilateral closure acknowledgement" if ok else "bilateral closure acknowledgement check failed")
raise SystemExit(0 if ok else 1)
