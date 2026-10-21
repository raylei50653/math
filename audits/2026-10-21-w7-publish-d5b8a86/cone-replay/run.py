#!/usr/bin/env python3
"""Publication read-only replay; all new outputs confined beside this file."""
from hashlib import sha256
from pathlib import Path
import json, os, subprocess, sys, time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONE = ROOT/'audits/2026-10-20-w7-count-cone-d5b8a86'
OPT = ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86'

def snapshot():
    result = []
    for directory in (CONE, OPT):
        for p in sorted(directory.rglob('*')):
            if p.is_file():
                raw = p.read_bytes()
                result.append({'path': str(p.relative_to(ROOT)), 'bytes': len(raw),
                               'sha256': sha256(raw).hexdigest()})
    return result

def main():
    started = time.monotonic()
    before = snapshot()
    (HERE/'input-directory-snapshot.json').write_text(json.dumps(before, indent=2)+'\n')
    commands = [
        ('complete-normal', [str(CONE/'check.py'), '--controls', '--orbits'], {}),
        ('complete-hash17', [str(CONE/'check.py'), '--controls', '--orbits'], {'PYTHONHASHSEED':'17'}),
        ('independent-normal', [str(CONE/'independent/check.py'), '--model-controls', '--malformed-controls'], {}),
        ('independent-seed17', [str(CONE/'independent/check.py'), '--model-controls', '--malformed-controls', '--seed', '17'], {'PYTHONHASHSEED':'17'}),
    ]
    results = []
    for name, args, environment in commands:
        command = [sys.executable, '-B', *args]
        t = time.monotonic()
        with (HERE/(name+'.stdout')).open('w') as out, (HERE/(name+'.stderr')).open('w') as err:
            run = subprocess.run(command, cwd=ROOT, env=dict(os.environ, **environment), stdout=out, stderr=err)
        rec = {'name': name, 'command': command, 'environment': environment,
               'exit_code': run.returncode, 'seconds': time.monotonic()-t}
        if run.returncode == 0:
            report = json.loads((HERE/(name+'.stdout')).read_text())
            if name.startswith('complete'):
                assert report['necessary_cone'] == 'OPEN' and report['exact_certificate'] is None
                assert report['source_excluded'] is False and report['source_realized'] is False
                rec['necessary_cone'] = 'OPEN'
                rec['sealed_outputs'] = report['sealed_outputs']
                rec['input_custody'] = report['input_custody']
                rec['model'] = report['model']
                rec['complete_orbit_generation'] = report['complete_orbit_generation']['status']
            else:
                assert report['status'] == 'PASS'
                rec['status'] = 'PASS'
                rec['model_control_count'] = len(report['model_controls'])
                rec['malformed_control_count'] = len(report['malformed_controls'])
        results.append(rec)
        print(json.dumps(rec), flush=True)
        if run.returncode != 0:
            break
    after = snapshot()
    unchanged = before == after
    assert unchanged, 'existing cone/opt directory bytes changed'
    report = {'status': 'PASS' if len(results) == len(commands) and all(r['exit_code'] == 0 for r in results) else 'FAIL',
              'necessary_cone': 'OPEN', 'exact_certificate': None,
              'source_excluded': False, 'source_realized': False,
              'existing_cone_and_opt_files_unchanged': unchanged,
              'existing_file_count': len(before),
              'existing_total_bytes': sum(r['bytes'] for r in before),
              'results': results, 'seconds': time.monotonic()-started}
    (HERE/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)
    return 0 if report['status'] == 'PASS' else 1

if __name__ == '__main__':
    sys.exit(main())
