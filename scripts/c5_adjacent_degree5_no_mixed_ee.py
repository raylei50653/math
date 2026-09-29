#!/usr/bin/env python3
"""E-E source exclusion: six positive actual-support spans on a C5 disk.

The arbitrary-size topology and degree-list argument is in the report.
This certificate binds necessary source IDs, not realizing graphs or targets.
"""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2 import schema_audit
from c5_root_degree_excess import budget
from c5_single_spoke_cores import Q, U, PI, RHO, PERMS

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_be/observations.json'
OUT = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_ee/observations.json'
TABLE = OUT.with_name('exclusion_table.md')
NAMES = ('Cz', 'Dz', 'Ez', 'Cw', 'Dw', 'Ew')


def orders():
    found = set()
    for z, w in product(permutations(NAMES[:3]), permutations(NAMES[3:])):
        word = z + w
        i = word.index('Cz')
        found.add(word[i:] + word[:i])
    assert len(found) == 36
    return sorted(found)


def rotations(word):
    result = []
    for flips in product((False, True), repeat=2):
        ports = {n: (n + '_0',) for n in NAMES}
        for n, flip in zip(('Cz', 'Cw'), flips):
            ports[n] = (n + '_0', n + '_1')[::(-1 if flip else 1)]
        expanded = tuple(p for n in word for p in ports[n])
        assert len(expanded) == len(set(expanded)) == 8
        roots = {}
        for r, s, own in (('z', 'w', NAMES[:3]), ('w', 'z', NAMES[3:])):
            start = next(i for i, n in enumerate(word) if n in own and word[i-1] not in own)
            units = tuple(word[(start+j) % 6] for j in range(3))
            assert set(units) == set(own)
            roots[r] = (s,) + tuple(p for n in units for p in ports[n])
            assert len(roots[r]) == len(set(roots[r])) == 5
        result.append(dict(flips=flips, root_rotations=roots, neighborhood_word=expanded))
    return result


def lift_placements(length, zero_unit=None):
    """All sparse actual supports, not just consecutive-vertex intervals."""
    choices = {n: [s for k in ((1,) if n == zero_unit else range(2, length+1))
                   for s in combinations(range(length+1), k)
                   if s[-1]-s[0] < length] for n in NAMES}
    found = []
    for word in orders():
        def visit(j, end, assigned):
            if j == 6:
                for anchor in range(length):
                    found.append(dict(order=word, anchor=anchor,
                        lifts=tuple(assigned[n] for n in NAMES),
                        supports=tuple(tuple(sorted((anchor+i) % length for i in assigned[n]))
                                       for n in NAMES)))
                return
            for support in choices[word[j]]:
                if support[0] >= end and (j or support[0] == 0):
                    visit(j+1, support[-1], assigned | {word[j]: support})
        visit(0, 0, {})
    return found


def mask_packings(length, units):
    """Independent relaxed hull packing: all proper nonempty cyclic arcs.

    Drops root order and colors. Every valid lift placement injects into this
    larger domain; zero here is sufficient, positive counts are only controls.
    """
    masks = sorted({sum(1 << ((a+i) % length) for i in range(span))
                    for a in range(length) for span in range(1, length)})
    @lru_cache(None)
    def count(left, used):
        if not left:
            return 1
        return sum(count(left-1, used | mask) for mask in masks if not used & mask)
    return count(units, 0)


def side_kind(s):
    if s['root_boundary']:
        return 'A' if len(s['root_boundary']) == 2 else 'B'
    if s['ports'] == [2, 1, 1]:
        return 'E'
    assert s['ports'] == [2, 2]
    return 'D' if s['overlap_excess'] else 'C'


