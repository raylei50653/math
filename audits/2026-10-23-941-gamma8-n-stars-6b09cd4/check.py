#!/usr/bin/env python3
"""Read-only complete same-graph original-star reconstruction; paper is PROOF.md."""
import argparse
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import random
from models import reconstruct, PREV

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'

def require(ok, why):
    if not ok:
        raise ValueError(why)

def custody():
    data = json.loads((HERE / 'INPUTS.json').read_text())
    require(data['base'] == BASE and len(data['inputs']) == 11, 'input domain/BASE changed')
    for row in data['inputs']:
        raw = (HERE / row['snapshot']).read_bytes()
        require((len(raw), sha256(raw).hexdigest()) == (row['bytes'], row['sha256']),
                'frozen authority changed: ' + row['path'])
        require(raw == (ROOT / row['path']).read_bytes(), 'live authority changed: ' + row['path'])
    return dict(immutable_inputs=11, immutable_drift=0)

def direct_N1_control():
    previous = json.loads((HERE / 'frozen' / PREV).read_text())
    row = next(r for r in previous['u_full_link_trials'] if r['omega_type'] == 'N1')
    cases = []
    for link in row['all_proper_complete_u_links']:
        require({'m', 'n', 'v', 'U'} <= set(link), 'N1 complete u-star premises changed')
        exits = set(link) & {'p_d', 'p_x'}
        require(exits, 'N1 complete u-star has no exit')
        for w in ['n', 'v']:
            omega = {'d', 'p_d', 'U', 'p_x', w}
            common = sorted(set(link) & omega)
            require(len(common) >= 3, 'N1 three original common neighbors lost')
            cases.append(dict(u_link=link, omega_N3_neighbor=w, common_original_neighbors=common))
    require(len(cases) == 12, 'N1 complete-star control domain')
    return cases

@lru_cache(None)
def expected():
    trace = reconstruct()
    contexts, partial, complete = trace['contexts'], trace['preomega'], trace['rows']
    require(len(contexts) == 946 and len(partial) == 331 and complete == [],
            'complete original-star domain mismatch')
    require(Counter(r['omega_type'] for r in partial) == {'N1': 130, 'N3': 201},
            'partial original-star ownership domain')
    stages = {kind: {stage: sum(r['stage_counts'][stage] for r in contexts
                              if r['omega_type'] == kind)
                     for stage in ['initial_valid', 'n', 'v', 'a', 'b', 'omega']}
              for kind in ['N1', 'N3']}
    require(stages == {'N1': dict(initial_valid=66, n=125, v=160, a=147, b=130, omega=0),
                       'N3': dict(initial_valid=286, n=284, v=223, a=210, b=201, omega=0)},
            'joint source-star reconstruction transcript changed')
    return dict(
        schema='941-gamma8-n-stars-v1', base=BASE,
        paper_domain=dict(j=2, resource_count=7, M2_nonempty=True, omega_types=['N1', 'N3'],
                          complete_M=['T', 'm'], degree_T=5, degree_m=5,
                          same_original_G_F=True, original_rotation=True, original_attachments=True,
                          ordered_B14=True, literal_phi_psi=True, complete_components=True,
                          arbitrary_Z_external_spectators=True,
                          all_empty_fibres_and_full_lifts_preserved=True),
        complete_star_contexts=contexts,
        relaxed_joint_preomega_rows=partial,
        complete_joint_rows=complete,
        direct_N1_three_original_common_neighbor_controls=direct_N1_control(),
        paper_N3_case_tree=dict(
            N1_contact_count=1, contact_choices=['a', 'b', 'u'],
            K02_path=['d', 'p_d', 'U', 'p_x', 'x'],
            d_equals_U='original_degree_at_most_four',
            omega_original_degree=5,
            u_contact='u_envelope_excludes_both_K0_endpoints',
            a_contact='v_complete_star_and_three_common_original_neighbors',
            b_contact=dict(n_full_link=['b', 'T', 'm', 'u', 'p_a'],
                           u_full_links=[['n', 'm', 'v', 'U', 'p_a'],
                                         ['n', 'm', 'v', 'p_b', 'U', 'p_a']],
                           u6='nonconsecutive_u_U_original_chord_in_v_link',
                           u5='complete_a_link_cannot_close_after_p_b'),
            whole_side_reflection=True),
        conclusion=dict(stage_counts=stages, partial_N1_rows=130, partial_N3_rows=201,
                        complete_joint_original_star_rows=0,
                        paper_source_domain_excluded='nonempty_M2_Z7_omega_N1_or_N3',
                        finite_table_is_only_calibration=True,
                        nonempty_Z_lower_bound_after_round5_K_exclusions=8,
                        nonempty_X_lower_bound_after_round5_K_exclusions=9,
                        K_external_tails_closed=False,
                        common_oriented_original_faces_preserved=True),
        preserved_complete_predecessor_certificate=json.loads((HERE / 'frozen' / PREV).read_text()),
        authority_boundaries=dict(finite_control='triggered and holds',
                                  full_source_catalogue_control='not triggered',
                                  source_realizability='not triggered', eleven_whole_type_exclusions=0,
                                  general_wrong_side='OPEN', common_k_lower_bound=23,
                                  new_Lean=False, new_LP=False, smaller_bad_constructed=False))

