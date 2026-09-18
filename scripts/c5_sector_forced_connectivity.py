#!/usr/bin/env python3
"""3903 boundary-component extraction; no graph generation or planarity oracle."""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx
from boundary_relations import normalize
from c5_sector_targets import QUERIES

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_sector_positive_control/observations.json'
OUT = ROOT / 'artifacts/c5_sector_forced_connectivity/observations.json'
PAIRS = tuple(combinations(range(4), 2))
FRAME = ((1, 2), (2, 3), (3, 4))
REJECTED = {QUERIES[6], QUERIES[7]}


def partitions(vertices):
    if not vertices:
        yield ()
        return
    x, *rest = vertices
    for p in partitions(rest):
        yield tuple(sorted(((x,),) + p))
        for j in range(len(p)):
            yield tuple(sorted(p[:j] + (tuple(sorted((x,) + p[j])),) + p[j+1:]))


def together(p, u, v):
    return any(u in b and v in b for b in p)


def swapped(row, pair, blocks):
    result = list(row)
    for block in blocks:
        for v in block:
            result[v] = pair[1] if row[v] == pair[0] else pair[0]
    return normalize(result)


def crossing(p, q):
    # Distinct connected blocks cannot interlace on a disk boundary.
    return any(a in s and c in s and b in t and d in t
               or b in s and d in s and a in t and c in t
               for s in p for t in q if s != t
               for a, b, c, d in combinations(range(5), 4))


def extract(row, pair):
    terminals = [v for v in range(5) if row[v] in pair]
    candidates, accepted, rejected = [], [], []
    for p in partitions(terminals):
        if not all(together(p, u, v) for u, v in FRAME
                   if u in terminals and v in terminals):
            continue
        candidates.append(p)
        bad = []
        for bits in product((0, 1), repeat=len(p)):
            blocks = [b for b, bit in zip(p, bits) if bit]
            target = swapped(row, pair, blocks)
            if target in REJECTED:
                bad.append(dict(blocks=blocks, rejected_row=target))
        if bad:
            rejected.append(dict(partition=p, obstruction=bad[0]))
        else:
            accepted.append(p)
    assert accepted
    # Minimal positive clauses: component(u) must hit at least one target.
    clauses = []
    for u in terminals:
        others = [v for v in terminals if v != u]
        minimal = []
        for size in range(1, len(others)+1):
            for targets in combinations(others, size):
                if any(set(t) <= set(targets) for t in minimal):
                    continue
                if all(any(together(p, u, v) for v in targets) for p in accepted):
                    minimal.append(targets)
                    if not all(any(together(p, u, v) for v in targets) for p in candidates):
                        clauses.append(dict(start=u, must_hit=targets))
    return dict(pair=pair, frame_compatible=len(candidates),
                allowed=accepted, excluded=rejected, new_minimal_clauses=clauses)


def observed_partition(graph, colors, pair):
    sub = graph.subgraph(v for v in graph if colors[v] in pair)
    return tuple(sorted(tuple(sorted(set(c) & set(range(5))))
                        for c in nx.connected_components(sub) if set(c) & set(range(5))))


def path_certificate(graph, colors):
    inner = set(graph) - set(range(5))
    for a, b, c, d in combinations(range(5), 4):
        for pair in PAIRS:
            other = tuple(v for v in range(4) if v not in pair)
            paths = []
            for u, v, palette in ((a, c, pair), (b, d, other)):
                allowed = {w for w in inner | {u, v} if colors[w] in palette}
                sub = graph.subgraph(allowed)
                if u not in sub or v not in sub or not nx.has_path(sub, u, v):
                    break
                paths.append(nx.shortest_path(sub, u, v))
            if len(paths) != 2:
                continue
            p, q = paths
            assert not set(p) & set(q) and len(p) >= 3 and len(q) >= 3
            core = graph.subgraph(inner)
            r = min((nx.shortest_path(core, x, y) for x in p[1:-1] for y in q[1:-1]),
                    key=lambda path: (len(path), path))
            x, y = r[0], r[-1]
            assert not set(r[1:-1]) & set(p + q)
            ix, iy = p.index(x), q.index(y)
            nine = [list(range(a, b+1)), list(reversed(list(range(d, 5)) + list(range(a+1)))),
                    p[:ix+1], list(reversed(range(b, c+1))), list(range(c, d+1)),
                    list(reversed(p[ix:])), list(reversed(q[:iy+1])), q[iy:], list(reversed(r))]
            closed = graph.copy()
            closed.add_edges_from([(0, 1), (0, 4)])
            left, right = [a, c, y], [b, d, x]
            used = set()
            for path, (u, v) in zip(nine, product(left, right), strict=True):
                assert (path[0], path[-1]) == (u, v)
                assert len(set(path)) == len(path)
                assert all(closed.has_edge(s, t) for s, t in zip(path, path[1:]))
                assert not set(path[1:-1]) & (set(left + right) | used)
                used.update(path[1:-1])
            return dict(pair=pair, P=p, Q=q, R=r, left=left, right=right, nine_paths=nine)
    return None


