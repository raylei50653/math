#!/usr/bin/env python3
"""Exact edge switches, component reconnection, and intermediate compatibility.

uv run --with networkx==3.5 python scripts/c5_edge_switches.py [--check]
Uses only the fixed Errera regression and three existing survivor routes.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from c5_edge_states import Dual, TYPE_PAIRS
from c5_kempe_connectivity import adjacency, pair_components, swap, PAIRS, component
from c5_complementary_cube import singleton_of, encode

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_cells/edge_states.json'
OUT = ROOT / 'artifacts/c5_cells/edge_switches.json'


def trace(g, start, actions):
    edges = [tuple(e) for e in g['edges']]
    adj = adjacency(g['n'], edges)
    dual = Dual(g['n'], edges, g['faces'])

    def state(c):
        assert all(c[u] != c[v] for u, v in edges)
        bad = singleton_of(c) in (1, 3, 4)
        escapes = [(p, sorted(s)) for p in PAIRS for s in pair_components(adj, c, p)
                   if singleton_of(swap(c, s, p)) in (1, 3, 4)]
        row = dict(coloring=c, types=[c[u] ^ c[v] for u, v in edges],
                   T=dual.state(c), systems=dual.systems(c),
                   forbidden_now=bad, compatible_through_one_move=not bad and not escapes,
                   escape_actions=escapes)
        if c[:5] == (0, 1, 0, 2, 3):
            s = component(adj, c, (0, 2), 0)
            t = component(adj, c, (0, 3), 2)
            row.update(S=sorted(s), T_region=sorted(t),
                       interface=sorted((u, v) for u in s if c[u] == 2
                                        for v in adj[u] & t if c[v] == 3))
        return row

    c = tuple(start)
    states, transitions = [state(c)], []
    for action in actions:
        p, block = tuple(action['pair']), frozenset(action['component'])
        assert block in pair_components(adj, c, p)
        d = swap(c, block, p)
        k = p[0] ^ p[1]
        cut = {j for j, (u, v) in enumerate(edges) if (u in block) != (v in block)}
        before, after = dual.systems(c), dual.systems(d)
        si = TYPE_PAIRS.index(tuple(t for t in (1, 2, 3) if t != k))
        selected = [j for j, (_, es) in enumerate(before[si]) if cut & set(es)]
        assert set().union(*(set(before[si][j][1]) for j in selected)) == cut
        assert before[si] == after[si]
        delta = [c[u] ^ c[v] for u, v in edges]
        switched = [t ^ k if j in cut else t for j, t in enumerate(delta)]
        assert switched == [d[u] ^ d[v] for u, v in edges]
        assert swap(d, block, p) == c  # A concrete switch is reversible.
        reconnections = []
        for i in range(3):
            old, new = before[i], after[i]
            # Common retained edges give an exact incidence correspondence;
            # counts alone must not be interpreted as a topological contraction.
            overlaps = [[sorted(set(a[1]) & set(b[1])) for b in new] for a in old]
            reconnections.append(dict(system=TYPE_PAIRS[i], retained_edge_overlap=overlaps,
                                      old_cycles=sum(not t for t, _ in old),
                                      new_cycles=sum(not t for t, _ in new),
                                      removed_edges=sorted(set().union(*(set(es) for _, es in old)) -
                                                           set().union(*(set(es) for _, es in new))),
                                      added_edges=sorted(set().union(*(set(es) for _, es in new)) -
                                                         set().union(*(set(es) for _, es in old)))))
        transitions.append(dict(pair=p, component=sorted(block), xor=k,
                                cut_edge_indices=sorted(cut), cut_edges=[edges[j] for j in sorted(cut)],
                                preserved_system=TYPE_PAIRS[si], selected_components=selected,
                                same_compressed_T=dual.state(c) == dual.state(d),
                                reconnections=reconnections))
        c = d
        states.append(state(c))
    dual.systems.cache_clear()
    return dict(graph=g['name'], n=g['n'], edges=edges, faces=g['faces'],
                states=states, transitions=transitions)


def report():
    source = json.loads(SOURCE.read_text())
    regression = source['same_class_regression']
    g = next(g for g in source['graphs'] if g['name'] == regression['graph'])
    route = [dict(pair=regression['pair'], component=regression['component']),
             *regression['independently_labeled_bfs_routes'][1]['moves']]
    rows = [trace(g, regression['colorings'][0], route)]
    assert rows[0]['transitions'][0]['same_compressed_T']
    assert rows[0]['states'][0]['interface'] and not rows[0]['states'][1]['interface']
    assert rows[0]['states'][1]['S'] == [0] and rows[0]['states'][1]['T_region'] == [2]
    assert [s['compatible_through_one_move'] for s in rows[0]['states']] == [True, True, False, False]
    for g in source['graphs']:
        if g['name'].startswith('survivor'):
            for r in g['escapes']:
                rows.append(trace(g, r['start'], r['moves']))
    files = [SOURCE, Path(__file__), *(ROOT / 'scripts' / f for f in
              ('c5_edge_states.py', 'c5_kempe_connectivity.py', 'c5_complementary_cube.py',
               'c5_kempe_screen.py', 'c5_ab_swap_cube.py'))]
    return dict(trust='Fixed embedded graphs and exact Python replay; no graph contraction or Lean theorem.',
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files},
                summary=[dict(graph=r['graph'], switches=len(r['transitions']),
                              compatibility=[s['compatible_through_one_move'] for s in r['states']],
                              cycle_counts=[[sum(not t for t, _ in system) for system in s['systems']]
                                            for s in r['states']]) for r in rows], traces=rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    r = report()
    text = encode(r) + '\n'
    if args.check:
        assert OUT.read_text() == text
    else:
        OUT.write_text(text)
    print(json.dumps(r['summary'], indent=2))


if __name__ == '__main__':
    main()
