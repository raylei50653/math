#!/usr/bin/env python3
"""No mixed t_z=2,(2), t_w=0,(2,2), D_w=1: supports and original-path K5.

The report supplies arbitrary-size coverage. These are necessary relations,
support data and minor skeletons, not realizing disk sources or Lean proofs.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_mixed_edge_shared import schemas_for
from c5_adjacent_degree5_singleton_long_arc import component_options, valid_q_support
from c5_adjacent_degree5_no_mixed_t2_t1_bridge import (
    frame_evidence, minor_control, root_pairs, swapped,
)
from c5_single_spoke_cores import Q, U, TARGETS, PERMS, PI, RHO
from c5_single_spoke_frame_arc import admissible_supports, support_audit, verify_arcs
from c5_single_spoke_two_two_external import STYLES
from c5_single_spoke_two_two_minor import verify_minor
from c5_root_degree_excess import budget
import c5_single_spoke_two_two as legacy_two_two

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_t0_singles/observations.json'
SCOPE = ROOT / 'artifacts/c5_exchange_geometry_scope/observations.json'
OUT = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_t0_pairs/observations.json'
TABLE = OUT.with_name('support_table.md')
NAMES = ('Cz', 'z0', 'z1', 'Cw', 'Dw')
COMPONENTS = (('Cz', 'z', 0, 0), ('Cw', 'w', 0, 3), ('Dw', 'w', 1, 4))


def canonical(value):
    return json.loads(json.dumps(value, sort_keys=True))


def cardinalities(name):
    return (1,) if name in ('z0', 'z1') else range(2, 6)


def geometries():
    choices = {n: [s for k in cardinalities(n) for s in combinations(range(6), k)
                   if max(s) - min(s) < 5] for n in NAMES}
    orders = set()
    for z, w in product(permutations(NAMES[:3]), permutations(NAMES[3:])):
        order = z + w
        i = order.index('Cz')
        orders.add(order[i:] + order[:i])
    result = {}
    for order in sorted(orders):
        def visit(j, end, assigned):
            if j == len(NAMES):
                for anchor in range(5):
                    supports = tuple(tuple(sorted((anchor + i) % 5 for i in assigned[n])) for n in NAMES)
                    if supports[1] >= supports[2]:
                        continue
                    result.setdefault(supports, []).append(dict(
                        order=order, anchor=anchor, lifts=tuple(assigned[n] for n in NAMES)))
                return
            for support in choices[order[j]]:
                if min(support) >= end and (j or min(support) == 0):
                    visit(j + 1, max(support), assigned | {order[j]: support})
        visit(0, 0, {})
    return result


def independent_geometries():
    sides = []
    for names in (NAMES[:3], NAMES[3:]):
        found = set()
        choices = [[s for k in cardinalities(n) for s in combinations(range(5), k)] for n in names]
        for supports in product(*choices):
            if names[0] == 'Cz' and supports[1] >= supports[2]:
                continue
            for anchor in set().union(*map(set, supports)):
                lifts = [sorted((i - anchor) % 5 for i in s) for s in supports]
                if any(not (a[-1] <= b[0] or b[-1] <= a[0]) for a, b in combinations(lifts, 2)):
                    continue
                mask = sum(1 << ((anchor + j) % 5) for j in range(max(s[-1] for s in lifts)))
                found.add((supports, mask))
        sides.append(found)
    return {a + b for a, ma in sides[0] for b, mb in sides[1] if not ma & mb}


def rotations(order):
    result = []
    for flips in product((False, True), repeat=3):
        expansion = {n: (n,) for n in NAMES}
        for (name, _, _, _), flip in zip(COMPONENTS, flips, strict=True):
            ports = (name + '_0', name + '_1')
            expansion[name] = ports[::-1] if flip else ports
        roots = {}
        for root, own, other in (('z', NAMES[:3], 'w'), ('w', NAMES[3:], 'z')):
            start = next(i for i, n in enumerate(order) if n in own and order[i - 1] not in own)
            units = tuple(order[(start + j) % 5] for j in range(len(own)))
            assert set(units) == set(own)
            roots[root] = (other,) + tuple(p for n in units for p in expansion[n])
        result.append(dict(contact_flips=flips, root_rotations=roots,
                           neighborhood_word=tuple(p for n in order for p in expansion[n])))
    return result


def verify_placement(supports, placement, templates):
    order = placement['order']
    assert len(order) == len(set(order)) == 5 and set(order) == set(NAMES) and order[0] == 'Cz'
    side = [n in NAMES[:3] for n in order]
    assert sum(side[i] != side[i - 1] for i in range(5)) == 2
    lifts = dict(zip(NAMES, placement['lifts'], strict=True))
    assert min(lifts['Cz']) == 0 and max(lifts[order[-1]]) <= 5 and 0 <= placement['anchor'] < 5
    for name, support in zip(NAMES, supports, strict=True):
        values = lifts[name]
        assert tuple(sorted(set(values))) == tuple(values)
        assert len(values) in cardinalities(name) and max(values) - min(values) < 5
        assert tuple(sorted((placement['anchor'] + j) % 5 for j in values)) == tuple(support)
    assert supports[1] < supports[2]
    assert all(max(lifts[a]) <= min(lifts[b]) for a, b in zip(order, order[1:]))
    assert sum(max(lifts[n]) - min(lifts[n]) for n, _, _, _ in COMPONENTS) >= 3
    expected = {'z': {'w', 'Cz_0', 'Cz_1', 'z0', 'z1'},
                'w': {'z', 'Cw_0', 'Cw_1', 'Dw_0', 'Dw_1'}}
    assert {tuple(t['contact_flips']) for t in templates} == set(product((False, True), repeat=3))
    for t in templates:
        word = t['neighborhood_word']
        assert len(word) == len(set(word)) == 8
        assert set(word) == (expected['z'] | expected['w']) - {'z', 'w'}
        compressed = []
        for p in word:
            unit = p.split('_')[0]
            if not compressed or compressed[-1] != unit:
                compressed.append(unit)
        assert tuple(compressed) == tuple(order)
        for (name, _, _, _), flip in zip(COMPONENTS, t['contact_flips'], strict=True):
            ports = [name + '_0', name + '_1']
            assert [p for p in word if p.startswith(name + '_')] == (ports[::-1] if flip else ports)
        for root, other, own in (('z', 'w', NAMES[:3]), ('w', 'z', NAMES[3:])):
            rotation = t['root_rotations'][root]
            assert len(rotation) == len(set(rotation)) == 5 and set(rotation) == expected[root]
            assert rotation[0] == other
            start = next(i for i, p in enumerate(word) if p.split('_')[0] in own
                         and word[i - 1].split('_')[0] not in own)
            assert tuple(rotation[1:]) == tuple(word[(start + j) % 8] for j in range(4))


def bind_sources(data):
    sides, records = data['side_normal_forms'], []
    for jid, (i, j) in enumerate(data['abstract_conditions']['retained']):
        z, w = sides[i], sides[j]
        if (len(z['root_boundary']), z['ports'], len(w['root_boundary']), w['ports'],
            w['capacity_deficit'], w['overlap_excess']) != (2, [2], 0, [2, 2], 1, 0):
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
            for h in U - {c}:
                pair = tuple(sorted(U - {c, h}))
                for fs in (((h,), pair), (pair, (h,))):
                    rebuilt.add((sz, c, fz, fs))
    assert {(tuple(s['z']['root_boundary']), s['common'], tuple(s['z']['forbidden'][0]),
             tuple(map(tuple, s['w']['forbidden']))) for s in records} == rebuilt
    assert len(records) == 96 and Counter(tuple(map(len, s['w']['forbidden'])) for s in records) == {(1, 2): 48, (2, 1): 48}
    prior = json.loads(PREVIOUS.read_text())['next_frontier']
    assert prior['source_sha256'] == sha256(SOURCE.read_bytes()).hexdigest()
    assert prior['records'] == [dict(retained_join_id=s['retained_join_id'], side_ids=list(s['side_ids'])) for s in records]
    assert (records[0]['retained_join_id'], records[0]['side_ids']) == (3036, (133, 16))
    return records


def schema_audit():
    pairs = tuple(product(range(4), repeat=2))
    found = {f: [] for size in (1, 2) for f in combinations(range(4), size)}
    for mask in range(1, 1 << 16):
        rel = tuple(p for i, p in enumerate(pairs) if mask >> i & 1)
        f = tuple(sorted(set.intersection(*(set(p) for p in rel))))
        if f in found and all(any(t[j] == c and t[1-j] != c for t in rel) for c in f for j in range(2)):
            found[f].append(rel)
    schemas = {}
    for f, rels in found.items():
        expected = schemas_for(set(f))
        assert set(rels) == {tuple(r) for r in expected}
        assert len(rels) == (95 if len(f) == 1 else 1)
        if len(f) == 2:
            assert set(rels[0]) == {f, f[::-1]}
        schemas[','.join(map(str, f))] = expected
    return schemas


@lru_cache(None)
def stable_schema_ids(forbidden, support):
    stabilizer = [p for p in PERMS if all(p[Q[i]] == Q[i] for i in support)]
    return [j for j, rel in enumerate(schemas_for(set(forbidden))) if all(
        {tuple(p[c] for c in t) for t in rel} == set(rel) for p in stabilizer)]


def context(record, source):
    return dict(record_id=record['id'], root_boundary={r: source[r]['root_boundary'] for r in ('z', 'w')},
                components=[dict(name=n, root=r, support=record['supports'][pos],
                                 contacts=[n + '_0', n + '_1'], source_forbidden=source[r]['forbidden'][col])
                            for n, r, col, pos in COMPONENTS])


def evidence(ctx, row, bans):
    """Only the source-saturated original component is used, in its own row."""
    k = next(k for k, c in enumerate(ctx['components']) if len(c['source_forbidden']) == 2)
    pair = bans[k]
    if len(pair) != 2:
        return dict(component=k, applicable=False, eliminated=False, frame=None)
    comp = ctx['components'][k]
    family = admissible_supports(tuple(row), tuple(comp['support']), tuple(pair))
    frame = frame_evidence(ctx, k, family)
    return dict(component=k, ordered_contacts=comp['contacts'], source_forbidden=comp['source_forbidden'],
                row=row, target_forbidden=pair, applicable=True, frame=frame, eliminated=frame['eliminated'])


def row_evidence(ctx, row):
    components = [dict(name=c['name'], **component_options(2, tuple(c['support']), tuple(c['source_forbidden']), tuple(row)))
                  for c in ctx['components']]
    joins = []
    for fs in product(*(c['options'] for c in components)):
        ez = U - {row[i] for i in ctx['root_boundary']['z']} - set(fs[0])
        ew = U - set(fs[1]) - set(fs[2])
        pairs = sorted((a, b) for a, b in product(ez, ew) if a != b)
        assert pairs == root_pairs(ctx, row, fs)
        assert set(root_pairs(swapped(ctx), row, fs)) == {(b, a) for a, b in pairs}
        reasons = (['empty_z'] if not ez else []) + (['empty_w'] if not ew else [])
        if len(ez) == 1 and ez == ew:
            reasons.append('same_singleton')
        assert bool(reasons) == (not pairs)
        ev = evidence(ctx, row, fs) if not pairs and tuple(row) != Q else None
        joins.append(dict(forbidden_sets=fs, residuals=(sorted(ez), sorted(ew)), root_pairs=pairs,
                          witness=pairs[0] if pairs else None, obstruction_reasons=reasons, evidence=ev))
    direct = all(j['root_pairs'] for j in joins)
    accept = all(j['root_pairs'] or (j['evidence'] and j['evidence']['eliminated']) for j in joins)
    return dict(row=row, components=components, joins=joins,
                initial_status='accept' if direct else 'unresolved', status='accept' if accept else 'unresolved',
                closure_reason=('complete_relation_transport' if all(c['exact'] for c in components)
                                else 'transport_and_capacity_bound') if direct else
                               'saturated_component_target_K5' if accept else None)


def check_reflected_evidence(before, after):
    assert (before['component'], before['applicable'], before['eliminated']) == (after['component'], after['applicable'], after['eliminated'])
    if not before['applicable']:
        return
    assert {PI[c] for c in before['target_forbidden']} == set(after['target_forbidden'])
    a, b = before['frame'], after['frame']
    assert {tuple(sorted(RHO[i] for i in t)) for t in a['supports']} == set(map(tuple, b['supports']))
    keys = {(tuple(map(tuple, w['frame_arcs'])), w['route']['mode'], w['route']['component'], w['route']['landing'])
            for w in b['witnesses']}
    for w in a['witnesses']:
        arcs = tuple(tuple(sorted(RHO[i] for i in s)) for s in w['frame_arcs'])
        verify_arcs([s[0] for s in arcs], arcs)
        assert (arcs, w['route']['mode'], w['route']['component'], RHO[w['route']['landing']]) in keys


def symmetry_audit(records, sources, schemas):
    def key(s):
        return (tuple(s['z']['root_boundary']), tuple(s['z']['forbidden'][0]), tuple(map(tuple, s['w']['forbidden'])))
    sources_by_key = {key(s): s for s in sources}
    by_key = {(r['source_id'], r['supports']): r for r in records}
    target_count = 0
    for r in records:
        src = sources[r['source_id']]
        k = key(src)
        moved = (tuple(sorted(RHO[i] for i in k[0])), tuple(sorted(PI[c] for c in k[1])),
                 tuple(tuple(sorted(PI[c] for c in f)) for f in k[2]))
        sr = sources_by_key[moved]
        ss = tuple(tuple(sorted(RHO[i] for i in s)) for s in r['supports'])
        ss = (ss[0], *sorted(ss[1:3]), *ss[3:])
        ref = by_key[sr['id'], ss]
        r['reflected_id'] = ref['id']
        cr = context(ref, sr)
        check_reflected_evidence(r['source_evidence'], ref['source_evidence'])
        assert r['status'] == ref['status']
        for n, owner, col, _ in COMPONENTS:
            f = src[owner]['forbidden'][col]
            fk = ','.join(map(str, f))
            fr = ','.join(map(str, sorted(PI[c] for c in f)))
            assert {tuple(sorted(tuple(PI[c] for c in t) for t in schemas[fk][i])) for i in r['q_schema_ids'][n]} == {
                tuple(sorted(schemas[fr][i])) for i in ref['q_schema_ids'][n]}
        for t in r['targets']:
            raw = tuple(PI[t['row'][RHO[i]]] for i in range(5))
            tr = row_evidence(cr, raw)
            assert t['status'] == tr['status']
            moved_joins = {tuple(tuple(sorted(PI[c] for c in f)) for f in j['forbidden_sets']): j for j in t['joins']}
            for j in tr['joins']:
                old = moved_joins[tuple(j['forbidden_sets'])]
                assert {(PI[a], PI[b]) for a, b in old['root_pairs']} == set(j['root_pairs'])
                if old['evidence']:
                    check_reflected_evidence(old['evidence'], j['evidence'])
            target_count += 1
        twin_src = sources_by_key[(k[0], k[1], k[2][::-1])]
        twin = by_key[twin_src['id'], (*r['supports'][:3], r['supports'][4], r['supports'][3])]
        r['component_swapped_id'] = twin['id']
        assert r['status'] == twin['status']
        for n, other in (('Cz', 'Cz'), ('Cw', 'Dw'), ('Dw', 'Cw')):
            assert r['q_schema_ids'][n] == twin['q_schema_ids'][other]
        for a, b in zip(r['targets'], twin['targets'], strict=True):
            assert a['status'] == b['status']
            assert {(tuple((j['forbidden_sets'][0], j['forbidden_sets'][2], j['forbidden_sets'][1])),
                     tuple(j['root_pairs'])) for j in a['joins']} == {
                    (tuple(j['forbidden_sets']), tuple(j['root_pairs'])) for j in b['joins']}
    return target_count


def minor_controls(records, sources):
    cases = []
    for r in records:
        if r['status'] == 'excluded':
            cases.append((r, 'source', r['source_evidence']))
        for ti, t in enumerate(r['targets']):
            for ji, j in enumerate(t['joins']):
                if j['evidence'] and j['evidence']['eliminated']:
                    cases.append((r, f'target_{ti}_join_{ji}', j['evidence']))
    controls, modes = [], {}
    for r, purpose, ev in cases:
        ctx = context(r, sources[r['source_id']])
        assert ev['frame']['reason'] == 'original_path_K5'
        witness = ev['frame']['witnesses'][0]
        for length in (1, 3, 5):
            controls.append(dict(purpose=purpose, **minor_control(ctx, ev['component'], witness, length)))
        for w in ev['frame']['witnesses']:
            modes.setdefault(w['route']['mode'], (ctx, ev['component'], w))
    # Exercise each available original route, all tether styles and distinct suppliers.
    for ctx, k, w in modes.values():
        possible = [sorted(set(ctx['components'][k]['support']) & set(a)) for a in w['frame_arcs'][:2]]
        supply = list(product(*possible))
        for length, styles, ext, suppliers in product((1, 5), product(STYLES, repeat=2), (1, 3), product(supply, repeat=2)):
            controls.append(dict(purpose='route_and_tether_control',
                **minor_control(ctx, k, w, length, styles, suppliers, ext)))
    assert len(cases) == 348 and set(modes) == {'other_spoke', 'other_root_component', 'same_root_component'}
    return controls


def negative_controls(geometry, records, sources, controls):
    ss, placements = next(iter(sorted(geometry.items())))
    p, ts = placements[0], rotations(placements[0]['order'])
    broken = []
    q = canonical(p)
    q['order'] = ['Cz', 'Cw', 'z0', 'Dw', 'z1']
    broken.append(('interleaved_root_units', ss, q, ts))
    q = canonical(ts)
    q[0]['root_rotations']['w'][-1] = q[0]['root_rotations']['w'][-2]
    broken.append(('merged_named_contacts', ss, p, q))
    q = canonical(ts)
    q[0]['root_rotations']['z'].remove('w')
    broken.append(('missing_original_zw_rotation', ss, p, q))
    result = []
    for name, support, placement, templates in broken:
        try:
            verify_placement(support, placement, templates)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    relation = ((0, 1), (1, 0))
    assert set.intersection(*map(set, relation)) == {0, 1}
    marginals = tuple(product({t[0] for t in relation}, {t[1] for t in relation}))
    assert set.intersection(*map(set, marginals)) == set()
    result.append('saturated_pair_marginals_lose_both_bans')
    assert not valid_q_support((), (0, 1)) and not valid_q_support((0, 2), (0, 1))
    result.append('empty_or_monochromatic_pair_support')
    r = records[79]
    ctx = context(r, sources[r['source_id']])
    assert r['targets'][0]['initial_status'] == 'unresolved' and r['targets'][0]['status'] == 'accept'
    assert not r['source_evidence']['eliminated']
    result.append('target_K5_is_not_a_source_exclusion')
    pair_k = next(k for k, c in enumerate(ctx['components']) if len(c['source_forbidden']) == 2)
    fs = [list(c['source_forbidden']) for c in ctx['components']]
    fs[pair_k] = [fs[pair_k][0]]
    assert not evidence(ctx, TARGETS[0], fs)['applicable']
    result.append('singleton_target_has_no_pair_path')
    assert any(not j['root_pairs'] for j in r['targets'][0]['joins'])
    assert any(j['root_pairs'] for j in r['targets'][0]['joins'])
    result.append('one_good_candidate_does_not_prove_the_target')
    base = next(c for c in controls if c['record_id'] == 0 and c['length'] == 3)
    edges, bags = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    broken_minors = [('missing_original_zw', edges - {('w', 'z')}, bags),
                     ('missing_external_spoke', edges - {('b0', 'z')}, bags),
                     ('missing_original_bridge', edges - {tuple(sorted(base['path'][:2]))}, bags),
                     ('missing_pair_contact', edges - {tuple(sorted(('w', base['path'][0])))}, bags),
                     ('overlapping_branch_sets', edges, [bags[0] | {'w'}, *bags[1:]])]
    for name, es, bs in broken_minors:
        try:
            verify_minor(es, bs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    return result


def next_frontier(data):
    sides, rows = data['side_normal_forms'], []
    for jid, pair in enumerate(data['abstract_conditions']['retained']):
        z, w = (sides[i] for i in pair)
        if (len(z['root_boundary']), z['ports'], len(w['root_boundary']), w['ports'],
            w['capacity_deficit'], w['overlap_excess']) == (2, [2], 0, [2, 2], 0, 1):
            rows.append(dict(retained_join_id=jid, side_ids=pair))
    assert len(rows) == 96
    return dict(scope='t_z=2,(2), t_w=0,(2,2), D_w=0,O_w=1; not audited in this layer',
                source_sha256=sha256(SOURCE.read_bytes()).hexdigest(), records=rows,
                first_sides=[sides[i] for i in rows[0]['side_ids']])


def coverage_extension(data, sources):
    old = json.loads(SCOPE.read_text())
    assert old['inputs_sha256'][str(SOURCE.relative_to(ROOT))] == sha256(SOURCE.read_bytes()).hexdigest()
    previous = {i for cell in old['matrix'] if cell['status'] == 'covered' for i in cell['retained_join_ids']}
    joins = data['abstract_conditions']['retained']
    lookup = {tuple(pair): i for i, pair in enumerate(joins)}
    added = {s['retained_join_id'] for s in sources} | {lookup[s['side_ids'][::-1]] for s in sources}
    assert len(previous) == 552 and len(added) == 192 and not previous & added
    return dict(previous_scope_sha256=sha256(SCOPE.read_bytes()).hexdigest(),
                newly_covered_source_join_ids=sorted(added), covered_source_join_ids=sorted(previous | added),
                covered_ordered_cells=7, covered_unordered_cells=4,
                covered_source_joins=744, remaining_source_joins=2804,
                scope='subtype coverage, not numbers of realizing graphs; previous artifacts unchanged')


def legacy_replay():
    """Preserve an old certificate whose documentation hash has since changed."""
    saved = json.loads(legacy_two_two.OUT.read_text())
    rebuilt = legacy_two_two.run()
    normalized = canonical(rebuilt)
    differences = [k for k in saved if saved[k] != normalized[k]]
    assert set(saved) == set(normalized) and differences == ['inputs']
    changed = [p for p in saved['inputs'] if saved['inputs'][p] != normalized['inputs'][p]]
    assert changed == ['docs/c5_single_spoke_cores.md']
    table = legacy_two_two.OUT.with_name('support_table.md')
    assert table.read_text() == legacy_two_two.support_table(rebuilt)
    payload = {k: v for k, v in normalized.items() if k != 'inputs'}
    return dict(legacy_byte_check_passes=False, mathematical_payload_equal=True, support_table_equal=True,
                changed_input_hashes={p: dict(saved=saved['inputs'][p], current=normalized['inputs'][p]) for p in changed},
                mathematical_payload_sha256=sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
                original_artifact_sha256=sha256(legacy_two_two.OUT.read_bytes()).hexdigest(),
                current_inputs=normalized['inputs'],
                scope='content replay only; old provenance is preserved, not rewritten')


def build():
    data = json.loads(SOURCE.read_text())
    sources, geometry, schemas = bind_sources(data), geometries(), schema_audit()
    assert set(geometry) == independent_geometries()
    geometries_out, templates, template_ids, records = [], [], {}, []
    for ss, placements in sorted(geometry.items()):
        gid = len(geometries_out)
        for p in placements:
            order = p['order']
            if order not in template_ids:
                template_ids[order] = len(templates)
                templates.append(dict(id=len(templates), order=order, contact_rotations=rotations(order)))
            p['rotation_template_id'] = template_ids[order]
            verify_placement(ss, p, templates[template_ids[order]]['contact_rotations'])
        geometries_out.append(dict(id=gid, supports=ss, placements=placements))
        for src in sources:
            if tuple(src['z']['root_boundary']) != tuple(s[0] for s in ss[1:3]):
                continue
            if not all(valid_q_support(ss[pos], tuple(src[r]['forbidden'][col])) for n, r, col, pos in COMPONENTS):
                continue
            ids = {n: stable_schema_ids(tuple(src[r]['forbidden'][col]), ss[pos]) for n, r, col, pos in COMPONENTS}
            assert all(ids.values())
            record = dict(id=len(records), source_id=src['id'], source_side_ids=src['side_ids'],
                          common=src['common'], geometry_id=gid, supports=ss, q_schema_ids=ids)
            ctx = context(record, src)
            q = row_evidence(ctx, Q)
            assert len(q['joins']) == 1 and q['joins'][0]['residuals'] == ([src['common']], [src['common']])
            ev = evidence(ctx, Q, q['joins'][0]['forbidden_sets'])
            record.update(q=q, source_evidence=ev, status='excluded' if ev['eliminated'] else 'retained',
                          targets=[] if ev['eliminated'] else [row_evidence(ctx, row) for row in TARGETS])
            records.append(record)
    reflected = symmetry_audit(records, sources, schemas)
    controls = minor_controls(records, sources)
    negatives = negative_controls(geometry, records, sources, controls)
    retained = [r for r in records if r['status'] == 'retained']
    fibers = [dict(source_id=s['id'], side_ids=s['side_ids'],
                   support_record_ids=[r['id'] for r in records if r['source_id'] == s['id']],
                   retained_record_ids=[r['id'] for r in retained if r['source_id'] == s['id']]) for s in sources]
    queries = [dict(record_id=r['id'], target_index=i, target=t) for r in retained
               for i, t in enumerate(r['targets']) if t['status'] != 'accept']
    summary = dict(original_frontier=len(sources), geometric_supports=len(geometry),
        placements=sum(map(len, geometry.values())), rotation_templates=len(templates),
        contact_rotation_checks=8 * sum(map(len, geometry.values())),
        necessary_support_records=len(records), source_records_with_support=sum(bool(f['support_record_ids']) for f in fibers),
        empty_source_fibers=sum(not f['support_record_ids'] for f in fibers),
        source_exclusions=len(records)-len(retained), retained_support_records=len(retained),
        retained_source_fibers=sum(bool(f['retained_record_ids']) for f in fibers),
        target_queries=2*len(retained), target_accepts=2*len(retained)-len(queries), unresolved_target_queries=len(queries),
        closure_reasons=dict(sorted(Counter(t['closure_reason'] for r in retained for t in r['targets']).items())),
        target_candidate_joins=sum(len(t['joins']) for r in retained for t in r['targets']),
        failing_candidate_causes=dict(Counter(c for r in retained for t in r['targets'] for j in t['joins'] for c in j['obstruction_reasons'])),
        literal_source_reflections=len(records), literal_target_reflections=reflected,
        whole_component_swaps=len(records), whole_root_swap_joins=len(records)+sum(len(t['joins']) for r in retained for t in r['targets']),
        binary_relations_checked=65535, singleton_schemas=380, pair_schemas=6,
        minor_controls=len(controls), negative_controls=len(negatives))
    assert len(geometry) == sum(map(len, geometry.values())) == 910
    assert len(records) == 364 and len(retained) == 24 and not queries
    assert summary['source_exclusions'] == 340 and summary['failing_candidate_causes'] == {'same_singleton': 8}
    old_replay = legacy_replay()
    inputs = [str(p.relative_to(ROOT)) for p in (SOURCE, PREVIOUS, SCOPE, legacy_two_two.OUT,
              legacy_two_two.OUT.with_name('support_table.md'))] + list(old_replay['current_inputs']) + ['scripts/' + n + '.py' for n in (
        'c5_adjacent_degree5_mixed_edge_shared', 'c5_adjacent_degree5_singleton_long_arc',
        'c5_adjacent_degree5_no_mixed_t2_t1_bridge', 'c5_single_spoke_cores', 'c5_single_spoke_frame_arc',
        'c5_single_spoke_two_two_minor', 'c5_single_spoke_two_two_external', 'c5_root_degree_excess',
        'c5_no_spoke_first_bridge')]
    return dict(schema=1, scope='same-source necessary support coverage, source K5 and target separation; no realizability or Lean theorem',
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs}, summary=summary,
        original_records=sources, source_fibers=fibers, geometries=geometries_out, rotation_templates=templates,
        q_complete_binary_schemas=schemas, records=records, open_queries=queries,
        support_algebra_controls=support_audit(), minor_controls=controls, negative_controls=negatives,
        next_frontier=next_frontier(data), coverage_extension=coverage_extension(data, sources),
        legacy_two_contact_replay=old_replay)


def render(data):
    lines = ['# 無 mixed t_z=2,(2)，t_w=0,(2,2)，D_w=1 的必要支援', '',
             '三原分量均為二接點；保留全部具名接點及原 z–w 邊。X 是 source K5 排除，A 是指定列已證。',
             '原 96 份資料的 364 份必要支援不宣稱可實現；排除 340 份，保留 24 份均 A/A。', '',
             '| ID | 原子表 | 原側 IDs | Cz / z0 / z1 / Cw / Dw | 狀態 | p₁ | p₂ |',
             '| ---: | ---: | --- | --- | --- | --- | --- |']
    for r in data['records']:
        support = ' / '.join(''.join(map(str, s)) for s in r['supports'])
        statuses = ['—', '—'] if r['status'] == 'excluded' else [t['closure_reason'] for t in r['targets']]
        lines.append(f"| {r['id']} | {r['source_id']} | {r['source_side_ids']} | {support} | "
                     f"{'X' if r['status'] == 'excluded' else 'A/A'} | {statuses[0]} | {statuses[1]} |")
    lines += ['', '## 原資料纖維', '', '| 原子表 | 原側 IDs | 必要支援 | 排除後保留 |', '| ---: | --- | ---: | ---: |']
    for f in data['source_fibers']:
        lines.append(f"| {f['source_id']} | {f['side_ids']} | {len(f['support_record_ids'])} | {len(f['retained_record_ids'])} |")
    lines += ['', '完整 schemas、rotations、原路徑見證與 target joins 見 [JSON](observations.json)。',
              '任意大小覆蓋及信任界線見 [報告](../../docs/c5_adjacent_degree5_no_mixed_t2_t0_pairs.md)。', '']
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
