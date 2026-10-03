#!/usr/bin/env python3
"""Exclude rejected two-unary omission for t=2, original partition (2,1,1).

The fixed necessary domain even allows independent unary choices across rows.
Original ordered binary relations and one literal color frame are retained.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U
from c5_excess_two_three_unary import orbit
from c5_excess_two_two_binary import CORES as SHARED_CORES, verify_source

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_two_unary/observations.json'
# Name the actual input explicitly for the artifact rebuild dependency scanner.
CORES = ROOT / 'artifacts/c5_941_three_spoke/observations.json'
assert CORES == SHARED_CORES
UNARY_CHOICES = tuple(range(-1, 4))


def forbidden(color):
    return set() if color == -1 else {color}


def options(mark, target, ri):
    q = ROWS[ri]
    spokes = [e[0] for e in mark['existing_spokes']]
    sc = {q[b] for b in spokes}
    fa = set(mark['rows'][ri]['binary']['forbidden'])
    result = []
    for u, v in product(UNARY_CHOICES, repeat=2):
        fu, fv = forbidden(u), forbidden(v)
        if (sc | fa | fu | fv != U) != bool(target >> ri & 1):
            continue
        if fa | fu | fv == U:  # Both original spokes omitted must accept.
            continue
        # Omit either unary and either spoke; keep the other of each.
        if any({q[b]} | fa | f == U for b in spokes for f in (fu, fv)):
            continue
        result.append(dict(unary_forbidden_colors=[u, v],
                           binary_omission_rejects=sc | fu | fv == U))
    return result


def gluing_controls(source):
    """Full five-port operators, plus all 15 x 15 nonempty unary domains.

Every operator's first three coordinates reference the original core's full
coloring witnesses.  Unary domains are algebraic inputs, not source graphs.
Shared operators only deduplicate identical literal inputs for this check.
"""
    inputs = {}
    for mi, mark in enumerate(source['marked_models']):
        for ri, (q, row) in enumerate(zip(ROWS, mark['rows'], strict=True)):
            relation = tuple(map(tuple, row['binary']['ordered_relation']))
            sc = tuple(sorted({q[e[0]] for e in mark['existing_spokes']}))
            key = (relation, sc)
            inputs.setdefault(key, []).append([mi, ri])
    domains = [tuple(c for c in range(4) if bits >> c & 1) for bits in range(1, 16)]
    records, digest, checks = [], sha256(), 0
    for (relation, sc), references in sorted(inputs.items()):
        fa = set.intersection(*(set(t) for t in relation))
        operator = [(r, x, y, u, v) for x, y in relation
                    for r in range(4) if r not in (*sc, x, y)
                    for u, v in product(range(4), repeat=2) if r not in (u, v)]
        for mi, ri in references:
            row = source['marked_models'][mi]['rows'][ri]
            core = set(map(tuple, row['ordered_port_relation']))
            assert core == {(r, x, y) for x, y in relation
                            for r in range(4) if r not in (*sc, x, y)}
            assert all(t[:3] in core for t in operator)
        for su, sv in product(domains, repeat=2):
            fu = set(su) if len(su) == 1 else set()
            fv = set(sv) if len(sv) == 1 else set()
            joined = [t for t in operator if t[3] in su and t[4] in sv]
            direct = [(r, x, y, u, v) for r, (x, y), u, v
                      in product(range(4), relation, su, sv)
                      if r not in (*sc, x, y, u, v)]
            assert set(joined) == set(direct)
            assert {t[0] for t in joined} == U - set(sc) - fa - fu - fv
            digest.update(json.dumps([relation, sc, su, sv, sorted(joined)]).encode())
            checks += 1
        records.append(dict(binary_relation=relation, spoke_colors=sc,
                            source_mark_row_references=references,
                            ordered_five_port_operator=operator))
    assert len(records) == 111 and checks == 24975
    assert sum(len(r['source_mark_row_references']) for r in records) == 3980
    return dict(operators=records, full_five_port_checks=checks,
                restricted_relations_sha256=digest.hexdigest(),
                unary_domains=domains,
                core_witness_lookup='Use first three tuple coordinates in the referenced '
                    'source row ordered_port_relation and parallel tuple_witnesses; '
                    'unary coloring existence is conditional on the actual source domains.')


def build():
    source = verify_source()
    controls = gluing_controls(source)
    counts, records = Counter(), []
    for mi, mark in enumerate(source['marked_models']):
        for candidate in (933, 941):
            for target in orbit(candidate):
                record = dict(mark=mi, candidate=candidate, target=target)
                if target & 1:
                    reason = 'first_core_rejects_required_row'
                    record['row'] = 0
                else:
                    rows = [options(mark, target, i) for i in range(10)]
                    empty = [i for i, row in enumerate(rows) if not row]
                    forced = [i for i, row in enumerate(rows)
                              if row and all(o['binary_omission_rejects'] for o in row)]
                    if empty:
                        reason = 'empty_necessary_row'
                        record['row'] = empty[0]
                    else:
                        assert len(forced) >= 2, (mi, candidate, target, rows)
                        reason = 'same_binary_omission_rejects_two_rows'
                        record['forced_rows'] = [dict(row=i, options=rows[i]) for i in forced[:2]]
                record['reason'] = reason
                counts[f'{candidate}_{reason}'] += 1
                records.append(record)
    assert len(records) == 3980
    assert dict(counts) == {
        '933_first_core_rejects_required_row': 398,
        '933_empty_necessary_row': 508,
        '933_same_binary_omission_rejects_two_rows': 1084,
        '941_first_core_rejects_required_row': 796,
        '941_empty_necessary_row': 333,
        '941_same_binary_omission_rejects_two_rows': 861,
    }
    paths = [Path(__file__).resolve(), CORES,
             ROOT / 'scripts/c5_excess_two_two_binary.py',
             ROOT / 'scripts/c5_independent_support_capacity.py',
             ROOT / 'scripts/c5_941_two_spoke.py',
             ROOT / 'scripts/c5_941_three_spoke.py',
             ROOT / 'scripts/c5_excess_two_three_unary.py',
             ROOT / 'scripts/c5_excess_two_spoke_unary.py',
             ROOT / 'scripts/c5_excess_two_double_spoke.py']
    return dict(schema=1, scope='conditional t=2 (2,1,1) rejected original two-unary omission',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        pattern_order=ROWS, target_orbits={str(m): orbit(m) for m in (933, 941)},
        port_order=['r', 'original_A_x', 'original_A_y', 'original_U_u', 'original_V_v'],
        unary_forbidden_encoding='-1 means empty; 0..3 means that singleton color',
        source_mark_semantics='Original marked_models indices in hashed three-spoke artifact; '
            'no added spoke is used; ownership, attachments and ordered relations retained.',
        gluing_controls=controls, exclusions=records,
        paper_dependencies=['connected all-degree-four disk single-missing classification',
            'original ordered binary relation and contact-preserving tail transfer',
            'unary slack and exact five-port gluing',
            'same original binary omission accepts all but at most one row',
            'candidate double-spoke and t=2 spoke-plus-unary omissions accept all rows'],
        summary=dict(sorted(counts.items()), bases=118, marked_roots=398,
            candidate_comparisons=len(records), literal_gluing_inputs=111,
            full_five_port_checks=controls['full_five_port_checks'], remaining=0,
            unary_D_conservation_used=False, new_support_geometry_used=False,
            omitted_component_graph_enumeration=False, new_lean_theorem=False,
            full_source_disk_realizability_claimed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=1, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
