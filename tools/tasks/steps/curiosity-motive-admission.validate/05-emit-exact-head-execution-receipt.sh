python - <<'PY' | tee reports/current/custody-record-envelope-execution.json
import json, os
print(json.dumps({"repository":"GCAT-BCAT-Engine/core-lite-prod","workflow":"Curiosity Motive Admission","head_sha":os.environ['GITHUB_SHA'],"execution_state":"EXECUTED","authority_effect":"NONE"}, sort_keys=True))
PY
