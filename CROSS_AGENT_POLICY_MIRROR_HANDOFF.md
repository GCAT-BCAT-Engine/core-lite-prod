# Cross-Agent Policy Mirror Handoff

## Active goal

```text
goal_id: BCAT-GCAT-XAGENT-POLICY-001
originating_session_goal: StegAgents constitutional identity, shared coordination, and cross-agent quorum authority
repository: GCAT-BCAT-Engine/core-lite-prod
branch: main
canonical_owner: GCAT-BCAT-Engine core-lite-prod policy bundle lane
claim_state: MACHINE_OWNED
claim_role: implementation, validation, and outbound policy publication
claim_created: 2026-08-02T08:26:00Z
claim_release_condition: immutable policy bundle is validated by StegAgents and StegEntity and produces matching decision results
```

## Existing repository goal and collision boundary

The current bilateral-closure acknowledgement goal remains independent and authoritative for its existing files. This cross-agent claim must not modify or supersede:

- `docs/BILATERAL_HANDOFF_CLOSURE_ACK.md`
- `receipts/bilateral-closure-ack.example.json`
- current master-records publication and closure tasks.

## Authoritative source contracts

- `StegVerse-Labs/StegAgents/docs/STEGAGENTS_CROSS_AGENT_AUTHORITY_HANDOFF.md`
- `StegVerse-Labs/StegAgents/schemas/stegagents.decision-record.schema.json`
- `StegVerse-Labs/StegAgents/schemas/stegagents.invariant-challenge.schema.json`
- `StegVerse-Labs/StegID/STEGID_MIRROR_HANDOFF.md`
- `StegVerse-Labs/StegEntity/docs/STEGENTITY_CROSS_AGENT_AUTHORITY_MIRROR_HANDOFF.md`

## Required production locations

```text
policies/cross-agent-authority.v1.json
schemas/cross-agent-authority-policy.schema.json
tools/check_cross_agent_authority_policy.py
tests/test_cross_agent_authority_policy.py
receipts/cross-agent-authority-policy-validation.json
outbound/cross-agent-authority-policy-manifest.json
.github/workflows/cross-agent-authority-policy.yml
```

## Required policy content

- action classes and impact levels;
- domain-specific eligible-role matrices;
- identity-independence requirements;
- quorum thresholds;
- denial and invariant-challenge effects;
- human and StegEntity gates;
- policy validity and expiry;
- incomplete-evidence quarantine behavior;
- canonical policy hash and version;
- explicit statement that policy does not mint identity or TVC execution authority.

## Completion state

```text
policy bundle: missing
schema: missing
validator: missing
tests: missing
validation receipt: missing
outbound manifest: missing
workflow: missing
consumer integration: missing
```

## Next executable action

Create the schema and policy bundle first, then implement a deterministic validator that returns `COMPLETE`, `BLOCKED`, `REVIEW_REQUIRED`, or `FAILED`. The validator must fail closed when identity, eligibility, independence, threshold, gate, expiry, or evidence requirements are unavailable.

## Blockers

No external blocker prevents repository-local schema, policy, validator, fixtures, tests, receipt, or workflow development.

Consumer activation is blocked until StegAgents and StegEntity import the same immutable policy hash.

Machine-observable release condition: both consumers reproduce the same eligibility, threshold, challenge, and gate result from the outbound manifest.

## Machine-owned tasks

The repository-native policy workflow owns validation after installation. It must persist a validation receipt, reject missing files, detect duplicate or stale policy versions, and identify the next incomplete deliverable.

## Integration and propagation obligations

- source policy owner: `GCAT-BCAT-Engine/core-lite-prod`;
- consumers: `StegVerse-Labs/StegAgents`, `StegVerse-Labs/StegEntity`, `StegVerse-Labs/TVC`;
- durable custody candidate after validation: `master-records`;
- publication is not authorized until consumer integration and governed activation are verified;
- no Site, Publisher, admissibility-wiki, or stegguardian-wiki propagation is currently claimed.

## Session consolidation

The action-class, eligible-role, standing, threshold, denial, invariant-challenge, human-gate, expiration, and quarantine requirements originating in the cross-agent authority session are merged into this handoff. No future policy implementation requires access to that conversation.

MERGED INTO: `GCAT-BCAT-Engine/core-lite-prod/CROSS_AGENT_POLICY_MIRROR_HANDOFF.md`

## Validation commands

```bash
python tools/check_cross_agent_authority_policy.py
python -m unittest discover tests
python tools/check_org_core_lite_activation.py
```

## Archive conditions

The originating session may archive when the TVC capability requirement, coordination-custody requirement, and consumer tasks are also durably assigned. This repository goal remains active independently of that session.

## Completion posture

- developed files: 1 of 7
- developed-files percentage: 14%
- validation percentage: 0%
- integration percentage: 0%
- goal-activation percentage: 5%
