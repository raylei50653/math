#!/usr/bin/env python3
"""Read-only cross-check of independently produced complete audit relations."""
from hashlib import sha256
import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, why):
    if not ok:
        raise ValueError(why)


def read(name):
    raw = (HERE / name).read_bytes()
    return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)


def main():
    root = read('certificate.json.gz')
    six = read('six_degree/certificate-v2.json.gz')
    double = read('double_five/certificate.json.gz')
    geometry = read('geometry/runs/normal.json')
    originals = root['short_initial_full_fibres']['nine_identity_cases_including_the_excluded_alias_control']
    compared_initial = 0
    for row in six['ordinary_C14_cases']:
        own = next(r for r in originals if r['kind'] == 'I' and r['target'] == row['target']
                   and r['actual_U'] == 'U' and r['actual_V'] == 'V')
        require([r['joint_colours'] for r in own['all_joint_lifts']] ==
                [r['mutable_colors'] for r in row['complete_initial_seven_point_fibre']['complete_seven_point_fibre']],
                'independent complete I initial relation differs')
        compared_initial += 1
    for row in double['original_identity_cases']:
        own = next(r for r in originals if r['kind'] == 'II' and r['target'] == row['target']
                   and r['actual_U'] == row['U_actual_name'] and r['actual_V'] == row['V_actual_name'])
        full = double['complete_literal_joint_kernel_pool'][row['original_joint_kernel_ref']]
        require(own['mutable_order'] == full['inner_order'], 'different mutable vertex identities')
        require([r['joint_colours'] for r in own['all_joint_lifts']] ==
                [r['all_eight_inner_colors'] for r in full['all_joint_eight_point_lifts']],
                'independent complete II initial relation differs')
        compared_initial += 1
    for kind in ('I', 'II'):
        own = [{'sigma': r['literal_B6'], 'all_lifts': r['all_inner_lifts'][kind]}
               for r in root['B6_complete_relations']['all_31_complete_fibres']]
        other = next(r['all_proper_sigma_fibres'] for r in geometry['short_patch_complete_fibres']
                     if r['kind'] == kind)
        require(own == other, 'independent all-B6 relation including zeros differs')
    require([len(r['surviving_types_after_same_initial_E_gate']) for r in six['ordinary_C14_cases']]
            == [4, 4, 2, 4, 4, 2], 'six-degree residual changed')
    private = [r for r in double['partition_summaries']
               if r['identity'] in ('44459:U=U:V=V', '44466:U=U:V=V')]
    require([len(r['final_necessary_survivors']) for r in private] == [4, 4, 3, 4, 4, 3],
            'double-five residual changed')
    narrow = double['original_alias_source_subcase_excluded']
    require(narrow['target'] == 44466 and narrow['U'] == 'w'
            and narrow['all_original_02_columns'] == [220297, 220299], 'alias source scope changed')
    require(geometry['source_exclusions'] == ['typeII_targetB_U_equals_original_w'],
            'geometry claimed an additional source exclusion')
    require(not geometry['whole_L_excluded'] and not six['ordinary_Type_I_excluded']
            and not double['all_typeII_sources_excluded'] and not root['source_realized'],
            'a necessary relation was promoted to source closure')
    names = ['certificate.json.gz', 'six_degree/certificate-v2.json.gz',
             'double_five/certificate.json.gz', 'geometry/runs/normal.json']
    print(json.dumps({'result': 'PASS', 'independent_initial_relation_comparisons': compared_initial,
                      'independent_B6_rows_including_zeros': 62,
                      'ordinary_I_residual_per_target': [4, 4, 2],
                      'ordinary_II_residual_per_target': [4, 4, 3],
                      'source_exclusions': root['source_conditional_exclusions'],
                      'L_entirely_excluded': False,
                      'complete_relation_input_sha256': {p: sha256((HERE / p).read_bytes()).hexdigest()
                                                         for p in names}}, sort_keys=True))


if __name__ == '__main__':
    main()
