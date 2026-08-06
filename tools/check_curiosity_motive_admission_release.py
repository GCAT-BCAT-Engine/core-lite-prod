#!/usr/bin/env python3
"""Deterministic fail-closed release verifier for GCAT-CMG-03."""

from __future__ import annotations
import argparse, copy, hashlib, json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"receipts"/"curiosity-motive-admission-validation.json"
MANIFEST=ROOT/"outbound"/"curiosity-motive-admission-manifest.json"
RECEIPT_SHA="24d4984457708c4fea6b7a182bee82004b93be6d2cb21626300b48a13d8a72c2"
MANIFEST_SHA="6344432f06de75f771af0cb1148a6a0197ffdcadb21068b0eb246b0afcc469cc"
RECORD_SHA="6bfbd1af3aecd03c3b4579d0465f0962dd49f3741e786046a4189735223e3eac"

@dataclass(frozen=True)
class Result:
 status:str; receipt_sha256:str; manifest_sha256:str; custody_state:str
 errors:tuple[str,...]; execution_activated:bool=False; input_mutated:bool=False
 next_task:str="REVIEW_REQUIRED"
 def to_dict(self)->dict[str,Any]:
  return {"schema":"stegverse.gcat_bcat.curiosity_motive_admission_release_validation.v1",
   "status":self.status,"receipt_sha256":self.receipt_sha256,
   "manifest_sha256":self.manifest_sha256,"record_hash":RECORD_SHA,
   "normative_decision":"DENY","custody_state":self.custody_state,
   "errors":list(self.errors),"execution_activated":self.execution_activated,
   "input_mutated":self.input_mutated,"next_task":self.next_task}

def canon(v:Any)->str:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def sha(v:bytes)->str:return hashlib.sha256(v).hexdigest()
def get(r:Mapping[str,Any],path:str)->Any:
 v:Any=r
 for p in path.split("."):
  if not isinstance(v,Mapping) or p not in v:raise KeyError(path)
  v=v[p]
 return v
def expect(r:Mapping[str,Any],path:str,want:Any,e:list[str])->None:
 try:got=get(r,path)
 except KeyError:e.append("missing:"+path);return
 if got!=want:e.append(f"mismatch:{path}:expected={canon(want)}:actual={canon(got)}")

