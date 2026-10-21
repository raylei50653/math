#!/usr/bin/env python3
"""Two-step necessary palette audit, without inventing cross-palette transport."""
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import argparse, gzip, importlib.util, json, random, sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = '2c38d1dcb4490017312467deb19d9da02b7bb2a6'
SOURCE = Path('audits/2026-10-21-w7-L-path-30dde27/six_degree')
WORKSPACE = HERE.parents[2]

def require(ok, why):
    if not ok:
        raise ValueError(why)

def packed(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n').encode()

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def compute(seed=None):
    # Parent snapshot freezes these two files. The imported original checker
    # verifies every further dependency against its own original manifest.
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base'] == BASE, 'exclusive BASE changed')
    for row in manifest['inputs']:
        raw = (ROOT / row['frozen_path']).read_bytes()
        require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                'frozen parent authority drift')
    frozen = ROOT / 'frozen' / SOURCE
    for name in ('BASE.json', 'check.py', 'certificate-v2.json.gz'):
        require((frozen / name).read_bytes() == (WORKSPACE / SOURCE / name).read_bytes(),
                'original authority differs from frozen parent bytes: ' + name)
    m = load_module('original_six_degree', WORKSPACE / SOURCE / 'check.py')
    source, helper, cap, old = m.inputs()
    original = json.loads(gzip.decompress((frozen / 'certificate-v2.json.gz').read_bytes()))
    index = {tuple(row): i for i, row in enumerate(cap['states'])}
    graph = m.graph_type_I(source)
    # cap_lifts is mathematical data determined only by this complete rim.
    helper.cap_lifts = lru_cache(None)(helper.cap_lifts)
    used = set()
    rng = random.Random(seed) if seed is not None else None
    kernels = {}
    image_words = {}
    checks = {}

    def normalize(word):
        normalized = m.canonical(word)
        inverse = {c: actual for c, actual in zip(normalized, word)}
        for c, actual in zip(sorted(set(range(4)) - inverse.keys()),
                             sorted(set(range(4)) - set(word))):
            inverse[c] = actual
        require(set(inverse) == set(range(4)) and set(inverse.values()) == set(range(4)),
                'full global inverse missing')
        return normalized, tuple(inverse[c] for c in range(4))

    def image(word):
        word = tuple(word)
        normalized, inverse = normalize(word)
        if normalized not in kernels:
            kernels[normalized] = m.complete_fibre(dict(zip(m.B14, normalized)), graph,
                                                  cap, index, helper, used, rng)
        image_words[word] = (normalized, inverse)
        return kernels[normalized]['has_forbidden_full_join']

    def second_check(word, mate):
        # Conjugating the exact whole-colour inverse also conjugates the split.
        word = tuple(word)
        normalized, inverse = normalize(word)
        forward = {actual: c for c, actual in enumerate(inverse)}
        palette = {forward[0], forward[mate]}
        if 0 not in palette:
            palette = set(range(4)) - palette
        normalized_mate = next(c for c in palette if c != 0)
        key = (normalized, normalized_mate)
        if key in checks:
            return key
        partitions = sorted(helper.nc_specific(normalized, (0, normalized_mate)))
        require(partitions, 'missing necessary NC family')
        order = list(range(len(partitions)))
        if rng:
            rng.shuffle(order)
        rows = {}
        for i in order:
            p = partitions[i]
            masks = list(range(1 << (max(p) + 1)))
            if rng:
                rng.shuffle(masks)
            actions = {}
            forbidden = []
            for mask in masks:
                action = tuple(c ^ (normalized_mate if mask >> b & 1 else 0)
                               for c, b in zip(normalized, p))
                bad = image(action)
                actions[mask] = action
                if bad:
                    forbidden.append(mask)
            rows[i] = {'F_partition': list(p),
                       'all_action_words': [list(actions[j]) for j in range(len(masks))],
                       'forbidden_action_masks': sorted(forbidden)}
        checks[key] = {'normalized_F_boundary': list(normalized),
                       'split_containing_0': [0, normalized_mate],
                       'complete_necessary_NC_types': [rows[i] for i in range(len(partitions))],
                       'surviving_type_ids': [i for i in range(len(partitions))
                                              if not rows[i]['forbidden_action_masks']]}
        return key

    cases = []
    for case in original['ordinary_C14_cases']:
        first = case['split_containing_0'][1]
        if first not in (2, 3):
            continue
        second = 5 - first
        literal = tuple(case['literal_F_boundary_colors'])
        rows = []
        for p in case['surviving_types_after_same_initial_E_gate']:
            action_rows = []
            for mask in range(1 << (max(p) + 1)):
                word = tuple(c ^ (first if mask >> b & 1 else 0) for c, b in zip(literal, p))
                require(not image(word), 'first action contradicts original complete certificate')
                key = second_check(word, second)
                action_rows.append({'first_action_mask': mask, 'literal_F_boundary': list(word),
                                    'second_check_key': [list(key[0]), key[1]],
                                    'second_palette_has_necessary_survivor': bool(checks[key]['surviving_type_ids'])})
            rows.append({'initial_F_partition': p, 'all_first_actions': action_rows,
                         'passes_two_step_necessary_test': all(r['second_palette_has_necessary_survivor'] for r in action_rows)})
        cases.append({'target': case['target'], 'first_split_containing_0': [0, first],
                      'second_split_containing_0': [0, second], 'initial_types': rows})

    kernel_ids = {word: i for i, word in enumerate(sorted(kernels))}
    image_ids = {word: i for i, word in enumerate(sorted(image_words))}
    check_ids = {key: i for i, key in enumerate(sorted(checks))}
    for row in checks.values():
        for p in row['complete_necessary_NC_types']:
            p['all_action_image_ids'] = [image_ids[tuple(word)] for word in p.pop('all_action_words')]
    for case in cases:
        for row in case['initial_types']:
            for action in row['all_first_actions']:
                key = action.pop('second_check_key')
                action['second_check_id'] = check_ids[(tuple(key[0]), key[1])]
                action['first_action_image_id'] = image_ids[tuple(action['literal_F_boundary'])]
    return {'base': BASE, 'scope': 'two-step necessary 03-to-02 and 02-to-03 tests on the same complete F',
            'ordered_F_boundary': list(m.B14),
            'cases': cases,
            'normalized_second_palette_checks': [checks[key] for key in sorted(checks)],
            'complete_boundary_images': [
                {'literal_F_boundary': list(word),
                 'normalized_complete_kernel_id': kernel_ids[image_words[word][0]],
                 'whole_colour_inverse': list(image_words[word][1])}
                for word in sorted(image_words)],
            'complete_normalized_seven_point_kernels': [
                {'normalized_F_boundary': list(word), **kernels[word]} for word in sorted(kernels)],
            'complete_original_cap_kernel': [
                {'state': sid, 'canonical_D_rim': cap['states'][sid],
                 'complete_original_cap_fibres': helper.cap_lifts(tuple(cap['states'][sid]))[0]}
                for sid in sorted(used)],
            'normalization_rule': 'one whole-colour inverse is applied to every boundary, all seven mutable colours, and every cap assignment in a kernel reference',
            'unknown_cross_palette_partition_updates_filled_in': False,
            'independent_survivors_joined_as_actual_source': False,
            'ordinary_Type_I_excluded': False,
            'actual_F_source_realized': False,
            'whole_C14_family_enumerated': False,
            'V_equals_w_alias_covered': False}

