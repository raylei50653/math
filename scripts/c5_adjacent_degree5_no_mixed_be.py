#!/usr/bin/env python3
"""B-E necessary same-source supports and complete-relation target transport.

Arbitrary-size coverage is proved in the report; no realization is claimed.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2 import schema_audit, stable_schema_ids
from c5_adjacent_degree5_singleton_long_arc import component_options, valid_q_support
from c5_root_degree_excess import budget
from c5_single_spoke_cores import Q, U, PI, RHO, TARGETS

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_no_mixed/observations.json"
PREVIOUS = ROOT / "artifacts/c5_adjacent_degree5_no_mixed_bb/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_no_mixed_be/observations.json"
TABLE = OUT.with_name("support_table.md")
NAMES = ("Cz", "Dz", "z0", "Cw", "Dw", "Ew")
COMPONENTS = (("Cz", "z", 0, 0, 2), ("Dz", "z", 1, 1, 1),
              ("Cw", "w", 0, 3, 2), ("Dw", "w", 1, 4, 1), ("Ew", "w", 2, 5, 1))


def cardinalities(name):
    return range(2, 6) if name != "z0" else (1,)


def geometries():
    choices = {name: [s for k in cardinalities(name) for s in combinations(range(6), k)
                      if max(s) - min(s) < 5] for name in NAMES}
    orders = set()
    for z, w in product(permutations(NAMES[:3]), permutations(NAMES[3:])):
        order = z + w
        i = order.index("Cz")
        orders.add(order[i:] + order[:i])
    result = {}
    for order in sorted(orders):
        def visit(j, end, assigned):
            if j == 6:
                for anchor in range(5):
                    supports = tuple(tuple(sorted((anchor + i) % 5 for i in assigned[n]))
                                     for n in NAMES)
                    result.setdefault(supports, []).append(dict(
                        order=order, anchor=anchor, lifts=tuple(assigned[n] for n in NAMES)))
                return
            for support in choices[order[j]]:
                if min(support) >= end and (j or min(support) == 0):
                    visit(j + 1, max(support), assigned | {order[j]: support})
        visit(0, 0, {})
    return result


def independent_geometries():
    """Actual support hulls on each whole side, with disjoint frame-edge masks."""
    sides = []
    for names in (NAMES[:3], NAMES[3:]):
        found = set()
        choices = [[s for k in cardinalities(n) for s in combinations(range(5), k)] for n in names]
        for supports in product(*choices):
            for anchor in set().union(*map(set, supports)):
                lifts = [sorted((i - anchor) % 5 for i in s) for s in supports]
                if any(not (a[-1] <= b[0] or b[-1] <= a[0])
                       for a, b in combinations(lifts, 2)):
                    continue
                span = max(s[-1] for s in lifts)
                mask = sum(1 << ((anchor + j) % 5) for j in range(span))
                found.add((supports, mask))
        sides.append(found)
    # Group by masks to avoid an unnecessarily large all-pairs product.
    groups = []
    for side in sides:
        by_mask = {}
        for supports, mask in side:
            by_mask.setdefault(mask, set()).add(supports)
        groups.append(by_mask)
    return {a + b for ma, aa in groups[0].items() for mb, bb in groups[1].items()
            if not ma & mb for a, b in product(aa, bb)}


def rotations(order):
    result = []
    for flips in product((False, True), repeat=2):
        expansion = {n: (n,) for n in NAMES}
        for name, flip in zip(("Cz", "Cw"), flips):
            ports = (name + "_0", name + "_1")
            expansion[name] = ports[::-1] if flip else ports
        expansion["Dz"] = ("Dz_0",)
        expansion["Dw"] = ("Dw_0",)
        expansion["Ew"] = ("Ew_0",)
        roots = {}
        for root, own, other in (("z", NAMES[:3], "w"), ("w", NAMES[3:], "z")):
            start = next(i for i, n in enumerate(order) if n in own and order[i - 1] not in own)
            units = tuple(order[(start + j) % 6] for j in range(3))
            assert set(units) == set(own)
            roots[root] = (other,) + tuple(p for n in units for p in expansion[n])
            assert len(roots[root]) == len(set(roots[root])) == 5
        result.append(dict(contact_flips=flips, root_rotations=roots,
                           neighborhood_word=tuple(p for n in order for p in expansion[n])))
    return result


def verify_placement(supports, placement, contact_rotations):
    """Check named incidences and lifts independently of their generators."""
    order = placement["order"]
    assert len(order) == len(NAMES) and set(order) == set(NAMES) and order[0] == "Cz"
    side = [n in NAMES[:3] for n in order]
    assert sum(side[i] != side[i - 1] for i in range(6)) == 2
    lifts = dict(zip(NAMES, placement["lifts"], strict=True))
    assert len(supports) == 6 and 0 <= placement["anchor"] < 5
    assert min(lifts["Cz"]) == 0 and max(lifts[order[-1]]) <= 5
    for i, (name, support) in enumerate(zip(NAMES, supports, strict=True)):
        values = lifts[name]
        assert tuple(sorted(set(values))) == tuple(values)
        assert len(values) in cardinalities(name) and max(values) - min(values) < 5
        assert tuple(sorted((placement["anchor"] + j) % 5 for j in values)) == tuple(support)
    assert all(max(lifts[a]) <= min(lifts[b]) for a, b in zip(order, order[1:]))
    assert sum(max(lifts[n]) - min(lifts[n]) for n, _, _, _, _ in COMPONENTS) == 5
    expected = {"z": {"w", "Cz_0", "Cz_1", "Dz_0", "z0"},
                "w": {"z", "Cw_0", "Cw_1", "Dw_0", "Ew_0"}}
    assert len(contact_rotations) == 4
    assert {tuple(r["contact_flips"]) for r in contact_rotations} == set(product((False, True), repeat=2))
    for record in contact_rotations:
        word = record["neighborhood_word"]
        assert len(word) == len(set(word)) == 8
        assert set(word) == (expected["z"] | expected["w"]) - {"z", "w"}
        compressed = []
        for port in word:
            unit = port.split("_")[0]
            if not compressed or compressed[-1] != unit:
                compressed.append(unit)
        assert tuple(compressed) == tuple(order)
        for name, flip in zip(("Cz", "Cw"), record["contact_flips"], strict=True):
            ports = [name + "_0", name + "_1"]
            assert [p for p in word if p.startswith(name + "_")] == (ports[::-1] if flip else ports)
        for root, other, units in (("z", "w", NAMES[:3]), ("w", "z", NAMES[3:])):
            rotation = record["root_rotations"][root]
            assert len(rotation) == 5 and set(rotation) == expected[root] and rotation[0] == other
            start = next(i for i, p in enumerate(word)
                         if p.split("_")[0] in units and word[i - 1].split("_")[0] not in units)
            assert tuple(rotation[1:]) == tuple(word[(start + j) % 8] for j in range(4))


def bind_sources(original, previous):
    sides = original['side_normal_forms']
    sources = []
    for jid, (i, j) in enumerate(original['abstract_conditions']['retained']):
        z, w = sides[i], sides[j]
        if (len(z['root_boundary']), z['ports'], len(w['root_boundary']), w['ports']) != (1, [2, 1], 0, [2, 1, 1]):
            continue
        budgets = {r: budget(s) for r, s in (('z', z), ('w', w))}
        assert budgets['z']['component_deficits'] == [1, 0]
        assert budgets['w']['component_deficits'] == [1, 0, 0]
        sources.append(dict(id=len(sources), retained_join_id=jid, side_ids=(i, j),
                            common=z['common'], z=z, w=w, source_budgets=budgets))
    def key(s):
        return (tuple(s['z']['root_boundary']), s['common'],
                tuple(map(tuple, s['z']['forbidden'])), tuple(map(tuple, s['w']['forbidden'])))
    rebuilt = {((i,), c, tuple((a,) for a in az), tuple((a,) for a in aw))
               for i in range(5) for c in U - {Q[i]}
               for az in permutations(sorted(U - {Q[i], c}))
               for aw in permutations(sorted(U - {c}))}
    assert len(sources) == 180 and {key(s) for s in sources} == rebuilt
    frontier = previous['next_frontier']
    assert frontier['source_sha256'] == sha256(SOURCE.read_bytes()).hexdigest()
    assert frontier['records'] == [dict(retained_join_id=s['retained_join_id'], side_ids=list(s['side_ids'])) for s in sources]
    assert (sources[0]['retained_join_id'], sources[0]['side_ids']) == (2136, (91, 64))
    return sources


def row_evidence(source, supports, row):
    components = [dict(name=n, **component_options(k, supports[pos], tuple(source[r]['forbidden'][col]), row))
                  for n, r, col, pos, k in COMPONENTS]
    assert all(c['exact'] and len(c['options']) == 1 for c in components)
    bans = tuple(c['options'][0] for c in components)
    ez = U - {row[i] for i in source['z']['root_boundary']} - set(bans[0]) - set(bans[1])
    ew = U - set(bans[2]) - set(bans[3]) - set(bans[4])
    pairs = sorted((a, b) for a, b in product(ez, ew) if a != b)
    direct = [(a, b) for a, b in product(range(4), repeat=2)
              if a != b and all(a != row[i] for i in source['z']['root_boundary'])
              and all((a if r == 'z' else b) not in f for (_, r, _, _, _), f in zip(COMPONENTS, bans))]
    assert pairs == direct
    return dict(row=row, components=components, forbidden_sets=bans,
                residuals=(sorted(ez), sorted(ew)), root_pairs=pairs,
                witness=pairs[0] if pairs else None,
                status='accept' if pairs else 'reject')


def audit_relations(records, sources, schemas):
    lookup = {(s['id'], r['supports']): r for s in sources for r in records if r['source_id'] == s['id']}
    def key(s):
        return (tuple(s['z']['root_boundary']), tuple(map(tuple, s['z']['forbidden'])),
                tuple(map(tuple, s['w']['forbidden'])))
    by_key = {key(s): s['id'] for s in sources}
    transported = reflected = reversed_relations = 0
    for rec in records:
        src = sources[rec['source_id']]
        zf = tuple((PI[f[0]],) for f in src['z']['forbidden'])
        wf = tuple((PI[f[0]],) for f in src['w']['forbidden'])
        sid = by_key[(tuple(RHO[i] for i in src['z']['root_boundary']), zf, wf)]
        support = tuple(tuple(sorted(RHO[i] for i in s)) for s in rec['supports'])
        twin = lookup[sid, support]
        rec['reflection'] = dict(record_id=twin['id'])
        for t in rec['targets']:
            raw = tuple(PI[t['row'][RHO[i]]] for i in range(5))
            after = row_evidence(sources[sid], support, raw)
            moved = tuple(tuple(sorted(PI[c] for c in f)) for f in t['forbidden_sets'])
            assert moved == after['forbidden_sets']
            assert sorted((PI[a], PI[b]) for a, b in t['root_pairs']) == after['root_pairs']
            reflected += 1
        for n, root, col, pos, k in COMPONENTS:
            h = src[root]['forbidden'][col][0]
            other = n
            if k == 2:
                rels = [schemas[h][i] for i in rec['q_schema_ids'][n]]
                assert {tuple(sorted(tuple(PI[c] for c in tup) for tup in rel)) for rel in rels} == {
                    tuple(sorted(schemas[PI[h]][i])) for i in twin['q_schema_ids'][other]}
                assert {tuple(sorted(tuple(reversed(tup)) for tup in rel)) for rel in rels} == {
                    tuple(sorted(rel)) for rel in rels}
                reversed_relations += len(rels)
            else:
                rels = [rec['q_single_contact_relations'][n]]
                assert twin['q_single_contact_relations'][other] == ((PI[h],),)
            for t in rec['targets']:
                c = next(c for c in t['components'] if c['name'] == n)
                perm = c['permutation']
                assert all(perm[Q[i]] == t['row'][i] for i in rec['supports'][pos])
                for rel in rels:
                    moved = [tuple(perm[v] for v in tup) for tup in rel]
                    assert tuple(sorted(set.intersection(*map(set, moved)))) == c['options'][0]
                    transported += 1
    return dict(whole_relation_transports=transported, contact_reversals=reversed_relations,
                literal_target_reflections=reflected)


def root_swap_audit(original, records, sources, geometry_records, templates):
    joins = {tuple(pair): i for i, pair in enumerate(original['abstract_conditions']['retained'])}
    swapped_sources = []
    for s in sources:
        ids = s['side_ids'][::-1]
        swapped_sources.append(dict(source_id=s['id'], retained_join_id=joins[ids], side_ids=ids))
    for rec in records:
        src = sources[rec['source_id']]
        rec['root_swapped_context'] = dict(
            root_boundary={'z': [], 'w': src['z']['root_boundary']},
            components=[dict(name=n, root={'z': 'w', 'w': 'z'}[r],
                             contacts=[f'{n}_{i}' for i in range(k)], support=rec['supports'][pos])
                        for n, r, _, pos, k in COMPONENTS],
            original_spoke=('w', f"b{src['z']['root_boundary'][0]}"), edge=('w', 'z'))
        for placement in geometry_records[rec['geometry_id']]['placements']:
            for rotation in templates[placement['rotation_template_id']]['contact_rotations']:
                moved = {dict(z='w', w='z')[r]: tuple(dict(z='w', w='z').get(v, v) for v in word)
                         for r, word in rotation['root_rotations'].items()}
                assert all(len(set(word)) == 5 for word in moved.values())
                assert moved['z'][0] == 'w' and moved['w'][0] == 'z'
        for t in [rec['q'], *rec['targets']]:
            row, fs = t['row'], t['forbidden_sets']
            direct = [(a, b) for a, b in product(range(4), repeat=2)
                      if a != b and all(b != row[i] for i in src['z']['root_boundary'])
                      and all((b if r == 'z' else a) not in f for (_, r, _, _, _), f in zip(COMPONENTS, fs))]
            assert sorted((b, a) for a, b in t['root_pairs']) == direct
    return swapped_sources


def negative_controls(geometry):
    # Five positive spans cannot fit if one unit is stretched to span two.
    s = next(iter(sorted(geometry)))
    bad = list(s)
    bad[0] = (0, 1, 2)
    assert tuple(bad) not in geometry
    # Original unary components must have positive span; they are not spokes.
    for i in (1, 4, 5):
        bad = list(s)
        bad[i] = (s[i][0],)
        assert tuple(bad) not in geometry
    # Identical marginals lose the always-used color of a complete relation.
    relation = ((0, 0), (0, 1), (1, 0))
    marginals = tuple(set(t[i] for t in relation) for i in range(2))
    assert set.intersection(*map(set, relation)) == {0}
    assert set.intersection(*map(set, product(*marginals))) == set()
    return ['positive_span_overflow', 'Dz_not_spoke', 'Dw_not_spoke', 'Ew_not_spoke',
            'complete_relation_not_marginals']


def build():
    original, previous = json.loads(SOURCE.read_text()), json.loads(PREVIOUS.read_text())
    sources = bind_sources(original, previous)
    geometry = geometries()
    assert set(geometry) == independent_geometries()
    assert len(geometry) == sum(map(len, geometry.values())) == 180
    schemas = schema_audit()
    records, geometry_records, templates = [], [], []
    template_ids = {}
    for supports, placements in sorted(geometry.items()):
        gid = len(geometry_records)
        for placement in placements:
            order = placement['order']
            if order not in template_ids:
                template_ids[order] = len(templates)
                templates.append(dict(id=len(templates), order=order, contact_rotations=rotations(order)))
            placement['rotation_template_id'] = template_ids[order]
            verify_placement(supports, placement, templates[template_ids[order]]['contact_rotations'])
            assert all(max(placement['lifts'][pos])-min(placement['lifts'][pos]) == 1 for _, _, _, pos, _ in COMPONENTS)
        geometry_records.append(dict(id=gid, supports=supports, placements=placements))
        for src in sources:
            if supports[2] != tuple(src['z']['root_boundary']):
                continue
            if not all(len({Q[i] for i in supports[pos]}) >= 2 and
                       valid_q_support(supports[pos], tuple(src[root]['forbidden'][col]))
                       for _, root, col, pos, _ in COMPONENTS):
                continue
            ids = {n: stable_schema_ids(src[root]['forbidden'][col][0], supports[pos])
                   for n, root, col, pos, k in COMPONENTS if k == 2}
            assert all(len(v) == 17 for v in ids.values())
            q = row_evidence(src, supports, Q)
            assert q['residuals'] == ([src['common']],)*2 and not q['root_pairs']
            targets = [row_evidence(src, supports, row) for row in TARGETS]
            assert all(t['status'] == 'accept' for t in targets)
            records.append(dict(id=len(records), source_id=src['id'], source_side_ids=src['side_ids'],
                                geometry_id=gid, supports=supports, q_schema_ids=ids,
                                q_single_contact_relations={n: ((src[root]['forbidden'][col][0],),)
                                                           for n, root, col, _, k in COMPONENTS if k == 1},
                                q=q, targets=targets))
    assert len(records) == 144
    # Dropping the original zw would make every rejected q join nonempty.
    assert all(r['q']['residuals'][0] and r['q']['residuals'][1] for r in records)
    audits = audit_relations(records, sources, schemas)
    swaps = root_swap_audit(original, records, sources, geometry_records, templates)
    fibers = [dict(source_id=s['id'], retained_join_id=s['retained_join_id'], side_ids=s['side_ids'],
                   support_record_ids=[r['id'] for r in records if r['source_id'] == s['id']]) for s in sources]
    for f in fibers:
        f['classification'] = 'necessary_supports_present' if f['support_record_ids'] else 'no_compatible_disk_support'
    old = set(previous['coverage_extension']['covered_source_join_ids'])
    added = {s['retained_join_id'] for s in sources} | {s['retained_join_id'] for s in swaps}
    assert len(old) == 1172 and len(added) == 360 and not old & added
    negatives = negative_controls(geometry) + ['original_zw_required']
    assert sum(bool(f['support_record_ids']) for f in fibers) == 60
    inputs = [str(p.relative_to(ROOT)) for p in (SOURCE, PREVIOUS)] + ['scripts/'+n+'.py' for n in (
        'c5_adjacent_degree5_no_mixed_t2', 'c5_adjacent_degree5_mixed_edge_shared',
        'c5_adjacent_degree5_singleton_long_arc', 'c5_root_degree_excess', 'c5_single_spoke_cores',
        'c5_single_spoke_two_two_external', 'c5_single_spoke_two_two_minor')]
    summary = dict(original_frontier=len(sources), geometric_supports=len(geometry),
                   contact_rotation_checks=4*len(geometry), necessary_support_records=len(records),
                   source_records_with_support=sum(bool(f['support_record_ids']) for f in fibers),
                   empty_source_fibers=sum(not f['support_record_ids'] for f in fibers),
                   target_queries=2*len(records), complete_relation_target_accepts=2*len(records),
                   unresolved_queries=0, source_minor_exclusions=0, target_minor_queries=0,
                   whole_source_root_swaps=len(records), complete_join_root_swaps=3*len(records),
                   negative_controls=len(negatives), **audits)
    return dict(schema=1, scope='necessary same-source supports; arbitrary-size paper reduction; no disk realization or Lean theorem',
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
                summary=summary, original_records=sources, source_fibers=fibers,
                geometries=geometry_records, rotation_templates=templates,
                q_complete_binary_schemas=schemas, records=records, root_swapped_sources=swaps,
                negative_controls=negatives, open_queries=[],
                coverage_extension=dict(previous_covered_source_joins=len(old),
                    newly_covered_source_join_ids=sorted(added), covered_source_join_ids=sorted(old|added),
                    covered_source_joins=len(old|added), remaining_source_joins=3548-len(old|added),
                    covered_unordered_cells=7, remaining_unordered_cells=8))


def render(data):
    lines = ['# B–E 五分量必要支援與完整關係搬運', '',
             '支援順序 Cz / Dz / z0 / Cw / Dw / Ew；三個 unary 皆為原分量。',
             '144 份支援、288 個 target 全接受；必要表不是 disk 實現。', '',
             '| ID | 原 join ID | 原側 IDs | 支援 | p₁ root witness | p₂ root witness |',
             '| ---: | ---: | --- | --- | --- | --- |']
    for r in data['records']:
        src = data['original_records'][r['source_id']]
        support = ' / '.join(''.join(map(str, s)) for s in r['supports'])
        lines.append(f"| {r['id']} | {src['retained_join_id']} | {r['source_side_ids']} | {support} | {r['targets'][0]['witness']} | {r['targets'][1]['witness']} |")
    lines += ['', '## 全部原 ID 纖維', '', '| 子表 ID | 原 join ID | 原側 IDs | 支援數 |', '| ---: | ---: | --- | ---: |']
    for f in data['source_fibers']:
        lines.append(f"| {f['source_id']} | {f['retained_join_id']} | {f['side_ids']} | {len(f['support_record_ids'])} |")
    lines += ['', '[完整關係、rotations 與證書](observations.json)。',
              '[前提、紙面覆蓋及證據界線](../../docs/c5_adjacent_degree5_no_mixed_be.md)。', '']
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
