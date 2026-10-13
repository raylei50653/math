#!/usr/bin/env python3
"""Literal all-row count controls; no target-source enumeration."""
import argparse
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
OLD = 'audits/2026-10-12-neartri-complete-relation-reductions-5d70a399'
COEFFICIENTS = {42: 1, 8: -1, 10: 1, 14: -1, 16: -1, 21: 1,
                23: 1, 30: 1, 33: -1, 44: -1, 51: -1,
                53: 1, 67: 1, 88: -1}


def norm(word):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in word)


def patterns():
    return sorted({norm(p) for p in product(range(4), repeat=7)
                   if all(p[i] != p[(i + 1) % 7] for i in range(7))})


def all_lifts(n, edges, boundary):
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    if any(boundary[u] == boundary[v] for u, v in edges if u < 7 and v < 7):
        return []
    colors = list(boundary) + [-1] * (n - 7)
    result = []

    def visit():
        choices = []
        for v in range(7, n):
            if colors[v] >= 0:
                continue
            allowed = sorted(set(range(4)) - {colors[u] for u in adjacency[v]})
            if not allowed:
                return
            choices.append((len(allowed), v, allowed))
        if not choices:
            result.append(colors[:])
            return
        _, v, allowed = min(choices)
        for c in allowed:
            colors[v] = c
            visit()
        colors[v] = -1

    visit()
    return sorted(result)


def partitions(n):
    def visit(word):
        if len(word) == n:
            yield tuple(tuple(i for i, x in enumerate(word) if x == j)
                        for j in range(max(word) + 1))
            return
        for x in range(max(word) + 2):
            yield from visit(word + [x])
    yield from visit([0])


def equality_value(partition, word):
    return int(all(len({word[v] for v in block}) == 1 for block in partition))


def graph_record(name, n, edges, pats, expect_zero):
    edges = sorted({tuple(sorted(e)) for e in edges})
    lifts = [all_lifts(n, edges, p) for p in pats]
    counts = [len(row) for row in lifts]
    mask = sum(1 << i for i, value in enumerate(counts) if value)
    residual = sum(coef * counts[i] for i, coef in COEFFICIENTS.items())
    assert (residual == 0) == expect_zero, (name, residual)
    return dict(name=name, vertex_count=n, edges=edges, counts=counts,
                relation=mask, full_lifts=lifts, identity_residual=residual,
                identity_status='triggered and holds' if expect_zero else 'counterexample',
                target_source_status='not triggered')


def build():
    cap = json.loads((AUDIT / 'frozen' / OLD / 'cap_probe.json').read_text())
    pats = patterns()
    assert pats == list(map(tuple, cap['pattern_order']))
    records = []
    cycle = [(i, (i + 1) % 7) for i in range(7)]
    records.append(graph_record('bare-C7', 7, cycle, pats, True))
    records.append(graph_record('wheel-C7', 8, cycle + [(i, 7) for i in range(7)], pats, True))
    # Reuse a cap that accepts the crucial row42 and has a private vertex.
    candidates = [(d['actual_cap_vertex_count'], int(mask), d)
                  for mask, d in cap['relations'].items()
                  if int(mask) >> 42 & 1 and d['actual_cap_vertex_count'] > 7]
    n, mask, d = min(candidates, key=lambda item: item[:2])
    record = graph_record('existing-cap-accepts-row42', n, d['actual_cap_edges'], pats, True)
    assert record['relation'] == mask and record['counts'][42] > 0
    record['existing_cap_mask'] = mask
    records.append(record)
    # A literal graph enforcing a crossing equality partition demonstrates
    # why the cofacial disk premise cannot be dropped. Each K5-minus-edge
    # gadget has a private triangle adjacent to both named endpoints.
    bad = []
    for partition in partitions(7):
        residual = sum(c * equality_value(partition, pats[i]) for i, c in COEFFICIENTS.items())
        if residual:
            bad.append((sum(len(b) - 1 for b in partition), partition, residual))
    _, partition, residual = min(bad)
    edges = cycle[:]
    n = 7
    pairs = []
    for block in partition:
        for v in block[1:]:
            u = block[0]
            pairs.append((u, v))
            tri = list(range(n, n + 3))
            n += 3
            edges += list(combinations(tri, 2)) + [(x, y) for x in (u, v) for y in tri]
    record = graph_record('crossing-equality-gadgets-outside-disk-domain', n, edges, pats, False)
    factor = 6 ** len(pairs)
    assert record['counts'] == [factor * equality_value(partition, p) for p in pats]
    record['enforced_partition'] = partition
    record['identity_residual'] = factor * residual
    record['disk_status'] = 'impossible: equality count vector violates the independently proved disk identity'
    records.append(record)
    upper = cap['inner_mask']
    abstract_counts = [int(upper >> i & 1) for i in range(91)]
    abstract_residual = sum(c * abstract_counts[i] for i, c in COEFFICIENTS.items())
    assert abstract_residual == 1
    return dict(pattern_order=pats, coefficients=COEFFICIENTS, literal_controls=records,
                abstract_upper_control=dict(counts=abstract_counts, residual=abstract_residual,
                    status='counterexample', meaning='Kempe and cap feasibility does not imply a realizable count vector'),
                trust='All fixed boundary rows and all literal vertex lifts; target source is not triggered.')


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'controls.json')
    args = parser.parse_args()
    payload = build()
    if args.write:
        with args.certificate.open('x') as stream:
            json.dump(payload, stream, separators=(',', ':'), sort_keys=True)
            stream.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == json.loads(json.dumps(payload)), 'control certificate mismatch'
    print(json.dumps(dict(status='PASS', literal_graphs=len(payload['literal_controls']),
        fixed_row_queries=91 * len(payload['literal_controls']),
        full_lifts=sum(len(row) for graph in payload['literal_controls'] for row in graph['full_lifts']),
        target_source_status='not triggered'), sort_keys=True))


if __name__ == '__main__':
    main()
