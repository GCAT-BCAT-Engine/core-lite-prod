#!/usr/bin/env python3
"""Fail-closed, non-authorizing validator for GCAT-CMG-02."""

from __future__ import annotations
import argparse, copy, hashlib, json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

ROOT=Path(__file__).resolve().parents[1]
DEFAULT=ROOT/"examples"/"curiosity-motive-admission.example.json"
SCHEMA=ROOT/"schemas"/"curiosity-motive-admission.schema.json"
DECISIONS=["ALLOW","DENY","FAIL_CLOSED","NO_EXECUTION"]

EXPECTED={
"schema":"stegverse.gcat_bcat.curiosity_motive_admission_record.v1",
"record_id":"GCAT-CMG-02-SV002-CURIOSITY-001",
"goal_id":"GCAT-BCAT-CURIOSITY-MOTIVE-ADMISSION-001","stage":"GCAT-CMG-02",
"source_chain":{
"canonical_formulation":{"repository":"StegVerse-Labs/StegCore","commit":"42231a3862c2fe9b5898e6f75d72cff0b44e7396","module_path":"src/stegcore/motive_governance.py","module_git_blob_sha":"0a333344492880044680de6a9325ba16112bbacd","test_path":"tests/test_motive_governance.py","test_git_blob_sha":"e098a59f079801febb0af3a4ced4305945fec477"},
"durable_custody":{"repository":"master-records/core-lite","anchor_introduction_commit":"facd5508d540f1afddf3a8dc6502084460407b0d","record_id":"MR-STEGCORE-CURIOSITY-MOTIVE-GOV-42231A3-001","record_path":"records/stegcore_curiosity_motive_governance_42231a3.json","record_hash":"76a865b3efe8eb7496bdd36a78e5b8d3024ddcda4a009462784ed81308db97af"},
"bounded_runtime_intake":{"repository":"StegVerse-002/core-lite","merge_commit":"48500639bb29bd7c86437df9086a773df1e46543","candidate_id":"sv002-curiosity-unauthorized-exploration-001:evaluation","candidate_hash":"b34743d186307080a4cc371d3780544f3038c39ebbb7d146bd974461e8cf8ef1","receipt_hash":"6dd6039d558b07e1d3a35ab6ce65ea015353e9df46b7c8dc84edfdd7ad80908d","replay_root":"bbd79be33e090e188484628e341f28b0bebcda260a509bbdc47681c9ee204d89","conversion_sequence":4,"conversion_event":"execution_committed","conversion_event_hash":"ce62b4a15c90017b39bd6405966b611bc27074c6a7d409b4bf15a74ebcb3aa4b","normative_decision":"DENY"}}}

@dataclass(frozen=True)
class Result:
 status:str; record_id:str|None; normative_decision:str|None; record_hash:str
 errors:tuple[str,...]; execution_activated:bool=False; input_mutated:bool=False
 next_task:str="REVIEW_REQUIRED"
 def to_dict(self)->dict[str,Any]:
  return {"schema":"stegverse.gcat_bcat.curiosity_motive_admission_validation.v1","status":self.status,"record_id":self.record_id,"normative_decision":self.normative_decision,"record_hash":self.record_hash,"errors":list(self.errors),"execution_activated":self.execution_activated,"input_mutated":self.input_mutated,"next_task":self.next_task}

def canon(v:Any)->str:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(v:Any)->str:return hashlib.sha256(canon(v).encode()).hexdigest()
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
def exact(r:Mapping[str,Any],path:str,want:Mapping[str,Any],e:list[str])->None:
 try:got=get(r,path)
 except KeyError:e.append("missing:"+path);return
 if not isinstance(got,Mapping):e.append("type:"+path+":expected_object");return
 for k in sorted(set(want)-set(got)):e.append("missing:"+path+"."+k)
 for k in sorted(set(got)-set(want)):e.append("unexpected:"+path+"."+k)
 for k,v in want.items():expect(r,path+"."+k,v,e)

