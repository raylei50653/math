#!/usr/bin/env python3
"""Exact local replay of original-cap pockets and complete C10 contact sets."""
import argparse
import collections
import copy
import hashlib
import json
import runpy
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
OLD = ROOT / 'audits/2026-10-19-r6-941-acceptance-13dc5ff/B'
RIM = ('a', 'n', 'R', 'L', 'q', 'c', 's', 'v', 'w', 't')
CAP = ('b', 'p', 'h', 'x', 'y', 'r')
OUTER = ('x', 'y', 'a', 'b', 'c')
LEFT = (('b', 'a', 'p'), ('b', 'p', 'q'), ('b', 'q', 'c'),
        ('p', 'a', 'n'), ('p', 'n', 'h'), ('p', 'h', 'q'),
        ('h', 'n', 'R'), ('h', 'R', 'L'), ('h', 'L', 'q'))
RIGHT = (('a', 'y', 't'), ('y', 'r', 't'), ('y', 'x', 'r'),
         ('x', 'r', 's'), ('x', 's', 'c'), ('r', 't', 'w'),
         ('r', 'w', 'v'), ('r', 'v', 's'))
CAP_STARS = {'b': {'a', 'c', 'p', 'q'}, 'p': {'a', 'b', 'q', 'h', 'n'},
             'h': {'p', 'q', 'L', 'R', 'n'}, 'x': {'y', 'c', 'r', 's'},
             'y': {'x', 'a', 'r', 't'}, 'r': {'x', 'y', 't', 'w', 'v', 's'}}
NEW_PATHS = (('a', 'b', 'q'), ('a', 'y', 'x', 's'),
             ('n', 'p', 'b', 'c'), ('q', 'b', 'a', 't'),
             ('c', 'x', 'y', 't'))
INPUT_PATHS = (
    OLD / 'CONTACTS.md', OLD / 'check_contacts.py', OLD / 'contacts.json',
    OLD / 'PROOF.md', OLD.parent / 'D/PROOF.md',
    ROOT / 'audits/2026-10-19-r6-941-quotients-13dc5ff/SOURCE_CONTRACT.md',
    ROOT / 'audits/2026-10-19-r6-941-leakage-b89c591/B/SOURCE_CONTRACT.md',
    ROOT / 'audits/2026-10-19-r6-941-quotients-13dc5ff/B/CHORDS.md')


def edge(a, b):
    return tuple(sorted((a, b)))


def edges(face):
    return {edge(face[i], face[(i + 1) % len(face)]) for i in range(len(face))}


def hashes():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in INPUT_PATHS}


def local_geometry():
    """Virtual spokes locate original vertices; they assert no original edges."""
    core_faces = tuple(('z', RIM[i], RIM[(i + 1) % 10]) for i in range(10))
    faces = LEFT + RIGHT + core_faces + (OUTER,)
    incidence = collections.defaultdict(list)
    for i, face in enumerate(faces):
        for e in edges(face):
            incidence[e].append(i)
    assert all(len(v) == 2 for v in incidence.values()), 'closed reference surface'
    assert 17 - len(incidence) + len(faces) == 2, 'sphere Euler characteristic'
    known = set().union(*(edges(f) for f in LEFT + RIGHT))
    known |= {edge(RIM[i], RIM[(i + 1) % 10]) for i in range(10)}
    for v in CAP:
        actual = {w for e in known if v in e for w in e if w != v}
        assert actual == CAP_STARS[v], ('full original cap star', v)
    assert {e for e in known if set(e) <= set(RIM)} == {
        edge(RIM[i], RIM[(i + 1) % 10]) for i in range(10)}

    def interior(cycle):
        barrier = edges(cycle)
        exterior = {len(faces) - 1}
        todo = list(exterior)
        while todo:
            f = todo.pop()
            for e in edges(faces[f]) - barrier:
                for g in incidence[e]:
                    if g not in exterior:
                        exterior.add(g)
                        todo.append(g)
        inside_faces = sorted(set(range(len(faces))) - exterior)
        vertices = sorted({v for i in inside_faces for v in faces[i]} - set(cycle))
        return inside_faces, vertices

    return known, interior


