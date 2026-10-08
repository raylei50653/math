#!/usr/bin/env python3
"""Read-only review of M4 delivery and its final receipt; archive new evidence only."""
import argparse
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

FINAL = '1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf'
CANDIDATE = 'ba0b447f09617591d9f2ba81c988f537af771791'
MAIN = '2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090'
M4 = 'audits/2026-10-07-m4-local'
RAW_LOG = 'audits/2026-10-07-m3-fresh-checkout/logs/provenance_branch_whitespace.stdout.log'
ALLOWED = {
    'C44_input': {'/layers/6/es_source_present', '/layers/6/es_source_hash_matches'},
    'E4_reductions': {'/sources/artifacts/c5_excess_two_e3/REPORT.md/bytes',
                      '/sources/artifacts/c5_excess_two_e3/REPORT.md/sha256'},
    'E5_controls': {'/source_sha256/artifacts/c5_excess_two_e3/REPORT.md'},
    'E4C': {'/source_hashes/docs/c5_kempe_guide.md'},
    'E5_branches': {'/sources_sha256/docs/c5_excess_two_mixed_core_spokes.md'},
}


def metadata(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def load(path):
    return json.loads(path.read_bytes())


def diff(a, b, path=''):
    if type(a) is not type(b):
        return [{'path': path, 'saved': a, 'current': b}]
    if isinstance(a, dict):
        assert a.keys() == b.keys(), path
        return [d for k in sorted(a) for d in diff(a[k], b[k], path + '/' + k)]
    if isinstance(a, list):
        assert len(a) == len(b), path
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in diff(x, y, path + '/' + str(i))]
    return [] if a == b else [{'path': path, 'saved': a, 'current': b}]


