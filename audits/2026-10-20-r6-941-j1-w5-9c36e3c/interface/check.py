#!/usr/bin/env python3
"""Exact expanded W5 interface and necessary Kempe closure; not realizability."""
from pathlib import Path
from itertools import product
import argparse
import gzip
import hashlib
import importlib.util
import json

D = Path(__file__).resolve().parent
A = D.parent
F = A / 'frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/frozen'
P = F / 'audits/2026-10-19-r6-941-chains-13dc5ff/A/interface.py'
spec = importlib.util.spec_from_file_location('frozen_interface', P)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
m = old.m
NAMES = ('a','n','u2','u1','L','q','c','s','v','w','t')


def packed(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()


def compute():
    for row in json.loads((A/'INPUTS.json').read_text()):
        raw = (A/'frozen'/row['path']).read_bytes()
        assert len(raw) == row['bytes']
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
    states = [t for t in m.growth(11, four=True) if m.proper(t)]
    index = {t:i for i,t in enumerate(states)}
    matrices = {name:[[0]*len(states) for _ in m.ROWS] for name in ('G','Q1','J1')}
    caps = []
    for i, state in enumerate(states):
        a,n,u2,u1,L,q,c,s,v,w,t = state
        right = [(x,y,r) for x,y,r in product(range(4), repeat=3)
                 if r not in (s,v,w,t,x,y) and x not in (c,s,y) and y not in (a,t)]
        left = [(b,p,h,R) for b,p,h,R in product(range(4),repeat=4)
                if b not in (a,c,q,p) and p not in (a,q,n,h)
                and h not in (q,L,R,n) and R not in (n,u2,u1,L)]
        quot = [(b,R) for b,R in product(range(4),repeat=2)
                if b not in (a,c,q) and b == n and R == q
                and R not in (n,u2,u1,L)]
        ji = [(b,R) for b,R in product(range(4),repeat=2)
              if b not in (a,c,q) and b == L and a != R
              and R not in (n,u2,u1,L)]
        lifts = {'G':left,'Q1':quot,'J1':ji}
        for name, ls in lifts.items():
            for lift in ls:
                b = lift[0]
                for x,y,r in right:
                    row = m.ROWS.index(''.join(map(str,m.canonical((x,y,a,b,c)))))
                    matrices[name][row][i] += 1
        caps.append({'core':state,'original_left_bphR':left,'Q1_left_bR':quot,
                     'J1_left_bR':ji,'right_xyr':right})
        oldcap, _ = old.cap(state, 'R')
        assert all(oldcap[g] == [matrices[g][j][i] for j in range(10)] for g in ('G','Q1'))
    K = old.kempe(11, states)
    zero = {i for i in range(len(states))
            if any(matrices['G'][j][i] for j in (1,4,6)) or matrices['Q1'][9][i]
            or any(matrices['J1'][j][i] for j in (4,6))}
    cap_zero = sorted(zero)
    parent = json.loads((F.parent/'J1/certificate.json').read_text())
    parent_live = set(parent['final_live'])
    ten = [t for t in m.growth(10,four=True) if m.proper(t)]
    ten_index = {t:i for i,t in enumerate(ten)}
    inherited = []
    for i,tup in enumerate(states):
        a,n,u2,u1,L,q,c,s,v,w,t = tup
        bad_R = [R for R in range(4) if R not in (n,u2,u1,L)
                 and ten_index[m.canonical((a,n,R,L,q,c,s,v,w,t))] not in parent_live]
        if bad_R:
            zero.add(i)
            inherited.append({'core_id':i,'zero_R_lifts':bad_R})
    live, rounds = m.close(K, set(range(len(states))) - zero)
    witnesses = []
    for e0,e1 in ((0,1),(1,0)):
        literal = (0,1,2,1,2,3,1,2,e0,e1,2)
        i = index[m.canonical(literal)]
        witnesses.append({'literal':literal,'canonical_id':i,'survives':i in live,
                          'original_R':3,'original_u2_u1':[2,1]})
    # Each present chord is an actual original edge. Nonedges are not turned
    # into constraints on colour equality. These conditional runs do not assert
    # that any of the profiles is a realizable source.
    chords = (('a','u2'),('s','u2'),('v','u2'),('v','u1'),('w','u1'))
    positions = [tuple(sorted((NAMES.index(u),NAMES.index(v)))) for u,v in chords]
    profiles = []
    for mask in range(1<<len(chords)):
        chosen = [e for j,e in enumerate(positions) if mask & (1<<j)]
        if any(a<c<b<d or c<a<d<b for (a,b),(c,d) in __import__('itertools').combinations(chosen,2)):
            continue
        allowed = {i for i,t in enumerate(states) if i not in zero and all(t[u]!=t[v] for u,v in chosen)}
        plive, prounds = m.close(K,allowed)
        profiles.append({'present_chords':[chords[j] for j in range(5) if mask & (1<<j)],
                         'live_states':len(plive),'deletions_by_round':[len(r) for r in prounds],
                         'live_ids':plive,'deletion_rounds':prounds,
                         'witnesses_survive':[w['canonical_id'] in plive for w in witnesses],
                         'original_positive_rows_survive':[any(matrices['G'][j][i] for i in plive) for j in (0,2,3,5,7,8,9)]})
    excluded_chords = [p['present_chords'][0] for p in profiles
                       if len(p['present_chords']) == 1 and not p['original_positive_rows_survive'][-1]]
    assert excluded_chords == list(chords[1:])
    return {'status':'necessary expanded interface; source not realized',
            'ordered_rim':NAMES,'states':len(states),'caps':caps,
            'matrices_sha256':hashlib.sha256(packed(matrices)).hexdigest(),
            'kempe':{'columns':len(K['columns']),'half_rows':len(K['hrows']),
                     'noncrossing_partitions':K['noncrossing_count'],
                     'columns_sha256':hashlib.sha256(packed(K['columns'])).hexdigest()},
            'initial_zero':sorted(zero),'live':live,'deletion_rounds':rounds,
            'cap_zero':cap_zero,'inherited_C10_zero_lifts':inherited,
            'witnesses':witnesses,
            'conditional_chord_profiles':profiles,
            'source_theorems':{'excluded_original_chords':excluded_chords,
                               'n_ge_6_expanded_C11_induced':True,
                               'n_eq_5_delete_n_induced_C10':True},
            'source_positive_rows_survive':[any(matrices['G'][j][i] for i in live) for j in (0,2,3,5,7,8,9)],
            'source_excluded':False,'smaller_bad_constructed':False,'new_Lean':False}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--certificate',type=Path,default=D/'certificate-v4.json.gz')
    args = ap.parse_args()
    data = json.loads(packed(compute()))
    if args.build:
        with args.certificate.open('xb') as raw:
            with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as out:
                out.write(packed(data)+b'\n')
    else:
        with gzip.open(args.certificate,'rt') as src:
            assert json.load(src) == data
    print(json.dumps({k:data[k] for k in ('status','states','kempe','witnesses','source_positive_rows_survive','source_theorems','source_excluded')}|{'live_states':len(data['live'])},sort_keys=True))


if __name__ == '__main__':
    main()
