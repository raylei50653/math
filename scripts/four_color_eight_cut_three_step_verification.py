#!/usr/bin/env python3
"""Necessary cut screens and exact three-step original-edge fibres; no 4CT oracle."""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import four_color_seven_cut_verification as base

ROOT = Path(__file__).resolve().parents[1]


def mapping_from_links(links):
    parent = list(range(8))

    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v

    for i in links:
        parent[root((i + 1) % 8)] = root(i)
    return base.normalize(tuple(root(i) for i in range(8)))


def minimal_endpoint_maps(a, b):
    """One shared endpoint at each triangular dual face; no additional IDs merged.

    Any actual map is a coarsening of one map returned here. Thus not forcing
    nonconsecutive identifications is a necessary relaxation, not an assumption.
    """
    choices = [tuple(side for side, row in enumerate((a, b))
                     if row[i] == row[(i + 1) % 8]) for i in range(8)]
    for sides in product(*choices):
        maps = tuple(mapping_from_links([i for i, side in enumerate(sides) if side == s])
                     for s in (0, 1))
        # A simple original graph cannot have two edges with both endpoints equal.
        if len(set(zip(*maps))) == 8:
            yield maps


@lru_cache(None)
def tied_options(row, split, endpoint_map):
    pairs = base.SPLITS[split]
    groups = [[i for i, c in enumerate(row) if c in pair] for pair in pairs]
    answer = []
    for left in base.partitions(groups[0]):
        for right in base.partitions(groups[1]):
            blocks = left + right
            owner = {i: j for j, block in enumerate(blocks) for i in block}
            if any(endpoint_map[i] == endpoint_map[j] and owner[i] != owner[j]
                   for i in range(8) for j in range(i)):
                continue
            if not base.noncrossing(blocks):
                continue
            orbit = set()
            for selected in range(1 << len(blocks)):
                changed = list(row)
                for j, block in enumerate(blocks):
                    if selected >> j & 1:
                        pair = next(p for p in pairs if row[block[0]] in p)
                        for i in block:
                            changed[i] = sum(pair) - changed[i]
                orbit.add(base.normalize(tuple(changed)))
            answer.append((tuple(sorted(orbit)), blocks))
    return tuple(answer)


def tied_first_obstruction(fixed, moving, endpoint_map):
    for split in range(3):
        if not any(all(base.incompatible(fixed, changed) for changed in orbit)
                   for orbit, _ in tied_options(moving, split, endpoint_map)):
            return split
    return None


def compatible_rows(endpoint_map):
    size = len(set(endpoint_map))
    return sorted({base.normalize(tuple(colors[j] for j in endpoint_map))
                   for colors in product(range(4), repeat=size)
                   if all(endpoint_map[i] == endpoint_map[(i + 1) % 8]
                          or colors[endpoint_map[i]] != colors[endpoint_map[(i + 1) % 8]]
                          for i in range(8))})


@lru_cache(None)
def one_side_closure(fixed, endpoint_map):
    """Greatest necessary Kempe family blocked against one fixed other-side row.

    Every actual complete moving-side coloring is included initially and each
    actual component partition has its full split orbit included. Synchronous
    peeling therefore preserves all actual blocked families, even through
    four-color boundary states. Abstract witnesses may change across splits.
    """
    rows = compatible_rows(endpoint_map)
    alive = {row for row in rows if base.incompatible(fixed, row)}
    initial = len(alive)
    rounds = []
    while True:
        removed = []
        for row in sorted(alive):
            for split in range(3):
                if not any(all(changed in alive for changed in orbit)
                           for orbit, _ in tied_options(row, split, endpoint_map)):
                    removed.append((row, split))
                    break
        if not removed:
            break
        alive.difference_update(row for row, _ in removed)
        rounds.append(removed)
    return dict(all_rows=len(rows), initial_blocked_rows=initial,
                round_sizes=list(map(len, rounds)),
                removed_rounds=rounds, residual=sorted(alive))


