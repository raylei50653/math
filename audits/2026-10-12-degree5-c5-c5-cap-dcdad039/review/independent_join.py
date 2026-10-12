#!/usr/bin/env python3
"""Independent fixed-frame cap join; does not import the primary checker.

Reconstructs proper labeled relation sets by all 24 global colour permutations,
then enumerates every x,y,z,v tuple for every B row and all ordered cap pairs.
Outputs are a second finite check, not a new completeness theorem for K.
"""
from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'frozen/audits/2026-10-12-cofacial-uniform-separation-eb6b2303/frozen/artifacts/c5_cells/cells.json'
OUT = Path(__file__).with_suffix('.json')


def run():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    patterns = data['pattern_order']
    masks = sorted(map(int, data['cells']))
    assert len(masks) == 132 and len(patterns) == 10
    color_permutations = list(permutations(range(4)))
    expanded = {
        mask: {tuple(perm[c] for c in pat)
               for i, pat in enumerate(patterns) if mask & (1 << i)
               for perm in color_permutations}
        for mask in masks
    }
    # No per-cap colour renaming takes place within the join.
    interfaces = []
    for a,b,c,d,e in patterns:
        options = []
        for x,y,z,v in product(range(4), repeat=4):
            if v in {a,x,c,y,z}:
                continue
            p, q = (a,b,c,y,z), (a,x,c,d,e)
            if all(p[i] != p[(i+1)%5] for i in range(5)) and all(q[i] != q[(i+1)%5] for i in range(5)):
                options.append(((x,y,z,v),p,q))
        interfaces.append(options)
    histogram = Counter()
    records = []
    total_joint_tuples = 0
    digest = sha256()
    for pm in masks:
        for qm in masks:
            result = 0
            counts = []
            for i, options in enumerate(interfaces):
                tuples = [t for t,p,q in options if p in expanded[pm] and q in expanded[qm]]
                counts.append(len(tuples))
                total_joint_tuples += len(tuples)
                if tuples:
                    result |= 1 << i
                digest.update(json.dumps([pm,qm,i,tuples], separators=(',',':')).encode())
                digest.update(b'\n')
            records.append([pm,qm,result,counts])
            histogram[result] += 1
    ac_masks = [m for m in masks if [0,2] in data['cells'][str(m)]['edges']]
    result = {
        'schema': 'independent-degree5-c5-c5-join-v1',
        'source_sha256': sha256(raw).hexdigest(),
        'method': '24 actual color-name permutations then all 4^4 ordered assignments in a fixed B frame',
        'pattern_order': patterns,
        'pair_count': len(records),
        'pair_records_schema': ['P_mask','Q_mask','output_mask','ten_row_complete_interface_tuple_counts'],
        'pair_records': records,
        'output_histogram': {str(k):v for k,v in sorted(histogram.items())},
        'outside_K': sorted(set(histogram) - set(masks)),
        'complete_interface_joint_sha256': digest.hexdigest(),
        'total_complete_interface_tuples': total_joint_tuples,
        'literal_ac_cap_masks': ac_masks,
        'double_ac_pairs': len(ac_masks)**2,
        'status': 'triggered and holds' if not set(histogram) - set(masks) else 'counterexample',
        'scope': 'fixed-frame relation join only; main certificate separately verifies literal whole graph lifts and embedding',
    }
    return result


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    if args.check:
        assert json.loads(OUT.read_text()) == result
    else:
        with OUT.open('x') as f:
            json.dump(result, f, sort_keys=True, indent=2)
            f.write('\n')
    print(json.dumps({k:result[k] for k in ['pair_count','output_histogram','outside_K','total_complete_interface_tuples','double_ac_pairs','status']}, sort_keys=True))
