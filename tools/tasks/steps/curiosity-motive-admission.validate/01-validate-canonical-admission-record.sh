mkdir -p reports/current
python tools/check_curiosity_motive_admission.py | tee reports/current/curiosity-motive-admission-validation.json