def cut_audit():
    rows = sorted({base.normalize(r) for r in product(range(3), repeat=8)
                   if len(set(r)) == 3})
    decisions, survivors = [], []
    for a in rows:
        for b in rows:
            if base.incompatible(a, b):
                x = base.first_obstruction(b, a)
                y = base.first_obstruction(a, b)
                decisions.append((a, b, x, y))
                if x is None and y is None:
                    survivors.append((a, b))
    triangular = [(a, b) for a, b in survivors
                  if all(a[i] == a[(i + 1) % 8] or b[i] == b[(i + 1) % 8]
                         for i in range(8))]
    mapped = []
    for a, b in triangular:
        for mx, my in minimal_endpoint_maps(a, b):
            x = tied_first_obstruction(b, a, mx)
            y = tied_first_obstruction(a, b, my)
            mapped.append(dict(a=a, b=b, endpoint_X=mx, endpoint_Y=my,
                               X_failed_split=x, Y_failed_split=y))
    for case in mapped:
        case['X_multistep'] = one_side_closure(tuple(case['b']), tuple(case['endpoint_X']))
        case['Y_multistep'] = one_side_closure(tuple(case['a']), tuple(case['endpoint_Y']))
        case['bilateral_multistep_survives'] = (
            tuple(case['a']) in case['X_multistep']['residual']
            and tuple(case['b']) in case['Y_multistep']['residual'])
    shape = lambda r: ''.join(map(str, sorted(Counter(r).values(), reverse=True)))
    assert len(rows) == 966 and len(decisions) == 80640 and len(survivors) == 5392
    return dict(three_color_rows=len(rows), Hall_failures=len(decisions),
                one_block_bilateral_survivors=len(survivors),
                survivor_multiplicities=dict(sorted(Counter(
                    f'{shape(a)}x{shape(b)}' for a, b in survivors).items())),
                triangular_adjacency_survivors=len(triangular),
                triangular_pairs=triangular, endpoint_map_cases=mapped,
                tied_full_split_orbit_survivors=sum(
                    r['X_failed_split'] is None and r['Y_failed_split'] is None for r in mapped),
                bilateral_multistep_survivors=sum(c['bilateral_multistep_survives'] for c in mapped),
                decision_digest=sha256(json.dumps(decisions, separators=(',', ':')).encode()).hexdigest())


def three_step_audit():
    # Original graph: x1=0,x2=1,z=2; boundary a,b,c,d,e,f=3,...,8.
    # ab,cd provide genuine triangle anchors. e,f are adjacent only to z.
    edges = [(0, 1), (0, 2), (1, 2), (0, 3), (0, 4), (3, 4),
             (1, 5), (1, 6), (5, 6), (2, 7), (2, 8)]
    fibres, counts = [], Counter()
    witness = None
    for boundary in product(range(4), repeat=6):
        # Exact successive joins/projections, always keeping a common prefix.
        first = []
        for x2, z in product(range(4), repeat=2):
            lifts = [x1 for x1 in range(4)
                     if all((x1, x2, z, *boundary)[u] != (x1, x2, z, *boundary)[v]
                            for u, v in edges if 0 in (u, v))]
            first.append((x2, z, lifts))
        second = {z: [(x1, x2) for x2, oldz, lifts in first if oldz == z
                      for x1 in lifts
                      if all((x1, x2, z, *boundary)[u] != (x1, x2, z, *boundary)[v]
                             for u, v in edges if 0 not in (u, v) and 1 in (u, v))]
                  for z in range(4)}
        lifted = [(x1, x2, z) for z, lifts in second.items() for x1, x2 in lifts
                  if all((x1, x2, z, *boundary)[u] != (x1, x2, z, *boundary)[v]
                         for u, v in edges if 0 not in (u, v) and 1 not in (u, v))]
        direct = [inner for inner in product(range(4), repeat=3)
                  if all((*inner, *boundary)[u] != (*inner, *boundary)[v] for u, v in edges)]
        assert sorted(lifted) == direct
        ab, cd = set(boundary[:2]), set(boundary[2:4])
        valid_boundary = len(ab) == len(cd) == 2
        A, B = set(range(4)) - ab, set(range(4)) - cd
        pre_z = {z for z in range(4) if second[z]}
        counts[f'pre_z_support_{len(pre_z)}'] += valid_boundary
        if valid_boundary and len(pre_z) == 2 and not direct and witness is None:
            witness = dict(boundary=boundary, A=sorted(A), B=sorted(B),
                           support_z_before_original_z_leaf_edges=sorted(pre_z),
                           leaf_colors=boundary[4:])
        fibres.append(dict(row=boundary, full_internal_lifts=direct))
    assert witness is not None
    return dict(vertices=list(range(9)), original_edges=edges,
                elimination_order=[0, 1, 2], boundary_order=list(range(3, 9)),
                complete_boundary_rows=4**6, complete_original_assignments=4**9,
                full_solution_count=sum(len(f['full_internal_lifts']) for f in fibres),
                nonempty_fibres=sum(bool(f['full_internal_lifts']) for f in fibres),
                counts=dict(sorted(counts.items())),
                two_color_exclusion_control=witness, complete_fibres=fibres)


