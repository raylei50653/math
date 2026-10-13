#!/usr/bin/env python3
"""Independent named-edge construction and direct P colouring support audit.

Does not import the primary assembler, terminal kernel or transfer functions.
The only compared input is the primary result table after independent search.
"""
from itertools import product
from pathlib import Path
from collections import Counter
import json
import time
import copy
import gzip

ROOT = Path(__file__).resolve().parents[1]
BROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
QUERIES = (
    ('c15-933',(0,1,2,0,0),933),('c18-933',(0,2,1,0,0),933),
    ('c04-941',(0,0,1,0,2),941),('c07-941',(0,0,2,0,1),941),
    ('c15-941',(0,1,2,0,0),941),('c18-941',(0,2,1,0,0),941),
    ('c20-941',(1,0,0,0,2),941),('c30-941',(2,0,0,0,1),941))

def canonical(word):
    d = {}
    return ''.join(str(d.setdefault(c,len(d))) for c in word)

ROWS = sorted({canonical(w) for w in product(range(4),repeat=6)
               if all(w[i] != w[(i+1)%6] for i in range(6))})

def construct(kind,pair,side,slot,collar):
    # Construct edges from the independently stated original contact lists.
    edges = set()
    def edge(a,b):
        assert a != b
        edges.add(tuple(sorted((a,b))))
    def cycle(vs):
        for a,b in zip(vs,vs[1:]+vs[:1]): edge(a,b)
    B = ['b'+str(i) for i in range(5)]
    C = ['c'+str(i) for i in range(8)]
    T = ['t'+str(i) for i in range(8)]
    cycle(B); cycle(C)
    original = ['a0']
    for i in range(1,5):
        original += ['y%d_%d'%(i,j) for j in range(1,collar[i]+1)] + ['a'+str(i)]
    original += ['y0_'+str(j) for j in range(1,collar[0]+1)]
    assert len(original) == 8
    image = dict(zip(original,C))
    for i in range(5):
        edge(B[i],image['a'+str(i)])
        edge(B[(i+1)%5],image['a'+str(i)])
        for j in range(1,collar[i]+1): edge(B[i],image['y%d_%d'%(i,j)])
    for i in range(8):
        edge(T[i],C[i]); edge(T[i],C[(i+1)%8])
    endpoints = ['x'] if kind == 'PINCH' else ['x','y']
    for ep in endpoints:
        edge(ep,C[pair]); edge(ep,C[(pair+4)%8])
    if kind == 'BRIDGE': edge('x','y')
    D = None
    for s in range(2):
        start = (pair+4*s)%8
        endpoint = endpoints[s] if kind == 'BRIDGE' else 'x'
        ring = [endpoint] + [T[(start+i)%8] for i in range(4)]
        if s == side:
            ring.insert(slot+1,'w')
            edge('w',C[(start+slot)%8])
            D = ring
        else:
            for t in ring: edge('zF',t)
        cycle(ring)
    vertices = B+C+T+endpoints+['w','zF']
    assert len(vertices) == (24 if kind == 'PINCH' else 25)
    return vertices, sorted(edges), D

def colour_support(vertices,edges,D,beta):
    index = {v:i for i,v in enumerate(vertices)}
    adj = [[] for v in vertices]
    for a,b in edges:
        a,b = index[a],index[b]
        adj[a].append(b); adj[b].append(a)
    degrees = [len(a) for a in adj]
    colors = [-1]*len(vertices)
    domains = [15]*len(vertices)
    for i,c in enumerate(map(int,beta)):
        colors[i] = c; domains[i] = 0
    for v in range(5):
        for u in adj[v]:
            if colors[u] >= 0:
                assert colors[u] != colors[v]
            else: domains[u] &= ~(1<<colors[v])
    free = set(range(5,len(vertices)))
    di = [index[d] for d in D]
    supports = set()
    count = 0
    def visit():
        nonlocal count
        if not free:
            count += 1
            supports.add(canonical([colors[i] for i in di]))
            return
        v = min(free,key=lambda x:(domains[x].bit_count(),-degrees[x],x))
        opts = domains[v]
        if not opts: return
        free.remove(v)
        while opts:
            bit = opts & -opts; opts -= bit
            colors[v] = bit.bit_length()-1
            changed = []
            possible = True
            for u in adj[v]:
                if u in free and domains[u]&bit:
                    changed.append((u,domains[u])); domains[u] ^= bit
                    if not domains[u]: possible = False
            if possible: visit()
            for u,old in changed: domains[u] = old
        colors[v] = -1
        free.add(v)
    visit()
    return supports,count

def compare_primary(record,vertices,edges,primary):
    assert record['name'] == primary['name']
    assert record['target'] == primary['target']
    assert record['D'] == primary['graph']['D']
    assert vertices == primary['graph']['vertices']
    assert [list(e) for e in edges] == primary['graph']['edges']
    assert record['masks'] == primary['D_orbit_B_masks']
    assert record['allowed'] == primary['allowed_D_orbits']
    assert record['possible'] == primary['maximal_allowed_B_mask']
    assert record['missing'] == primary['missing_target_mask']
    assert dict(zip(BROWS,record['direct_P_B_lift_counts'])) == primary['row_full_lift_counts']
    missing_index = BROWS.index(primary['chosen_missing_B_row'])
    assert record['missing'] & (1<<missing_index)
    implications = primary['orbit_forbidden_row_witnesses']
    assert set(implications) == {q for q,m in record['masks'].items() if m & (1<<missing_index)}
    for q,row in implications.items():
        b = 1<<BROWS.index(row)
        assert record['masks'][q]&b and not record['target']&b

