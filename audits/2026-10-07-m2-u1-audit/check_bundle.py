#!/usr/bin/env python3
"""Validate fresh M2 output syntax/links/whitespace, logs and frozen input bytes."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def record(raw):
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def main():
    before = json.loads((HERE / 'input-before.json').read_text())
    after = json.loads((HERE / 'input-after.json').read_text())
    assert before == after and len(before) == 32
    candidate = 'ba0b447f09617591d9f2ba81c988f537af771791'
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == candidate
    tracked, restored = 0, 0
    for rel, expected in before.items():
        raw = (ROOT / rel).read_bytes()
        assert record(raw) == expected, rel
        if rel == 'artifacts/c5_excess_two_mixed_omission/observations.json':
            manifest = json.loads((ROOT / 'artifacts/MANIFEST.json').read_text())['files'][rel]
            assert expected == {key: manifest[key] for key in ('bytes', 'sha256')}
            restored += 1
        else:
            assert subprocess.check_output(['git', 'show', candidate + ':' + rel], cwd=ROOT) == raw, rel
            tracked += 1
    a, b = [(HERE / name).read_bytes() for name in
            ('independent-default.json', 'independent-seed17.json')]
    assert a == b
    result = json.loads(a)
    assert result['candidate_sha'] == candidate
    assert result['independent_checker_sha256'] == record((HERE / 'verify.py').read_bytes())['sha256']
    assert result['classification'] == 'triggered and holds'
    assert result['target_intersection'] == [] and result['input_zero_byte_drift']
    assert sum(result['sigma_histogram'].values()) == 3498
    assert sum(result['double_triangle_sigma_histogram'].values()) == 1024
    assert len(result['per_form']) == 344
    assert (HERE / 'logs/run-controls-default.stdout.log').read_bytes() == (
        HERE / 'logs/run-controls-seed17.stdout.log').read_bytes()
    log_checks = 0
    for command in json.loads((HERE / 'commands.json').read_text()):
        # The initial new bundle checker misclassified no-index's ordinary
        # diff status 1. Preserve its failed log; it is not a mathematical run.
        assert command['exit_code'] == 0 or (
            command['label'] == 'fresh-bundle-check' and command['exit_code'] == 1), command['label']
        for stream in ('stdout', 'stderr'):
            r = command[stream]
            assert record((HERE / r['path']).read_bytes()) == {
                key: r[key] for key in ('bytes', 'sha256')}, r['path']
            log_checks += 1
    files = [p for p in sorted(HERE.rglob('*')) if p.is_file()
             and '__pycache__' not in p.parts and p.suffix != '.pyc']
    python_files, links = 0, 0
    for path in files:
        raw = path.read_bytes()
        if path.suffix == '.py':
            tree = ast.parse(raw, filename=str(path))
            if path.name in ('verify.py', 'run_controls.py'):
                names = {node.module.split('.')[0] for node in ast.walk(tree)
                         if isinstance(node, ast.ImportFrom) and node.module}
                names.update(alias.name.split('.')[0] for node in ast.walk(tree)
                             if isinstance(node, ast.Import) for alias in node.names)
                allowed = {'__future__', 'argparse', 'collections', 'copy', 'hashlib',
                           'itertools', 'json', 'pathlib', 'subprocess'}
                assert names <= allowed, names - allowed
            python_files += 1
        if path.suffix == '.md':
            text = re.sub(r'```.*?```', '', raw.decode(), flags=re.S)
            for destination in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in destination:
                    continue
                target = (path.parent / destination.split('#')[0]).resolve()
                # DELIVERY is written after validation so it covers the new
                # validation logs and updated command ledger without a cycle.
                if target == HERE / 'DELIVERY.json':
                    continue
                assert target.exists(), (path.name, destination)
                links += 1
        whitespace = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)],
                                    capture_output=True, text=True)
        assert whitespace.returncode in (0, 1) and not whitespace.stdout and not whitespace.stderr, (
            path.name, whitespace.stdout, whitespace.stderr)
    print(json.dumps(dict(candidate_sha=candidate, input_files=len(before),
        tracked_candidate_exact_byte_matches=tracked, restored_manifest_matches=restored,
        zero_input_byte_drift=True, mathematical_results_byte_identical=True,
        result_sha256=record(a)['sha256'], command_log_hashes_checked=log_checks,
        new_python_syntax_checked=python_files, new_markdown_local_links_checked=links,
        new_file_whitespace_checks=len(files), all_checks_passed=True), sort_keys=True))


if __name__ == '__main__':
    main()
