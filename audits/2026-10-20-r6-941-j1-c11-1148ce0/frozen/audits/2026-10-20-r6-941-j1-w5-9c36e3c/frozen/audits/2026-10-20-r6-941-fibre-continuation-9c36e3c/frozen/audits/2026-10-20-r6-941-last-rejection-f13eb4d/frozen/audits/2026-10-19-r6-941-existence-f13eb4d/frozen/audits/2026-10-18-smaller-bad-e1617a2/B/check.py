#!/usr/bin/env python3
"""Replay two specified quotients of one frozen graph, with every old lift."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = 'e1617a2756813327d7ad333cfdd0fd92fa9efc38'
OUTER = tuple('xyabc')
DELETED = {'p', 'h'}


def edge(u, v):
    return tuple(sorted((u, v)))


def proper(assignment, edges):
    return all(assignment[u] != assignment[v] for u, v in edges)


def enumerate_fibres(vertices, edges, rows):
    previous = {v: [] for v in vertices}
    positions = {v: i for i, v in enumerate(vertices)}
    for u, v in edges:
        if positions[u] > positions[v]:
            u, v = v, u
        previous[v].append(u)
    fibres = {}
    for row in rows:
        current = dict(zip(OUTER, map(int, row)))
        found = []

        def visit(index):
            if index == len(vertices):
                found.append([current[v] for v in vertices])
                return
            vertex = vertices[index]
            for colour in range(4):
                if all(current[neighbour] != colour
                       for neighbour in previous[vertex]):
                    current[vertex] = colour
                    visit(index + 1)
                    del current[vertex]

        assert proper(current, [e for e in edges if set(e) <= set(OUTER)])
        visit(len(OUTER))
        fibres[row] = sorted(found)
    return fibres


def build():
    manifest = json.loads((ROOT / 'INPUTS.json').read_text())
    assert manifest['base'] == BASE
    for entry in manifest['files']:
        content = (ROOT / 'frozen' / entry['path']).read_bytes()
        assert len(content) == entry['bytes']
        assert hashlib.sha256(content).hexdigest() == entry['sha256']
    original = json.loads((ROOT / 'frozen/audits/'
        '2026-10-18-smaller-source-9f1fe84/C/certificate.json').read_text())
    catalogue_path = ROOT.parent / 'frozen/artifacts/c5_cells/cells.json'
    catalogue_content = catalogue_path.read_bytes()
    parent_manifest = json.loads((ROOT.parent / 'INPUTS.json').read_text())
    catalogue_entry = next(e for e in parent_manifest['files']
                           if e['path'] == 'artifacts/c5_cells/cells.json')
    assert hashlib.sha256(catalogue_content).hexdigest() == catalogue_entry['sha256']
    catalogue = json.loads(catalogue_content)
    masks = {int(mask) for mask in catalogue['cells']}
    rows = [''.join(map(str, row)) for row in catalogue['pattern_order']]
    assert len(rows) == 10
    old_vertices = tuple(original['whole_graph_control']['G']['vertices'])
    # Rebuild edges from the oriented original faces independently of its edge list.
    faces = original['whole_graph_oriented_faces']
    old_edges = {edge(face[i], face[(i + 1) % 3])
                 for face in faces for i in range(3)}
    assert old_edges == set(map(tuple, original['whole_graph_control']['G']['edges']))
    old_fibres = enumerate_fibres(old_vertices, old_edges, rows)
    old_counts = [len(old_fibres[row]) for row in rows]
    assert old_counts == original['whole_graph_control']['G']['counts']
    surviving = tuple(v for v in old_vertices if v not in DELETED)
    reduced_edges = {e for e in old_edges if not (set(e) & DELETED)}
    result = {'base': BASE, 'rows': rows,
              'source_target': 'not-triggered',
              'original': {'vertices': list(old_vertices),
                           'edges': [list(e) for e in sorted(old_edges)],
                           'inner_vertices': len(old_vertices) - 5,
                           'full_fibres': old_fibres, 'counts': old_counts},
              'graphs': {}, 'negative_controls': {}}
    for name, changes, free_pin in (
            ('Q1', {'n': 'b', 'R': 'q'}, 'L'),
            ('Q2', {'n': 'b', 'L': 'b'}, 'R')):
        quotient = {v: changes.get(v, v) for v in surviving}
        vertices = tuple(dict.fromkeys(quotient[v] for v in surviving))
        assert vertices[:5] == OUTER
        assert all(quotient[u] != quotient[v] for u, v in reduced_edges)
        edges = {edge(quotient[u], quotient[v]) for u, v in reduced_edges}
        assert len(old_vertices) - len(vertices) == 4
        assert len(old_vertices) - 5 == 7 and len(vertices) - 5 == 3
        full_fibres = enumerate_fibres(vertices, edges, rows)
        counts = [len(full_fibres[row]) for row in rows]
        mask = sum(1 << i for i, count in enumerate(counts) if count)
        assert mask in masks, 'This fixed completed control must not be called bad'
        records = {}
        for row in rows:
            records[row] = []
            for values in full_fibres[row]:
                chi = dict(zip(vertices, values))
                pullback = {v: chi[quotient[v]] for v in surviving}
                assert proper(pullback, reduced_edges)
                actual = []
                for p, h in itertools.product(range(4), repeat=2):
                    lifted = dict(pullback, p=p, h=h)
                    if proper(lifted, old_edges):
                        actual.append([p, h])
                        assert [lifted[v] for v in old_vertices] in old_fibres[row]
                expected = [[p, h] for p, h in itertools.product(range(4), repeat=2)
                            if p not in {pullback[v] for v in ('a', 'b', 'q')}
                            and h not in {pullback['b'], pullback['q'],
                                          pullback[free_pin], p}]
                assert actual == expected
                nonempty = (pullback['L'] != pullback['a'] if name == 'Q1'
                            else pullback['a'] == pullback['q']
                            or pullback['R'] != pullback['a'])
                assert bool(actual) == nonempty
                records[row].append({'colouring': values,
                                     'pullback': [pullback[v] for v in surviving],
                                     'all_old_lifts': actual})
        # Explicit complete failed-lifting control from paper section 9.
        chosen = dict(zip(OUTER, map(int, '01202')), q=1, r=3)
        chosen[free_pin] = 2
        assert proper(chosen, edges)
        negative = next(rec for rec in records['01202']
                        if rec['colouring'] == [chosen[v] for v in vertices])
        assert negative['all_old_lifts'] == []
        result['negative_controls'][name + '_unconditional_old_lift'] = negative
        if name == 'Q2':
            equal_case = next(rec for row_records in records.values() for rec in row_records
                             if dict(zip(surviving, rec['pullback']))['a']
                             == dict(zip(surviving, rec['pullback']))['q']
                             == dict(zip(surviving, rec['pullback']))['R'])
            assert equal_case['all_old_lifts']
            result['negative_controls']['Q2_omitted_a_equals_q_case'] = equal_case
        result['graphs'][name] = {
            'vertices': list(vertices), 'edges': [list(e) for e in sorted(edges)],
            'quotient_map': quotient, 'pullback_order': list(surviving),
            'inner_vertices': len(vertices) - 5, 'counts': counts, 'mask': mask,
            'in_K132': mask in masks, 'full_fibres_with_old_lifts': records}
    assert all(old_fibres[row] for row in ('01021', '01202', '01212'))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--negative-control', action='store_true')
    args = parser.parse_args()
    result = build()
    target = ROOT / 'certificate.json'
    if args.write:
        target.write_text(json.dumps(result, indent=2) + '\n')
    else:
        assert result == json.loads(target.read_text())
    if args.negative_control:
        # Demonstrate that the two tempting universal claims are actually false.
        assert not result['negative_controls']['Q1_unconditional_old_lift']['all_old_lifts']
        assert not result['negative_controls']['Q2_unconditional_old_lift']['all_old_lifts']
        assert result['negative_controls']['Q2_omitted_a_equals_q_case']['all_old_lifts']
    print(json.dumps({'status': 'pass', 'source_target': 'not-triggered',
                      'graphs': {name: {key: record[key] for key in
                                        ('inner_vertices', 'counts', 'mask', 'in_K132')}
                                 for name, record in result['graphs'].items()},
                      'certificate_sha256': hashlib.sha256(target.read_bytes()).hexdigest()},
                     sort_keys=True))


if __name__ == '__main__':
    main()
