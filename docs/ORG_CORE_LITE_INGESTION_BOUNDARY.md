# Org Core-Lite Ingestion Boundary

## Purpose

This document defines the first GCAT-BCAT-Engine org-level core-lite ingestion boundary.

The repo is responsible for org-level continuation, validation, and routing evidence for dependent repositories. It is not the final destination for every payload and does not replace repository-local closure logic.

## Current Goal

```text
org: GCAT-BCAT-Engine
repo: core-lite-prod
goal: org-level ingestion and continuation alignment
state: event_record_validation_ready
activation_state: pending_routing_matrix_and_receipt_writer
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
This repo is not yet a full production ingestion engine.
This repo does not certify downstream installation by itself.
This repo does not replace Publisher/Site closure receipts.
```

## Current Acceptance Criteria

```text
boundary document exists
self-management status exists
validation checker exists
activation runner exists
README points to this boundary
workflow validates boundary and status
event record schema exists
event record example exists
event record validator exists
activation runner validates event records
```

## Archive Readiness

```text
thread_archive_ready: false
reason: Event-record validation is present, but routing matrix and receipt writer still need to be created and aligned.
```
