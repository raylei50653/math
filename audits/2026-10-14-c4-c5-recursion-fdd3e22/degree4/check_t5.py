#!/usr/bin/env python3
"""Exact nested all-lift and necessary Kempe control for original r6,t5.

Paper geometry is in R6_TRANSFER.md. The generic h!=p case uses seven pins;
the literal h=p case uses six distinct vertices, without an extra internal p.
"""
import argparse
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('local_transfer', HERE / 'check_transfer.py')
transfer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transfer)
COLORS = tuple(range(4))
EDGES = transfer.EDGES
PINS = ('z', 's', 'v', 'w', 'h', 'p', 'q')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def generic_allowed(row):
    if any(row[a] == row[b] for a, b in EDGES):
        return False
    z, s, v, w, h, p, q = row
    return all(transfer.allowed((z, s, v, w, t, p, q))
               for t in COLORS if t not in (z, w, h))


def direct_allowed(row):
    """Independent direct local graph extension plus fixed-frame case table."""
    if any(row[a] == row[b] for a, b in EDGES):
        return False
    table = {
        (0, 1, 0, 1): {(2, 3), (3, 2)},
        (0, 1, 0, 2): set(),
        (0, 1, 2, 1): {(1, 3), (2, 3), (3, 1), (3, 2)},
        (0, 1, 2, 3): {(1, 3), (3, 1)},
    }
    z, s, v, w, h, p, q = row
    for t, r in product(COLORS, repeat=2):
        if t in (z, w, h) or r in (s, v, w, t):
            continue
        lifted = transfer.canonical((z, s, r, t, p, q))
        if lifted[4:] not in table[lifted[:4]]:
            return False
    return True


def alias_allowed(row):
    z, s, v, w, p, q = row
    return generic_allowed((z, s, v, w, p, p, q))


