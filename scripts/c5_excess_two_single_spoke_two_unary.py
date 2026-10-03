#!/usr/bin/env python3
"""Exclude two original unary omissions for t=1, partition (2,1,1,1).

The retained binary and unary are original components of the same core.
Two arbitrary nonempty unary domains are glued in one literal color frame.
Arbitrary-size coverage and contact-preserving transfer are paper inputs.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_independent_support_capacity import B, ROWS, U, components
from c5_941_two_spoke import base_record, component_record, relabel_mask, search

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_single_spoke_two_unary/observations.json'
CORES = ROOT / 'artifacts/c5_941_two_spoke/observations.json'


def literal(value):
    return json.loads(json.dumps(value))


def orbit(mask):
    return sorted({relabel_mask(mask, [(s*j + t) % 5 for j in range(5)])
                   for s in (-1, 1) for t in range(5)})


def verify_source():
    source = json.loads(CORES.read_text())
    for path, digest in source['source_sha256'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    assert source['pattern_order'] == literal(ROWS)
    bases, marks = source['bases'], source['marked_models']
    for base in bases:
        assert literal(base_record(base['family'], base['input_index'], base)) == base
    expected = {(bi, r) for bi, base in enumerate(bases)
                for r in range(5, base['vertices'])
                if sum(r in e and min(e) >= 5 for e in base['edges']) == 3}
    assert len(marks) == len(expected) == 148 and len(bases) == 82
    assert {(m['base_id'], m['root']) for m in marks} == expected
    for mark in marks:
        base = bases[mark['base_id']]
        n, r = base['vertices'], mark['root']
        edges = set(map(tuple, base['edges']))
        inside = set(range(5, n))
        nb = {v: {b if a == v else a for a, b in edges if v in (a, b)}
              for v in range(n)}
        spoke, = sorted(nb[r] & B)
        parts = components(inside - {r}, edges)
        binary, = [vs for vs in parts if len(set(vs) & nb[r]) == 2]
        unary, = [vs for vs in parts if len(set(vs) & nb[r]) == 1]
        x, y = sorted(set(binary) & nb[r])
        w, = sorted(set(unary) & nb[r])
        assert len(parts) == 2 and (x, y) in edges
        assert mark['existing_spoke'] == [spoke, r]
        assert mark['port_order'] == [r, x, y, w]
        assert mark['binary_vertices'] == binary and mark['binary_contacts'] == [x, y]
        assert mark['unary_vertices'] == unary and mark['unary_contact'] == w
        assert mark['binary_support'] == sorted(set.union(*(nb[v] & B for v in binary)))
        assert mark['unary_support'] == sorted(set.union(*(nb[v] & B for v in unary)))
        for q, row in zip(ROWS, mark['rows'], strict=True):
            assert row['row'] == list(q)
            assert row['binary'] == literal(component_record(binary, [x, y], edges, q))
            assert row['unary'] == literal(component_record(unary, [w], edges, q))
            joined = {(a, c, d, e[0]) for c, d in row['binary']['ordered_relation']
                      for e in row['unary']['ordered_relation']
                      for a in U - {q[spoke], c, d, e[0]}}
            actual = {tuple(f[v] for v in mark['port_order'])
                      for f in search(inside, edges, dict(enumerate(q)))}
            saved = list(map(tuple, row['ordered_port_relation']))
            assert actual == joined == set(saved) and len(saved) == len(set(saved))
            for t, witness in zip(saved, row['tuple_witnesses'], strict=True):
                assert len(witness) == n and witness[:5] == list(q)
                assert all(c in U for c in witness)
                assert tuple(witness[v] for v in mark['port_order']) == t
                assert all(witness[a] != witness[b] for a, b in edges)
        assert [bool(row['ordered_port_relation']) for row in mark['rows']] == [False] + [True]*9
    return source


def gluing_controls(source):
    inputs = {}
    for mi, mark in enumerate(source['marked_models']):
        for ri, row in enumerate(mark['rows']):
            key = tuple(map(tuple, row['ordered_port_relation']))
            inputs.setdefault(key, []).append([mi, ri])
    domains = [tuple(c for c in range(4) if bits >> c & 1) for bits in range(1, 16)]
    records, digest, checks = [], sha256(), 0
    for core, references in sorted(inputs.items()):
        roots = {t[0] for t in core}
        operator = sorted(t + (u, v) for t in core
                          for u, v in product(range(4), repeat=2) if t[0] not in (u, v))
        accepted = []
        for su, sv in product(domains, repeat=2):
            joined = [t for t in operator if t[4] in su and t[5] in sv]
            direct = sorted(t + (u, v) for t, u, v in product(core, su, sv)
                            if t[0] != u and t[0] != v)
            assert joined == direct
            fu = set(su) if len(su) == 1 else set()
            fv = set(sv) if len(sv) == 1 else set()
            assert {t[0] for t in joined} == roots - fu - fv
            digest.update(json.dumps([core, su, sv, joined]).encode())
            accepted.append(bool(joined))
            checks += 1
        assert all(accepted) == (len(roots) >= 3)
        records.append(dict(core_ordered_relation=core,
            source_mark_row_references=references, ordered_six_port_operator=operator,
            root_colors=sorted(roots), survives_all_domain_pairs=all(accepted)))
    assert sum(len(r['source_mark_row_references']) for r in records) == 1480
    return dict(operators=records, unary_domains=domains, full_six_port_checks=checks,
        restricted_relations_sha256=digest.hexdigest(),
        witness_lookup='The first four coordinates index the referenced source core row '
        'ordered_port_relation and tuple_witnesses. U and V full colorings are supplied '
        'by the actual original nonempty endpoint domains, not free graph vertices.')


def build():
    source = verify_source()
    controls = gluing_controls(source)
    counts, records, core_records = Counter(), [], []
    for mi, mark in enumerate(source['marked_models']):
        root_sets = [sorted({t[0] for t in row['ordered_port_relation']}) for row in mark['rows']]
        forced_mask = sum(1 << ri for ri, roots in enumerate(root_sets) if len(roots) >= 3)
        core_records.append(dict(mark=mi, base_id=mark['base_id'], root=mark['root'],
            existing_spoke=mark['existing_spoke'], original_core_port_order=mark['port_order'],
            root_colors_by_row=root_sets, two_unary_universal_acceptance_mask=forced_mask))
        for candidate in (933, 941):
            for target in orbit(candidate):
                record = dict(mark=mi, candidate=candidate, target=target)
                if target & 1:
                    reason = 'core_rejects_required_row'
                    record['row'] = 0
                else:
                    witnesses = [ri for ri, roots in enumerate(root_sets)
                                 if len(roots) >= 3 and not (target >> ri & 1)]
                    assert witnesses, (mi, candidate, target)
                    ri = witnesses[0]
                    relation = mark['rows'][ri]['ordered_port_relation']
                    reason = 'three_root_colors_survive_two_unaries'
                    record.update(row=ri, root_colors=root_sets[ri],
                        core_tuple_witness_indices=[next(j for j, t in enumerate(relation) if t[0] == c)
                                                    for c in root_sets[ri]])
                record['reason'] = reason
                records.append(record)
                counts[f'{candidate}_{reason}'] += 1
    assert dict(counts) == {
        '933_core_rejects_required_row': 148,
        '933_three_root_colors_survive_two_unaries': 592,
        '941_core_rejects_required_row': 296,
        '941_three_root_colors_survive_two_unaries': 444,
    }
    paths = [Path(__file__).resolve(), CORES, ROOT / 'scripts/c5_941_two_spoke.py',
             ROOT / 'scripts/c5_independent_support_capacity.py']
    return dict(schema=1, scope='conditional t=1 (2,1,1,1) original two-unary omission',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        inherited_source_sha256=source['source_sha256'], pattern_order=ROWS,
        target_orbits={str(c): orbit(c) for c in (933, 941)},
        port_order=['r', 'original_A_x', 'original_A_y', 'original_W_w', 'original_U_u', 'original_V_v'],
        source_mark_semantics='148 original one-spoke marked cores from the hashed input; '
        'the input unary is W. Its added-spoke records are not used. All three choices '
        'of omitted unary pair follow by naming the retained unary W, with no graph '
        'automorphism or independent color normalization assumed.',
        cores=core_records, gluing_controls=controls, exclusions=records,
        named_capacity_two_omissions=[
            dict(omitted=list(pair), reason='six_port_exclusion_after_naming_retained_unary_W')
            for pair in [('U', 'V'), ('U', 'W'), ('V', 'W')]] + [
            dict(omitted=['spoke', unit], reason='paper_classification_internal_root_degree_four')
            for unit in ['U', 'V', 'W']] + [
            dict(omitted=['A'], reason='paper_classification_three_bridge_root')],
        paper_dependencies=['connected all-degree-four disk single-missing classification',
            'triangle-bridge root coverage and original-contact-preserving tail transfer',
            'classified cores have internal degree at most three; degree-three roots lie on triangles',
            'nonempty original unary endpoint relations by slack',
            'same-boundary exact six-port gluing; two unaries forbid at most two colors'],
        summary=dict(sorted(counts.items()), bases=82, marked_roots=148,
            core_ten_row_checks=1480, candidate_comparisons=len(records),
            literal_gluing_inputs=len(controls['operators']),
            full_six_port_checks=controls['full_six_port_checks'], remaining=0,
            cross_row_omission_constraints_used=False, unary_D_conservation_used=False,
            new_support_geometry_used=False, new_source_graph_enumeration=False,
            no_all_degree_four_subcore_is_paper_corollary=True,
            new_lean_theorem=False, full_source_disk_realizability_claimed=False))


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
