#!/usr/bin/env python3
"""Full k<=3 weak-deletion audit on the existing plantri parent deletion domain.

uv run --with networkx==3.5 python scripts/c5_weak_deletion_audit.py [--check]
No completion lemma, trace enumeration, or Sigma-based search pruning.
"""
import argparse
from collections import Counter, defaultdict
from itertools import product
import json
from pathlib import Path

from c5_cell_enumerator import REPS, compat_tables
from c5_disk_deletions import CYCLE, canonical, parse_disk, relation, sha
from c5_disk_weak_successors import members, submasks

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'artifacts/c5_disk_deletions/observations.json'
OUT = ROOT / 'artifacts/c5_weak_deletion_audit/observations.json'


def digest(value):
    import hashlib
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def certify_parents(source):
    """Re-expand every input embedding, fixing boundary labels pointwise."""
    for run in source['inputs']['runs']:
        k = run['k']
        path = INPUT.parent / 'plantri' / run['file']
        assert sha(path) == run['sha256']
        lines = path.read_text().splitlines()
        assert len(lines) == run['count']
        graphs = set()
        for line in lines:
            edges, outer, _ = parse_disk(line, k)
            for direction in (1, -1):
                for shift in range(5):
                    order = [outer[(shift + direction*i) % 5] for i in range(5)]
                    order += sorted(set(range(5+k)) - set(outer))
                    labels = {v: i for i, v in enumerate(order)}
                    graphs.add(canonical(5+k, [(labels[u], labels[v]) for u, v in edges]))
        rows = [p for p in source['parents'] if p['k'] == k]
        assert sorted(graphs) == [tuple(map(tuple, p['edges'])) for p in rows]


def lattice(parent):
    k = parent['k']
    edges = sorted(set(map(tuple, parent['edges'])) - CYCLE)
    size = 1 << len(edges)
    sigma = [0] * size
    tables, full = compat_tables(k, edges)
    # Intersection DP over compatible interior assignments.
    for j, boundary in enumerate(REPS):
        viable = [full] * size
        for mask in range(1, size):
            bit = mask & -mask
            viable[mask] = viable[mask ^ bit] & tables[bit.bit_length()-1][j]
        # Independent existential coloring: mark each assignment's complete
        # satisfied-edge mask, then propagate truth to every subset (zeta OR).
        exists = bytearray(size)
        for inner in product(range(4), repeat=k):
            colors = boundary + inner
            good = sum(1 << i for i, (u, v) in enumerate(edges) if colors[u] != colors[v])
            exists[good] = 1
        for i in range(len(edges)):
            bit = 1 << i
            for mask in range(size):
                if not mask & bit:
                    exists[mask] |= exists[mask | bit]
        for mask in range(size):
            assert bool(viable[mask]) == bool(exists[mask])
            sigma[mask] |= int(exists[mask]) << j
    assert sigma[-1] == parent['sigma']
    weak = [0] * size  # Bit s denotes target relation integer s, not a color row.
    strict = silent = 0
    for mask in range(size):
        for i in members(mask):
            child = mask ^ (1 << i)
            assert sigma[mask] & sigma[child] == sigma[mask]
            if sigma[child] == sigma[mask]:
                weak[mask] |= weak[child]
                silent += 1
            else:
                weak[mask] |= 1 << sigma[child]
                strict += 1
        assert not weak[mask] >> sigma[mask] & 1
    # Independent definition check for EVERY state: subset-zeta union of the
    # direct strict exits of equal-Sigma submasks. Monotonicity guarantees that
    # each such submask is reachable through equal-Sigma intermediate states.
    direct = [0] * size
    for mask in range(size):
        for i in members(mask):
            child = mask ^ (1 << i)
            if sigma[child] != sigma[mask]:
                direct[mask] |= 1 << sigma[child]
    for s in set(sigma):
        reference = [direct[m] if sigma[m] == s else 0 for m in range(size)]
        for i in range(len(edges)):
            bit = 1 << i
            for mask in range(size):
                if mask & bit:
                    reference[mask] |= reference[mask ^ bit]
        for mask in range(size):
            if sigma[mask] == s:
                assert reference[mask] == weak[mask]
    return edges, sigma, weak, silent, strict


def reference_exit(mask, sigma):
    """Definition via all equal-Sigma submasks; independent of weak DP."""
    paths = {}
    for sub in submasks(mask):
        if sigma[sub] == sigma[mask]:
            for i in members(sub):
                child = sub ^ (1 << i)
                if sigma[child] != sigma[mask]:
                    paths.setdefault(sigma[child], (sub, child))
    return paths


