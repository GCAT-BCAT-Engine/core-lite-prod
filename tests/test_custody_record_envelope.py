import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "receipts" / "master-records-curiosity-motive-custody-ack.json"


class CustodyRecordEnvelopeTests(unittest.TestCase):
    def test_import_record_envelope_and_hash(self):
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        self.assertEqual(record["record_type"], "master_records_curiosity_motive_custody_ack_import")
        self.assertEqual(record["source_repository"], "master-records/core-lite")
        self.assertEqual(record["destination_repository"], "GCAT-BCAT-Engine/core-lite-prod")
        convention = record["hash_convention"]
        self.assertEqual(convention["excluded_field"], "import_hash")
        body = dict(record)
        declared = body.pop("import_hash")
        computed = hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(declared, computed)

    def test_schema_and_record_type_are_not_contradictory(self):
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        self.assertTrue(record["schema"].endswith("custody_ack_import.v1"))
        self.assertIn("custody_ack_import", record["record_type"])


if __name__ == "__main__":
    unittest.main()
