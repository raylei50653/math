#!/usr/bin/env python3
"""Independent stdlib replay of the bounded C5 encoding evidence.

Brute force complete lifts, including empty rows and bins. Facial legality is
separately replayed by c5_cell_transform.py --check under networkx==3.5.
"""
from collections import Counter
import gzip
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PATTERNS = ('01012', '01021', '01023', '01201', '01202',
            '01203', '01212', '01213', '01231', '01232')
FRAME = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
A_BITS = (6, 4, 3, 1, 0)
B_BITS = (8, 2, 7, 9, 5)


def require(condition, message):
    if not condition:
        raise ValueError(message)


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


def mask(rows):
    return sum(1 << j for j, row in enumerate(rows) if row['count'])


def graph_key(graph):
    k = len(graph['vertices']) - 5
    require(graph['vertices'] == list(range(5 + k)), 'Literal vertex frame changed')
    require(graph['boundary'] == list(range(5)), 'Literal C5 frame changed')
    edges = {tuple(e) for e in graph['edges']}
    require(FRAME <= edges, 'Missing C5 frame edge')
    available = [e for e in combinations(range(5 + k), 2) if e not in FRAME]
    return f'{k}:{sum(1 << i for i, e in enumerate(available) if e in edges)}'


def encode(sigma):
    return tuple(sum(((sigma >> oldbit) & 1) << i for i, oldbit in enumerate(bits))
                 for bits in (A_BITS, B_BITS))


def decode(a, b):
    return sum(((value >> i) & 1) << oldbit
               for value, bits in ((a, A_BITS), (b, B_BITS))
               for i, oldbit in enumerate(bits))


