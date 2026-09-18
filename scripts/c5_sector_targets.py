#!/usr/bin/env python3
"""Fixed-q sector targets, saved-witness comparisons, and a bounded inverse search.

No arbitrary-size exclusion; no claim that a Sigma representative preserves open rows.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

from boundary_relations import normalize
from c5_cell_enumerator import REPS, SINGLETON, T4
from c5_k4_blocks import CYCLE, Q, coloring

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_cells/cells.json'
OUT = ROOT / 'artifacts/c5_sector_targets/observations.json'
EXTRAS = tuple(normalize((a, *Q[1:])) for a in (1, 2))
QUERIES = REPS + EXTRAS
FULL = tuple(b for b in product(range(4), repeat=5)
             if all(b[i] != b[(i+1) % 5] for i in range(5)))
OPTIONS = tuple(tuple(sorted({QUERIES.index(normalize((a, *b[1:])))
                             for a in range(4) if a not in {b[0], b[1], b[4]}}))
                for b in REPS)
FOUR = tuple(QUERIES.index(normalize((a, *Q[1:]))) for a in range(4))
QI = REPS.index(Q)
ADJ = tuple(i for i, s in SINGLETON.items() if (s-SINGLETON[QI]) % 5 in (1, 4))


def transfer(mask):
    return sum(int(any(mask >> j & 1 for j in opts)) << i
               for i, opts in enumerate(OPTIONS))


def screen():
    opened = sorted({normalize(b) for b in product(range(4), repeat=5)
                     if all(b[i] != b[i+1] for i in (1, 2, 3))})
    used = {j for opts in OPTIONS for j in opts} | set(FOUR)
    assert len(opened) == 19 and used == set(range(12))
    survivors, targets = [], []
    for mask in range(1 << 12):
        relation = {b for b in QUERIES if mask >> QUERIES.index(b) & 1}
        # Independent set queries in the common color frame.
        direct = [any(normalize((a, *b[1:])) in relation for a in range(4)
                      if a not in {b[0], b[1], b[4]}) for b in REPS]
        outer = transfer(mask)
        assert direct == [bool(outer >> i & 1) for i in range(10)]
        accepted = [normalize((a, *Q[1:])) in relation for a in range(4)]
        if outer & T4 == T4 and not outer >> QI & 1 and accepted == [True]*3+[False]:
            survivors.append(mask)
            if any(outer == 1023-(1 << QI)-(1 << p) for p in ADJ):
                targets.append(mask)
                for b in FULL:
                    actual = any(normalize((a, *b[1:])) in relation for a in range(4)
                                 if a not in {b[0], b[1], b[4]})
                    assert actual == bool(outer >> REPS.index(normalize(b)) & 1)
    assert len(survivors)*128 == 3072 and len(targets)*128 == 640
    assert targets == [3647, 3703, 3895, 3901, 3903]
    return dict(open_rows=opened, query_order=QUERIES, unused_rows=[b for b in opened if b not in QUERIES],
                transfer_options=OPTIONS, fixed_q_indices=FOUR,
                survivors_19bit=len(survivors)*128, double_missing_19bit=len(targets)*128,
                targets=[dict(mask=m, bits_in_query_order=[m >> i & 1 for i in range(12)],
                              outer_sigma=transfer(m)) for m in targets])


def signature(graph):
    opened = graph.copy()
    opened.remove_edges_from([(0, 1), (0, 4)])
    return sum(int(coloring(opened, dict(enumerate(b))) is not None) << i
               for i, b in enumerate(QUERIES))


def brute_signature(graph):
    """Separate product enumeration of internal assignments; ignore frame edges."""
    inner = sorted(set(graph)-set(range(5)))
    edges = [(u, v) for u, v in graph.edges() if u >= 5 or v >= 5]
    result = 0
    for i, b in enumerate(QUERIES):
        for cs in product(range(4), repeat=len(inner)):
            colors = dict(enumerate(b)) | dict(zip(inner, cs))
            if all(colors[u] != colors[v] for u, v in edges):
                result |= 1 << i
                break
    return result


def diagnose(graph, targets):
    mask = signature(graph)
    assert mask == brute_signature(graph)
    return dict(edges=sorted(sorted(e) for e in graph.edges()), signature=mask,
                outer_sigma=transfer(mask), forbidden_q=[a for a, i in enumerate(FOUR) if not mask >> i & 1],
                target_differences={str(t): [i for i in range(12) if (mask ^ t) >> i & 1] for t in targets})


def eligible(graph):
    inner = sorted(set(graph)-set(range(5)))
    return (bool(inner) and nx.is_connected(graph.subgraph(inner))
            and all(graph.degree(v) == 4 for v in inner)
            and sum(v >= 5 for v in graph[0]) == 2
            and {tuple(sorted(e)) for e in graph.edges() if max(e) < 5} == CYCLE)


def disk(graph):
    apex = max(graph)+1
    augmented = graph.copy()
    augmented.add_edges_from((apex, b) for b in range(5))
    ok, embedding = nx.check_planarity(augmented)
    if not ok:
        return None
    embedding.check_structure()
    return {str(v): list(embedding.neighbors_cw_order(v)) for v in sorted(augmented)}


def corpus(targets):
    records, seen = [], set()
    cells = json.loads(SOURCE.read_text())['cells']
    for key, cell in sorted(cells.items(), key=lambda kv: int(kv[0])):
        for sign, shift in product((1, -1), range(5)):
            mapping = lambda v: (sign*v+shift) % 5 if v < 5 else v
            graph = nx.Graph(sorted(CYCLE))
            graph.add_edges_from((mapping(u), mapping(v)) for u, v in cell['edges'])
            if not eligible(graph):
                continue
            edges = tuple(sorted(tuple(sorted(e)) for e in graph.edges()))
            if edges in seen:
                continue
            seen.add(edges)
            rotation = disk(graph)
            assert rotation is not None
            records.append(dict(source_sigma=int(key), boundary_map=[mapping(v) for v in range(5)],
                                apex_rotation=rotation, **diagnose(graph, targets)))
    assert any(r['signature'] & 1023 == 831 and r['forbidden_q'] == [2, 3] for r in records)
    return dict(saved_cells=len(cells), records=records,
                signature_counts=dict(sorted(Counter(r['signature'] for r in records).items())))


def bounded_search(target):
    # Exhaustive labeled simple graphs for 1 <= |C| <= 3, with specified degrees.
    # This is a fresh small inverse search, not a rerun of the cell enumerator.
    counts, records = Counter(), []
    for k in range(1, 4):
        for field in ('degree_candidates', 'disk_candidates', 'target_hits_before_disk', 'target_disk_hits'):
            counts[f'k{k}_{field}'] = 0
        vertices = tuple(range(5, 5+k))
        possible = tuple(combinations(vertices, 2))
        for bits in range(1 << len(possible)):
            core = nx.Graph()
            core.add_nodes_from(vertices)
            core.add_edges_from(e for i, e in enumerate(possible) if bits >> i & 1)
            if not nx.is_connected(core):
                continue
            choices = [tuple(combinations(range(5), 4-core.degree(v))) for v in vertices]
            for attachments in product(*choices):
                if sum(0 in a for a in attachments) != 2:
                    continue
                graph = nx.Graph(sorted(CYCLE))
                graph.add_edges_from(core.edges())
                graph.add_edges_from((v, b) for v, a in zip(vertices, attachments) for b in a)
                assert eligible(graph)
                counts[f'k{k}_degree_candidates'] += 1
                # Target constraints first. No planarity oracle is used to color.
                mask = signature(graph)
                assert mask == brute_signature(graph)
                counts[f'k{k}_target_hits_before_disk'] += int(mask == target)
                rotation = disk(graph)
                if rotation is not None:
                    counts[f'k{k}_disk_candidates'] += 1
                    counts[f'k{k}_target_disk_hits'] += int(mask == target)
                    records.append(dict(k=k, apex_rotation=rotation, **diagnose(graph, [target])))
    double = [r for r in records if any(r['outer_sigma'] == 1023-(1 << QI)-(1 << p) for p in ADJ)]
    assert len(double) == 2 and all(r['signature'] == 1855 and r['forbidden_q'] == [2, 3] for r in double)
    return dict(target=target, max_internal_vertices=3, counts=dict(sorted(counts.items())),
                adjacent_double_missing_disk_records=double, disk_records=records)


def build():
    abstract = screen()
    targets = [t['mask'] for t in abstract['targets']]
    saved = corpus(targets)
    search = bounded_search(targets[0])
    # The actual named nonminimal control, with full original rows and deletions.
    graph = nx.Graph(sorted(CYCLE))
    graph.add_edges_from([(7, 0), (7, 1), (7, 4), (7, 5), (7, 6),
                          (5, 2), (5, 3), (6, 1), (6, 2), (5, 6)])
    missing = [b for b in FULL if coloring(graph, dict(enumerate(b))) is None]
    assert {normalize(b) for b in missing} == {Q, (0, 1, 2, 1, 2)}
    redundant = []
    for e in sorted(tuple(sorted(e)) for e in graph.edges() if tuple(sorted(e)) not in CYCLE):
        child = graph.copy()
        child.remove_edge(*e)
        if coloring(child, dict(enumerate(Q))) is None:
            redundant.append(e)
    assert redundant == [(4, 7)]
    inputs = [SOURCE] + [ROOT/'scripts'/f'{name}.py' for name in
              ('c5_sector_targets', 'boundary_relations', 'c5_cell_enumerator', 'c5_k4_blocks')]
    return dict(schema=1, scope='Fixed-q abstract screen, saved graph controls, exhaustive |C|<=3 inverse search. No general exclusion or Lean theorem.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
                abstract=abstract, corpus=saved, inverse_search=search,
                negative_control=dict(full_rows_checked=len(FULL), redundant_edges=redundant),
                summary=dict(targets=targets, saved_eligible_graphs=len(saved['records']),
                             saved_target_hits=sum(r['signature'] in targets for r in saved['records']),
                             inverse_counts=search['counts']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
