from __future__ import annotations
import copy, importlib.util, json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/"tools"/"check_curiosity_motive_admission.py"
EXAMPLE=ROOT/"examples"/"curiosity-motive-admission.example.json"
SPEC=importlib.util.spec_from_file_location("cmg",TOOL);assert SPEC and SPEC.loader
M=importlib.util.module_from_spec(SPEC);sys.modules[SPEC.name]=M;SPEC.loader.exec_module(M)

class Tests(unittest.TestCase):
 def setUp(self):self.r=json.loads(EXAMPLE.read_text())
 def check_bad(self,path,value):
  record=copy.deepcopy(self.r);current=record
  parts=path.split(".")
  for part in parts[:-1]:current=current[part]
  current[parts[-1]]=value
  out=M.validate_record(record);self.assertEqual(out.status,"FAIL_CLOSED");self.assertTrue(any(parts[-1] in error for error in out.errors))
 def test_valid(self):
  out=M.validate_record(copy.deepcopy(self.r));self.assertEqual(out.status,"COMPLETE");self.assertEqual(out.errors,());self.assertEqual(out.normative_decision,"DENY");self.assertFalse(out.execution_activated);self.assertFalse(out.input_mutated);self.assertEqual(out.next_task,"GCAT-CMG-03")
 def test_deterministic(self):self.assertEqual(M.validate_record(copy.deepcopy(self.r)).to_dict(),M.validate_record(copy.deepcopy(self.r)).to_dict())
 def test_non_mutating(self):
  record=copy.deepcopy(self.r);before=copy.deepcopy(record);out=M.validate_record(record);self.assertEqual(record,before);self.assertFalse(out.input_mutated)
 def test_missing_finding(self):
  record=copy.deepcopy(self.r);del record["findings"]["observer"];self.assertEqual(M.validate_record(record).status,"FAIL_CLOSED")
 def test_receipt_tamper(self):self.check_bad("source_chain.bounded_runtime_intake.receipt_hash","0"*64)
 def test_competing_enum(self):self.check_bad("findings.normative.decision","ADMIT")
 def test_motive_authority(self):self.check_bad("findings.motivational.grants_authority",True)
 def test_observer_override(self):self.check_bad("findings.observer.defines_actor_motive",True)
 def test_occurrence_claim(self):self.check_bad("findings.event.occurrence_claim",True)
 def test_execution_activation(self):self.check_bad("findings.normative.execution_activated",True)
 def test_verifier_disagreement(self):self.check_bad("admission_boundary.verifier_agreement",False)
 def test_schema_vocabulary(self):
  schema=json.loads((ROOT/"schemas"/"curiosity-motive-admission.schema.json").read_text());self.assertEqual(schema["properties"]["findings"]["properties"]["normative"]["properties"]["decision"]["enum"],M.DECISIONS);self.assertEqual(schema["properties"]["canonical_decision_vocabulary"]["const"],M.DECISIONS)
 def test_cli(self):
  run=subprocess.run([sys.executable,str(TOOL),str(EXAMPLE)],cwd=ROOT,capture_output=True,text=True);self.assertEqual(run.returncode,0,run.stderr);out=json.loads(run.stdout);self.assertEqual(out["status"],"COMPLETE");self.assertFalse(out["execution_activated"]);self.assertFalse(out["input_mutated"])
if __name__=="__main__":unittest.main()