def negative_controls(record,vertices,edges,primary):
    result = {}
    for label,field in [('corrupt_allowed_union','maximal_allowed_B_mask'),
                        ('corrupt_missing_target','missing_target_mask')]:
        damaged = copy.deepcopy(primary)
        damaged[field] ^= 1
        try: compare_primary(record,vertices,edges,damaged)
        except AssertionError: result[label] = True
        else: raise AssertionError(label+' accepted')
    damaged = copy.deepcopy(primary)
    damaged['D_orbit_B_masks'][ROWS[0]] ^= 1
    try: compare_primary(record,vertices,edges,damaged)
    except AssertionError: result['corrupt_orbit_matrix'] = True
    else: raise AssertionError('corrupt orbit matrix accepted')
    damaged = copy.deepcopy(primary)
    damaged['row_full_lift_counts'][BROWS[0]] -= 1
    try: compare_primary(record,vertices,edges,damaged)
    except AssertionError: result['missing_full_P_lift'] = True
    else: raise AssertionError('missing full P lift accepted')
    # Actual graph mutations: independent complete colouring counts must catch
    # deleting the bridge, and replacing the single PINCH endpoint by two
    # independently coloured copies. These are source P graphs, not just pins.
    collar = QUERIES[0][1]
    bridge_v,bridge_e,bridge_d = construct('BRIDGE',0,0,0,collar)
    loose_e = [e for e in bridge_e if e != ('x','y')]
    assert len(loose_e)+1 == len(bridge_e)
    original_s,original_n = colour_support(bridge_v,bridge_e,bridge_d,BROWS[0])
    loose_s,loose_n = colour_support(bridge_v,loose_e,bridge_d,BROWS[0])
    assert original_s <= loose_s and original_n < loose_n
    result['omitted_original_bridge'] = {'proper_P_lifts':original_n,'invalid_relaxed_lifts':loose_n}
    pinch_v,pinch_e,pinch_d = construct('PINCH',0,0,0,collar)
    pinch_s,pinch_n = colour_support(pinch_v,pinch_e,pinch_d,BROWS[0])
    # Identifying x=y in the loose graph is exactly this original PINCH P;
    # the extra colourings counted above assign different endpoint colours.
    assert pinch_s <= loose_s and pinch_n < loose_n
    result['split_shared_original_endpoint'] = {'proper_P_lifts':pinch_n,'invalid_split_lifts':loose_n}
    return result

def run():
    start = time.monotonic()
    certificate = ROOT/'transfer/certificate.json.gz'
    if certificate.exists():
        with gzip.open(certificate,'rt') as source: raw = json.load(source)
    else:
        # Only for the initial compression transition; the final archive wins.
        raw = json.loads((ROOT/'transfer/certificate.json').read_text())
    assert len(ROWS) == 31
    reference = {r['name']:r for r in raw['exteriors']}
    records = []
    counts = Counter()
    for kind in ('PINCH','BRIDGE'):
      for pair in range(4):
       for side in range(2):
        for slot in range(5):
         cache = {}
         for query,collar,target in QUERIES:
          if collar not in cache:
            vertices,edges,D = construct(kind,pair,side,slot,collar)
            masks = dict.fromkeys(ROWS,0)
            lifts = []
            for bi,beta in enumerate(BROWS):
                support,n = colour_support(vertices,edges,D,beta)
                for q in support: masks[q] |= 1<<bi
                lifts.append(n)
            cache[collar] = (masks,lifts,vertices,edges,D)
          masks,lifts,vertices,edges,D = cache[collar]
          allowed = {q:m for q,m in masks.items() if not m & (1023 ^ target)}
          possible = 0
          for mask in allowed.values(): possible |= mask
          name = f'{kind}-{pair}-{side}-{slot}-{query}'
          assert possible != target and possible & target == possible,name
          record = dict(name=name,D=D,target=target,masks=masks,
                              allowed=allowed,possible=possible,
                              missing=target ^ possible,direct_P_B_lift_counts=lifts)
          compare_primary(record,vertices,edges,reference[name])
          records.append(record)
          counts['independent_queries'] += 1
          counts['source_target_unattainable'] += 1
          counts['direct_P_lifts_with_duplicated_query_collars'] += sum(lifts)
         print(kind,pair,side,slot,'verified',len(records),'seconds',round(time.monotonic()-start,2),flush=True)
    assert len(records) == 640
    output = dict(method='independent named edges and direct full P colour search; no primary assembler or W kernel',
                  B_rows=BROWS,D_rows=ROWS,summary=dict(counts),records=records)
    dest = Path(__file__).with_name('independent_transfer.json')
    text = json.dumps(output,indent=2,sort_keys=True)+'\n'
    if dest.exists(): assert dest.read_text() == text
    else: dest.open('x').write(text)
    first = records[0]
    vertices,edges,D = construct('PINCH',0,0,0,QUERIES[0][1])
    controls = negative_controls(first,vertices,edges,reference[first['name']])
    control_path = Path(__file__).with_name('negative_controls.json')
    control_text = json.dumps(controls,indent=2,sort_keys=True)+'\n'
    if control_path.exists(): assert control_path.read_text() == control_text
    else: control_path.open('x').write(control_text)
    print(json.dumps({'semantic_negative_controls':controls},sort_keys=True),flush=True)
    print(json.dumps(dict(counts),sort_keys=True),flush=True)

if __name__ == '__main__': run()
