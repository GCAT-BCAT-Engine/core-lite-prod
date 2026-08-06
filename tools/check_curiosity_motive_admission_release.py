#!/usr/bin/env python3
"""Fail-closed verifier for GCAT-CMG-03 release and GCAT-CMG-04 custody ack."""
from __future__ import annotations
import argparse, copy, hashlib, json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/'receipts/curiosity-motive-admission-validation.json'
MANIFEST=ROOT/'outbound/curiosity-motive-admission-manifest.json'
ACK_IMPORT=ROOT/'receipts/master-records-curiosity-motive-custody-ack.json'
RECEIPT_SHA='24d4984457708c4fea6b7a182bee82004b93be6d2cb21626300b48a13d8a72c2'
MANIFEST_SHA='6344432f06de75f771af0cb1148a6a0197ffdcadb21068b0eb246b0afcc469cc'
RECORD_SHA='6bfbd1af3aecd03c3b4579d0465f0962dd49f3741e786046a4189735223e3eac'
ACK_IMPORT_HASH='1d65230536d7cc7db60cc544c84d42d9d25fc3c9382b66d703476ac34b88813e'
ACKNOWLEDGEMENT_HASH='0a98789be976aad5c18936fe823f9732d683f4e149051e34976eb4743678eb24'
CUSTODY_RECORD_HASH='f7db74f1a2caafab593f2beacc203901ac5a72d5d0fd44b7e0f9b209170a528f'

@dataclass(frozen=True)
class Result:
 status:str; receipt_sha256:str; manifest_sha256:str; custody_state:str; errors:tuple[str,...]
 execution_activated:bool=False; input_mutated:bool=False; next_task:str='REVIEW_REQUIRED'
 ack_import_hash:str=''; acknowledgement_hash:str=''; custody_record_hash:str=''; ack_import_file_sha256:str=''
 def to_dict(self)->dict[str,Any]:
  return {'schema':'stegverse.gcat_bcat.curiosity_motive_admission_release_validation.v2','status':self.status,
   'receipt_sha256':self.receipt_sha256,'manifest_sha256':self.manifest_sha256,'record_hash':RECORD_SHA,
   'normative_decision':'DENY','custody_state':self.custody_state,'ack_import_hash':self.ack_import_hash,
   'acknowledgement_hash':self.acknowledgement_hash,'custody_record_hash':self.custody_record_hash,
   'ack_import_file_sha256':self.ack_import_file_sha256,'errors':list(self.errors),
   'execution_activated':self.execution_activated,'input_mutated':self.input_mutated,'next_task':self.next_task}

def canon(v:Any)->str:return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha_bytes(v:bytes)->str:return hashlib.sha256(v).hexdigest()
def sha_canon(v:Any)->str:return sha_bytes(canon(v).encode())
def get(r:Mapping[str,Any],p:str)->Any:
 v:Any=r
 for k in p.split('.'):
  if not isinstance(v,Mapping) or k not in v:raise KeyError(p)
  v=v[k]
 return v
def expect(r:Mapping[str,Any],p:str,w:Any,e:list[str])->None:
 try:a=get(r,p)
 except KeyError:e.append('missing:'+p);return
 if a!=w:e.append(f'mismatch:{p}:expected={canon(w)}:actual={canon(a)}')
def hash_without(r:Mapping[str,Any],field:str)->str:
 x=copy.deepcopy(r);x.pop(field,None);return sha_canon(x)