def calculate():
    catalogue_bytes = (HERE / 'cells.json').read_bytes()
    need(sha256(catalogue_bytes).hexdigest() == transfer.CATALOGUE_SHA256,
         'frozen catalogue drift')
    catalogue = json.loads(catalogue_bytes)
    patterns = [tuple(row) for row in catalogue['pattern_order']]
    masks = sorted(map(int, catalogue['cells']))
    need(len(masks) == 132, 'catalogue size')
    generic_labelled = []
    for row in product(COLORS, repeat=7):
        need(generic_allowed(row) == direct_allowed(row), 'nested/direct disagreement')
        if generic_allowed(row):
            generic_labelled.append(row)
    alias_labelled = []
    for row in product(COLORS, repeat=6):
        z, s, v, w, p, q = row
        need(alias_allowed(row) == direct_allowed((z, s, v, w, p, p, q)),
             'alias nested/direct disagreement')
        if alias_allowed(row):
            alias_labelled.append(row)
    generic_table, alias_table = [], []
    generic_mask = alias_mask = 0
    for i, boundary in enumerate(patterns):
        pq = [x for x in permutations(COLORS, 2) if generic_allowed(boundary + x)]
        qs = [q for q in COLORS if alias_allowed(boundary + (q,))]
        generic_table.append({'index': i, 'boundary': transfer.name(boundary),
                              'ordered_pq': [transfer.name(x) for x in pq]})
        alias_table.append({'index': i, 'boundary': transfer.name(boundary),
                            'q_colours': transfer.name(qs)})
        if pq:
            generic_mask |= 1 << i
        if qs:
            alias_mask |= 1 << i
    candidates = [m for m in masks if not m & ~generic_mask]
    alias_candidates = [m for m in masks if not m & ~alias_mask]
    need(generic_mask == 575 and candidates == [564, 567, 572, 575],
         'generic all-lift screen')
    need(alias_mask == 542 and not alias_candidates, 'alias all-lift screen')
    rows = sorted({transfer.canonical(row) for row in generic_labelled})
    live, closure = transfer.fixed_point(rows, EDGES)
    support = sum(1 << i for i, boundary in enumerate(patterns)
                  if any(transfer.canonical(row[:5]) == boundary for row in live))
    final_candidates = [m for m in masks if not m & ~support]
    need(len(rows) == 22 and len(live) == 12 and support == 63,
         'generic fixed point')
    need(not final_candidates, 'catalogue survived')
    # These are exactly the two orbit pairs excluded in the short paper proof.
    first_pair = [(0, 1, 2, 0, 2, 2, 3), (0, 1, 2, 0, 2, 3, 2)]
    second_pair = [(0, 1, 2, 3, 2, 2, 3), (0, 1, 2, 3, 2, 3, 2)]
    need(all(transfer.name(row) in closure['rounds'][0]['removed']
             for row in first_pair), 'first paper exclusion not in round1')
    need(all(transfer.name(row) in closure['rounds'][1]['removed']
             for row in second_pair), 'second paper exclusion not in round2')
    # Paper proof only removes bit9, without using the additional closure rows.
    paper_upper_mask = generic_mask & ~(1 << 9)
    need(paper_upper_mask == 63, 'paper upper bound')
    need(not [m for m in masks if not m & ~paper_upper_mask], 'paper catalogue gap')
    need(not generic_allowed((0, 1, 2, 1, 2, 1, 3)), 'forbidden ABCBC negative')
    need(not generic_allowed((0, 1, 2, 3, 1, 2, 3)), 'forbidden ABCDB negative')
    need(generic_allowed(second_pair[0]) and second_pair[0] not in live,
         'outer-only positive row must fail Kempe control')
    return {
        'status': 'PASS; r6,t5 source branch excluded by exact local necessity and K132',
        'generic_pins': PINS, 'generic_skeleton': EDGES,
        'alias_pins': ('z', 's', 'v', 'w', 'p', 'q'), 'alias_identity': 'h=p',
        'generic_table': generic_table, 'alias_table': alias_table,
        'generic_outer_upper_mask': generic_mask, 'generic_K_candidates': candidates,
        'alias_outer_upper_mask': alias_mask, 'alias_K_candidates': alias_candidates,
        'generic_labelled_rows': len(generic_labelled),
        'alias_labelled_rows': len(alias_labelled),
        'generic_initial_orbits': [transfer.name(row) for row in rows],
        'generic_final_orbits': [transfer.name(row) for row in sorted(live)],
        'generic_final_outer_support': support, 'generic_final_K_candidates': final_candidates,
        'paper_upper_mask_after_two_Kempe_steps': paper_upper_mask,
        'paper_first_excluded_orbits': [transfer.name(row) for row in first_pair],
        'paper_second_excluded_orbits': [transfer.name(row) for row in second_pair],
        'closure': closure,
        'negative_controls': {'all_16384_generic_rows_crosschecked': True,
                              'all_4096_alias_rows_crosschecked': True,
                              'forbidden_ABCBC_rejected': True,
                              'forbidden_ABCDB_rejected': True,
                              'local_positive_ABCDC_removed_by_Kempe': True},
        'actual_target_sources': 0,
        'catalogue_sha256': transfer.CATALOGUE_SHA256,
        'transfer_script_sha256': sha256((HERE / 'check_transfer.py').read_bytes()).hexdigest(),
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 't5.json')
    args = parser.parse_args()
    result = calculate()
    payload = json.dumps(result, indent=2) + '\n'
    if args.check:
        need(args.certificate.read_text() == payload, 't5 certificate differs')
    else:
        with args.certificate.open('x') as handle:
            handle.write(payload)
    print(json.dumps({'ok': True, 'generic_upper_mask': 575,
                      'generic_K_candidates': [564, 567, 572, 575],
                      'generic_fixed_point': {'orbits': [22, 12], 'outer_support': 63,
                                              'K_candidates': []},
                      'alias_upper_mask': 542, 'alias_K_candidates': [],
                      'actual_target_sources': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
