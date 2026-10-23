#!/usr/bin/env python3
"""Read-only composition and custody check; source coverage is in PROOF.md."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREVIOUS = 'audits/2026-10-23-941-types-wrong-side-round5-6b09cd4/'
CHILDREN = [
    'audits/2026-10-23-941-gamma8-n-stars-6b09cd4',
    'audits/2026-10-23-941-gamma8-empty-seven-6b09cd4',
    'audits/2026-10-23-941-gamma8-n7-review-6b09cd4',
]
INPUT_PATHS = {
    'docs/HANDOFF.md', 'docs/STATUS.md', 'docs/c5_kempe_guide.md',
    'docs/DOCUMENTATION.md',
    *[PREVIOUS + name for name in
      ['FINAL_MANIFEST.json', 'REPORT.md', 'PROOF.md', 'certificate.json', 'check.py']],
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def check_row(path, row):
    data = path.read_bytes()
    require((len(data), hashlib.sha256(data).hexdigest()) ==
            (row['bytes'], row['sha256']), 'authority drift: ' + str(path))


def custody(inputs_path):
    manifest = read(inputs_path)
    require(manifest['base'] == BASE, 'exclusive BASE')
    entries = manifest['inputs']
    require(len(entries) == len(INPUT_PATHS) and
            {row['path'] for row in entries} == INPUT_PATHS,
            'complete entry authority domain')
    routing = {}
    for row in entries:
        expected_kind = 'routing-entry' if row['path'].startswith('docs/') else 'immutable'
        require(row['authority'] == expected_kind, 'authority kind')
        require(row['snapshot'] == 'entry/' + row['path'], 'entry snapshot location')
        check_row(HERE / row['snapshot'], row)
        if expected_kind == 'immutable':
            check_row(ROOT / row['path'], row)
        else:
            routing[row['path']] = HERE / row['snapshot']
    previous = read(HERE / 'entry' / (PREVIOUS + 'FINAL_MANIFEST.json'))
    require(previous['base'] == BASE and len(previous['entries']) == 202,
            'complete round5 final manifest')
    for row in previous['entries']:
        check_row(routing.get(row['path'], ROOT / row['path']), row)
    children = read(HERE / 'CHILD_MANIFESTS.json')
    require(children['base'] == BASE and
            [row['directory'] for row in children['children']] == CHILDREN,
            'all three child authority domains')
    count = 0
    for row in children['children']:
        path = ROOT / row['directory'] / 'FINAL_MANIFEST.json'
        check_row(path, row['manifest'])
        child = read(path)
        require(child['base'] == BASE, 'child exclusive BASE')
        entries = child['entries'] if 'entries' in child else child['files']
        require(len(entries) == row['entries'], 'child manifest cardinality')
        for entry in entries:
            relative = (entry['path'] if entry['path'].startswith(row['directory'] + '/')
                        else row['directory'] + '/' + entry['path'])
            path = ROOT / relative
            require(path.resolve().is_relative_to((ROOT / row['directory']).resolve()),
                    'child exclusive write boundary')
            check_row(path, entry)
            count += 1
    return dict(round5_entries=202, child_entries=count, immutable_drift=0)


def expected():
    old = read(HERE / 'entry' / (PREVIOUS + 'certificate.json'))
    require(old['nonempty']['resource_seven_omega_remaining'] == ['N1', 'N3'],
            'literal remaining round5 branches')
    nonempty = read(ROOT / CHILDREN[0] / 'certificate.json')
    require(nonempty['conclusion']['paper_source_domain_excluded'] ==
            'nonempty_M2_Z7_omega_N1_or_N3' and
            nonempty['conclusion']['nonempty_Z_lower_bound_after_round5_K_exclusions'] == 8 and
            nonempty['conclusion']['nonempty_X_lower_bound_after_round5_K_exclusions'] == 9 and
            nonempty['conclusion']['complete_joint_original_star_rows'] == 0 and
            nonempty['conclusion']['K_external_tails_closed'] is False,
            'nonempty source proof and open K tails composition')
    empty = read(ROOT / CHILDREN[1] / 'certificate.json')
    require(empty['all_D_bound']['resource_lower_bound'] == '2*D-7' and
            empty['all_D_bound']['D8_min_exterior'] == 10,
            'empty wheel bound composition')
    require(empty['both_K']['remaining_extra_colors'] == [0, 2] and
            empty['both_K']['remaining_alias_d_U'] is False and
            empty['boundaries']['paper_D6_bothK_K8'] == 'OPEN',
            'K8 open stopping point')
    review = read(ROOT / CHILDREN[2] / 'certificate.json')
    require(review['N1_common_neighbor_minimum'] == 3 and
            review['terminal_snapshot_rows'] == {'N1': 130, 'N3': 201} and
            review['terminal_complete_omega_stars'] == [],
            'independent complete omega-star review')
    return dict(
        schema='941-common-N-star-round6-v1', base=BASE,
        source_domain=dict(Gamma_length=8, strict_inner_count=2,
                           necessary_types=11, same_original_G_F=True,
                           original_rotation_and_attachments=True,
                           ordered_B14_and_literal_phi_psi=True,
                           complete_components_empty_fibres_full_lifts=True,
                           arbitrary_spectators=True),
        nonempty=dict(resource_seven_excluded=['K0', 'K2', 'N1', 'N3'],
                      new_paper_exclusions=['N1', 'N3'],
                      rootless_K_resource_lower_bound=8,
                      exterior_lower_bound=9,
                      partial_N_star_rows={'N1': 130, 'N3': 201},
                      complete_omega_stars=0,
                      same_graph_short_proof_required=True),
        empty=dict(resource_lower_bound='max(7,2*D-7)',
                   alias_d_U_resource_lower_bound='max(7,2*D-6)',
                   exterior_lower_bound=8, D8_exterior_lower_bound=10,
                   D6_seven_resources_other_02_excluded=True,
                   D6_seven_resources_remaining=[
                       'two_N', 'one_N_one_K', 'K0_and_K2_K8_collar'],
                   both_K_requires_d_distinct_U=True,
                   both_K_N_degree_patterns=[[5, 5, 5, 5, 5, 7],
                                            [5, 5, 5, 5, 6, 6]],
                   K8_abstract_controls=21, K8_replacement='OPEN'),
        common_eleven_type_exterior_lower_bound=8,
        non_single_M2_exterior_lower_bound=10,
        authority=dict(finite_control='triggered and holds',
                       full_source_realizability='not triggered',
                       full_eleven_types='OPEN', general_wrong_side='OPEN',
                       common_k=23, W7_excluded_profiles=38,
                       W7_total_profiles=40, J1_targets=2, J2_targets=6,
                       general_smaller_bad='OPEN', new_Lean=False,
                       new_matching=False, new_LP=False))


def verify(actual, reference):
    require(actual == reference, 'integrated same-source contract mismatch')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--produce', action='store_true')
    parser.add_argument('--negative', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--inputs', type=Path, default=HERE / 'INPUTS.json')
    args = parser.parse_args()
    frozen = custody(args.inputs)
    reference = expected()
    if args.produce:
        with args.certificate.open('x') as out:
            json.dump(reference, out, ensure_ascii=False, indent=2, sort_keys=True)
            out.write('\n')
    actual = read(args.certificate)
    verify(actual, reference)
    negatives = []
    if args.negative:
        mutations = [
            ('lose_N3_branch', lambda d: d['nonempty']['resource_seven_excluded'].pop()),
            ('weaken_nonempty_bound', lambda d: d['nonempty'].update(exterior_lower_bound=8)),
            ('raise_common_bound', lambda d: d.update(common_eleven_type_exterior_lower_bound=9)),
            ('close_K8_without_replacement', lambda d: d['empty'].update(K8_replacement='excluded')),
            ('drop_U_alias', lambda d: d['empty'].update(alias_d_U_resource_lower_bound='max(7,2*D-7)')),
            ('exclude_spectators', lambda d: d['source_domain'].update(arbitrary_spectators=False)),
            ('claim_full_source', lambda d: d['authority'].update(full_source_realizability='triggered and holds')),
            ('raise_common_k', lambda d: d['authority'].update(common_k=24)),
        ]
        for name, mutation in mutations:
            bad = copy.deepcopy(actual)
            mutation(bad)
            try:
                verify(bad, reference)
            except ValueError:
                negatives.append(name)
            else:
                raise ValueError('negative accepted: ' + name)
    print(json.dumps(dict(status='PASS', custody=frozen,
                          nonempty_min_exterior=9, empty_min_exterior=8,
                          empty_D8_min_exterior=10, common_min_exterior=8,
                          full_source='not triggered',
                          negative_rejected=negatives), sort_keys=True))


if __name__ == '__main__':
    main()
