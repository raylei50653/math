#!/usr/bin/env python3
"""Read-only integration of independently checked C8-STRUCT certificates."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
OLD = HERE / 'frozen/audits/2026-10-13-c8-joint-count-3097ef5'
BASE = '243a125a80e4d8de40957f59d8da0bdbc974cf69'
EXPECTED = {
    ('c15', 933): 134, ('c18', 933): 134,
    ('c04', 941): 193, ('c07', 941): 193,
    ('c15', 941): 171, ('c18', 941): 175,
    ('c20', 941): 171, ('c30', 941): 175,
}
EXCLUDED = {('c16', 941), ('c32', 941)}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check_inputs(manifest_path):
    frozen = json.loads(manifest_path.read_text())
    require(frozen['base'] == frozen['start_head'] == BASE, 'BASE mismatch')
    require(len(frozen['inputs']) == 58, 'missing BASE input')
    inputs = frozen['inputs'] + json.loads((HERE / 'DERIVED_INPUTS.json').read_text())['inputs']
    require(len({e['path'] for e in inputs}) == len(inputs), 'duplicate input')
    for entry in inputs:
        data = (HERE / 'frozen' / entry['path']).read_bytes()
        require(len(data) == entry['bytes'], 'input length drift: ' + entry['path'])
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'input hash drift: ' + entry['path'])
    old_manifest = json.loads((OLD / 'MANIFEST.json').read_text())
    interface_entry = next(e for e in old_manifest['audit_files'] if e['path'] == 'interface.json')
    require(inputs[-1]['sha256'] == interface_entry['sha256'], 'unanchored generated interface')
    return len(inputs)


def run(relative):
    result = subprocess.run([sys.executable, '-B', str(HERE / relative)],
                            text=True, capture_output=True)
    require(result.returncode == 0, relative + '\n' + result.stdout + result.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-manifest', type=Path, default=HERE / 'BASE.json')
    args = parser.parse_args()
    count = check_inputs(args.base_manifest)
    checks = ['geometry/check_geometry.py', 'classification/checker.py',
              'classification/quotient_checker.py', 'kempe/checker.py']
    for checker in checks:
        run(checker)

    # Independent integration: count-stage success is NOT final source success.
    old = json.loads((OLD / 'counts/certificate.v2.json').read_text())
    interface = json.loads((OLD / 'interface.json').read_text())
    cases = {c['id']: c for c in interface['cases']}
    old_queries = {(q['case_id'], q['target']): q for q in old['queries']
                   if q['status'] == 'necessary_condition_residual'}
    new = json.loads((HERE / 'kempe/certificate.json').read_text())
    queries = {(q['case_id'], q['target']): q for q in new['queries']}
    require(set(queries) == set(old_queries) == set(EXPECTED) | EXCLUDED,
            'ten-query whitelist mismatch')
    for key in EXCLUDED:
        boundary = cases[key[0]]['boundary_order']
        a, b = boundary.index('a1'), boundary.index('a4')
        equal = [i for i, word in enumerate(old['pattern_order']) if word[a] == word[b]]
        require(len(equal) == 74, 'incomplete equality fibre')
        upper = old_queries[key]['final_upper_mask']
        require(not any(upper >> i & 1 for i in equal), 'equality fibre not empty in upper')
    results = []
    for key, size in sorted(EXPECTED.items()):
        q = queries[key]
        x = list(map(Fraction, q['counts']))
        require(sum(v > 0 for v in x) == size, 'residual support mismatch')
        # The 91 columns are exactly the proper NC identifications; every one
        # must admit a positive complete boundary extension after chordlessness.
        positive = [sum(x[i] * row[j] for i, row in enumerate(old['equality_rows']))
                    for j in range(91)]
        require(all(v > 0 for v in positive), 'cofacial nonemptiness violated')
        results.append({'query': f'{key[0]}-{key[1]}', 'support': size,
                        'status': 'necessary-condition residual',
                        'cofacial_conditions': 91})
    print(json.dumps({'status': 'PASS', 'frozen_inputs': count,
                      'source_queries_excluded': 2,
                      'excluded': ['c16-941', 'c32-941'],
                      'source_queries_residual': 8,
                      'total_C8_excluded': 62, 'total_C8_queries': 70,
                      'bounds': {'h': 3, 'n5': 9},
                      'residuals': results, 'independent_checkers': checks}, sort_keys=True))


if __name__ == '__main__':
    main()
