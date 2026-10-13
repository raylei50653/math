#!/usr/bin/env python3
"""Three-target h <= 2 collar audit, using only the audit's frozen inputs.

The collar columns are finite annulus computations, not a graph-source search.
The source-level deduction additionally needs the paper's actual-collar lemma.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
FROZEN = AUDIT / 'frozen'
OLD = FROZEN / 'audits/2026-10-12-neartri-complete-relation-reductions-5d70a399'
C7 = FROZEN / 'audits/2026-10-13-c7-joint-kempe-19209f4c/joint'
TARGETS = (932, 933, 941)


def canonical(value):
    return json.loads(json.dumps(value))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_inputs():
    manifest = json.loads((AUDIT / 'INPUTS.json').read_text())
    for entry in manifest['inputs']:
        path = FROZEN / entry['path']
        assert path.stat().st_size == entry['bytes'], f'input size: {path}'
        assert sha256(path) == entry['sha256'], f'input hash: {path}'
    return dict(base=manifest['base'], manifest_sha256=sha256(AUDIT / 'INPUTS.json'),
                frozen_files_verified=len(manifest['inputs']))


def annulus(t):
    outer = [f'b{i}' for i in range(5)]
    inner = []
    supports = []
    for i in range(5):
        inner.append(f'a{i}')
        supports.append([outer[i], outer[(i+1) % 5]])
        for j in range(1, t[(i+1) % 5]+1):
            inner.append(f'y{(i+1) % 5}_{j}')
            supports.append([outer[(i+1) % 5]])
    edges = [[outer[i], outer[(i+1) % 5]] for i in range(5)]
    edges += [[inner[i], inner[(i+1) % len(inner)]] for i in range(len(inner))]
    edges += [[v, b] for v, bs in zip(inner, supports) for b in bs]
    faces = [[outer[i], outer[(i+1) % 5], f'a{i}'] for i in range(5)]
    for i in range(5):
        fan = [f'a{(i-1) % 5}'] + [f'y{i}_{j}' for j in range(1, t[i]+1)] + [f'a{i}']
        faces += [[outer[i], u, v] for u, v in zip(fan, fan[1:])]
    return dict(outer_vertex_order=outer, inner_vertex_order=inner,
                inner_supports_named=supports, annulus_edges=edges,
                annulus_faces=faces, joint_vertex_order=outer+inner)


def explicit_fibres(old, cols, lifts, patterns):
    """Each inner representative is fixed once; every outer fibre, even empty."""
    fibres = []
    for i, (q, words) in enumerate(zip(patterns, lifts)):
        by_outer_row = [[] for _ in old.P5]
        for b in words:
            by_outer_row[old.I5[old.norm(b)]].append(list(b)+list(q))
        recovered = sum(1 << j for j, fibre in enumerate(by_outer_row) if fibre)
        assert recovered == cols[i]
        fibres.append(by_outer_row)
    return fibres


def build():
    custody = validate_inputs()
    old = load_module('frozen_collar', OLD / 'collar_checker.py')
    old_payload = old.build()
    assert canonical(old_payload) == json.loads((OLD / 'collar_certificate.json').read_text()), 'old collar replay mismatch'
    count = load_module('frozen_count', C7 / 'count_identity.py')
    count_payload = count.build()
    assert canonical(count_payload) == json.loads((C7 / 'count_identity_certificate.json').read_text()), 'C7 count replay mismatch'

    # Retain all original 21 collars, their order, columns, literal lifts, and
    # the original two checks; the sole new target is 932.
    cases = []
    for case_index, old_case in enumerate(old_payload['cases']):
        t = tuple(old_case['boundary_extras'])
        n = 5+sum(t)
        cols = old_case['column_masks']
        lifts = old_case['outer_lifts_for_each_named_inner_row']
        case = dict(old_case)
        case.update(annulus(t))
        case['case_index'] = case_index
        case['joint_full_lifts_by_inner_index_then_outer_index'] = explicit_fibres(old, cols, lifts, old.patterns(n))
        case['targets'] = [old.prune(cols, old_payload['kempe_obligations'][str(n)], target) for target in TARGETS]
        assert case['targets'][1:] == old_case['targets'], 'original target changed'
        for result in case['targets']:
            result['final_excluded'] = result['excluded']
            result['exclusion_method'] = 'complete transfer and necessary Kempe screen' if result['excluded'] else None
        cases.append(case)

    survivors = [(c, r) for c in cases for r in c['targets'] if not r['excluded']]
    assert len(survivors) == 1
    case, result = survivors[0]
    assert case['boundary_extras'] == (0, 0, 1, 0, 1) and result['target'] == 941
    assert result['fixed_point'] == count_payload['upper_mask']
    assert case['inner_vertex_order'] == ['a0', 'a1', 'y2_1', 'a2', 'a3', 'y4_1', 'a4']
    assert canonical(old.patterns(7)) == canonical(count_payload['pattern_order'])
    assert count_payload['upper_preimages_of_outer_word'] == [6, 58, 89]
    assert count_payload['outer_accepted_word'] == [0, 1, 2, 3, 2]
    assert all(all(not (result['fixed_point'] >> term['index'] & 1) for term in identity['rhs'])
               for identity in count_payload['identities'])
    assert count_payload['identities'][4]['lhs'] == [dict(index=6, word=old.patterns(7)[6], coefficient=1),
                                                    dict(index=35, word=old.patterns(7)[35], coefficient=1)]
    result['final_excluded'] = True
    result['exclusion_method'] = 'C7 universal extension-count identities plus nonnegativity, exact transfer=941'
    result['count_certificate_reference'] = 'c7_count_identity_replay'

    table = []
    for c in cases:
        for r in c['targets']:
            table.append(dict(case_index=c['case_index'], h=sum(c['boundary_extras']),
                              boundary_extras=c['boundary_extras'], target=r['target'],
                              initial_rows=r['initial'].bit_count(), fixed_point_rows=r['fixed_point'].bit_count(),
                              possible_outer_union=r['possible_outer_union'],
                              transfer_kempe_excluded=r['excluded'], final_excluded=r['final_excluded']))
    assert len(table) == 63 and all(r['final_excluded'] for r in table)
    assert all(r['fixed_point_rows'] == 0 for r in table if r['target'] == 932)
    return dict(schema='c5-no4ct-three-target-collar-v1', custody=custody,
                boundary_order=old_payload['boundary_order'], color_frame=old_payload['color_frame'],
                outer_pattern_order=old_payload['outer_pattern_order'],
                inner_pattern_orders=old_payload['inner_pattern_orders'],
                complementary_splits=old_payload['complementary_splits'],
                kempe_obligations=old_payload['kempe_obligations'], cases=cases,
                finite_query_table=table, c7_count_identity_replay=count_payload,
                input_certificates={str(p.relative_to(FROZEN)): sha256(p) for p in
                                    (OLD / 'collar_certificate.json', C7 / 'count_identity_certificate.json')},
                summary=dict(named_collars=21, target_queries=63, new_932_queries=21,
                             transfer_kempe_exclusions=62, count_identity_exclusions=1, final_exclusions=63),
                evidence_scope=dict(finite_computation='complete annulus fibres, Kempe necessary conditions, and C7 exact count identities',
                                    paper_input='actual named simple collar obtained from crosscut exclusion and absence of separating triangles',
                                    graph_source_search=False, target_source_status='not triggered',
                                    four_color_theorem_used=False, stronger_arbitrary_C7_subset_U_theorem_used=False,
                                    unbounded_932_933_941='OPEN', general_K_infinity_equals_K_le_5='OPEN',
                                    lean_formalization='not performed'))


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    payload = build()
    if args.write:
        with args.certificate.open('x') as stream:
            json.dump(payload, stream, sort_keys=True, separators=(',', ':'))
            stream.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == canonical(payload), 'certificate mismatch'
    print(json.dumps(dict(status='PASS', **payload['summary'], target_source_status='not triggered',
                          frozen_files_verified=payload['custody']['frozen_files_verified'])))


if __name__ == '__main__':
    main()
