#!/usr/bin/env python3
"""Actual smaller annuli, all fibres and B-preserving total lift selectors.

This supplements the primary checker. The independent checker checks these
graphs without importing this file or check.py.
"""
import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import check

ROOT = Path(__file__).resolve().parent


def prism():
    faces = [[0, 4, 3, 2, 1]]+[[i, (i+1) % 5, 5+(i+1) % 5, 5+i] for i in range(5)]+[check.U]
    edges, rotation = check.embedding(10, faces)
    wheel_faces = faces[:-1]+[[5+i, 5+(i+1) % 5, 10] for i in range(5)]
    wheel_edges, wr = check.embedding(11, wheel_faces, sorted(edges+[[i, 10] for i in check.U]))
    return {'key': 'prism', 'vertices': list(range(10)), 'B': check.B, 'U': check.U,
            'private': [], 'faces': faces, 'edges': edges, 'rotation': rotation,
            'wheel_faces': wheel_faces, 'wheel_edges': wheel_edges, 'wheel_rotation': wr,
            'ownership': {'outer_face': 0, 'empty_U_face': len(faces)-1,
                          'centre_after_restoration': 10, 'pin_map': list(range(10))},
            'status': 'triggered and holds: representative, not a minimum source'}


def representative_graphs():
    reps = [check.fill(prism())]
    for mask, word, order in [(639, 'BU', 'BBBUUU'), (959, 'BD', 'BUUBU'), (1021, 'UU', 'BBUBBU')]:
        g = check.fill(check.make({'r': 4, 'c': 1, 'diamond': word, 'gap': 0, 'path': '', 'after': order}))
        assert g['Sigma'] == mask
        reps.append(g)
    assert reps[0]['Sigma'] == 1023
    return reps


def certificate():
    reps = representative_graphs()
    by_mask = {g['Sigma']: g for g in reps}
    transfers, weak_witness = [], None
    distribution, reductions = Counter(), Counter()
    with gzip.open(ROOT/'certificate.jsonl.gz', 'rt') as f:
        header = json.loads(next(f))
        assert header['base'] == check.BASE
        for line in f:
            g = json.loads(line)
            rep = by_mask[g['Sigma']]
            r, rp = len(g['private']), len(rep['private'])
            assert rp < r and 6+rp < 6+r
            rows = []
            for i, (source, target) in enumerate(zip(g['rows'], rep['rows'])):
                assert source['beta'] == target['beta']
                sf, tf = source['wheel_full_lifts'], target['wheel_full_lifts']
                assert bool(sf) == bool(tf)
                # For every input lift, choose the same complete target lift in
                # its original literal beta fibre. Null records an EMPTY row.
                rows.append({'beta': source['beta'], 'source_selector': sf[0] if sf else None,
                             'representative_selector': tf[0] if tf else None})
                if weak_witness is None and g['Sigma'] == 1023:
                    for cell, tau in enumerate(check.TAUS):
                        if len(set(tau)) != 3:
                            continue
                        left, right = source['cells'][cell], target['cells'][cell]
                        if bool(left) != bool(right):
                            weak_witness = {'status': 'counterexample', 'claim': 'equal Sigma implies equal R3',
                                            'source_key': g['key'], 'Sigma': 1023, 'beta': source['beta'],
                                            'tau': tau, 'source_A_lift': left[0] if left else None,
                                            'representative_A_lift': right[0] if right else None,
                                            'source_nonempty': bool(left), 'representative_nonempty': bool(right)}
                            break
            transfers.append({'source_key': g['key'], 'Sigma': g['Sigma'], 'r': r, 'r_prime': rp,
                              'k': 6+r, 'k_prime': 6+rp, 'delta_k': r-rp,
                              'pin_map': list(range(10)), 'preservation': 'complete Sigma only', 'rows': rows})
            distribution[g['Sigma']] += 1
            reductions[r-rp] += 1
    assert len(transfers) == 974 and weak_witness is not None
    return {'base': check.BASE, 'beta_order': check.BETAS, 'tau_order': check.TAUS,
            'representatives': reps, 'transfers': transfers, 'strength_counterexample': weak_witness,
            'summary': {'representatives': len(reps), 'source_templates': len(transfers),
                        'masks': dict(distribution), 'strict_reductions': dict(reductions),
                        'representative_cells': 40960,
                        'representative_empty_cells': sum(not cell for g in reps for row in g['rows'] for cell in row['cells']),
                        'representative_A_lifts': sum(len(cell) for g in reps for row in g['rows'] for cell in row['cells']),
                        'representative_G_lifts': sum(len(row['wheel_full_lifts']) for g in reps for row in g['rows']),
                        'actual_minimum_933_941_source': 'not triggered'}}


def main():
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    args = ap.parse_args()
    cert = certificate()
    data = check.encoded(cert)
    target = ROOT/'representatives.json.gz'
    if args.write:
        with target.open('xb') as f:
            f.write(gzip.compress(data, mtime=0))
        with (ROOT/'representatives-summary.json').open('x') as f:
            json.dump(cert['summary'], f, indent=2, sort_keys=True)
            f.write('\n')
    else:
        assert gzip.decompress(target.read_bytes()) == data
        assert json.loads((ROOT/'representatives-summary.json').read_text()) == json.loads(json.dumps(cert['summary']))
    print(json.dumps(cert['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
