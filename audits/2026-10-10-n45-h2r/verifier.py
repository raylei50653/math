#!/usr/bin/env python3
"""Read-only custody and fixed semantics, without adjudicating arbitrary-size proofs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
from semantic_checks import run, need

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / 'audits/2026-10-10-n45-high23-supervision'
EXCLUDE = {'manifest.json', 'delivery.json', 'receipt-normal.json',
           'receipt-seed17.json', 'receipt-negative.json'}


def hash_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def read(name):
    return json.loads((HERE / name).read_text())


def file_meta(path):
    s = path.lstat()
    return {'kind': 'regular' if stat.S_ISREG(s.st_mode) else 'other',
            'bytes': s.st_size, 'mode': stat.S_IMODE(s.st_mode),
            'sha256': hash_bytes(path.read_bytes())}


def check(negative):
    intake = read('frozen/dispatch/intake.json')
    worker = 'audits/2026-10-10-n45-s-high2'
    spec = intake['workers'][worker]
    for name, metadata in spec['fulltree'].items():
        for path in [ROOT / worker / name, PARENT / spec['frozen'] / name,
                     HERE / 'frozen/worker' / name]:
            need(file_meta(path) == metadata, 'H2R-FULLTREE-DRIFT:' + str(path))
    for base in [ROOT / worker, HERE / 'frozen/worker']:
        actual = {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()}
        need(actual == set(spec['fulltree']), 'H2R-FULLTREE-UNIVERSE')
    inputs = read('frozen/worker/inputs-final.json')
    for item in inputs['inputs']:
        need(hash_bytes((HERE / 'frozen/worker' / item['frozen']).read_bytes()) == item['sha256'],
             'H2R-FROZEN-SOURCE-INPUT')
        raw = (subprocess.run(['git', 'show', inputs['BASE'] + ':' + item['path']],
                              cwd=ROOT, capture_output=True, check=True).stdout
               if item['origin'] == 'BASE' else (ROOT / item['path']).read_bytes())
        need(hash_bytes(raw) == item['sha256'], 'H2R-LIVE-OR-BASE-INPUT:' + item['path'])
    for pin in inputs['pins']:
        need(hash_bytes((ROOT / pin['path']).read_bytes()) == pin['sha256'], 'H2R-CURRENT-PIN')
    need(len(inputs['inputs']) == 41 and len(inputs['pins']) == 8, 'H2R-INPUT-COUNT')
    for name in ['audit-contract.md', 'h2r-task.md', 'intake.json']:
        need((HERE / 'frozen/dispatch' / name).read_bytes() == (PARENT / name).read_bytes(),
             'H2R-DISPATCH-DRIFT')

    manifest = read('manifest.json')
    need(set(manifest['metadata_exclusions']) == EXCLUDE, 'H2R-MANIFEST-EXCLUSIONS')
    payload = {p.relative_to(HERE).as_posix(): file_meta(p) for p in HERE.rglob('*')
               if p.is_file() and p.relative_to(HERE).as_posix() not in EXCLUDE}
    need(payload == manifest['payload'], 'H2R-IMMUTABLE-PAYLOAD-DRIFT')
    judgment = read('independent-judgment.json')
    need(len(judgment['claims']) == 12, 'H2R-TWELVE-CLAIMS')
    gaps = [c['id'] for c in judgment['claims'] if c['raw_verdict'] == 'gap']
    need(gaps == ['H2-EXCLUSION'] and judgment['qualified_HIGH2_conclusion'] ==
         'holds with explicit qualification', 'H2R-RAW-FINDING-QUALIFICATION')
    need(judgment['finite_HIGH2_source'] ==
         {'established': False, 'executed': False, 'trigger_count': None}, 'H2R-SOURCE-CONFLATION')
    for claim in judgment['claims']:
        need(len(claim['hypotheses_used']) == 13 and claim['BASE_sections'] and
             claim['new_source_hypotheses'] == [], 'H2R-CLAIM-SCOPE-FIELDS')
    finding = read('findings.json')['findings'][0]
    need(finding['id'] == 'H2R-EXCLUSION-FOUR-COLOR-UNUSED' and
         finding['missing_query_premise'] == 'gamma uses exactly three colors on the complete boundary B',
         'H2R-FINDING-MISSING')

    source = read('frozen/worker/frozen/base/artifacts/c5_single_spoke_two_two/observations.json')
    records = {r['id']: r for r in source['records']}
    mappings = read('frozen/worker/control-summary.json')['mapping']
    rho = [3, 2, 1, 0, 4]
    for m in mappings:
        if m['record_id'] is not None:
            rec = records[m['record_id']]
            spoke = rho[m['s_spoke']] if m['whole_reflection'] else m['s_spoke']
            need(rec['spoke'] == spoke and rec['supports'] == m['C_then_U_supports'] and
                 rec['bans'] == m['C_then_U_bans'], 'H2R-BASE-RECORD-IDENTITY')
            need({tuple(tuple(x) for x in p['lifted_supports']) for p in rec['placements']} ==
                 {tuple(tuple(x) for x in p) for p in m['slit_order_placements']},
                 'H2R-BASE-PLACEMENT')
        else:
            need(not m['slit_order_placements'], 'H2R-SOURCE-EXCLUSION-PLACEMENT')
    need(len(mappings) == 8, 'H2R-MAPPING-COUNT')

    text = (HERE / 'REPORT.md').read_text()
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if '://' not in link:
            need((HERE / link.split('#')[0]).is_file(), 'H2R-AUTHORED-LOCAL-LINK:' + link)
    for name in ['REPORT.md', 'verifier.py', 'semantic_checks.py']:
        text = (HERE / name).read_text()
        need(text.endswith('\n') and all(x == x.rstrip() for x in text.splitlines()),
             'H2R-AUTHORED-WHITESPACE:' + name)
    semantic = run(read('proof-witness.json'), negative=negative)
    return {'ok': True, 'audit_id': 'N45-H2R', 'worker_fulltree_files': 118,
            'source_inputs': 41, 'current_pins': 8, 'source_input_drift': 0,
            'immutable_payload_files': len(payload), 'paper_proof_verified_by_code': False,
            'raw_claims_holds': 11, 'raw_claim_gap': ['H2-EXCLUSION'],
            'qualified_HIGH2_conclusion': 'holds with explicit qualification',
            'finite_HIGH2_source_trigger_count': None,
            'manifest_sha256': hash_bytes((HERE / 'manifest.json').read_bytes()),
            'fixed_semantics': semantic}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', required=True, action='store_true')
    parser.add_argument('--negative-control', action='store_true')
    args = parser.parse_args()
    try:
        result = check(args.negative_control)
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print(json.dumps({'ok': False, 'audit_id': 'N45-H2R', 'finding': str(e)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
