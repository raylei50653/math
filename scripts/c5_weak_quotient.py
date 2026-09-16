#!/usr/bin/env python3
"""Analyze the sealed 87-Sigma certificate, without replaying deletion lattices.

python scripts/c5_weak_quotient.py [--check]
Only Python's standard library is required. This is finite evidence, not Lean.
"""
import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'artifacts/c5_weak_deletion_audit/observations.json'
OUT = ROOT / 'artifacts/c5_weak_quotient/observations.json'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def normalize(row):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in row)


def paths_from(start, adjacency):
    """Shortest paths; sorted neighbors break ties lexicographically."""
    paths = {start: [start]}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for target in sorted(adjacency[node]):
            if target not in paths:
                paths[target] = paths[node] + [target]
                queue.append(target)
    del paths[start]
    return paths


def build():
    source = json.loads(INPUT.read_text())
    # Bind to the saved audit's inputs and code, without invoking its checker.
    for name, expected in (source['inputs'] | source['source_sha256']).items():
        assert digest(ROOT / name) == expected, name
    assert not source['conclusion']['collision_sigma']
    variants = source['sigma_variants']
    assert all(len(entries) == 1 for entries in variants.values())
    weak = {int(s): set(entries[0]['weak_exits']) for s, entries in variants.items()}
    nodes = sorted(weak)
    assert len(nodes) == 87
    edges = {(s, t) for s in nodes for t in weak[s]}
    inclusion = {(s, t) for s in nodes for t in nodes if s != t and s & t == s}
    assert edges <= inclusion
    middle = {(s, t): [r for r in nodes if (s, r) in inclusion and (r, t) in inclusion]
              for s, t in inclusion}
    covers = {pair for pair in inclusion if not middle[pair]}
    paths = {s: paths_from(s, weak) for s in nodes}
    closure = {(s, t) for s in nodes for t in paths[s]}
    # Independent Floyd-Warshall closure checks BFS, without relying on counts.
    floyd = set(edges)
    for r in nodes:
        floyd |= {(s, t) for s in nodes for t in nodes
                  if (s, r) in floyd and (r, t) in floyd}
    assert closure == floyd and closure <= inclusion
    reduction = {(s, t) for s, t in edges
                 if not any((r, t) in closure for r in weak[s] - {t})}
    reduced = {s: {t for a, t in reduction if a == s} for s in nodes}
    assert {(s, t) for s in nodes for t in paths_from(s, reduced)} == closure
    assert all(not any((s, r) in closure and (r, t) in closure for r in nodes)
               for s, t in reduction)
    depth, height = {}, {}
    for s in nodes:  # strict bit inclusion implies numeric increase
        depth[s] = max((depth[a] + 1 for a, b in edges if b == s), default=0)
    for s in reversed(nodes):
        height[s] = max((height[t] + 1 for t in weak[s]), default=0)

    patterns = list(map(tuple, source['pattern_order']))
    rows = list(product(range(4), repeat=5))
    rows = [p for p in rows if all(p[i] != p[(i+1) % 5] for i in range(5))]
    assert len(rows) == 240 and sorted({normalize(p) for p in rows}) == patterns
    actions, equivariance, failures = [], [], []
    for reflection in (0, 1):
        for shift in range(5):
            name = f'r{shift}s{reflection}'
            # Same pullback convention as c5_cell_enumerator.d5_index_maps.
            positions = [((-1 if reflection else 1) * (i+shift)) % 5 for i in range(5)]
            perm = [patterns.index(normalize(tuple(p[i] for i in positions))) for p in patterns]
            assert sorted(perm) == list(range(10))

            def act(s):
                return sum(1 << perm[j] for j in range(10) if s >> j & 1)

            assert {act(s) for s in nodes} == set(nodes)
            # Check compression/action against all ordered proper rows.
            for s in nodes:
                transformed = {tuple(p[i] for i in positions) for p in rows
                               if s >> patterns.index(normalize(p)) & 1}
                expected = {p for p in rows if act(s) >> patterns.index(normalize(p)) & 1}
                assert transformed == expected
                lhs, rhs = weak[act(s)], {act(t) for t in weak[s]}
                entry = dict(action=name, sigma=s, image=act(s), lhs=sorted(lhs), rhs=sorted(rhs))
                equivariance.append(entry)
                if lhs != rhs:
                    failures.append(entry)
            actions.append(dict(name=name, pullback_positions=positions, pattern_permutation=perm,
                                node_map=[[s, act(s)] for s in nodes]))

    parents_path = ROOT / next(iter(source['inputs']))
    parents = {p['id']: p for p in json.loads(parents_path.read_text())['parents']}
    cycle = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}
    node_rows = []
    for s in nodes:
        entry = variants[str(s)][0]
        parent_id, mask = entry['representative']
        parent = parents[parent_id]
        optional = sorted(set(map(tuple, parent['edges'])) - cycle)
        graph = sorted(cycle | {e for i, e in enumerate(optional) if mask >> i & 1})
        node_rows.append(dict(sigma=s, pattern_indices=[j for j in range(10) if s >> j & 1],
                              outdegree=len(weak[s]), indegree=sum(t == s for _, t in edges),
                              dag_depth=depth[s], height_to_sink=height[s],
                              weak_exits=sorted(weak[s]), reachable=sorted(paths[s]),
                              inclusion_covers=sorted(t for a, t in covers if a == s),
                              representative=dict(parent=parent_id, mask=mask, k=parent['k'], edges=graph)))

    def comparison(actual, expected, kind):
        extra, missing = sorted(actual - expected), sorted(expected - actual)
        witnesses = []
        for s, t in extra:
            witness = dict(kind='extra', pair=[s, t], shortest_weak_path=paths[s][t])
            if kind == 'covers':
                # Three nodes are a minimum-size certificate of a non-cover.
                witness['intermediate'] = min(middle[s, t], key=lambda r: (r.bit_count(), r))
            witnesses.append(witness)
        for s, t in missing:
            witness = dict(kind='missing', pair=[s, t])
            if kind == 'covers':
                witness.update(weak_exits=sorted(weak[s]), intermediates=middle[s, t])
            else:
                # Forward-closed reachable set excludes target: certificate of nonreachability.
                cut = {s} | set(paths[s])
                assert t not in cut and all(weak[r] <= cut for r in cut)
                witness['forward_closed_cut'] = sorted(cut)
            witnesses.append(witness)
        key = lambda w: (w['pair'][0].bit_count(), w['pair'][1].bit_count(), *w['pair'])
        return dict(equal=actual == expected, common=len(actual & expected),
                    extra=extra, missing=missing, witnesses=witnesses,
                    smallest_by_kind={k: min((w for w in witnesses if w['kind'] == k), key=key, default=None)
                                      for k in ('extra', 'missing')})

    cover_comparison = comparison(edges, covers, 'covers')
    order_comparison = comparison(closure, inclusion, 'order')
    # Independently replay only the minimal counterexample representatives;
    # this is not the sealed deletion-lattice audit.
    minimal_ids = set()
    for comparison_row in (cover_comparison, order_comparison):
        for witness in comparison_row['smallest_by_kind'].values():
            if witness:
                minimal_ids.update(witness['pair'])
                if 'intermediate' in witness:
                    minimal_ids.add(witness['intermediate'])
    for node in node_rows:
        if node['sigma'] not in minimal_ids:
            continue
        graph = node['representative']
        actual = set()
        for boundary in rows:
            for inner in product(range(4), repeat=graph['k']):
                colors = boundary + inner
                if all(colors[u] != colors[v] for u, v in graph['edges']):
                    actual.add(boundary)
                    break
        expected = {p for p in rows if node['sigma'] >> patterns.index(normalize(p)) & 1}
        assert actual == expected
    redundant = []
    for s, t in sorted(edges - reduction):
        adjacency = dict(weak)
        adjacency[s] = weak[s] - {t}
        redundant.append(dict(pair=[s, t], shortest_alternative_path=paths_from(s, adjacency)[t]))
    return dict(schema=1, scope='The 87 observed Sigma classes in the sealed k<=3 audit only.',
                inputs={str(INPUT.relative_to(ROOT)): digest(INPUT)},
                source_sha256={str(Path(__file__).resolve().relative_to(ROOT)): digest(Path(__file__))},
                pattern_order=patterns,
                minimal_representatives_full_row_checked=sorted(minimal_ids),
                witness_convention='Per mismatch: minimal node certificate (pair or non-cover triple); shortest paths by BFS with numeric tie-break. Intermediate minimizes (popcount, integer). Global minima minimize (source popcount, target popcount, source, target). Graph representatives are inherited, NOT claimed graph-minimal. Missing reachability uses the least forward-closed set containing source.',
                nodes=node_rows, edges=sorted(edges), inclusion_order=sorted(inclusion),
                inclusion_covers=sorted(covers), transitive_closure=sorted(closure),
                transitive_reduction=sorted(reduction), redundant_edge_witnesses=redundant,
                W_vs_covers=cover_comparison, TC_vs_inclusion=order_comparison,
                d5=dict(actions=actions, comparisons=equivariance, failures=failures),
                summary=dict(nodes=len(nodes), edges=len(edges), inclusion_pairs=len(inclusion),
                             inclusion_covers=len(covers), closure_pairs=len(closure),
                             reduction_edges=len(reduction), max_dag_depth=max(depth.values()),
                             depth_histogram=dict(sorted(Counter(depth.values()).items())),
                             sources=[s for s in nodes if depth[s] == 0],
                             sinks=[s for s in nodes if not weak[s]],
                             cover_common=cover_comparison['common'],
                             cover_extra=len(cover_comparison['extra']), cover_missing=len(cover_comparison['missing']),
                             order_extra=len(order_comparison['extra']), order_missing=len(order_comparison['missing']),
                             d5_checks=len(equivariance), d5_failures=len(failures)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'artifact differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))
    for name in ('W_vs_covers', 'TC_vs_inclusion'):
        print(name, json.dumps(result[name]['smallest_by_kind']))


if __name__ == '__main__':
    main()