def build():
    original = json.loads(SOURCE.read_text())
    previous = json.loads(PREVIOUS.read_text())
    for path, data in ((SOURCE, original), (PREVIOUS, previous)):
        script = ROOT / 'scripts' / (path.parent.name + '.py')
        assert sha256(script.read_bytes()).hexdigest() == data['source_sha256']
    sides, joins = original['side_normal_forms'], original['abstract_conditions']['retained']
    records = []
    for jid, (i, j) in enumerate(joins):
        z, w = sides[i], sides[j]
        if side_kind(z) != 'E' or side_kind(w) != 'E':
            continue
        assert z['common'] == w['common']
        budgets = {r: budget(s) for r, s in (('z', z), ('w', w))}
        assert all(b['component_deficits'] == [1, 0, 0] and
                   (b['D'], b['O'], b['kappa']) == (1, 0, 0) for b in budgets.values())
        components = []
        for names, r, other, side in ((NAMES[:3], 'z', 'w', z), (NAMES[3:], 'w', 'z', w)):
            for col, name in enumerate(names):
                k, ban = side['ports'][col], side['forbidden'][col]
                assert len(ban) == 1
                components.append(dict(name=name, root=r, contacts=[f'{name}_{p}' for p in range(k)],
                    forbidden=ban, complete_relation_schema_color=ban[0] if k == 2 else None,
                    complete_unary_relation=[ban] if k == 1 else None,
                    external_path=dict(root_edge=[r, other], through_component='D'+other,
                                       through_contact='D'+other+'_0', ends_in='B', avoids=name),
                    min_span=1))
        records.append(dict(id=len(records), retained_join_id=jid, side_ids=(i, j),
            common=z['common'], z=z, w=w, source_budgets=budgets, original_edge=('z', 'w'),
            components=components, total_span_lower_bound=6, boundary_length=5,
            support_record_ids=[], classification='no_disk_source_six_positive_spans'))
    def key(r):
        return (r['common'], tuple(f[0] for f in r['z']['forbidden']),
                tuple(f[0] for f in r['w']['forbidden']))
    rebuilt = {(c, az, aw) for c in range(4)
               for az in permutations(sorted(U-{c})) for aw in permutations(sorted(U-{c}))}
    by_key = {key(r): r for r in records}
    assert len(records) == len(by_key) == 144 and set(by_key) == rebuilt
    assert (records[0]['retained_join_id'], records[0]['side_ids']) == (1428, (64, 64))
    assert tuple(PI[Q[RHO[i]]] for i in range(5)) == tuple(Q)
    frame_checks = 0
    for r in records:
        c, az, aw = key(r)
        r['root_swapped_id'] = by_key[c, aw, az]['id']
        r['reflected_id'] = by_key[PI[c], tuple(PI[a] for a in az), tuple(PI[a] for a in aw)]['id']
        r['single_contact_swap_ids'] = [by_key[c, a, b]['id'] for a, b in product(
            (az, (az[0], az[2], az[1])), (aw, (aw[0], aw[2], aw[1])))]
        for perm in PERMS:
            ez, ew = U-{perm[a] for a in az}, U-{perm[a] for a in aw}
            assert ez == ew == {perm[c]}
            assert not [(a, b) for a, b in product(ez, ew) if a != b]
            assert (perm[c], tuple(perm[a] for a in az), tuple(perm[a] for a in aw)) in by_key
            frame_checks += 1
    for r in records:
        assert records[r['root_swapped_id']]['root_swapped_id'] == r['id']
        assert records[r['reflected_id']]['reflected_id'] == r['id']
        assert len(set(r['single_contact_swap_ids'])) == 4
        for j, rid in enumerate(r['single_contact_swap_ids']):
            assert records[rid]['single_contact_swap_ids'][j] == r['id']
    schemas = schema_audit()
    templates = [dict(id=i, order=o, contact_rotations=rotations(o)) for i, o in enumerate(orders())]
    assert lift_placements(5) == [] and mask_packings(5, 6) == 0
    positive = lift_placements(6)
    assert len(positive) == 216 and mask_packings(6, 6) == 720
    assert mask_packings(5, 5) == 120
    relaxations = {}
    for n in ('Dz', 'Ez', 'Dw', 'Ew'):
        values = lift_placements(5, n)
        assert len(values) == 180
        relaxations[n] = dict(count=len(values), witness=values[0])
    relation = ((0, 0), (0, 1), (1, 0))
    assert set.intersection(*map(set, relation)) == {0}
    assert set.intersection(*map(set, product({0, 1}, repeat=2))) == set()
    old = set(previous['coverage_extension']['covered_source_join_ids'])
    added = {r['retained_join_id'] for r in records}
    assert len(old) == 1532 and len(added) == 144 and not old & added
    covered = old | added
    cells = {}
    for jid, (i, j) in enumerate(joins):
        label = '-'.join(sorted((side_kind(sides[i]), side_kind(sides[j]))))
        cells.setdefault(label, []).append(jid)
    for ids in cells.values():
        assert not (set(ids) & covered) or set(ids) <= covered
    remaining = {k: v for k, v in sorted(cells.items()) if not set(v) <= covered}
    assert len(cells)-len(remaining) == 8 and sum(map(len, remaining.values())) == 1872
    frontier = [dict(retained_join_id=jid, side_ids=ij) for jid, ij in enumerate(joins)
                if side_kind(sides[ij[0]]) == 'B' and side_kind(sides[ij[1]]) == 'C']
    assert len(frontier) == 180
    inputs = [SOURCE, PREVIOUS] + [ROOT/'scripts'/f'{n}.py' for n in (
        'c5_adjacent_degree5_no_mixed_t2', 'c5_adjacent_degree5_mixed_edge_shared',
        'c5_root_degree_excess', 'c5_single_spoke_cores')]
    return dict(schema=1, scope='arbitrary-size paper source exclusion plus finite controls; no targets, realization or Lean theorem',
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        summary=dict(original_source_joins=144, disk_source_exclusions=144, necessary_support_records=0,
            target_queries=0, target_accepts=0, new_source_minor_certificates=0,
            cyclic_words=36, contact_rotations=144, q_binary_schemas=380,
            whole_source_root_swaps=144, source_reflections=144, unary_swap_checks=576,
            common_color_frame_checks=frame_checks, c6_positive_placements=216,
            relaxed_unary_placements=720),
        original_records=records, q_complete_binary_schemas=schemas, rotation_templates=templates,
        geometric_control=dict(c5_six_positive_lifts=[], c5_six_positive_mask_packings=0,
            c5_five_positive_mask_packings=120, c6_six_positive_mask_packings=720,
            c6_positive_witness=positive[0], unary_zero_span_relaxations=relaxations,
            complete_relation_not_marginals=True),
        coverage_extension=dict(previous_covered_source_joins=len(old),
            newly_covered_source_join_ids=sorted(added), covered_source_join_ids=sorted(covered),
            covered_source_joins=len(covered), remaining_source_joins=3548-len(covered),
            covered_unordered_cells=8, remaining_unordered_cells=7, remaining_cells=remaining),
        next_frontier=dict(class_name='B-C', source_sha256=sha256(SOURCE.read_bytes()).hexdigest(), records=frontier))


def render(data):
    lines = ['# E–E 六份正跨度來源排除', '',
        '144 份原必要接合全無 disk 支援；0 target 查詢，沒有把空纖維算作接受。', '',
        '| ID | 原 join ID | 原側 IDs | 共同 c | z 禁色 | w 禁色 | 最小總跨度 |',
        '| ---: | ---: | --- | ---: | --- | --- | ---: |']
    for r in data['original_records']:
        lines.append(f"| {r['id']} | {r['retained_join_id']} | {r['side_ids']} | {r['common']} | {r['z']['forbidden']} | {r['w']['forbidden']} | 6 > 5 |")
    lines += ['', '[完整 schemas、具名接點及逐筆來源](observations.json)。',
              '[紙面證明與證據界線](../../docs/c5_adjacent_degree5_no_mixed_ee.md)。', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    for path, payload in ((OUT, json.dumps(data, sort_keys=True, indent=2)+'\n'), (TABLE, render(data))):
        if args.check:
            assert path.read_bytes() == payload.encode(), f'certificate differs: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(data['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
