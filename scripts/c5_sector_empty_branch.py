#!/usr/bin/env python3
"""Local identity certificates for the empty B3 branch; no graph search."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_sector_empty_branch/observations.json'
CROSS = ROOT / 'artifacts/c5_sector_cross_row/observations.json'
STARS = ROOT / 'artifacts/c5_sector_saturated_cuts/observations.json'
PAIRS = list(combinations(range(4), 2))
OLD = (0, 1, 0, 2, 1)
RAW = (1, 0, 1, 2, 1)
ALPHA = (0, 1, 2, 1, 2)


def build():
    states = json.loads(CROSS.read_text())['abstract']['states']
    assert states[397]['row'] == list(OLD)
    swap = {0: 1, 1: 0, 2: 2, 3: 3}
    assert [swap[c] for c in RAW] == states[330]['row']
    old_parts = dict(zip(PAIRS, states[397]['partitions'], strict=True))
    new_parts = {tuple(sorted(swap[c] for c in pair)): part
                 for pair, part in zip(PAIRS, states[330]['partitions'], strict=True)}

    def separated(parts, pair, a, b):
        assert any(a in cc for cc in parts[pair])
        assert any(b in cc for cc in parts[pair])
        return not any(a in cc and b in cc for cc in parts[pair])

    leaves = []
    for attachment in combinations(range(5), 3):
        if len({ALPHA[v] for v in attachment}) != 3:
            continue
        assert 0 in attachment
        for color in sorted(set(range(4)) - {OLD[v] for v in attachment}):
            # A color-1 neighbor of 0 lies in its maximal 01 component.
            selected = color == 1
            raw_color = 0 if selected else color
            if color == 1:
                assert attachment == (0, 2, 3)
                assert raw_color == 0 and RAW[3] == 2
                witness = dict(kind='nonempty_B3', path=[5, 3], pair=[0, 2],
                               deleted_frame=1)
            elif 2 in attachment:
                pair = (0, color)
                assert separated(old_parts, pair, 0, 2)
                assert {OLD[0], color, OLD[2]} <= set(pair)
                witness = dict(kind='old_separation', path=[0, 5, 2], pair=list(pair))
            else:
                assert 4 in attachment
                pair = (1, color)
                assert separated(new_parts, pair, 0, 4)
                assert {RAW[0], raw_color, RAW[4]} <= set(pair)
                witness = dict(kind='new_separation', path=[0, 5, 4], pair=list(pair))
            path = witness['path']
            edges = {tuple(sorted((5, v))) for v in attachment}
            assert all(tuple(sorted(e)) in edges for e in zip(path, path[1:]))
            assert len(path) == len(set(path))
            leaves.append(dict(attachments=attachment, old_color=color,
                               selected=selected, raw_color=raw_color, exclusion=witness))
    assert len(leaves) == 7
    assert sum(e['exclusion']['kind'] == 'nonempty_B3' for e in leaves) == 1

    # For 0-b-2, both alternating barriers would have to use the only
    # interior vertex b. Their necessary complete neighbor multisets differ.
    star_types = [[0, 0, d, d] for d in (2, 3)]
    assert star_types[0] != star_types[1]
    assert len([0, 0, 2, 2, 3, 3]) > 4
    b_candidates = [list(a) for k in range(1, 5) for a in combinations(range(5), k)
                    if 0 in a and all(OLD[v] != 1 for v in a)]
    assert b_candidates == [[0], [0, 2], [0, 3], [0, 2, 3]]
    b_survivors = [a for a in b_candidates if 2 not in a and 3 not in a]
    assert b_survivors == [[0]]

    inherited = json.loads(STARS.read_text())
    for name, digest in inherited['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    inputs = {CROSS, STARS, Path(__file__).resolve()}
    inputs.update(ROOT / name for name in inherited['input_sha256'])
    return dict(schema=1, scope='Local necessary configurations, not complete sector realizations; arbitrary-size claims are paper proofs.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                              for p in sorted(inputs)},
                old_row=OLD, raw_new_row=RAW, leaf_cases=leaves,
                color1_neighbor=dict(candidate_attachments=b_candidates,
                                     surviving_attachments=b_survivors,
                                     hypothetical_path=[0, 5, 2],
                                     required_star_multisets=star_types,
                                     internal_degree=3),
                summary=dict(leaf_color_cases=len(leaves), separation_exclusions=6,
                             empty_branch_exclusions=1, color1_attachment_cases=4,
                             color1_attachment_survivors=1),
                closure_effect=dict(inherited_profiles=603, profile_deletions=0,
                                    fixed_point_recomputed=False))


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