def witness(parent, mask):
    edges, sigma, weak, _, _ = lattice(parent)
    paths = reference_exit(mask, sigma)
    assert sorted(paths) == list(members(weak[mask]))
    graph = tuple(sorted(CYCLE | {edges[i] for i in members(mask)}))
    assert relation(5+parent['k'], graph)[0] == sigma[mask]
    routes = []
    for target, (sub, child) in sorted(paths.items()):
        current = mask
        silent = []
        for i in members(mask ^ sub):
            current ^= 1 << i
            assert sigma[current] == sigma[mask]
            silent.append(edges[i])
        strict, = members(sub ^ child)
        target_graph = tuple(sorted(CYCLE | {edges[i] for i in members(child)}))
        assert relation(5+parent['k'], target_graph)[0] == target
        routes.append(dict(target=target, silent_deleted=silent, strict_deleted=edges[strict]))
    return dict(parent=parent['id'], k=parent['k'], mask=mask, edges=graph,
                sigma=sigma[mask], weak_exits=sorted(paths), exit_routes=routes,
                definition_checked_submasks=1 << mask.bit_count())


def build():
    source = json.loads(INPUT.read_text())
    assert source['pattern_order'] == [list(b) for b in REPS]
    certify_parents(source)
    groups = defaultdict(dict)
    per_k = [Counter() for _ in range(4)]
    rows = []
    unique = [dict() for _ in range(4)]
    for index, parent in enumerate(source['parents']):
        k = parent['k']
        edges, sigma, weak, silent, strict = lattice(parent)
        universe = [(u, v) for u in range(5+k) for v in range(u+1, 5+k) if (u, v) not in CYCLE]
        edge_bits = [1 << universe.index(e) for e in edges]
        graph_masks = [0] * len(sigma)
        for mask, (s, w) in enumerate(zip(sigma, weak)):
            if mask:
                bit = mask & -mask
                graph_masks[mask] = graph_masks[mask ^ bit] | edge_bits[bit.bit_length()-1]
            previous = unique[k].setdefault(graph_masks[mask], (s, w))
            assert previous == (s, w), "same labelled graph differs across parent lattices"
            entry = groups[s].setdefault(w, dict(count=0, by_k=Counter(), representative=[parent['id'], mask]))
            entry['count'] += 1
            entry['by_k'][k] += 1
        # Root definition check covers every parent, including all silent descendants.
        assert sorted(reference_exit(len(sigma)-1, sigma)) == list(members(weak[-1]))
        per_k[k].update(parents=1, raw_states=len(sigma), silent=silent, strict=strict)
        rows.append(dict(parent=parent['id'], states=len(sigma), table_sha256=digest([sigma, weak]),
                         root_weak_exits=list(members(weak[-1]))))
        if (index+1) % 50 == 0:
            print(f'audited {index+1}/726 parents', flush=True)
    variants = {str(s): [dict(weak_exits=list(members(w)), **entry)
                         for w, entry in sorted(ws.items())] for s, ws in sorted(groups.items())}
    collisions = [s for s, ws in sorted(groups.items()) if len(ws) > 1]
    lookup = {p['id']: p for p in source['parents']}
    examples = []
    for s in collisions:
        entries = variants[str(s)]
        pair = [witness(lookup[e['representative'][0]], e['representative'][1]) for e in entries[:2]]
        examples.append(dict(sigma=s, pair=pair,
                             distinguishing_targets=sorted(set(pair[0]['weak_exits']) ^ set(pair[1]['weak_exits']))))
    statistics = [dict(k=k, **row, unique_labelled_graphs=len(unique[k]),
                       transitions=row['silent']+row['strict']) for k, row in enumerate(per_k)]
    return dict(schema=1,
                scope='All nonboundary-edge deletion descendants of all 726 existing k=0..3 plantri parents; all vertices retained; no completion lemma.',
                semantics='tau preserves Sigma; strict action label is target Sigma; W=tau* then one strict step; edge identities and costs hidden',
                inputs={str(INPUT.relative_to(ROOT)): sha(INPUT)},
                source_sha256={str(p.relative_to(ROOT)): sha(p) for p in [Path(__file__).resolve(),
                    ROOT/'scripts/c5_disk_deletions.py', ROOT/'scripts/c5_disk_weak_successors.py',
                    ROOT/'scripts/c5_cell_enumerator.py', ROOT/'scripts/local_closure.py',
                    ROOT/'scripts/boundary_relations.py']},
                pattern_order=REPS, statistics=statistics, parent_tables=rows, sigma_variants=variants,
                conclusion=dict(raw_states=sum(r['raw_states'] for r in statistics),
                                transitions=sum(r['transitions'] for r in statistics),
                                unique_labelled_graphs=sum(map(len, unique)), relations=len(groups),
                                collision_sigma=collisions, sigma_is_weak_bisimulation=not collisions),
                witnesses=examples,
                verification='Every mask: compatible-assignment intersection vs independent coloring satisfied-mask downward zeta; all deletion edges monotone; W DAG DP vs equal-Sigma submask exit union by independent subset zeta on every state; duplicate labelled graphs agree across parents. Every root and witness: exhaustive equal-Sigma submask exit definition. Witness sources and exit targets: all 240 boundary rows backtracking. Parent embeddings re-expanded from hashed plantri files.')


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
    print(json.dumps(result['statistics'], indent=2))
    print(json.dumps(result['conclusion'], indent=2))


if __name__ == '__main__':
    main()
