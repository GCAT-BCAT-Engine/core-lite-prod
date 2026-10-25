set +e
python tools/check_curiosity_motive_admission_release_v3.py --require-ack --ack-import reports/current/nonexistent-acknowledgement.json > reports/current/curiosity-motive-admission-missing-ack-status.json
code=$?
set -e
test "$code" -eq 2
python - <<'PY'
import json
from pathlib import Path
result=json.loads(Path('reports/current/curiosity-motive-admission-missing-ack-status.json').read_text())
assert result['status']=='BLOCKED'
assert result['custody_state']=='AWAITING_DESTINATION_ACKNOWLEDGEMENT'
PY