def validate(cert, seed=0):
    reference = expected()
    require(set(cert) == set(reference), 'certificate key domain changed')
    keys = list(reference)
    random.Random(seed).shuffle(keys)
    for key in keys:
        require(cert[key] == reference[key], 'certificate mismatch: ' + key)
    return dict(status='PASS', complete_star_contexts=946, relaxed_preomega_rows=331,
                N1_preomega_rows=130, N3_preomega_rows=201, complete_joint_rows=0,
                direct_N1_controls=12, predecessor_fibres_and_full_lifts_preserved=True,
                paper_domain='nonempty_M2_Z7_N1_N3_excluded', source_realizability='not triggered',
                eleven_whole_type_exclusions=0)

def negatives(cert):
    controls = [
        ('drop_joint_partial_star', lambda c: c['relaxed_joint_preomega_rows'].pop()),
        ('drop_complete_original_contact', lambda c: c['relaxed_joint_preomega_rows'][0]['full_links']['n'].pop()),
        ('drop_actual_original_face_edge', lambda c: c['relaxed_joint_preomega_rows'][0]['edges'].pop()),
        ('invent_complete_omega_star', lambda c: c['complete_joint_rows'].append({})),
        ('forget_d_U_alias', lambda c: c['paper_N3_case_tree'].update(d_equals_U='OPEN')),
        ('permit_two_N1_contacts', lambda c: c['paper_N3_case_tree'].update(N1_contact_count=2)),
        ('forget_u6_original_chord', lambda c: c['paper_N3_case_tree']['b_contact'].update(u6='OPEN')),
        ('close_K_external_tails', lambda c: c['conclusion'].update(K_external_tails_closed=True)),
        ('drop_empty_fibres', lambda c: c['paper_domain'].update(all_empty_fibres_and_full_lifts_preserved=False)),
        ('claim_source_realization', lambda c: c['authority_boundaries'].update(source_realizability='triggered and holds')),
        ('claim_whole_eleven_type_exclusion', lambda c: c['authority_boundaries'].update(eleven_whole_type_exclusions=11)),
        ('raise_common_k', lambda c: c['authority_boundaries'].update(common_k_lower_bound=24)),
    ]
    rejected = []
    for name, mutate in controls:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            validate(bad)
        except (ValueError, KeyError, TypeError):
            rejected.append(name)
        else:
            raise ValueError('negative accepted: ' + name)
    return dict(negative_controls_rejected=rejected, count=len(rejected))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--negative', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    cert = json.loads(args.certificate.read_text())
    out = dict(custody=custody(), validation=validate(cert, args.seed))
    if args.negative:
        out['negative'] = negatives(cert)
    print(json.dumps(out, sort_keys=True))

if __name__ == '__main__':
    main()
