#!/usr/bin/env python3
"""Exhaustive labelled C5 additions; colouring evidence, geometry unchecked."""
import argparse
from collections import Counter
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

from local_closure import direct_graph_extend

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/extension_effects/observations.json'
CYCLE = [(i, (i + 1) % 5) for i in range(5)]
PAIRS = list(combinations(range(5), 2))
BOUNDARY = [b for b in product(range(4), repeat=5)
            if all(b[u] != b[v] for u, v in CYCLE)]
FULL = set(range(len(BOUNDARY)))


def neighbors(mask):
    return [i for i in range(5) if mask >> i & 1]


def available(b, mask):
    return set(range(4)) - {b[i] for i in neighbors(mask)}


def pair_view(rows):
    # Exact labelled pair projections, not merely equal/different flags.
    return [{(BOUNDARY[k][u], BOUNDARY[k][v]) for k in rows}
            for u, v in PAIRS]


def encode(rows):
    return format(sum(1 << k for k in rows), '060x')


def build():
    records = []
    checks = 0

    def record(name, family, n, extra, predicted, before=FULL):
        nonlocal checks
        edges = CYCLE + extra
        actual = {k for k, b in enumerate(BOUNDARY)
                  if direct_graph_extend(n, edges, b)}
        checks += len(BOUNDARY)
        assert actual == predicted and actual <= before
        lost = sorted(before - actual)
        changes = [list(pair) for pair, p, q in
                   zip(PAIRS, pair_view(before), pair_view(actual)) if p != q]
        records.append(dict(name=name, family=family, vertices=n, added_edges=extra,
                            before=encode(before), after=encode(actual),
                            before_count=len(before), after_count=len(actual),
                            lost_count=len(lost), changed_pairs=changes,
                            lost_witness=list(BOUNDARY[lost[0]]) if lost else None,
                            geometry='unknown'))
        return actual

    for u, v in PAIRS:
        if (u - v) % 5 not in (1, 4):
            record(f'chord_{u}_{v}', 'boundary_edge', 5, [(u, v)],
                   {k for k, b in enumerate(BOUNDARY) if b[u] != b[v]})
    stars = {}
    for mask in range(32):
        stars[mask] = record(f'star_{mask}', 'one_vertex', 6,
                            [(i, 5) for i in neighbors(mask)],
                            {k for k, b in enumerate(BOUNDARY) if available(b, mask)})
        if mask.bit_count() <= 3:
            assert stars[mask] == FULL
    for left, right in product(range(32), repeat=2):
        extra = [(i, 5) for i in neighbors(left)] + [(i, 6) for i in neighbors(right)]
        independent = stars[left] & stars[right]
        record(f'two_{left}_{right}_0', 'two_independent', 7, extra, independent)
        linked = {k for k, b in enumerate(BOUNDARY)
                  if any(x != y for x in available(b, left) for y in available(b, right))}
        record(f'two_{left}_{right}_1', 'internal_edge', 7, extra + [(5, 6)], linked,
               before=independent)
        # An edge loses precisely those extensions with the same singleton list.
        assert independent - linked == {
            k for k in independent if len(available(BOUNDARY[k], left)) == 1
            and available(BOUNDARY[k], left) == available(BOUNDARY[k], right)}
    summary = {}
    for family in sorted({r['family'] for r in records}):
        group = [r for r in records if r['family'] == family]
        summary[family] = dict(cases=len(group),
                              strict=sum(r['lost_count'] > 0 for r in group),
                              strict_with_same_pairs=sum(r['lost_count'] > 0 and
                                                         not r['changed_pairs'] for r in group),
                              empty=sum(r['after_count'] == 0 for r in group),
                              after_counts=dict(sorted(Counter(r['after_count'] for r in group).items())))
    witnesses = {}
    for category, predicate in [
        ('hidden_higher_order', lambda r: r['family'] == 'one_vertex' and
         r['lost_count'] > 0 and not r['changed_pairs']),
        ('interior_edge_forces_pair', lambda r: r['family'] == 'internal_edge' and
         r['before_count'] == 240 and 0 < r['after_count'] < 240 and r['changed_pairs']),
        ('interior_edge_hidden', lambda r: r['family'] == 'internal_edge' and
         r['lost_count'] > 0 and not r['changed_pairs']),
    ]:
        candidates = [r for r in records if predicate(r)]
        if candidates:
            witnesses[category] = min(candidates, key=lambda r: (len(r['added_edges']), r['name']))['name']
    return dict(schema=1, scope='fixed ordered C5; no chords in vertex cases; labelled private vertices; geometry unchecked',
                source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (Path(__file__).resolve(), ROOT / 'scripts/local_closure.py')},
                boundary_rows=BOUNDARY, pair_order=PAIRS,
                encoding='240-bit hex; bit k is boundary_rows[k]; no independent colour renaming',
                direct_graph_queries=checks, summary=summary, witnesses=witnesses, rows=records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        if OUT.read_text() != data:
            raise SystemExit('artifact differs; rebuild explicitly')
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(dict(summary=result['summary'], witnesses=result['witnesses'],
                          direct_graph_queries=result['direct_graph_queries']), indent=2))


if __name__ == '__main__':
    main()
