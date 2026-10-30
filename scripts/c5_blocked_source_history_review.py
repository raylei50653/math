#!/usr/bin/env python3
"""Independent transfer-word and cocycle review; no imports from homology tool."""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / 'audits/2026-10-29-kempe-realizability/history-cocycles.json'
SOURCES = ROOT / 'audits/2026-10-29-kempe-realizability/source/controls.json'
PAIRS = ((0, 3), (1, 3), (1, 2), (0, 2), (0, 3))
ALIGN = (2, 3, 1, 0)
BOUNDARY = ((0, 0, 0, 0, 0, 3), (1, 1, 1, 2, 2, 2),
            (0, 3, 3, 3, 3, 3), (2, 2, 2, 2, 0, 0), (3, 3, 1, 1, 1, 1))


def round_words():
    words = [[] for _ in range(4)]
    matrix = [[0] * 4 for _ in range(4)]
    for start in range(4):
        for choices in product((0, 1), repeat=5):
            row = [start]
            for bit, pair in zip(choices, PAIRS):
                old = row[-1]
                if bit and old not in pair:
                    break
                row.append(sum(pair) - old if bit else old)
            else:
                successor = ALIGN[row[-1]]
                words[start].append((successor, tuple(row)))
                matrix[start][successor] += 1
    return words, matrix


def all_cycles(period, words):
    answer = []
    for start in range(4):
        stack = [(start, ())]
        for _ in range(period):
            stack = [(target, history + row) for old, history in stack
                     for target, row in words[old]]
        answer.extend(history for target, history in stack if target == start)
    assert len(answer) == len(set(answer))
    return sorted(answer)


def check_cocycles():
    cert = json.loads(CERT.read_text())
    words, matrix = round_words()
    assert matrix == [[3, 2, 3, 1], [2, 1, 2, 1], [1, 1, 1, 1], [3, 2, 3, 1]]
    rows = []
    for item in cert['certificates']:
        period = item['period']
        histories = all_cycles(period, words)
        assert histories == list(map(tuple, item['histories']))
        edges = [e for e in combinations(range(len(histories)), 2)
                 if all(a != b for a, b in zip(*(histories[v] for v in e)))]
        assert edges == list(map(tuple, item['edges']))
        lookup = {edge: j for j, edge in enumerate(edges)}
        adjacent = [set() for _ in histories]
        for a, b in edges:
            adjacent[a].add(b)
            adjacent[b].add(a)
        triangles = [(a, b, c) for a, b in edges for c in adjacent[a] & adjacent[b] if c > b]
        marked = set(item['cocycle_marked_edges'])
        assert len(marked) == len(item['cocycle_marked_edges'])
        assert marked <= set(range(len(edges)))
        for a, b, c in triangles:
            assert sum(lookup[e] in marked for e in ((a, b), (a, c), (b, c))) % 2 == 0
        ids = {row: j for j, row in enumerate(histories)}
        boundary = [ids[row * period] for row in BOUNDARY]
        paired = [lookup[tuple(sorted((boundary[j], boundary[(j + 1) % 5])))] for j in range(5)]
        assert sum(e in marked for e in paired) % 2 == 1
        rows.append(dict(period=period, histories=len(histories), edges=len(edges),
                         triangles=len(triangles), cocycle_support=len(marked),
                         boundary_pairing=1))
    third_words = [(list(row), target) for entries in words for target, row in entries
                   if all(x != y and x != z for x, y, z in zip(row, BOUNDARY[3], BOUNDARY[4]))]
    assert third_words == [([0, 0, 0, 0, 2, 2], 1), ([1, 1, 3, 3, 3, 3], 0)]
    return matrix, rows, third_words


def actual_filling():
    cert = json.loads(SOURCES.read_text())['controls'][0]
    states = list(map(tuple, cert['normalized_colorings']))
    returns = {r['source']: r for r in cert['H_returns']}
    cycle = cert['H_cycles'][0]
    assert len(cycle) == 4
    histories = [() for _ in states[0]]
    for j, state_id in enumerate(cycle):
        row = returns[state_id]
        assert row['target'] == cycle[(j + 1) % 4]
        colors = [states[state_id]] + [tuple(m['coloring']) for m in row['moves']]
        q = states[state_id]
        for move in row['moves']:
            pair, vertices = tuple(move['pair']), set(move['component'])
            # Rebuild complete induced components directly from the original edges.
            active = {v for v, color in enumerate(q) if color in pair}
            queue = [move['root']]
            seen = set(queue)
            for u in queue:
                for a, b in cert['exterior_edges']:
                    v = b if a == u else a if b == u else None
                    if v is not None and v in active and v not in seen:
                        seen.add(v)
                        queue.append(v)
            assert seen == vertices
            q = tuple(sum(pair) - color if v in vertices else color for v, color in enumerate(q))
            assert q == tuple(move['coloring'])
            assert all(q[a] != q[b] for a, b in cert['exterior_edges'])
        assert tuple(ALIGN[x] for x in q) == states[row['target']]
        for v in range(len(histories)):
            histories[v] += tuple(c[v] for c in colors)
    assert histories[:5] == [h * 4 for h in BOUNDARY]
    faces = [f for f in cert['sphere_faces'] if 16 not in f]
    chain = Counter()
    for face in faces:
        h = tuple(sorted(histories[v] for v in face))
        assert len(set(h)) == 3
        assert all(all(a != b for a, b in zip(x, y)) for x, y in combinations(h, 2))
        chain[h] ^= 1
    boundary = Counter()
    for face, coefficient in chain.items():
        if coefficient:
            for e in combinations(face, 2):
                boundary[e] ^= 1
    expected = Counter()
    for j in range(5):
        expected[tuple(sorted((histories[j], histories[(j + 1) % 5])))] ^= 1
    assert {e for e, x in boundary.items() if x} == {e for e, x in expected.items() if x}
    return dict(source=cert['name'], period=4, original_faces=len(faces),
                distinct_history_vertices=len(set(histories)), filling_triangles=sum(chain.values()),
                boundary_chain_verified=True, S5=False)


if __name__ == '__main__':
    matrix, cocycles, third_words = check_cocycles()
    result = dict(status='INDEPENDENT CHECK OK', transfer_matrix=matrix,
                  cocycles=cocycles, exterior_face_third_words=third_words,
                  all_odd_periods_excluded_by_third_vertex=True,
                  actual_period4_filling=actual_filling(),
                  input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                                for p in (CERT, SOURCES)})
    print(json.dumps(result, sort_keys=True))