def main():
    base = json.loads((HERE / 'BASE.json').read_text())
    for name, expected in base['sha256'].items():
        require(sha256((ROOT / name).read_bytes()).hexdigest() == expected,
                f'Input bytes changed: {name}')
    reports = {}
    for name, expected in base['reports'].items():
        report = json.loads((HERE / name).read_text())
        require(report['pattern_order'] == list(PATTERNS), f'Pattern order: {name}')
        require(graph_key(report['source']['graph']) == expected['source_graph_key'],
                f'Source graph identity: {name}')
        require(report['source']['sigma'] == expected['source_sigma'], f'Source mask: {name}')
        require(report['result']['sigma'] == expected['result_sigma'], f'Result mask: {name}')
        for label in ('source', 'deleted', 'both_edges', 'result'):
            state = report[label]
            rows = full_rows(state['graph'])
            require(state['rows'] == rows, f'Complete rows: {name}/{label}')
            require(state['sigma'] == mask(rows), f'Row mask: {name}/{label}')
        catalogue = report['catalogue']['match']['representative']
        require(catalogue['rows'] == full_rows(catalogue['graph']), f'Catalogue rows: {name}')
        require(catalogue['sigma'] == mask(catalogue['rows']) == report['result']['sigma'],
                f'Catalogue mask: {name}')
        source_edges = {tuple(e) for e in report['source']['graph']['edges']}
        removed, added = (tuple(report['operations'][key]) for key in ('remove', 'add'))
        require(removed in source_edges and added not in source_edges, f'Operation: {name}')
        for label, edges in (('deleted', source_edges - {removed}),
                             ('both_edges', source_edges | {added}),
                             ('result', (source_edges - {removed}) | {added})):
            require({tuple(e) for e in report[label]['graph']['edges']} == edges,
                    f'Edge edit: {name}/{label}')
            require(report[label]['graph']['vertices'] == report['source']['graph']['vertices']
                    and report[label]['graph']['boundary'] == report['source']['graph']['boundary'],
                    f'Fixed graph frame: {name}/{label}')
        indices = {v: j for j, v in enumerate(report['vertex_order'])}
        require(len(report['joint_rows']) == 10, f'Complete joint row count: {name}')
        for joint, row in zip(report['joint_rows'], report['deleted']['rows']):
            require(joint['pattern'] == row['pattern'], f'Joint pattern: {name}')
            bins = {key: {'count': 0, 'lifts': []} for key in ('00', '01', '10', '11')}
            for lift in row['lifts']:
                key = ''.join(str(int(lift[indices[u]] != lift[indices[v]]))
                              for u, v in (removed, added))
                bins[key]['lifts'].append(lift)
                bins[key]['count'] += 1
            require(joint['fibres'] == bins, f'Four full bins: {name}/{row["pattern"]}')
        q = tuple(sum(1 << i for i, row in enumerate(report['joint_rows'])
                      if row['fibres'][key]['count']) for key in ('00', '01', '10', '11'))
        require(q[2] | q[3] == report['source']['sigma'], f'Source projection: {name}')
        require(q[1] | q[3] == report['result']['sigma'], f'Result projection: {name}')
        packed = sum(value << (10 * i) for i, value in enumerate(q))
        require(tuple((packed >> (10 * i)) & 1023 for i in range(4)) == q,
                f'40-bit joint support packing: {name}')
        reverse = (q[0], q[2], q[1], q[3])
        require(reverse[2] | reverse[3] == report['result']['sigma']
                and reverse[1] | reverse[3] == report['source']['sigma'],
                f'Reversed operation projection: {name}')
        reports[name] = report
    collisions = []
    for names, same_counts in ((('collision-1-708.json', 'collision-1-736.json'), False),
                                (('collision-2-38030.json', 'collision-2-6734.json'), True)):
        a, b = (reports[name] for name in names)
        require(a['source']['sigma'] == b['source']['sigma'], 'Collision source masks differ')
        require(a['operations'] == b['operations'], 'Collision operations differ')
        require(a['flip']['local'] == b['flip']['local'], 'Collision local faces differ')
        require(a['source']['graph']['vertices'] == b['source']['graph']['vertices']
                and len(a['source']['graph']['edges']) == len(b['source']['graph']['edges']),
                'Collision structural stratum differs')
        require(a['source']['graph'] != b['source']['graph'], 'Collision source graphs identical')
        require(a['result']['sigma'] != b['result']['sigma'], 'Collision results identical')
        if same_counts:
            require([r['count'] for r in a['source']['rows']] ==
                    [r['count'] for r in b['source']['rows']], 'Ten source counts differ')
        collisions.append({'reports': names, 'source_sigma': a['source']['sigma'],
                           'result_sigmas': [a['result']['sigma'], b['result']['sigma']],
                           'equal_ten_counts_required': same_counts})
    for i in range(5):
        a = PATTERNS[A_BITS[i]]
        require(len(set(a)) == 3 and a.count(a[i]) == 1, f'A definition: {i}')
        b = PATTERNS[B_BITS[i]]
        require(len(set(b)) == 4 and b[(i - 1) % 5] == b[(i + 1) % 5], f'B definition: {i}')
    require(set(A_BITS + B_BITS) == set(range(10)), '5+5 partition is not bijective')
    for sigma in range(1024):
        a, b = encode(sigma)
        require(decode(a, b) == sigma, f'5+5 roundtrip: {sigma}')
        for i in range(5):
            left, right = (i - 1) % 5, (i + 1) % 5
            allowed = sum(1 << j for j, pattern in enumerate(PATTERNS)
                          if pattern[left] != pattern[right])
            clear_a = (1 << ((i - 2) % 5)) | (1 << ((i + 2) % 5))
            updated = decode(a & ~clear_a, b & ~(1 << i))
            require(updated == sigma & allowed, f'Chord clearing: mask {sigma}, chord {i}')
    require(encode(891) == (31, 25) and encode(987) == (31, 13), '891 example encoding')
    with gzip.open(ROOT / 'artifacts/c5_cell_flip_distances/atlas.json.gz', 'rt') as stream:
        atlas = json.load(stream)
    labels = []
    for sigma, source in atlas['sources'].items():
        for move in atlas['nodes'][source['start']]['moves']:
            old, new = int(sigma), atlas['nodes'][move['target']]['sigma']
            labels.append((old ^ new, old & ~new, new & ~old))
    kinds = Counter('exchange' if lost and gained else 'loss_only' if lost else
                    'gain_only' if gained else 'preserved' for _, lost, gained in labels)
    require(len(labels) == 1179, 'Initial flip count changed')
    require(len({label[0] for label in labels}) == 290, 'XOR label count changed')
    require(len({label[1:] for label in labels}) == 514, 'Directed label count changed')
    require(kinds == {'exchange': 1063, 'gain_only': 96, 'loss_only': 20}, 'Flip kind counts changed')
    print(json.dumps({'status': 'PASS', 'verification_scope':
                      'Independent exhaustive complete lifts and four bins; saved local facial data compared, facial validity separately replayed by transform --check.',
                      'input_hashes_checked': len(base['sha256']), 'full_reports': len(reports),
                      'complete_graph_states': 4 * len(reports),
                      'catalogue_representatives_checked': len(reports),
                      'joint_rows_including_empty_bins': 10 * len(reports),
                      'collisions': collisions, 'encoding_roundtrips': 1024,
                      'chord_clearing_cases': 5 * 1024,
                      'initial_flips': len(labels), 'xor_labels': 290, 'lost_gained_labels': 514,
                      'initial_flip_kinds': dict(kinds)}, indent=2))


if __name__ == '__main__':
    main()
