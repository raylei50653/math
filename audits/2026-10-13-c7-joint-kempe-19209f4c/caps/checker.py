#!/usr/bin/env python3
"""Exact relation completion from frozen named collar and existing cap corpus.

This is a universal necessary relation restriction, not a graph search or a
realizability assertion. No SAT solver or graph enumeration is used.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = '2026-10-12-neartri-complete-relation-reductions-5d70a399'
COLLAR = HERE.parent / 'frozen' / 'audits' / OLD / 'collar_certificate.json'
CAPS = HERE / 'frozen' / 'cap_probe.json'


def dump(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n'


def rows(mask, n=91):
    return [i for i in range(n) if mask >> i & 1]


def close(mask, table):
    rounds = []
    while True:
        bad = []
        for i in rows(mask):
            for j, options in enumerate(table[i]):
                if not any(o & ~mask == 0 for o in options):
                    bad.append([i, j])
                    break
        if not bad:
            return mask, rounds
        rounds.append({'before': mask, 'removals': bad})
        mask &= ~sum(1 << i for i, j in bad)


def outer(mask, columns):
    result = 0
    for i in rows(mask):
        result |= columns[i]
    return result


def build():
    c = json.loads(COLLAR.read_text())
    d = json.loads(CAPS.read_text())
    case = next(x for x in c['cases'] if x['boundary_extras'] == [0, 0, 1, 0, 1])
    target = next(x for x in case['targets'] if x['target'] == 941)
    upper = target['fixed_point']
    patterns = c['inner_pattern_orders']['7']
    table = c['kempe_obligations']['7']
    columns = case['column_masks']
    cap_masks = sorted(map(int, d['relations']))
    assert upper == d['inner_mask'] and patterns == d['pattern_order']
    leave_one_out = []
    mandatory = 0
    for i in rows(upper):
        fixed, rounds = close(upper & ~(1 << i), table)
        union = outer(fixed, columns)
        fails = [r for r in cap_masks if not r & fixed]
        if union != 941:
            mandatory |= 1 << i
        leave_one_out.append(dict(removed=i, rounds=rounds, fixed_point=fixed,
                                  outer_union=union, first_missed_cap=fails[0] if fails else None))
    optional = rows(upper & ~mandatory)
    completion_checks = []
    residuals = []
    for bits in range(1 << len(optional)):
        mask = mandatory | sum(1 << i for j, i in enumerate(optional) if bits >> j & 1)
        fixed, rounds = close(mask, table)
        union = outer(mask, columns)
        completion_checks.append(dict(optional_bits=bits, fixed_point=fixed,
                                      outer_union=union, feasible=fixed == mask and union == 941))
        if fixed != mask or union != 941:
            continue
        accepted = rows(mask)
        residuals.append(dict(mask=mask, optional_bits=bits, cardinality=len(accepted),
                              accepted_indices=accepted,
                              rejected_indices=rows(((1 << 91) - 1) & ~mask),
                              accepted_words=[''.join(map(str, patterns[i])) for i in accepted],
                              kempe_orbit_witnesses=[
                                  [min(o for o in options if o & ~mask == 0) for options in table[i]]
                                  for i in accepted],
                              outer_union=union))
    minimal = [r['mask'] for r in residuals if not any(
        s['mask'] != r['mask'] and s['mask'] & r['mask'] == s['mask'] for s in residuals)]
    hits = [[(mask & cap & -(mask & cap)).bit_length() - 1 for cap in cap_masks]
            for mask in minimal]
    assert all(i >= 0 for vector in hits for i in vector)
    intersections = set(r & upper for r in cap_masks)
    cap_antichain = sorted(m for m in intersections if not any(
        n != m and n & m == n for n in intersections))
    singletons = [m for m in cap_antichain if m.bit_count() == 1]
    singleton_caps = [dict(intersection=m, cap_mask=next(r for r in cap_masks if r & upper == m),
                           description=d['relations'][str(next(r for r in cap_masks if r & upper == m))])
                      for m in singletons]
    assert upper.bit_count() == 55 and mandatory.bit_count() == 45
    assert len(optional) == 10 and len(residuals) == 72
    assert sorted(m.bit_count() for m in minimal) == [47, 48, 48, 49]
    assert all(any(m & r['mask'] == m for m in minimal) for r in residuals)
    # Caps and outer941 independently force the same mandatory rows under
    # the inherited Kempe obligations; no cap strengthens the 72-mask screen.
    assert [r['removed'] for r in leave_one_out if r['first_missed_cap'] is not None] == rows(mandatory)
    concise_implications = []
    for i, split, forced in [(6, 2, 19), (19, 0, 12), (12, 2, 89), (89, 2, 42),
                              (58, 2, 57), (57, 0, 37), (37, 2, 42)]:
        options = [o for o in table[i][split] if o & ~upper == 0]
        assert len(options) == 1 and options[0] >> forced & 1
        concise_implications.append(dict(row=i, split=split, forced=forced,
                                         unique_allowed_orbit=options[0], orbit_indices=rows(options[0])))
    outer01232 = [i for i in rows(upper) if columns[i] >> 9 & 1]
    assert outer01232 == [6, 58, 89]
    return dict(
        input_sha256={str(p.relative_to(HERE.parent)): sha256(p.read_bytes()).hexdigest()
                      for p in (COLLAR, CAPS)},
        boundary_extras=case['boundary_extras'], inner_supports=case['inner_supports'],
        outer_pattern_order=c['outer_pattern_order'], inner_pattern_order=patterns,
        target=941, accepted_outer_indices=rows(941, 10), rejected_outer_indices=rows(1023 ^ 941, 10),
        upper_mask=upper, mandatory_mask=mandatory, mandatory_indices=rows(mandatory),
        mandatory_words=[''.join(map(str, patterns[i])) for i in rows(mandatory)],
        optional_indices=optional, optional_words=[''.join(map(str, patterns[i])) for i in optional],
        forbidden_indices=rows(((1 << 91) - 1) & ~upper),
        leave_one_out=leave_one_out, completion_checks=completion_checks, residuals=residuals,
        minimal_masks=minimal, cardinality_histogram=dict(sorted(Counter(r['cardinality'] for r in residuals).items())),
        cap_mask_order=cap_masks, minimal_mask_cap_hit_indices=hits,
        cap_intersections_count=len(intersections), cap_intersections_minimal_antichain=cap_antichain,
        singleton_caps=singleton_caps,
        row42_forcing=dict(outer_word='01232', outer_index=9, inner_preimages=outer01232,
                           forced_inner_index=42, forced_inner_word='0120231',
                           implications=concise_implications),
        source_status='not triggered', realizability='not_decided_by_Kempe_and_existing_caps',
        conclusion='Every eligible actual relation is one of these 72 abstract masks; no mask is claimed realized.')


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    result = build()
    if args.write:
        with args.certificate.open('x') as out:
            out.write(dump(result))
    else:
        assert json.loads(args.certificate.read_text()) == json.loads(dump(result)), 'certificate mismatch'
    print(json.dumps(dict(status='PASS', mandatory_rows=len(result['mandatory_indices']),
                          optional_rows=len(result['optional_indices']), residual_relations=len(result['residuals']),
                          minimal_relation_size=min(r['cardinality'] for r in result['residuals']),
                          cap_controls=len(result['cap_mask_order']), source_status=result['source_status']), sort_keys=True))


if __name__ == '__main__':
    main()
