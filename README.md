# core-lite-prod

Org-level core services repo for `GCAT-BCAT-Engine`.

## Current Goal

```text
org: GCAT-BCAT-Engine
repo: core-lite-prod
goal: receiver handoff scaffold
state: receiver_handoff_scaffold_ready
activation_state: pending_receiver_repository_installation
```

## Boundary Documents

```text
docs/ORG_CORE_LITE_INGESTION_BOUNDARY.md
docs/ORG_CORE_LITE_SELF_MANAGEMENT_STATUS.md
docs/ORG_CORE_LITE_SELF_MANAGED_COMPLETION.md
docs/DOWNSTREAM_CONFIRMATION_WRITE_PATH.md
docs/MASTER_RECORDS_RECEIVER_HANDOFF.md
```

## Validation Groups

```text
schemas/org-core-lite-event-record.schema.json
examples/org-core-lite-event-record.example.json
tools/validate_org_core_lite_event_record.py

data/org-core-lite-routing-matrix.json
tools/check_org_core_lite_routing_matrix.py

tools/write_org_core_lite_receipt.py
receipts/org-core-lite-continuation-receipt.example.json
tools/check_org_core_lite_receipt.py

data/master-records-retention-map.json
examples/downstream-install-confirmation.example.json
tools/check_retention_bridge.py

tools/write_downstream_confirmation.py
receipts/downstream-install-confirmation.generated.example.json
data/master-record-pointer-update.example.json
tools/check_downstream_confirmation_writer.py

docs/MASTER_RECORDS_RECEIVER_HANDOFF.md
schemas/master-record-pointer-update.schema.json
tools/check_master_records_receiver_handoff.py
github/workflows/master-records-receiver-handoff.yml
```

Actual workflow path: `.github/workflows/master-records-receiver-handoff.yml`.

## Validation

Run:

```bash
python tools/check_org_core_lite_activation.py
python tools/check_downstream_confirmation_writer.py
python tools/check_master_records_receiver_handoff.py
```

Expected output includes:

```text
valid: org core-lite boundary
valid: retention bridge
valid: downstream confirmation writer
valid: master records receiver handoff
```

## Boundary

```text
README is documentation only.
The event record example is example evidence only.
The routing matrix is routing configuration only.
The continuation receipt is continuation evidence only.
The retention map is pointer and custody policy only.
The downstream confirmation example is example evidence only.
The generated downstream confirmation receipt is example evidence only.
The pointer update example is pointer-update evidence only.
The receiver handoff is receiver contract evidence only.
```

## Next Integration Candidate

Create the actual receiver repository/package or continue hardening workflow integration in this repo.
