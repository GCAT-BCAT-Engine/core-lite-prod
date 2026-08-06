from __future__ import annotations
import copy,importlib.util,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TOOL=ROOT/"tools"/"check_curiosity_motive_admission_release.py"
R=ROOT/"receipts"/"curiosity-motive-admission-validation.json";M=ROOT/"outbound"/"curiosity-motive-admission-manifest.json"
S=importlib.util.spec_from_file_location("release",TOOL);assert S and S.loader
X=importlib.util.module_from_spec(S);sys.modules[S.name]=X;S.loader.exec_module(X)
class Tests(unittest.TestCase):
 def setUp(self):self.rb=R.read_bytes();self.mb=M.read_bytes();self.r=json.loads(self.rb);self.m=json.loads(self.mb)
 def runv(self,r=None,m=None,**kw):
  r=copy.deepcopy(self.r if r is None else r);m=copy.deepcopy(self.m if m is None else m)
  rb=self.rb if r==self.r else (json.dumps(r,indent=2,sort_keys=True)+"\n").encode()
  mb=self.mb if m==self.m else (json.dumps(m,indent=2,sort_keys=True)+"\n").encode()
  return X.validate(r,m,rb,mb,**kw)
 def test_valid(self):
  o=self.runv();self.assertEqual(o.status,"COMPLETE");self.assertEqual(o.custody_state,"CUSTODY_CANDIDATE_ONLY");self.assertEqual(o.errors,());self.assertFalse(o.execution_activated);self.assertFalse(o.input_mutated)
 def test_deterministic(self):self.assertEqual(self.runv().to_dict(),self.runv().to_dict())
 def test_nonmutating(self):
  r=copy.deepcopy(self.r);m=copy.deepcopy(self.m);br=copy.deepcopy(r);bm=copy.deepcopy(m);o=X.validate(r,m,self.rb,self.mb);self.assertEqual((r,m),(br,bm));self.assertFalse(o.input_mutated)
 def test_receipt_tamper(self):
  r=copy.deepcopy(self.r);r["validated_record"]["record_hash"]="0"*64;self.assertEqual(self.runv(r=r).status,"FAIL_CLOSED")
 def test_manifest_tamper(self):
  m=copy.deepcopy(self.m);m["source"]["commit"]="0"*40;self.assertEqual(self.runv(m=m).status,"FAIL_CLOSED")
 def test_receipt_digest_tamper(self):
  m=copy.deepcopy(self.m);m["source"]["validation_receipt_sha256"]="0"*64;self.assertEqual(self.runv(m=m).status,"FAIL_CLOSED")
 def test_execution_activation(self):
  r=copy.deepcopy(self.r);r["authority_boundary"]["execution_activated"]=True;self.assertEqual(self.runv(r=r).status,"FAIL_CLOSED")
 def test_policy_publication(self):
  m=copy.deepcopy(self.m);m["authority_boundary"]["policy_published"]=True;self.assertEqual(self.runv(m=m).status,"FAIL_CLOSED")
 def test_decision_tamper(self):
  m=copy.deepcopy(self.m);m["validated_record"]["normative_decision"]="ADMIT";self.assertEqual(self.runv(m=m).status,"FAIL_CLOSED")
 def test_require_ack_blocks(self):
  o=self.runv(require_ack=True);self.assertEqual(o.status,"BLOCKED");self.assertEqual(o.next_task,"MR-GCAT-CMG-CUSTODY-001")
 def test_valid_ack(self):
  base=self.runv();ack={"schema":"stegverse.master_records.curiosity_motive_custody_ack.v1","task_id":"MR-GCAT-CMG-CUSTODY-001","source_manifest_id":"GCAT-CMG-03-OUTBOUND-FF8E3B0-001","source_manifest_sha256":base.manifest_sha256,"source_receipt_sha256":base.receipt_sha256,"verification_status":"COMPLETE"}
  o=self.runv(require_ack=True,ack=ack);self.assertEqual(o.status,"COMPLETE");self.assertEqual(o.custody_state,"ACKNOWLEDGED")
 def test_invalid_ack(self):
  ack={"schema":"stegverse.master_records.curiosity_motive_custody_ack.v1","task_id":"MR-GCAT-CMG-CUSTODY-001","source_manifest_id":"GCAT-CMG-03-OUTBOUND-FF8E3B0-001","source_manifest_sha256":"0"*64,"source_receipt_sha256":"0"*64,"verification_status":"COMPLETE"}
  self.assertEqual(self.runv(require_ack=True,ack=ack).status,"FAIL_CLOSED")
 def test_cli(self):
  p=subprocess.run([sys.executable,str(TOOL)],cwd=ROOT,capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout)["status"],"COMPLETE")
 def test_cli_blocked(self):
  p=subprocess.run([sys.executable,str(TOOL),"--require-ack"],cwd=ROOT,capture_output=True,text=True);self.assertEqual(p.returncode,2);self.assertEqual(json.loads(p.stdout)["status"],"BLOCKED")
if __name__=="__main__":unittest.main()
