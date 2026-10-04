#!/usr/bin/env python3
"""Freeze returned A3/B3/C3 and preserve every earlier audit attempt."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

PREFIX = 'audits/2026-10-04-task-d4'
NEW = ('c5_excess_two_mixed_core_four_spoke_mixed12_01_01',
       'c5_excess_two_mixed_core_four_spoke_mixed22_long_face',
       'c5_mixed_p3_two_frame_ternary_unary')


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True).strip()


def inventory(root):
    paths = [root / 'README.md', root / '.gitignore', root / 'requirements.txt']
    for d in ('docs', 'scripts', 'tools', 'artifacts', 'audits'):
        paths += list((root / d).rglob('*'))
    return {str(p.relative_to(root)): {'sha256': digest(p), 'size': p.stat().st_size}
            for p in sorted(set(paths)) if p.is_file()
            and '__pycache__' not in p.parts and p.suffix != '.pyc'
            and not str(p.relative_to(root)).startswith(PREFIX + '/')}


def capture(root, out):
    assert not (out / 'baseline.json').exists(), 'Never replace a captured baseline'
    before = inventory(root)
    inputs = {'README.md', '.gitignore', 'requirements.txt', 'artifacts/MANIFEST.json'}
    for d in ('scripts', 'docs', 'tools'):
        inputs.update(p for p in before if p.startswith(d + '/'))
    pending = ['artifacts/' + name + '/observations.json' for name in NEW]
    seen = set()
    while pending:
        rel = pending.pop()
        if rel in seen:
            continue
        seen.add(rel)
        inputs.add(rel)
        obj = json.loads((root / rel).read_text())
        for key in ('input_sha256', 'inputs_sha256', 'scripts_sha256', 'source_sha256'):
            for dep in obj.get(key, {}):
                inputs.add(dep)
                if dep.startswith('artifacts/') and dep.endswith('.json'):
                    pending.append(dep)
    # Scope ledgers are replayed from complete predecessors, never their counts.
    inputs.update(p for p in before if p.startswith('artifacts/c5_mixed_p3_common_endpoint/'))
    for rel in sorted(inputs):
        dst = out / 'snapshot' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / rel, dst)
        assert digest(dst) == before[rel]['sha256']
    after = inventory(root)
    changes = [p for p in before if before[p] != after.get(p)]
    data = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
                head=git(root, 'rev-parse', 'HEAD'),
                tracking_head=git(root, 'rev-parse', 'origin/main'),
                git_status=git(root, 'status', '--short'), files=before,
                input_paths=sorted(inputs), changes_during_capture=changes,
                returned_work='User explicitly confirmed final A3/B3/C3 workspaces returned',
                no_commit_push=True)
    write(out / 'baseline.json', data)
    print(json.dumps(dict(files=len(before), frozen_inputs=len(inputs), changes=changes)))
    assert not changes


def verify(root, out, result):
    assert not result.exists(), 'Use a fresh result path'
    base = json.loads((out / 'baseline.json').read_text())
    current = inventory(root)
    changes = [dict(path=p, before_sha256=v['sha256'],
                    after_sha256=current.get(p, {}).get('sha256'))
               for p, v in base['files'].items() if v != current.get(p)]
    inputs = list(base['input_paths'])
    if (out / 'snapshot_supplement.json').exists():
        inputs += json.loads((out / 'snapshot_supplement.json').read_text())['input_paths']
    frozen = [p for p in inputs
              if digest(out / 'snapshot' / p) != base['files'][p]['sha256']]
    protected = [r for r in changes if r['path'].startswith(
        ('scripts/', 'tools/', 'artifacts/', 'audits/', 'docs/history/'))]
    head, tracking = git(root, 'rev-parse', 'HEAD'), git(root, 'rev-parse', 'origin/main')
    passed = not frozen and not protected and head == base['head'] and tracking == base['tracking_head']
    write(result, dict(all_checks_passed=passed, baseline_files=len(base['files']),
          frozen_input_count=len(inputs), changed_existing_files=changes,
          protected_changes=protected, frozen_changes=frozen,
          additions=sorted(set(current) - set(base['files'])),
          head_before=base['head'], head_after=head,
          tracking_before=base['tracking_head'], tracking_after=tracking,
          no_commit_push=True, scope='Fixed snapshot and prior bytes; local refs only, no remote fetch'))
    print(json.dumps(dict(passed=passed, changed_documents=len(changes), protected_changes=len(protected))))
    assert passed


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=('capture', 'verify'))
    p.add_argument('--repo', type=Path, default=Path('.'))
    p.add_argument('--output', type=Path)
    p.add_argument('--result', type=Path)
    a = p.parse_args()
    root = a.repo.resolve()
    out = (a.output or root / PREFIX).resolve()
    if a.action == 'capture':
        capture(root, out)
    else:
        assert a.result is not None
        verify(root, out, a.result.resolve())


if __name__ == '__main__':
    main()