def diagnostics(raw):
    return [{'path': m[1], 'line': int(m[2]), 'message': m[3]}
            for line in raw.decode().splitlines()
            if (m := re.match(r'^(.+):(\d+): (.+)$', line))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo, receipt, output = args.repo.resolve(), args.receipt.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)

    def git(*argv):
        return subprocess.check_output(['git', '-C', str(repo), *argv])

    assert git('rev-parse', 'HEAD').decode().strip() == FINAL
    assert git('rev-parse', FINAL + '^').decode().strip() == CANDIDATE
    assert not git('status', '--porcelain', '--untracked-files=no').strip()
    delivery = load(repo / M4 / 'DELIVERY.json')
    entries = delivery['files']
    assert len(entries) == delivery['file_count'] == 572
    assert sum(e['bytes'] for e in entries) == delivery['file_bytes'] == 26350701
    for entry in entries:
        raw = (repo / entry['path']).read_bytes()
        assert metadata(raw) == {k: entry[k] for k in ('bytes', 'sha256')}, entry['path']
        assert git('show', FINAL + ':' + entry['path']) == raw, entry['path']
    seal_raw = (repo / M4 / 'DELIVERY.json').read_bytes()
    assert git('show', FINAL + ':' + M4 + '/DELIVERY.json') == seal_raw
    changed = git('diff', '--name-only', CANDIDATE, FINAL).decode().splitlines()
    assert set(changed) == {e['path'] for e in entries} | {M4 + '/DELIVERY.json'}
    assert len(changed) == 573
    assert sum(e['bytes'] for e in entries) + len(seal_raw) == 26469605
    original = load(repo / M4 / 'original-bundles.json')['files']
    assert len(original) == len({e['path'] for e in original}) == 328
    for entry in original:
        assert metadata((repo / entry['path']).read_bytes()) == {k: entry[k] for k in ('bytes', 'sha256')}

    inventory = load(receipt / 'OUTPUT_INVENTORY.json')
    assert inventory['verified_exact_final_sha'] == FINAL
    for entry in inventory['files']:
        assert metadata((receipt / entry['path']).read_bytes()) == {k: entry[k] for k in ('bytes', 'sha256')}
    assert {p.relative_to(receipt).as_posix() for p in receipt.rglob('*') if p.is_file()} == {
        e['path'] for e in inventory['files']} | {'OUTPUT_INVENTORY.json'}
    logs_count = 0
    for folder in (receipt, receipt / 'review'):
        for command in load(folder / 'commands.json'):
            assert command['exit_code'] == command.get('expected_exit', 0)
            for log in command['logs']:
                compressed = (folder / log['path']).read_bytes()
                assert metadata(compressed) == log['gzip']
                assert metadata(gzip.decompress(compressed)) == log['raw']
                logs_count += 1
    final_receipt = load(receipt / 'FINAL_RECEIPT.json')
    verification = load(receipt / 'review/verification.json')
    assert final_receipt['final_delivery_sha'] == verification['tested_checkout_sha'] == FINAL
    assert verification['tested_head_tree'] == git('rev-parse', FINAL + '^{tree}').decode().strip()
    assert final_receipt['seal'] == metadata(seal_raw)
    assert final_receipt['lean_build_rerun'] is False
    assert final_receipt['axiom_process_rerun'] is False
    assert final_receipt['merge_ready'] is False

    source = load(receipt / 'review/source-comparison.json')
    assert {e['path'] for e in source['byte_changes']} == {'docs/STATUS.md', 'docs/c5_kempe_guide.md'}
    lean = source['lean_source_config_generated_products']
    assert len(lean) == 109
    for entry in lean + source['byte_changes']:
        assert metadata((repo / entry['path']).read_bytes()) == entry['tested'], entry['path']
    assert all(e['m3'] == e['tested'] for e in lean)
    syntax = load(receipt / 'syntax.json')
    assert len(syntax['files']) == syntax['count'] == 17
    for entry in syntax['files']:
        raw = (repo / entry['path']).read_bytes()
        assert metadata(raw) == {k: entry[k] for k in ('bytes', 'sha256')}
        ast.parse(raw, filename=entry['path'])
    links = load(receipt / 'audit-links.json')
    assert len(links['passed']) == 63 and len(links['archival_unavailable']) == 6
    for entry in links['passed']:
        target = entry['destination'].split('#')[0]
        assert (repo / entry['path']).parent.joinpath(target).resolve().exists(), entry

    failures = load(receipt / 'review/strict-failures.json')['failures']
    assert {e['name'] for e in failures} == set(ALLOWED)
    for entry in failures:
        saved_raw = (repo / entry['saved_path']).read_bytes()
        fresh_raw = (receipt / 'review' / entry['fresh_path']).read_bytes()
        assert metadata(saved_raw) == entry['saved'] and metadata(fresh_raw) == entry['fresh']
        delta = diff(json.loads(saved_raw), json.loads(fresh_raw))
        assert delta == entry['differences']
        assert {d['path'] for d in delta} == ALLOWED[entry['name']]
        assert entry['strict_exit_code'] == 1 and entry['strict_status'] == 'FAIL'
    e4c = load(receipt / 'review/provenance/e4c/summary.json')
    assert e4c['source_hashes']['docs/c5_kempe_guide.md'] == metadata((repo / 'docs/c5_kempe_guide.md').read_bytes())['sha256']

    whitespace_commands = {}
    for name, base, expected in [('new', CANDIDATE, 85), ('branch', MAIN, 171)]:
        proc = subprocess.run(['git', '-C', str(repo), 'diff', '--check', base, FINAL], capture_output=True)
        assert proc.returncode == 2 and not proc.stderr
        (output / (name + '-whitespace.log.gz')).write_bytes(gzip.compress(proc.stdout, mtime=0))
        whitespace_commands[name] = diagnostics(proc.stdout)
        assert len(whitespace_commands[name]) == expected
    assert {e['path'] for e in whitespace_commands['new']} == {RAW_LOG}
    whitespace = load(receipt / 'review/whitespace.json')
    assert whitespace_commands['new'] == whitespace['new_imported_historical_log']['diagnostics']
    key = lambda e: (e['path'], e['line'], e['message'])
    assert sorted(whitespace_commands['branch'], key=key) == sorted(
        whitespace['historical']['diagnostics'] + whitespace_commands['new'], key=key)
    assert not whitespace['new_authored_diagnostics']
    assert (repo / RAW_LOG).read_bytes() == gzip.decompress(
        (repo / 'artifacts/c5_integrate_branch_review/logs/branch_whitespace.log.gz').read_bytes())
    axioms = load(receipt / 'review/axioms-reparsed.json')
    assert axioms == load(repo / 'audits/2026-10-07-m3-fresh-checkout/lean-axioms-summary.json')
    assert axioms['declaration_count'] == 558 and not axioms['sorryAx'] and not axioms['unexpected_axioms']
    assert axioms['log_sha256'] == metadata((repo / 'audits/2026-10-07-m3-fresh-checkout/logs/lean-axioms.stdout.log').read_bytes())['sha256']
    assert axioms['source_sha256'] == metadata((repo / 'Math/ExcessTwoCertificatesAudit.lean').read_bytes())['sha256']

    shutil.copytree(receipt, output / 'final-receipt')
    copied = output / 'final-receipt'
    for path in receipt.rglob('*'):
        if path.is_file():
            assert (copied / path.relative_to(receipt)).read_bytes() == path.read_bytes()
    result = {'status': 'ACCEPTED locally within named exceptions', 'exact_final_sha': FINAL,
              'parent': CANDIDATE, 'main_baseline': MAIN, 'committed_delivery_files': len(changed),
              'committed_delivery_bytes': 26469605, 'original_bundle_files_unchanged': 328,
              'receipt_files_without_inventory': len(inventory['files']), 'receipt_raw_logs_verified': logs_count,
              'lean_sources_config_products_unchanged': 109, 'syntax_parsed_files': 17,
              'strict_failures_preserved': 5, 'historical_whitespace': 86,
              'imported_log_whitespace': 85, 'new_authored_whitespace': 0,
              'axioms_reparsed': 558, 'lean_build_rerun': False, 'lean_axiom_process_rerun': False,
              'archived_receipt': 'final-receipt/FINAL_RECEIPT.json', 'merge_ready': False,
              'next_task': 'M4-R', 'remote_verified_in_this_review': False,
              'tracked_tree_clean': not git('status', '--porcelain', '--untracked-files=no').strip(),
              'candidate_diff_shortstat': git('diff', '--shortstat', CANDIDATE, FINAL).decode().strip(),
              'main_diff_shortstat': git('diff', '--shortstat', MAIN, FINAL).decode().strip()}
    (output / 'review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
