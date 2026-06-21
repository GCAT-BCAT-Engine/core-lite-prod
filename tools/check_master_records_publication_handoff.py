from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
doc = ROOT / "docs" / "MASTER_RECORDS_PUBLICATION_HANDOFF.md"
ack = ROOT / "receipts" / "master-records-publication-ack.example.json"
sha_pattern = re.compile(r"^sha256:[a-f0-9]{64}$")
ok = True
if not doc.exists():
    print("missing: docs/MASTER_RECORDS_PUBLICATION_HANDOFF.md")
    ok = False
else:
    text = doc.read_text(encoding="utf-8")
    for term in ["state: publication_handoff_acknowledgement_ready", "target_repo: master-records/telemetry", "status_record_only: true"]:
        if term not in text:
            print(f"missing doc term: {term}")
            ok = False
if not ack.exists():
    print("missing: receipts/master-records-publication-ack.example.json")
    ok = False
else:
    data = json.loads(ack.read_text(encoding="utf-8"))
    ok = ok and data.get("schema") == "stegverse.org_core_lite.master_records_publication_ack.v1"
    ok = ok and data.get("source_repository") == "GCAT-BCAT-Engine/core-lite-prod"
    ok = ok and data.get("target_repository") == "master-records/telemetry"
    ok = ok and data.get("acknowledgement_state") == "published_example_acknowledged"
    ok = ok and str(data.get("master_record_pointer", "")).startswith("master-records/dist/")
    ok = ok and sha_pattern.match(str(data.get("event_hash", ""))) is not None
    paths = data.get("published_paths", [])
    for required in ["examples/inbound-master-record-pointer-update.example.json", "examples/inbound-downstream-install-confirmation.example.json", "receipts/cross-repo-confirmation-receipt.example.json", "data/receipt-pairing-index.json"]:
        ok = ok and required in paths
    ok = ok and data.get("status_record_only") is True
    ok = ok and data.get("source_activation_claim") is False
    ok = ok and data.get("downstream_install_claim") is False
    ok = ok and data.get("full_retention_claim") is False
print("valid: master records publication handoff" if ok else "master records publication handoff check failed")
raise SystemExit(0 if ok else 1)
