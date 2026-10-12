#!/usr/bin/env python3
"""Replay this isolated package, retaining corruptions and all command outputs.

Results and logs use exclusive creation. Existing certificates are read only.
Run --output verification-v2.json to retain a later replay separately.
"""
import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=PACKAGE / 'verification.json')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit('refusing to overwrite verification output')
    logdir = PACKAGE / 'logs' / output.stem
    logdir.mkdir(exist_ok=False)
    checker = PACKAGE / 'controls/check_w5.py'
    certificate = PACKAGE / 'controls/certificate.json.gz'
    independent = PACKAGE / 'review/independent_check.py'
    tracked = [p for p in PACKAGE.rglob('*') if p.is_file()
               and 'logs' not in p.relative_to(PACKAGE).parts
               and '__pycache__' not in p.parts]
    before = {str(p.relative_to(PACKAGE)): digest(p) for p in tracked}
    results = []

    def run(name, argv, expected=0, cwd=ROOT, seed=None):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        if seed is not None:
            env['PYTHONHASHSEED'] = str(seed)
        proc = subprocess.run(argv, cwd=cwd, env=env, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = logdir / (name + '.log')
        with log.open('x') as f:
            f.write(proc.stdout)
        result = {'name': name, 'argv': list(map(str, argv)), 'cwd': str(cwd),
                  'seed': seed, 'exit_code': proc.returncode,
                  'expected_exit_code': expected,
                  'matched_expected': proc.returncode == expected,
                  'log': str(log.relative_to(PACKAGE))}
        results.append(result)
        return result

    python = sys.executable
    run('normal', [python, '-B', str(checker), '--check'])
    run('seed17-other-cwd', [python, '-B', str(checker), '--check', '--seed', '17'],
        cwd=Path('/tmp'), seed=17)
    run('independent', [python, '-B', str(independent), '--check',
                       str(PACKAGE / 'review/independent_results.json'),
                       '--primary', str(certificate)])

    with gzip.open(certificate, 'rt') as f:
        original = json.load(f)
    mutations = {}
    value = copy.deepcopy(original)
    row = value['graphs'][0]['rows'][0]
    index = next(i for i, cell in enumerate(row['cells']) if not cell)
    del row['cells'][index]
    mutations['missing-empty-cell'] = (value, f'delete graph0 row0 empty cell {index}')
    value = copy.deepcopy(original)
    del value['graphs'][0]['rows'][-1]
    mutations['missing-row'] = (value, 'delete graph0 final outer row')
    value = copy.deepcopy(original)
    cell = next(cell for cell in value['graphs'][0]['rows'][0]['cells'] if cell)
    cell[0][0] = (cell[0][0] + 1) % 4
    mutations['wrong-full-lift'] = (value, 'change B0 color in first nonempty full H lift')
    value = copy.deepcopy(original)
    value['U'][0], value['U'][1] = value['U'][1], value['U'][0]
    mutations['wrong-named-pins'] = (value, 'swap original U0 and U1 labels')
    value = copy.deepcopy(original)
    value['graphs'][0]['quotients'][0]['map'][0][1] = 1
    mutations['wrong-pullback-map'] = (value, 'map original B0 to B1 in quotient0')
    value = copy.deepcopy(original)
    value['graphs'][0]['rows'][0]['g_lifts'][0][-1] = 0
    mutations['wrong-center-lift'] = (value, 'set first prism G center color to 0')
    recipes = {}
    for name, (value, recipe) in mutations.items():
        path = logdir / (name + '.json.gz')
        payload = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
        with path.open('xb') as f:
            f.write(gzip.compress(payload, mtime=0))
        recipes[name] = recipe
        run(name, [python, '-B', str(checker), '--check', '--certificate', str(path)],
            expected=1)
    run('exclusive-create', [python, '-B', str(checker), '--write'], expected=1)
    run('docs', [python, 'scripts/check_docs.py'])
    run('formal-docgraph', [python, 'tools/docgraph', '--include', 'docs/**/*.md', 'check'])
    # Existing historical frozen copies declare repeated IDs. Report this
    # failure explicitly instead of treating the formal-docs PASS as global.
    run('whole-tree-docgraph', [python, 'tools/docgraph', 'check'], expected=1)
    run('git-diff-check', ['git', 'diff', '--check'])

    inputs = json.loads((PACKAGE / 'INPUTS.json').read_text())
    frozen_drift, live_drift = [], []
    for item in inputs['inputs']:
        for prefix, drift in [(PACKAGE / 'frozen', frozen_drift), (ROOT, live_drift)]:
            path = prefix / item['path']
            if not path.exists() or digest(path) != item['sha256']:
                drift.append(item['path'])
    evidence_drift = [name for name, old in before.items()
                      if not (PACKAGE / name).exists() or digest(PACKAGE / name) != old]
    report = {
        'base': inputs['base'], 'commands': results,
        'all_expected_results': all(r['matched_expected'] for r in results),
        'whole_tree_docgraph_status': 'FAIL: retained historical duplicate IDs; inspect log',
        'negative_recipes': recipes, 'frozen_input_drift': frozen_drift,
        'live_input_drift': live_drift, 'read_only_evidence_drift': evidence_drift,
        'evidence_sha256_before': before,
        'scope': 'This is a bounded named-relation audit, not a general reducibility proof.',
    }
    with output.open('x') as f:
        json.dump(report, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write('\n')
    ok = report['all_expected_results'] and not frozen_drift and not evidence_drift
    print(json.dumps({'expected_checks_match': ok, 'commands': len(results),
                      'frozen_drift': len(frozen_drift), 'live_drift': len(live_drift),
                      'evidence_drift': len(evidence_drift),
                      'whole_tree_docgraph': 'FAIL', 'output': str(output)}))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
