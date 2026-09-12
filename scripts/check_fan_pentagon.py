#!/usr/bin/env python3
"""Independent full replay; does not import the search or its bitset update.

Recomputes patterns and all 4^5 interior assignments, checks every recorded
Sigma, checks every accepted mask and every rejected prefix with NetworkX,
and verifies that disjoint prefix intervals cover all 2^25 attachment masks.
Stored witness rotations and all 240 labelled boundary colourings are replayed.

uv run --with numpy==2.4.3 --with networkx==3.5 python scripts/check_fan_pentagon.py
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
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'artifacts/fan_pentagon')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    folder = args.input
    summary = json.loads((folder / 'summary.json').read_text())
    for name, digest in summary['sha256'].items():
        assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == digest, name
    rows = list(struct.iter_unpack('<IH', (folder / 'disk_rows.bin').read_bytes()))
    rejects = [m for m, in struct.iter_unpack('<I', (folder / 'nonplanar_frontier.bin').read_bytes())]
    masks = np.array([m for m, _ in rows], dtype=np.uint32)
    expected = np.array([b for _, b in rows], dtype=np.uint16)
    assert rows == sorted(set(rows)) and len(set(map(int, masks))) == len(rows)
    assert rejects == sorted(set(rejects))
    assert all(0 <= m < 1 << 25 and 0 <= b < 1024 for m, b in rows)
    assert all(0 < m < 1 << 25 for m in rejects)

    def reverse25(mask):
        return int(f'{mask:025b}'[::-1], 2)

    intervals = [(reverse25(m), 1) for m, _ in rows]
    intervals.extend((reverse25(m), 1 << (25 - m.bit_length())) for m in rejects)
    cursor = 0
    for start, length in sorted(intervals):
        assert start == cursor, ('coverage gap or overlap', start, cursor)
        cursor += length
    assert cursor == 1 << 25
    del intervals
    print('disjoint prefix coverage: all 33,554,432 masks', flush=True)

    outer = [(i, (i + 1) % 5) for i in range(5)]
    inner = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (0, 3)]
    base = outer + [(u + 5, v + 5) for u, v in inner]
    assignments = list(it.product(range(4), repeat=5))
    boundary = [b for b in assignments if all(b[u] != b[v] for u, v in outer)]

    def normalize(b):
        seen = []
        for c in b:
            if c not in seen:
                seen.append(c)
        return tuple(seen.index(c) for c in b)

    reps = sorted({normalize(b) for b in boundary})
    interior = [c for c in assignments if all(c[u] != c[v] for u, v in inner)]
    assert len(boundary) == 240 and len(interior) == 96
    witness_data = json.loads((folder / 'states.json').read_text())
    assert witness_data['pattern_order'] == [list(b) for b in reps]

    def forbidden_masks(b):
        return np.array([sum(1 << (5 * u + v) for u in range(5) for v in range(5)
                             if b[u] == c[v]) for c in interior], dtype=np.uint32)

    actual = np.zeros(len(rows), dtype=np.uint16)
    for j, b in enumerate(reps):
        forbidden = forbidden_masks(b)
        for start in range(0, len(rows), 4096):
            chunk = masks[start:start + 4096]
            accept = np.any((chunk[:, None] & forbidden[None, :]) == 0, axis=1)
            actual[start:start + len(chunk)] |= accept.astype(np.uint16) << j
    assert np.array_equal(actual, expected)
    print(f'all {len(rows)} exact Sigma values replayed by explicit interior assignments', flush=True)

    counts = Counter(map(int, actual))
    states = {r['sigma_bits']: r for r in witness_data['states']}
    assert len(states) == len(witness_data['states']) and set(states) == set(counts)
    minima = {}
    for m, b in rows:
        if b not in minima or (m.bit_count(), m) < (minima[b].bit_count(), minima[b]):
            minima[b] = m
    old_data = json.loads((ROOT / 'artifacts/automata/disk_states.json').read_text())
    old = {r['state_bits'] for r in old_data['states']}
    three = [j for j, b in enumerate(reps) if len(set(b)) == 3]
    t3 = sum(1 << j for j in three)

    def profile(bits):
        return sorted(next(i for i, c in enumerate(b) if b.count(c) == 1)
                      for j, b in enumerate(reps) if j in three and bits >> j & 1)

    for bits, r in states.items():
        m = r['mask']
        assert m == minima[bits] and r['count'] == counts[bits]
        assert r['three_profile'] == profile(bits) and r['new_vs_triangle'] == (bits not in old)
        edges = base + [(u, v + 5) for u in range(5) for v in range(5) if m >> (5 * u + v) & 1]
        assert r['edges'] == [list(e) for e in sorted(tuple(sorted(e)) for e in edges)]
        emb = nx.PlanarEmbedding()
        emb.set_data({int(v): ns for v, ns in r['apex_rotation'].items()})
        emb.check_structure()
        required = {frozenset(e) for e in edges + [(10, i) for i in range(5)]}
        assert set(emb.nodes) == set(range(11))
        assert {frozenset(e) for e in emb.edges} == required
        # Delete apex in the supplied rotation, then verify C5 is facial.
        disk = nx.PlanarEmbedding()
        disk.set_data({v: [u for u in emb.neighbors_cw_order(v) if u != 10] for v in range(10)})
        disk.check_structure()
        cycle_darts = {(i, (i + 1) % 5) for i in range(5)}
        face = disk.traverse_face(0, 1)
        face_rev = disk.traverse_face(1, 0)
        assert (set(zip(face, face[1:] + face[:1])) == cycle_darts or
                set(zip(face_rev, face_rev[1:] + face_rev[:1])) == {(v, u) for u, v in cycle_darts})
        for b in boundary:
            accept = bool(np.any((np.uint32(m) & forbidden_masks(b)) == 0))
            assert accept == bool(bits >> reps.index(normalize(b)) & 1), (m, b)
    print(f'{len(states)} witness rotations and 240 labelled colourings per witness checked', flush=True)

    checks = dict(total_masks=1 << 25, covered_masks=cursor, disk_masks=len(rows),
                  rejected_prefixes=len(rejects), planarity_calls=len(rows) + len(rejects) - 1,
                  distinct_sigma=len(states), triangle_sigma=len(old),
                  internal_colorings=len(interior),
                  new_sigma=sorted(set(states) - old), missing_triangle_sigma=sorted(old - set(states)),
                  min_three_profile=min(map(lambda b: len(profile(b)), states)),
                  profile_size_mask_counts=dict(sorted(Counter({str(k): sum(n for b, n in counts.items()
                      if len(profile(b)) == k) for k in range(6) if any(len(profile(b)) == k for b in counts)}).items())),
                  profile_size_state_counts=dict(sorted(Counter(str(len(profile(b))) for b in states).items())),
                  profiles=[list(p) for p in sorted({tuple(profile(b)) for b in states})],
                  exact_T4_masks=counts[1023 ^ t3],
                  bad_masks=sum(n for b, n in counts.items() if b and not b & t3),
                  empty_sigma_masks=counts[0],
                  adjacent_two_profiles=all((p[1] - p[0]) in (1, 4)
                                            for b in states if len(p := profile(b)) == 2))
    for key, value in checks.items():
        assert summary[key] == value, (key, summary[key], value)

    graph = nx.Graph()
    graph.add_nodes_from(range(11))
    graph.add_edges_from(base + [(10, i) for i in range(5)])
    start_time = time.monotonic()
    for kind, entries in (('disk', [(m, True) for m, _ in rows]),
                          ('frontier', [(m, False) for m in rejects])):
        for idx, (mask, planar) in enumerate(entries, 1):
            extra = [(u, v + 5) for u in range(5) for v in range(5) if mask >> (5 * u + v) & 1]
            graph.add_edges_from(extra)
            assert nx.check_planarity(graph)[0] == planar, (kind, mask)
            graph.remove_edges_from(extra)
            if idx % 25000 == 0:
                print(f'{kind} {idx}/{len(entries)} elapsed={time.monotonic() - start_time:.1f}s', flush=True)
    report = dict(status='PASS; computational replay, not a Lean topology proof',
                  coverage='disjoint intervals cover all 2^25 masks',
                  checked_disk_masks=len(rows), checked_nonplanar_prefixes=len(rejects),
                  checked_sigma_masks=len(rows), checked_full_coloring_witnesses=len(states),
                  checked_rotation_witnesses=len(states),
                  numpy_version=np.__version__, networkx_version=nx.__version__,
                  input_sha256={name: hashlib.sha256((folder / name).read_bytes()).hexdigest()
                                for name in ('summary.json', 'disk_rows.bin', 'nonplanar_frontier.bin', 'states.json')})
    destination = args.report or folder / 'replay.json'
    destination.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
