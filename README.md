# core-lite-prod

Org-level core services repo for `GCAT-BCAT-Engine`.

## Current Goal

```text
org: GCAT-BCAT-Engine
repo: core-lite-prod
goal: downstream confirmation receipt write-path and master-record pointer update flow
state: downstream_confirmation_write_path_ready
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

## Retention Bridge Validation

```text
data/master-records-retention-map.json
examples/downstream-install-confirmation.example.json
tools/check_retention_bridge.py
```

## Downstream Confirmation Write Path

```text
tools/write_downstream_confirmation.py
receipts/downstream-install-confirmation.generated.example.json
data/master-record-pointer-update.example.json
tools/check_downstream_confirmation_writer.py
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

The primary runner now executes through downstream confirmation writer validation. The downstream confirmation writer checker validates the generated confirmation receipt and pointer update flow.

Expected output includes:

```text
valid: org core-lite boundary
valid: org core-lite event records
valid: org core-lite routing matrix
valid: org core-lite continuation receipt
valid: org core-lite self-managed completion
valid: retention bridge
valid: downstream confirmation writer
valid: org core-lite activation checks
```

## Workflow

Displayed workflow path:

```text
github/workflows/org-core-lite-validation.yml
```

Actual repository path: `.github/workflows/org-core-lite-validation.yml`.

Current workflow state:

```text
The workflow runs the primary activation runner.
The primary activation runner now includes downstream confirmation writer validation.
Workflow trigger expansion for downstream writer artifacts remains the next hardening item if connector safety allows direct workflow mutation.
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
The master-record pointer update example is pointer-update evidence only.
```

## Next Integration Candidate

Harden workflow trigger coverage for downstream confirmation writer artifacts, then continue with master-records-side receiver scaffolding.
