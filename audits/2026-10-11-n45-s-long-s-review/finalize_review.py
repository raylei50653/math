#!/usr/bin/env python3
"""Freeze the root's independent acceptance and correction addendum only."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'


def load(name):
    return json.loads((HERE / name).read_bytes())


def write(name, data):
    with (HERE / name).open('xb') as stream:
        stream.write((json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode())


def main():
    checks = load('checks.json')
    assert checks['checks_pass'] and checks['live_input_union_count'] == 112
    for name in ['independent-custody', 'independent-domain']:
        run = load('logs/' + name + '.command.json')
        assert run['exit'] == 0 and run['expected_exit_observed']
        assert not (HERE / run['stderr']).read_bytes()
    custody = load('logs/independent-custody.stdout.log')
    domain = load('logs/independent-domain.stdout.log')
    assert domain['schedule_counts'] == {'raw': 28, 'restoration_excluded': 4, 'remaining': 24}
    assert domain['query_counts'] == {'no initial necessary-table match': 12, 'T4 excluded': 4,
                                     'subsequent source excluded': 10, 'final retained necessary query': 4}
    spec = importlib.util.spec_from_file_location('review_snapshot', HERE / 'replay.py')
    capture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(capture)
    current = capture.snapshot()
    before = load('custody-before.json')
    assert current == before
    write('final-review-checks.json', {'base': BASE, 'checks_pass': True,
                                     'all_original_trees_and_112_live_inputs_unchanged': current == before,
                                     'head': current['head'], 'tracked_diff': current['tracked_diff'],
                                     'independent_native_commands': ['independent-custody', 'independent-domain']})

    profiles = sorted((t, m, n) for t in range(6) for m in range(2, 6) for n in range(1, 6)
                      if t + m + n == 5)
    assert profiles == [(0, 2, 3), (0, 3, 2), (0, 4, 1), (1, 2, 2), (1, 3, 1), (2, 2, 1)]
    write('coverage.json', {'contract': 'K1-K12; original U owner=s; X=G-e itself same-beta minimal',
                           'derivation': 'm_s>=2; n_U>=1; t_s>=0; m_s+n_U+t_s=5',
                           'profiles': [{'t_s': t, 'm_s': m, 'n_U': n,
                                         'status': 'A paper excluded' if (t, m, n) not in [(1, 2, 2), (2, 2, 1)]
                                         else 'B partial paper exclusion; pair22 restoration OPEN'}
                                        for t, m, n in profiles],
                           'source_realizability_claimed': False})
    write('remaining-schedules.json', {'base': BASE, 'scope': 'necessary schedules, not source realizations',
                                     'counts': domain['schedule_counts'],
                                     'raw_schedules': domain['schedules'],
                                     'remaining_schedules': [s for s in domain['schedules'] if not s['restoration_excluded']],
                                     'excluded_schedules': [s for s in domain['schedules'] if s['restoration_excluded']]})
    corrected_queries = [q for q in domain['queries'] if q['beta_q'] == 1
                         and (q['original_s_spoke'], q['F_C_beta']) in [(0, [2]), (2, [0])]]
    assert len(corrected_queries) == 2
    assert all(q['BASE_record_ids'] == [60] and q['T4_retained'] == [60]
               and q['classification'] == 'subsequent source excluded' for q in corrected_queries)
    corrections = [
        {'id': 'B-QUERY-PARTITION', 'artifact': '../2026-10-11-n45-s-long-s-fibre/REPORT.md',
         'location': 'section 6, lines 238-241', 'original_partition': [14, 4, 8, 4],
         'accepted_partition': [12, 4, 10, 4],
         'order': ['no initial match', 'T4 excluded', 'subsequent source excluded', 'final retained'],
         'misclassified_queries': corrected_queries,
         'mathematical_necessary_domain_changed': False},
        {'id': 'B-RESIDUAL-DEPENDENCY', 'artifact': '../2026-10-11-n45-s-long-s-fibre/claims.json',
         'claim_id': 'SF-RESIDUAL', 'field': 'premises',
         'add_required_claim': 'SF-T2-Q0-Q1-RESTORED',
         'reason': 'the four restored-edge schedule exclusions require this proved lemma',
         'paper_proof_missing': False},
    ]
    write('corrections.json', {'base': BASE, 'application': 'review addendum only; original files unchanged',
                             'original_B_pins': before['authority_artifacts']['B']['artifacts'],
                             'findings': corrections, 'review': 'fibre-paper-review.md'})

    a_claims = json.loads((capture.TARGETS['A'] / 'claims.json').read_bytes())['claims']
    b_claims = json.loads((capture.TARGETS['B'] / 'claims.json').read_bytes())['claims']
    assert len(a_claims) == 12 and len(b_claims) == 15
    special = {'SF-T1-MAP': 'accepted necessary domain with B-QUERY-PARTITION addendum; relative to BASE dependencies',
               'SF-T1-EXTEND': 'accepted relative to explicit frozen BASE paper/finite-terminal dependencies',
               'SF-T2-EXTEND': 'accepted relative to explicit frozen BASE paper/finite-terminal dependencies',
               'SF-RESIDUAL': 'accepted necessary domain with B-RESIDUAL-DEPENDENCY addendum; restoration remains OPEN',
               'SF-FINITE': 'accepted fixed finite interface calibration only'}
    c_root = REPO / 'audits/2026-10-11-n45-s-long-s-joint-review'
    c_judgment = json.loads((c_root / 'independent-judgment.json').read_bytes())
    assert c_judgment['verdict'] == 'accepted_fixed_finite_calibration'
    assert json.loads((c_root / 'checks.json').read_bytes())['checks_pass']
    assert all((HERE / name).is_file() for name in ['REPORT.md', 'direct-paper-review.md',
                                                 'fibre-paper-review.md', 'custody-review.md'])
    acceptance = {
        'task_id': 'N45-S-LONG-S-REVIEW', 'date': '2026-10-11', 'base': BASE,
        'verdict': 'accepted scoped paper and fixed finite calibration with independent review addendum',
        'authority_level': 'isolated independent audit adoption; shared research docs not updated',
        'reviewed_deliveries': before['authority_artifacts'], 'blocking_findings': [],
        'corrective_findings': [c['id'] for c in corrections], 'corrections': 'corrections.json',
        'A': {'verdict': 'accepted four scoped arbitrary-size paper exclusions',
              'claims': [{'id': c['id'], 'judgment': 'accepted under K1-K12'} for c in a_claims],
              'excluded_profiles_t_s_m_s_n_U': [[0, 4, 1], [0, 3, 2], [0, 2, 3], [1, 3, 1]],
              'pair_and_singleton_all_contract_splits': True, 'review': 'direct-paper-review.md'},
        'B': {'verdict': 'accepted scoped claims with correction addendum and explicit inherited dependencies',
              'claims': [{'id': c['id'], 'judgment': special.get(c['id'], 'accepted under K1-K12')} for c in b_claims],
              'limited_source_exclusions': ['singleton S', 'pair original r-splits (1,3)/(3,1)',
                                            't_s=2,beta=q0,q1 in same-frame Q(G)'],
              'query_partition': [12, 4, 10, 4], 'schedule_counts': domain['schedule_counts'],
              'q0_q1_supplement': 'pure paper existence plus complete fixed-r2/s3 fibre bijection; all q1 lifts restore rb4',
              'open_residual': 'pair22 t_s1/2 full original r-fibre restoration on Delta',
              'review': 'fibre-paper-review.md', 'remaining_domain': 'remaining-schedules.json'},
        'C': {'verdict': c_judgment['verdict'],
              'review': '../2026-10-11-n45-s-long-s-joint-review/REPORT.md',
              'judgment_pin': capture.file_pin(c_root / 'independent-judgment.json'),
              'review_delivery_pin': capture.file_pin(c_root / 'delivery.json'),
              'finite_domain': {'graphs': 19, 'omissions': 21, 'rows': 210, 'ordered_pins': 3360}},
        'native_verification': {'A_B_checks': 'checks.json', 'final_custody': 'final-review-checks.json',
                                'A_B_independent_custody': custody,
                                'independent_domain_command': 'logs/independent-domain.command.json',
                                'C_complete_independent_lifts': '../2026-10-11-n45-s-long-s-joint-review/independent-judgment.json'},
        'trust_dependencies': ['original complete K1-K12 source premises', 'explicit frozen BASE paper conclusions',
                               'external pinned Gallai degree-list theorem, independently read; no new Lean',
                               'unreplayed inherited finite terminal chains where explicitly stated'],
        'missing_BASE_artifact_replays': {'status': 'not triggered', 'executed': False,
                                         'paths': [r['missing_artifact']['path'] for r in custody['results']]},
        'target_finite_source': {'status': 'not triggered', 'established': False, 'executed': False, 'trigger_count': None},
        'not_established': ['whole U-owner-s exclusion', 'source realizability', 'new Lean', 'general N45/N2/E', 'epsilon>=3 main theorem'],
        'scope_boundaries': {'original_outputs_modified': False, 'shared_files_modified': False,
                             'old_certificates_modified': False, 'commit_push_PR': False},
    }
    write('acceptance.json', acceptance)
    print(json.dumps({'verdict': acceptance['verdict'], 'A_claims': 12, 'B_claims': 15,
                      'schedule_counts': domain['schedule_counts'], 'original_custody_changed': False}, sort_keys=True))


if __name__ == '__main__':
    main()
