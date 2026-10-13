#!/usr/bin/env python3
"""Brute-force every full lift in the eight selected flip reports and CSV."""
import csv
import gzip
from itertools import combinations, product
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
PATTERNS = ('01012', '01021', '01023', '01201', '01202',
            '01203', '01212', '01213', '01231', '01232')


def full_rows(graph):
    vertices, boundary = graph['vertices'], graph['boundary']
    inner = [v for v in vertices if v not in boundary]
    rows = []
    for pattern in PATTERNS:
        lifts = []
        for values in product(range(4), repeat=len(inner)):
            colors = dict(zip(boundary, map(int, pattern)))
            colors.update(zip(inner, values))
            if all(colors[u] != colors[v] for u, v in graph['edges']):
                lifts.append([colors[v] for v in vertices])
        rows.append({'pattern': pattern, 'count': len(lifts), 'lifts': sorted(lifts)})
    return rows


def graph_key(graph):
    k = len(graph['vertices']) - 5
    assert graph['vertices'] == list(range(5 + k)) and graph['boundary'] == list(range(5))
    frame = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
    available = [e for e in combinations(range(5 + k), 2) if e not in frame]
    edges = {tuple(e) for e in graph['edges']}
    assert frame <= edges
    return f'{k}:{sum(1 << i for i, e in enumerate(available) if e in edges)}'


def main():
    with gzip.open(BASE / 'atlas.json.gz', 'rt') as stream:
        atlas = json.load(stream)
    with (BASE / 'distances.csv').open(newline='') as stream:
        matrix = list(csv.reader(stream))
    assert matrix[0] == ['source_representative/target_relation', *map(str, atlas['mask_order'])]
    assert len(matrix) == 133
    for line, source in zip(matrix[1:], atlas['mask_order']):
        row = atlas['sources'][str(source)]['distance']
        assert line == [str(source), *(str(row[str(t)]) if row[str(t)] is not None
                                      else '>3' for t in atlas['mask_order'])]
    paths = json.loads((BASE / 'witnesses/paths.json').read_text())
    count = 0
    for path in paths:
        saved_source = atlas['sources'][str(path['source'])]
        assert saved_source['distance'][str(path['target'])] == path['distance']
        keys = saved_source['paths'][str(path['target'])]
        assert path['relations'] == [atlas['nodes'][key]['sigma'] for key in keys]
        assert len(path['full_reports']) == path['distance']
        previous = None
        for i, filename in enumerate(path['full_reports']):
            report = json.loads((BASE / 'witnesses' / filename).read_text())
            assert graph_key(report['source']['graph']) == keys[i]
            assert graph_key(report['result']['graph']) == keys[i + 1]
            for name in ('source', 'deleted', 'both_edges', 'result'):
                state = report[name]
                assert state['rows'] == full_rows(state['graph'])
                assert state['sigma'] == sum(1 << j for j, row in enumerate(state['rows']) if row['count'])
            if previous is not None:
                assert report['source']['graph'] == previous
            previous = report['result']['graph']
            assert [report['source']['sigma'], report['result']['sigma']] == path['relations'][i:i+2]
            indices = {v: j for j, v in enumerate(report['vertex_order'])}
            for joint, row in zip(report['joint_rows'], report['deleted']['rows']):
                assert joint['pattern'] == row['pattern']
                bins = {key: {'count': 0, 'lifts': []} for key in ('00', '01', '10', '11')}
                for lift in row['lifts']:
                    key = ''.join(str(int(lift[indices[u]] != lift[indices[v]]))
                                  for u, v in (report['operations']['remove'], report['operations']['add']))
                    bins[key]['lifts'].append(lift)
                    bins[key]['count'] += 1
                assert joint['fibres'] == bins
            count += 1
    print(json.dumps({'status': 'PASS', 'full_reports': count, 'complete_graph_states': 4 * count,
                      'joint_rows_including_empty_cells': 10 * count,
                      'csv_entries': 132 ** 2}, indent=2))


if __name__ == '__main__':
    main()
