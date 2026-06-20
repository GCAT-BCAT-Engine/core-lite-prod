# core-lite-prod

Org-level core services repo for `GCAT-BCAT-Engine`.

## Current Goal

```text
org: GCAT-BCAT-Engine
repo: core-lite-prod
goal: org-level ingestion and continuation alignment
state: self_managed_completion_ready
activation_state: self_managed_validation_ready
```

## Boundary Documents

```text
docs/ORG_CORE_LITE_INGESTION_BOUNDARY.md
docs/ORG_CORE_LITE_SELF_MANAGEMENT_STATUS.md
docs/ORG_CORE_LITE_SELF_MANAGED_COMPLETION.md
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

## Self-Managed Completion

```text
docs/ORG_CORE_LITE_SELF_MANAGED_COMPLETION.md
tools/check_org_core_lite_self_managed_completion.py
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
python tools/check_org_core_lite_self_managed_completion.py
```

Expected output:

```text
valid: org core-lite boundary
valid: examples/org-core-lite-event-record.example.json
valid: org core-lite event records
valid: org core-lite routing matrix
valid: org core-lite continuation receipt
valid: org core-lite self-managed completion
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
The self-managed completion document is a status record only.
```

## Next Integration Candidate

Connect org-level core-lite event records to master-records retention and downstream repository install confirmation.
