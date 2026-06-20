# core-lite-prod

Org-level core services repo for `GCAT-BCAT-Engine`.

## Current Goal

```text
org: GCAT-BCAT-Engine
repo: core-lite-prod
goal: org-level ingestion and continuation alignment
state: event_record_validation_ready
activation_state: pending_routing_matrix_and_receipt_writer
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

The event record validator checks repository identifiers, event type, hash fields, routing decision, retention status, and master-record pointer presence.

## Validation

Run the org core-lite validation sequence:

```bash
python tools/check_org_core_lite_activation.py
```

That runner executes:

```bash
python tools/check_org_core_lite_boundary.py
python tools/validate_org_core_lite_event_record.py
```

Expected output:

```text
valid: org core-lite boundary
valid: examples/org-core-lite-event-record.example.json
valid: org core-lite event records
valid: org core-lite activation checks
```

## Workflow

The workflow path is displayed as:

```text
github/workflows/org-core-lite-validation.yml
```

In the repository, the actual path is `.github/workflows/org-core-lite-validation.yml`.

## Non-Activation Boundary

```text
This README is not an activation receipt.
The ingestion boundary document is not an activation receipt.
The self-management status is not an activation receipt.
The event record example is not a downstream installation receipt.
```

## Next Build Step

Move from event-record validation to routing matrix and receipt-writer alignment.
