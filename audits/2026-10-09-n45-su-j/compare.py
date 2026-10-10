#!/usr/bin/env python3
"""Post-computation scope diagnostics and comparison; never runs supervisor code."""
from collections import Counter
import hashlib
import json
from pathlib import Path

H = Path(__file__).resolve().parent
R = H.parent.parent


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, value):
    with (H / name).open('x') as f:
        json.dump(value, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write('\n')


c = read(H / 'certificate.json')
n = c['counts']
sdir = R / 'audits/2026-10-09-n45-s-supervision'
udir = R / 'audits/2026-10-09-n45-batch-supervision'
s = read(sdir / 'independent_review.json')
u = read(udir / 'independent_review.json')
pairs = {
    'S': {
        'singleton_rows': n['singleton_candidates'],
        'singleton_contact_bound_triggered': n['singleton_contact_bound_holds'],
        'singleton_low_incidence_valid': sum(
            x['status'] == 'triggered and holds' and x['k_r'] + x['k_s'] <= 3
            for x in c['singleton_orbit_table']),
        'abstract_capacity_columns': n['abstract_capacity_columns'],
        'scalar_incidence_rows': len(c['both_short_incidence_counts']),
        'cross_row_mask_cases': len(c['S_cross_row_masks']),
        'full_graph_rows': n['S_full_sigma_rows'],
        'spoke_rejected_row_queries': n['S_spoke_rejection_rows'],
        'complete_root_pair_cells': n['S_full_sigma_root_pair_queries'] + n['S_spoke_root_pair_queries'],
        'validated_S_full_lifts': n['S_full_lifts_validated'],
        'S_source_triggered': n['target_source_triggered'],
    },
    'U': {
        'U_graphs': n['graphs'],
        'U_original_pair_cells': n['original_root_pair_queries'],
        'U_derivative_pair_cells': n['derivative_root_pair_queries'],
        'U_contact_deleted_pair_cells': n['contact_edge_deleted_root_pair_queries'],
        'U_local_relation_rows_vs_J': n['piece_relations'],
        'U_full_piece_lifts_vs_J': n['full_piece_lifts'],
        'U_BC2_columns_vs_J': n['capacity_G_triggered and holds'] + n['capacity_X_triggered and holds'],
    },
}
comparison = []
for label, own in pairs.items():
    old = s if label == 'S' else u['counts']
    for key, value in own.items():
        comparison.append({'section': label, 'field': key, 'independent': value,
                           'supervisor': old[key], 'equal': value == old[key]})
assert all(x['equal'] for x in comparison)
save('supervisor-comparison.json', {
    'independent_certificate_sha256': sha(H / 'certificate.json'),
    'read_order': 'independent exclusive certificate and normal/seed17 replays completed before supervisor review.py/results were read',
    'supervisor_inputs': [{'path': str(p.relative_to(R)), 'sha256': sha(p)}
                          for p in (sdir / 'review.py', sdir / 'independent_review.json',
                                    udir / 'review.py', udir / 'independent_review.json')],
    'comparisons': comparison, 'semantic_differences': [],
    'scope_differences': [
        'This checker independently reconstructs 690 local relations and all 2986 lifts; S supervision only compared source metadata to J.',
        'This checker reconstructs capacity terms from empty local fibres; batch U supervision compared worker terms to J.',
        'Independent solver uses bit-domain propagation; supervisor uses fixed vertex order forward checking.',
        'This checker additionally enumerates fixed critical edgecuts and new-gamma root projections; no new graph search.',
        'A payload/paper judgments are outside this comparison.',
        'U counts accepted rows as one not-triggered record; J counts each direction. Counts are not interchangeable.',
    ],
})

def canonical(row):
    mapping = {}
    answer = []
    for x in row:
        if x not in mapping:
            mapping[x] = len(mapping)
        answer.append(mapping[x])
    return answer


patterns = read(H / 'base-source/artifacts/c5_cells/cells.json')['pattern_order']
target_images = {}
for mask in (933, 941):
    images = set()
    for shift in range(5):
        for direction in (1, -1):
            transported = 0
            for i, pattern in enumerate(patterns):
                image = canonical([pattern[(shift + direction * j) % 5] for j in range(5)])
                if mask & (1 << i):
                    transported |= 1 << patterns.index(image)
            images.add(transported)
    target_images[str(mask)] = sorted(images)
occurrences = []
for p in sorted((H / 'base-source/artifacts/c5_excess_two_e4c/controls').glob('*.json')):
    g = read(p)
    roots = sorted(v for v in g['vertices'] if v >= 5 and sum(v in e for e in g['edges']) == 5)
    for row in g['row_cores']:
        for core in row['cores']:
            degree = [sum(r in e for e in core['edges']) for r in roots]
            assert degree == core['root_degrees']
            occurrences.append({'id': g['id'], 'm': g['m'], 'index': row['index'],
                                'root_degrees': degree, 'omitted_pieces': core['omitted_pieces']})
assert all(x['root_degrees'] == [5, 5] for x in occurrences if x['m'] == 2)
calibrations = [x for x in occurrences if x['root_degrees'] in ([4, 5], [5, 4])]
assert len(calibrations) == 12 and all(x['m'] == 1 for x in calibrations)
assert all(g['sigma'] not in set(target_images['933'] + target_images['941'])
           for g in c['graphs'] if g['m'] == 2)
split = {}
for m in (2, 1):
    gs = [g for g in c['graphs'] if g['m'] == m]
    rows = [r for g in gs for r in g['joins']]
    ders = [d for g in gs for d in g['unit_derivatives']]
    xr = [r for d in ders for r in d['joins_X']]
    split['N' + str(m)] = {
        'graphs': len(gs), 'original_pin_queries': len(rows) * 16,
        'original_nonempty_pins': sum(len(r['root_pairs']) for r in rows),
        'original_empty_pins': sum(16 - len(r['root_pairs']) for r in rows),
        'unit_derivatives': len(ders), 'X_pin_queries': len(xr) * 16,
        'X_nonempty_pins': sum(len(r['root_pairs']) for r in xr),
        'X_empty_pins': sum(16 - len(r['root_pairs']) for r in xr),
        'contact_deleted_pin_queries': len(xr) * 16,
        'G_capacity_columns': sum(t['status'] == 'triggered and holds' for r in rows for t in r['capacity']),
        'X_capacity_columns': sum(t['status'] == 'triggered and holds' for r in xr for t in r['capacity']),
        'G_not_triggered_records': sum(t['status'] == 'not triggered' for r in rows for t in r['capacity']),
        'X_not_triggered_records': sum(t['status'] == 'not triggered' for r in xr for t in r['capacity']),
    }
empty = []
for g in c['graphs']:
    for p in g['pieces']:
        if p['kind'] != 'unary' or sum(p['incidences']) != 1:
            continue
        r = str(p['owners'][0])
        for row in p['rows']:
            if not row['F'][r]:
                empty.append({'graph': g['id'], 'piece': p['id'], 'vertices': p['vertices'],
                              'contact_order': p['contact_order'], 'index': row['index'],
                              'tuples_and_full_lifts': row['tuples'], 'F_U': [],
                              'status': 'counterexample to always-singleton F only'})
assert len(empty) == 38
example = read(R / 'audits/2026-10-09-n45-u/certificate-final.json')['capacity_one_F_empty_control']
own = next(x for x in empty if all(x[k] == example[k] for k in ('graph', 'piece', 'vertices', 'index')))
assert own['contact_order'] == example['contact'] and own['tuples_and_full_lifts'] == example['tuples_and_full_lifts']
save('diagnostics.json', {
    'D5_whole_frame_target_masks': target_images, 'all_N2_complete_targets_not_triggered': True,
    'N2_sigma_counts': dict(Counter(str(g['sigma']) for g in c['graphs'] if g['m'] == 2)),
    'split': split, 'saved_core_degrees_checked_from_core_edges': occurrences,
    'saved_N1_45_54_occurrences': calibrations,
    'minimal_core_enumeration': 'not rerun; only supplied core-edge metadata and retained-edge lifts checked',
    'unit_F_empty_negative_controls': empty,
    'independent_full_fibres': {
        'original': {'nonempty': n['original_nonempty_pins'], 'empty': n['original_empty_pins']},
        'X': {'nonempty': n['X_nonempty_pins'], 'empty': n['X_empty_pins']},
        'G_contact_deleted': {'nonempty': n['X_nonempty_pins'], 'empty': n['X_empty_pins']},
        'local': {'nonempty': n['local_root_pin_fibres'] - n['local_empty_fibres'], 'empty': n['local_empty_fibres']},
    },
})
print(json.dumps({'supervisor_fields_compared': len(comparison), 'semantic_differences': [],
                  'split': split, 'negative_F_controls': len(empty)}, sort_keys=True))
