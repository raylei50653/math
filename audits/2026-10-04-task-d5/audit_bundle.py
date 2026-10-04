#!/usr/bin/env python3
"""Capture immutable D5 inputs and verify earlier files without rewriting them."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

PREFIX = 'audits/2026-10-04-task-d5'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write(path, data):
    assert not path.exists(), f'Preserve previous result: {path}'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True).strip()


def inventory(root):
    paths = {root / p for p in git(root, 'ls-files').splitlines()}
    for directory in ('docs', 'scripts', 'tools', 'artifacts', 'audits'):
        paths.update((root / directory).rglob('*'))
    return {str(p.relative_to(root)): {'sha256': digest(p), 'size': p.stat().st_size}
            for p in sorted(paths) if p.is_file()
            and not {'__pycache__', '.git', '.lake'} & set(p.parts)
            and p.suffix != '.pyc'
            and not str(p.relative_to(root)).startswith(PREFIX + '/')}


def capture(root, out):
    assert not (out / 'baseline.json').exists(), 'Never replace a captured baseline'
    before = inventory(root)
    inputs = [p for p in before if not p.startswith('audits/')]
    snapshot = out / '.snapshot'
    for rel in inputs:
        target = snapshot / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / rel, target)
        assert digest(target) == before[rel]['sha256']
    (out / 'snapshot').symlink_to('.snapshot', target_is_directory=True)
    after = inventory(root)
    changes = [p for p in before if before[p] != after.get(p)]
    versions = {'python': sys.version, 'python_executable': sys.executable,
                'platform': platform.platform(), 'packages': {}}
    for package in ('networkx', 'numpy', 'rustworkx'):
        try:
            versions['packages'][package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions['packages'][package] = 'not installed in this interpreter'
    for name, command in [('git', ['git', '--version']), ('lake', ['lake', '--version']),
                          ('lean', ['lean', '--version']), ('uv', ['uv', '--version'])]:
        proc = subprocess.run(command, cwd=root, capture_output=True, text=True)
        versions[name] = {'command': command, 'exit_code': proc.returncode,
                          'stdout': proc.stdout, 'stderr': proc.stderr}
    write(out / 'baseline.json', {
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'head': git(root, 'rev-parse', 'HEAD'),
        'tracking_head': git(root, 'rev-parse', 'origin/main'),
        'git_status': git(root, 'status', '--short'), 'files': before,
        'input_paths': inputs, 'changes_during_capture': changes,
        'returned_work': 'User explicitly confirms final A4/B4/C4 returned',
        'snapshot_policy': 'All live scripts/docs/tools/artifacts and tracked build inputs; historical audits preserved in place',
        'no_commit_push': True})
    write(out / 'environment_versions.json', versions)
    print(json.dumps({'baseline_files': len(before), 'frozen_inputs': len(inputs), 'changes': changes}))
    assert not changes


def verify(root, out, result):
    base = json.loads((out / 'baseline.json').read_text())
    current = inventory(root)
    changes = [{'path': p, 'before_sha256': v['sha256'],
                'after_sha256': current.get(p, {}).get('sha256')}
               for p, v in base['files'].items() if v != current.get(p)]
    frozen = [p for p in base['input_paths']
              if digest(out / 'snapshot' / p) != base['files'][p]['sha256']]
    protected = [r for r in changes if r['path'].startswith(
        ('scripts/', 'tools/', 'artifacts/', 'audits/', 'docs/history/'))]
    head, tracking = git(root, 'rev-parse', 'HEAD'), git(root, 'rev-parse', 'origin/main')
    passed = not frozen and not protected and head == base['head'] and tracking == base['tracking_head']
    write(result, {'all_checks_passed': passed, 'baseline_files': len(base['files']),
        'preserved_existing_files': len(base['files']) - len(changes),
        'frozen_input_count': len(base['input_paths']), 'changed_existing_files': changes,
        'protected_changes': protected, 'frozen_changes': frozen,
        'additions': sorted(set(current) - set(base['files'])),
        'head_before': base['head'], 'head_after': head,
        'tracking_before': base['tracking_head'], 'tracking_after': tracking,
        'no_commit_push': True, 'scope': 'Local refs and captured bytes; no remote fetch'})
    print(json.dumps({'passed': passed, 'document_changes': len(changes), 'protected_changes': len(protected)}))
    assert passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('capture', 'verify'))
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--result', type=Path)
    args = parser.parse_args()
    root = args.repo.resolve()
    out = root / PREFIX
    if args.action == 'capture':
        capture(root, out)
    else:
        assert args.result is not None
        verify(root, out, args.result.resolve())


if __name__ == '__main__':
    main()
