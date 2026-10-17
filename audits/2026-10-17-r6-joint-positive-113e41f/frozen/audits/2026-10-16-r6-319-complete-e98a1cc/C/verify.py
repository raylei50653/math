#!/usr/bin/env python3
"""Independent exhaustive verification of a planar bridge countercontrol."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROTATION = [[1, 2, 3, 4, 5], [0, 5, 6, 7, 2], [0, 1, 7, 3],
            [0, 2, 7, 8, 9, 4], [0, 3, 9, 5], [0, 4, 9, 6, 1],
            [1, 5, 9, 8, 7], [1, 6, 8, 3, 2], [3, 7, 6, 9],
            [3, 8, 6, 5, 4]]
PINS = dict(m=1, z=5, v=0, w=2, p=6, q=9)


def edge(u, v):
    return tuple(sorted((u, v)))


def components(vertices, edges):
    adj = {u: [] for u in vertices}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    unseen, out = set(vertices), []
    while unseen:
        todo, found = [min(unseen)], set()
        while todo:
            u = todo.pop()
            if u in found:
                continue
            found.add(u)
            unseen.discard(u)
            todo.extend(v for v in adj[u] if v not in found)
        out.append(sorted(found))
    return out


def all_colourings(vertices, edges):
    adj = {u: set() for u in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    chosen, out = {}, []
    def visit():
        if len(chosen) == len(vertices):
            out.append(tuple(chosen[u] for u in vertices))
            return
        u = max((u for u in vertices if u not in chosen),
                key=lambda u: (len({chosen[v] for v in adj[u] if v in chosen}), len(adj[u]), -u))
        forbidden = {chosen[v] for v in adj[u] if v in chosen}
        for c in range(4):
            if c not in forbidden:
                chosen[u] = c
                visit()
        chosen.pop(u, None)
    visit()
    return sorted(out)


def perfect_matchings(vertices, edges):
    adj = {u: [] for u in vertices}
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    def visit(left, chosen):
        if not left:
            yield sorted(chosen)
            return
        u = min(left)
        for v, i in adj[u]:
            if v in left:
                yield from visit(left - {u, v}, chosen + [i])
    return sorted(visit(set(vertices), []))


def integrate(vertices, edges, matching):
    bits, todo = {vertices[0]: 0}, [vertices[0]]
    while todo:
        u = todo.pop()
        for i, (a, b) in enumerate(edges):
            if u not in (a, b):
                continue
            v = b if a == u else a
            bit = bits[u] ^ int(i not in matching)
            if v in bits:
                assert bits[v] == bit
            else:
                bits[v] = bit
                todo.append(v)
    assert len(bits) == len(vertices)
    return [bits[u] for u in vertices]


def pin_fibres(colourings, ordered_pins):
    """Dense 4^arity universe, plus exact indices of every private full lift."""
    counts = [0] * (4 ** len(ordered_pins))
    lift_indices = {}
    for i, colouring in enumerate(colourings):
        index = 0
        for u in ordered_pins:
            index = 4 * index + colouring[u]
        counts[index] += 1
        lift_indices.setdefault(str(index), []).append(i)
    assert sum(counts) == len(colourings)
    return dict(ordered_pins=ordered_pins, arity=len(ordered_pins),
                universe='all tuples in {0,1,2,3}^arity, lexicographic base-4 index; no tuple omitted',
                complete_fibre_counts=counts,
                full_colour_record_indices=lift_indices,
                empty_fibres=sum(x == 0 for x in counts))


def reconstruct():
    vertices = list(range(len(ROTATION)))
    edges = sorted({edge(u, v) for u, ns in enumerate(ROTATION) for v in ns})
    assert all(u in ROTATION[v] for u, ns in enumerate(ROTATION) for v in ns)
    darts = {(u, v) for u, ns in enumerate(ROTATION) for v in ns}
    oriented_faces = []
    while darts:
        start = min(darts)
        dart, face = start, []
        while not face or dart != start:
            assert dart in darts
            darts.remove(dart)
            u, v = dart
            face.append(u)
            around = ROTATION[v]
            dart = (v, around[(around.index(u) + 1) % len(around)])
        assert len(face) == 3
        oriented_faces.append(face)
    faces = sorted(tuple(sorted(f)) for f in oriented_faces)
    assert len(vertices) - len(edges) + len(faces) == 2
    assert len(components(vertices, edges)) == 1
    # The explicit orientable cellular rotation has Euler characteristic two.
    # Exhaustively retain the stronger four-connectivity check as finite data.
    for deleted in combinations(vertices, 3):
        left = set(vertices) - set(deleted)
        assert len(components(left, [uv for uv in edges if set(uv) <= left])) == 1
    triangles = sorted(tuple(c) for c in combinations(vertices, 3)
                       if all(edge(u, v) in edges for u, v in combinations(c, 2)))
    assert triangles == faces
    incident = {uv: [] for uv in edges}
    for i, face in enumerate(faces):
        for u, v in combinations(face, 2):
            incident[edge(u, v)].append(i)
    assert all(len(fs) == 2 for fs in incident.values())
    dual_edges = [incident[uv] for uv in edges]
    marks = [edges.index(edge(PINS[a], PINS[b])) for a, b in [('v', 'w'), ('p', 'q'), ('m', 'z')]]
    assert len(set(sum((dual_edges[i] for i in marks), []))) == 6
    assert tuple(sorted(PINS[k] for k in ['m', 'v', 'w'])) in faces
    assert tuple(sorted(PINS[k] for k in ['z', 'p', 'q'])) in faces
    colours = all_colourings(vertices, edges)
    assert len(colours) == 144
    event_counts = Counter()
    for colour in colours:
        e, f, g = [colour[edges[i][0]] ^ colour[edges[i][1]] for i in marks]
        event_counts['E1'] += int(e == f != g)
        event_counts['E2'] += int(e == g != f)
        event_counts['all_equal'] += int(e == f == g)
        assert (e == f) == (e == g)
    pm_rows = []
    for matching in perfect_matchings(list(range(len(faces))), dual_edges):
        complement = [uv for i, uv in enumerate(dual_edges) if i not in matching]
        cycles = components(list(range(len(faces))), complement)
        assert all(sum(u in uv for uv in complement) == 2 for u in range(len(faces)))
        bits = integrate(vertices, edges, matching)
        fibres = [list(c) for c in colours if [x >> 1 for x in c] == bits]
        oddness = sum(len(c) % 2 for c in cycles)
        assert len(fibres) == (0 if oddness else 2 ** (len(cycles) + 1))
        pattern = ''.join(str(int(i in matching)) for i in marks)
        pm_rows.append(dict(matching=matching, pattern=pattern,
                            complement_cycles=cycles, oddness=oddness,
                            integrated_bits=bits, complete_colour_fibre=fibres))
    joint = [r for r in pm_rows if r['pattern'] in ['110', '101']]
    assert len(joint) == 1 and joint[0]['pattern'] == '101' and joint[0]['oddness'] == 2
    assert sorted(len(c) for c in joint[0]['complement_cycles']) == [7, 9]
    weighted = {p: sum(2 ** len(r['complement_cycles']) for r in pm_rows
                      if r['pattern'] == p and r['oddness'] == 0)
                for p in ['111', '110', '101']}
    assert weighted == {'111': 6, '110': 0, '101': 0}
    e, f, g = marks
    assert event_counts['E1'] == 12 * weighted['110']
    assert event_counts['E2'] == 12 * weighted['101']
    # Complete two-star fibres, with every labelled W colouring and every lift.
    m, z = PINS['m'], PINS['z']
    wvertices = [u for u in vertices if u not in [m, z]]
    wedges = [uv for uv in edges if m not in uv and z not in uv]
    wfibres = []
    for row in all_colourings(wvertices, wedges):
        colouring = dict(zip(wvertices, row))
        am = sorted(set(range(4)) - {colouring[u] for u in ROTATION[m] if u != z})
        az = sorted(set(range(4)) - {colouring[u] for u in ROTATION[z] if u != m})
        lifts = [[a, b] for a in am for b in az if a != b]
        actual = sorted([[c[m], c[z]] for c in colours if all(c[u] == colouring[u] for u in wvertices)])
        assert lifts == actual
        wfibres.append(dict(complete_W_colour=list(row), A_m=am, A_z=az,
                            all_hub_lifts=lifts))
    # A single original-edge even111 to ordinary101 exchange already loses evenness.
    start = next(r for r in pm_rows if r['pattern'] == '111' and len(r['complement_cycles']) == 2)
    end = joint[0]
    difference = sorted(set(start['matching']) ^ set(end['matching']))
    assert e not in difference and g not in difference and f in difference
    assert len(components({u for i in difference for u in dual_edges[i]},
                          [dual_edges[i] for i in difference])) == 1
    transition_traces = []
    for old in [r for r in pm_rows if r['pattern'] == '111']:
        oldset, newset = set(old['matching']), set(end['matching'])
        delta = oldset ^ newset
        delta_components = components({u for i in delta for u in dual_edges[i]},
                                      [dual_edges[i] for i in delta])
        assert len(delta_components) == 1
        for colouring in colours:
            differences = [colouring[u] ^ colouring[v] for u, v in edges]
            if colouring[0] != 0 or {i for i, x in enumerate(differences) if x == 1} != oldset:
                continue
            removed, added = oldset - newset, newset - oldset
            b_at = {u: i for i in added for u in dual_edges[i]}
            transitions = sorted(i for i in removed
                                 if differences[b_at[dual_edges[i][0]]] != differences[b_at[dual_edges[i][1]]])
            placement = []
            for cycle in end['complement_cycles']:
                ts = [i for i in transitions if dual_edges[i][0] in cycle]
                assert len(ts) % 2 == len(cycle) % 2
                placement.append(dict(vertices=cycle, transitions=ts))
            transition_traces.append(dict(even_111=old['matching'],
                                          root_zero_alpha_one_complete_colour=colouring,
                                          single_alternating_cycle=sorted(delta),
                                          transitions=transitions, placement=placement))
    assert len(transition_traces) == 6
    assert [len(t['transitions']) for t in transition_traces] == [2] * 4 + [4] * 2
    # Diagnose this control against the original source, without promoting it
    # to a source. The z/e gaps determine a unique cellular split of m.
    induced = {}
    for length in [4, 5]:
        induced[length] = []
        for subset in combinations(vertices, length):
            subedges = [uv for uv in edges if set(uv) <= set(subset)]
            if len(subedges) == length and all(sum(u in uv for uv in subedges) == 2 for u in subset):
                if len(components(subset, subedges)) == 1:
                    induced[length].append(list(subset))
    assert [c for c in induced[4] if not set(c) & {m, z}] == [[3, 6, 7, 9]]
    assert [c for c in induced[5] if not set(c) & {m, z}] == []
    def unique_arc(rotation, start, stop, avoid):
        possible = []
        for direction in [-1, 1]:
            pos = rotation.index(start)
            path = [start]
            while len(path) <= len(rotation):
                pos = (pos + direction) % len(rotation)
                u = rotation[pos]
                path.append(u)
                if u == avoid:
                    break
                if u == stop:
                    possible.append(path)
                    break
        assert len(possible) == 1
        return possible[0]
    s_arc = unique_arc(ROTATION[m], z, PINS['v'], PINS['w'])
    t_arc = unique_arc(ROTATION[m], z, PINS['w'], PINS['v'])
    assert s_arc == [5, 0] and t_arc == [5, 6, 7, 2]
    a_arc = unique_arc(ROTATION[z], m, PINS['p'], PINS['q'])
    c_arc = unique_arc(ROTATION[z], PINS['q'], m, PINS['p'])
    assert a_arc == [1, 6] and c_arc == [9, 4, 0, 1]
    cross_edges = [edge(PINS[u], PINS[v]) for u in ['v', 'w'] for v in ['p', 'q']
                   if edge(PINS[u], PINS[v]) in edges]
    assert cross_edges == []
    ordinary_low = [u for u in vertices if u not in PINS.values() and len(ROTATION[u]) < 5]
    assert ordinary_low == [4, 8]
    uedges = sorted([uv for uv in edges if m not in uv] +
                    [edge(10, u) for u in s_arc] + [edge(1, u) for u in t_arc])
    original_boundary = [5, 10, 0, 2, 1]
    boundary_edges = {edge(original_boundary[i], original_boundary[(i+1) % 5]) for i in range(5)}
    boundary_chords = [uv for uv in uedges if set(uv) <= set(original_boundary) and uv not in boundary_edges]
    assert boundary_chords == [(0, 5)]
    uvertices = list(range(11))
    ucolours = all_colourings(uvertices, uedges)
    rows = ['ABABC', 'ABACB', 'ABACD', 'ABCAB', 'ABCAC', 'ABCAD', 'ABCBC', 'ABCBD', 'ABCDB', 'ABCDC']
    table = [['BC', 'CB'], ['BC', 'CB', 'CD', 'DC'], ['BC', 'BD', 'CB', 'CD', 'DB', 'DC'],
             ['BC', 'CB', 'CD', 'DC'], ['BC', 'CB'], ['BC', 'BD', 'CB', 'CD', 'DB', 'DC'],
             [], [], ['CD', 'DC'], []]
    rtable = {'ABAB': ['CD', 'DC'], 'ABAC': [],
              'ABCB': ['CD', 'DC', 'BD', 'DB'], 'ABCD': ['BD', 'DB']}
    def frame(colouring, boundary):
        mapping = {}
        for u in boundary:
            mapping.setdefault(colouring[u], chr(65 + len(mapping)))
        for value in range(4):
            mapping.setdefault(value, chr(65 + len(mapping)))
        return ''.join(mapping[colouring[u]] for u in boundary), mapping
    split_records = []
    for boundary, pq in [([5, 10, 0, 2, 1], [6, 9]), ([5, 1, 2, 0, 10], [9, 6])]:
        fibres, support, violations = [], Counter(), Counter()
        for colouring in ucolours:
            row, mapping = frame(colouring, boundary)
            pair = ''.join(mapping[colouring[u]] for u in pq)
            support[row] += 1
            passes = pair in table[rows.index(row)]
            if not passes:
                violations[row + ':' + pair] += 1
            # Every legal r colour is retained, including an empty r fibre.
            r_lifts = []
            for value in sorted(set(range(4)) - {colouring[u] for u in boundary[1:]}):
                extended = list(colouring) + [value]
                rrow, rmapping = frame(extended, [boundary[0], boundary[1], 11, boundary[4]])
                rpair = ''.join(rmapping[colouring[u]] for u in pq)
                r_lifts.append(dict(r_colour=value, R_row=rrow, pq=rpair,
                                    allowed=rpair in rtable[rrow]))
            assert passes == all(r['allowed'] for r in r_lifts)
            fibres.append(dict(complete_U_colour=list(colouring), C5_row=row,
                               pq=pair, all_r_lifts=r_lifts, passes_full_transfer=passes))
        mask = sum(1 << rows.index(row) for row in support)
        assert sum(violations.values()) == 192
        split_records.append(dict(boundary=boundary, pq=pq, mask=mask,
                                  row_counts=dict(sorted(support.items())),
                                  transfer_violations=dict(sorted(violations.items())),
                                  seven_pin_fibres=pin_fibres(ucolours, boundary + pq),
                                  complete_U_fibres=fibres))
    assert [x['mask'] for x in split_records] == [1016, 967]
    assert len(ucolours) == 432
    return dict(schema=1, source='not triggered', BASE='e98a1cc1afd9a428600dcf4027d8138078c01650',
                rotation=ROTATION, pins=PINS, edges=edges, faces=faces,
                dual_edges=dual_edges, marks=marks, complete_J_colourings=colours,
                J_six_pin_fibres=pin_fibres(colours, [PINS[k] for k in ['z', 'm', 'v', 'w', 'p', 'q']]),
                perfect_matching_rows=pm_rows, W_vertices=wvertices,
                complete_W_fibres=wfibres,
                exchange=dict(even_111=start['matching'], ordinary_101=end['matching'],
                              alternating_cycle_edge_indices=difference),
                independent_transition_crosscheck=transition_traces,
                source_diagnostics=dict(degrees=[len(ns) for ns in ROTATION],
                                        induced_cycles=induced,
                                        literal_m_split_neighbours=dict(s=s_arc, t=t_arc),
                                        split_arc_lengths=[len(s_arc)-1, len(t_arc)-1],
                                        implied_original_s_t_degrees=[len(s_arc)+2, len(t_arc)+2],
                                        implied_a_c_degrees=[len(a_arc)+2, len(c_arc)+2],
                                        implied_h=len(ROTATION[z])-3,
                                        unmarked_vertices_below_degree_five=ordinary_low,
                                        cross_edges_vw_pq=cross_edges, U_edges=uedges,
                                        forbidden_U_boundary_chords=boundary_chords,
                                        complete_reflected_splits=split_records),
                summary=dict(V=10, E=24, F=16, four_connected=True,
                             labelled_J_colourings=len(colours), perfect_matchings=len(pm_rows),
                             empty_colour_fibres=sum(not r['complete_colour_fibre'] for r in pm_rows),
                             ordinary_101=1, ordinary_110=0, joint_minimum=2,
                             weighted=weighted, event_counts=dict(event_counts),
                             complete_W_colourings=len(wfibres),
                             empty_W_fibres=sum(not r['all_hub_lifts'] for r in wfibres)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    frozen_inputs = json.loads((HERE / 'INPUTS.json').read_text())
    assert frozen_inputs['BASE'] == 'e98a1cc1afd9a428600dcf4027d8138078c01650'
    for item in frozen_inputs['frozen_inputs']:
        assert hashlib.sha256((HERE / item['path']).read_bytes()).hexdigest() == item['sha256']
    actual = json.loads(json.dumps(reconstruct()))
    if args.check:
        expected = json.loads(args.certificate.read_text())
        assert actual == expected, 'certificate differs from independent full reconstruction'
    else:
        with args.certificate.open('x') as handle:
            json.dump(actual, handle, indent=2)
            handle.write('\n')
    print(json.dumps(actual['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
