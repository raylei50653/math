#!/usr/bin/env python3
"""Join each fixed original profile to complete target-orbit supports, read-only.

Only 69 fixed profiles x 15 already classified columns x 16 rows are inspected.
No LP, graph enumeration, union of profiles, or source realization is used.
"""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
GEOMETRY_SHA = 'ee7b544a16192a9e6d4b37682d7177f03981acc8e427bc188777ff6f942bdcba'
spec = importlib.util.spec_from_file_location('target_exchange_review', HERE / 'target_exchange.py')
exchange = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exchange)
require = exchange.require


def first_failure(column, chords, index):
    for row in column:
        literal = exchange.decode(row)
        for a, b in chords:
            if literal[index[a]] == literal[index[b]]:
                return {'original_chord': [a, b], 'half_row': row,
                        'equal_literal_colour': literal[index[a]]}
    return None


def component_test(column, chords, index):
    reference = exchange.decode(column[0])
    block_of = {i: block_id for block_id, block in enumerate(exchange.components(column))
                for i in block}
    for a, b in chords:
        i, j = index[a], index[b]
        if reference[i] // 2 != reference[j] // 2:
            continue
        if reference[i] == reference[j] or block_of[i] != block_of[j]:
            return False
    return True


def compute():
    raw = (AUDIT / 'geometry/certificate.json').read_bytes()
    require(sha256(raw).hexdigest() == GEOMETRY_SHA, 'generated geometry certificate changed')
    geometry = json.loads(raw)
    manifest = json.loads((AUDIT / 'BASE.json').read_text())
    require(manifest['base'] == '30f2d19275657393b7354ed75eca31439d8ee12b', 'BASE changed')
    frozen = {record['path']: record for record in manifest['inputs']}
    checked_inputs = {}
    for path, record in geometry['inputs'].items():
        data = (ROOT / path).read_bytes()
        require(len(data) == record['bytes'] and sha256(data).hexdigest() == record['sha256'],
                'original geometry input drift: ' + path)
        if path in frozen:
            require(all(record[key] == frozen[path][key] for key in ('bytes', 'sha256')),
                    'geometry dependency differs from original BASE: ' + path)
        checked_inputs[path] = dict(record, original_BASE_entry=path in frozen)
    # Recompute the entire two-target classification from the frozen source,
    # then compare its recorded file. This prevents local subset replacement.
    targets = exchange.audit()
    require(targets == json.loads((HERE / 'target_exchange.json').read_text()),
            'target exchange dependency mismatch')
    source_dir = exchange.SOURCE
    for name, record in targets['inputs'].items():
        path = str((source_dir / name).relative_to(ROOT))
        require(all(record[key] == frozen[path][key] for key in ('bytes', 'sha256')),
                'target orbit input differs from original BASE: ' + path)
        checked_inputs[path] = dict(record, original_BASE_entry=True)
    index = {name: i for i, name in enumerate(geometry['C13'])}
    require(len(index) == 13, 'original ordered rim changed')
    survivors = geometry['surviving_original_profile_ids']
    require(len(survivors) == len(set(survivors)) == 69, 'expected 69 fixed profiles')
    profiles_by_id = {p['original_profile_id']: p for p in geometry['profiles']}
    require(len(profiles_by_id) == 112, 'original profile list changed')
    records, histogram = [], Counter()
    per_target_ids = {'44459': [], '44466': []}
    union_ids = []
    for profile_id in survivors:
        profile = profiles_by_id[profile_id]
        chords = profile['chords']
        require(all(a in index and b in index for a, b in chords),
                'an optional original edge is not on the retained rim')
        kept = {name: [] for name in exchange.EXPECTED}
        excluded = []
        for record in targets['columns']:
            column = record['half_rows']
            failure = first_failure(column, chords, index)
            accepted = failure is None
            require(accepted == component_test(column, chords, index),
                    'full-row test differs from same-palette component test')
            if accepted:
                kept[record['family']].append(record['column_id'])
            else:
                excluded.append(dict(failure, column_id=record['column_id']))
        count_a = len(kept['shared']) + len(kept['44459_only'])
        count_b = len(kept['shared']) + len(kept['44466_only'])
        counts = [count_a, count_b, len(kept['shared'])]
        histogram[tuple(counts)] += 1
        for target, count in (('44459', count_a), ('44466', count_b)):
            if count:
                per_target_ids[target].append(profile_id)
        if count_a or count_b:
            union_ids.append(profile_id)
        records.append({'original_profile_id': profile_id, 'original_chords': chords,
                        'retained_columns': kept, 'target_A_B_shared_counts': counts,
                        'excluded_columns_first_bad_row': excluded})
    require(histogram == {(10, 10, 5): 12, (2, 0, 0): 16,
                          (0, 2, 0): 12, (0, 0, 0): 29},
            'fixed-profile support histogram changed')
    require(union_ids == geometry['target_union_surviving_original_profile_ids'],
            'unexpected change beyond the geometry target-proper count')
    for target, ids in per_target_ids.items():
        require(ids == geometry['target_compatibility'][target]['surviving_original_profile_ids'],
                'unexpected individual target profile count')
    # A concrete witness-only false acceptance: A is proper for profile10,
    # but 8 of its 10 full orbit supports contain an improper flipped row.
    example = next(p for p in records if p['original_profile_id'] == 10)
    literal_a = exchange.LITERAL[0]
    require(all(literal_a[index[a]] != literal_a[index[b]]
                for a, b in example['original_chords']), 'negative-control target not proper')
    removed = next(r for r in example['excluded_columns_first_bad_row']
                   if r['column_id'] == 43330)
    require(removed['original_chord'] == ['u3', 'v'], 'wrong negative-control chord')
    require(example['retained_columns']['44459_only'] == [66582, 67755],
            'witness-only false acceptance was not rejected')
    return {
        'status': 'COMPLETE ORBITS JOINED TO EACH FIXED ORIGINAL PROFILE; strict W7 OPEN',
        'generated_geometry_dependency': {'path': str((AUDIT / 'geometry/certificate.json').relative_to(ROOT)),
                                          'bytes': len(raw), 'sha256': GEOMETRY_SHA},
        'original_inputs_checked': checked_inputs,
        'fixed_profiles_checked': 69,
        'full_target_columns_per_profile': 15,
        'rows_per_column': 16,
        'profile_support_histogram': [dict(target_A=a, target_B=b, shared=s, profiles=n)
                                     for (a,b,s),n in sorted(histogram.items())],
        'target_supporting_profiles': per_target_ids,
        'target_union_supporting_profiles': union_ids,
        'additional_profiles_excluded_beyond_target_literal_properness': 0,
        'profiles': records,
        'negative_control_witness_only_filter_rejected': {
            'original_profile_id': 10, 'target': 44459, 'target_literal_is_proper': True,
            'column_id': 43330, 'bad_flipped_row': removed,
            'target_columns_before': 10, 'complete_columns_after': 2},
        'same_palette_component_test_agrees_with_every_row_test': True,
        'source_realized': False,
        'strict_W7_source_excluded': False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    result = compute()
    path = HERE / 'profile_orbits.json'
    if args.build:
        with path.open('x') as out:
            json.dump(result, out, indent=2, sort_keys=True)
            out.write('\n')
    else:
        require(result == json.loads(path.read_text()), 'profile orbit certificate changed')
    keys = ['status', 'fixed_profiles_checked', 'profile_support_histogram',
            'additional_profiles_excluded_beyond_target_literal_properness',
            'same_palette_component_test_agrees_with_every_row_test']
    print(json.dumps({key: result[key] for key in keys}, sort_keys=True))


if __name__ == '__main__':
    main()
