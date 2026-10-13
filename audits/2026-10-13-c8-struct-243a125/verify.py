#!/usr/bin/env python3
"""Record normal/seed17 integration, negative control and documentation checks."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    number = 1
    while (HERE / f'validation-{number:02d}').exists():
        number += 1
    dest = HERE / f'validation-{number:02d}'
    dest.mkdir()
    records = []

    def run(name, command, seed=None, expect=0):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        if seed is not None:
            env['PYTHONHASHSEED'] = str(seed)
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        (dest / (name + '.stdout')).write_text(result.stdout)
        (dest / (name + '.stderr')).write_text(result.stderr)
        records.append({'name': name, 'command': command, 'seed': seed,
                        'exit_code': result.returncode, 'expected_exit': expect,
                        'stdout': str((dest / (name + '.stdout')).relative_to(HERE)),
                        'stderr': str((dest / (name + '.stderr')).relative_to(HERE))})
        if expect is not None:
            assert result.returncode == expect, name + ': ' + result.stderr
        return result

    normal = run('check', [sys.executable, '-B', str(HERE / 'check.py')])
    seeded = run('check.seed17', [sys.executable, '-B', str(HERE / 'check.py')], 17)
    assert normal.stdout == seeded.stdout and normal.stderr == seeded.stderr
    with tempfile.TemporaryDirectory(prefix='c8-struct-negative-') as tmp:
        altered = json.loads((HERE / 'BASE.json').read_text())
        altered['inputs'][0]['sha256'] = '0' * 64
        path = Path(tmp) / 'BASE.bad.json'
        path.write_text(json.dumps(altered))
        run('negative-frozen-hash', [sys.executable, '-B', str(HERE / 'check.py'),
                                     '--base-manifest', str(path)], expect=1)

    run('docs-live', [sys.executable, 'scripts/check_docs.py'], expect=None)
    run('docgraph-formal', [sys.executable, 'tools/docgraph', '--include', 'docs/**/*.md', 'check'])
    run('docgraph-whole-tree', [sys.executable, 'tools/docgraph', 'check'], expect=None)
    run('diff-whitespace', ['git', 'diff', '--check'])

    spec = importlib.util.spec_from_file_location('c8_docs', ROOT / 'scripts/check_docs.py')
    docs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(docs)
    scoped = list(HERE.rglob('*.md'))
    scoped = [p for p in scoped if 'frozen' not in p.relative_to(HERE).parts]
    scoped += [ROOT / p for p in ('docs/STATUS.md', 'docs/c5_kempe_guide.md',
                                 'docs/c5_neartri_boundary_collar.md')]
    issues = []
    links_checked = 0
    for path in scoped:
        for line, target in docs.links(path.read_text()):
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            links_checked += 1
            pointed = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not pointed.exists():
                issues.append(f'{path.relative_to(ROOT)}:{line}: missing {target}')
            elif url.fragment and pointed.suffix == '.md':
                if unquote(url.fragment) not in docs.anchors(pointed.read_text()):
                    issues.append(f'{path.relative_to(ROOT)}:{line}: missing anchor {target}')
    own_issues = [e for e in issues if e.startswith(str(HERE.relative_to(ROOT)) + ':')
                  or e.startswith(str(HERE.relative_to(ROOT)) + '/')]
    # Direct docs can acquire unrelated edits from concurrent sessions. Record
    # every issue; only this audit's own new links are asserted here.
    assert not own_issues, own_issues
    data = {'schema': 'c8-struct-verification-v1', 'runs': records,
            'normal_seed17_byte_equal': True,
            'root_frozen_hash_negative': 'rejected',
            'summary': json.loads(normal.stdout),
            'scoped_markdown_files': len(scoped), 'scoped_links_checked': links_checked,
            'scoped_link_issues': issues,
            'audit_link_issues': own_issues,
            'subsystem_verification': ['classification/verification.json',
                                       'geometry/check.log', 'geometry/check.seed17.log',
                                       'geometry/negative_controls.log',
                                       'kempe/verification.json', 'kempe/discovery.replay.json']}
    with (dest / 'verification.json').open('x') as out:
        json.dump(data, out, indent=2)
        out.write('\n')
    print(json.dumps({'verification': str((dest / 'verification.json').relative_to(ROOT)),
                      'mathematical_status': 'PASS', 'documentation_runs': records[3:],
                      'scoped_link_issues': issues}, sort_keys=True))


if __name__ == '__main__':
    main()
