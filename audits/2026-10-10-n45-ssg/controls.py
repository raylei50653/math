#!/usr/bin/env python3
"""Independent C5 arithmetic only: no interior graph or source realization."""
from collections import Counter
from itertools import product, permutations, combinations
import json


def proper(row):
    return all(row[i] != row[(i + 1) % 5] for i in range(5))


def canonical(row):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in row)


def singleton(row):
    counts = Counter(row)
    return next(i for i, c in enumerate(row) if counts[c] == 1)


def moved(row, mapping):
    ans = [None] * 5
    for old, new in enumerate(mapping):
        ans[new] = row[old]
    return tuple(ans)


def run():
    all_rows = sorted(row for row in product(range(4), repeat=5) if proper(row))
    three = [row for row in all_rows if len(set(row)) == 3]
    four = [row for row in all_rows if len(set(row)) == 4]
    patterns = sorted({canonical(row) for row in all_rows})
    t4 = [i for i, row in enumerate(patterns) if len(set(row)) == 4]
    q_index = {singleton(row): i for i, row in enumerate(patterns) if len(set(row)) == 3}
    assert len(all_rows) == 240 and len(three) == len(four) == 120
    assert t4 == [2, 5, 7, 8, 9]
    assert q_index == {4: 0, 3: 1, 2: 3, 1: 4, 0: 6}
    assert [i for i in range(10) if not (933 >> i) & 1] == [1, 3, 4, 6]
    assert [i for i in range(10) if not (941 >> i) & 1] == [1, 4, 6]

    recolors = []
    for row in three:
        unique = singleton(row)
        unused = next(iter(set(range(4)) - set(row)))
        assert sorted(Counter(row).values()) == [1, 2, 2]
        for v in range(5):
            changed = list(row)
            changed[v] = unused
            changed = tuple(changed)
            assert proper(changed)
            assert (len(set(changed)) == 4) == (v != unique)
            if v != unique:
                assert patterns.index(canonical(changed)) in t4
                assert all(changed[i] == row[i] for i in range(5) if i != v)
                assert row[v] not in {changed[(v - 1) % 5], changed[(v + 1) % 5]}
                recolors.append({'row': row, 'v': v, 'T4_row': changed})

    two_unattached = 0
    for row in three:
        for a, b in combinations(range(5), 2):
            assert any(v != singleton(row) for v in (a, b))
            two_unattached += 1

    single_point_masks = {}
    for m in range(5):
        covered = set(t4)
        for item in recolors:
            if item['v'] == m:
                covered.add(patterns.index(canonical(item['row'])))
        assert covered == set(range(10)) - {q_index[m]}
        single_point_masks[str(m)] = sorted(covered)

    arcs = []
    counts = Counter()
    for lu, ll in product(range(2, 6), repeat=2):
        for u, l in product(range(5), repeat=2):
            eu = {(u + i) % 5 for i in range(lu)}
            el = {(l + i) % 5 for i in range(ll)}
            if eu & el:
                continue
            assert (lu, ll) in {(2, 2), (2, 3), (3, 2)}
            iu = [(u + i) % 5 for i in range(1, lu)]
            assert len(iu) == lu - 1
            assert len({(u + i) % 5 for i in range(lu + 1)}) == lu + 1
            counts[f'{lu},{ll}'] += 1
            arcs.append({'U_start': u, 'U_length': lu, 'L_start': l,
                         'L_length': ll, 'U_edges': sorted(eu),
                         'L_edges': sorted(el), 'U_interior': iu})
    assert dict(counts) == {'2,2': 10, '2,3': 5, '3,2': 5}

    q2 = (0, 1, 2, 0, 1)
    q2_common_actions = 0
    q2_recolors = 0
    for sign, offset in product((1, -1), range(5)):
        mapping = [(offset + sign * i) % 5 for i in range(5)]
        for color_map in permutations(range(4)):
            row = tuple(color_map[c] for c in moved(q2, mapping))
            assert proper(row) and singleton(row) == mapping[2]
            q2_common_actions += 1
            unused = next(iter(set(range(4)) - set(row)))
            for old_v in range(5):
                if old_v == 2:
                    continue
                new_v = mapping[old_v]
                new = list(row)
                new[new_v] = unused
                assert proper(new) and len(set(new)) == 4
                q2_recolors += 1
    assert q2_common_actions == 240 and q2_recolors == 960

    return {'task': 'N45-SSG-independent-fixed-arithmetic',
            'scope': 'C5 rows, single-vertex recolor, whole-frame D5/S4, and disjoint ordered arc arithmetic only',
            'source_graphs_created': 0, 'source_trigger_count': None,
            'source_trigger_status': 'not computed; controls do not encode original SS sources',
            'original_faces_proved_by_controls': False,
            'all_literal_rows': len(all_rows), 'literal_three_rows': len(three),
            'literal_four_rows': len(four), 'canonical_pattern_order': patterns,
            'T4_indices': t4, 'singleton_to_q_index': q_index,
            'single_vertex_recolors': len(recolors),
            'two_unattached_point_row_checks': two_unattached,
            'one_unattached_point_covered_masks': single_point_masks,
            'ordered_arc_count': len(arcs), 'ordered_arc_identity_counts': dict(sorted(counts.items())),
            'q2_common_D5_S4_actions': q2_common_actions,
            'q2_single_vertex_recolors_after_common_actions': q2_recolors,
            'ordered_arc_witnesses': arcs,
            'result': 'all fixed arithmetic assertions hold; arbitrary-size paper reasoning remains separate'}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
