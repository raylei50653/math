#!/usr/bin/env python3
"""Check report links, new text whitespace, and indexed outside-file custody."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent


def main():
    pre_seal = '--pre-seal' in sys.argv[1:]
    links_only = '--links-only' in sys.argv[1:]
    old = json.loads((OUT / 'custody-start.json').read_text())
    drift = []
    unhashed_directory_markers = []
    for e in old['files']:
        p = ROOT / e['path']
        if e['kind'] == 'regular':
            if not p.is_file() or p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest() != e['sha256']:
                drift.append(e['path'])
        elif e['kind'] == 'symlink':
            if not p.is_symlink() or os.readlink(p) != e['target']:
                drift.append(e['path'])
        elif e['path'].endswith('/'):
            # Preserve the original snapshot: these are Git directory markers,
            # not regular-file byte evidence. Report them separately.
            unhashed_directory_markers.append(e['path'])
            if not p.is_dir():
                drift.append(e['path'])
        elif p.exists() or p.is_symlink():
            drift.append(e['path'])
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    current = {p.decode() for p in subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], env=env).split(b'\0') if p}
    prefix = OUT.relative_to(ROOT).as_posix() + '/'
    oldpaths = {e['path'] for e in old['files']}
    new = sorted(p for p in current - oldpaths if not p.startswith(prefix))
    normalize = lambda s: '\n'.join(line for line in s.splitlines() if prefix.rstrip('/') not in line)
    start = normalize((OUT / 'git-status-start.txt').read_text())
    now = normalize(subprocess.check_output(['git', 'status', '--short', '--branch'], env=env, text=True))
    custody_failures = ['outside drift ' + p for p in drift] + ['outside new path ' + p for p in new]
    if start != now:
        custody_failures.append('outside Git status drift')
    failures = [] if links_only else list(custody_failures)
    report = OUT / 'REPORT.md'
    links = re.findall(r'\[[^\]]*\]\(([^)]+)\)', report.read_text())
    local = []
    deferred_metadata = []
    for url in links:
        if '://' in url or url.startswith('#'):
            continue
        path = url.split('#', 1)[0]
        if not (report.parent / path).exists():
            if pre_seal and path in {'manifest.json', 'delivery.json', 'receipt.json'}:
                deferred_metadata.append(path)
            else:
                failures.append('missing report link ' + url)
        local.append(url)
    textfiles = []
    for p in OUT.rglob('*'):
        if p.is_file() and p.suffix in ['.py', '.md', '.txt', '.json'] and 'frozen' not in p.relative_to(OUT).parts:
            textfiles.append(p.relative_to(OUT).as_posix())
            for n, line in enumerate(p.read_text().splitlines(), 1):
                if line.rstrip() != line or '\t' in line:
                    failures.append('whitespace ' + str(p.relative_to(OUT)) + ':' + str(n))
    result = {'outside_indexed_files': len(old['files']), 'outside_drift': drift,
              'outside_new_paths': new, 'outside_status_unchanged': start == now,
              'report_local_links': len(local), 'new_text_files_checked': len(textfiles),
              'deferred_metadata_links': deferred_metadata,
              'unhashed_directory_markers': unhashed_directory_markers,
              'custody_failures': custody_failures,
              'verification_mode': 'local links and whitespace only' if links_only else 'local and outside custody',
              'failures': failures, 'scope': 'indexed files; ignored files and .git not inventoried'}
    print(json.dumps(result, sort_keys=True))
    return bool(failures)


if __name__ == '__main__':
    sys.exit(main())
