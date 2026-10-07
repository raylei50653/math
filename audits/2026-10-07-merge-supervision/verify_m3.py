#!/usr/bin/env python3
"""Verify M3 delivery and close only the two named provenance diagnostics.

Writes new supervisory evidence to an exclusive fresh output directory.
Candidate source, historical artifacts, and M2/M3 delivery bytes stay intact.
This verifies delivered Lean logs; it does not rerun Lean or the broad search.
"""
import argparse
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import time

CANDIDATE = 'ba0b447f09617591d9f2ba81c988f537af771791'
MAIN_BASE = '2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090'
PARENT = 'a1ca89db9c04c6e65ba0b1cb0928df9e8c163e42'


def metadata(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def differences(left, right, path=''):
    if type(left) is not type(right):
        return [{'path': path, 'saved': left, 'current': right}]
    if isinstance(left, dict):
        assert left.keys() == right.keys(), ('changed key set', path)
        return [item for key in sorted(left)
                for item in differences(left[key], right[key], path + '/' + key)]
    if isinstance(left, list):
        assert len(left) == len(right), ('changed list length', path)
        return [item for i, (a, b) in enumerate(zip(left, right))
                for item in differences(a, b, path + '/' + str(i))]
    return [] if left == right else [{'path': path, 'saved': left, 'current': right}]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    bundle = repo / 'audits/2026-10-07-m3-fresh-checkout'
    checks = []

    def git(*argv):
        return subprocess.check_output(['git', '-C', str(repo), *argv])

    def read(name):
        return json.loads((bundle / name).read_bytes())

    def write(name, obj):
        (output / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

    def execute(name, argv, expected_exit=0, extra_env=None):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        env.update(extra_env or {})
        started = time.monotonic()
        result = subprocess.run(argv, cwd=repo, env=env, capture_output=True)
        entry = {'name': name, 'argv': argv, 'cwd': str(repo),
                 'environment_overrides': {'PYTHONDONTWRITEBYTECODE': '1', **(extra_env or {})},
                 'exit_code': result.returncode, 'expected_exit': expected_exit,
                 'seconds': round(time.monotonic() - started, 6), 'logs': []}
        for stream in ('stdout', 'stderr'):
            raw = getattr(result, stream)
            filename = name + '.' + stream + '.log'
            (output / filename).write_bytes(raw)
            entry['logs'].append({'path': filename, **metadata(raw)})
        checks.append(entry)
        write('commands.json', checks)
        assert result.returncode == expected_exit, entry
        return result

    assert git('rev-parse', 'HEAD').decode().strip() == CANDIDATE
    assert git('rev-parse', CANDIDATE + '^').decode().strip() == PARENT
    assert git('merge-base', CANDIDATE, MAIN_BASE).decode().strip() == MAIN_BASE
    assert not git('diff', '--name-only', CANDIDATE).strip()
    manifest = read('BUNDLE_INVENTORY.json')
    assert manifest['candidate_sha'] == CANDIDATE
    assert manifest['file_count'] == len(manifest['files']) == 264
    assert manifest['file_bytes'] == sum(item['bytes'] for item in manifest['files'])
    for item in manifest['files']:
        assert metadata((bundle / item['path']).read_bytes()) == {
            key: item[key] for key in ('bytes', 'sha256')}, item['path']
    execute('m3-delivery-seal', ['python3', str(bundle / 'seal_bundle.py'), '--check'])

    command_records = list((bundle / 'commands').glob('*.json'))
    verified_logs = 0
    for path in command_records:
        record = json.loads(path.read_bytes())
        for item in record['logs']:
            assert metadata((bundle / item['path']).read_bytes()) == {
                key: item[key] for key in ('bytes', 'sha256')}, item['path']
            verified_logs += 1
    for record in read('setup.json')['commands']:
        assert metadata((bundle / record['log']).read_bytes())['sha256'] == record['sha256']
    validation = read('validation.json')
    names = validation['required_checks']['names']
    assert len(names) == 29
    commands_by_name = {c['name']: c for c in validation['commands']}
    assert [name for name in names if commands_by_name[name]['exit_code']] == ['c44-input-audit']
    for name in names:
        assert commands_by_name[name] == read('commands/' + name + '.json'), name

    before = json.loads(gzip.decompress((bundle / 'sources-before.json.gz').read_bytes()))
    after = json.loads(gzip.decompress((bundle / 'sources-after.json.gz').read_bytes()))
    assert before['entries'] == after['entries'] and before['entry_count'] == 7190
    assert not after['added'] and not after['removed'] and not after['changed'] and after['zero_drift']
    for item in read('fresh-compressions.json')['files']:
        compressed = (bundle / item['gzip_name']).read_bytes()
        raw = gzip.decompress(compressed)
        assert metadata(compressed) == {'bytes': item['gzip_bytes'], 'sha256': item['gzip_sha256']}
        assert metadata(raw) == {'bytes': item['raw_bytes'], 'sha256': item['raw_sha256']}

    # Check every tracked candidate source against the recorded fresh snapshot
    # without extracting or writing candidate files.
    archive = subprocess.Popen(['git', '-C', str(repo), 'archive', CANDIDATE], stdout=subprocess.PIPE)
    tracked_matches = 0
    with tarfile.open(fileobj=archive.stdout, mode='r|') as stream:
        for item in stream:
            if item.isdir():
                continue
            record = before['entries'][item.name]
            if item.issym():
                assert record == {'kind': 'symlink', 'target': item.linkname}, item.name
            else:
                assert item.isfile(), item.name
                raw = stream.extractfile(item).read()
                assert record['kind'] == 'file' and metadata(raw) == {
                    key: record[key] for key in ('bytes', 'sha256')}, item.name
            tracked_matches += 1
    assert archive.wait() == 0

    provenance = read('provenance-summary.json')
    comparisons = []
    for item in provenance['comparisons']:
        saved_raw = (repo / item['source']).read_bytes()
        fresh_raw = (bundle / item['fresh']).read_bytes()
        assert metadata(saved_raw) == item['source_inventory']
        assert metadata(fresh_raw) == item['fresh_inventory']
        delta = differences(json.loads(saved_raw), json.loads(fresh_raw))
        assert delta == item['differences'], item['name']
        assert {x['path'] for x in delta} == set(item['allowed_leaf_paths'])
        comparisons.append({'name': item['name'], 'strict_byte_status': 'FAIL',
                            'differences': delta, 'all_other_serialized_fields_equal': True})
    for item in provenance['e4c_control_inventory']:
        assert (repo / 'artifacts/c5_excess_two_e4c' / item['path']).read_bytes() == (
            bundle / 'provenance/e4c' / item['path']).read_bytes()
    assert len(provenance['e4c_control_inventory']) == 54

    # Recompute the two new findings using unchanged producer logic, in memory,
    # writing only fresh supervisory outputs. No historical producer main runs.
    sys.path.insert(0, str(repo / 'scripts'))

    def load(name):
        path = repo / 'scripts' / (name + '.py')
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    c44 = load('c5_excess_two_c44_input_audit')
    c44_raw = c44.encoded(c44.audit())
    (output / 'c44-recomputed.json').write_bytes(c44_raw)
    c44_saved = c44.OUTPUT.read_bytes()
    delta = differences(json.loads(c44_saved), json.loads(c44_raw))
    assert delta == [
        {'path': '/layers/6/es_source_hash_matches', 'saved': None, 'current': True},
        {'path': '/layers/6/es_source_present', 'saved': False, 'current': True}]
    diagnostic = read('c44-summary.json')['finding']['diagnostic']
    assert metadata(c44_raw) == {'bytes': diagnostic['computed_bytes'], 'sha256': diagnostic['computed_sha256']}
    assert metadata(c44_saved) == {'bytes': diagnostic['saved_bytes'], 'sha256': diagnostic['saved_sha256']}
    layer = json.loads(c44_raw)['layers'][6]
    assert metadata((repo / layer['es_source']).read_bytes())['sha256'] == layer['es_source_expected_sha256']
    c44_exception = {'id': 'M3-C44-INPUT-AUDIT-001', 'strict_byte_status': 'FAIL',
                     'differences': delta, 'all_other_serialized_fields_equal': True,
                     'source_expected_hash_verified': True,
                     'disposition': 'bounded presence metadata exception after exact archive restoration; retain original ledger and strict FAIL'}

    e5 = load('c5_excess_two_e5_branches')
    e5_raw = (json.dumps(e5.build(), sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
    (output / 'e5-branches-recomputed.json').write_bytes(e5_raw)
    assert e5_raw == (bundle / 'provenance/e5_branches.json').read_bytes()
    e5_comparison = next(c for c in comparisons if c['name'] == 'E5_branches')
    current_doc = 'docs/c5_excess_two_mixed_core_spokes.md'
    assert metadata((repo / current_doc).read_bytes())['sha256'] == e5_comparison['differences'][0]['current']
    e5_exception = {'id': 'M3-PROV-E5-BRANCHES', **e5_comparison,
                    'disposition': 'single named document hash exception; retain original branches artifact and strict FAIL; disclose separately from historical failures'}
    execute('c44-strict-preserved', ['python3', str(repo / 'scripts/c5_excess_two_c44_input_audit.py'), '--check'], 1)
    execute('e5-branches-strict-preserved', ['python3', str(repo / 'scripts/c5_excess_two_e5_branches.py'), '--check'], 1)

    execute('axioms-log-revalidation', [
        'python3', str(bundle / 'check_lean_axioms.py'), '--source',
        str(repo / 'Math/ExcessTwoCertificatesAudit.lean'), '--log',
        str(bundle / 'logs/lean-axioms.stdout.log'), '--output', str(output / 'axioms-revalidated.json')])
    assert json.loads((output / 'axioms-revalidated.json').read_bytes()) == read('lean-axioms-summary.json')
    for name in ('lean-build', 'lean-axioms'):
        assert commands_by_name[name]['exit_code'] == 0
    execute('m3-authoring-check-portable-environment', ['python3', str(bundle / 'check_bundle.py')],
            extra_env={'PYTHONPATH': str(repo / 'scripts')})
    historical = gzip.decompress((repo / 'artifacts/c5_integrate_branch_review/logs/branch_whitespace.log.gz').read_bytes())
    assert historical == (bundle / 'logs/provenance_branch_whitespace.stdout.log').read_bytes()
    assert read('whitespace-comparison.json')['current_count'] == 86

    # Preserve a new Git-derived M1 package inventory. This is not a recovered
    # historical M1 command log and must never be labelled as one.
    package = []
    for line in git('diff-tree', '--no-commit-id', '--name-status', '-r', CANDIDATE).decode().splitlines():
        change, path = line.split('\t', 1)
        raw = git('show', CANDIDATE + ':' + path)
        assert raw == (repo / path).read_bytes()
        package.append({'change': change, 'path': path, **metadata(raw)})
    assert len(package) == 17
    write('m1-package-reconstructed.json', {'candidate_sha': CANDIDATE, 'parent_sha': PARENT,
                                          'main_base_sha': MAIN_BASE, 'method': 'fresh reconstruction from immutable Git blobs; not original M1 logs', 'files': package})
    assert not git('diff', '--name-only', CANDIDATE).strip()
    for item in manifest['files']:
        assert metadata((bundle / item['path']).read_bytes()) == {
            key: item[key] for key in ('bytes', 'sha256')}, item['path']
    result = {'candidate_sha': CANDIDATE, 'main_base_sha': MAIN_BASE, 'parent_sha': PARENT,
              'm3_review': 'computational and Lean evidence verified; two provenance supplements closed with explicit strict FAIL exceptions',
              'required_checks_original': {'total': 29, 'pass': 28, 'fail': 1},
              'm3_delivery_files_verified': 264, 'command_records_verified': len(command_records),
              'raw_logs_verified': verified_logs, 'source_snapshot_entries': 7190,
              'source_snapshot_zero_drift': True, 'tracked_candidate_snapshot_matches': tracked_matches,
              'new_exceptions': [c44_exception, e5_exception], 'historical_provenance_comparisons': comparisons[:3],
              'axiom_declarations_verified': 558, 'positive_without_native': 179,
              'project_build_rerun_by_supervisor': False,
              'm3_candidate_and_original_delivery_changed': False, 'merge_ready': False,
              'm4_local_pending': ['formal bundle and disclosure integration',
                                   'recover original M1/supervisor temporary evidence if available; otherwise record unavailable and use fresh evidence without replacing history',
                                   'portable validation instructions with explicit repo/source/output arguments',
                                   'final commit and affected documentation checks'],
              'm4_remote_pending': ['publish branch and PR', 'exact final SHA Lean CI and remote refs checks']}
    write('review.json', result)
    print(json.dumps({k: result[k] for k in ('m3_review', 'm3_delivery_files_verified', 'raw_logs_verified',
                                            'tracked_candidate_snapshot_matches', 'axiom_declarations_verified', 'merge_ready')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
