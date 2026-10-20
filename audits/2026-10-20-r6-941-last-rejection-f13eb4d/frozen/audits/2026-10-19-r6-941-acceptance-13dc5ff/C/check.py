#!/usr/bin/env python3
"""Independent exact support classifier; no source-realization search or imports."""
import argparse
from collections import Counter
import copy
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = HERE.parents[2]
BASE = '13dc5ff163045c85b5c82dde438eb5f275dab999'
ROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
CAT = 'audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json'
CONTROL = 'audits/2026-10-19-r6-941-leakage-b89c591/A/source-positive-certificate.json'


def canonical(word):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in word)


def proper(word):
    return all(a != b for a, b in zip(word, word[1:] + word[:1]))


def restricted_growth(n, word=(0,)):
    if len(word) == n:
        yield word
    else:
        for color in range(min(3, max(word) + 1) + 1):
            yield from restricted_growth(n, word + (color,))


def hits(mask, required, absent):
    return mask & required == required and mask & absent == 0


def classify(mask, rules):
    return [i for i, rule in enumerate(rules)
            if hits(mask, rule['required_mask'], rule['absent_mask'])]


def prime_rules(catalogue):
    """Every partial Boolean assignment, with a witness for deleting each literal."""
    rules = []
    for state in itertools.product((0, 1, 2), repeat=10):
        required = sum(1 << i for i, value in enumerate(state) if value == 1)
        absent = sum(1 << i for i, value in enumerate(state) if value == 2)
        if any(hits(mask, required, absent) for mask in catalogue):
            continue
        witnesses = []
        for i, value in enumerate(state):
            if value:
                relaxed = [mask for mask in catalogue
                           if hits(mask, required & ~(1 << i), absent & ~(1 << i))]
                if not relaxed:
                    break
                witnesses.append({'removed_row': i, 'removed_value': value,
                                  'catalogue_witness': min(relaxed)})
        else:
            rules.append({'required_mask': required, 'absent_mask': absent,
                          'required_rows': [ROWS[i] for i in range(10) if required >> i & 1],
                          'absent_rows': [ROWS[i] for i in range(10) if absent >> i & 1],
                          'literal_minimality_witnesses': witnesses})
    return rules


def cap_matrices():
    """Rebuild complete literal C8 fibres directly, retaining every p,h lift."""
    eight = [word for word in restricted_growth(8) if proper(word)]
    index = {word: i for i, word in enumerate(eight)}
    matrices = {name: [[0] * len(eight) for _ in ROWS]
                for name in ('G', 'Q1', 'Q2', 'GB')}
    fibre_records = []
    for ri, word in enumerate(ROWS):
        x, y, a, b, c = map(int, word)
        for n, right, left, q in itertools.product(range(4), repeat=4):
            boundary = (a, n, right, left, q, c, x, y)
            allowed = proper(boundary) and b not in (a, c, q)
            lifts = [[p, h] for p, h in itertools.product(range(4), repeat=2)
                     if allowed and p not in (a, b, q, n, h)
                     and h not in (p, q, left, right, n)]
            candidates = {'Q1': allowed and n == b and right == q,
                          'Q2': allowed and n == b and left == b,
                          'GB': allowed and b not in (n, left, right)}
            eid = index[canonical(boundary)] if proper(boundary) else None
            fibre_records.append([ri, n, right, left, q, eid, lifts,
                                  [int(candidates[name]) for name in ('Q1', 'Q2', 'GB')]])
            if allowed:
                matrices['G'][ri][eid] += len(lifts)
                for name, accepted in candidates.items():
                    matrices[name][ri][eid] += int(accepted)
    assert len(eight) == 274 and len(fibre_records) == 2560
    digest = hashlib.sha256(json.dumps(fibre_records, separators=(',', ':')).encode()).hexdigest()
    return eight, matrices, fibre_records, digest


def projection(matrix, counts):
    return [sum(a * b for a, b in zip(row, counts)) for row in matrix]


def support(counts):
    return sum(1 << i for i, count in enumerate(counts) if count > 0)


