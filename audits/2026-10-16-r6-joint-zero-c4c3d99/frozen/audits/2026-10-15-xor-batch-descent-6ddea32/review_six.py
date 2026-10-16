#!/usr/bin/env python3
"""Independent six-pin arithmetic and full-colouring replay; read-only target."""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / '2026-10-15-six-pin-lifts-6ddea32'


def proper_rows(vertices, edges):
    adjacent = {v: set() for v in vertices}
    for a, b in edges:
        adjacent[a].add(b); adjacent[b].add(a)
    order = sorted(vertices, key=lambda v: (-len(adjacent[v]), v))
    current, output = {}, []
    def rec(i):
        if i == len(order):
            output.append([current[v] for v in vertices]); return
        v = order[i]
        for colour in range(4):
            if all(current.get(w) != colour for w in adjacent[v]):
                current[v] = colour; rec(i + 1); del current[v]
    rec(0)
    return sorted(output)


def abstract():
    proper, hits = [], []
    for row in itertools.product(range(4), repeat=6):
        m, v, w, z, p, q = row
        if len({m, v, w}) != 3 or len({z, p, q}) != 3 or m == z:
            continue
        proper.append(row)
        event = not ({p, q} & {v, w})
        assert event == ((v ^ w) == (p ^ q) != (m ^ z))
        if event: hits.append(row)
    assert len(proper) == 432 and len(hits) == 96
    cases = []
    for values in itertools.product((1, 2, 3), repeat=3):
        if values[0] == values[1] != values[2]: continue
        for pair in itertools.combinations((1, 2, 3), 2):
            active = [i for i, x in enumerate(values) if x in pair]
            partitions = set()
            for labels in itertools.product(range(len(active)), repeat=len(active)):
                names, canonical = {}, []
                for label in labels:
                    if label not in names: names[label] = len(names)
                    canonical.append(names[label])
                partitions.add(tuple(canonical))
            for labels in sorted(partitions):
                part = [None] * 3
                for i, label in zip(active, labels): part[i] = label
                returns, single = [], []
                for bits in range(1 << (max(labels, default=-1) + 1)):
                    after = [pair[1] if x == pair[0] else pair[0]
                             if x == pair[1] else x
                             for x in values]
                    after = [after[i] if part[i] is not None and bits & (1 << part[i]) else x
                             for i, x in enumerate(values)]
                    if after[0] == after[1] != after[2]:
                        returns.append(bits)
                        if bits and not bits & (bits - 1): single.append(bits)
                assert bool(returns) == bool(single)
                cases.append({'values': list(values), 'pair': list(pair), 'partition': part,
                              'E_masks': returns, 'single_cycle_E_masks': single,
                              'safe': not returns})
    assert len(cases) == 165
    return cases


def main():
    data = json.loads((TARGET / 'certificate.json').read_text())
    expected = abstract()
    assert expected == data['abstract_cubes']
    controls = []
    for g in data['controls']:
        rows = proper_rows(g['vertices'], g['edges'])
        assert rows == g['all_full_J_colourings']
        ps = g['pins']; pi = {v: i for i, v in enumerate(g['vertices'])}
        event_count = sum(not ({r[pi[ps['p']]], r[pi[ps['q']]]} &
                              {r[pi[ps['v']]], r[pi[ps['w']]]}) for r in rows)
        assert event_count == g['E_count']
        u = g['U']; urows = proper_rows(u['vertices'], u['edges'])
        assert urows == u['all_full_colourings']
        ui = {v: i for i, v in enumerate(u['vertices'])}
        assert len(urows) == len(u['all_r_lifts_including_empties'])
        empty = 0
        for row, saved in zip(urows, u['all_r_lifts_including_empties']):
            actual = sorted(set(range(4)) - {row[ui[u['pins'][x]]] for x in 'svwt'})
            assert saved == {'full_U_colouring': row, 'all_r_lifts': actual}
            empty += not actual
        controls.append({'name': g['name'], 'J_rows': len(rows), 'E_rows': event_count,
                         'U_rows': len(urows), 'empty_r_lifts': empty})
    print(json.dumps({'status': 'PASS', 'proper_six_rows': 432, 'E_six_rows': 96,
                      'abstract_partition_cases': len(expected), 'controls': controls,
                      'target_certificate_sha256': hashlib.sha256((TARGET / 'certificate.json').read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == '__main__': main()
