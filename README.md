# core-lite-prod

Org-level core services repo for `GCAT-BCAT-Engine`.

## Current Goal

```text
org: GCAT-BCAT-Engine
repo: core-lite-prod
goal: org-level ingestion and continuation alignment
state: boundary_scaffold_ready
activation_state: pending_validator_and_workflow_alignment
```

## Boundary Documents

```text
docs/ORG_CORE_LITE_INGESTION_BOUNDARY.md
docs/ORG_CORE_LITE_SELF_MANAGEMENT_STATUS.md
```

## Validation

Run the org core-lite validation sequence:

```bash
python tools/check_org_core_lite_activation.py
```

That runner executes:

```bash
python tools/check_org_core_lite_boundary.py
```

Expected output:

```text
valid: org core-lite boundary
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
```

## Next Build Step

Move from boundary scaffold to routing-schema and event-record validation.