def verify(actual, expected):
    require(actual == expected, 'two-step necessary coverage, complete fibre, or authority changed')

def controls(result):
    from copy import deepcopy
    rejected = 0
    for field in ('unknown_cross_palette_partition_updates_filled_in',
                  'independent_survivors_joined_as_actual_source', 'ordinary_Type_I_excluded',
                  'actual_F_source_realized', 'whole_C14_family_enumerated', 'V_equals_w_alias_covered'):
        damaged = deepcopy(result); damaged[field] = True
        try: verify(damaged, result)
        except ValueError: rejected += 1
    damaged = deepcopy(result)
    next(k for k in damaged['complete_normalized_seven_point_kernels']
         if k['complete_seven_point_fibre'])['complete_seven_point_fibre'].pop()
    try: verify(damaged, result)
    except ValueError: rejected += 1
    damaged = deepcopy(result)
    damaged['complete_boundary_images'][0]['whole_colour_inverse'] = [0, 0, 0, 0]
    try: verify(damaged, result)
    except ValueError: rejected += 1
    damaged = deepcopy(result)
    damaged['normalized_second_palette_checks'][0]['complete_necessary_NC_types'][0]['all_action_image_ids'].pop()
    try: verify(damaged, result)
    except ValueError: rejected += 1
    damaged = deepcopy(result)
    next(rows for kernel in damaged['complete_original_cap_kernel']
         for graph in kernel['complete_original_cap_fibres'].values()
         for rows in graph.values() if rows).pop()
    try: verify(damaged, result)
    except ValueError: rejected += 1
    require(rejected == 10, 'negative controls failed')
    return rejected

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--seed', type=int)
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json.gz')
    args = ap.parse_args()
    result = json.loads(packed(compute(args.seed)))
    rejected = controls(result)
    if args.build:
        with args.certificate.open('xb') as f:
            with gzip.GzipFile(fileobj=f, mode='wb', mtime=0) as z:
                z.write(packed(result))
    verify(json.loads(gzip.decompress(args.certificate.read_bytes())), result)
    print(json.dumps({'result': 'PASS',
                      'cases': [{ 'target': c['target'], 'first_split': c['first_split_containing_0'],
                                  'initial_types': len(c['initial_types']),
                                  'two_step_surviving_types': sum(t['passes_two_step_necessary_test'] for t in c['initial_types'])}
                                 for c in result['cases']],
                      'normalized_second_palette_checks': len(result['normalized_second_palette_checks']),
                      'boundary_images': len(result['complete_boundary_images']),
                      'complete_normalized_seven_point_kernels': len(result['complete_normalized_seven_point_kernels']),
                      'complete_original_cap_states': len(result['complete_original_cap_kernel']),
                      'negative_controls': rejected,
                      'new_source_exclusions': []}, sort_keys=True))

if __name__ == '__main__':
    main()
