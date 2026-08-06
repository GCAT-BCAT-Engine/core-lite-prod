#!/usr/bin/env python3
"""Compatibility entrypoint for the migrated custody acknowledgement envelope.

Preserves every v2 release/custody check while binding the verifier to the
new record-local import self-hash. No authority semantics are changed.
"""
from __future__ import annotations

import check_curiosity_motive_admission_release as verifier

MIGRATED_IMPORT_HASH = "ed597ecde9b7736a610f273774820d662c5bec066bdad5e3980f33bc7ed87996"

verifier.ACK_IMPORT_HASH = MIGRATED_IMPORT_HASH
verifier.ACK_CHECKS["import_hash"] = MIGRATED_IMPORT_HASH
verifier.ACK_CHECKS["record_type"] = "master_records_curiosity_motive_custody_ack_import"
verifier.ACK_CHECKS["source_repository"] = "master-records/core-lite"
verifier.ACK_CHECKS["destination_repository"] = "GCAT-BCAT-Engine/core-lite-prod"
verifier.ACK_CHECKS["hash_convention.algorithm"] = "SHA-256"
verifier.ACK_CHECKS["hash_convention.excluded_field"] = "import_hash"
verifier.ACK_CHECKS["hash_convention.serialization.encoding"] = "UTF-8"
verifier.ACK_CHECKS["hash_convention.serialization.format"] = "JSON"
verifier.ACK_CHECKS["hash_convention.serialization.separators"] = [",", ":"]
verifier.ACK_CHECKS["hash_convention.serialization.sort_keys"] = True

if __name__ == "__main__":
    raise SystemExit(verifier.main())
