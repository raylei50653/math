#!/usr/bin/env python3
"""Independent standard-library audit of U2 fixed-support constraints.

Read the primary certificate as immutable input; do not import its producer.
Derive the forbidden domain from all 65,536 binary contact relations, rebuild
boundary rows and local equality groups, and independently intersect literal
S4 constraints. This audits the finite support calculation, not the inherited
arbitrary-size core classification or a source-realization theorem.

Generate: python3 scripts/c5_excess_two_adjacent_two_mixed_core44_audit.py
Replay:   python3 scripts/c5_excess_two_adjacent_two_mixed_core44_audit.py --check
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'artifacts/c5_excess_two_adjacent_two_mixed_core44/observations.json'
OUT = INPUT.with_name('independent_support_audit.json')
PAIRS = tuple((a, b) for a in range(4) for b in range(4))
PERMUTATIONS = tuple(permutations(range(4)))


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':')) + '\n'


def boundary_rows():
    """Restricted-growth words directly, rather than normalized products."""
    result = []

    def extend(word):
        if len(word) == 5:
            if word[-1] != word[0]:
                result.append(tuple(word))
            return
        for color in range(min(3, max(word) + 1) + 1):
            if color != word[-1]:
                extend(word + [color])

    extend([0])
    assert len(result) == len(set(result)) == 10
    return tuple(sorted(result))


def forbidden_relation_domain():
    """Enumerate complete T and compute F by 16 independent avoidance masks."""
    avoiding = [sum(1 << i for i, (x, y) in enumerate(PAIRS)
                    if x != a and y != b) for a, b in PAIRS]
    row_masks = [15 << (4 * a) for a in range(4)]
    column_masks = [sum(1 << (4 * a + b) for a in range(4)) for b in range(4)]
    images, admitted, digest = set(), 0, sha256()
    for relation in range(65536):
        forbidden = sum(1 << i for i, allowed in enumerate(avoiding)
                        if relation & allowed == 0)
        capacity = all((forbidden & mask).bit_count() <= 1
                       for mask in row_masks + column_masks)
        digest.update(relation.to_bytes(2, 'little'))
        digest.update(forbidden.to_bytes(2, 'little'))
        digest.update(bytes([capacity]))
        if capacity:
            admitted += 1
            images.add(frozenset(pair for i, pair in enumerate(PAIRS)
                                 if forbidden >> i & 1))
    domain = sorted(images, key=lambda f: (len(f), tuple(sorted(f))))
    assert admitted == 65431 and len(domain) == 89
    assert all(len(f) <= 2 for f in domain)
    assert set(domain) == {frozenset((b, a) for a, b in f) for f in domain}
    return domain, admitted, digest.hexdigest()


def equality_shape(values):
    first_positions = sorted({values.index(color) for color in values})
    return tuple(first_positions.index(values.index(color)) for color in values)


def permute_relation(forbidden, permutation):
    return frozenset((permutation[a], permutation[b]) for a, b in forbidden)


def support_reference(mask, rows, forbidden_domain, saved):
    """Reconstruct all shapes and transports before consulting saved choices."""
    support = tuple(b for b in range(5) if mask >> b & 1)
    groups = {}
    for ri, row in enumerate(rows):
        values = tuple(row[b] for b in support)
        groups.setdefault(equality_shape(values), []).append(ri)
    assert saved['support_mask'] == mask and saved['actual_support'] == list(support)
    assert len(saved['shapes']) == len(groups) and len(saved['rows']) == len(rows)
    reference = []
    for sid, (shape, indices) in enumerate(groups.items()):
        ri = indices[0]
        values = tuple(rows[ri][b] for b in support)
        maps = {i: [p for p in PERMUTATIONS
                    if tuple(p[c] for c in values) == tuple(rows[i][b] for b in support)]
                for i in indices}
        stabilizers = maps[ri]
        choices = [f for f in forbidden_domain
                   if all(permute_relation(f, p) == f for p in stabilizers)]
        original = saved['shapes'][sid]
        assert original['shape'] == list(shape) and original['representative_row'] == ri
        assert original['values'] == list(values)
        assert set(map(tuple, original['stabilizers'])) == set(stabilizers)
        saved_choices = [frozenset(map(tuple, f)) for f in original['choices']]
        assert len(saved_choices) == len(set(saved_choices)) == len(choices)
        assert set(saved_choices) == set(choices)
        transports = {}
        for i in indices:
            assert maps[i]
            transported = []
            for f in saved_choices:
                images = {permute_relation(f, p) for p in maps[i]}
                assert len(images) == 1
                transported.append(images.pop())
            original_row = saved['rows'][i]
            assert original_row['shape'] == sid
            assert tuple(original_row['permutation']) in maps[i]
            assert [frozenset(map(tuple, f)) for f in original_row['forbidden_choices']] == transported
            transports[i] = transported
        reference.append(dict(rows=indices, choices=saved_choices, transports=transports))
    return reference


def target_orbits(rows):
    """Transport accepted equality patterns directly on the dihedral cycle."""
    positions = {row: ri for ri, row in enumerate(rows)}
    result = {}
    for mask in (933, 941):
        images = set()
        for direction in (-1, 1):
            for shift in range(5):
                image = 0
                for ri, row in enumerate(rows):
                    if mask >> ri & 1:
                        moved = tuple(row[(direction * b + shift) % 5] for b in range(5))
                        image |= 1 << positions[equality_shape(moved)]
                images.add(image)
        result[str(mask)] = sorted(images)
    return result


def audit_support(ks, target, reference, saved):
    """Use literal F sets and independent local-group intersections."""
    intersections, row_choices = [], {}
    for group in reference:
        allowed = set(range(len(group['choices'])))
        for ri in group['rows']:
            values = {i for i, f in enumerate(group['transports'][ri])
                      if bool(ks[ri] - f) == bool(target >> ri & 1)}
            row_choices[ri] = values
            allowed &= values
        intersections.append(allowed)
    empty = next((i for i, allowed in enumerate(intersections) if not allowed), None)
    if empty is not None:
        assert saved['empty_shape'] == empty
        assert 'subdivision_index' not in saved and 'forbidden_schedule' not in saved
        expected_conflicts = [dict(row_index=ri, allowed_choice_indices=sorted(row_choices[ri]))
                              for ri in reference[empty]['rows']]
        assert saved['conflicting_row_constraints'] == expected_conflicts
        assert not set.intersection(*(row_choices[ri] for ri in reference[empty]['rows']))
        status = 'incompatible'
        schedule = None
    else:
        assert 'empty_shape' not in saved
        assert saved['possible_choice_indices'] == [sorted(a) for a in intersections]
        assignment = saved['shape_assignment']
        assert len(assignment) == len(reference)
        assert assignment == [min(a) for a in intersections]
        schedule = [None] * len(ks)
        for index, group in enumerate(reference):
            assert assignment[index] in intersections[index]
            for ri in group['rows']:
                schedule[ri] = group['transports'][ri][assignment[index]]
        assert [frozenset(map(tuple, f)) for f in saved['forbidden_schedule']] == schedule
        actual_mask = sum(1 << ri for ri, (k, f) in enumerate(zip(ks, schedule, strict=True))
                          if k - f)
        assert actual_mask == target
        status = 'compatible'
    result = dict(status=status,
                  local_shape_choice_masks=[sum(1 << i for i in a) for a in intersections])
    if empty is not None:
        result['first_empty_shape'] = empty
    else:
        result['literal_forbidden_schedule'] = [sorted(f) for f in schedule]
        result['subdivision_index'] = saved['subdivision_index']
    return result


def build():
    input_bytes = INPUT.read_bytes()
    primary = json.loads(input_bytes)
    rows = boundary_rows()
    assert primary['pattern_order'] == [list(row) for row in rows]
    forbidden, admitted, algebra_digest = forbidden_relation_domain()
    assert len(primary['forbidden_pair_domain']) == len(forbidden)
    assert set(map(frozenset, (map(tuple, f) for f in primary['forbidden_pair_domain']))) == set(forbidden)
    orbits = target_orbits(rows)
    assert primary['target_D5_orbits'] == orbits
    assert len(primary['fixed_actual_support_domains']) == 32
    references = [support_reference(mask, rows, forbidden, saved)
                  for mask, saved in enumerate(primary['fixed_actual_support_domains'])]
    targets = sorted(set().union(*map(set, orbits.values())))
    counts, results, subdivision_keys = Counter(), [], {}
    for fi, form in enumerate(primary['forms']):
        for marked in form['marked_cores']:
            counts['marked_cores'] += 1
            roots = marked['original_root_order']
            assert len(marked['rows']) == len(rows)
            ks = [set(map(tuple, r['root_pairs'])) for r in marked['rows']]
            assert sum(1 << ri for ri, k in enumerate(ks) if k) == 1022
            comparisons = marked['target_comparisons']
            assert [t['target_mask'] for t in comparisons] == targets
            for test in comparisons:
                counts['target_comparisons'] += 1
                target = test['target_mask']
                empty = [ri for ri, k in enumerate(ks) if target >> ri & 1 and not k]
                capacity = [ri for ri, k in enumerate(ks)
                            if not (target >> ri & 1) and k and frozenset(k) not in forbidden]
                if empty:
                    assert test['exclusion'] == 'target_accepts_empty_core_row'
                    assert test['row_index'] == empty[0] and 'support_tests' not in test
                    counts['accepted_empty_exclusions'] += 1
                elif capacity:
                    assert test['exclusion'] == 'mixed11_forbidden_capacity'
                    assert test['row_index'] == capacity[0] and 'support_tests' not in test
                    counts['capacity_exclusions'] += 1
                else:
                    assert test['exclusion'] == 'fixed_support_transport_or_nondisk'
                    counts['fixed_support_comparisons'] += 1
                    assert len(test['support_tests']) == 32
                    checks = []
                    for mask, saved in enumerate(test['support_tests']):
                        assert saved['support_mask'] == mask
                        checked = audit_support(ks, target, references[mask], saved)
                        counts['support_queries'] += 1
                        counts[checked['status'] + '_supports'] += 1
                        checked['support_mask'] = mask
                        if checked['status'] == 'compatible':
                            key = (fi, tuple(roots), mask)
                            subdivision = primary['subdivisions'][checked['subdivision_index']]
                            assert subdivision['form_id'] == fi
                            assert subdivision['original_root_order'] == roots
                            assert subdivision['actual_support'] == [b for b in range(5) if mask >> b & 1]
                            subdivision_keys.setdefault(key, checked['subdivision_index'])
                            assert subdivision_keys[key] == checked['subdivision_index']
                        checks.append(checked)
                    results.append(dict(form_id=fi, original_root_order=roots,
                                        target_mask=target, support_checks=checks))
    assert counts == Counter(dict(marked_cores=570, target_comparisons=5700,
        accepted_empty_exclusions=1710, capacity_exclusions=3927,
        fixed_support_comparisons=63, support_queries=2016,
        incompatible_supports=1917, compatible_supports=99))
    for key in ('marked_cores', 'target_comparisons', 'accepted_empty_exclusions',
                'capacity_exclusions', 'fixed_support_comparisons', 'support_queries',
                'incompatible_supports'):
        assert counts[key] == primary['summary'][key]
    assert counts['compatible_supports'] == primary['summary']['compatible_nondisk_supports']
    assert len(subdivision_keys) == len(set(subdivision_keys.values())) == 27
    counts.update(normal_forms=len(primary['forms']), boundary_rows=len(rows),
        binary_relations=65536, admitted_binary_relations=admitted,
        forbidden_pair_choices=len(forbidden), fixed_support_domains=len(references),
        independently_derived_local_shapes=sum(len(r) for r in references),
        referenced_subdivisions=len(subdivision_keys))
    return dict(schema=1,
        scope='independent finite binary-relation and fixed-support S4 audit only',
        source_sha256={str(path.relative_to(ROOT)): sha256(data).hexdigest()
                       for path, data in ((INPUT, input_bytes),
                                          (Path(__file__).resolve(), Path(__file__).read_bytes()))},
        binary_relation_enumeration_sha256=algebra_digest,
        independently_derived_forbidden_domain=[sorted(f) for f in forbidden],
        support_comparisons=results, summary=dict(sorted(counts.items())),
        limitations='does not rederive whole-core colorings, verify topology paths, or audit inherited arbitrary-size classification')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    encoded = encode(data)
    if args.check:
        assert OUT.read_text() == encoded, 'independent audit differs; preserve historical inputs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print(json.dumps(dict(status='checked' if args.check else 'written',
                          **data['summary']), sort_keys=True))


if __name__ == '__main__':
    main()
