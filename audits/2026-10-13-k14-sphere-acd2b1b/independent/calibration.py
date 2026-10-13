#!/usr/bin/env python3
"""Independent tiny full-relation controls with actual empty fibres."""
import importlib.util
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


main = module('primary', HERE / 'check.py')
other = module('independent', HERE / 'frozen/audits/2026-10-13-k13-collar-50d5474/independent/check.py')
ring = [(i, (i + 1) % 5) for i in range(5)]
fixtures = [('C5', 5, ring), ('W5', 6, ring + [(i, 5) for i in range(5)]),
            ('C5_chord02', 5, ring + [(0, 2)])]
results = []
for name, n, edges in fixtures:
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    counts = []
    for word in main.WORDS:
        expected = []
        for tail in itertools.product('0123', repeat=n - 5):
            coloring = word + ''.join(tail)
            if all(coloring[u] != coloring[v] for u, v in edges):
                expected.append(coloring)
        actual = main.lifts(adjacency, word)
        second, _ = other.colourings(dict(enumerate(adjacency)), list(range(5)), word)
        assert actual == second == expected, (name, word)
        counts.append(len(expected))
    results.append(dict(name=name, counts=counts, empty_fibres=counts.count(0),
                        target_source='not triggered'))
assert results[1]['empty_fibres'] == 5
assert results[2]['empty_fibres'] > 0
print(json.dumps({'full_fibre_controls': results, 'status': 'triggered and holds'}, sort_keys=True))
