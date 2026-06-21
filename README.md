# core-lite-prod

Org-level core services repo for `GCAT-BCAT-Engine`.

## Current Goal

```text
org: GCAT-BCAT-Engine
repo: core-lite-prod
goal: mirrored bilateral closure acknowledgement
state: bilateral_closure_acknowledgement_ready
activation_state: receiver_publication_acknowledgement_ready
```

## Boundary Documents

```text
docs/ORG_CORE_LITE_INGESTION_BOUNDARY.md
docs/ORG_CORE_LITE_SELF_MANAGEMENT_STATUS.md
docs/ORG_CORE_LITE_SELF_MANAGED_COMPLETION.md
docs/DOWNSTREAM_CONFIRMATION_WRITE_PATH.md
docs/MASTER_RECORDS_RECEIVER_HANDOFF.md
docs/MASTER_RECORDS_PUBLICATION_HANDOFF.md
docs/BILATERAL_HANDOFF_CLOSURE_ACK.md
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

docs/MASTER_RECORDS_PUBLICATION_HANDOFF.md
receipts/master-records-publication-ack.example.json
tools/check_master_records_publication_handoff.py

docs/BILATERAL_HANDOFF_CLOSURE_ACK.md
receipts/bilateral-closure-ack.example.json
tools/check_bilateral_closure_ack.py
```

## Validation

Run:

```bash
python tools/check_org_core_lite_activation.py
python tools/check_downstream_confirmation_writer.py
python tools/check_master_records_publication_handoff.py
python tools/check_bilateral_closure_ack.py
```

Expected output includes:

```text
valid: org core-lite boundary
valid: retention bridge
valid: downstream confirmation writer
valid: master records publication handoff
valid: bilateral closure acknowledgement
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
The publication handoff acknowledgement is status evidence only.
The bilateral closure acknowledgement is mirrored status evidence only.
```

## Next Integration Candidate

Create an ecosystem-level handoff status index covering core-lite-prod and master-records/telemetry.
