from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
EVENT = ROOT / "examples" / "org-core-lite-event-record.example.json"
OUT = ROOT / "receipts" / "downstream-install-confirmation.generated.example.json"

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def digest(data: dict) -> str:
    raw = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()

def main() -> int:
    event = load(EVENT)
    payload = {
        "schema": "stegverse.org_core_lite.downstream_install_confirmation.v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "org": "GCAT-BCAT-Engine",
        "event_id": event["event_id"],
        "origin_repository": "GCAT-BCAT-Engine/core-lite-prod",
        "destination_repository": event["origin_repository"],
        "event_hash": event["event_hash"],
        "receipt_hash": event["receipt_hash"],
        "event_record_digest": digest(event),
        "installed": False,
        "install_state": "pending_confirmation",
        "destination_deprecated": False,
        "superseded_by": None,
        "master_record_pointer": event["master_record_pointer"],
        "pointer_update_path": "master-records/dist/gcat-event-0001/pointer.json",
        "scope": "generated_confirmation_example"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote: {OUT.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
