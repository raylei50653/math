#!/usr/bin/env python3
"""Check graph/incidence/attachment correspondence; no DFS or planarity calls.

uv run --with rustworkx==0.17.1 python scripts/c5_graph_bridge_check.py --check
This is an independent Python replay, not Lean extraction.
"""
import argparse
import hashlib
import json
from pathlib import Path

import c5_cell_reduced as R

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'artifacts/c5_cells/graph_bridge_check.json'


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def start(m):
    return 5 + 5 * m + m * (m - 1) // 2


def index(u, v):
    require(u != v and max(u, v) >= 5, 'not an interior edge')
    return start(max(u, v) - 5) + min(u, v)


def verify_layout(k, edges, touch):
    expected = {(u, v) for v in range(5, 5 + k) for u in range(v)}
    require(set(edges[5:]) == expected, 'edge universe mismatch')
    require(len(edges) == start(k), 'universe size mismatch')
    for e, (u, v) in enumerate(edges[5:], 5):
        require(index(u, v) == e == index(v, u), 'edge index mismatch')
    for m in range(k):
        incident = {index(5 + m, v) for v in range(5 + k) if v != 5 + m}
        require(len(incident) == 4 + k, 'incident map not bijective')
        require(incident == touch[m], 'touch mismatch')


def check_k(k):
    R._setup(k)
    edges = R._W['edges']
    touch = [{e for e in range(len(edges)) if row >> e & 1} for row in R._W['touch']]
    verify_layout(k, edges, touch)
    observations = 0
    for mask in range(1 << len(edges)):
        neighbors = [set() for _ in range(5 + k)]
        for u, v in R.C.CYCLE:
            neighbors[u].add(v)
            neighbors[v].add(u)
        for e, (u, v) in enumerate(edges):
            if mask >> e & 1:
                neighbors[u].add(v)
                neighbors[v].add(u)
        encoded = {index(u, v) for v in range(5, 5 + k) for u in neighbors[v] if u < v}
        require(encoded == {e for e in range(5, len(edges)) if mask >> e & 1},
                'graph encoding round trip failed')
        for m in range(k):
            x = 5 + m
            graph_degree = len(neighbors[x])
            graph_att = sum(2 ** i for i in range(5) if i in neighbors[x])
            require(graph_degree == len(encoded & touch[m]) ==
                    (mask & R._W['touch'][m]).bit_count(), 'degree bridge mismatch')
            require(graph_att == sum(2 ** i for i in range(5) if start(m) + i in encoded)
                    == R.att_value(mask, m), 'attachment bridge mismatch')
            observations += 1
    return dict(k=k, full_graphs=1 << len(edges), vertex_observations=observations,
                round_trip_mismatches=0, degree_mismatches=0, attachment_mismatches=0)


def negative_controls():
    edges, _ = R.block_edge_order(2)
    touch = [{e for e, pair in enumerate(edges) if 5 + m in pair} for m in range(2)]
    bad_edges = list(edges)
    bad_edges[5], bad_edges[6] = bad_edges[6], bad_edges[5]
    bad_touch = [row.copy() for row in touch]
    bad_touch[0].remove(index(5, 6))
    for es, ts, message in [(bad_edges, touch, 'edge index mismatch'),
                            (edges, bad_touch, 'touch mismatch')]:
        try:
            verify_layout(2, es, ts)
        except AssertionError as error:
            require(str(error) == message, 'wrong negative-control failure')
        else:
            raise AssertionError('mutation accepted')
    return dict(swapped_attachment_bits_rejected=True, missing_later_incidence_rejected=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    paths = ['scripts/c5_graph_bridge_check.py', 'scripts/c5_cell_reduced.py',
             'scripts/c5_cell_enumerator.py', 'Math/ReducedGraphBridge.lean',
             'Math/ReducedViable.lean', 'Math/SymNormalForm.lean', 'artifacts/c5_cells/cells.json']
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
    for k in range(13):
        edges, _ = R.block_edge_order(k)
        touch = [{e for e, pair in enumerate(edges) if 5 + m in pair} for m in range(k)]
        verify_layout(k, edges, touch)
    report = dict(scope='all graphs k<=2, all chord choices; layout only k<=12; no planarity or DFS',
                  source_sha256=hashes, negative_controls=negative_controls(), cases=[])
    for k in range(3):
        row = check_k(k)
        report['cases'].append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
    require(all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h for p, h in hashes.items()),
            'source changed during audit')
    payload = json.dumps(report, sort_keys=True, indent=2) + '\n'
    if args.check:
        require(REPORT.read_text() == payload, 'report replay differs')
        print('graph bridge replay: PASS')
    else:
        REPORT.write_text(payload)
        print(f'wrote {REPORT}')


if __name__ == '__main__':
    main()
