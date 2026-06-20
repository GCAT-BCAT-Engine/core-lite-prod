# core-lite-prod

Org-level core services repo for `GCAT-BCAT-Engine`.

## Current Goal

```text
org: GCAT-BCAT-Engine
repo: core-lite-prod
goal: org-level ingestion and continuation alignment
state: routing_matrix_validation_ready
activation_state: pending_receipt_writer_alignment
```

## Boundary Documents

```text
docs/ORG_CORE_LITE_INGESTION_BOUNDARY.md
docs/ORG_CORE_LITE_SELF_MANAGEMENT_STATUS.md
```

## Event Record Validation

```text
schemas/org-core-lite-event-record.schema.json
examples/org-core-lite-event-record.example.json
tools/validate_org_core_lite_event_record.py
```

## Routing Matrix Validation

```text
data/org-core-lite-routing-matrix.json
tools/check_org_core_lite_routing_matrix.py
```

## Validation

Run:

```bash
python tools/check_org_core_lite_activation.py
```

That runner executes:

```bash
python tools/check_org_core_lite_boundary.py
python tools/validate_org_core_lite_event_record.py
python tools/check_org_core_lite_routing_matrix.py
```

Expected output:

```text
valid: org core-lite boundary
valid: examples/org-core-lite-event-record.example.json
valid: org core-lite event records
valid: org core-lite routing matrix
valid: org core-lite activation checks
```

## Workflow

Displayed workflow path:

```text
github/workflows/org-core-lite-validation.yml
```

Actual repository path: `.github/workflows/org-core-lite-validation.yml`.

## Non-Activation Boundary

```text
This README is not an activation receipt.
The ingestion boundary document is not an activation receipt.
The self-management status is not an activation receipt.
The event record example is not a downstream installation receipt.
The routing matrix is not a downstream installation receipt.
```

## Next Build Step

Move from routing matrix validation to receipt-writer alignment.
