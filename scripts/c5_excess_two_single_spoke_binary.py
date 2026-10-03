#!/usr/bin/env python3
"""Exclude an original binary omission for t=1, partition (2,2,1).

Retain original core contacts and glue the omitted component's complete ordered
binary relation. Nonempty relations are unions of singleton ordered pairs;
singleton gluing controls suffice with the paper union-distribution identity.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_excess_two_single_spoke_two_unary import orbit, verify_source
from c5_independent_support_capacity import ROWS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_single_spoke_binary/observations.json'
CORES = ROOT / 'artifacts/c5_941_two_spoke/observations.json'


def gluing_controls(source):
    inputs = {}
    for mi, mark in enumerate(source['marked_models']):
        for ri, row in enumerate(mark['rows']):
            key = tuple(map(tuple, row['ordered_port_relation']))
            inputs.setdefault(key, []).append([mi, ri])
    pairs = list(product(range(4), repeat=2))
    records, digest = [], sha256()
    singleton_checks = union_checks = 0
    for core, references in sorted(inputs.items()):
        roots = {t[0] for t in core}
        operator = sorted(t + pair for t in core for pair in pairs
                          if t[0] not in pair)
        fibers = []
        for pair in pairs:
            joined = [t for t in operator if t[4:] == pair]
            direct = sorted(t + pair for t in core
                            if t[0] != pair[0] and t[0] != pair[1])
            assert joined == direct
            assert {t[0] for t in joined} == roots - set(pair)
            fibers.append(joined)
            singleton_checks += 1
        assert all(fibers) == (len(roots) >= 3)
        # Full relations distribute over unions of ordered pairs. Check the
        # operator, independent Cartesian definition and forbidden-set formula
        # on every two-pair relation, including non-Cartesian binary relations.
        for i, j in combinations(range(16), 2):
            relation = [pairs[i], pairs[j]]
            joined = sorted(fibers[i] + fibers[j])
            direct = sorted(t + pair for t, pair in product(core, relation)
                            if t[0] != pair[0] and t[0] != pair[1])
            assert joined == direct
            forbidden = set(pairs[i]) & set(pairs[j])
            assert {t[0] for t in joined} == roots - forbidden
            digest.update(json.dumps([core, relation, joined]).encode())
            union_checks += 1
        records.append(dict(core_ordered_relation=core,
            source_mark_row_references=references, ordered_six_port_operator=operator,
            ordered_pairs=pairs, singleton_relation_fibers=fibers,
            root_colors=sorted(roots), survives_every_nonempty_binary_relation=all(fibers)))
    assert sum(len(r['source_mark_row_references']) for r in records) == 1480
    return dict(operators=records, singleton_relation_checks=singleton_checks,
        two_pair_relation_checks=union_checks, union_controls_sha256=digest.hexdigest(),
        arbitrary_relation_coverage='Paper identity: J(T,R) is the union of J(T,{p}) '
        'over ordered pairs p in R. Binary marginals are never substituted for R.',
        witness_lookup='First four coordinates index the original source core row '
        'ordered_port_relation and tuple_witnesses; last two coordinates use one '
        'full coloring of the actual omitted original binary C in the same frame.')


def build():
    source = verify_source()
    controls = gluing_controls(source)
    counts, records, core_records = Counter(), [], []
    for mi, mark in enumerate(source['marked_models']):
        root_sets = [sorted({t[0] for t in row['ordered_port_relation']})
                     for row in mark['rows']]
        core_records.append(dict(mark=mi, base_id=mark['base_id'], root=mark['root'],
            existing_spoke=mark['existing_spoke'], original_core_port_order=mark['port_order'],
            root_colors_by_row=root_sets,
            binary_universal_acceptance_mask=sum(1 << ri for ri, colors in enumerate(root_sets)
                                                 if len(colors) >= 3)))
        for candidate in (933, 941):
            for target in orbit(candidate):
                record = dict(mark=mi, candidate=candidate, target=target)
                if target & 1:
                    reason = 'core_rejects_required_row'
                    record['row'] = 0
                else:
                    witnesses = [ri for ri, colors in enumerate(root_sets)
                                 if len(colors) >= 3 and not (target >> ri & 1)]
                    assert witnesses, (mi, candidate, target)
                    ri = witnesses[0]
                    relation = mark['rows'][ri]['ordered_port_relation']
                    reason = 'three_root_colors_survive_original_binary'
                    # For EVERY ordered pair, save a compatible original core
                    # tuple/full-coloring index, not just the root projection.
                    lifts = [dict(binary_pair=list(pair), core_tuple_witness_index=next(
                        j for j, t in enumerate(relation) if t[0] not in pair))
                        for pair in product(range(4), repeat=2)]
                    record.update(row=ri, root_colors=root_sets[ri], binary_pair_lifts=lifts)
                record['reason'] = reason
                records.append(record)
                counts[f'{candidate}_{reason}'] += 1
    assert dict(counts) == {
        '933_core_rejects_required_row': 148,
        '933_three_root_colors_survive_original_binary': 592,
        '941_core_rejects_required_row': 296,
        '941_three_root_colors_survive_original_binary': 444,
    }
    paths = [Path(__file__).resolve(), CORES,
             ROOT / 'scripts/c5_excess_two_single_spoke_two_unary.py',
             ROOT / 'scripts/c5_941_two_spoke.py',
             ROOT / 'scripts/c5_independent_support_capacity.py']
    return dict(schema=1, scope='conditional t=1 (2,2,1) original binary omission',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        inherited_source_sha256=source['source_sha256'], pattern_order=ROWS,
        target_orbits={str(c): orbit(c) for c in (933, 941)},
        port_order=['r', 'original_A_x', 'original_A_y', 'original_W_w',
                    'original_C_u', 'original_C_v'],
        source_mark_semantics='148 original one-spoke marked cores; added-spoke records '
        'are unused. Name the retained binary A and the omitted binary C; either '
        'original omission is covered without graph symmetry or separate color normalization.',
        cores=core_records, gluing_controls=controls, exclusions=records,
        named_capacity_two_omissions=[
            dict(omitted=[binary], reason='six_port_exclusion_after_naming_omitted_binary_C')
            for binary in ['A', 'C']] + [
            dict(omitted=['spoke', 'W'], reason='paper_classification_internal_root_degree_four')],
        paper_dependencies=['connected all-degree-four disk single-missing classification',
            'triangle-bridge root coverage and original-contact-preserving tail transfer',
            'nonempty original binary ordered relation by contact slack',
            'same-boundary exact six-port gluing distributes over ordered pair unions',
            'a fixed binary coloring occupies at most two root colors'],
        summary=dict(sorted(counts.items()), bases=82, marked_roots=148,
            core_ten_row_checks=1480, candidate_comparisons=len(records), remaining=0,
            literal_gluing_inputs=len(controls['operators']),
            singleton_relation_checks=controls['singleton_relation_checks'],
            two_pair_relation_checks=controls['two_pair_relation_checks'],
            binary_pair_lifts=sum(len(r.get('binary_pair_lifts', [])) for r in records),
            cross_row_omission_constraints_used=False, new_support_geometry_used=False,
            new_source_graph_enumeration=False, new_lean_theorem=False,
            no_all_degree_four_subcore_is_paper_corollary=True,
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
