#!/usr/bin/env python3
"""Read-only bounded literal/pin calibration; never an actual-source checker."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
ROWS = ['01012', '01021', '01023', '01201', '01202', '01203',
        '01212', '01213', '01231', '01232']
Q = ['01212', '01202', '01201', '01021', '01012']
SUPPORTS = {'U': [0, 1, 2], 'L': [2, 3, 4], 'S': [4, 0]}
SCHEDULES = [('933', '0123'), ('933', '0124'), ('933', '0234'),
             ('933', '1234'), ('941', '023'), ('941', '024'), ('941', '124')]


def verify_inputs():
    pins = json.loads((ROOT / 'inputs.json').read_text())
    for rec in pins['inputs']:
        data = (ROOT / rec['local_frozen_path']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == rec['sha256'], rec['path']
        if rec['authority'] == 'BASE Git blob':
            p = subprocess.run(['git', 'cat-file', 'blob', BASE + ':' + rec['path']],
                               cwd=ROOT, capture_output=True, check=True)
            assert p.stdout == data, rec['path']
    for rec in pins['external_theorem_pins']:
        assert hashlib.sha256((ROOT / rec['local_frozen_path']).read_bytes()).hexdigest() == rec['sha256']
    return len(pins['inputs'])


def expected():
    beta = tuple(map(int, Q[2]))
    queries = []
    for literal in ROWS:
        row = tuple(map(int, literal))
        for piece, support in SUPPORTS.items():
            before = [beta[i] for i in support]
            after = [row[i] for i in support]
            maps = [list(p) for p in itertools.permutations(range(4))
                    if [p[v] for v in before] == after]
            queries.append({'literal': literal, 'piece': piece, 'ordered_support': support,
                            'beta_query': before, 'query': after, 'colour_maps': maps})
    transports = []
    for q, lmap, smap in [(3, [2, 1, 0, 3], [0, 1, 2, 3]),
                         (4, [1, 2, 0, 3], [0, 2, 1, 3])]:
        row = tuple(map(int, Q[q]))
        for piece, p, seed in [('L', lmap, [2, 3]), ('S', smap, [0, 3])]:
            support = SUPPORTS[piece]
            assert [p[beta[i]] for i in support] == [row[i] for i in support]
            assert [p[v] for v in seed] == [0, 3]
        assert [row[i] for i in SUPPORTS['U']] == [0, 1, 0]
        assert [row[i] for i in [0, 2]] == [0, 0]
        assert row[4] != 0
        transports.append({'target_q': q, 'literal': Q[q], 'L_colour_map': lmap,
                           'S_colour_map': smap, 'L_beta_pins': [2, 3],
                           'S_beta_pins': [0, 3], 'target_pins': [0, 3],
                           'gamma_b4': row[4], 'restores_e': True})
    partitions = []
    col = set(range(4))
    for s_bad in itertools.combinations(range(4), 2):
        s_bad = set(s_bad)
        partitions.append({'S_beta_forbidden_r': sorted(s_bad),
                           'L_beta_forbidden_r': sorted(col - s_bad),
                           'satisfies_proved_S_r0_r1_nonempty': not bool(s_bad & {0, 1})})
    assert sum(p['satisfies_proved_S_r0_r1_nonempty'] for p in partitions) == 1
    schedules = []
    for orbit, mask in SCHEDULES:
        delta = [int(q) for q in mask if q != '2']
        restored = [q for q in [3, 4] if q in delta]
        assert restored
        cells = []
        for literal in ROWS:
            row = list(map(int, literal))
            cells.append({'literal': literal, 'gamma_b4': row[4],
                          'pins': [[a, b] for a in range(4) for b in range(4)]})
        schedules.append({'orbit': orbit, 'QG': list(map(int, mask)), 'delta': delta,
                          'original_s_spokes': [0, 2], 'proved_restoration_q': restored,
                          'selected_q': 4 if 4 in restored else 3,
                          'ambient_cells': cells})
    assert sum(len(c['pins']) for s in schedules for c in s['ambient_cells']) == 1120
    return {'task_id': 'N45-S-LONG-S-T2-Q2-RESTORE',
            'adoption_status': '待獨立驗收',
            'scope': 'bounded literal/pin algebra; no actual source relations or preimage counts',
            'base': BASE, 'queries': queries, 'proof_transports': transports,
            'beta_two_colour_partitions': partitions, 'schedules': schedules,
            'source_relation_values': None, 'source_preimage_counts': None,
            'target_source': {'executed': False, 'trigger_count': None, 'status': 'not triggered'}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--print-certificate', action='store_true')
    parser.add_argument('--certificate', type=Path, default=ROOT / 'calibration.json')
    args = parser.parse_args()
    assert args.check != args.print_certificate, 'choose exactly one operation'
    n = verify_inputs()
    result = expected()
    if args.print_certificate:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        delivered = json.loads(args.certificate.read_text())
        assert delivered == result, 'calibration certificate mismatch (literal map or complete ambient cells)'
        print(json.dumps({'status': 'triggered and holds', 'domain': 'literal/pin calibration only',
                          'frozen_dispatch_inputs': n, 'query_permutation_checks': 720,
                          'beta_partition_cases': 6, 'schedules': 7, 'ambient_pin_cells': 1120,
                          'target_source_executed': False, 'target_trigger_count': None}, sort_keys=True))


if __name__ == '__main__':
    main()
