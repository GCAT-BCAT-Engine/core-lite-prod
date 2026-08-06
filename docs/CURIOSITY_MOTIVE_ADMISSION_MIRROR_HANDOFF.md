# Curiosity and Motive Admission Mirror Handoff

## Scope and authority

```text
goal_id: GCAT-BCAT-CURIOSITY-MOTIVE-ADMISSION-001
repository: GCAT-BCAT-Engine/core-lite-prod
stage: GCAT-CMG-01
claim_state: SCOPED_INTEGRATION
claim_role: immutable evidence binding and admission-vocabulary mapping
execution_activated: false
may_execute_actions: false
may_bind_repository_state: false
may_form_quorum: false
may_publish_policy: false
```

This is a scoped handoff. It does not supersede
`CROSS_AGENT_POLICY_MIRROR_HANDOFF.md`, the bilateral-closure lane, or any
existing Master Records publication obligation. The cross-agent policy handoff
remains authoritative for its own policy-bundle goal.

## Canonical upstream chain

### Formulation and verifier

```text
repository: StegVerse-Labs/StegCore
commit: 42231a3862c2fe9b5898e6f75d72cff0b44e7396
module: src/stegcore/motive_governance.py
module_git_blob_sha: 0a333344492880044680de6a9325ba16112bbacd
test: tests/test_motive_governance.py
test_git_blob_sha: e098a59f079801febb0af3a4ced4305945fec477
```

### Durable custody

```text
repository: master-records/core-lite
anchor_introduction_commit: facd5508d540f1afddf3a8dc6502084460407b0d
record_id: MR-STEGCORE-CURIOSITY-MOTIVE-GOV-42231A3-001
record_path: records/stegcore_curiosity_motive_governance_42231a3.json
record_hash: 76a865b3efe8eb7496bdd36a78e5b8d3024ddcda4a009462784ed81308db97af
```

### Bounded runtime-intake evidence

```text
repository: StegVerse-002/core-lite
merge_commit: 48500639bb29bd7c86437df9086a773df1e46543
candidate_hash: b34743d186307080a4cc371d3780544f3038c39ebbb7d146bd974461e8cf8ef1
receipt_hash: 6dd6039d558b07e1d3a35ab6ce65ea015353e9df46b7c8dc84edfdd7ad80908d
replay_root: bbd79be33e090e188484628e341f28b0bebcda260a509bbdc47681c9ee204d89
conversion_sequence: 4
conversion_event_hash: ce62b4a15c90017b39bd6405966b611bc27074c6a7d409b4bf15a74ebcb3aa4b
```

The bounded runtime-intake finding reconstructs the supplied witness. It does
not establish an unrecorded occurrence and does not authorize re-execution.

## Required claim separation

Every future consumer in this repository must preserve four independent
findings:

1. event reconstruction;
2. motivational attribution;
3. normative authority decision;
4. observer record.

Required invariants:

```text
motive_does_not_grant_authority: true
normative_denial_does_not_negate_motive: true
observer_description_does_not_define_motive: true
reconstruction_does_not_constitute_occurrence: true
phenomenal_status_not_inferred: true
verifier_disagreement_fails_closed: true
```

## Canonical decision vocabulary

This lane must consume, preserve, and emit only the existing normative decision
values:

```text
ALLOW
DENY
FAIL_CLOSED
NO_EXECUTION
```

No GCAT/BCAT-specific competing decision enum is authorized. Evidence admission
posture is metadata about whether a record may proceed to validation; it is not
an authority decision.

Mapping rules:

- `ALLOW` means valid reconstructed execution with valid commit-time authority.
- `DENY` means reconstructed execution without valid authority.
- `FAIL_CLOSED` means the witness, authority, provenance, or verifier agreement
  is insufficient to establish a valid transition.
- `NO_EXECUTION` means no execution commitment was reconstructed.

A high-confidence functional-curiosity finding may coexist with `DENY` or
`FAIL_CLOSED`. Curiosity, motive, emotion, or affect is never an authority
credential.

## Installed Stage 1 surface

```text
docs/CURIOSITY_MOTIVE_ADMISSION_MIRROR_HANDOFF.md
data/curiosity-motive-admission-map.json
```

Stage 1 binds the upstream chain and defines the admission mapping. It does not
claim schema conformance, executable validation, test coverage, workflow
execution, receipt generation, or activation.

## Next bounded stage

Create `GCAT-CMG-02` as a separate pull request containing:

```text
schemas/curiosity-motive-admission.schema.json
tools/check_curiosity_motive_admission.py
examples/curiosity-motive-admission.example.json
tests/test_curiosity_motive_admission.py
```

The validator must verify the pinned source, anchor, runtime receipt, four
finding types, and canonical decision value. Missing or contradictory evidence
must result in `FAIL_CLOSED`; the tool must not activate execution or mutate the
input record.
