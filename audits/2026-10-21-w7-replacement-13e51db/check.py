#!/usr/bin/env python3
"""Named local delete-and-triangulate caps; no source enumeration."""
from pathlib import Path
from itertools import product, combinations
from functools import lru_cache
import argparse, gzip, hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
UP = ROOT / 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting'
RIM = ('a','n','u4','u3','u2','u1','L','q','c','s','v','w','t')

def canon(t):
    d = {}
    return tuple(d.setdefault(x,len(d)) for x in t)

ROWS = sorted({canon(t) for t in product(range(4),repeat=5)
               if all(t[i] != t[(i+1)%5] for i in range(5))})

def edge(a,b): return tuple(sorted((a,b)))

def triangulations(poly):
    if len(poly) <= 3: return [set()]
    out = []
    for k in range(1,len(poly)-1):
        sides = set()
        if k > 1: sides.add(edge(poly[0],poly[k]))
        if k < len(poly)-2: sides.add(edge(poly[k],poly[-1]))
        for a in triangulations(poly[:k+1]):
            for b in triangulations(poly[k:]): out.append(a | b | sides)
    return out

FACES = ('a b p','b p q','p q h','p h n','p n a','h q L',
         'h L R','h R n','R n u4','R u4 u3','R u3 u2','R u2 u1','R u1 L')
EDGES = {edge(a,b) for f in FACES for a,b in combinations(f.split(),2)}
LINKS = {'p':('a','b','q','h','n'),
         'h':('p','q','L','R','n'),
         'R':('n','h','L','u1','u2','u3','u4')}

@lru_cache(None)
def right(a,c,s,v,w,t,b):
    ans = 0
    for x,y,r in product(range(4),repeat=3):
        if r not in (s,v,w,t,x,y) and x not in (c,s,y) and y not in (a,t):
            ans |= 1 << ROWS.index(canon((x,y,a,b,c)))
    return ans

def cap_function(edges, interior):
    names = ('a','n','u4','u3','u2','u1','L','q','c','b') + tuple(interior)
    ix = {v:i for i,v in enumerate(names)}
    indexed = [(ix[a],ix[b]) for a,b in edges | {edge('b','c')}]
    @lru_cache(None)
    def cap(boundary):
        mask = 0
        for b in range(4):
            for extra in product(range(4),repeat=len(interior)):
                t = boundary + (b,) + extra
                if all(t[i] != t[j] for i,j in indexed):
                    mask |= 1 << b
                    break
        return mask
    return cap

def run():
    custody = json.loads((HERE / 'BASE.json').read_text())
    for record in custody['inputs']:
        raw = (ROOT / record['path']).read_bytes()
        if len(raw) != record['bytes'] or hashlib.sha256(raw).hexdigest() != record['sha256']:
            raise ValueError('input custody mismatch: ' + record['path'])
    data = json.load(gzip.open(UP / 'caps.json.gz'))
    closure = json.load(gzip.open(ROOT / 'audits/2026-10-21-w7-transport-synthesis-d23f94f/independent-results.json.gz'))
    live = {p: next(c['live_state_ids'] for c in closure['cases'] if c['name'] == f'profile:{p}')
            for p in (0,1)}
    states = data['states']
    originals = [sum((bool(data['matrices']['G'][j][i]) << j) for j in range(10))
                 for i in range(len(states))]
    original_cap = cap_function(EDGES, ('p','h','R'))
    for i in live[0]:
        a,n,u4,u3,u2,u1,L,q,c,s,v,w,t = states[i]
        bm = original_cap(tuple(states[i][:9])); mask = 0
        for b in range(4):
            if bm >> b & 1: mask |= right(a,c,s,v,w,t,b)
        if mask != originals[i]: raise ValueError('original G full-cap support mismatch')
    allowed = 941
    output = []
    for removed,poly in LINKS.items():
        for j,chords in enumerate(triangulations(poly)):
            edges = {e for e in EDGES if removed not in e} | chords
            cap = cap_function(edges, [v for v in ('p','h','R') if v != removed])
            evidence = {'removed':removed,'triangulation':j,'added_chords':sorted(chords),
                        'profiles':[]}
            for profile in (0,1):
                counters = {'live_tested':0,'new_forbidden':0,'lost_original':0,'different':0}
                first = {}
                for i in live[profile]:
                    state = states[i]
                    a,n,u4,u3,u2,u1,L,q,c,s,v,w,t = state
                    bm = cap(tuple(state[:9])); new = 0
                    for b in range(4):
                        if bm >> b & 1: new |= right(a,c,s,v,w,t,b)
                    old = originals[i]
                    counters['live_tested'] += 1
                    flags = {'new_forbidden':bool(new & ~allowed),
                             'lost_original':bool(old & ~new),'different':old != new}
                    for k,flag in flags.items():
                        if flag:
                            counters[k] += 1
                            first.setdefault(k, {'state':i,'tuple':state,'original_rows':old,'new_rows':new})
                evidence['profiles'].append({'profile':profile,**counters,'first':first})
            output.append(evidence)
    rim = tuple(range(7))
    cycle = {edge(i,(i+1)%7) for i in rim}
    proper = sorted({canon(t) for t in product(range(4),repeat=7)
                     if all(t[i] != t[(i+1)%7] for i in rim)})
    wheel = [t for t in proper if len(set(t)) == 3]
    tri = triangulations(rim)
    if len(tri) != 42 or len({tuple(sorted(es)) for es in tri}) != 42:
        raise ValueError('C7 triangulation generation incomplete or duplicate')
    controls = []
    for j,es in enumerate(tri):
        full = cycle | es
        witness = next(t for t in proper if len(set(t)) == 4 and all(t[a]!=t[b] for a,b in full))
        controls.append({'triangulation':j,'chords':sorted(es),'four_colour_witness':witness})
    if len(proper)!=91 or len(wheel)!=21 or len(output)!=52:
        raise ValueError('finite scope mismatch')
    return {'base':custody['base'],'method':'same ordered C13 state and complete original C5 cap support',
            'input_profile_live_counts':{str(p):len(live[p]) for p in live},
            'original_cap_support_rechecked':len(live[0]),
            'wheel':{'proper_C7_states':len(proper),'W7_extendible_states':len(wheel),
                     'zero_interior_triangulation_controls':controls},
            'candidates':output,'source_exclusion':False,'source_realization':False,
            'necessary_state_leakage_is_actual_source_leakage':False,
            'general_W7':'OPEN','new_Lean':False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args = parser.parse_args()
    result = json.loads(json.dumps(run()))
    if args.build: args.certificate.write_text(json.dumps(result,indent=2)+'\n')
    elif result != json.loads(args.certificate.read_text()):
        raise ValueError('certificate does not match complete replay')
    print(json.dumps({'status':'bounded replacement obstructions only; source OPEN',
                      'candidates':len(result['candidates']),
                      'profile_live_counts':result['input_profile_live_counts'],
                      'all_candidates_have_necessary_leakage':all(p['new_forbidden']>0 for c in result['candidates'] for p in c['profiles'])},sort_keys=True))
