#!/usr/bin/env python3
"""Verify immutable M4-R evidence and reproduce its docs failure from Git archive."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile
import zipfile

FINAL = '1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf'
MAIN = '2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090'
SYNTHETIC = 'ca65f8796c6d83296fee2b22a77467d46b37ebec'
TARGETS = ['audits/2026-10-04-task-d5/c4/scope_ledger.json',
           'audits/2026-10-04-task-d2/integration_doc_changes.diff']


def meta(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def load(path):
    return json.loads(path.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--live', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo, live, output = args.repo.resolve(), args.live.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    bundle = repo / 'audits/2026-10-07-m4-remote'
    inventory = load(bundle / 'OUTPUT_INVENTORY.json')
    assert inventory['accepted_head'] == FINAL
    assert inventory['file_count'] == len(inventory['files']) == 341
    for entry in inventory['files']:
        assert meta((bundle / entry['path']).read_bytes()) == {k: entry[k] for k in ('bytes', 'sha256')}, entry['path']
    assert {p.relative_to(bundle).as_posix() for p in bundle.rglob('*') if p.is_file()} == {
        e['path'] for e in inventory['files']} | {'OUTPUT_INVENTORY.json'}
    original_logs = 0
    for command in load(bundle / 'commands.json'):
        folder = bundle / 'commands' / command['label']
        assert load(folder / 'command.json') == command
        for log in command['logs'].values():
            assert meta((folder / log['path']).read_bytes()) == {k: log[k] for k in ('bytes', 'sha256')}
            original_logs += 1

    ci = []
    for run_id, sha in [(37592725527, FINAL), (37592797376, SYNTHETIC), (37592841563, FINAL)]:
        folder = bundle / 'ci' / str(run_id)
        ledger = load(folder / 'log-evidence.json')
        assert meta((folder / 'original-logs.zip').read_bytes()) == {k: ledger['original_zip'][k] for k in ('bytes', 'sha256')}
        with zipfile.ZipFile(folder / 'original-logs.zip') as z:
            assert z.testzip() is None
            assert set(z.namelist()) == {e['path'] for e in ledger['entries']}
            for entry in ledger['entries']:
                assert meta(z.read(entry['path'])) == {k: entry[k] for k in ('bytes', 'sha256')}
            for entry in ledger['actual_checkout_evidence']:
                lines = z.read(entry['path']).decode('utf-8-sig').splitlines()
                assert 'git log -1 --format=%H' in lines[entry['command_line'] - 1]
                assert re.search(r'\b' + sha + r'\b', lines[entry['sha_line'] - 1])
                assert entry['sha'] == sha
            assert ledger['checkout_shas'] == [sha]
            if run_id != 37592841563:
                raw = z.read('build/5_Build.txt').decode('utf-8-sig')
                assert 'lake build --no-ansi' in raw and 'Build completed successfully (8831 jobs).' in raw
            else:
                raw = z.read('check/3_Check local documentation.txt').decode('utf-8-sig')
                assert 'FAIL: 2 errors (573 Markdown files, 6714 local links)' in raw
                assert all(target.rsplit('/', 1)[1] in raw for target in TARGETS)
        ci.append({'run_id': run_id, 'checkout_sha_verified_from_original_zip': sha,
                   'original_zip': ledger['original_zip']})

    state = load(live / 'state.json')
    pr = state['pr']
    assert pr['headRefOid'] == state['remote_refs']['integrate-kprime-e3'] == FINAL
    assert pr['baseRefOid'] == state['remote_refs']['main'] == MAIN
    assert state['local_refs'] == [FINAL, FINAL, MAIN]
    assert pr['state'] == 'OPEN' and not pr['isDraft']
    assert pr['mergeable'] == 'MERGEABLE' and pr['mergeStateStatus'] == 'CLEAN'
    assert not pr['autoMergeRequest'] and not state['tracked_status']
    assert not pr['reviews']['totalCount'] and not pr['reviewThreads']['totalCount']
    assert not state['main_protection'] and not state['effective_rules']
    assert state['synthetic_merge']['parents'] == [MAIN, FINAL]
    head_tree = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', FINAL + '^{tree}']).decode().strip()
    assert state['synthetic_merge']['tree'] == head_tree
    for key, run in state['runs'].items():
        assert run['head_sha'] == FINAL and run['status'] == 'completed'
        assert run['conclusion'] == ('failure' if key == '37592841563' else 'success')

    commands = []
    def run(name, argv, cwd, expected):
        proc = subprocess.run(argv, cwd=cwd, capture_output=True)
        logs = []
        for stream in ('stdout', 'stderr'):
            raw = getattr(proc, stream)
            path = name + '.' + stream + '.log.gz'
            (output / path).write_bytes(gzip.compress(raw, mtime=0))
            logs.append({'path': path, 'raw': meta(raw)})
        commands.append({'name': name, 'argv': argv, 'cwd': str(cwd), 'exit_code': proc.returncode,
                         'expected_exit': expected, 'logs': logs})
        (output / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        assert proc.returncode == expected, (name, proc.stdout, proc.stderr)
        return proc

    # Full immutable Git tree without any untracked/materialized evidence.
    checkout = Path(tempfile.mkdtemp(prefix='math-m4r-docs-supervisor-'))
    proc = subprocess.Popen(['git', '-C', str(repo), 'archive', '--format=tar', FINAL], stdout=subprocess.PIPE)
    with tarfile.open(fileobj=proc.stdout, mode='r|') as tar:
        tar.extractall(checkout, filter='data')
    assert proc.wait() == 0
    assert not (checkout / 'scratch').exists()
    assert not any((checkout / p).exists() for p in TARGETS)
    before = run('docs-before-restore', ['python3', 'scripts/check_docs.py'], checkout, 1)
    errors = [line for line in before.stdout.decode().splitlines() if line.startswith('missing path:')]
    assert len(errors) == 2 and all(any(target.rsplit('/', 1)[1] in e for e in errors) for target in TARGETS)
    assert b'FAIL: 2 errors (573 Markdown files, 6714 local links)' in before.stdout
    catalog = load(checkout / 'audits/ARCHIVE.json')
    # The catalog format is validated against the returned diagnosis entries.
    diagnosis = load(bundle / 'docs-diagnosis/diagnosis.json')
    assert diagnosis['accepted_final_sha'] == FINAL and len(diagnosis['paths']) == 2
    restored = []
    for entry in diagnosis['paths']:
        path = entry['path']
        assert path in TARGETS
        expected = entry['catalog']
        # Find the exact original path in the committed catalog without guessing its layout.
        def find(value):
            if isinstance(value, dict):
                if path in value:
                    yield value[path]
                if value.get('path') == path:
                    yield value
                for child in value.values():
                    yield from find(child)
            elif isinstance(value, list):
                for child in value:
                    yield from find(child)
        matches = list(find(catalog))
        assert any(all(item.get(k) == expected[k] for k in ('bytes', 'sha256')) for item in matches)
        compressed = (checkout / entry['blob']['path']).read_bytes()
        assert meta(compressed) == {k: entry['blob'][k] for k in ('bytes', 'sha256')}
        raw = gzip.decompress(compressed)
        assert meta(raw) == {k: expected[k] for k in ('bytes', 'sha256')}
        dest = checkout / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        restored.append({'path': path, **meta(raw), 'committed_gzip': entry['blob']['path']})
    after = run('docs-after-two-target-restore', ['python3', 'scripts/check_docs.py'], checkout, 0)
    assert b'OK: 573 Markdown files, 6714 local links; anchors, index, handoff checked' in after.stdout
    run('docgraph-after-restore', ['python3', 'tools/docgraph', 'check'], checkout, 0)
    run('seal', ['python3', 'audits/2026-10-07-m4-local/seal.py', '--repo', str(repo), '--check'], repo, 0)
    assert not subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain', '--untracked-files=no']).strip()
    result = {'status': 'M4-R accepted under existing local-documentation evidence option',
              'exact_head': FINAL, 'base': MAIN, 'main_advanced': False,
              'remote_package_entries_verified': 341, 'remote_command_raw_logs_verified': original_logs,
              'ci_original_zip_evidence': ci, 'synthetic_merge_tree_equals_head_tree': True,
              'clean_git_archive_checkout': str(checkout), 'docs_before_restore_exit': 1,
              'docs_after_only_two_target_restore_exit': 0, 'restored_targets': restored,
              'docgraph_exit': 0, 'seal_exit': 0, 'remote_docs_ci_conclusion': 'FAIL retained',
              'documentation_gate_basis': 'M4_REMOTE.md item 4 explicitly allows exact-head local docs evidence',
              'ready_under_agreed_merge_gates': True, 'merge_authorized': False, 'merge_performed': False,
              'next_step': 'separate explicit merge authorization and last-minute exact-head/base/CI refresh',
              'follow_up_debt': 'docs.yml archive restoration step; no fix or new commit in this review'}
    (output / 'review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
