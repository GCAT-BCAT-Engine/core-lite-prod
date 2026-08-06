from __future__ import annotations
import copy, importlib.util, json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/'tools/check_curiosity_motive_admission_release.py';R=ROOT/'receipts/curiosity-motive-admission-validation.json'
M=ROOT/'outbound/curiosity-motive-admission-manifest.json';A=ROOT/'receipts/master-records-curiosity-motive-custody-ack.json'
S=importlib.util.spec_from_file_location('release',TOOL);assert S and S.loader
X=importlib.util.module_from_spec(S);sys.modules[S.name]=X;S.loader.exec_module(X)

class Tests(unittest.TestCase):
 def setUp(self):
  self.rb=R.read_bytes();self.mb=M.read_bytes();self.ab=A.read_bytes()
  self.r=json.loads(self.rb);self.m=json.loads(self.mb);self.a=json.loads(self.ab)
 def runv(self,r=None,m=None,a='default',require=False):
  r=copy.deepcopy(self.r if r is None else r);m=copy.deepcopy(self.m if m is None else m)
  a=copy.deepcopy(self.a if a=='default' and require else (None if a=='default' else a))
  rb=self.rb if r==self.r else (json.dumps(r,indent=2,sort_keys=True)+'\n').encode()
  mb=self.mb if m==self.m else (json.dumps(m,indent=2,sort_keys=True)+'\n').encode()
  ab=self.ab if a==self.a else ((json.dumps(a,indent=2,sort_keys=True)+'\n').encode() if a is not None else b'')
  return X.validate(r,m,rb,mb,require_ack=require,ack_import=a,ack_import_bytes=ab)
 def test_release_candidate(self):
  o=self.runv();self.assertEqual((o.status,o.custody_state,o.next_task),('COMPLETE','CUSTODY_CANDIDATE_ONLY','MR-GCAT-CMG-CUSTODY-001'));self.assertFalse(o.execution_activated)
 def test_exact_ack(self):
  o=self.runv(require=True);self.assertEqual((o.status,o.custody_state,o.next_task),('COMPLETE','ACKNOWLEDGED','SESSION-CONSOLIDATION-001'))
  self.assertEqual((o.ack_import_hash,o.acknowledgement_hash,o.custody_record_hash),(X.ACK_IMPORT_HASH,X.ACKNOWLEDGEMENT_HASH,X.CUSTODY_RECORD_HASH))
 def test_deterministic(self):self.assertEqual(self.runv(require=True).to_dict(),self.runv(require=True).to_dict())
 def test_nonmutating(self):
  r,m,a=copy.deepcopy((self.r,self.m,self.a));before=copy.deepcopy((r,m,a));o=X.validate(r,m,self.rb,self.mb,require_ack=True,ack_import=a,ack_import_bytes=self.ab)
  self.assertEqual((r,m,a),before);self.assertFalse(o.input_mutated)
 def test_missing_ack_blocked(self):
  o=self.runv(a=None,require=True);self.assertEqual((o.status,o.custody_state,o.next_task),('BLOCKED','AWAITING_DESTINATION_ACKNOWLEDGEMENT','MR-GCAT-CMG-CUSTODY-001'))
 def assert_ack_tamper(self,path,value):
  a=copy.deepcopy(self.a);v=a
  keys=path.split('.')
  for k in keys[:-1]:v=v[k]
  v[keys[-1]]=value;self.assertEqual(self.runv(a=a,require=True).status,'FAIL_CLOSED')
 def test_bare_ack_insufficient(self):self.assertEqual(self.runv(a=self.a['acknowledgement'],require=True).status,'FAIL_CLOSED')
 def test_source_merge(self):self.assert_ack_tamper('source.ack_merge_commit','0'*40)
 def test_source_blob(self):self.assert_ack_tamper('source.ack_git_blob_sha','0'*40)
 def test_source_workflow(self):self.assert_ack_tamper('source.exact_main_repository_validation.workflow_run',1)
 def test_artifact_digest(self):self.assert_ack_tamper('source.exact_main_dedicated_validation.artifact_digest','sha256:'+'0'*64)
 def test_receipt_hash(self):self.assert_ack_tamper('acknowledgement.source_receipt_sha256','0'*64)
 def test_decision(self):self.assert_ack_tamper('acknowledgement.validated_record.normative_decision','ALLOW')
 def test_motive(self):self.assert_ack_tamper('acknowledgement.validated_record.functional_motive_finding','instrumental_exploration')
 def test_observer_contract(self):self.assert_ack_tamper('acknowledgement.findings_contract.observer_description_does_not_define_motive',False)
 def test_authority_expansion(self):self.assert_ack_tamper('acknowledgement.authority_boundary.execution_authority_granted',True)
 def test_runtime_activation(self):self.assert_ack_tamper('import_effect.runtime_activation',True)
 def test_occurrence_claim(self):self.assert_ack_tamper('import_effect.occurrence_proven',True)
 def test_phenomenal_claim(self):self.assert_ack_tamper('import_effect.phenomenal_status_inferred',True)
 def test_import_hash(self):self.assert_ack_tamper('import_hash','0'*64)
 def test_nested_ack_hash(self):self.assert_ack_tamper('acknowledgement.acknowledgement_hash','0'*64)
 def test_release_tamper(self):
  r=copy.deepcopy(self.r);r['validated_record']['record_hash']='0'*64;self.assertEqual(self.runv(r=r).status,'FAIL_CLOSED')
 def test_manifest_tamper(self):
  m=copy.deepcopy(self.m);m['source']['commit']='0'*40;self.assertEqual(self.runv(m=m).status,'FAIL_CLOSED')
 def cli(self,*args):return subprocess.run([sys.executable,str(TOOL),*args],cwd=ROOT,capture_output=True,text=True)
 def test_cli_candidate(self):
  p=self.cli();self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout)['custody_state'],'CUSTODY_CANDIDATE_ONLY')
 def test_cli_ack(self):
  p=self.cli('--require-ack');d=json.loads(p.stdout);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual((d['status'],d['custody_state'],d['next_task']),('COMPLETE','ACKNOWLEDGED','SESSION-CONSOLIDATION-001'))
 def test_cli_missing(self):
  p=self.cli('--require-ack','--ack-import',str(ROOT/'receipts/does-not-exist.json'));self.assertEqual(p.returncode,2);self.assertEqual(json.loads(p.stdout)['status'],'BLOCKED')
 def test_cli_malformed(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'bad.json';f.write_text('{bad',encoding='utf-8');p=self.cli('--require-ack','--ack-import',str(f))
  self.assertEqual(p.returncode,1);self.assertEqual(json.loads(p.stdout)['status'],'FAIL_CLOSED')
if __name__=='__main__':unittest.main()
