#!/usr/bin/env python3
"""N2 bridge: frozen-input, literal arithmetic, independent MRV full-lift replay.

No producer, historical colouring code or independent_checker is imported.
This checks finite interfaces and controls, not arbitrary-size paper proofs.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROWS = ((0,1,0,1,2),(0,1,0,2,1),(0,1,0,2,3),(0,1,2,0,1),
        (0,1,2,0,2),(0,1,2,0,3),(0,1,2,1,2),(0,1,2,1,3),
        (0,1,2,3,1),(0,1,2,3,2))
Q = {0:6, 1:4, 2:3, 3:1, 4:0}
FRAME = {tuple(sorted((i,(i+1)%5))) for i in range(5)}


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode()


def arithmetic():
    masks = [m for m in range(1024) if m & 932 == 932
             and all(not (m >> Q[q] & 1) for q in (0,1,3))]
    assert masks == [932,933,940,941]
    spectrum = [{'mask':m, 'Q':[q for q,j in Q.items() if not m>>j&1],
                 'q2_accepted':bool(m>>Q[2]&1), 'q4_accepted':bool(m&1)} for m in masks]
    pairs = []
    for a,b in combinations(range(5),2):
        eq = [q for q,j in Q.items() if ROWS[j][a] == ROWS[j][b]]
        assert len(eq) == (0 if (a,b) in FRAME else 2)
        pairs.append({'pair':[a,b], 'equal_rows':eq})
    four = []
    for omitted in range(5):
        keep = [q for q in range(5) if q != omitted]
        vs = [[ROWS[Q[q]][v] for q in keep] for v in range(5)]
        es = [[sorted([ROWS[Q[q]][a],ROWS[Q[q]][b]]) for q in keep]
              for a,b in sorted(FRAME)]
        assert len({tuple(v) for v in vs}) == 5
        assert len({tuple(tuple(t) for t in e) for e in es}) == 5
        four.append({'omitted':omitted, 'rows':keep, 'vertex_signatures':vs,
                     'edge_signatures':es})
    diffs = []
    for a in range(5):
        arc = [a,(a+1)%5,(a+2)%5]
        hits = [q for q in (0,1,3) if len({ROWS[Q[q]][b] for b in arc})==3]
        assert hits
        diffs.append({'arc':arc, 'selected_diff_rows':hits})
    # Complete finite colour-set interface of the UC3 capacity argument.
    # All forbidden sets for each one-incidence mixed have size <=1.
    small = [set()] + [{c} for c in range(4)]
    schedules = tight = 0
    for bits in range(16):
        fu = {c for c in range(4) if bits>>c&1}
        for p,q in product(small, repeat=2):
            schedules += 1
            if set(range(4))-fu <= p|q:
                assert len(fu)>=2
                tight += len(fu)==2
    # One common boundary reflection, followed by S4 normalization of words.
    def normal(word):
        names={}; out=[]
        for x in word:
            if x not in names:names[x]=len(names)
            out.append(names[x])
        return tuple(out)
    perm = [ROWS.index(normal([row[(1-i)%5] for i in range(5)])) for row in ROWS]
    image = sum(1<<perm[j] for j in range(10) if 940>>j&1)
    assert image==933
    return {'spectrum':spectrum, 'nonadjacent_pair_collisions':pairs,
            'any_four_signatures':four, 'diff_rows':diffs,
            'uc3_set_schedules':schedules, 'uc3_tight_schedules':tight,
            'whole_boundary_reflection_row_permutation':perm,
            'reflected_940':image, 'source_realization_claim':False}


def all_lifts(vertices, edges, row):
    """Adaptive minimum-remaining-colours search, independent of numeric DFS."""
    adj={v:set() for v in vertices}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    colour=dict(enumerate(row)); result=[]
    assert all(colour[a]!=colour[b] for a,b in edges if a<5 and b<5)
    def visit(todo):
        if not todo:
            result.append(tuple(colour[v] for v in vertices));return
        available={v:set(range(4))-{colour[w] for w in adj[v] if w in colour}
                   for v in todo}
        v=min(todo,key=lambda x:(len(available[x]),-len(adj[x]),x))
        for c in sorted(available[v]):
            colour[v]=c;visit(todo-{v})
        colour.pop(v,None)
    visit(set(vertices)-set(range(5)))
    return sorted(result)


def check_controls(data):
    assert data['row_order']==[list(r) for r in ROWS]
    assert data['source_exclusion_evidence'] is False
    cells=empty=lifts_count=queries=0
    for g in data['graphs']:
        assert g['ordered_B']==list(range(5))
        vertices=g['vertices']; edges=g['edges']; roots=g['roots']
        assert len(edges)==len({tuple(e) for e in edges})
        assert {tuple(e) for e in edges if e[1]<5}==FRAME
        cache={}
        def check_relation(es,record):
            nonlocal cells,empty,lifts_count,queries
            key=tuple(sorted(tuple(e) for e in es)); observed_mask=0
            for j,row in enumerate(ROWS):
                ck=(key,j)
                if ck not in cache:cache[ck]=all_lifts(vertices,es,row);queries+=1
                lifts=cache[ck]
                rr=record['rows'][j]
                assert rr['index']==j and rr['boundary']==list(row)
                assert rr['accepted']==bool(lifts) and rr['lift_count']==len(lifts)
                if lifts:observed_mask |= 1<<j
                fibres=rr['fibres']
                assert len(fibres)==16
                nonempty=[]
                for cell,(a,b) in zip(fibres,product(range(4),repeat=2)):
                    assert cell['root_colors']==[a,b]
                    expected=[f for f in lifts if f[roots[0]]==a and f[roots[1]]==b]
                    assert sorted(tuple(f) for f in cell['lifts'])==expected
                    if expected:nonempty.append([a,b])
                    cells+=1;empty+=not expected;lifts_count+=len(expected)
                assert rr['root_relation']==nonempty
            assert record['sigma_mask']==observed_mask
            assert record['Q']==[q for q,j in Q.items() if not observed_mask>>j&1]
        a=g['analysis'];check_relation(edges,a['original'])
        for d in a['deletions']:
            check_relation([e for e in edges if e!=d['edge']],d['result'])
        for c in a['minimal_cores']:
            check_relation(c['edges'],c['result'])
            for d in c['minimality_deletions']:
                check_relation([e for e in c['edges'] if e!=d['edge']],d['result'])
    return {'graphs':len(data['graphs']), 'distinct_row_queries':queries,
            'queried_fibre_cells':cells, 'empty_fibre_cells':empty,
            'full_lifts_with_query_multiplicity':lifts_count,
            'full_N2_source_status':'not triggered'}


def inputs():
    records=[]
    for name in ('BASE.json','SUPPLEMENTAL_INPUTS.json','U4_INPUTS.json'):
        doc=json.loads((HERE/name).read_text())
        assert doc['base']=='243a125a80e4d8de40957f59d8da0bdbc974cf69'
        for rec in doc['inputs']:
            digest=sha256((HERE/'frozen'/rec['path']).read_bytes()).hexdigest()
            assert digest==rec['sha256'], rec['path']
            records.append((rec['path'],digest))
    return {'unique_frozen_inputs':len(dict(records)), 'input_drift':0}


def build():
    control=json.loads((HERE/'controls/graphs.json').read_text())
    return {'schema':'n2-bridge-primary-v1', 'inputs':inputs(),
            'arithmetic':arithmetic(), 'full_control_replay':check_controls(control),
            'controls_sha256':sha256((HERE/'controls/graphs.json').read_bytes()).hexdigest(),
            'paper_theorem_proved_by_this_checker':False}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true')
    ap.add_argument('--negative-tests',action='store_true')
    ap.add_argument('--artifact',type=Path,default=HERE/'observations.json')
    args=ap.parse_args();out=build()
    if args.check:
        assert args.artifact.read_bytes()==encoded(out), 'artifact mismatch'
    else:
        with args.artifact.open('xb') as f:f.write(encoded(out))
    negatives=[]
    if args.negative_tests:
        source=json.loads((HERE/'controls/graphs.json').read_text())
        bad=deepcopy(source)
        for row in bad['graphs'][0]['analysis']['original']['rows']:
            cell=next((f for f in row['fibres'] if f['lifts']),None)
            if cell:
                cell['lifts'].pop();break
        try:check_controls(bad)
        except AssertionError:negatives.append('missing_full_lift rejected')
        else:raise AssertionError('missing lift accepted')
        bad=deepcopy(out);bad['arithmetic']['spectrum'][0]['q2_accepted']=True
        assert encoded(bad)!=encoded(out);negatives.append('invented_q2_acceptance rejected')
    print(json.dumps({'status':'PASS',**out['inputs'],**out['full_control_replay'],
                      'negative_tests':negatives,'arithmetic':'PASS'},sort_keys=True))


if __name__=='__main__':main()
