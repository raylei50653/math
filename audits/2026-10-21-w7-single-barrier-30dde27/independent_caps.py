#!/usr/bin/env python3
"""Independent full-cap reconstruction for same-exterior strip recolouring.

No child checker implementation is imported.  Raw cap assignments are checked
against the original stars and compared to the frozen original matrices.
"""
import argparse
from copy import deepcopy
from functools import lru_cache
import gzip
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREFIX = 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/'
P = ['n', 'u4', 'u3', 'u2', 'u1', 'L']
RIM = ['a', *P, 'q', 'c', 's', 'v', 'w', 't']
ORIGINAL_P = (1, 2, 1, 2, 1, 2)
ROWS = ['01012','01021','01023','01201','01202',
        '01203','01212','01213','01231','01232']
ZERO = {'G': {'01021','01202','01212'}, 'Q1': {'01232'}, 'J1': {'01202','01212'}}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(row):
    palette = {}
    return tuple(palette.setdefault(c, len(palette)) for c in row)


def read_inputs():
    manifest = json.loads((HERE/'BASE.json').read_text())
    for entry in manifest['inputs']:
        raw = (HERE/'frozen'/entry['path']).read_bytes()
        require(len(raw) == entry['bytes'] and sha256(raw).hexdigest() == entry['sha256'], 'frozen drift')
        require(raw == (ROOT/entry['path']).read_bytes(), 'live authority drift')
    caps = json.loads(gzip.decompress((HERE/'frozen'/PREFIX/'caps.json.gz').read_bytes()))
    require(caps['ordered_rim'] == RIM, 'literal rim changed')
    return caps


@lru_cache(None)
def direct_caps(row):
    a,n,u4,u3,u2,u1,L,q,c,s,v,w,t = row
    spokes = {n,u4,u3,u2,u1,L}
    right = [(x,y,r) for x,y,r in product(range(4), repeat=3)
             if r not in (s,v,w,t,x,y) and x not in (c,s,y) and y not in (a,t)]
    left = {
        'G': [(b,p,h,R) for b,p,h,R in product(range(4),repeat=4)
              if b not in (a,c,q,p) and p not in (a,q,n,h)
              and h not in (q,L,R,n) and R not in spokes],
        'Q1': [(b,R) for b,R in product(range(4),repeat=2)
               if b == n and R == q and b not in (a,c,q) and R not in spokes],
        'J1': [(b,R) for b,R in product(range(4),repeat=2)
               if b == L and a != R and b not in (a,c,q) and R not in spokes],
    }
    counts = {g: [0]*10 for g in ZERO}
    bad = []
    for graph in ZERO:
        for ls in left[graph]:
            for rs in right:
                boundary = (rs[0],rs[1],a,ls[0],c)
                word = ''.join(map(str,canonical(boundary)))
                counts[graph][ROWS.index(word)] += 1
                if word in ZERO[graph]:
                    bad.append({'graph':graph,'row':word,'left_cap':list(ls),
                                'right_cap':list(rs),'literal_outer_frame':list(boundary)})
    return counts, bad


def evaluate(caps, state_index, literal, paths):
    output = []
    for path in sorted(paths):
        row = list(literal)
        row[1:7] = path
        require(all(row[i] != row[(i+1)%13] for i in range(13)), 'nonproper original rim')
        sid = state_index[canonical(row)]
        counts, bad = direct_caps(tuple(row))
        require(all(counts[g] == [caps['matrices'][g][r][sid] for r in range(10)] for g in ZERO),
                'direct whole-cap counts disagree with original full-fibre matrices')
        output.append({'P_colors':list(path),'literal_D_rim':row,'state':sid,
                       'full_cap_counts':counts,'bad_full_cap_lifts':bad})
    return output


