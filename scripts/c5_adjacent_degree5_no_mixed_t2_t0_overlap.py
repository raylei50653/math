#!/usr/bin/env python3
"""Exclude no-mixed t_z=2,(2), t_w=0,(2,2), D_w=0,O_w=1 sources.

Both original saturated components are checked separately. The report supplies
arbitrary-size coverage; supports and minor skeletons are not realizing graphs.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import c5_adjacent_degree5_no_mixed_t2_t0_pairs as previous
from c5_adjacent_degree5_no_mixed_t2_t1_bridge import (
    frame_evidence, minor_control, root_pairs, swapped,
)
from c5_single_spoke_cores import Q, U, PI, RHO
from c5_single_spoke_frame_arc import admissible_supports, verify_arcs
from c5_single_spoke_two_two_external import STYLES
from c5_single_spoke_two_two_minor import verify_minor
from c5_root_degree_excess import budget

ROOT = Path(__file__).resolve().parents[1]
SOURCE, PREVIOUS, SCOPE = previous.SOURCE, previous.OUT, previous.SCOPE
OUT = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_t0_overlap/observations.json'
TABLE = OUT.with_name('support_table.md')
COMPONENTS = previous.COMPONENTS


def bind_sources(data):
    sides, records = data['side_normal_forms'], []
    for jid, (i, j) in enumerate(data['abstract_conditions']['retained']):
        z, w = sides[i], sides[j]
        if (len(z['root_boundary']), z['ports'], len(w['root_boundary']), w['ports'],
            w['capacity_deficit'], w['overlap_excess']) != (2, [2], 0, [2, 2], 0, 1):
            continue
        records.append(dict(id=len(records), retained_join_id=jid, side_ids=(i, j), z=z, w=w,
            common=z['common'], source_budgets={r: budget(s) for r, s in (('z', z), ('w', w))}))
    rebuilt = set()
    for sz in combinations(range(5), 2):
        seen = {Q[i] for i in sz}
        if len(seen) != 2:
            continue
        for c in U - seen:
            fz = tuple(sorted(U - seen - {c}))
            for h, a, b in permutations(sorted(U - {c})):
                rebuilt.add((sz, c, fz, (tuple(sorted((h, a))), tuple(sorted((h, b))))))
    assert {(tuple(s['z']['root_boundary']), s['common'], tuple(s['z']['forbidden'][0]),
             tuple(map(tuple, s['w']['forbidden']))) for s in records} == rebuilt
    assert len(records) == 96
    prior = json.loads(PREVIOUS.read_text())['next_frontier']
    assert prior['source_sha256'] == sha256(SOURCE.read_bytes()).hexdigest()
    assert prior['records'] == [dict(retained_join_id=s['retained_join_id'], side_ids=list(s['side_ids'])) for s in records]
    assert (records[0]['retained_join_id'], records[0]['side_ids']) == (3040, (133, 30))
    return records


def evidence(ctx):
    result = []
    for k in (1, 2):
        comp = ctx['components'][k]
        pair = tuple(comp['source_forbidden'])
        assert len(pair) == len(comp['contacts']) == 2
        family = admissible_supports(Q, tuple(comp['support']), pair)
        assert family, 'whole actual support must preserve the source pair'
        frame = frame_evidence(ctx, k, family)
        # Each successful component has an original w-z-spoke route already.
        spoke_witnesses = [w for w in frame['witnesses'] if w['route']['mode'] == 'other_spoke']
        assert bool(spoke_witnesses) == frame['eliminated']
        result.append(dict(component=k, name=comp['name'], ordered_contacts=comp['contacts'],
            source_forbidden=pair, frame=frame, eliminated=frame['eliminated'],
            selected_witness=spoke_witnesses[0] if spoke_witnesses else None))
    return dict(components=result, eliminated=any(e['eliminated'] for e in result))


def compare_reflected(a, b):
    assert a['eliminated'] == b['eliminated']
    for x, y in zip(a['components'], b['components'], strict=True):
        assert x['component'] == y['component'] and x['eliminated'] == y['eliminated']
        assert {PI[c] for c in x['source_forbidden']} == set(y['source_forbidden'])
        fx, fy = x['frame'], y['frame']
        assert {tuple(sorted(RHO[i] for i in t)) for t in fx['supports']} == set(map(tuple, fy['supports']))
        keys = {(tuple(map(tuple, w['frame_arcs'])), w['route']['mode'], w['route']['component'],
                 w['route']['landing']) for w in fy['witnesses']}
        for w in fx['witnesses']:
            arcs = tuple(tuple(sorted(RHO[i] for i in s)) for s in w['frame_arcs'])
            verify_arcs([s[0] for s in arcs], arcs)
            assert (arcs, w['route']['mode'], w['route']['component'], RHO[w['route']['landing']]) in keys


def symmetry_audit(records, sources, schemas):
    def key(s):
        return (tuple(s['z']['root_boundary']), tuple(s['z']['forbidden'][0]), tuple(map(tuple, s['w']['forbidden'])))
    source_lookup = {key(s): s for s in sources}
    lookup = {(r['source_id'], r['supports']): r for r in records}
    for r in records:
        s = sources[r['source_id']]
        k = key(s)
        moved = (tuple(sorted(RHO[i] for i in k[0])), tuple(sorted(PI[c] for c in k[1])),
                 tuple(tuple(sorted(PI[c] for c in f)) for f in k[2]))
        sr = source_lookup[moved]
        ss = tuple(tuple(sorted(RHO[i] for i in t)) for t in r['supports'])
        ss = (ss[0], *sorted(ss[1:3]), *ss[3:])
        ref = lookup[sr['id'], ss]
        r['reflected_id'] = ref['id']
        compare_reflected(r['source_evidence'], ref['source_evidence'])
        for name, root, col, _ in COMPONENTS:
            f = s[root]['forbidden'][col]
            fk, fr = ','.join(map(str, f)), ','.join(map(str, sorted(PI[c] for c in f)))
            assert {tuple(sorted(tuple(PI[c] for c in t) for t in schemas[fk][i])) for i in r['q_schema_ids'][name]} == {
                tuple(sorted(schemas[fr][i])) for i in ref['q_schema_ids'][name]}
        twin_source = source_lookup[(k[0], k[1], k[2][::-1])]
        twin = lookup[twin_source['id'], (*r['supports'][:3], r['supports'][4], r['supports'][3])]
        r['component_swapped_id'] = twin['id']
        for name, other in (('Cz', 'Cz'), ('Cw', 'Dw'), ('Dw', 'Cw')):
            assert r['q_schema_ids'][name] == twin['q_schema_ids'][other]
        for a, b in zip(r['source_evidence']['components'], reversed(twin['source_evidence']['components']), strict=True):
            frame = previous.canonical(a['frame'])
            for w in frame['witnesses']:
                w['route']['component'] = {'Cw': 'Dw', 'Dw': 'Cw'}.get(w['route']['component'], w['route']['component'])
                w['route']['path'] = [v.replace('Cw_', 'TMP_').replace('Dw_', 'Cw_').replace('TMP_', 'Dw_') for v in w['route']['path']]
            assert sorted(frame['witnesses'], key=lambda w: json.dumps(w, sort_keys=True)) == sorted(
                previous.canonical(b['frame']['witnesses']), key=lambda w: json.dumps(w, sort_keys=True))
            assert frame['supports'] == b['frame']['supports'] and a['eliminated'] == b['eliminated']
        ctx = previous.context(r, s)
        sw = evidence(swapped(ctx))
        renamed = previous.canonical(r['source_evidence'])
        for e in renamed['components']:
            for w in e['frame']['witnesses'] + ([e['selected_witness']] if e['selected_witness'] else []):
                w['route']['path'] = [dict(z='w', w='z').get(v, v) for v in w['route']['path']]
        assert renamed == previous.canonical(sw)


def minor_controls(records, sources):
    controls, modes = [], {}
    for r in records:
        ctx = previous.context(r, sources[r['source_id']])
        for e in r['source_evidence']['components']:
            if not e['eliminated']:
                continue
            assert e['frame']['reason'] == 'original_path_K5'
            for length in (1, 3, 5):
                controls.append(dict(purpose='source', **minor_control(ctx, e['component'], e['selected_witness'], length)))
            for w in e['frame']['witnesses']:
                score = 1
                for arc in w['frame_arcs'][:2]:
                    score *= len(set(ctx['components'][e['component']]['support']) & set(arc))
                mode = w['route']['mode']
                if mode not in modes or score > modes[mode][0]:
                    modes[mode] = (score, ctx, e['component'], w)
    assert len(controls) == 1200 and set(modes) == {'other_spoke', 'other_root_component', 'same_root_component'}
    for _, ctx, k, w in modes.values():
        possible = [sorted(set(ctx['components'][k]['support']) & set(a)) for a in w['frame_arcs'][:2]]
        supply = list(product(*possible))
        for length, styles, ext, suppliers in product((1, 5), product(STYLES, repeat=2), (1, 3), product(supply, repeat=2)):
            controls.append(dict(purpose='route_and_tether_control',
                **minor_control(ctx, k, w, length, styles, suppliers, ext)))
    assert any(c['suppliers'][0] != c['suppliers'][1] for c in controls)
    return controls


def negative_controls(geometry, records, sources, controls):
    result = []
    ss, placements = next(iter(sorted(geometry.items())))
    placement, templates = placements[0], previous.rotations(placements[0]['order'])
    bad_order, bad_contacts = previous.canonical(placement), previous.canonical(templates)
    bad_order['order'] = ['Cz', 'Cw', 'z0', 'Dw', 'z1']
    bad_contacts[0]['root_rotations']['w'][-1] = bad_contacts[0]['root_rotations']['w'][-2]
    for name, p, t in [('interleaved_root_units', bad_order, templates), ('merged_named_contacts', placement, bad_contacts)]:
        try:
            previous.verify_placement(ss, p, t)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    rel = ((0, 1), (1, 0))
    marginals = tuple(product({t[0] for t in rel}, {t[1] for t in rel}))
    assert set.intersection(*map(set, rel)) == {0, 1} and set.intersection(*map(set, marginals)) == set()
    result.append('pair_marginals_lose_both_source_bans')
    assert not previous.valid_q_support((), (0, 1)) and not previous.valid_q_support((0, 2), (0, 1))
    result.append('empty_or_monochromatic_pair_support')
    for k in (0, 1):
        misses = [r['id'] for r in records if not r['source_evidence']['components'][k]['eliminated']]
        assert len(misses) == 12
        result.append(dict(name=f'checking_only_component_{k+1}_misses_sources', missed_record_ids=misses))
    r = records[4]
    e = r['source_evidence']['components'][0]
    assert e['frame']['supports'] == [[1, 2], [2, 3], [1, 2, 3]] and not e['eliminated']
    ctx = previous.context(r, sources[r['source_id']])
    assert all(frame_evidence(ctx, 1, (set(t),))['eliminated'] for t in e['frame']['supports'])
    result.append('per_support_partitions_do_not_supply_one_fixed_partition')
    assert frame_evidence(ctx, 1, ())['reason'] == 'no_possible_bag'
    result.append('empty_family_is_not_a_K5_witness')
    base = next(c for c in controls if c['record_id'] == 0 and c['component'] == 1 and c['length'] == 3)
    edges, bags = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    bad = [('missing_original_zw', edges - {('w', 'z')}, bags),
           ('missing_external_spoke', edges - {('b4', 'z')}, bags),
           ('missing_original_bridge', edges - {tuple(sorted(base['path'][:2]))}, bags),
           ('missing_original_contact', edges - {tuple(sorted(('w', base['path'][0])))}, bags),
           ('overlapping_branch_sets', edges, [bags[0] | {'w'}, *bags[1:]])]
    for name, es, bs in bad:
        try:
            verify_minor(es, bs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    return result


def coverage_extension(data, sources):
    old = json.loads(PREVIOUS.read_text())
    assert old['inputs_sha256'][str(SOURCE.relative_to(ROOT))] == sha256(SOURCE.read_bytes()).hexdigest()
    covered = set(old['coverage_extension']['covered_source_join_ids'])
    lookup = {tuple(pair): i for i, pair in enumerate(data['abstract_conditions']['retained'])}
    added = {s['retained_join_id'] for s in sources} | {lookup[s['side_ids'][::-1]] for s in sources}
    assert len(covered) == 744 and len(added) == 192 and not covered & added
    all_covered = covered | added
    # All and only the cells with a t=2 side are now covered.
    sides = data['side_normal_forms']
    assert all_covered == {i for i, pair in enumerate(data['abstract_conditions']['retained'])
                          if any(len(sides[j]['root_boundary']) == 2 for j in pair)}
    return dict(previous_sha256=sha256(PREVIOUS.read_bytes()).hexdigest(),
        newly_covered_source_join_ids=sorted(added), covered_source_join_ids=sorted(all_covered),
        new_closure='source_exclusion', covered_ordered_cells=9, covered_unordered_cells=5,
        remaining_unordered_cells=10, covered_source_joins=936, remaining_source_joins=2612,
        scope='subtype coverage; all t=2-side cells covered; not counts of realizing graphs')


def next_frontier(data):
    sides, rows = data['side_normal_forms'], []
    for jid, pair in enumerate(data['abstract_conditions']['retained']):
        if all(len(sides[i]['root_boundary']) == 1 and sides[i]['ports'] == [2, 1] for i in pair):
            rows.append(dict(retained_join_id=jid, side_ids=pair))
    assert len(rows) == 236 and rows[0] == dict(retained_join_id=2142, side_ids=[91, 91])
    return dict(scope='B-B: both t=1,(2,1); IDs only, no new support or target audit',
        source_sha256=sha256(SOURCE.read_bytes()).hexdigest(), records=rows,
        first_sides=[sides[i] for i in rows[0]['side_ids']])


def build():
    data = json.loads(SOURCE.read_text())
    sources, geometry, schemas = bind_sources(data), previous.geometries(), previous.schema_audit()
    assert set(geometry) == previous.independent_geometries()
    geometries, templates, template_ids, records = [], [], {}, []
    for ss, placements in sorted(geometry.items()):
        gid = len(geometries)
        for p in placements:
            order = p['order']
            if order not in template_ids:
                template_ids[order] = len(templates)
                templates.append(dict(id=len(templates), order=order, contact_rotations=previous.rotations(order)))
            p['rotation_template_id'] = template_ids[order]
            previous.verify_placement(ss, p, templates[template_ids[order]]['contact_rotations'])
        geometries.append(dict(id=gid, supports=ss, placements=placements))
        for src in sources:
            if tuple(src['z']['root_boundary']) != tuple(s[0] for s in ss[1:3]):
                continue
            if not all(previous.valid_q_support(ss[pos], tuple(src[root]['forbidden'][col])) for _, root, col, pos in COMPONENTS):
                continue
            ids = {n: previous.stable_schema_ids(tuple(src[root]['forbidden'][col]), ss[pos]) for n, root, col, pos in COMPONENTS}
            assert all(ids.values())
            record = dict(id=len(records), source_id=src['id'], source_side_ids=src['side_ids'],
                common=src['common'], geometry_id=gid, supports=ss, q_schema_ids=ids)
            ctx = previous.context(record, src)
            fs = [c['source_forbidden'] for c in ctx['components']]
            ez = U - {Q[i] for i in src['z']['root_boundary']} - set(fs[0])
            ew = U - set(fs[1]) - set(fs[2])
            assert ez == ew == {src['common']} and not root_pairs(ctx, Q, fs)
            assert not root_pairs(swapped(ctx), Q, fs)
            ev = evidence(ctx)
            assert ev['eliminated']
            record.update(source_forbidden=fs, source_residuals=(sorted(ez), sorted(ew)),
                          source_evidence=ev, status='excluded', targets=[])
            records.append(record)
    symmetry_audit(records, sources, schemas)
    controls = minor_controls(records, sources)
    negatives = negative_controls(geometry, records, sources, controls)
    fibers = [dict(source_id=s['id'], side_ids=s['side_ids'],
                   support_record_ids=[r['id'] for r in records if r['source_id'] == s['id']]) for s in sources]
    exclusions = Counter(tuple(e['eliminated'] for e in r['source_evidence']['components']) for r in records)
    assert exclusions == {(True, True): 188, (True, False): 12, (False, True): 12}
    summary = dict(original_frontier=len(sources), geometric_supports=len(geometry),
        placements=sum(map(len, geometry.values())), rotation_templates=len(templates),
        contact_rotation_checks=8*sum(map(len, geometry.values())), necessary_support_records=len(records),
        source_records_with_support=sum(bool(f['support_record_ids']) for f in fibers),
        empty_source_fibers=sum(not f['support_record_ids'] for f in fibers),
        source_exclusions=len(records), retained_support_records=0, target_queries=0, target_accepts=0,
        both_components_K5=188, only_Cw_K5=12, only_Dw_K5=12, component_K5_witnesses=400,
        original_w_z_spoke_suffices=True, literal_source_reflections=len(records),
        whole_component_swaps=len(records), whole_root_swaps=len(records),
        common_color_counts=dict(sorted(Counter(r['common'] for r in records).items())),
        binary_relations_checked=65535, singleton_schemas=380, pair_schemas=6,
        minor_controls=len(controls), negative_controls=len(negatives))
    assert len(geometry) == sum(map(len, geometry.values())) == 910 and len(records) == 212
    assert summary['source_records_with_support'] == 40
    paths = [SOURCE, PREVIOUS, SCOPE, Path(previous.__file__)]
    old = json.loads(PREVIOUS.read_text())
    paths += [ROOT / p for p in old['inputs_sha256'] if p.startswith('scripts/')]
    return dict(schema=1, scope='arbitrary-size paper source exclusion with finite necessary-support and K5 controls; no realizability or Lean theorem',
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))},
        summary=summary, original_records=sources, source_fibers=fibers, geometries=geometries,
        rotation_templates=templates, q_complete_binary_schemas=schemas, records=records,
        minor_controls=controls, negative_controls=negatives,
        coverage_extension=coverage_extension(data, sources), next_frontier=next_frontier(data))


def render(data):
    lines = ['# 無 mixed t_z=2,(2)，t_w=0,(2,2) 重疊型來源排除', '',
        '原 96 份資料接成 212 份必要支援，全部由原分量 K5 排除；0 target 查詢。',
        'Cw、Dw 各自的完整關係、路徑與具名接點保留；必要配置和 minor skeletons 不宣稱可實現。', '',
        '| ID | 原子表 | 原側 IDs | Cz / z0 / z1 / Cw / Dw | Cw K5 | Dw K5 |',
        '| ---: | ---: | --- | --- | --- | --- |']
    for r in data['records']:
        support = ' / '.join(''.join(map(str, s)) for s in r['supports'])
        status = ['X' if e['eliminated'] else '—' for e in r['source_evidence']['components']]
        lines.append(f"| {r['id']} | {r['source_id']} | {r['source_side_ids']} | {support} | {status[0]} | {status[1]} |")
    lines += ['', '## 原資料纖維', '', '| 原子表 | 原側 IDs | 必要支援（全排除） |', '| ---: | --- | ---: |']
    for f in data['source_fibers']:
        lines.append(f"| {f['source_id']} | {f['side_ids']} | {len(f['support_record_ids'])} |")
    lines += ['', '全部 schemas、rotations、原路徑與固定框弧見 [JSON](observations.json)。',
              '任意大小覆蓋與信任界線見 [報告](../../docs/c5_adjacent_degree5_no_mixed_t2_t0_overlap.md)。', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    for path, payload in ((OUT, json.dumps(result, sort_keys=True, indent=2) + '\n'), (TABLE, render(result))):
        if args.check:
            assert path.read_bytes() == payload.encode(), f'certificate differs: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
