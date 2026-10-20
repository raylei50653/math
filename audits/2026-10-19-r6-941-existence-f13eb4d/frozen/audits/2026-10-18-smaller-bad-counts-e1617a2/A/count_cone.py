#!/usr/bin/env python3
"""Counted fixed-split Kempe cone on the frozen C8 interface.

This is a necessary cone, not a graph-realizability criterion.
Use --build to reconstruct all combinatorial columns.
The --check route is stdlib-only and verifies integer equations exactly.
"""
import argparse
from collections import Counter
from fractions import Fraction
from functools import reduce
import hashlib
import itertools
import json
from math import gcd, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT.parent/'frozen/audits/2026-10-18-smaller-bad-e1617a2'
SOURCE = FROZEN/'kempe-consistency.json'
PROJECTIONS = FROZEN/'candidate-projections.json'
DATA = json.loads(SOURCE.read_text())
TUPLES = [tuple(t) for t in DATA['tuples']]
INDEX = {t:i for i,t in enumerate(TUPLES)}
MASKS = DATA['old_lift_masks']
PERMS = [p for p in itertools.permutations(range(4))
         if {p[0]//2,p[1]//2} == {p[0]//2} and {p[2]//2,p[3]//2} == {p[2]//2}]
assert len(PERMS) == 8

def canonical(t):
    d = {}
    return tuple(d.setdefault(c,len(d)) for c in t)

def hc(t):
    return min(tuple(p[c] for c in t) for p in PERMS)

def partitions(prefix=(0,)):
    if len(prefix) == 8:
        yield prefix
    else:
        for a in range(max(prefix)+2):
            yield from partitions(prefix+(a,))


def build():
    literal = [t for t in itertools.product(range(4),repeat=8)
               if all(t[i] != t[(i+1)%8] for i in range(8))]
    hist = Counter(hc(t) for t in literal)
    rows = sorted(hist)
    row_index = {t:i for i,t in enumerate(rows)}
    four = list(itertools.combinations(range(8),4))
    nc = [p for p in partitions() if not any(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b]
                                             for a,b,c,d in four)]
    assert len(literal)==6564 and len(nc)==1430
    columns = {}
    for t in rows:
        side = tuple(c//2 for c in t)
        for p in nc:
            blocks = [tuple(i for i,v in enumerate(p) if v==b) for b in range(max(p)+1)]
            if any(len({side[i] for i in block})!=1 for block in blocks):
                continue
            if any(side[i]==side[(i+1)%8] and p[i]!=p[(i+1)%8] for i in range(8)):
                continue
            transitions = sum(side[i] != side[(i+1)%8] for i in range(8))
            if len(blocks) != transitions//2 + 1:
                continue
            orbit = [tuple(c^1 if chosen & (1<<p[i]) else c for i,c in enumerate(t))
                     for chosen in range(1<<len(blocks))]
            assert len(set(orbit)) == len(orbit)
            col = tuple(sorted(Counter(row_index[hc(x)] for x in orbit).items()))
            columns.setdefault(col,{'start':list(t),'partition':list(p)})
    cols = []
    for col in sorted(columns):
        cols.append({'entries':[list(e) for e in col],**columns[col]})
    result = {'scope':'necessary triangulated disk C8 counted Kempe cone; not source realization',
              'triangulated_maximal_partitions':True,
              'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'literal_split':[[0,1],[2,3]],'palette_stabilizer':[list(p) for p in PERMS],
              'literal_tuple_count':len(literal),'noncrossing_partition_count':len(nc),
              'rows':[{'tuple':list(t),'tuple_id':INDEX[canonical(t)],'orbit_size':hist[t]} for t in rows],
              'columns':cols}
    return result



def check(cone,cert):
    assert cert['cone_sha256']==hashlib.sha256((ROOT/'cone-triangulated.json').read_bytes()).hexdigest()
    assert cone==build(), 'full combinatorial cone differs from reconstruction'
    projections=json.loads(PROJECTIONS.read_text())['complete_local_records']
    catalogue=json.loads((ROOT.parent/'frozen/artifacts/c5_cells/cells.json').read_text())
    K={int(mask) for mask in catalogue['cells']}
    assert len(cert['results'])==len(DATA['results'])==3
    for rec,prior in zip(cert['results'],DATA['results']):
        assert rec['source_mask']==prior['source_mask']
        assert rec['boolean_live_ids']==prior['surviving_ids']
        live=set(rec['boolean_live_ids'])
        allowed=[j for j,col in enumerate(cone['columns'])
                 if all(cone['rows'][r]['tuple_id'] in live for r,v in col['entries'])]
        assert rec['allowed_columns']==allowed
        counts=rec['counts']
        assert len(counts)==274 and all(isinstance(v,int) and v>=0 for v in counts)
        support={i for i,v in enumerate(counts) if v}
        assert support==set(rec['maximal_support'])
        assert live-support==set(rec['forced_zero_ids'])
        residual=[-row['orbit_size']*counts[row['tuple_id']] for row in cone['rows']]
        for j,w in rec['positive_orbit_weights']:
            assert isinstance(w,int) and w>0 and j in allowed
            for r,v in cone['columns'][j]['entries']:
                residual[r]+=w*v
        assert not any(residual), 'integer cone equation failed'
        orig=0
        candidates=dict.fromkeys(('GA','GB','H','S','Q1','Q2'),0)
        for i in support:
            orig|=MASKS[i]
            for name,v in projections[i]['local_candidate_masks'].items():candidates[name]|=v
        assert orig==rec['source_mask']==rec['original_projection']
        assert candidates==rec['candidate_masks']
        assert all(mask in K for mask in candidates.values())
        if rec['forced_zero_ids']:
            dual=rec['forced_zero_dual']; y=dual['row_values']; scale=dual['scale']
            assert len(y)==len(cone['rows']) and scale>0
            assert all(isinstance(v,int) for v in y)
            coefficients=[0]*274
            for row,v in zip(cone['rows'],y):coefficients[row['tuple_id']]-=row['orbit_size']*v
            for i in live:
                assert coefficients[i]>=scale*int(i in rec['forced_zero_ids'])
            for j in allowed:
                assert sum(y[r]*v for r,v in cone['columns'][j]['entries'])>=0
        else:
            assert support==live
    return {'exact_integer_count_equations':True,'exact_dual_for_forced_zeros':True,
            'full_cone_rebuilt':True,'results':[
        {'source_mask':rec['source_mask'],'support_size':len(rec['maximal_support']),
         'max_count':max(rec['counts']),'weight_support':len(rec['positive_orbit_weights']),
         'forced_zero_ids':rec['forced_zero_ids'],'candidate_masks':rec['candidate_masks']}
         for rec in cert['results']]}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.build:
        result=build()
        with (ROOT/'cone-triangulated.json').open('x') as f:
            f.write(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'rows':len(result['rows']),'columns':len(result['columns'])}))
    if args.check:
        print(json.dumps(check(json.loads((ROOT/'cone-triangulated.json').read_text()),
                               json.loads((ROOT/'triangulated-witnesses.json').read_text()))))