def signatures(caps, index):
    result = []
    for profile in (0,1):
        for center in range(0 if profile == 0 else 1,6):
            betas = ([None] + [0,3])
            for beta in betas:
                if beta is not None and ((center == 0 and beta != 0) or
                    (center == 5 and beta != 3) or (profile == 1 and center == 1 and beta != 0)):
                    continue
                domains = [{1,2} for _ in P]
                if profile == 1:
                    domains[0] = {1,2,3}
                domains[center] = {ORIGINAL_P[center]}
                if beta is not None:
                    domains[center].add(3-beta)
                paths = [x for x in product(*[sorted(d) for d in domains])
                         if all(a != b for a,b in zip(x,x[1:])) and x[0] != 0 and x[-1] != 3
                         and (profile == 0 or x[1] != 0)]
                for target in (0,1):
                    literal = [0,*ORIGINAL_P,3,1,2,target,1-target,2]
                    lifts = evaluate(caps,index,literal,paths)
                    excluded = any(x['bad_full_cap_lifts'] for x in lifts)
                    expected = beta is not None and (
                        (profile == 0 and (center == 0 or (center in (1,2,3,4) and beta == 3))) or
                        (profile == 1 and center in (2,3,4)))
                    require(excluded == expected, 'conditional exclusion table changed')
                    result.append({'profile':profile,'barrier_center':P[center],
                                   'center_signature':'rigid' if beta is None else 'single_H_same_03_endpoints',
                                   'beta':beta,'target':44459 if target == 0 else 44466,
                                   'P_domains':[sorted(d) for d in domains],
                                   'all_strip_lifts':lifts,'source_subbranch_excluded':excluded})
    require(len(result) == 58, 'all signature coverage changed')
    require(sum(r['source_subbranch_excluded'] for r in result) == 22, 'conditional table closure changed')
    return result


def four_phase_K1(caps,index):
    spec = importlib.util.spec_from_file_location('original_collar', HERE/'frozen/audits/2026-10-21-w7-profile0-13e51db/check.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    payload = json.loads(gzip.decompress((HERE/'frozen/audits/2026-10-21-w7-exploration-30dde27/barrier/colorings.json.gz').read_bytes()))
    result = []
    for case in payload['cases']:
        if case['K'] != 1:
            continue
        _, graph = module.collar(case['profile'],case['H_lengths'],with_graph=True)
        S = case['S']; A = S[1:]
        y = next(x for x in A if x.startswith('H'))
        cut = A.index(y)
        sigma = next(dict(zip(S,r[0])) for r in case['records']
                     if dict(zip(S,r[0]))[y] in (1,2))
        center = case['H_order'][case['H_lengths'].index(1)]
        for target, fa, fq in product((0,1),repeat=3):
            # Whole actual 03 components act on A as prefix/suffix.  Their
            # complete E action is not replaced by flipping just these traces.
            fixed = {x:sigma[x] ^ (3 if ((j < cut and fa) or (j > cut and fq)) else 0)
                     for j,x in enumerate(A)}
            literal = [fixed['a'],*ORIGINAL_P,fixed['q'],1,2,target,1-target,2]
            literal[10 if target == 0 else 11] ^= 3 if fq else 0
            domains = [sorted(set(range(4)) - {fixed[z] for z in graph[t] if z in fixed}) for t in P]
            paths = [x for x in product(*domains) if all(a != b for a,b in zip(x,x[1:]))]
            lifts = evaluate(caps,index,literal,paths)
            excluded = any(x['bad_full_cap_lifts'] for x in lifts)
            expected = case['profile'] == 0 and center in ('n','u4','u2') and fa == fq
            require(excluded == expected, 'four-phase original-source action changed')
            result.append({'profile':case['profile'],'barrier_center':center,'target':target,
                           'flip_complete_03_a':fa,'flip_complete_03_q':fq,
                           'all_strip_lifts':lifts,'bad_cap_reached':excluded})
    require(len(result) == 88, 'K1 four-phase coverage changed')
    return result


def compute():
    caps = read_inputs(); index = {tuple(v):i for i,v in enumerate(caps['states'])}
    return {'signatures':signatures(caps,index),'K1_four_complete_03_phases':four_phase_K1(caps,index),
            'closure_scope':'conditional single-barrier signatures only; profiles 0/1 remain OPEN',
            'K1_original_positions_excluded':{'0':['n','u4','u2'],'1':[]},
            'profile0_excluded':False,'profile1_excluded':False,'original_source_realized':False,
            'new_Lean':False,'LP_run':False}


def verify(actual, expected):
    require(actual == expected,'damaged cap witness or enlarged closure')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'independent-caps.json')
    args = parser.parse_args(); expected = compute()
    if args.build:
        with args.certificate.open('x') as stream:
            json.dump(expected,stream,indent=2,sort_keys=True);stream.write('\n')
    verify(json.loads(args.certificate.read_text()),expected)
    controls = 0
    for field in ('profile0_excluded','profile1_excluded','original_source_realized'):
        bad = deepcopy(expected);bad[field] = True
        try:
            verify(bad,expected)
        except ValueError:
            controls += 1
    require(controls == 3,'negative scope controls failed')
    print(json.dumps({'result':'PASS','signature_cases':58,'excluded_signature_target_cases':22,
                      'K1_four_phase_cases':88,'K1_excluded':expected['K1_original_positions_excluded'],
                      'negative_controls':controls,'full_profile_exclusions':[]},sort_keys=True))


if __name__ == '__main__':
    main()
