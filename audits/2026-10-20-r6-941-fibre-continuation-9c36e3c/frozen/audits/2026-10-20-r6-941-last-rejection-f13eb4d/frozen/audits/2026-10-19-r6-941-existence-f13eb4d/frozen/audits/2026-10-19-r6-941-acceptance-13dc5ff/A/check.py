#!/usr/bin/env python3
"""Exact stdlib replay of common-core acceptance-zero controls and support closure."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
Q=ROOT/"audits/2026-10-19-r6-941-quotients-13dc5ff/A"
OLD=ROOT/"audits/2026-10-19-r6-941-leakage-b89c591/A"
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=module("interface_model",Q/"model.py");o=module("counted_model",OLD/"model.py")
BASE="13dc5ff163045c85b5c82dde438eb5f275dab999"
CAT=ROOT/"audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json"
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def verify_controls(cert,data):
 eight,ten,index,transfer,hrows,hi,hist,parts,M,MU=data
 assert cert["base"]==BASE,"BASE"
 assert cert["source_realized"] is False and cert["smaller_bad_source_constructed"] is False,"authority boundary"
 assert cert["pin_order"]==["a","n","R","L","q","c","s","v","w","t"] and cert["rows"]==list(o.ROWS),"literal pin order"
 assert cert["source_positive_subset_ids"]==o.source_positive_subsets(index),"source positive restrictions"
 required=(OLD/"model.py",Q/"model.py",Q.parent/"SOURCE_CONTRACT.md",D.parent/"INPUTS.json",CAT)
 assert cert["inputs_sha256"]=={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in required},"complete frozen input binding"
 assert [r["name"] for r in cert["records"]]==["Q1_accept_zero","Q2_accept_zero"],"complete branch domain"
 K=set(map(int,json.loads(CAT.read_text())["cells"]));assert len(K)==132,"frozen full K132 catalogue"
 out=[]
 for rec in cert["records"]:
  name=rec["zero_acceptance_candidate"];other="Q2" if name=="Q1" else "Q1"
  assert rec["name"]==name+"_accept_zero" and name in ("Q1","Q2"),"branch label"
  z=rec["core_counts"];assert len(z)==2461 and all(type(v) is int and v>=0 for v in z),"nonnegative complete core counts"
  coeff=rec["planar_coefficients"];assert len({j for j,v in coeff})==len(coeff) and all(type(j) is int and 0<=j<603 and type(v) is int and v for j,v in coeff),"signed planar coefficient domain"
  rebuilt=[0]*2461
  for j,value in coeff:
   p=parts[j];pairs=[(i,next(k for k in range(i) if p[k]==p[i])) for i in range(10) if p[i] in p[:i]]
   for i,t in enumerate(ten):
    if all(t[a]==t[b] for a,b in pairs):rebuilt[i]+=value
  assert rebuilt==z,"same-core signed planar span"
  residual=[-hist[t]*z[index[o.canonical(t)]] for t in hrows];seen=set()
  for orbit in rec["orbits"]:
   key=(tuple(orbit["start"]),tuple(orbit["partition"]));assert key not in seen,"duplicate complete orbit";seen.add(key)
   w=orbit["weight"];assert type(w) is int and w>0,"positive complete orbit weight"
   for j,value in o.orbit_column(*key,hi).items():residual[j]+=w*value
  assert not any(residual),"full literal counted-component equations"
  e=[sum(v*z[i] for i,v in r) for r in transfer];assert e==rec["exterior_counts"],"same complete cap transfer"
  counts={g:o.mv(mat,e) for g,mat in M.items()};assert counts==rec["graph_counts"],"same-source complete graph lifts"
  assert o.mask(counts["G"])==941,"all ten original support fibres"
  masks={g:o.mask(counts[g]) for g in ("Q1","Q2","GB")}
  assert all(v in K for v in masks.values()),"all three candidate full supports in K132"
  u=o.mv(MU,z);assert u==rec["U_counts"] and o.mask(u)==319,"full same-core U319"
  pos={s:sum(z[i] for i in ids) for s,ids in cert["source_positive_subset_ids"].items()}
  assert pos==rec["source_positive_subset_counts"] and all(v>0 for v in pos.values()),"both mandatory source-positive fibres"
  assert counts[name][9]==0 and counts[other][9]>0,"selected zero and same other acceptance"
  assert counts[other][4]>0 and counts[other][6]>0,"same accepting candidate two surviving rejections"
  out.append({"zero_acceptance_candidate":name,"other_acceptance":counts[other][9],"other_rejections":[counts[other][j] for j in (1,4,6)],"source_mask":941,"candidate_masks":masks,"U_mask":319,"d_a":pos["h_equals_a"],"d_b":pos["h_equals_b"],"positive_core_fibres":sum(v>0 for v in z),"complete_counted_orbits":len(rec["orbits"]),"source_realized":False})
 return out

def reconstruct_closures():
 F=m.interfaces();K=m.kempe(10,F["ten"]);K8=m.kempe(8,F["eight"])
 base=[i for i in range(2461) if all(F["C"]["G"][j][i]==0 for j in (1,4,6))]
 base8=[i for i in range(274) if all(F["M"]["G"][j][i]==0 for j in (1,4,6))]
 obs=[F["M"]["Q1"][9],F["M"]["Q2"][9]]+[F["M"][g][j] for g in ("Q1","Q2","GB") for j in (1,4,6)]+[F["sectors"][s] for s in ("Aa","Ab")]
 subsets=o.source_positive_subsets({t:i for i,t in enumerate(F["ten"])})
 results={}
 for name in ("base","Q1","Q2"):
  initial=base if name=="base" else [i for i in base if not F["C"][name][9][i]]
  live,rounds=m.close(K,initial)
  initial8=base8 if name=="base" else [i for i in base8 if not F["M"][name][9][i]]
  live8,rounds8=m.close(K8,initial8);parts,A,basis=m.planar_basis(F["eight"],live8)
  _,piv=m.rref([[sum(x*y for x,y in zip(v,b)) for v in obs] for b in basis])
  survive={g:{m.ROWS[j]:sum(F["C"][g][j][i] for i in live) for j in (1,4,6,9)} for g in ("G","Q1","Q2","GB")}
  results[name]={"initial":initial,"rounds":rounds,"live":live,"candidate_projection_units":survive,"source_positive_subset_survivors":{s:[i for i in ids if i in live] for s,ids in subsets.items()},"E_initial":initial8,"E_rounds":rounds8,"E_live":live8,"E_planar_dimension":len(basis),"E_basis_sha256":sha([[str(v) for v in b] for b in basis]),"observable_projection_rank":len(piv)}
 assert len(results["base"]["live"])==2023
 for name in ("Q1","Q2"):
  r=results[name];assert len(r["live"])==1973 and r["E_planar_dimension"]==40 and r["observable_projection_rank"]==8
  assert all(r["candidate_projection_units"][g][m.ROWS[j]]>0 for g in ("Q1","Q2") for j in (1,4,6))
 return {"base":BASE,"model_input_sha256":hashlib.sha256((Q/"model.py").read_bytes()).hexdigest(),"full_source_contract_sha256":hashlib.sha256((Q.parent/"SOURCE_CONTRACT.md").read_bytes()).hexdigest(),"columns":len(K["columns"]),"columns_sha256":sha(K["columns"]),"H_rows":len(K["hrows"]),"results":results,"main_target_closed":False,"model_controls_are_source_realizations":False}

def reconstruct_chains():
 F=m.interfaces();ix={t:i for i,t in enumerate(F["ten"])};records=[]
 for name,R,L,pair,root,avoid in (("Q1",3,1,(2,3),2,(4,)),("Q2",2,3,(1,3),3,(1,9))):
  for v,w in ((2,3),(3,2)):
   t=(0,1,R,L,2,0,1,v,w,1);i=ix[m.canonical(t)];valid=[]
   # Use literal caps rather than canonical colours for every switch.
   def left(a):
    A,N,U,V,Q,C,S,I,J,T=a
    return [(b,p,h) for b in range(4) for p in range(4) for h in range(4) if b not in {A,C,Q,p} and p not in {A,Q,N,h} and h not in {Q,U,V,N}]
   def right(a):
    A,N,U,V,Q,C,S,I,J,T=a
    return [(x,y,r) for x in range(4) for y in range(4) for r in range(4) if r not in {S,I,J,T,x,y} and x not in {C,S,y} and y not in {A,T}]
   assert (1,3,0) in left(t) and (2,3,0) in right(t)
   for mask in range(1<<10):
    if not mask&(1<<root) or any(mask&(1<<j) for j in avoid):continue
    if any(mask&(1<<j) and c not in pair for j,c in enumerate(t)):continue
    switched=tuple((sum(pair)-c) if mask&(1<<j) else c for j,c in enumerate(t))
    if not m.proper(switched):continue
    assert (1,3,0) in left(switched) and (2,3,0) in right(switched),"all fixed original cap attachments after actual component switch"
    A,N,U,V,Q,C,S,I,J,T=switched
    assert 1 not in {A,C,Q}
    assert (N==1 and U==Q) if name=="Q1" else (N==V==1)
    valid.append({"mask":mask,"switched_core":list(switched)})
   assert valid
   records.append({"zero_acceptance_candidate":name,"literal_core":list(t),"canonical_core_id":i,"fixed_left_cap":[1,3,0],"fixed_right_cap":[2,3,0],"swap_pair":list(pair),"root_boundary_index":root,"must_meet_boundary_indices":list(avoid),"all_proper_separating_swaps":valid})
 return {"base":BASE,"source_scope":"every full h=a D_old fibre of the named complete 941 source","records":records,"component_interpretation":{"Q1":"R and q are in the same F[{2,3}] component","Q2":"the F[{1,3}] component of L meets n or t"}}

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--build",action="store_true");ap.add_argument("--negative-controls",action="store_true");args=ap.parse_args()
 data=o.build();cert=json.loads((D/"acceptance-zero-controls.json").read_text());summary=verify_controls(cert,data)
 expected=reconstruct_closures();path=D/"support-closures.json"
 if args.build:
  if path.exists():assert json.loads(path.read_text())==expected
  else:
   with path.open("x") as f:json.dump(expected,f,indent=2);f.write("\n")
 actual=json.loads(path.read_text());assert actual==expected,"complete simultaneous support closure"
 chain_expected=reconstruct_chains();chain_path=D/"chain-certificates.json"
 if args.build:
  with chain_path.open("x") as f:json.dump(chain_expected,f,indent=2);f.write("\n")
 chain_actual=json.loads(chain_path.read_text());assert chain_actual==chain_expected,"full original-source component-switch caps"
 for rec in cert["records"]:
  branch=actual["results"][rec["zero_acceptance_candidate"]];live=set(branch["live"]);live8=set(branch["E_live"])
  assert all(v==0 for i,v in enumerate(rec["core_counts"]) if i not in live),"all derived empty core fibres"
  assert all(v==0 for i,v in enumerate(rec["exterior_counts"]) if i not in live8),"all derived empty exterior fibres"
 negative=[]
 if args.negative_controls:
  def reject(name,mutate):
   bad=copy.deepcopy(cert);mutate(bad)
   try:verify_controls(bad,data)
   except AssertionError as e:negative.append({"name":name,"rejected":True,"reason":str(e)})
   else:raise AssertionError("accepted negative control: "+name)
  reject("different-core-count-splice",lambda c:c["records"][0].__setitem__("core_counts",c["records"][1]["core_counts"]))
  reject("drop-complete-orbit-multiplicity",lambda c:c["records"][0]["orbits"][0].__setitem__("weight",c["records"][0]["orbits"][0]["weight"]+1))
  reject("truncate-signed-planar-span",lambda c:c["records"][0]["planar_coefficients"].pop())
  reject("cross-candidate-rejection-splice",lambda c:c["records"][0]["graph_counts"].__setitem__("Q2",c["records"][1]["graph_counts"]["Q2"]))
  reject("omit-positive-U-fibre",lambda c:c["records"][0]["U_counts"].__setitem__(8,0))
  reject("omit-source-positive-fibre",lambda c:c["records"][0]["source_positive_subset_counts"].__setitem__("h_equals_a",0))
  reject("claim-source-realization",lambda c:c.__setitem__("source_realized",True))
  reject("change-literal-frame",lambda c:c["pin_order"].reverse())
  for name,mutate in (("truncate-support-deletion-round",lambda c:c["results"]["Q1"]["rounds"][0].pop()),("drop-acceptance-zero-initial-condition",lambda c:c["results"]["Q2"].__setitem__("initial",c["results"]["base"]["initial"])),("false-new-linear-identity",lambda c:c["results"]["Q1"].__setitem__("observable_projection_rank",7))):
   bad=copy.deepcopy(actual);mutate(bad);assert bad!=expected;negative.append({"name":name,"rejected":True,"reason":"complete simultaneous support closure"})
 if args.negative_controls:
  bad=copy.deepcopy(chain_actual);bad["records"][0]["fixed_left_cap"][1]=2;assert bad!=chain_expected;negative.append({"name":"change-fixed-original-cap","rejected":True,"reason":"full original-source component-switch caps"})
 print(json.dumps({"source_component_chain_records":len(chain_actual["records"]),"pass":True,"base":BASE,"exact_integer_same_core_controls":summary,"support_branch_live":{n:len(v["live"]) for n,v in actual["results"].items()},"negative_controls":negative,"main_target":"OPEN"},sort_keys=True,ensure_ascii=False))
if __name__=="__main__":main()
