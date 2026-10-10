#!/usr/bin/env python3
"""Read-only LOW2 artifact checks, not a mathematical or source validator."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
PROBES = ('bad-digest', 'missing-nested-delivery', 'duplicate-path',
          'unsafe-path', 'missing-payload', 'bad-receipt')
RUNS = ('normal', 'seed17') + PROBES
RECEIPT_LOGS = {f'receipt/{name}.{stream}.log'
                for name in RUNS for stream in ('stdout', 'stderr')}
# Exact relative paths only. Frozen/nested homonyms are ordinary payload.
EXCLUDED = {'MANIFEST.sha256', 'delivery.json', 'receipt.json'} | RECEIPT_LOGS
IDS = ['LOW2-CORE', 'LOW2-COMP', 'LOW2-JOIN', 'LOW2-F',
       'LOW2-MAP', 'LOW2-EXCLUSION']


def require(test, message):
    if not test:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def payload_inventory():
    regular, links = [], {}
    for path in HERE.rglob('*'):
        relative = path.relative_to(HERE).as_posix()
        if relative in EXCLUDED:
            continue
        if path.is_symlink():
            links[relative] = os.readlink(path)
        elif path.is_file():
            regular.append(relative)
    return sorted(regular), links


def check_manifest(path):
    regular, links = payload_inventory()
    require(not links, 'payload symlink inventory differs: expected none')
    records = {}
    for number, line in enumerate(path.read_text().splitlines(), 1):
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, f'manifest syntax: line {number}')
        digest, relative = match.groups()
        require(not Path(relative).is_absolute() and '..' not in Path(relative).parts,
                f'manifest unsafe path: {relative}')
        require(relative not in records, f'manifest duplicate path: {relative}')
        records[relative] = digest
    require(sorted(records) == regular, 'manifest payload inventory differs')
    for relative, digest in sorted(records.items()):
        require(sha(HERE / relative) == digest, f'manifest digest differs: {relative}')
    return len(records)


def check_inputs_and_workspace():
    require(git('rev-parse', 'HEAD').decode().strip() == BASE, 'workspace HEAD differs')
    initial = read_json(HERE / 'inputs-initial.json')
    require(initial['BASE'] == initial['head'] == BASE, 'initial HEAD differs')
    require(len(initial['pins']) == 8, 'task pin inventory differs')
    for item in initial['pins']:
        require(item['matches'] and item['expected'] == item['actual'], 'initial pin failed')
        require(sha(ROOT / item['path']) == item['expected'], 'live task pin differs: ' + item['path'])
    for item in initial['current_inputs']:
        require(sha(HERE / 'frozen/current' / item['path']) == item['sha256'],
                'frozen current input differs: ' + item['path'])
    for item in read_json(HERE / 'base-inputs.json')['inputs']:
        blob = git('show', BASE + ':' + item['path'])
        require(hashlib.sha256(blob).hexdigest() == item['sha256'], 'BASE bytes differ')
        require(git('rev-parse', BASE + ':' + item['path']).decode().strip() == item['git_blob'],
                'BASE object differs')
        require((HERE / 'frozen/BASE' / item['path']).read_bytes() == blob, 'frozen BASE differs')
    prefix = HERE.relative_to(ROOT).as_posix() + '/'
    actual = sorted({p.decode() for p in git('ls-files', '--cached', '--others',
                                           '--exclude-standard', '-z').split(b'\0')
                     if p and not p.decode().startswith(prefix)})
    old = read_json(HERE / 'preexisting-files.json')
    require(actual == sorted(old), 'preexisting Git inventory differs')
    for relative, record in sorted(old.items()):
        path = ROOT / relative
        if record['kind'] == 'file':
            require(path.is_file() and not path.is_symlink() and sha(path) == record['sha256'],
                    'preexisting file differs: ' + relative)
            require(stat.S_IMODE(path.stat().st_mode) == record['mode'], 'file mode differs: ' + relative)
        elif record['kind'] == 'symlink':
            require(path.is_symlink() and os.readlink(path) == record['target'],
                    'preexisting symlink differs: ' + relative)
        elif record['kind'] == 'directory':
            require(path.is_dir(), 'nested repository directory disappeared: ' + relative)
        elif record['kind'] == 'missing':
            require(not path.exists() and not path.is_symlink(), 'previously missing path appeared')
        else:
            raise ValueError('unknown preexisting inventory kind')
    for args, name in [(('diff', '--binary'), 'initial-tracked-diff'),
                       (('diff', '--cached', '--binary'), 'initial-cached-diff')]:
        require(git(*args) == (HERE / f'logs/{name}.stdout.log').read_bytes(), 'preexisting diff differs')
    return {kind: sum(v['kind'] == kind for v in old.values())
            for kind in ('file', 'symlink', 'directory', 'missing')}


def check_authored():
    claims = read_json(HERE / 'claims.json')
    require(claims['task'] == 'N45-S-LOW2', 'task differs')
    require(claims['delivery_status'] == 'candidate_pending_independent_adoption', 'candidate status differs')
    require([c['id'] for c in claims['claims']] == IDS, 'claim inventory differs')
    require(claims['source_controls'] == [] and claims['source_control_evaluation'] == 'not established; not executed; no trigger count',
            'source coverage misclassified')
    require(claims['source_realization'] is False and claims['new_Lean'] is False, 'evidence layer differs')
    for claim in claims['claims']:
        require(claim['source_contract'] == claims['full_source_contract'], 'incomplete claim contract')
        require(set(claim['dependencies']) <= set(IDS), 'unknown dependency')
        require(claim['machine_proved'] is False, 'tool mislabeled as proof')
    external = read_json(HERE / 'external/source.json')
    require(external['response_status'] == 200 and external['byte_equal'], 'official PDF differs from BASE')
    require(sha(HERE / 'external/gallai-official.pdf') == external['official_sha256'] == external['BASE_sha256'],
            'external PDF digest differs')
    require(external['pdftotext_exit'] == 0, 'PDF extraction failed')
    authored = ['REPORT.md', 'claims.json', 'verify.py', 'seal.py', 'run_checks.py', 'checks.json']
    for relative in authored:
        data = (HERE / relative).read_text()
        require(data.endswith('\n'), 'authored text lacks newline: ' + relative)
        require(all(line.rstrip(' \t') == line for line in data.splitlines()), 'authored trailing whitespace: ' + relative)
    text = (HERE / 'REPORT.md').read_text()
    text = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
    text = re.sub(r'(`+).*?\1', '', text)
    count = 0
    for destination in re.findall(r'\]\(([^\s)]+)\)', text):
        if '://' in destination:
            continue
        target = destination.split('#', 1)[0]
        if target in EXCLUDED and not (HERE / target).exists():
            continue  # During initial sealing the three named metadata files are pending.
        require((HERE / target).exists(), 'missing authored report link: ' + destination)
        count += 1
    return count


def check_receipt(receipt_path):
    delivery = read_json(HERE / 'delivery.json')
    require(delivery['manifest_sha256'] == sha(HERE / 'MANIFEST.sha256'), 'delivery manifest binding differs')
    require(delivery['receipt_sha256'] == sha(receipt_path), 'delivery receipt binding differs')
    require(delivery['paper_status'] == 'candidate_pending_independent_adoption', 'delivery scope differs')
    receipt = read_json(receipt_path)
    require(set(receipt['metadata']) == RECEIPT_LOGS, 'receipt metadata inventory differs')
    for relative, digest in receipt['metadata'].items():
        require(sha(HERE / relative) == digest, 'receipt metadata digest differs: ' + relative)
    require([r['name'] for r in receipt['commands']] == list(RUNS), 'receipt run inventory differs')
    for run in receipt['commands']:
        require(run['exit_code'] == run['expected_exit'], 'recorded tool exit differs')
        require(run['control_classification'] == 'triggered and holds', 'artifact control classification differs')
        require(run['stdout'] == f'receipt/{run["name"]}.stdout.log', 'stdout path differs')
        require(run['stderr'] == f'receipt/{run["name"]}.stderr.log', 'stderr path differs')
        if run['name'] in PROBES:
            require(run['rejection_stage'] in (HERE / run['stderr']).read_text(), 'negative rejected at wrong stage')
    require((HERE / 'receipt/normal.stdout.log').read_bytes() == (HERE / 'receipt/seed17.stdout.log').read_bytes(),
            'normal/seed17 stdout differs')
    require(receipt['payload_before'] == receipt['payload_after'], 'read-only checks changed payload')
    require(receipt['payload_after'] == sha(HERE / 'MANIFEST.sha256'), 'receipt payload identity differs')
    require(receipt['new_files_outside_audit'] == [] and receipt['changed_preexisting_files'] == [],
            'scope record differs')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=HERE / 'MANIFEST.sha256')
    parser.add_argument('--receipt', type=Path, default=HERE / 'receipt.json')
    parser.add_argument('--payload-only', action='store_true')
    args = parser.parse_args()
    try:
        count = check_manifest(args.manifest)
        live = check_inputs_and_workspace()
        links = check_authored()
        if not args.payload_only:
            check_receipt(args.receipt)
        print(json.dumps({'status': 'artifact_integrity_holds', 'payload_files': count,
                          'task_pins': 8, 'BASE_blobs': 4, 'live_inventory': live,
                          'nested_repository_recursive_hash': False,
                          'authored_local_links': links,
                          'receipt_checked': not args.payload_only,
                          'paper_proved_by_this_tool': False,
                          'source_controls': 'not established; not executed; no trigger count'},
                         sort_keys=True))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print('integrity rejection: ' + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