def independent_centers_audit():
    edges = [(0, 2), (1, 2), (0, 3), (0, 4), (0, 5),
             (1, 6), (1, 7), (1, 8)]
    fibres, witness = [], None
    for row in product(range(4), repeat=6):
        A = set(range(4)) - set(row[:3])
        B = set(range(4)) - set(row[3:])
        coherent = [(a, b, z) for a in sorted(A) for b in sorted(B) for z in range(4)
                    if z != a and z != b]
        direct = [inner for inner in product(range(4), repeat=3)
                  if all((*inner, *row)[u] != (*inner, *row)[v] for u, v in edges)]
        assert sorted(coherent) == direct
        support = sorted({inner[2] for inner in direct})
        if len(A) == len(B) == 1 and A != B and witness is None:
            witness = dict(boundary=row, A=sorted(A), B=sorted(B), z_support=support)
        fibres.append(dict(row=row, full_internal_lifts=direct))
    assert witness is not None
    return dict(vertices=list(range(9)), original_edges=edges, boundary_order=list(range(3, 9)),
                elimination_order=[0, 1, 2], complete_fibres=fibres,
                complete_original_assignments=4**9,
                full_solution_count=sum(len(f['full_internal_lifts']) for f in fibres),
                distinct_singleton_bundles_control=witness)


def perimeter_controls():
    """All nontrivial vertex subsets of one fixed triangulation, not a theorem."""
    import networkx as nx
    graph = nx.icosahedral_graph()
    planar, embedding = nx.check_planarity(graph)
    assert planar
    marked, faces = set(), []
    for u in embedding:
        for v in embedding[u]:
            if (u, v) not in marked:
                face = embedding.traverse_face(u, v, marked)
                assert len(face) == 3
                faces.append(face)
    cuts, eight = [], []
    for mask in range(1, (1 << len(graph)) - 1):
        X = {v for v in graph if mask >> v & 1}
        Y = set(graph) - X
        cut = sum((u in X) != (v in X) for u, v in graph.edges())
        if cut == 8 and min(len(X), len(Y)) >= 2:
            small = X if len(X) <= len(Y) else Y
            assert len(small) == 2
            u, v = sorted(small)
            assert graph.has_edge(u, v) and graph.degree(u) == graph.degree(v) == 5
            eight.append(sorted(small))
        if min(len(X), len(Y)) < 3:
            continue
        assert cut >= 9
        if not nx.is_connected(graph.subgraph(X)) or not nx.is_connected(graph.subgraph(Y)):
            continue
        def walk_length(side):
            # Y is in one complementary face; all other faces of T[side] are
            # actual original triangular faces, as the induced embedding shows.
            side_faces = sum(set(f) <= side for f in faces)
            edge_count = graph.subgraph(side).number_of_edges()
            return 2 * edge_count - 3 * side_faces
        bx, by = walk_length(X), walk_length(Y)
        mixed_x = sum(len(set(f) & X) == 2 for f in faces)
        mixed_y = sum(len(set(f) & X) == 1 for f in faces)
        assert bx == mixed_x and by == mixed_y and bx + by == cut
        cuts.append([sorted(X), cut, bx, by])
    return dict(networkx_version=nx.__version__,
                vertices=sorted(graph), original_edges=sorted(sorted(e) for e in graph.edges()),
                oriented_faces=faces, connected_bond_controls=len(cuts),
                minimum_cut_both_sides_at_least_three=min(c[1] for c in cuts),
                eight_cuts_small_sides=eight, connected_cut_perimeters=cuts,
                limitation='Only the fixed icosahedron; arbitrary triangulations use the paper proof.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', required=True, type=Path)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    result = dict(cut=cut_audit(), three_step=three_step_audit(),
                  independent_centers=independent_centers_audit(),
                  perimeter=perimeter_controls(),
                  scope='Necessary boundary screens and one original-edge template; no arbitrary-source existence or 4CT theorem.')
    path = args.out_dir / 'results.json'
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    sources = ['scripts/four_color_eight_cut_three_step_verification.py',
               'scripts/four_color_seven_cut_verification.py',
               'docs/four_color_seven_cut_verification.md',
               'docs/four_color_two_step_verification.md']
    receipt = dict(baseline='e1a90fea41702d7c98747716a5960198aecbecb3',
                   sources={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in sources},
                   outputs={'results.json': sha256(path.read_bytes()).hexdigest()})
    (args.out_dir / 'verification.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in result['cut'].items()
                      if k not in ('triangular_pairs', 'endpoint_map_cases')}, sort_keys=True))
    print(json.dumps({k: v for k, v in result['three_step'].items() if k != 'complete_fibres'}, sort_keys=True))


if __name__ == '__main__':
    main()