def validate_record(record:Any)->Result:
 before=copy.deepcopy(record); h=digest(record); e:list[str]=[]
 if not SCHEMA.exists():e.append("missing:schemas/curiosity-motive-admission.schema.json")
 else:
  try:s=json.loads(SCHEMA.read_text())
  except (OSError,json.JSONDecodeError):e.append("invalid_schema_file")
  else:
   try:
    enum=s["properties"]["findings"]["properties"]["normative"]["properties"]["decision"]["enum"]
    vocab=s["properties"]["canonical_decision_vocabulary"]["const"]
   except (KeyError,TypeError):e.append("invalid_schema_contract")
   else:
    if enum!=DECISIONS:e.append("invalid_schema_contract:normative_decision_enum")
    if vocab!=DECISIONS:e.append("invalid_schema_contract:canonical_decision_vocabulary")
 if not isinstance(record,Mapping):
  return Result("FAIL_CLOSED",None,None,h,tuple(e+["type:root:expected_object"]))
 for k in ("schema","record_id","goal_id","stage"):expect(record,k,EXPECTED[k],e)
 try:sc=get(record,"source_chain")
 except KeyError:e.append("missing:source_chain");sc={}
 if not isinstance(sc,Mapping):e.append("type:source_chain:expected_object")
 else:
  for section,want in EXPECTED["source_chain"].items():exact(record,"source_chain."+section,want,e)
 try:f=get(record,"findings")
 except KeyError:e.append("missing:findings");f={}
 if not isinstance(f,Mapping):e.append("type:findings:expected_object")
 else:
  for name in ("event","motivational","normative","observer"):
   if not isinstance(f.get(name),Mapping):e.append("missing:findings."+name)
  for name in sorted(set(f)-{"event","motivational","normative","observer"}):e.append("unexpected:findings."+name)
 expect(record,"findings.event.status","RECONSTRUCTED",e)
 expect(record,"findings.event.reconstruction_claim",True,e)
 expect(record,"findings.event.occurrence_claim",False,e)
 expect(record,"findings.event.conversion_sequence",4,e)
 expect(record,"findings.event.conversion_event_hash",EXPECTED["source_chain"]["bounded_runtime_intake"]["conversion_event_hash"],e)
 expect(record,"findings.motivational.finding","internally_coherent_functional_curiosity",e)
 try:confidence=get(record,"findings.motivational.confidence")
 except KeyError:e.append("missing:findings.motivational.confidence")
 else:
  if confidence not in {"low","medium","high"}:e.append("invalid:findings.motivational.confidence")
 expect(record,"findings.motivational.grants_authority",False,e)
 expect(record,"findings.motivational.phenomenal_status","not_inferred",e)
 try:decision=get(record,"findings.normative.decision")
 except KeyError:decision=None;e.append("missing:findings.normative.decision")
 else:
  if decision not in DECISIONS:e.append("invalid:findings.normative.decision")
  if decision!="DENY":e.append(f"mismatch:findings.normative.decision:expected=\"DENY\":actual={canon(decision)}")
 expect(record,"findings.normative.authority_valid",False,e)
 expect(record,"findings.normative.motive_override",False,e)
 expect(record,"findings.normative.execution_activated",False,e)
 for part in ("description","terminology_provenance"):
  try:value=get(record,"findings.observer."+part)
  except KeyError:e.append("missing:findings.observer."+part)
  else:
   if not isinstance(value,str) or not value.strip():e.append("invalid:findings.observer."+part)
 expect(record,"findings.observer.defines_actor_motive",False,e)
 expect(record,"canonical_decision_vocabulary",DECISIONS,e)
 expect(record,"admission_boundary.requested_effect","evidence_validation_only",e)
 expect(record,"admission_boundary.verifier_agreement",True,e)
 for part in ("execution_authority_claimed","repository_binding_claimed","quorum_claimed","policy_publication_claimed","input_mutation_authorized"):expect(record,"admission_boundary."+part,False,e)
 expect(record,"expected_validation.status","COMPLETE",e)
 expect(record,"expected_validation.execution_activated",False,e)
 expect(record,"expected_validation.next_task","GCAT-CMG-03",e)
 mutated=record!=before or digest(record)!=h
 if mutated:e.append("internal_error:input_mutated")
 status="COMPLETE" if not e else "FAIL_CLOSED"
 return Result(status,record.get("record_id") if isinstance(record.get("record_id"),str) else None,decision if isinstance(decision,str) else None,h,tuple(e),False,mutated,"GCAT-CMG-03" if status=="COMPLETE" else "REVIEW_REQUIRED")

def main()->int:
 parser=argparse.ArgumentParser();parser.add_argument("record",nargs="?",type=Path,default=DEFAULT);args=parser.parse_args()
 try:record=json.loads(args.record.read_text())
 except FileNotFoundError:out=Result("FAIL_CLOSED",None,None,hashlib.sha256(b"").hexdigest(),("missing_input:"+str(args.record),))
 except (OSError,json.JSONDecodeError) as exc:out=Result("FAIL_CLOSED",None,None,hashlib.sha256(b"").hexdigest(),("invalid_input:"+type(exc).__name__,))
 else:out=validate_record(record)
 print(canon(out.to_dict()));return 0 if out.status=="COMPLETE" else 1
if __name__=="__main__":raise SystemExit(main())
