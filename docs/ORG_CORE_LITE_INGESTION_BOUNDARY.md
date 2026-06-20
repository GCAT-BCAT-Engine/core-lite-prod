# Org Core-Lite Ingestion Boundary

## Purpose

This document defines the first GCAT-BCAT-Engine org-level core-lite ingestion boundary.

The repo is responsible for org-level continuation, validation, and routing evidence for dependent repositories. It is not the final destination for every payload and does not replace repository-local closure logic.

## Current Goal

```text
org: GCAT-BCAT-Engine
repo: core-lite-prod
goal: org-level ingestion and continuation alignment
state: self_managed_completion_ready
activation_state: self_managed_validation_ready
```

## Boundary Role

```text
role: org_core_lite_ingestion_engine
scope: GCAT-BCAT-Engine repositories
primary_function: receive, validate, classify, and route continuation events
secondary_function: preserve event records, hashes, receipts, and routing pointers
non_function: replace final repository activation or closure receipts
```

## Continuation Contract

The org-level engine must preserve the following classes of evidence:

```text
origin_repository
destination_repository
event_type
event_hash
bundle_hash
receipt_hash
state_before_hash
state_after_hash
routing_decision
retention_status
installed_confirmation
supersession_reference
master_record_pointer
```

## Event Record Schema

```text
schemas/org-core-lite-event-record.schema.json
examples/org-core-lite-event-record.example.json
tools/validate_org_core_lite_event_record.py
```

The event record schema validates repository identity, event type, hash fields, routing decision, retention status, and master-record pointer presence.

## Routing Matrix

```text
data/org-core-lite-routing-matrix.json
tools/check_org_core_lite_routing_matrix.py
```

The routing matrix binds event types to routing decisions, retention status, destination-confirmation requirements, and master-record pointer requirements.

## Continuation Receipt Writer

```text
tools/write_org_core_lite_receipt.py
receipts/org-core-lite-continuation-receipt.example.json
tools/check_org_core_lite_receipt.py
```

The receipt writer combines the event record and routing matrix into a non-activating continuation receipt. The receipt records event digest, routing matrix digest, route decision, retention status, and master-record pointer.

## Self-Managed Completion

```text
docs/ORG_CORE_LITE_SELF_MANAGED_COMPLETION.md
tools/check_org_core_lite_self_managed_completion.py
```

The self-managed completion record and checker make this repository resumable from repo-resident artifacts without prior chat context.

## Retention Boundary

```text
retain_full_bundle_only_for: active_pending_custody, quarantine, superseded_pending_retention, explicit_local_distribution
prefer_pointer_records_for: installed, confirmed, superseded, or externally retained bundles
master_record_pointer_required: true
```

Downstream failures remain in pending custody until install is confirmed, a newer bundle supersedes the event, or the destination is confirmed deprecated.

## Non-Claims

```text
This document is not an activation receipt.
This repo does not certify all GCAT-BCAT-Engine repositories as ingested.
This repo does not certify downstream installation by itself.
This repo does not replace Publisher/Site closure receipts.
The routing matrix is not a downstream installation receipt.
The continuation receipt is not a downstream installation receipt or repository activation receipt.
```

## Current Acceptance Criteria

```text
boundary document exists
self-management status exists
self-managed completion record exists
validation checker exists
activation runner exists
README points to this boundary
workflow validates boundary and status
event record schema exists
event record example exists
event record validator exists
activation runner validates event records
routing matrix exists
routing matrix checker exists
activation runner validates routing matrix
continuation receipt writer exists
continuation receipt example exists
continuation receipt checker exists
activation runner validates continuation receipt
self-managed completion checker exists
activation runner validates self-managed completion
```

## Archive Readiness

```text
thread_archive_ready: true
reason: Boundary, event-record validation, routing matrix, continuation receipt writer/checker, activation runner, workflow, README, status, and self-managed completion record are present and aligned.
```
