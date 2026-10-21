#!/usr/bin/env python3
"""Independent synchronous full-family zero propagation for 40 fixed profiles.

A uint64 bit tracks each source separately. Columns take intersections of their
complete state sets; half-rows take unions of incident columns; states take
intersections of their three half-rows. This is separate from queue/DAG proofs.
"""
import argparse
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = "audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/"
PROFILE = "audits/2026-10-21-w7-structural-30f2d19/review/profile_orbits.json"
EDGES = [["u3","v"],["u1","v"],["u3","w"],["u1","w"],
         ["u4","v"],["u3","s"],["u2","v"],["u2","w"]]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_inputs():
    manifest = json.loads((HERE/"BASE.json").read_text())
    require(manifest["base_commit"] == "d23f94f739468593db653ec03f903c30adfd5fb0", "wrong BASE")
    records = {r["path"]:r for r in manifest["inputs"]}
    result = []
    for name in [SOURCE+"caps.json.gz",SOURCE+"orbits.json.gz",PROFILE]:
        raw = (ROOT/name).read_bytes()
        frozen = (HERE/records[name]["frozen_path"]).read_bytes()
        require(raw == frozen and len(raw) == records[name]["bytes"] and
                hashlib.sha256(raw).hexdigest() == records[name]["sha256"], "source drift: "+name)
        result.append(json.loads(gzip.decompress(raw) if name.endswith(".gz") else raw))
    return result


def compute():
    caps, orbit, profile_table = read_inputs()
    names = caps["ordered_rim"]
    require(names == ["a","n","u4","u3","u2","u1","L","q","c","s","v","w","t"], "changed ordered rim")
    states = np.asarray(caps["states"],dtype=np.uint8)
    pairs = sorted(orbit["rowids"])
    keys = np.asarray([h for h,s in pairs],dtype=np.int64)
    rowstate = np.asarray([s for h,s in pairs],dtype=np.int64)
    lengths = np.asarray([len(c) for c in orbit["columns"]],dtype=np.int64)
    offsets = np.concatenate([np.zeros(1,dtype=np.int64),np.cumsum(lengths)[:-1]])
    raw_rows = np.asarray([h for col in orbit["columns"] for h in col],dtype=np.int64)
    rows = np.searchsorted(keys,raw_rows)
    require(np.array_equal(keys[rows],raw_rows), "unmapped half-row")
    flat_states = rowstate[rows]
    row_degree = np.bincount(rows,minlength=len(keys))
    base_live = np.ones(len(states),dtype=np.bool_)
    np.logical_and.at(base_live,rowstate,row_degree>0)
    require(int(base_live.sum()) == 61308, "wrong original fixed point")
    profiles = [p for p in profile_table["profiles"] if any(p["retained_columns"].values())]
    require(len(profiles)==40,"wrong original coverage")
    cases = [{"name":"edge:"+"-".join(edge),"original_chords":[edge]} for edge in EDGES]
    cases += [{"name":"profile:"+str(p["original_profile_id"]),
               "original_profile_id":p["original_profile_id"],"original_chords":p["original_chords"]} for p in profiles]
    require(len(cases)<64,"too many simultaneous cases")
    live = np.zeros(len(states),dtype=np.uint64)
    for bit,case in enumerate(cases):
        proper = base_live.copy()
        for a,b in case["original_chords"]:
            proper &= states[:,names.index(a)] != states[:,names.index(b)]
        live[proper] |= np.uint64(1<<bit)
    rounds = []
    for step in range(len(states)+1):
        column_live = np.bitwise_and.reduceat(live[flat_states],offsets)
        supported = np.zeros(len(keys),dtype=np.uint64)
        np.bitwise_or.at(supported,rows,np.repeat(column_live,lengths))
        next_live = live.copy()
        np.bitwise_and.at(next_live,rowstate,supported)
        rounds.append({"round":step,"live_states":[int(np.count_nonzero(next_live & np.uint64(1<<b))) for b in range(len(cases))]})
        if np.array_equal(next_live,live):
            break
        live = next_live
    else:
        raise ValueError("synchronous iteration failed to terminate")
    results=[]
    for bit,case in enumerate(cases):
        state_ids=np.flatnonzero(live & np.uint64(1<<bit)).tolist()
        column_ids=np.flatnonzero(column_live & np.uint64(1<<bit)).tolist()
        target_alive=[s for s in [44459,44466] if s in state_ids]
        result={**case,"live_state_count":len(state_ids),"live_column_count":len(column_ids),
                "live_state_ids":state_ids,"live_column_ids":column_ids,"target_states_alive":target_alive,
                "excluded_by_target_zero":not target_alive}
        results.append(result)
    return {"method":"independent synchronous uint64 intersections and unions over all full original columns",
            "base":"d23f94f739468593db653ec03f903c30adfd5fb0","original_states":61308,
            "original_columns":len(orbit["columns"]),"cases":results,"synchronous_rounds":rounds,
            "source_realization_claimed":False,"general_W7":"OPEN","new_Lean":False}