def build():
    rows = []
    for i, row in enumerate(QUERIES):
        if not (3903 >> i & 1):
            continue
        records = [extract(row, pair) for pair in PAIRS]
        # A profile is for ONE coloring only. Never combine different rows.
        profiles = list(product(*(r['allowed'] for r in records)))
        planar = [p for p in profiles
                  if all(not crossing(s, s) for s in p)
                  and all(not crossing(p[j], p[k]) for j, k in ((0, 5), (1, 4), (2, 3)))]
        assert planar  # The local abstraction alone does not exclude disk.
        rows.append(dict(index=i, row=row, pairs=records,
                         abstract_profiles=len(profiles), disk_compatible_profiles=len(planar),
                         disk_compatible_example=planar[0]))
    source = json.loads(SOURCE.read_text())
    controls = []
    for record in source['proper_hits']:
        graph = nx.Graph(record['sector_edges'])
        graph.remove_edges_from([(0, 1), (0, 4)])
        inner = sorted(set(graph) - set(range(5)))
        row_records = []
        extracted = None
        mask = 0
        for i, row in enumerate(QUERIES):
            extensions = []
            for cs in product(range(4), repeat=len(inner)):
                colors = dict(enumerate(row)) | dict(zip(inner, cs))
                if not all(colors[u] != colors[v] for u, v in graph.edges()):
                    continue
                mask |= 1 << i
                abstract = next(r for r in rows if r['index'] == i)
                profile = [observed_partition(graph, colors, pair) for pair in PAIRS]
                for p, constraints in zip(profile, abstract['pairs']):
                    assert p in constraints['allowed']
                # Save all extensions, not only a selected successful witness.
                crossings = []
                for j, k in ((0, 5), (1, 4), (2, 3)):
                    if crossing(profile[j], profile[k]):
                        crossings.append([PAIRS[j], PAIRS[k]])
                if crossings and extracted is None:
                    witness = path_certificate(graph, colors)
                    if witness is not None:
                        extracted = dict(row_index=i, internal_colors=cs, **witness)
                extensions.append(dict(internal_colors=cs, partitions=profile,
                                       complementary_crossings=crossings))
            row_records.append(dict(index=i, extensions=extensions))
        assert mask == 3903 and extracted is not None
        controls.append(dict(source_index=record['source_index'], internal_vertices=inner,
                             rows=row_records, extracted_subdivision=extracted))
    ninth = [e for c in controls for r in c['rows'] if r['index'] == 9 for e in r['extensions']]
    assert len(controls) == 22 and len(ninth) == 32
    assert not any(e['complementary_crossings'] for e in ninth)
    inputs = [SOURCE] + [ROOT / 'scripts' / (n + '.py') for n in
                        ('c5_sector_forced_connectivity', 'c5_sector_targets',
                         'boundary_relations', 'c5_cell_enumerator', 'c5_k4_blocks')]
    return dict(schema=1,
                scope='One-coloring Kempe partition necessary conditions only; seven unqueried open rows stay unknown. Fixed 22 saved graphs, no generation.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
                query_order=QUERIES, rows=rows, controls=controls,
                summary=dict(accepted_rows=len(rows), pair_cases=6*len(rows),
                             excluded_partitions=sum(len(p['excluded']) for r in rows for p in r['pairs']),
                             rows_with_disk_compatible_profiles=len(rows),
                             controls=len(controls), extracted_subdivisions=len(controls),
                             row9_extensions_without_complementary_crossing=len(ninth),
                             control_extensions=sum(len(r['extensions']) for c in controls for r in c['rows']),
                             control_extensions_with_complementary_crossing=sum(bool(e['complementary_crossings']) for c in controls for r in c['rows'] for e in r['extensions']),
                             per_row_profiles={str(r['index']): [r['abstract_profiles'], r['disk_compatible_profiles']] for r in rows}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
