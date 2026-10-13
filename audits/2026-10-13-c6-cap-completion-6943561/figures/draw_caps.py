#!/usr/bin/env python3
"""Named three-cap diagram; harmonic disk embedding, all 27 edges shown."""
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def cap(kind, chords, runs):
    m = len(runs)
    edges = {tuple(sorted((i, (i + 1) % 6))) for i in range(6)}
    edges.update(tuple(sorted((6 + i, 6 + (i + 1) % m))) for i in range(m))
    edges.update(tuple(sorted((6 + a, 6 + b))) for a, b in chords)
    if m == 5:
        edges.update((6 + i, 11) for i in range(5))
    offset = 0
    for i, run in enumerate(runs):
        edges.update(tuple(sorted(((offset + j) % 6, 6 + i))) for j in range(run + 1))
        offset += run
    assert offset == 6 and len(edges) == 27
    return {'id': kind, 'edges': sorted(edges), 'outer_runs': runs}


def layout(edges):
    pos = np.zeros((12, 2))
    for i in range(6):
        theta = -math.pi / 2 + i * math.pi / 3
        pos[i] = (math.cos(theta), math.sin(theta))
    matrix, rhs = np.zeros((6, 6)), np.zeros((6, 2))
    for i in range(6, 12):
        neighbors = [b if a == i else a for a, b in edges if i in (a, b)]
        matrix[i - 6, i - 6] = len(neighbors)
        for j in neighbors:
            if j >= 6:
                matrix[i - 6, j - 6] -= 1
            else:
                rhs[i - 6] += pos[j]
    pos[6:] = np.linalg.solve(matrix, rhs)
    def turn(a, b, c):
        u, v = pos[b] - pos[a], pos[c] - pos[a]
        return u[0] * v[1] - u[1] * v[0]
    for a, b in edges:
        for c, d in edges:
            if len({a, b, c, d}) == 4:
                assert not (turn(a, b, c) * turn(a, b, d) < -1e-12 and
                            turn(c, d, a) * turn(c, d, b) < -1e-12)
    return pos


def main():
    caps = [cap('A: central triangle', [(0, 2), (2, 4), (4, 0)], [0, 2, 0, 2, 0, 2]),
            cap('B: path of triangles', [(0, 2), (0, 3), (3, 5)], [0, 2, 1, 0, 2, 1]),
            cap('W: unique deep center', [], [2, 1, 1, 1, 1])]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1380" height="520" viewBox="0 0 1380 520">',
             '<rect width="1380" height="520" fill="#fff"/>',
             '<style>text{font-family:Arial,sans-serif;fill:#172b4d} .title{font-size:20px;font-weight:bold} .note{font-size:15px} .node{font-size:12px;font-weight:bold;fill:white;text-anchor:middle;dominant-baseline:central}</style>']
    for index, graph in enumerate(caps):
        edges = graph['edges']
        pos = layout(edges) * 175 + np.array([230 + 460 * index, 250])
        parts.append(f'<text class="title" x="{460 * index + 35}" y="35">{graph["id"]}</text>')
        for a, b in edges:
            color = '#b76a17' if a >= 6 else '#8493a5'
            width = 2.8 if a >= 6 or b < 6 else 1.7
            parts.append(f'<line x1="{pos[a,0]:.4f}" y1="{pos[a,1]:.4f}" x2="{pos[b,0]:.4f}" y2="{pos[b,1]:.4f}" stroke="{color}" stroke-width="{width}"/>')
        for i, (x, y) in enumerate(pos):
            color = '#245d8f' if i < 6 else '#a85212'
            if index == 2 and i == 11:
                color = '#a82e4d'
            name = f'b{i}' if i < 6 else f'x{i-6}'
            parts.append(f'<circle cx="{x:.4f}" cy="{y:.4f}" r="12" fill="{color}"/><text class="node" x="{x:.4f}" y="{y:.4f}">{name}</text>')
        degree = [sum(i in e for e in edges) for i in range(12)]
        graph['boundary_degrees'], graph['private_degrees'] = degree[:6], degree[6:]
        assert min(degree[6:]) >= 5
        parts.append(f'<text class="note" x="{460 * index + 35}" y="465">Boundary degrees: {", ".join(map(str,degree[:6]))}</text>')
        parts.append(f'<text class="note" x="{460 * index + 35}" y="493">Private degrees: {", ".join(map(str,degree[6:]))}</text>')
    parts.append('</svg>')
    (HERE / 'three_caps.svg').write_text('\n'.join(parts) + '\n')
    (HERE / 'named_caps.json').write_text(json.dumps(caps, indent=2) + '\n')
    print('Three diagrams: 27 edges each; private minimum degree 5; no crossings.')


if __name__ == '__main__':
    main()
