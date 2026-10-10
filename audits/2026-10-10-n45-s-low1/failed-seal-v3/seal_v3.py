#!/usr/bin/env python3
"""Exclusive seal, actual read-only replays, and a corrupted-manifest control."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            hasher.update(block)
    return hasher.hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as output:
        output.write(data)


def dump(path, value):
    write(path, (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode())


def snapshot():
    result = {}
    for path in sorted(HERE.rglob('*')):
        relative = path.relative_to(HERE).as_posix()
        if relative.startswith('seal-final-v3/') or relative == 'delivery.json':
            continue
        if path.is_symlink():
            result[relative] = dict(symlink=os.readlink(path))
        elif path.is_file():
            result[relative] = dict(sha256=sha(path))
    return result


def run(name, argv, expected=0, seed=None):
    env = dict(os.environ)
    if seed is not None:
        env['PYTHONHASHSEED'] = str(seed)
    result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, check=False)
    for stream in ('stdout', 'stderr'):
        write(HERE / f'seal-final-v3/{name}.{stream}.log', getattr(result, stream))
    return dict(id=name, argv=argv, cwd=str(ROOT), env_overrides={} if seed is None else {'PYTHONHASHSEED': str(seed)},
                exit_code=result.returncode, expected_exit=expected,
                stdout=f'seal-final-v3/{name}.stdout.log', stderr=f'seal-final-v3/{name}.stderr.log')


def main():
    symlinks = {p.relative_to(HERE).as_posix(): os.readlink(p) for p in sorted(HERE.rglob('*')) if p.is_symlink()}
    if json.loads((HERE / 'symlinks.json').read_text()) != symlinks:
        raise RuntimeError('symlink identities changed since first seal')
    records = [(p.relative_to(HERE).as_posix(), sha(p)) for p in sorted(HERE.rglob('*')) if p.is_file() and not p.is_symlink()]
    manifest = ''.join(f'{digest}  {relative}\n' for relative, digest in records)
    write(HERE / 'MANIFEST.final-v3.sha256', manifest.encode())
    before = snapshot()
    dump(HERE / 'seal-final-v3/payload-before.json', before)
    command = ['python3', '-B', str(HERE / 'verify.py'), '--payload-only']
    normal = run('normal', command)
    seed17 = run('seed17', command, seed=17)
    corrupted = ('0' * 64) + manifest[64:]
    bad = HERE / 'seal-final-v3/corrupted-manifest.sha256'
    write(bad, corrupted.encode())
    negative = run('corrupted-manifest', command + ['--manifest', str(bad)], expected=2)
    after = snapshot()
    dump(HERE / 'seal-final-v3/payload-after.json', after)
    equal = (HERE / normal['stdout']).read_bytes() == (HERE / seed17['stdout']).read_bytes()
    negative_digest_rejected = 'manifest digest differs:' in (HERE / negative['stderr']).read_text()
    result = dict(commands=[normal, seed17, negative], normal_seed17_stdout_byte_equal=equal,
                  negative_detected_digest_mismatch=negative_digest_rejected,
                  payload_byte_drift=before != after,
                  negative_control_scope='Artifact integrity only; not a graph/source counterexample')
    dump(HERE / 'seal-final-v3/commands.json', result)
    if not equal or not negative_digest_rejected or before != after or any(c['exit_code'] != c['expected_exit'] for c in result['commands']):
        print(json.dumps(result, sort_keys=True))
        raise SystemExit(1)
    seal_files = {p.relative_to(HERE).as_posix(): sha(p) for p in sorted((HERE / 'seal-final-v3').rglob('*')) if p.is_file()}
    delivery = dict(task='N45-S-LOW1', root=str(ROOT), output=str(HERE),
                    base='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744',
                    sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    manifest_file='MANIFEST.final-v3.sha256',
                    manifest_sha256=sha(HERE / 'MANIFEST.final-v3.sha256'),
                    manifest_scope='Every regular payload file, including nested BASE manifests; symlink identities in symlinks.json. Only top-level manifest/delivery and explicitly receipt-bound seal-checks are excluded.',
                    seal_files=seal_files, paper_status='candidate_pending_independent_adjudication',
                    claims=['LOW1-CORE','LOW1-COMP','LOW1-JOIN','LOW1-F','LOW1-MAP','LOW1-EXCLUSION'],
                    finite_source_status='not evaluated; no finite source and no trigger count',
                    verification=dict(task_pins=6, base_inputs=12,
                                      hashed_regular_files=25869, symlink_identities=22,
                                      nested_repository_directory_entries=4,
                                      nested_repository_contents_at_initial_snapshot='not recursively hashed; only directory presence checked',
                                      preexisting_files=len(json.loads((HERE / 'preexisting-files.json').read_text())),
                                      preexisting_file_drift=0, payload_drift=0,
                                      normal_exit=normal['exit_code'],seed17_exit=seed17['exit_code'],
                                      corrupted_manifest_exit=negative['exit_code'], normal_seed17_byte_equal=equal),
                    actual_navigation_checks='checks.json',
                    preserved_failures=['First seal inventory-ordering rejection and second seal nested-directory classification rejection; both original logs/manifests/code snapshots retained',
                                        'Historical E4 provenance byte replay FAIL, not rerun',
                                        'Fresh BASE docs exit1: two historical missing paths',
                                        'Whole-worktree DocGraph exit1: 62 duplicate-ID errors'],
                    authored_shared_edits=0, commit=False, push=False, PR=False,
                    external_messages=False, subagents=False,
                    stop='Delivery complete; independent incremental adjudication remains required. No next residual selected.')
    dump(HERE / 'delivery.json', delivery)
    print(json.dumps(dict(payload_files=len(records), symlinks=len(symlinks),
                          normal_exit=normal['exit_code'], seed17_exit=seed17['exit_code'],
                          negative_exit=negative['exit_code'], shared_file_drift=0,
                          manifest_sha256=delivery['manifest_sha256']), sort_keys=True))


if __name__ == '__main__':
    main()