def verify(expected, actual):
    require(expected==actual,"independent full state/column result mismatch")
    cases={r["name"]:r for r in actual["cases"]}
    require(cases["profile:0"]["target_states_alive"]==[44459,44466],"the chordless control lost targets")
    return True


def controls(actual):
    bad=deepcopy(actual); bad["cases"][0]["live_state_ids"].append(44459)
    try:
        verify(bad,actual)
    except ValueError:
        pass
    else:
        raise ValueError("a corrupted full state list was accepted")
    bad=deepcopy(actual); bad["cases"][0]["original_chords"]=[["u3","w"]]
    try:
        verify(bad,actual)
    except ValueError:
        pass
    else:
        raise ValueError("a replaced source-edge gate was accepted")
    require(actual["cases"][8]["name"]=="profile:0","missing no-edge control")
    return ["corrupted full state list rejected","replaced original-edge gate rejected",
            "no-edge positive-target control retained"]


def verify_residual(actual):
    manifest=json.loads((HERE/"BASE.json").read_text())
    records={r["path"]:r for r in manifest["inputs"]}
    names=["audits/2026-10-21-w7-structural-30f2d19/geometry/certificate.json",
           "audits/2026-10-21-w7-u1v-30f2d19/RESIDUAL.json"]
    inputs=[]
    for name in names:
        raw=(ROOT/name).read_bytes(); record=records[name]
        require(raw==(HERE/record["frozen_path"]).read_bytes() and
                hashlib.sha256(raw).hexdigest()==record["sha256"],"residual source drift: "+name)
        inputs.append(json.loads(raw))
    geometry, prior=inputs
    table={r["original_profile_id"]:r for r in geometry["profiles"]}
    cert=json.loads((HERE/"RESIDUAL.json").read_text())
    remaining=[r for r in actual["cases"][8:] if not r["excluded_by_target_zero"]]
    excluded={r["original_profile_id"] for r in actual["cases"][8:] if r["excluded_by_target_zero"]}
    previous=set(prior["previously_excluded_original_profile_ids"]+prior["newly_excluded_original_profile_ids"])
    require(cert["remaining_original_profile_ids"]==[r["original_profile_id"] for r in remaining]==[0,1],
            "the complete remaining source coverage changed")
    require(cert["newly_excluded_original_profile_ids"]==sorted(excluded-previous) and
            cert["previously_excluded_original_profile_ids"]==sorted(previous),"exclusion partition changed")
    require(len(excluded)==38 and len(previous)==16,"wrong profile counts")
    require(cert["scope"]=="same original 941/Q1 acceptance-zero/J1 type-III five-edge strict only-R/W7 source; complete original positive-witness profile coverage",
            "source scope changed")
    require(cert["general_W7"]==cert["general_J1_J2"]=="OPEN" and
            cert["source_realization_claimed"] is False and cert["new_Lean"] is False,"scope was promoted")
    require(len(cert["profiles"])==len(remaining),"remaining profile omitted")
    for saved,case in zip(cert["profiles"],remaining):
        i=case["original_profile_id"]
        require(saved["original_profile_id"]==i and saved["complete_original_contacts"]==table[i]["profile"] and
                saved["all_original_chords"]==table[i]["chords"],"complete original contacts changed")
        for key in ["live_state_count","live_column_count","target_states_alive"]:
            require(saved[key]==case[key],"remaining support mismatch")
    return [0,1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build",action="store_true")
    parser.add_argument("--controls",action="store_true")
    args=parser.parse_args()
    actual=compute()
    path=HERE/"independent-results.json.gz"
    if args.build:
        with path.open("xb") as out:
            out.write(gzip.compress(json.dumps(actual,sort_keys=True,separators=(",",":")).encode(),mtime=0))
    expected=json.loads(gzip.decompress(path.read_bytes()))
    verify(expected,actual)
    remaining=verify_residual(actual)
    summary={"result":"PASS","case_count":len(actual["cases"]),"synchronous_rounds":len(actual["synchronous_rounds"]),
             "profiles_remaining":remaining,
             "edge_summaries":[{k:v for k,v in r.items() if k not in ["live_state_ids","live_column_ids"]} for r in actual["cases"] if r["name"].startswith("edge:")]}
    if args.controls:
        summary["controls"]=controls(actual)
    print(json.dumps(summary,sort_keys=True))

if __name__=="__main__":
    main()
