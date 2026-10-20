"""Read-only integrated replay of the frozen existence research increment."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = 'f13eb4d0887d962021992ae7afe3323af4d79cd3'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seal', type=Path, default=HERE / 'OUTPUTS.json')
    args = ap.parse_args()
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    assert manifest['base'] == BASE
    routing = set(manifest['routing_drift_allowed'])
    assert routing == {'docs/STATUS.md', 'docs/c5_kempe_guide.md'}
    assert len({r['path'] for r in manifest['files']}) == len(manifest['files']) == 516
    for record in manifest['files']:
        rel = record['path']
        raw = (HERE / 'frozen' / rel).read_bytes()
        assert len(raw) == record['bytes'] and hashlib.sha256(raw).hexdigest() == record['sha256'], ('frozen drift', rel)
        if rel not in routing:
            assert (ROOT / rel).read_bytes() == raw, ('historical input drift', rel)
    seal = json.loads(args.seal.read_text())
    assert seal['base'] == BASE and seal['main_target'] == 'OPEN'
    assert seal['source_realized'] is False and seal['smaller_bad_constructed'] is False

    def verify_outputs():
        for rel, digest in seal['files'].items():
            assert hashlib.sha256((HERE / rel).read_bytes()).hexdigest() == digest, ('output seal drift', rel)

    verify_outputs()
    exploration = json.loads((HERE / 'D/summary.json').read_text())
    raw = gzip.decompress((HERE / 'D/exploration.json.gz').read_bytes())
    assert len(raw) == exploration['raw_bytes']
    assert hashlib.sha256(raw).hexdigest() == exploration['raw_sha256']
    assert exploration['status'] == 'exploration_only' and not exploration['source_exclusion_proved']
    scripts = ['A/research.py', 'B/check.py', 'C/check.py', 'C/compare.py',
               'C/acceptance.py', 'counts.py', 'review_lifts.py',
               'A/review_b.py', 'A/review_counts.py', 'B/review_c.py']

    def run(rel):
        result = subprocess.run([sys.executable, '-B', str(HERE / rel)],
                                cwd=ROOT, capture_output=True, text=True)
        assert result.returncode == 0, (rel, result.stdout, result.stderr)
        return {'checker': rel, 'exit_code': result.returncode,
                'stdout_sha256': hashlib.sha256(result.stdout.encode()).hexdigest()}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, scripts))
    verify_outputs()
    print(json.dumps({'pass': True, 'base': BASE, 'frozen_inputs': len(manifest['files']),
                      'frozen_drift': 0, 'output_drift': 0, 'checks': results,
                      'main_target': 'OPEN', 'source_realized': False,
                      'smaller_bad_constructed': False, 'new_Lean_theorem': False}, sort_keys=True))


if __name__ == '__main__':
    main()