BASE_CHECKS={
 'receipt.schema':'stegverse.gcat_bcat.curiosity_motive_admission_validation_receipt.v1',
 'receipt.receipt_id':'GCAT-CMG-03-VALIDATION-FF8E3B0-001','receipt.validated_record.record_hash':RECORD_SHA,
 'receipt.validated_record.status':'COMPLETE','receipt.validated_record.normative_decision':'DENY',
 'receipt.validated_record.execution_activated':False,'receipt.validated_record.input_mutated':False,
 'receipt.exact_main_validation.commit':'ff8e3b04628456c1bcc0571833a1a6f3071909ea',
 'receipt.exact_main_validation.workflow_run':31062909742,'receipt.exact_main_validation.job':92494415341,
 'receipt.exact_main_validation.conclusion':'success','receipt.release_state.custody_state':'CUSTODY_CANDIDATE_ONLY',
 'manifest.schema':'stegverse.gcat_bcat.curiosity_motive_admission_outbound_manifest.v1',
 'manifest.manifest_id':'GCAT-CMG-03-OUTBOUND-FF8E3B0-001','manifest.source.commit':'ff8e3b04628456c1bcc0571833a1a6f3071909ea',
 'manifest.source.validation_receipt_sha256':RECEIPT_SHA,'manifest.validated_record.record_hash':RECORD_SHA,
 'manifest.validated_record.normative_decision':'DENY','manifest.validated_record.validation_status':'COMPLETE',
 'manifest.custody_request.destination_repository':'master-records/core-lite','manifest.custody_request.task_id':'MR-GCAT-CMG-CUSTODY-001',
 'manifest.status':'READY_FOR_INDEPENDENT_CUSTODY_VERIFICATION','manifest.next_task':'MR-GCAT-CMG-CUSTODY-001'}
ACK_CHECKS={
 'schema':'stegverse.gcat_bcat.master_records_curiosity_motive_custody_ack_import.v1','import_id':'GCAT-CMG-04-MR-ACK-A0774A7-001',
 'goal_id':'GCAT-BCAT-CURIOSITY-MOTIVE-ADMISSION-001','stage':'GCAT-CMG-04','hash_algorithm':'sha256-canonical-json-v1','import_hash':ACK_IMPORT_HASH,
 'source.repository':'master-records/core-lite','source.ack_merge_commit':'a0774a7ec6228d4655b4f96bb49f64312d078249',
 'source.ack_path':'records/gcat_bcat_curiosity_motive_admission_ack_001.json','source.ack_git_blob_sha':'f313045f39b9208f3c8db4067be14f7e3ccf9e66',
 'source.acknowledgement_hash':ACKNOWLEDGEMENT_HASH,'source.exact_main_repository_validation.workflow_run':31066067903,
 'source.exact_main_repository_validation.job':92503934615,'source.exact_main_repository_validation.conclusion':'success',
 'source.exact_main_repository_validation.tests_run':34,'source.exact_main_repository_validation.tests_result':'OK',
 'source.exact_main_dedicated_validation.workflow_run':31066067909,'source.exact_main_dedicated_validation.job':92503934624,
 'source.exact_main_dedicated_validation.artifact_id':8953863184,
 'source.exact_main_dedicated_validation.artifact_digest':'sha256:c50fa23976393044fa0ac410abb80c8c7b2fc1550151bd6c620279c1e689d606',
 'source.exact_main_dedicated_validation.conclusion':'success','source.exact_main_dedicated_validation.tests_run':13,
 'source.exact_main_dedicated_validation.tests_result':'OK','acknowledgement.schema':'stegverse.master_records.curiosity_motive_custody_ack.v1',
 'acknowledgement.acknowledgement_id':'MR-GCAT-CMG-CUSTODY-ACK-19F9E09-001','acknowledgement.task_id':'MR-GCAT-CMG-CUSTODY-001',
 'acknowledgement.source_manifest_id':'GCAT-CMG-03-OUTBOUND-FF8E3B0-001','acknowledgement.source_manifest_sha256':MANIFEST_SHA,
 'acknowledgement.source_receipt_sha256':RECEIPT_SHA,'acknowledgement.custody_state':'ACKNOWLEDGED',
 'acknowledgement.verification_status':'COMPLETE','acknowledgement.next_task':'GCAT-CMG-04',
 'acknowledgement.acknowledgement_hash':ACKNOWLEDGEMENT_HASH,'acknowledgement.destination_custody.repository':'master-records/core-lite',
 'acknowledgement.destination_custody.destination_commit':'19f9e093ce0348c748b71362b62249e9dfa7efc8',
 'acknowledgement.destination_custody.record_path':'records/gcat_bcat_curiosity_motive_admission_001.json',
 'acknowledgement.destination_custody.record_git_blob_sha':'f5aa980822d0459a2456a8220d9b52e364507a59',
 'acknowledgement.destination_custody.record_hash':CUSTODY_RECORD_HASH,
 'acknowledgement.destination_custody.repository_validation.workflow_run':31065016921,
 'acknowledgement.destination_custody.repository_validation.job':92500827200,
 'acknowledgement.destination_custody.repository_validation.tests_run':36,
 'acknowledgement.destination_custody.repository_validation.tests_result':'OK',
 'acknowledgement.destination_custody.repository_validation.conclusion':'success',
 'acknowledgement.destination_custody.dedicated_validation.workflow_run':31065016923,
 'acknowledgement.destination_custody.dedicated_validation.job':92500827206,
 'acknowledgement.destination_custody.dedicated_validation.artifact_id':8953515160,
 'acknowledgement.destination_custody.dedicated_validation.artifact_digest':'sha256:2e730d8d373b0c8c907ad13c515301516cd89031a068caebfc043cf0587caedb',
 'acknowledgement.destination_custody.dedicated_validation.tests_run':15,
 'acknowledgement.destination_custody.dedicated_validation.tests_result':'OK',
 'acknowledgement.destination_custody.dedicated_validation.conclusion':'success',
 'acknowledgement.validated_record.record_id':'GCAT-CMG-02-SV002-CURIOSITY-001',
 'acknowledgement.validated_record.record_hash':RECORD_SHA,
 'acknowledgement.validated_record.functional_motive_finding':'internally_coherent_functional_curiosity',
 'acknowledgement.validated_record.normative_decision':'DENY','expected_validation.status':'COMPLETE',
 'expected_validation.custody_state':'ACKNOWLEDGED','expected_validation.normative_decision':'DENY',
 'expected_validation.execution_activated':False,'expected_validation.input_mutated':False,
 'expected_validation.next_task':'SESSION-CONSOLIDATION-001'}