def gap_arcs(contacts):
    positions = sorted(RIM.index(v) for v in contacts)
    result = []
    for j, start in enumerate(positions):
        stop = positions[(j + 1) % len(positions)]
        length = (stop - start) % 10 or 10
        result.append([RIM[(start + k) % 10] for k in range(length + 1)])
    return result


def compute():
    assert json.loads((D / 'INPUTS.json').read_text()) == hashes(), 'frozen source bytes'
    old = runpy.run_path(str(OLD / 'check_contacts.py'))['compute']()
    assert json.loads((OLD / 'contacts.json').read_text()) == old
    known, interior = local_geometry()
    pockets = []
    for path in NEW_PATHS:
        assert all(edge(path[i], path[i + 1]) in known for i in range(len(path) - 1))
        cycle = ('z',) + path
        inside_faces, vertices = interior(cycle)
        capacity = 0 if len(cycle) in (3, 4) else 1
        assert len(cycle) in (4, 5) and len(vertices) > capacity
        pockets.append({'path': list(path), 'cycle': list(cycle),
                        'bounded_reference_faces': inside_faces,
                        'known_original_interior_vertices': vertices,
                        'original_short_circle_interior_capacity': capacity,
                        'forbidden_private_contact_pair': [path[0], path[-1]]})
    assert [p['known_original_interior_vertices'] for p in pockets] == [
        ['L', 'R', 'h', 'n', 'p'], ['r', 't', 'v', 'w'],
        ['L', 'R', 'h', 'q'], ['L', 'R', 'h', 'n', 'p'], ['r', 's', 'v', 'w']]
    complete, allowed = [], []
    for oldrow in old['complete_contact_subsets']:
        s = set(oldrow['contacts'])
        newviolations = [i for i, p in enumerate(pockets)
                         if set(p['forbidden_private_contact_pair']) <= s]
        valid = oldrow['necessary_allowed'] and not newviolations
        lower = None
        if valid:
            gap_count = sum(len(a) > 2 for a in gap_arcs(s)) if s else 0
            lower = max(5 - len(s), gap_count)
            assert lower >= 2
            if len(s) == 4:
                assert lower >= 2 and len(s) + lower >= 6
            allowed.append(oldrow['contacts'])
        complete.append({'contacts': oldrow['contacts'],
                         'old_necessary_allowed': oldrow['necessary_allowed'],
                         'new_forbidden_pockets': newviolations,
                         'necessary_allowed': valid,
                         'private_neighbor_lower_bound_if_allowed': lower})
    counts = {str(k): v for k, v in sorted(collections.Counter(map(len, allowed)).items())}
    assert counts == {'0': 1, '1': 10, '2': 19, '3': 14, '4': 2}
    four = [s for s in allowed if len(s) == 4]
    assert four == [['n', 'R', 's', 'v'], ['R', 'L', 'v', 'w']]
    obstructions = []
    for first in four:
        for second in four:
            gaps = []
            for arc in gap_arcs(first):
                missing = [v for v in second if v not in arc]
                assert missing, 'second private vertex cannot occupy this spoke sector'
                gaps.append({'closed_rim_arc': arc, 'second_contacts_outside_arc': missing})
            obstructions.append({'first_complete_contacts': first,
                                 'second_complete_contacts': second,
                                 'all_sector_obstructions': gaps})
    distances = []
    for u, v in (('a', 's'), ('c', 'n'), ('q', 't'), ('c', 't')):
        assert edge(u, v) not in known
        aliases = []
        for cap in CAP:
            hits = [w for w in (u, v) if w in CAP_STARS[cap]]
            assert len(hits) < 2
            aliases.append({'cap_vertex': cap, 'adjacent_pair_members': hits})
        rim_common = [w for w in RIM if edge(u, w) in known and edge(v, w) in known]
        assert not rim_common
        assert any(set(p['forbidden_private_contact_pair']) == {u, v} for p in pockets)
        distances.append({'original_pair': [u, v], 'distance_lower_bound': 3,
                          'all_deleted_cap_aliases': aliases, 'rim_common_neighbors': rim_common})
    return {'base': '13dc5ff163045c85b5c82dde438eb5f275dab999',
            'input_hashes': hashes(), 'rim': list(RIM),
            'original_cap_faces': [list(f) for f in LEFT + RIGHT],
            'complete_original_cap_stars': {v: sorted(s) for v, s in CAP_STARS.items()},
            'reference_spokes_are_original_edge_assertions': False,
            'new_original_pocket_obstructions': pockets,
            'complete_contact_subsets': complete,
            'necessary_allowed_by_cardinality': counts,
            'allowed_four_contact_sets': four,
            'all_ordered_four_contact_pair_obstructions': obstructions,
            'maximum_number_of_four_contact_private_vertices': 1,
            'new_original_distance_bounds': distances,
            'private_induced_graph': {'connected': True, 'minimum_degree': 2,
                                      'minimum_original_degree_at_four_contact_vertex': 6,
                                      'edge_count_lower_bound': 6,
                                      'euler_contact_identity': 'contacts=3*m+7-edges(H)',
                                      'contact_count_upper_bound': '3*m+1'},
            'new_internal_size_bound_asserted': False,
            'all_necessary_contact_sets_source_realizable': False,
            'old_allK_control_source_excluded': False,
            'same_accepting_candidate_three_rejections_proved': False,
            'strictly_smaller_bad_constructed': False, 'main_target_closed': False}