def validate(receipt:Any,manifest:Any,receipt_bytes:bytes,manifest_bytes:bytes,
             *,require_ack:bool=False,ack:Any=None)->Result:
 before=(copy.deepcopy(receipt),copy.deepcopy(manifest)); e:list[str]=[]
 rd,md=sha(receipt_bytes),sha(manifest_bytes)
 if not isinstance(receipt,Mapping):e.append("type:receipt:expected_object");receipt={}
 if not isinstance(manifest,Mapping):e.append("type:manifest:expected_object");manifest={}
 if rd!=RECEIPT_SHA:e.append(f"mismatch:receipt_sha256:expected={RECEIPT_SHA}:actual={rd}")
 if md!=MANIFEST_SHA:e.append(f"mismatch:manifest_sha256:expected={MANIFEST_SHA}:actual={md}")
 checks={
  "receipt.schema":"stegverse.gcat_bcat.curiosity_motive_admission_validation_receipt.v1",
  "receipt.receipt_id":"GCAT-CMG-03-VALIDATION-FF8E3B0-001",
  "receipt.validated_record.record_hash":RECORD_SHA,
  "receipt.validated_record.status":"COMPLETE",
  "receipt.validated_record.normative_decision":"DENY",
  "receipt.validated_record.execution_activated":False,
  "receipt.validated_record.input_mutated":False,
  "receipt.exact_main_validation.commit":"ff8e3b04628456c1bcc0571833a1a6f3071909ea",
  "receipt.exact_main_validation.workflow_run":31062909742,
  "receipt.exact_main_validation.job":92494415341,
  "receipt.exact_main_validation.conclusion":"success",
  "receipt.release_state.custody_state":"CUSTODY_CANDIDATE_ONLY",
  "manifest.schema":"stegverse.gcat_bcat.curiosity_motive_admission_outbound_manifest.v1",
  "manifest.manifest_id":"GCAT-CMG-03-OUTBOUND-FF8E3B0-001",
  "manifest.source.commit":"ff8e3b04628456c1bcc0571833a1a6f3071909ea",
  "manifest.source.validation_receipt_sha256":RECEIPT_SHA,
  "manifest.validated_record.record_hash":RECORD_SHA,
  "manifest.validated_record.normative_decision":"DENY",
  "manifest.validated_record.validation_status":"COMPLETE",
  "manifest.custody_request.destination_repository":"master-records/core-lite",
  "manifest.custody_request.task_id":"MR-GCAT-CMG-CUSTODY-001",
  "manifest.status":"READY_FOR_INDEPENDENT_CUSTODY_VERIFICATION",
  "manifest.next_task":"MR-GCAT-CMG-CUSTODY-001"}
 for key,want in checks.items():
  root,path=key.split(".",1);expect(receipt if root=="receipt" else manifest,path,want,e)
 for root,name in ((receipt,"authority_boundary"),(manifest,"authority_boundary")):
  try:b=get(root,name)
  except KeyError:e.append("missing:"+name);continue
  if not isinstance(b,Mapping):e.append("type:"+name+":expected_object");continue
  for k,v in b.items():
   if k in {"evidence_admission_only","custody_candidate_only"}:
    if v is not True:e.append(f"mismatch:{name}.{k}:expected=true")
   elif v is not False:e.append(f"mismatch:{name}.{k}:expected=false")
 expect(manifest,"source.validation_receipt_sha256",rd,e)
 mutated=(receipt,manifest)!=before
 if mutated:e.append("internal_error:input_mutated")
 if e:return Result("FAIL_CLOSED",rd,md,"QUARANTINED",tuple(e),False,mutated)
 if require_ack:
  if not isinstance(ack,Mapping):
   return Result("BLOCKED",rd,md,"AWAITING_DESTINATION_ACKNOWLEDGEMENT",(),False,False,"MR-GCAT-CMG-CUSTODY-001")
  for p,w in {"schema":"stegverse.master_records.curiosity_motive_custody_ack.v1",
              "task_id":"MR-GCAT-CMG-CUSTODY-001",
              "source_manifest_id":"GCAT-CMG-03-OUTBOUND-FF8E3B0-001",
              "source_manifest_sha256":md,"source_receipt_sha256":rd,
              "verification_status":"COMPLETE"}.items():expect(ack,p,w,e)
  if e:return Result("FAIL_CLOSED",rd,md,"QUARANTINED",tuple("ack:"+x for x in e))
  return Result("COMPLETE",rd,md,"ACKNOWLEDGED",(),False,False,"SESSION-CONSOLIDATION-001")
 return Result("COMPLETE",rd,md,"CUSTODY_CANDIDATE_ONLY",(),False,False,"MR-GCAT-CMG-CUSTODY-001")

def read(path:Path)->tuple[Any,bytes]:
 raw=path.read_bytes();return json.loads(raw.decode()),raw
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--receipt",type=Path,default=RECEIPT)
 p.add_argument("--manifest",type=Path,default=MANIFEST);p.add_argument("--require-ack",action="store_true")
 p.add_argument("--ack",type=Path);a=p.parse_args()
 try:
  r,rb=read(a.receipt);m,mb=read(a.manifest);ack=read(a.ack)[0] if a.ack else None
  out=validate(r,m,rb,mb,require_ack=a.require_ack,ack=ack)
 except FileNotFoundError as x:out=Result("FAIL_CLOSED",sha(b""),sha(b""),"QUARANTINED",("missing_input:"+str(x.filename),))
 except (OSError,UnicodeDecodeError,json.JSONDecodeError) as x:out=Result("FAIL_CLOSED",sha(b""),sha(b""),"QUARANTINED",("invalid_input:"+type(x).__name__,))
 print(canon(out.to_dict()));return 0 if out.status=="COMPLETE" else (2 if out.status=="BLOCKED" else 1)
if __name__=="__main__":raise SystemExit(main())
