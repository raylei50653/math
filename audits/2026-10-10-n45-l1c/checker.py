#!/usr/bin/env python3
"""Independent frozen-artifact checker; neither imports worker code nor proves mathematics."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORKER = ROOT / 'audits/2026-10-10-n45-s-low1'
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
EXPECTED_MANIFEST = '7dba2b7df58370838b12c5184e590de4e46e00628db84a204d38db3e139e6292'
STAGE = 'initialization'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe(relative):
    p = Path(relative)
    require(not p.is_absolute() and '..' not in p.parts and p.as_posix() == relative,
            f'unsafe path: {relative}')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def verify(args):
    global STAGE
    STAGE = 'payload-inventory'
    regular, links = [], {}
    for path in WORKER.rglob('*'):
        relative = path.relative_to(WORKER).as_posix()
        if relative in {'MANIFEST.final-v4.sha256', 'delivery.json'} or relative.startswith('seal-final-v4/'):
            continue
        if path.is_symlink():
            links[relative] = os.readlink(path)
        elif path.is_file():
            regular.append(relative)
    regular.sort()
    require(len(regular) == 6049 and len(links) == 5, 'unexpected final-v4 inventory counts')
    records = {}
    for line in args.manifest.read_text().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, 'malformed manifest line')
        value, relative = match.groups()
        safe(relative)
        require(relative not in records, f'duplicate manifest path: {relative}')
        records[relative] = value
    require(sorted(records) == regular, 'manifest payload inventory differs')
    STAGE = 'symlink-identities'
    require(links == read(args.symlinks), 'payload symlink identities differ')
    STAGE = 'payload-digests'
    for relative, value in sorted(records.items()):
        require(digest(WORKER / relative) == value, f'manifest digest differs: {relative}')

    STAGE = 'receipt-inventory'
    receipt = read(args.receipt)
    require(receipt['manifest_file'] == 'MANIFEST.final-v4.sha256', 'receipt manifest filename differs')
    require(receipt['manifest_sha256'] == EXPECTED_MANIFEST == digest(WORKER / 'MANIFEST.final-v4.sha256'),
            'receipt original manifest binding differs')
    require(receipt['paper_status'] == 'candidate_pending_independent_adjudication', 'candidate status differs')
    metadata, metadata_links = [], []
    for path in (WORKER / 'seal-final-v4').rglob('*'):
        relative = path.relative_to(WORKER).as_posix()
        if path.is_symlink():
            metadata_links.append(relative)
        elif path.is_file():
            metadata.append(relative)
    require(not metadata_links, 'unexpected receipt symlink')
    require(len(metadata) == 10 and sorted(metadata) == sorted(receipt['seal_files']),
            'receipt exact metadata inventory differs')
    STAGE = 'receipt-digests'
    for relative, value in sorted(receipt['seal_files'].items()):
        safe(relative)
        require(relative.startswith('seal-final-v4/'), 'receipt metadata outside final-v4')
        require(digest(WORKER / relative) == value, f'receipt digest differs: {relative}')

    STAGE = 'recorded-replays'
    commands = read(WORKER / 'seal-final-v4/commands.json')
    cmd = {x['id']: x for x in commands['commands']}
    require(set(cmd) == {'normal', 'seed17', 'corrupted-manifest'}, 'worker final replay inventory differs')
    require(cmd['normal']['exit_code'] == cmd['seed17']['exit_code'] == 0, 'recorded final success exit differs')
    require(cmd['corrupted-manifest']['exit_code'] == 2, 'recorded final negative exit differs')
    normal = (WORKER / cmd['normal']['stdout']).read_bytes()
    seeded = (WORKER / cmd['seed17']['stdout']).read_bytes()
    require(normal == seeded, 'recorded final normal/seed17 bytes differ')
    require(cmd['seed17']['env_overrides'] == {'PYTHONHASHSEED': '17'}, 'seed17 environment differs')
    final_negative = (WORKER / cmd['corrupted-manifest']['stderr']).read_text()
    require(final_negative == 'integrity rejection: manifest digest differs: MANIFEST.final-v2.sha256\n',
            'final negative failed before digest stage')
    require(read(WORKER / 'seal-final-v4/payload-before.json') == read(WORKER / 'seal-final-v4/payload-after.json'),
            'recorded final payload drift')
    for item in [cmd['normal'], cmd['seed17']]:
        require((WORKER / item['stderr']).read_bytes() == b'', 'recorded success has stderr')
    decoded = json.loads(normal)
    require(decoded['regular_payload_files'] == 6049 and decoded['payload_symlinks'] == 5,
            'worker reported wrong inventory')
    require(decoded['receipt_checked'] is False, 'worker sealing runs were not payload-only')
    parent = read(HERE / 'frozen/parent-initial-strict-replays.json')['records']
    require(parent['normal']['exit_code'] == parent['seed17']['exit_code'] == 0,
            'parent initial strict replay exit differs')
    require(parent['normal']['output'] == parent['seed17']['output'], 'parent initial strict bytes differ')
    require(json.loads(parent['normal']['output'])['receipt_checked'] is True, 'parent initial receipt not checked')
    require(parent['corrupted']['exit_code'] == 2 and 'manifest digest differs:' in parent['corrupted']['output'],
            'parent initial negative failed before digest stage')

    STAGE = 'base-inputs'
    base_inputs = read(WORKER / 'base-inputs.json')
    require(base_inputs['base'] == BASE and len(base_inputs['inputs']) == 12, 'BASE input inventory differs')
    for item in base_inputs['inputs']:
        blob = git('show', f'{BASE}:{item["path"]}')
        require(hashlib.sha256(blob).hexdigest() == item['sha256'], f'BASE SHA256 differs: {item["path"]}')
        require(git('rev-parse', f'{BASE}:{item["path"]}').decode().strip() == item['git_blob'],
                f'BASE git blob differs: {item["path"]}')
        require((WORKER / 'base-source' / item['path']).read_bytes() == blob,
                f'BASE archive bytes differ: {item["path"]}')
    external = read(WORKER / 'external-source-check.json')
    require(digest(WORKER / 'external/gallai-official.pdf') == external['official_sha256'] == external['base_sha256'],
            'frozen official PDF bytes differ')

    STAGE = 'frozen-current-pins'
    initial = read(WORKER / 'inputs-initial.json')
    auditor = read(HERE / 'inputs.json')
    require(digest(WORKER / 'delivery.json') == auditor['worker_receipt_sha256'],
            'original worker receipt bytes changed')
    require(digest(HERE / 'frozen/parent-initial-strict-replays.json') == auditor['parent_initial_strict_replays_sha256'],
            'parent initial strict evidence binding differs')
    require(len(initial['pins']) == len(auditor['task_pins']) == 6, 'current pin inventory differs')
    require(initial['head'] == auditor['head'] == BASE, 'HEAD snapshot differs')
    for item, audit in zip(initial['pins'], auditor['task_pins']):
        require(item['path'] == audit['path'] and item['actual'] == item['expected'] == audit['expected'],
                'initial/current frozen task pin record differs')
        require(digest(WORKER / 'frozen/current' / item['path']) == item['expected'],
                f'frozen task pin bytes differ: {item["path"]}')
        require(audit['current_live_sha256_at_audit_start'] == item['expected'], 'audit-start live pin differed')

    STAGE = 'historical-failures'
    wanted = {
        'seal-checks': 'integrity rejection: manifest payload inventory differs\n',
        'seal-final-v2': 'integrity rejection: previously missing file appeared: audits/2026-10-09-n45-pc/source/\n',
        'seal-final-v3': 'integrity rejection: missing report link: 1_[color=3]−1_[color=2]\n',
    }
    for folder, expected_error in wanted.items():
        old = {x['id']: x for x in read(WORKER / folder / 'commands.json')['commands']}
        require(old['normal']['exit_code'] == old['seed17']['exit_code'] == 2, 'historical failure exit differs')
        require((WORKER / old['normal']['stderr']).read_text() == expected_error, 'historical rejection stage differs')
        require((WORKER / old['seed17']['stderr']).read_text() == expected_error, 'seeded historical stage differs')
        neg = (WORKER / old['corrupted-manifest']['stderr']).read_text()
        require(('manifest payload inventory differs' in neg) if folder == 'seal-checks' else ('manifest digest differs:' in neg),
                'historical negative stage differs')
    paper = (WORKER / 'REPORT.md').read_text().split('## 7.', 1)[0]
    for version in ['v1', 'v2', 'v3']:
        original = WORKER / f'failed-seal-{version}'
        require((original / 'REPORT.md').read_text().split('## 7.', 1)[0] == paper,
                'paper sections changed between seal attempts')
        require((original / 'verify.py').is_file() and (original / 'finding.json').is_file(), 'missing failed-code snapshot')

    STAGE = 'scope-and-documentation-records'
    previous = read(WORKER / 'preexisting-files.json')
    counts = {kind: sum(x['kind'] == kind for x in previous.values()) for kind in ['file', 'symlink', 'missing']}
    directories = sorted(p for p in previous if p.endswith('/'))
    require(counts == {'file': 25869, 'symlink': 22, 'missing': 4} and len(previous) == 25895,
            'initial pre-existing inventory differs')
    require(len(directories) == 4 and all(previous[p]['kind'] == 'missing' for p in directories),
            'nested repositories were not classified as directory-only')
    claims = read(WORKER / 'claims.json')
    require(claims['source_controls'] == [] and claims['source_control_evaluation'].startswith('not performed'),
            'unperformed finite source controls misclassified')
    require(claims['delivery_status'] == 'candidate_only_not_adopted', 'paper candidate status differs')
    checks = read(WORKER / 'checks.json')
    cc = {x['id']: x for x in checks['commands']}
    require(cc['fresh-base-docs']['exit_code'] == cc['current-whole-docgraph']['exit_code'] == 1,
            'historical documentation failure suppressed')
    require(len(checks['fresh_base_missing_paths']) == 2 and checks['whole_worktree_duplicate_id_lines'] == 62,
            'documentation failure counts differ')
    missing_lines = [line for line in (WORKER / cc['fresh-base-docs']['stdout']).read_text().splitlines()
                     if line.startswith('missing path:')]
    require(missing_lines == checks['fresh_base_missing_paths'], 'BASE missing-path recorded lines differ')
    whole = (WORKER / cc['current-whole-docgraph']['stdout']).read_text()
    whole += (WORKER / cc['current-whole-docgraph']['stderr']).read_text()
    require(sum('duplicate-id' in line for line in whole.splitlines()) == 62,
            'DocGraph duplicate-ID log count differs')
    return {
        'status': 'frozen_artifact_integrity_holds', 'regular_payload_files': 6049,
        'payload_symlinks': 5, 'receipt_bound_metadata_files': 10,
        'base_inputs_git_object_and_sha256': 12, 'frozen_current_pins': 6,
        'initial_hashed_preexisting_regular_files': 25869, 'initial_preexisting_symlinks': 22,
        'initial_nested_repository_directory_entries': 4, 'initial_nested_repository_recursive_hash': False,
        'parent_initial_strict_receipt_checked': True, 'historical_failed_seal_generations_preserved': 3,
        'paper_sections_1_to_6_identical_across_retries': True,
        'new_finite_source_controls': 'not established or evaluated; no trigger count',
        'paper_math_adjudication': 'outside this tool scope', 'lean_general_N2_E': 'OPEN',
        'finding': 'checks.json postseal_actual_results points to failed v1; final evidence is receipt-bound seal-final-v4/commands.json',
        'live_workspace_inventory_replay': 'parent initial exact inventory passed before fresh audit directories; frozen replay intentionally does not reassert current inventory or adopted current docs',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=WORKER / 'MANIFEST.final-v4.sha256')
    parser.add_argument('--symlinks', type=Path, default=WORKER / 'symlinks.json')
    parser.add_argument('--receipt', type=Path, default=WORKER / 'delivery.json')
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args), sort_keys=True))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f'artifact rejection [{STAGE}]: {error}', file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
