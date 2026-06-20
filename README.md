# core-lite-prod

Org-level core services repo for `GCAT-BCAT-Engine`.

## Current Goal

```text
org: GCAT-BCAT-Engine
repo: core-lite-prod
goal: org-level ingestion and continuation alignment
state: receipt_writer_validation_ready
activation_state: pending_self_managed_completion
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

## Continuation Receipt Validation

```text
tools/write_org_core_lite_receipt.py
receipts/org-core-lite-continuation-receipt.example.json
tools/check_org_core_lite_receipt.py
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
python tools/check_org_core_lite_receipt.py
```

Expected output:

```text
valid: org core-lite boundary
valid: examples/org-core-lite-event-record.example.json
valid: org core-lite event records
valid: org core-lite routing matrix
valid: org core-lite continuation receipt
valid: org core-lite activation checks
```

## Workflow

Displayed workflow path:

```text
github/workflows/org-core-lite-validation.yml
```

Actual repository path: `.github/workflows/org-core-lite-validation.yml`.

## Boundary

```text
README is documentation only.
The event record example is example evidence only.
The routing matrix is routing configuration only.
The continuation receipt is continuation evidence only.
```

## Next Build Step

Move from receipt-writer validation to self-managed completion alignment.