BOUNDARY={'custody_acknowledgement_only':True,'execution_activated':False,'execution_authority_granted':False,
 'occurrence_proven':False,'phenomenal_status_inferred':False,'policy_published':False,
 'public_publication_authorized':False,'quorum_formed':False,'repository_binding_granted':False,'runtime_activation':False}
FINDINGS={'canonical_decisions':['ALLOW','DENY','FAIL_CLOSED','NO_EXECUTION'],'motive_does_not_grant_authority':True,
 'normative_denial_does_not_negate_motive':True,'observer_description_does_not_define_motive':True,
 'phenomenal_status_not_inferred':True,'reconstruction_does_not_constitute_occurrence':True,
 'required_findings':['event','motivational','normative','observer'],'verifier_disagreement_fails_closed':True}
EFFECT={'custody_dependency_released':True,'custody_state':'ACKNOWLEDGED','execution_activated':False,
 'execution_authority_granted':False,'runtime_activation':False,'repository_binding_granted':False,
 'quorum_formed':False,'policy_published':False,'public_publication_authorized':False,
 'occurrence_proven':False,'phenomenal_status_inferred':False}
EXPECTED={'status':'COMPLETE','custody_state':'ACKNOWLEDGED','normative_decision':'DENY',
 'execution_activated':False,'input_mutated':False,'next_task':'SESSION-CONSOLIDATION-001'}