def compute():
    manifest = json.loads((AUDIT / 'INPUTS.json').read_text())
    assert manifest['base'] == BASE and len(manifest['files']) == 406
    frozen = {entry['path']: entry for entry in manifest['files']}
    hashes = {}
    for path in (CAT, CONTROL):
        raw = (ROOT / path).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        assert frozen[path]['sha256'] == digest and frozen[path]['bytes'] == len(raw)
        hashes[path] = digest
    catalogue = sorted(map(int, json.loads((ROOT / CAT).read_text())['cells']))
    assert len(catalogue) == len(set(catalogue)) == 132
    assert all(type(mask) is int and 0 <= mask < 1024 for mask in catalogue)
    rules = prime_rules(catalogue)
    assert len(rules) == 56
    classified = {mask for mask in range(1024) if not classify(mask, rules)}
    assert classified == set(catalogue), 'complete 1024-mask equivalence'
    assert all(rule['required_mask'].bit_count() <= 1 for rule in rules)
    assert all(a | b in classified for a in catalogue for b in catalogue), 'union closure'
    alpha_rules = [rule for rule in rules if rule['required_mask'] == 512]
    assert {rule['absent_mask'] for rule in alpha_rules} == {68, 82, 272}
    alternatives = []
    for absent in (68, 272):
        mask = 1023 & ~absent
        assert mask not in classified and mask & 512
        assert not hits(mask, 512, 82), 'not the old four-row certificate'
        alternatives.append({'support_mask': mask, 'required_mask': 512,
                             'absent_mask': absent, 'old_four_row_contract': False})
    eight, matrices, fibre_records, fibres_digest = cap_matrices()
    controls = json.loads((ROOT / CONTROL).read_text())['records']
    projections = []
    for record in controls:
        exterior = record['exterior_counts']
        assert len(exterior) == len(eight)
        assert all(type(n) is int and n >= 0 for n in exterior)
        counts = {name: projection(matrix, exterior) for name, matrix in matrices.items()}
        assert counts == record['graph_counts'], 'independent same-E complete cap projection'
        assert support(counts['G']) == 941
        projections.append({'name': record['name'], 'same_E_vector': True,
                            'graphs': {name: {'counts': values, 'support': support(values),
                                             'violated_rule_indices': classify(support(values), rules)}
                                       for name, values in counts.items()}})
    allk = next(record for record in projections if record['name'] == 'allK_source_positive')
    assert all(allk['graphs'][name]['support'] == 1023 and
               not allk['graphs'][name]['violated_rule_indices'] for name in ('Q1','Q2','GB'))
    submasks = [mask for mask in catalogue if mask & ~941 == 0]
    assert submasks == [165, 424, 429]
    assert classify(941, rules) == [next(i for i, rule in enumerate(rules)
                                         if rule['required_mask'] == 512 and rule['absent_mask'] == 82)]
    shape = Counter((rule['required_mask'].bit_count(), rule['absent_mask'].bit_count())
                    for rule in rules)
    return {'base': BASE, 'input_manifest_sha256': hashlib.sha256((AUDIT/'INPUTS.json').read_bytes()).hexdigest(),
            'frozen_input_sha256': hashes, 'literal_rows': list(ROWS), 'catalogue': catalogue,
            'rules': rules, 'rule_shape': [[p,z,n] for (p,z),n in sorted(shape.items())],
            'classified_catalogue_masks': sorted(classified), 'outside_catalogue_masks': 892,
            'all_pair_union_checks': len(catalogue)**2, 'union_closed': True,
            'alpha_rules': alpha_rules, 'alternative_full_support_witnesses': alternatives,
            'catalogue_submasks_of_941': submasks,
            'complete_cap_fibres': 2560, 'complete_cap_fibres_sha256': fibres_digest,
            'complete_cap_fibre_fields': ['row_id','n','R','L','q','C8_id','all_p_h_lifts','Q1_Q2_GB_flags'],
            'complete_cap_fibre_records': fibre_records,
            'C8_rows': [list(word) for word in eight], 'count_matrices': matrices,
            'control_projections': projections, 'source_realization_claimed': False,
            'new_smaller_bad_source_constructed': False, 'same_candidate_target_proved': False}


def verify(certificate, expected):
    assert certificate == expected, 'complete classifier and same-source control evidence'


def negative_controls(certificate, expected):
    records = []
    def reject(name, mutate):
        wrong = copy.deepcopy(certificate)
        mutate(wrong)
        try:
            verify(wrong, expected)
        except AssertionError:
            records.append({'name': name, 'rejected': True})
        else:
            raise AssertionError('accepted negative control: ' + name)
    reject('drop-one-prime-full-support-rule', lambda c: c['rules'].pop())
    reject('pretend-two-zero-certificate-is-the-old-contract',
           lambda c: c['alternative_full_support_witnesses'][0].__setitem__('old_four_row_contract', True))
    reject('replace-same-source-control-by-another-E-vector',
           lambda c: c['control_projections'][1].__setitem__('graphs', c['control_projections'][0]['graphs']))
    reject('drop-one-complete-p-h-lift',
           lambda c: next(row[6] for row in c['complete_cap_fibre_records'] if row[6]).pop())
    reject('promote-necessary-allK-control-to-realized-source',
           lambda c: c.__setitem__('source_realization_claimed', True))
    reject('turn-union-closure-into-single-witness-reduction',
           lambda c: c.__setitem__('new_smaller_bad_source_constructed', True))
    # Independently check the logical splice error, beyond mutation rejection.
    required, absent = 512, 82
    a, b = 1023 & ~2, 1023 & ~(16 | 64)
    assert not hits(a, required, absent) and not hits(b, required, absent)
    assert all(not (a if i == 1 else b) & (1 << i) for i in (1,4,6))
    records.append({'name': 'cross-candidate-zero-splice-is-not-a-rule-witness',
                    'rejected': True, 'candidate_masks': [a,b]})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE/'certificate.json')
    args = parser.parse_args()
    expected = compute()
    if args.build:
        with args.certificate.open('x') as output:
            json.dump(expected, output, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            output.write('\n')
    certificate = json.loads(args.certificate.read_text())
    verify(certificate, expected)
    result = {'ok': True, 'prime_rules': len(certificate['rules']),
              'exact_support_masks_checked': 1024, 'catalogue_union_closed': True,
              'alpha_rule_absent_masks': [68,82,272],
              'allK_source_positive_still_survives': True,
              'new_smaller_bad_source_constructed': False,
              'negative_controls': negative_controls(certificate, expected)}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
