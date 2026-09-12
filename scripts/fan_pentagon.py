#!/usr/bin/env python3
"""Exhaustive ordered C5 + internal triangulated pentagon experiment.

Internal user labels 1..5 are graph vertices 5..9. Edges are the pentagon
and diagonals 1-3, 1-4. All 25 boundary/interior edges are optional.
No embedding order is imposed on the interior. Disk testing uses an apex
joined to all five boundary vertices. All results are computational, not
Lean topology theorems. No four-colour theorem is used.

uv run --with rustworkx==0.17.1 --with networkx==3.5 python scripts/fan_pentagon.py
"""
import argparse
from collections import Counter
import hashlib
import itertools as it
import json
from pathlib import Path
import struct
import time

import networkx as nx
import rustworkx as rx
from search_boundary import CYCLE, REPS

ROOT = Path(__file__).resolve().parents[1]
INNER_EDGES = ((5, 6), (6, 7), (7, 8), (8, 9), (5, 9), (5, 7), (5, 8))
BASE = tuple(sorted(CYCLE + INNER_EDGES))
ATT = tuple(it.product(range(5), range(5, 10)))
THREE = tuple(j for j, b in enumerate(REPS) if len(set(b)) == 3)
T3 = sum(1 << j for j in THREE)
T4 = 1023 ^ T3


def edges_of(mask):
    return BASE + tuple(e for j, e in enumerate(ATT) if mask >> j & 1)


def profile(bits):
    return sorted(next(i for i in range(5) if b.count(b[i]) == 1)
                  for j, b in enumerate(REPS) if j in THREE and bits >> j & 1)


def lists_for(mask, b):
    return [set(range(4)) - {b[u] for j, (u, v) in enumerate(ATT)
                            if v == 5 + k and mask >> j & 1} for k in range(5)]


def path_accept(lists):
    for hub in sorted(lists[0]):
        reachable = lists[1] - {hub}
        for k in range(2, 5):
            reachable = {c for c in lists[k] - {hub}
                         if any(c != d for d in reachable)}
        if reachable:
            return True
    return False


def rotation_certificate(mask):
    """Keep the apex: its boundary triangles certify the intended outer face."""
    graph = nx.Graph()
    graph.add_nodes_from(range(11))
    graph.add_edges_from(edges_of(mask) + tuple((10, i) for i in range(5)))
    ok, emb = nx.check_planarity(graph)
    assert ok
    emb.check_structure()
    return {str(v): list(emb.neighbors_cw_order(v)) for v in range(11)}


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/fan_pentagon')
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    interior = tuple(t for t in it.product(range(4), repeat=5)
                     if all(t[u - 5] != t[v - 5] for u, v in INNER_EDGES))
    assert len(interior) == 96
    compatible = tuple(tuple(sum(1 << k for k, t in enumerate(interior)
                                 if b[u] != t[v - 5]) for b in REPS)
                       for u, v in ATT)
    graph = rx.PyGraph(multigraph=False)
    graph.add_nodes_from(range(11))
    graph.add_edges_from_no_data(BASE + tuple((10, i) for i in range(5)))
    rows, rejected = [], []
    calls = 0
    started = time.monotonic()

    def visit(mask, start, surviving):
        nonlocal calls
        bits = sum(1 << j for j, choices in enumerate(surviving) if choices)
        rows.append((mask, bits))
        for e in range(start, 25):
            u, v = ATT[e]
            graph.add_edge(u, v, None)
            calls += 1
            candidate = mask | (1 << e)
            if rx.is_planar(graph):
                visit(candidate, e + 1,
                      tuple(a & b for a, b in zip(surviving, compatible[e])))
            else:
                # All supersets adding only bits above e are nonplanar.
                rejected.append(candidate)
            graph.remove_edge(u, v)
            if calls % 100000 == 0:
                print(f'calls={calls} accepted={len(rows)} rejected={len(rejected)} '
                      f'seconds={time.monotonic() - started:.1f}', flush=True)

    visit(0, 0, ((1 << len(interior)) - 1,) * len(REPS))
    rows.sort()
    rejected.sort()
    covered = len(rows) + sum(1 << (25 - m.bit_length()) for m in rejected)
    assert covered == 1 << 25
    with (out / 'disk_rows.bin').open('wb') as f:
        for mask, bits in rows:
            f.write(struct.pack('<IH', mask, bits))
    with (out / 'nonplanar_frontier.bin').open('wb') as f:
        for mask in rejected:
            f.write(struct.pack('<I', mask))
    states = {}
    counts = Counter(bits for _, bits in rows)
    for mask, bits in rows:
        if bits not in states or (mask.bit_count(), mask) < (states[bits].bit_count(), states[bits]):
            states[bits] = mask
    old_data = json.loads((ROOT / 'artifacts/automata/disk_states.json').read_text())
    assert old_data['pattern_order'] == [list(b) for b in REPS]
    old = {row['state_bits'] for row in old_data['states']}
    witnesses = []
    for bits, mask in sorted(states.items()):
        assert bits == sum(1 << j for j, b in enumerate(REPS)
                           if path_accept(lists_for(mask, b)))
        witnesses.append(dict(mask=mask, sigma_bits=bits, count=counts[bits],
                              new_vs_triangle=bits not in old,
                              three_profile=profile(bits),
                              edges=sorted(edges_of(mask)),
                              apex_rotation=rotation_certificate(mask)))
    write_json(out / 'states.json', dict(pattern_order=REPS, states=witnesses))
    summary = dict(status='computationally observed; not Lean verified',
                   grammar='ordered induced outer C5 + internal C5(5..9) with 5-7,5-8 + any attachments',
                   attachment_bit='5*u + (v-5), u=0..4, v=5..9',
                   disk_rows_format='sorted records: uint32 little-endian mask, uint16 little-endian Sigma',
                   frontier_format='sorted uint32 little-endian masks; higher bits free, lower bits fixed',
                   total_masks=1 << 25, covered_masks=covered,
                   disk_masks=len(rows), rejected_prefixes=len(rejected), planarity_calls=calls,
                   internal_colorings=len(interior), distinct_sigma=len(states),
                   triangle_sigma=len(old), new_sigma=sorted(set(states) - old),
                   missing_triangle_sigma=sorted(old - set(states)),
                   min_three_profile=min(len(profile(b)) for b in states),
                   profile_size_mask_counts=dict(sorted(Counter(len(profile(b)) for _, b in rows).items())),
                   profile_size_state_counts=dict(sorted(Counter(len(profile(b)) for b in states).items())),
                   profiles=sorted({tuple(profile(b)) for b in states}),
                   exact_T4_masks=counts[T4],
                   bad_masks=sum(n for b, n in counts.items() if b and not b & T3),
                   empty_sigma_masks=counts[0],
                   adjacent_two_profiles=all((p[1] - p[0]) % 5 in (1, 4)
                                             for b in states if len(p := profile(b)) == 2),
                   sha256={name: hashlib.sha256((out / name).read_bytes()).hexdigest()
                           for name in ('disk_rows.bin', 'nonplanar_frontier.bin', 'states.json')})
    write_json(out / 'summary.json', summary)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
