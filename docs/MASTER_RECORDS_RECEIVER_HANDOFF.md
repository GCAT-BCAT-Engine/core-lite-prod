# Master Records Receiver Handoff

## Purpose

This handoff defines the receiver-side contract expected by a future `master-records` repository for pointer updates emitted from `GCAT-BCAT-Engine/core-lite-prod`.

## Current State

```text
source_org: GCAT-BCAT-Engine
source_repo: core-lite-prod
receiver_org: master-records
receiver_scope: pointer_update_and_retention_confirmation
state: receiver_handoff_scaffold_ready
activation_state: pending_receiver_repository_installation
```

## Inputs

```text
data/master-record-pointer-update.example.json
receipts/downstream-install-confirmation.generated.example.json
receipts/org-core-lite-continuation-receipt.example.json
```

## Receiver Responsibilities

```text
validate_pointer_update_schema
validate_event_hash
validate_receipt_hash
validate_master_record_pointer_prefix
store_or_confirm_master_record_pointer
return_receiver_confirmation_receipt
preserve_non_activation_boundary
```

## Sender Responsibilities

```text
preserve_event_record
preserve_routing_matrix_digest
preserve_continuation_receipt
preserve_downstream_confirmation_receipt
retain_pending_until_destination_confirmation_or_supersession_or_deprecation
```

## Boundary Notes

```text
handoff_only: true
receiver_repository_created: not_claimed
receiver_installation_confirmed: false
master_record_pointer_update_applied: false
```

## Next Step

Create the receiver repository or receiver-side validation package that can accept `master-record-pointer-update.example.json` and return an explicit receiver confirmation receipt.