def verify(value, expected):
    assert value == expected, 'complete exact pocket/contact certificate'


def negative_controls(expected):
    controls = (
        ('omit-empty-complete-contact-set', lambda x: x['complete_contact_subsets'].pop(0)),
        ('drop-known-n-from-C4-pocket', lambda x: x['new_original_pocket_obstructions'][0]
         ['known_original_interior_vertices'].remove('n')),
        ('forget-original-C5-W5-exception', lambda x: x['new_original_pocket_obstructions'][1]
         .__setitem__('original_short_circle_interior_capacity', 0)),
        ('allow-private-a-q-common-neighbor', lambda x: x['complete_contact_subsets'][17]
         .__setitem__('necessary_allowed', True)),
        ('allow-two-four-contact-private-vertices', lambda x:
         x.__setitem__('maximum_number_of_four_contact_private_vertices', 2)),
        ('allow-degree-five-four-contact-private-vertex', lambda x: x['private_induced_graph']
         .__setitem__('minimum_original_degree_at_four_contact_vertex', 5)),
        ('claim-old-allK-source-excluded-without-contact-data', lambda x:
         x.__setitem__('old_allK_control_source_excluded', True)),
        ('upgrade-main-target', lambda x: x.__setitem__('main_target_closed', True)),
    )
    rejected = []
    for label, mutate in controls:
        bad = copy.deepcopy(expected)
        mutate(bad)
        try:
            verify(bad, expected)
        except AssertionError:
            rejected.append(label)
        else:
            raise AssertionError(('negative control accepted', label))
    return rejected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--certificate', type=Path, default=D / 'certificate.json')
    args = ap.parse_args()
    if args.build:
        with (D / 'INPUTS.json').open('x') as f:
            json.dump(hashes(), f, sort_keys=True, indent=2)
            f.write('\n')
    expected = compute()
    if args.build:
        with args.certificate.open('x') as f:
            json.dump(expected, f, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            f.write('\n')
    verify(json.loads(args.certificate.read_text()), expected)
    print(json.dumps({'pass': True, 'complete_contact_sets': 1024,
                      'necessary_allowed_sets': 46, 'new_forbidden_private_pairs': 5,
                      'four_contact_types': expected['allowed_four_contact_sets'],
                      'maximum_four_contact_vertices': 1,
                      'new_original_distance_bounds': [p['original_pair'] for p in
                                                       expected['new_original_distance_bounds']],
                      'negative_controls_rejected': negative_controls(expected),
                      'main_target': 'OPEN'}, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
