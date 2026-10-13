#!/usr/bin/env python3
"""Explicit same-slot representative and preservation-strength controls.
No claim of minimum-source realizability. Each graph has every named fibre.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
from check import B, U, BETAS, TAUS, embedding, fill, encoded, make

ROOT = Path(__file__).resolve().parent


def graph(key, n, faces):
    edges, rotation = embedding(n, faces)
    wf = faces[:-1]+[[5+i, 5+(i+1) % 5, n] for i in range(5)]
    we, wr = embedding(n+1, wf)
    assert we == sorted(edges+[[u, n] for u in U])
    private = list(range(10, n))
    pe = [e for e in edges if e[0] >= 10]
    unseen, components = set(private), 0
    while unseen:
        components += 1
        todo = [min(unseen)]
        while todo:
            x = todo.pop()
            if x not in unseen:
                continue
            unseen.remove(x)
            todo.extend(b if a == x else a for a, b in pe if x in (a, b))
    return fill({'key': key, 'vertices': list(range(n)), 'B': B, 'U': U,
                 'private': private, 'r': n-10, 'faces': faces, 'edges': edges,
                 'rotation': rotation, 'wheel_faces': wf, 'wheel_edges': we,
                 'wheel_rotation': wr, 'degree_G': [sum(v in e for e in we) for v in range(n+1)],
                 'degree_private': [sum(v in e for e in pe) for v in private],
                 'rho_private': len(pe)-len(private)+components,
                 'ownership': {'outer_face': 0, 'empty_U_face': len(faces)-1,
                               'centre_after_restoration': n, 'pin_map': list(range(10))},
                 'minimum_source': 'not triggered'})


def support(g):
    return {(i, j) for i, row in enumerate(g['rows']) for j, c in enumerate(row['cells'])
            if c and len(set(TAUS[j])) == 3}


def certificate():
    outer = [[0, 4, 3, 2, 1]]
    quads = [[i, (i+1) % 5, 5+(i+1) % 5, 5+i] for i in range(5)]
    p = graph('prism_representative_r0', 10, outer+quads+[U])
    triangles = []
    for i in range(5):
        triangles.extend([[i, (i+1) % 5, 5+i], [(i+1) % 5, 5+(i+1) % 5, 5+i]])
    d = graph('triangulated_prism_r0', 10, outer+triangles+[U])
    plus = graph('prism_private_degree2', 11,
                 outer+[[0, 1, 6, 5, 10], [0, 10, 5]]+quads[1:]+[U])
    contractible = graph('contractible_private_triangle_weaker_premises', 13,
                         outer+[[0, 10, 12, 11, 10, 0, 1, 6, 5], [10, 11, 12]]+quads[1:]+[U])
    essential = fill(make('DDDDD'))
    essential['key'] = 'essential_r5_weaker_premises'
    essential['rho_private'] = 1
    essential['minimum_source'] = 'not triggered: k=11; occupied private C5'
    assert contractible['rho_private'] == 1
    assert min(contractible['degree_G'][10:13]) == 2
    assert p['Sigma'] == d['Sigma'] == plus['Sigma'] == contractible['Sigma'] == 1023
    assert support(p) != support(d)
    assert support(p) == support(plus) == support(contractible)
    for i in range(10):
        for j in range(1024):
            assert len(plus['rows'][i]['cells'][j]) == 2*len(p['rows'][i]['cells'][j])
            assert len(contractible['rows'][i]['cells'][j]) == 18*len(p['rows'][i]['cells'][j])
    # This first necessary template supplies an explicit same-Sigma, different-R3
    # source/representative pair; all other templates use their complete certificate.
    with gzip.open(ROOT/'certificate.jsonl.gz', 'rt') as f:
        next(f)
        first = json.loads(next(f))
    assert first['Sigma'] == p['Sigma'] and support(first) != support(p)
    delta = sorted(support(first)^support(p))[0]
    i, j = delta
    witness = {'template': first['key'], 'beta': BETAS[i], 'tau': TAUS[j],
               'template_full_lifts': first['rows'][i]['cells'][j],
               'representative_full_lifts': p['rows'][i]['cells'][j]}
    gs = [p, d, plus, contractible, essential]
    return {'beta_order': BETAS, 'tau_order': TAUS, 'graphs': gs,
            'same_Sigma_different_R3': {'pair': [p['key'], d['key']],
                                      'status': 'counterexample to stronger implication'},
            'same_R3_different_multiplicity': {'pair': [p['key'], plus['key']], 'factor': 2,
                                              'status': 'counterexample to stronger implication'},
            'template_to_representative_R3_difference': witness,
            'weaker_unicyclic_controls': {
                'contractible': 'triggered and holds under weaker premises; full degree fails',
                'essential': 'triggered and holds under weaker premises; k>=13 and empty/proper C5 cap fail'},
            'source_minimality': 'not triggered',
            'representative': {'r_prime': 0, 'k_prime': 6, 'delta_k': [7, 8, 9, 10],
                               'strength': 'capped Sigma only; B colors preserved; U/centre colors may change'}}


def main():
    p = argparse.ArgumentParser()
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = p.parse_args()
    data = certificate()
    raw = encoded(data)
    path = ROOT/'strength.json.gz'
    out = {'graphs': len(data['graphs']), 'cells': 10240*len(data['graphs']),
           'H_full_lifts': sum(len(c) for g in data['graphs'] for row in g['rows'] for c in row['cells']),
           'G_full_lifts': sum(len(row['wheel_full_lifts']) for g in data['graphs'] for row in g['rows']),
           'empty_cells': sum(not c for g in data['graphs'] for row in g['rows'] for c in row['cells']),
           'graph_masks': {g['key']: g['Sigma'] for g in data['graphs']},
           'mathematical_sha256': hashlib.sha256(raw).hexdigest()}
    if args.write:
        with path.open('xb') as f:
            f.write(gzip.compress(raw, mtime=0))
        with (ROOT/'strength_summary.json').open('x') as f:
            json.dump(out, f, indent=2, sort_keys=True)
            f.write('\n')
    else:
        assert gzip.decompress(path.read_bytes()) == raw
        assert json.loads((ROOT/'strength_summary.json').read_text()) == out
    print(json.dumps(out, sort_keys=True))


if __name__ == '__main__':
    main()