def validate(receipt:Any,manifest:Any,receipt_bytes:bytes,manifest_bytes:bytes,*,require_ack:bool=False,
 ack_import:Any=None,ack_import_bytes:bytes=b'',ack:Any=None)->Result:
 if ack_import is None and ack is not None:ack_import=ack
 before=copy.deepcopy((receipt,manifest,ack_import));e:list[str]=[];rd=sha_bytes(receipt_bytes);md=sha_bytes(manifest_bytes)
 if not isinstance(receipt,Mapping):e.append('type:receipt:expected_object');receipt={}
 if not isinstance(manifest,Mapping):e.append('type:manifest:expected_object');manifest={}
 if rd!=RECEIPT_SHA:e.append(f'mismatch:receipt_sha256:expected={RECEIPT_SHA}:actual={rd}')
 if md!=MANIFEST_SHA:e.append(f'mismatch:manifest_sha256:expected={MANIFEST_SHA}:actual={md}')
 for k,w in BASE_CHECKS.items():root,p=k.split('.',1);expect(receipt if root=='receipt' else manifest,p,w,e)
 for root in (receipt,manifest):
  try:b=get(root,'authority_boundary')
  except KeyError:e.append('missing:authority_boundary');continue
  if not isinstance(b,Mapping):e.append('type:authority_boundary:expected_object');continue
  for k,v in b.items():
   if k in {'evidence_admission_only','custody_candidate_only'}:
    if v is not True:e.append(f'mismatch:authority_boundary.{k}:expected=true')
   elif v is not False:e.append(f'mismatch:authority_boundary.{k}:expected=false')
 expect(manifest,'source.validation_receipt_sha256',rd,e)
 ih=ah=fh=crh=''
 if require_ack:
  if ack_import is None:
   return Result('BLOCKED',rd,md,'AWAITING_DESTINATION_ACKNOWLEDGEMENT',tuple(e),False,(receipt,manifest,ack_import)!=before,'MR-GCAT-CMG-CUSTODY-001')
  if not isinstance(ack_import,Mapping):e.append('type:ack_import:expected_object')
  else:
   for p,w in ACK_CHECKS.items():expect(ack_import,p,w,e)
   expect(ack_import,'acknowledgement.authority_boundary',BOUNDARY,e);expect(ack_import,'acknowledgement.findings_contract',FINDINGS,e)
   expect(ack_import,'import_effect',EFFECT,e);expect(ack_import,'expected_validation',EXPECTED,e)
   ih=hash_without(ack_import,'import_hash');fh=sha_bytes(ack_import_bytes)
   if ih!=ACK_IMPORT_HASH:e.append(f'mismatch:computed_import_hash:expected={ACK_IMPORT_HASH}:actual={ih}')
   a=ack_import.get('acknowledgement')
   if isinstance(a,Mapping):
    ah=hash_without(a,'acknowledgement_hash')
    if ah!=ACKNOWLEDGEMENT_HASH:e.append(f'mismatch:computed_acknowledgement_hash:expected={ACKNOWLEDGEMENT_HASH}:actual={ah}')
   try:
    if get(ack_import,'source.acknowledgement_hash')!=get(ack_import,'acknowledgement.acknowledgement_hash'):e.append('mismatch:source_acknowledgement_hash_vs_nested')
   except KeyError:pass
   if not e:crh=CUSTODY_RECORD_HASH
 mutated=(receipt,manifest,ack_import)!=before
 if mutated:e.append('internal_error:input_mutated')
 if e:return Result('FAIL_CLOSED',rd,md,'QUARANTINED',tuple(e),False,mutated,'REVIEW_REQUIRED',ih,ah,crh,fh)
 if require_ack:return Result('COMPLETE',rd,md,'ACKNOWLEDGED',(),False,False,'SESSION-CONSOLIDATION-001',ih,ah,CUSTODY_RECORD_HASH,fh)
 return Result('COMPLETE',rd,md,'CUSTODY_CANDIDATE_ONLY',(),False,False,'MR-GCAT-CMG-CUSTODY-001')

def read(p:Path)->tuple[Any,bytes]:raw=p.read_bytes();return json.loads(raw.decode()),raw
def main()->int:
 p=argparse.ArgumentParser();p.add_argument('--receipt',type=Path,default=RECEIPT);p.add_argument('--manifest',type=Path,default=MANIFEST)
 p.add_argument('--require-ack',action='store_true');p.add_argument('--ack-import','--ack',dest='ack_import',type=Path,default=ACK_IMPORT);a=p.parse_args()
 try:r,rb=read(a.receipt);m,mb=read(a.manifest)
 except FileNotFoundError as x:o=Result('FAIL_CLOSED',sha_bytes(b''),sha_bytes(b''),'QUARANTINED',('missing_input:'+str(x.filename),))
 except (OSError,UnicodeDecodeError,json.JSONDecodeError) as x:o=Result('FAIL_CLOSED',sha_bytes(b''),sha_bytes(b''),'QUARANTINED',('invalid_input:'+type(x).__name__,))
 else:
  ai=None;aib=b''
  if a.require_ack and a.ack_import.exists():
   try:ai,aib=read(a.ack_import)
   except (OSError,UnicodeDecodeError,json.JSONDecodeError) as x:
    o=Result('FAIL_CLOSED',sha_bytes(rb),sha_bytes(mb),'QUARANTINED',('invalid_ack_import:'+type(x).__name__,));print(canon(o.to_dict()));return 1
  o=validate(r,m,rb,mb,require_ack=a.require_ack,ack_import=ai,ack_import_bytes=aib)
 print(canon(o.to_dict()));return 0 if o.status=='COMPLETE' else (2 if o.status=='BLOCKED' else 1)
if __name__=='__main__':raise SystemExit(main())
