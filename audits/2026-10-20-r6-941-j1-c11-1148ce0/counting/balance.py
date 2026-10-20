#!/usr/bin/env python3
"""Exact 132-row complete-count identity; stdlib only, default read-only."""
from pathlib import Path
import argparse
import gzip
import hashlib
import importlib.util
import json

D=Path(__file__).resolve().parent
OLD=D.parent/"frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c"
spec=importlib.util.spec_from_file_location("frozen_c11",OLD/"interface/check.py")
o=importlib.util.module_from_spec(spec)
spec.loader.exec_module(o)


def packed(x):
    return json.dumps(x,sort_keys=True,separators=(",",":")).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def model():
    path=OLD/"interface/certificate-v4.json.gz"
    inter=json.load(gzip.open(path,"rt"))
    states=[t for t in o.m.growth(11,four=True) if o.m.proper(t)]
    assert states==[tuple(c["core"]) for c in inter["caps"]]
    K=o.old.kempe(11,states)
    assert hashlib.sha256(packed(K["columns"])).hexdigest()==inter["kempe"]["columns_sha256"]
    live=set(inter["live"])
    good=[j for j,col in enumerate(K["columns"]) if all(K["rowids"][r] in live for r,v in col)]
    return inter,states,K,live,good


def build(data):
    inter,states,K,live,good=data
    ray_path=D.parent/"geometry/orbit-farkas-certificate.json"
    ray=json.loads(ray_path.read_text())
    assert ray["positive_row_multipliers"]==[[9,16]]
    assert all(r<len(K["hrows"]) for r,v in ray["equality_multipliers"])
    signed=[{"id":r,"literal":K["hrows"][r],"weight":v}
            for r,v in ray["equality_multipliers"] if K["rowids"][r] in live]
    return {
        "version":1,
        "ordered_rim":list(o.NAMES),
        "interface_sha256":sha(OLD/"interface/certificate-v4.json.gz"),
        "full_orbit_columns_sha256":inter["kempe"]["columns_sha256"],
        "full_ray_sha256":sha(ray_path),
        "half_row_weights":signed,
        "short_witness_ids":[r["canonical_id"] for r in inter["witnesses"]],
        "short_witness_literals":[r["literal"] for r in inter["witnesses"]],
        "witness_multiplier":16,
        "core_states":7381,
        "proved_zero_core_fibres":1430,
        "all_half_rows":22143,
        "all_complete_orbit_columns":36487,
        "remaining_complete_orbit_columns":20794,
        "forced_zero_orbit_columns":15693,
        "claim":"16*(Z_5093+Z_5100)=0",
        "new_Lean":False,
    }


def verify(cert,data):
    inter,states,K,live,good=data
    assert cert["version"]==1 and cert["ordered_rim"]==list(o.NAMES)
    assert cert["interface_sha256"]==sha(OLD/"interface/certificate-v4.json.gz")
    assert cert["full_orbit_columns_sha256"]==inter["kempe"]["columns_sha256"]
    assert cert["full_ray_sha256"]==sha(D.parent/"geometry/orbit-farkas-certificate.json")
    assert cert["short_witness_ids"]==[r["canonical_id"] for r in inter["witnesses"]]
    assert cert["short_witness_literals"]==[r["literal"] for r in inter["witnesses"]]
    assert cert["witness_multiplier"]==16 and cert["new_Lean"] is False
    assert cert["claim"]=="16*(Z_5093+Z_5100)=0"
    assert [cert[k] for k in ("core_states","proved_zero_core_fibres","all_half_rows",
            "all_complete_orbit_columns","remaining_complete_orbit_columns","forced_zero_orbit_columns")]==[
            len(states),len(states)-len(live),len(K["hrows"]),len(K["columns"]),
            len(good),len(K["columns"])-len(good)]
    assert len(states)==7381 and len(good)==20794
    y=[0]*len(K["hrows"]);used=set()
    for rec in cert["half_row_weights"]:
        r,v=rec["id"],rec["weight"]
        assert type(r) is int and type(v) is int and v in (-1,1)
        assert 0<=r<len(y) and r not in used and K["rowids"][r] in live
        assert rec["literal"]==list(K["hrows"][r])
        used.add(r);y[r]=v
    assert len(used)==132 and y.count(1)==64 and y.count(-1)==68
    core=[0]*len(states)
    for r,i in enumerate(K["rowids"]):
        core[i]+=K["hsize"][r]*y[r]
    expected=[0]*len(states)
    for i in cert["short_witness_ids"]:
        expected[i]=-cert["witness_multiplier"]
    assert core==expected,"signed halfrows do not give exactly the two complete fibres"
    for j in good:
        assert sum(y[r]*v for r,v in K["columns"][j])==0,("unbalanced complete orbit",j)
    # Every omitted column has a positive entry in a halfrow whose full core
    # fibre is already zero. AZ=B beta and beta>=0 force its beta to zero.
    good_set=set(good)
    for j,col in enumerate(K["columns"]):
        if j not in good_set:
            assert any(v>0 and K["rowids"][r] not in live for r,v in col)
    return {
        "status":"PASS exact 132-row complete-count identity",
        "positive_half_rows":64,"negative_half_rows":68,
        "remaining_complete_orbit_columns":len(good),
        "forced_zero_orbit_columns":len(K["columns"])-len(good),
        "identity":cert["claim"],
        "both_short_complete_fibres_zero":True,
        "arbitrary_source_excluded_under_inherited_contract":True,
        "signed_planar_span_used":False,"numeric_solver_used":False,"new_Lean":False,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--build",action="store_true")
    ap.add_argument("--certificate",type=Path,default=D/"balance-certificate.json")
    args=ap.parse_args()
    data=model()
    cert=json.loads(packed(build(data))) if args.build else json.loads(args.certificate.read_text())
    result=verify(cert,data)
    if args.build:
        with args.certificate.open("x") as out:
            json.dump(cert,out,ensure_ascii=False,indent=2);out.write("\n")
    print(json.dumps(result,sort_keys=True))


if __name__=="__main__":
    main()
