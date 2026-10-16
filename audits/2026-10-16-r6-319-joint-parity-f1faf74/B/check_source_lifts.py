#!/usr/bin/env python3
"""Independent all-five-vertex lift audit for the original nine-boundary disk.

This uses the declared original graph edges and brute-force assignments, not
C's nested palette exclusions or a projected marginal. It does not rerun any
graph enumeration or claim that a necessary boundary row is realizable.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random


PINS = ('c', 's', 'j', 'i', 'w', 't', 'a', 'p', 'q')
ADDED = ('v', 'r', 'x', 'y', 'b')
ATTACHMENTS = {
    'v': ('r', 'w', 'i', 'j', 's'),
    'r': ('x', 'y', 't', 'w', 'v', 's'),
    'x': ('y', 'c', 'r', 's'),
    'y': ('x', 'a', 'r', 't'),
    'b': ('a', 'c', 'p', 'q'),
}


def canonical(row):
    seen = []
    out = []
    for x in row:
        if x not in seen:
            seen.append(x)
        out.append(seen.index(x))
    return tuple(out)


def name(row):
    return ''.join('ABCD'[x] for x in row)


def reconstruct(seed, candidate):
    rng = random.Random(seed)
    root = Path(__file__).resolve().parents[1]
    binding = root / 'SOURCE_G_INPUT.json'
    bound = json.loads(binding.read_text())['inputs']
    assert len(bound) == 1
    frozen = root / 'frozen' / bound[0]['path']
    assert frozen.stat().st_size == bound[0]['size']
    assert hashlib.sha256(frozen.read_bytes()).hexdigest() == bound[0]['sha256']
    names = PINS + ADDED
    index = {v: i for i, v in enumerate(names)}
    boundary = [tuple(sorted((PINS[i], PINS[(i + 1) % 9]))) for i in range(9)]
    new_edges = sorted({tuple(sorted((a, b))) for a, ns in ATTACHMENTS.items() for b in ns})
    edges = sorted(set(boundary + new_edges))
    for a, ns in ATTACHMENTS.items():
        actual = {v if u == a else u for u, v in edges if a in (u, v)}
        assert actual == set(ns)
    assert {a: sum(a in uv for uv in edges) for a in ADDED} == {
        'v': 5, 'r': 6, 'x': 4, 'y': 4, 'b': 4}
    attach_indices = [(index[a], index[b]) for a, b in new_edges]
    patterns = sorted({canonical(r) for r in itertools.product(range(4), repeat=5)
                       if all(r[i] != r[(i + 1) % 5] for i in range(5))})
    assert len(patterns) == 10
    bit = {r: 1 << i for i, r in enumerate(patterns)}
    raw = list(itertools.product(range(4), repeat=9))
    rng.shuffle(raw)
    proper = sorted({canonical(r) for r in raw
                     if all(r[i] != r[(i + 1) % 9] for i in range(9))})
    assert len(proper) == 820
    extra = list(itertools.product(range(4), repeat=5))
    rng.shuffle(extra)
    fibres = {}
    for row in proper:
        out = []
        for ext in extra:
            full = row + ext
            if all(full[a] != full[b] for a, b in attach_indices):
                original_boundary = tuple(full[index[a]] for a in ('x', 'y', 'a', 'b', 'c'))
                out.append(list(ext) + [bit[canonical(original_boundary)]])
        fibres[name(row)] = sorted(out)
    c_data = json.loads(candidate.read_text())
    assert c_data['pins'] == list(PINS) and c_data['added'] == list(ADDED)
    summaries = []
    for mask in (932, 933, 941):
        upper = sorted(r for r, lifts in fibres.items()
                       if all(lift[-1] & mask for lift in lifts))
        supplied = next(r for r in c_data['results'] if r['source_mask'] == mask)
        assert upper == supplied['upper_rows']
        fixed = supplied['fixed_rows']
        assert set(fixed) <= set(upper)
        # These two support recalculations do not certify C's fixed-point run.
        # They do check every full lift over the exact supplied surviving rows.
        source_support = 0
        u_support = 0
        for r in fixed:
            for lift in fibres[r]:
                source_support |= lift[-1]
            row = tuple('ABCD'.index(a) for a in r)
            c, s, j, i, w, t, a, p, q = row
            if a != c:
                continue
            for v in range(4):
                if all(v != row[index[n]] for n in ('s', 'j', 'i', 'w')):
                    u_support |= bit[canonical((c, s, v, w, t))]
        assert source_support == supplied['source_lift_support'] == mask
        assert u_support == supplied['U_lift_support'] == 319
        summaries.append({'source_mask': mask, 'upper_rows': upper,
                          'empty_lift_rows_retained': [r for r in upper if not fibres[r]],
                          'provided_fixed_row_count': len(fixed),
                          'provided_fixed_source_support': source_support,
                          'provided_fixed_U_support': u_support})
    return {'scope': 'exact local full reconstruction and all upper rows; fixed-point elimination not independently rerun',
            'source_instances': 'not triggered',
            'source_geometry_sha256': bound[0]['sha256'],
            'candidate_sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
            'pins': list(PINS), 'added': list(ADDED),
            'all_local_edges': [list(e) for e in edges],
            'pattern_order': [name(r) for r in patterns],
            'all_820_complete_reconstruction_fibres': fibres,
            'cases': summaries}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--candidate', type=Path)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path)
    mode.add_argument('--check', type=Path)
    args = p.parse_args()
    candidate = args.candidate or Path(__file__).resolve().parents[1] / 'C/full-source-exploration.json'
    result = reconstruct(args.seed, candidate)
    if args.output:
        with args.output.open('x') as f:
            json.dump(result, f, sort_keys=True, indent=2)
            f.write('\n')
    elif json.loads(args.check.read_text()) != result:
        raise SystemExit('FAIL: complete original lift reconstruction differs')
    print(json.dumps({'status': 'PASS', 'proper_boundary_orbits': 820,
                      'upper_counts': [len(r['upper_rows']) for r in result['cases']],
                      'empty_fibre_counts': [len(r['empty_lift_rows_retained']) for r in result['cases']],
                      'provided_fixed_counts': [r['provided_fixed_row_count'] for r in result['cases']]}))


if __name__ == '__main__':
    main()
