#!/usr/bin/env python3
"""Read-only replay of complete fixed plane controls; not R6 source enumeration."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = '9c36e3c4789dfec07d60ec4e042f0bafe17451d1'
PORTS = (1, 2, 4, 5, 6)


def edge(a, b):
    return tuple(sorted((a, b)))


def cycle_edges(c):
    return {edge(a, b) for a, b in zip(c, c[1:] + c[:1])}


def components(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    unseen = set(vertices)
    answer = []
    while unseen:
        pending = [min(unseen)]
        found = set()
        while pending:
            v = pending.pop()
            if v not in found:
                found.add(v)
                pending.extend(adj[v] - found)
        unseen -= found
        answer.append(found)
    return answer


def whole_cycles(vertices, edges):
    adj = {v: [] for v in vertices}
    for a, b in sorted(edges):
        adj[a].append(b)
        adj[b].append(a)
    assert all(len(adj[v]) == 2 for v in vertices)
    result = []
    for comp in components(vertices, edges):
        start = min(comp)
        previous, current = None, start
        row = []
        while current not in row:
            row.append(current)
            nxt = min(w for w in adj[current] if w != previous)
            previous, current = current, nxt
        assert current == start and set(row) == comp
        result.append(row)
    return result


def all_matchings(vertices, edges):
    adj = {v: [] for v in vertices}
    for a, b in sorted(edges):
        adj[a].append(b)
        adj[b].append(a)

    def rec(unmatched, chosen):
        if not unmatched:
            yield frozenset(chosen)
            return
        a = min(unmatched)
        for b in sorted(adj[a]):
            if b in unmatched:
                yield from rec(unmatched - {a, b}, chosen + [edge(a, b)])
    return list(rec(set(vertices), []))


def validate_matching(vertices, edges, matching):
    assert matching <= edges
    assert sorted(v for ed in matching for v in ed) == sorted(vertices)


def rotations(n, ports, chords, sides):
    matching = {edge(0, 3)} | {edge(a, b) for a, b in zip(PORTS, ports)} | set(chords)
    rot = {}
    for cyc in [list(range(7)), list(range(7, 7 + n))]:
        for i, v in enumerate(cyc):
            third = next(b if a == v else a for a, b in matching if v in (a, b))
            inside = v in (0, 3) if v < 7 else (v in ports or sides[edge(v, third)] == 'cap')
            prev, nxt = cyc[(i - 1) % len(cyc)], cyc[(i + 1) % len(cyc)]
            rot[v] = [prev, nxt, third] if inside else [prev, third, nxt]
    return rot


def sphere_faces(rotation):
    darts = {(a, b) for a, bs in rotation.items() for b in bs}
    all_darts = set(darts)
    assert all((b, a) in darts for a, b in darts)
    faces = []
    while darts:
        first = min(darts)
        d = first
        face = []
        while True:
            assert d in darts
            darts.remove(d)
            a, b = d
            face.append(a)
            ns = rotation[b]
            d = (b, ns[(ns.index(a) + 1) % len(ns)])
            if d == first:
                break
        assert len(set(face)) == len(face)
        faces.append(face)
    assert len(rotation) - len(all_darts) // 2 + len(faces) == 2
    assert len(components(rotation, {edge(*d) for d in all_darts})) == 1
    return faces


def literal_labels(faces, e, f, g):
    def incident(ed):
        return [i for i, face in enumerate(faces) if ed in cycle_edges(face)]

    def at_vertex(v):
        return {i for i, face in enumerate(faces) if v in face}

    p = next(i for i, face in enumerate(faces) if set(face) == {0, 1, 2, 3})
    q = next(i for i in incident(f) if i != p)
    for z, m in itertools.permutations(incident(g)):
        if len({p, q, z, m}) != 4:
            continue
        if not any({p, q, z} == at_vertex(a) for a in f):
            continue
        if not set(faces[z]) & set(range(7)) or set(faces[m]) & set(range(7)):
            continue
        v, w = incident(e)
        if len({p, q, z, m, v, w}) != 6:
            continue
        if any({m, v, w} == at_vertex(a) for a in e):
            return dict(p=p, q=q, z=z, m=m, v=v, w=w)
    return None


def distance(vertices, edges, starts, ends):
    seen = set(starts)
    wave = set(starts)
    d = 0
    while not seen & set(ends):
        wave = {b if a in wave else a for a, b in edges if (a in wave) != (b in wave)} - seen
        assert wave
        seen |= wave
        d += 1
    return d


def labelled_tait_rows(edges, matching_rows, marks):
    """Every labelled Tait colouring with e colour 0, including both cycle orientations."""
    e, f, g = marks
    ordered = sorted(edges)
    output = []
    for row in matching_rows:
        matching = {tuple(ed) for ed in row['edges']}
        if e not in matching or row['oddness']:
            continue
        cycles = row['complement_cycles']
        for choices in itertools.product((0, 1), repeat=len(cycles)):
            colours = {ed: 0 for ed in matching}
            for c, flip in zip(cycles, choices):
                for i, (a, b) in enumerate(zip(c, c[1:] + c[:1])):
                    colours[edge(a, b)] = 1 + ((i + flip) % 2)
            for v in {a for ed in edges for a in ed}:
                assert {colours[ed] for ed in edges if v in ed} == {0, 1, 2}
            output.append({'edge_colours': [colours[ed] for ed in ordered],
                           'marked_colours': [colours[x] for x in (e, f, g)]})
    return sorted(output, key=lambda row: row['edge_colours'])


def monotone_walk(n, ports, chords, sides, a, b):
    left, right = ports[PORTS.index(a)], ports[PORTS.index(b)]
    assert left < right
    mate = {u: v for ed in chords for u, v in (ed, ed[::-1])}
    path = [left]
    jumps = []
    while path[-1] != right:
        x = path[-1] + 1
        path.append(x)
        if x == right:
            return {'cap_pair': [a, b], 'status': 'reached', 'outside_path': path,
                    'jumps': jumps, 'all_jump_arcs_odd': all(j['arc_length'] % 2 for j in jumps)}
        assert x < right and x in mate
        y = mate[x]
        ed = edge(x, y)
        if sides[ed] != 'cap':
            return {'cap_pair': [a, b], 'status': 'outside_chord_blocker',
                    'outside_path': path, 'blocker': list(ed), 'jumps': jumps}
        assert x < y < right
        jumps.append({'chord': list(ed), 'arc_vertices': list(range(x, y + 1)), 'arc_length': y - x})
        path.append(y)


def compute_control(spec):
    n, ports = spec['outer_length'], spec['outer_ports']
    chords = [tuple(ed) for ed in spec['outer_chords']]
    sides = dict(zip(chords, spec['chord_sides']))
    marks = tuple(tuple(ed) for ed in spec['marks'])
    e, f, g = marks
    vertices = set(range(7 + n))
    matching = {edge(0, 3)} | {edge(a, b) for a, b in zip(PORTS, ports)} | set(chords)
    old = cycle_edges(list(range(7))) | cycle_edges(list(range(7, 7 + n)))
    assert not old & matching
    edges = old | matching
    validate_matching(vertices, edges, matching)
    assert all(sum(v in ed for ed in edges) == 3 for v in vertices)
    assert e in matching and f not in matching and g in matching
    assert sides[e] == 'outside' and sides[g] == 'cap'
    rotation = rotations(n, ports, chords, sides)
    faces = sphere_faces(rotation)
    labels = literal_labels(faces, e, f, g)
    rows = []
    fibres = {''.join(bits): [] for bits in itertools.product('01', repeat=3)}
    for index, candidate in enumerate(all_matchings(vertices, edges)):
        validate_matching(vertices, edges, candidate)
        complement = whole_cycles(vertices, edges - candidate)
        difference = matching ^ candidate
        affected = {v for ed in difference for v in ed}
        diff_cycles = whole_cycles(affected, difference)
        assert all(len(c) % 2 == 0 for c in diff_cycles)
        for c in diff_cycles:
            seq = [edge(a, b) for a, b in zip(c, c[1:] + c[:1])]
            assert all((seq[i] in matching) != (seq[(i + 1) % len(seq)] in matching) for i in range(len(seq)))
        pattern = ''.join(str(int(ed in candidate)) for ed in marks)
        allowed = e not in difference and ((f in difference) == (g in difference))
        assert allowed == (pattern in ('101', '110'))
        row = {'index': index, 'edges': sorted(candidate), 'marked_type': pattern,
               'complement_cycles': complement, 'oddness': sum(len(c) % 2 for c in complement),
               'difference_cycles_from_M': diff_cycles, 'joint_admissible': allowed}
        rows.append(row)
        fibres[pattern].append(index)
    tait = labelled_tait_rows(edges, rows, marks)
    even_fibres = {key: [i for i in indices if rows[i]['oddness'] == 0] for key, indices in fibres.items()}
    walks = []
    for a, b in ((4, 5), (5, 6)):
        walk = monotone_walk(n, ports, chords, sides, a, b)
        if walk['status'] == 'reached':
            path = walk['outside_path']
            q = [a, b] + list(reversed(path))
            toggle = cycle_edges(q)
            candidate = matching ^ toggle
            validate_matching(vertices, edges, candidate)
            new = whole_cycles(vertices, edges - candidate)
            safe = e not in toggle and ((f in toggle) == (g in toggle))
            assert (not any(len(c) % 2 for c in new)) == walk['all_jump_arcs_odd']
            walk.update(alternating_cycle=q, mark_safe=safe, complement_cycles=new,
                        oddness=sum(len(c) % 2 for c in new))
        walks.append(walk)
    result = dict(spec, edges=sorted(edges), M=sorted(matching), old_complement_cycles=whole_cycles(vertices, old),
                  sphere_rotation={str(k): v for k, v in sorted(rotation.items())}, sphere_faces=faces,
                  literal_primal_labels=labels, marked_distances_from_cap=[distance(vertices, edges, range(7), ed) for ed in (e, g)],
                  source_failure_faces=[face for face in faces if len(face) == 3],
                  matching_rows=rows, matching_fibres=fibres, even_matching_fibres=even_fibres,
                  tait_colourings_e_zero=tait, monotone_intervals=walks)
    result['counts'] = {'perfect_matchings': len(rows), 'even_matchings': sum(row['oddness'] == 0 for row in rows),
                        'even_101': len(even_fibres['101']), 'even_110': len(even_fibres['110']),
                        'even_111': len(even_fibres['111']), 'tait_e_zero': len(tait),
                        'tait_all_distinct': sum(len(set(row['marked_colours'])) == 3 for row in tait)}
    if spec['name'] == 'literal_safe_cap_disappearance':
        q = [5, 6, 12, 13, 10, 11]
        toggle = cycle_edges(q)
        candidate = matching ^ toggle
        validate_matching(vertices, edges, candidate)
        assert not toggle & set(marks)
        complement = whole_cycles(vertices, edges - candidate)
        assert sorted(map(len, complement)) == [9, 11]
        m0 = {tuple(x) for x in [[0, 3], [1, 2], [4, 9], [5, 6], [7, 8], [10, 11], [12, 13], [14, 19], [15, 17], [16, 18]]}
        assert all(ed in m0 for ed in marks)
        assert not any(len(c) % 2 for c in whole_cycles(vertices, edges - m0))
        assert toggle <= (matching ^ m0)
        result['safe_non_descent'] = {'Q': q, 'M0': sorted(m0), 'M0_complement_cycles': whole_cycles(vertices, edges - m0),
                                      'N_edges': sorted(candidate), 'complement_cycles': complement, 'oddness': 2}
    return result


def frozen_inputs():
    manifest = json.loads((HERE.parent / 'INPUTS.json').read_text())
    assert manifest['base'] == BASE
    selected = ['audits/2026-10-17-r6-two-cycle-cap-3d325d7/PROOF.md',
                'audits/2026-10-17-r6-seven-five-repair-5b9a7b3/A/PROOF.md']
    rows = []
    for path in selected:
        record = next(row for row in manifest['inputs'] if row['path'] == path)
        data = (HERE.parent / 'frozen' / path).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == record['sha256'] and len(data) == record['bytes']
        rows.append({'path': path, 'bytes': len(data), 'sha256': digest})
    return rows


def expected():
    specs = [
        {'name': 'weak_geometry_no_repair', 'outer_length': 11, 'outer_ports': [7, 8, 9, 12, 17],
         'outer_chords': [[10, 15], [11, 14], [13, 16]], 'chord_sides': ['outside', 'outside', 'cap'],
         'marks': [[10, 15], [1, 2], [13, 16]]},
        {'name': 'literal_safe_cap_disappearance', 'outer_length': 13, 'outer_ports': [7, 8, 9, 11, 12],
         'outer_chords': [[10, 13], [14, 19], [15, 17], [16, 18]], 'chord_sides': ['outside', 'cap', 'cap', 'outside'],
         'marks': [[16, 18], [1, 2], [14, 19]]},
        {'name': 'literal_even_skip_failure', 'outer_length': 11, 'outer_ports': [7, 8, 9, 13, 14],
         'outer_chords': [[10, 12], [11, 16], [15, 17]], 'chord_sides': ['cap', 'outside', 'cap'],
         'marks': [[11, 16], [1, 2], [15, 17]]},
        {'name': 'literal_odd_skip_success', 'outer_length': 13, 'outer_ports': [7, 8, 9, 14, 15],
         'outer_chords': [[10, 13], [11, 18], [12, 17], [16, 19]], 'chord_sides': ['cap', 'outside', 'outside', 'cap'],
         'marks': [[11, 18], [1, 2], [16, 19]]},
    ]
    controls = [compute_control(spec) for spec in specs]
    weak, literal, skip, positive = controls
    assert weak['literal_primal_labels'] is None
    assert weak['counts']['even_101'] == weak['counts']['even_110'] == 0
    assert all(c['counts']['even_111'] > 0 and c['counts']['tait_all_distinct'] > 0 for c in controls[:2])
    assert all(c['literal_primal_labels'] is not None for c in controls[1:])
    assert all(min(c['marked_distances_from_cap']) >= 2 for c in controls)
    assert literal['monotone_intervals'][1]['mark_safe']
    assert literal['monotone_intervals'][1]['oddness'] == 0
    assert skip['monotone_intervals'][0]['mark_safe']
    assert sorted(map(len, skip['monotone_intervals'][0]['complement_cycles'])) == [3, 15]
    assert skip['monotone_intervals'][0]['jumps'][0]['arc_length'] == 2
    assert positive['monotone_intervals'][0]['mark_safe']
    assert positive['monotone_intervals'][0]['jumps'][0]['arc_length'] == 3
    assert sorted(map(len, positive['monotone_intervals'][0]['complement_cycles'])) == [4, 16]
    assert positive['counts']['tait_all_distinct'] > 0
    return {'schema': 2, 'base': BASE, 'authority': 'four fixed plane cubic controls; no R6 source realization',
            'source_realizability': 'not triggered', 'frozen_inputs': frozen_inputs(), 'controls': controls}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', nargs='?', type=Path, default=HERE / 'certificate-v2.json')
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    data = expected()
    if args.write:
        with args.write.open('x') as stream:
            json.dump(data, stream, indent=2, sort_keys=True)
            stream.write('\n')
        print('EXCLUSIVE CREATE PASS')
        return
    actual = json.loads(args.certificate.read_text())
    assert actual == json.loads(json.dumps(data)), 'certificate differs from complete exact replay'
    print(json.dumps({'status': 'PASS', 'source_realizability': 'not triggered',
                      'controls': {c['name']: c['counts'] for c in data['controls']}}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
