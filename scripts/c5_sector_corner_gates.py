#!/usr/bin/env python3
"""Audit necessary corner crossings and endpoint-aware saturated gates."""
import argparse
from hashlib import sha256
from itertools import combinations_with_replacement
import json
from pathlib import Path
from c5_sector_leaf_corners import alternating

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'artifacts/c5_sector_leaf_corners/observations.json'
OUT = ROOT / 'artifacts/c5_sector_corner_gates/observations.json'


def build():
    saved = json.loads(UPSTREAM.read_text())
    for name, digest in saved['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    barriers = {'Q': ('1', 'q'), 'P': ('3', 'p'), 'R': ('4', 'r'),
                'U': ('1', '3')}
    cases = []
    for corners in saved['retained']:
        word = ['1', '2', '3', *corners[1:]]
        hits = {}
        for target in ('1', '2'):
            path = ('b', target)
            hits[target] = [name for name, ends in barriers.items()
                            if not set(path) & set(ends) and alternating(word, path, ends)]
        cases.append(dict(corners=corners, expanded=word, alternating_barriers=hits))
    assert [c['alternating_barriers'] for c in cases] == [
        {'1': ['P', 'R'], '2': ['P', 'R', 'U']},
        {'1': [], '2': ['Q', 'U']}]
    # A b--2 path may meet frame vertex 1; Q/U then have a boundary
    # intersection without a saturated interior star. P/R have no such escape.
    local = []
    for d in (2, 3):
        for location in ('internal', 'b_endpoint'):
            required = [0, 0, d, d] if location == 'internal' else [0, d, d]
            candidates = []
            size = 4 if location == 'internal' else 3
            for colors in combinations_with_replacement((0, 2, 3), size):
                if all(colors.count(c) >= required.count(c) for c in (0, 2, 3)):
                    full = sorted(colors if location == 'internal' else (*colors, 0))
                    assert full == [0, 0, d, d]
                    candidates.append(dict(J_neighbor_colors=list(colors), G_neighbor_colors=full))
            assert len(candidates) == 1
            local.append(dict(d=d, location=location, possibilities=candidates))
    inputs = {UPSTREAM, Path(__file__).resolve()}
    inputs.update(ROOT / p for p in saved['input_sha256'])
    return dict(schema=1, scope='Necessary crossing and local degree audit; no sector realization or exclusion.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                cases=cases, local_stars=local,
                caveat='Q/U crossings for b--2 require avoiding frame vertex 1; P/R do not.',
                summary=dict(corner_orders=2, path_endpoint_cases=4, local_star_cases=4,
                             profile_deletions=0, inherited_profiles=603))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
