#!/usr/bin/env python3
"""Frozen finite checks for the paper dependency audit, not a graph theorem.

Requires networkx==3.5 for the 132 existing witnesses' apex planarity.
--write creates a certificate exclusively; --check reads and compares it.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FROZEN = HERE / 'frozen'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def report():
    import networkx as nx
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    for row in manifest['files']:
        need(hashlib.sha256((FROZEN / row['path']).read_bytes()).hexdigest()
             == row['sha256'], 'frozen input hash: ' + row['path'])
    spec = importlib.util.spec_from_file_location(
        'frozen_screen', FROZEN / 'scripts/c5_kempe_screen.py')
    screen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(screen)
    data = json.loads((FROZEN / 'artifacts/c5_cells/cells.json').read_text())
    known = set(map(int, data['cells']))
    cycle = [(i, (i + 1) % 5) for i in range(5)]
    def normalize(p):
        seen = {}
        return tuple(seen.setdefault(c, len(seen)) for c in p)
    pats = sorted({normalize(p) for p in itertools.product(range(4), repeat=5)
                   if all(p[u] != p[v] for u, v in cycle)})
    need(pats == list(screen.REPS) == list(map(tuple, data['pattern_order'])),
         'independent boundary pattern order')
    witness_rows = []
    for mask in sorted(known):
        cell = data['cells'][str(mask)]
        k = cell['k_eff']
        need(0 <= k <= 5, 'five-interior witness bound')
        edges = cycle + [tuple(e) for e in cell['edges']]
        counts = []
        for p in pats:
            count = 0
            for rest in itertools.product(range(4), repeat=k):
                coloring = p + rest
                if all(coloring[u] != coloring[v] for u, v in edges):
                    count += 1
            counts.append(count)
        actual = sum(1 << i for i, c in enumerate(counts) if c)
        need(actual == mask, 'complete witness relation ' + str(mask))
        graph = nx.Graph()
        graph.add_nodes_from(range(6 + k))
        graph.add_edges_from(edges + [(i, 5 + k) for i in range(5)])
        need(nx.check_planarity(graph)[0], 'witness apex planarity')
        witness_rows.append(dict(mask=mask, interior_vertices=k,
                                 full_row_counts=counts, apex_planar=True))
    table = screen.obligations()
    accepted = {m for m in range(1024) if screen.failure(m, table) is None}
    need(len(known) == 132 and len(accepted) == 154, 'screen sizes')
    need(0 in accepted and 0 not in known and known <= accepted, 'zero and inclusion')
    extras = accepted - known
    caps = {
        7: [(0, 2)], 56: [(0, 3)], 193: [(1, 3)],
        266: [(1, 4)], 592: [(2, 4)],
        63: [(0, 2), (0, 3)], 249: [(0, 3), (1, 3)],
        459: [(1, 3), (1, 4)], 599: [(0, 2), (2, 4)],
        858: [(1, 4), (2, 4)],
    }
    cap_rows = []
    for source, chords in sorted(caps.items()):
        cap = sum(1 << i for i, p in enumerate(pats)
                  if all(p[u] != p[v] for u, v in chords))
        need(cap in known and source & cap == 0, 'exact chord-cap intersection')
        need(all(set(a) & set(b) for a, b in itertools.combinations(chords, 2)),
             'noncrossing fan cap')
        cap_rows.append(dict(source=source, cap=cap, chords=[list(e) for e in chords],
                             cap_private_vertices=0, intersection=0))
    need({m for m in extras if m and m & 932 != 932} == set(caps), 'low orbit coverage')
    remaining = extras - {0} - set(caps)
    need(remaining == {screen.act(m, r, f) for m in (932, 933, 941)
                       for r in range(5) for f in (False, True)}, 'new residual domain')
    union_pairs = list(itertools.combinations_with_replacement(sorted(known), 2))
    need(len(union_pairs) == 8778 and all(a | b in known for a, b in union_pairs),
         'catalogue union closure')
    need(sorted(m for m in accepted if m & 932 == m) == [0, 932], 'pure T4 support')
    subs = {str(m): sorted(t for t in known if t & m == t) for m in (932, 933, 941)}
    need(subs == {'932': [], '933': [165], '941': [165, 424, 429]}, 'subset tables')
    for r in range(5):
        for f in (False, True):
            need({screen.act(m, r, f) for m in known} == known, 'D5 catalogue closure')
    return dict(
        trust='Finite inputs only; general descent and normal form are paper proofs; external Corollary 20 not replayed.',
        counts=dict(catalogue=132, kempe_including_zero=154, nonempty_extras=21,
                    zero_interior_caps=10, minimal_source_candidates=11, union_pairs=8778),
        extra_nonempty_orbits=screen.orbits(extras - {0}),
        minimal_source_orbits=screen.orbits(remaining),
        cap_rows=cap_rows, catalogue_subrelations=subs,
        t4_kempe_subrelations=[0, 932], witnesses=witness_rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    result = report()
    if args.write:
        with args.certificate.open('x') as handle:
            handle.write(json.dumps(result, indent=2) + '\n')
    else:
        need(json.loads(args.certificate.read_text()) == result, 'certificate mismatch')
    print(json.dumps(result['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
