#!/usr/bin/env python3
"""Create exact metadata once; execute normal, seed17 and a genuine inventory negative."""
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(name, data):
    with (HERE/name).open('x') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def run(name, seed=False, stdin=None):
    command = ['python3', '-B', str(HERE/'verify.py')]
    if stdin is not None:
        command.append('--manifest-stdin')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    env.pop('PYTHONHASHSEED', None)
    if seed:
        env['PYTHONHASHSEED'] = '17'
    start = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    p = subprocess.run(command, cwd=ROOT, env=env, input=stdin, capture_output=True)
    return {'name': name, 'command': command, 'cwd': str(ROOT),
            'environment': {'PYTHONDONTWRITEBYTECODE':'1', 'GIT_OPTIONAL_LOCKS':'0', 'PYTHONHASHSEED':'17' if seed else 'unset'},
            'start_UTC': start, 'elapsed_seconds': round(time.monotonic()-clock,3),
            'exit_code': p.returncode, 'stdout': p.stdout.decode(), 'stderr': p.stderr.decode(),
            'stdout_sha256': sha(p.stdout), 'stderr_sha256': sha(p.stderr),
            'stdin': stdin.decode() if stdin is not None else None,
            'stdin_sha256': sha(stdin) if stdin is not None else None}


def main():
    spec = importlib.util.spec_from_file_location('parent_verify', HERE/'verify.py')
    verify = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verify)
    manifest = {'audit_id': verify.AUDIT, 'exact_top_level_metadata_exclusions': sorted(verify.META),
                'payload': verify.inventory(HERE, verify.META)}
    write('manifest.json', manifest)
    normal = run('normal')
    seed = run('seed17', seed=True)
    negative = copy.deepcopy(manifest)
    omitted = 'frozen/audits/2026-10-10-n45-s-high2/receipt.json'
    del negative['payload'][omitted]
    negative_run = run('negative-nested-omission', stdin=(json.dumps(negative, ensure_ascii=False, indent=2)+'\n').encode())
    receipt = {'audit_id': verify.AUDIT, 'manifest_sha256': sha((HERE/'manifest.json').read_bytes()),
               'verifier_sha256': sha((HERE/'verify.py').read_bytes()),
               'negative_omitted_payload': omitted, 'executions':[normal,seed,negative_run]}
    # Save actual failures as well; never synthesize a successful result.
    write('receipt.json', receipt)
    assert normal['exit_code'] == seed['exit_code'] == 0, (normal, seed)
    assert normal['stdout'] == seed['stdout'] and normal['stderr'] == seed['stderr']
    assert negative_run['exit_code'] == 2 and 'immutable payload inventory' in negative_run['stderr']
    write('delivery.json', {'audit_id':verify.AUDIT, 'authority':'parent scoped adoption',
                            'manifest_sha256':receipt['manifest_sha256'],
                            'receipt_sha256':sha((HERE/'receipt.json').read_bytes()),
                            'verifier_sha256':receipt['verifier_sha256'],
                            'payload_files':len(manifest['payload']),
                            'original_workers_regular':206, 'independent_reviewers_regular':522,
                            'complete_named_trees_unchanged':True,
                            'shared_documents_changed':5, 'history_added':1,
                            'entrypoints':['REPORT.md','acceptance.json','verify.py'],
                            'new_finite_source':False,'new_Lean':False,'whole_worktree_custody':'not claimed',
                            'stop':'L2; remaining S long and broader cases OPEN; no commit/push'})
    print(json.dumps({'payload_files':len(manifest['payload']), 'normal':normal['exit_code'],
                      'seed17':seed['exit_code'],'negative':negative_run['exit_code'],
                      'identical_stdout':True},sort_keys=True))


if __name__ == '__main__':
    main()
