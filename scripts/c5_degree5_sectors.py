#!/usr/bin/env python3
"""Three-spoke sector reduction: finite boundary algebra and one negative control.

The arbitrary-size sector confinement is a paper argument, not a graph search.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

from boundary_relations import normalize
from c5_cell_enumerator import REPS, T4
from c5_degree5_interfaces import brute_interface, forbidden
from c5_disk_deletions import faces_of
from c5_k4_blocks import CYCLE, Q, U, coloring

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_sectors/observations.json'
SOURCE = ROOT / 'artifacts/c5_cells/cells.json'
FULL = tuple(b for b in product(range(4), repeat=5)
             if all(b[i] != b[(i+1) % 5] for i in range(5)))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def sector_controls():
    records = []
    for spokes in combinations(range(5), 3):
        if len({Q[v] for v in spokes}) != 3:
            continue
        for i, start in enumerate(spokes):
            end = spokes[(i+1) % 3]
            arc = [start]
            while arc[-1] != end:
                arc.append((arc[-1]+1) % 5)
            missing = sorted(set(range(3)) - {Q[v] for v in arc})
            record = dict(spokes=spokes, arc=arc)
            if missing:
                record.update(reason='unused-color swap contradicts F={D}',
                              swap_colors=[missing[0], 3])
            else:
                outside = sorted(set(range(5)) - set(arc) - set(spokes))
                if outside:
                    v = outside[0]
                    lifted = list(Q)
                    lifted[v] = 3
                    assert tuple(lifted) in FULL and len(set(lifted)) == 4
                    assert all(lifted[x] == Q[x] for x in set(arc) | set(spokes))
                    record.update(reason='unchanged constraints reject a T4 row',
                                  changed_vertex=v, rejected_T4=lifted)
                else:
                    assert len(arc) == 4
                    record.update(reason='remaining pentagon sector')
            records.append(record)
    assert Counter(r['reason'] for r in records) == {
        'unused-color swap contradicts F={D}': 8,
        'unchanged constraints reject a T4 row': 2,
        'remaining pentagon sector': 2}
    remaining = [r for r in records if r['reason'] == 'remaining pentagon sector']
    assert [(r['spokes'], r['arc']) for r in remaining] == [
        ((0, 1, 4), [1, 2, 3, 4]), ((2, 3, 4), [4, 0, 1, 2])]
    # Reflection i -> 3-i fixes b4 and exchanges the two sectors (and A/B).
    reflect = lambda v: (3-v) % 5
    assert sorted(map(reflect, remaining[0]['spokes'])) == list(remaining[1]['spokes'])
    assert list(reversed(list(map(reflect, remaining[0]['arc'])))) == remaining[1]['arc']
    return records


def transfer_controls():
    options = [[dict(z_color=a, sector_pattern=REPS.index(normalize((a, *b[1:]))))
                for a in sorted(U - {b[0], b[1], b[4]})] for b in REPS]
    lifted = {b: [REPS.index(normalize((a, *b[1:])))
                  for a in sorted(U - {b[0], b[1], b[4]})] for b in FULL}
    records = []
    for bits in range(1 << len(REPS)):
        result = sum(int(any(bits >> r['sector_pattern'] & 1 for r in row)) << i
                     for i, row in enumerate(options))
        # Independently evaluate the full four-color frame before normalization.
        concrete = {b for b in FULL if bits >> REPS.index(normalize(b)) & 1}
        for b, indices in lifted.items():
            actual = any((a, *b[1:]) in concrete for a in U
                         if a not in {b[0], b[1], b[4]})
            assert actual == any(bits >> i & 1 for i in indices)
            assert actual == bool(result >> REPS.index(normalize(b)) & 1)
        if result & T4 == T4 and not (result >> REPS.index(Q) & 1):
            records.append(dict(sector_sigma=bits, outer_sigma=result))
    assert len(records) == 24
    assert len({r['outer_sigma'] for r in records}) == 12
    return dict(options=options, abstract_survivors=records,
                candidate_relations=1024, full_row_checks=1024*len(FULL))


def negative_control():
    # Reuse one stored sector witness; never regenerate the cell catalogue.
    source = json.loads(SOURCE.read_text())['cells']['831']
    assert source['k_eff'] == 2
    z = 7
    graph = nx.Graph(sorted(CYCLE))
    graph.add_edges_from((z, b) for b in (0, 1, 4))
    graph.add_edges_from((z if u == 0 else u, z if v == 0 else v)
                        for u, v in source['edges'])
    assert graph.degree(z) == 5
    assert all(graph.degree(v) == 4 for v in (5, 6))
    assert set(graph.subgraph([5, 6]).edges()) == {(5, 6)}
    rows, accepted = [], []
    for b in REPS:
        lists = {v: U - {b[w] for w in graph[v] if w < 5} for v in (5, 6)}
        tuples = brute_interface(graph.subgraph([5, 6]), lists, [5, 6])
        bans = forbidden(tuples)
        available = U - {b[w] for w in (0, 1, 4)}
        allowed = available - bans
        witness = coloring(graph, dict(enumerate(b)))
        assert bool(allowed) == (witness is not None)
        if tuple(b) == Q:
            assert bans == {2, 3}  # The C-colored z-spoke is redundant.
        accepted.append(bool(allowed))
        rows.append(dict(boundary=b, tuples=sorted(tuples), forbidden=sorted(bans),
                         z_allowed=sorted(allowed),
                         coloring=None if witness is None else [witness[v] for v in range(8)]))
    sigma = sum(int(ok) << i for i, ok in enumerate(accepted))
    assert sigma & T4 == T4
    missing = [b for b, ok in zip(REPS, accepted) if not ok]
    assert missing == [Q, (0, 1, 2, 1, 2)]
    full_checks = []
    for b in FULL:
        witness = coloring(graph, dict(enumerate(b)))
        assert (witness is not None) == bool(sigma >> REPS.index(normalize(b)) & 1)
        full_checks.append(witness is not None)
    redundant, deletions = [], []
    for e in sorted(tuple(sorted(e)) for e in graph.edges() if tuple(sorted(e)) not in CYCLE):
        child = graph.copy()
        child.remove_edge(*e)
        witness = coloring(child, dict(enumerate(Q)))
        if witness is None:
            redundant.append(e)
        deletions.append(dict(edge=e, coloring=None if witness is None else
                              [witness[v] for v in range(8)]))
    assert redundant == [(4, z)]
    # One named topology control, explicitly distinct from an exhaustive disk search.
    apex = graph.copy()
    apex.add_edges_from((8, b) for b in range(5))
    planar, embedding = nx.check_planarity(apex)
    assert planar
    rotation = [list(embedding.neighbors_cw_order(v)) for v in range(9)]
    assert {tuple(sorted((v, w))) for v, ns in enumerate(rotation) for w in ns} == {
        tuple(sorted(e)) for e in apex.edges()}
    assert len(rotation) - apex.number_of_edges() + len(faces_of(rotation)) == 2
    return dict(source_sigma=831, source_edges=source['edges'], z=z,
                edges=sorted(tuple(sorted(e)) for e in graph.edges()),
                sigma=sigma, missing_patterns=missing, patterns=rows,
                full_relation=full_checks, q_deletions=deletions,
                redundant_edges=redundant, apex_rotation=rotation)


def build():
    sectors = sector_controls()
    transfer = transfer_controls()
    control = negative_control()
    names = ('c5_degree5_sectors', 'c5_degree5_interfaces', 'c5_cell_enumerator',
             'c5_disk_deletions', 'c5_k4_blocks', 'boundary_relations', 'local_closure')
    return dict(schema=1, scope='Paper sector reduction; finite algebra; nonminimal disk control. No general exclusion.',
                source_sha256={f'scripts/{name}.py': digest(ROOT/'scripts'/f'{name}.py') for name in names},
                input_sha256={str(SOURCE.relative_to(ROOT)): digest(SOURCE)},
                pattern_order=REPS, sectors=sectors, transfer=transfer, control=control,
                summary=dict(sector_cases=len(sectors), swap_excluded=8, T4_excluded=2,
                             remaining_mirror_sectors=2, abstract_relations=1024,
                             transfer_full_rows=transfer['full_row_checks'],
                             abstract_survivors=24, abstract_output_relations=12,
                             nonminimal_disk_controls=1, control_full_rows=len(FULL)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
