from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
checks = {
    "docs/ORG_CORE_LITE_INGESTION_BOUNDARY.md": [
        "state: self_managed_completion_ready",
        "activation_state: self_managed_validation_ready",
        "docs/ORG_CORE_LITE_SELF_MANAGED_COMPLETION.md",
        "tools/check_org_core_lite_self_managed_completion.py",
        "thread_archive_ready: true",
    ],
    "docs/ORG_CORE_LITE_SELF_MANAGEMENT_STATUS.md": [
        "repo_state: self_managed_completion_ready",
        "activation_state: self_managed_validation_ready",
        "self_managed_completion: ready",
    ],
}
ok = True
for rel, terms in checks.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    for term in terms:
        if term not in text:
            print(f"missing: {term} in {rel}")
            ok = False
print("valid: org core-lite boundary" if ok else "org core-lite boundary check failed")
raise SystemExit(0 if ok else 1)
