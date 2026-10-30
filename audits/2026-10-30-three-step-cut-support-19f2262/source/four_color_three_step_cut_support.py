#!/usr/bin/env python3
"""Positive finite cut-support relaxation; these relations are not source graphs.

The two complete S4 support relations are D-fixed on the actual side cycles.
Their exact natural join over all five ordered separator coordinates projects
to D16. This certificate demonstrates a stop point, not D16 realizability.
SAT was used only to discover the stored supports; replay needs no SAT solver.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import subprocess

import ck_kempe_obstruction as old

ROOT = Path(__file__).resolve().parents[1]
BOUNDARIES = ((2,6,7,8,4,5,0,1), (2,3,4,8,7,6))
SEPARATOR = (2,6,7,8,4)
SUPPORTS = (
    (10,13,14,15,16,30,36,37,43,44,47,49,51,52,53,54,56,57,58,63,65,67,
     69,74,81,82,84,88,89,90,91,92,93,94,96,97,98,103,105,107,109,112,
     114,115,116,117,119,124,126,127,131,133,138,140,141,142,143,144,145,
     148,149,150,151,157,158,164,165,168,170,172,173,175,176,177,178,180,
     185,187,188,192,194,199,201,202,203,204,205,206,207,208,209,210,211,
     212,213,215,216,217,218,221,223,224,225,226,230,231,232,233,235,236,
     237,238,240,241,242,243,245,246,247,249,250,251,252,253,254,255,259,
     260,261,262,263,265,266,268,270,271,272,273),
    (0,1,2,4,5,7,11,13,17,18,20),
)
D16 = tuple(tuple(map(int,s)) for s in (
    '010201','010212','010213','010231','012012','012021','012102','012121',
    '012123','012132','012301','012302','012312','012313','012321','012323'))


def canonical_json(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def make_certificate():
    patterns = [old.patterns(len(b)) for b in BOUNDARIES]
    sides = []
    for b,ps,support in zip(BOUNDARIES,patterns,SUPPORTS):
        mask = sum(1<<i for i in support)
        witnesses = []
        for i in support:
            for s in range(3):
                orbit,blocks = next((orbit,blocks) for orbit,blocks
                    in old.partition_options(len(b),i,s) if mask & orbit == orbit)
                witnesses.append(dict(pattern_index=i,split=s,blocks=blocks,
                                      orbit_indices=old._indices(orbit)))
        sides.append(dict(boundary_order=b,pattern_order=ps,support_indices=support,
                          support_patterns=[ps[i] for i in support],
                          complete_orbit_witnesses=witnesses))
    indices = [{p:i for i,p in enumerate(ps)} for ps in patterns]
    edges = {tuple(sorted((a,b))) for boundary in BOUNDARIES
             for a,b in zip(boundary,boundary[1:]+boundary[:1])}
    compatible = set()
    forbidden = set()
    joins = []
    separator_words = set()
    selected_pairs = set()
    outer = set()
    for f in product(range(4),repeat=9):
        if any(f[a]==f[b] for a,b in edges):
            continue
        pair = tuple(indices[s][old.normalize(tuple(f[v] for v in b))]
                     for s,b in enumerate(BOUNDARIES))
        compatible.add(pair)
        r = old.normalize(f[:6])
        if r not in D16:
            forbidden.add(pair)
        if all(pair[s] in SUPPORTS[s] for s in range(2)):
            assert r in D16
            joins.append(f)
            selected_pairs.add(pair)
            separator_words.add(tuple(f[v] for v in SEPARATOR))
            outer.add(r)
    assert outer==set(D16)
    seed = (0,1,2,1,2,1,3,2,3)
    assert seed in joins
    assert (len(joins),len(separator_words),len(selected_pairs))==(1824,180,75)
    # Every possible separator word is represented, including all empty fibres.
    fibres = []
    for ell in product(range(4),repeat=5):
        fibres.append(dict(separator_word=ell,
                           joint_rows=[f for f in joins if tuple(f[v] for v in SEPARATOR)==ell]))
    return dict(schema='three-step-cut-support-v1',
        scope='support-only relaxation; no common side graphs or hidden source lifts',
        outer_order=(0,1,2,3,4,5),outer_names=('z','a','b','w','c','d'),
        separator_order=SEPARATOR,seed_union_row=seed,d16_patterns=D16,sides=sides,
        full_domain_compatible_pairs=sorted(compatible),
        full_domain_forbidden_pairs=sorted(forbidden),
        join_rows=joins,complete_separator_fibres=fibres,
        outer_projection_patterns=sorted(outer),
        counts=dict(side_patterns=[len(p) for p in patterns],
            selected_side_patterns=list(map(len,SUPPORTS)),
            compatible_pairs=len(compatible),forbidden_pairs=len(forbidden),
            selected_compatible_pairs=len(selected_pairs),joint_literal_rows=len(joins),
            nonempty_separator_fibres=len(separator_words),
            empty_separator_fibres=4**5-len(separator_words)),
        join_sha256=sha256(canonical_json(joins)).hexdigest())


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',type=Path,required=True)
    args=parser.parse_args()
    args.out_dir.mkdir(parents=True,exist_ok=False)
    result=make_certificate()
    path=args.out_dir/'results.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    tracked=('scripts/four_color_three_step_cut_support.py',
             'scripts/four_color_three_step_cut_support_replay.py',
             'scripts/ck_kempe_obstruction.py')
    manifest=dict(base_sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  inputs={p:sha256((ROOT/p).read_bytes()).hexdigest() for p in tracked},
                  outputs={'results.json':sha256(path.read_bytes()).hexdigest()})
    (args.out_dir/'verification.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(result['counts'],sort_keys=True))


if __name__=='__main__':
    main()
