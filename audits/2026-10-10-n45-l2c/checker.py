#!/usr/bin/env python3
"""Independent frozen artifact checker; does not import worker modules."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

HERE = Path(__file__).resolve().parent
WORKER = HERE / 'frozen/worker'
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
RUNS = ('normal', 'seed17', 'bad-digest', 'missing-nested-delivery',
        'duplicate-path', 'unsafe-path', 'missing-payload', 'bad-receipt')
STAGES = {'bad-digest': 'manifest digest differs',
          'missing-nested-delivery': 'manifest payload inventory differs',
          'duplicate-path': 'manifest duplicate path',
          'unsafe-path': 'manifest unsafe path',
          'missing-payload': 'manifest payload inventory differs',
          'bad-receipt': 'delivery receipt binding differs'}
LOGS = {f'receipt/{name}.{stream}.log' for name in RUNS for stream in ('stdout', 'stderr')}
EXCLUDED = {'MANIFEST.sha256', 'delivery.json', 'receipt.json'} | LOGS
IDS = ['LOW2-CORE', 'LOW2-COMP', 'LOW2-JOIN', 'LOW2-F', 'LOW2-MAP', 'LOW2-EXCLUSION']


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text())


def inventory(root, exclusions):
    regular, links = [], []
    for path in root.rglob('*'):
        relative = path.relative_to(root).as_posix()
        if relative in exclusions:
            continue
        if path.is_symlink():
            links.append(relative)
        elif path.is_file():
            regular.append(relative)
    return sorted(regular), sorted(links)


def manifest_records(path):
    result = {}
    for number, line in enumerate(path.read_text().splitlines(), 1):
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, f'manifest syntax: line {number}')
        sha, relative = match.groups()
        parsed = PurePosixPath(relative)
        require(not parsed.is_absolute() and '..' not in parsed.parts,
                'manifest unsafe path: ' + relative)
        require(relative == parsed.as_posix(), 'manifest noncanonical path: ' + relative)
        require(relative not in result, 'manifest duplicate path: ' + relative)
        result[relative] = sha
    return result


def check_worker_manifest(path):
    files, links = inventory(WORKER, EXCLUDED)
    require(not links, 'worker symlink inventory differs')
    records = manifest_records(path)
    require(sorted(records) == files, 'manifest payload inventory differs')
    require(len(records) == 66, 'worker payload count differs')
    for relative, sha in sorted(records.items()):
        require(digest(WORKER / relative) == sha, 'manifest digest differs: ' + relative)
    for name in ('frozen/current/audits/2026-10-10-n45-s-low1/delivery.json',
                 'frozen/current/audits/2026-10-10-n45-l1r/delivery.json',
                 'frozen/current/audits/2026-10-10-n45-s-low1/seal-final-v4/commands.json'):
        require(name in records, 'nested metadata omitted: ' + name)
    return records


def check_full_capture():
    inputs = read(HERE / 'inputs.json')
    files, links = inventory(WORKER, set())
    require(not links and len(files) == 85, 'full capture inventory differs')
    require(files == sorted(inputs['worker_full_inventory']), 'full capture names differ')
    for relative, record in inputs['worker_full_inventory'].items():
        require(digest(WORKER / relative) == record['sha256'], 'captured worker file differs: ' + relative)
    require(inputs['head_at_capture'] == inputs['BASE'] == BASE, 'captured HEAD differs')
    require(inputs['preexisting_records_independently_rehashed'] ==
            {'file': 32177, 'symlink': 27, 'directory': 4, 'missing': 0}, 'preexisting counts differ')
    require(inputs['nested_repository_recursive_hash'] is False, 'nested directory scope changed')
    require(inputs['exact_live_git_inventory_repeated'] is False, 'live inventory scope changed')
    require(inputs['preexisting_tracking_diffs_byte_equal'] is True, 'captured diffs differ')
    require(digest(HERE / 'frozen/root-initial-strict-replays.json') ==
            inputs['root_initial_evidence_sha256'], 'root strict evidence differs')
    roots = read(HERE / 'frozen/root-initial-strict-replays.json')['records']
    require(roots['normal']['exit_code'] == roots['seed17']['exit_code'] == 0,
            'root strict positive exit differs')
    require(roots['normal']['output'] == roots['seed17']['output'], 'root strict stdout differs')
    require(roots['corrupted']['exit_code'] == roots['bad_receipt']['exit_code'] == 2,
            'root strict negative exit differs')
    require('manifest digest differs' in roots['corrupted']['output'], 'root manifest stage differs')
    require('delivery receipt binding differs' in roots['bad_receipt']['output'], 'root receipt stage differs')
    root_positive = json.loads(roots['normal']['output'])
    require(root_positive['receipt_checked'] is True and root_positive['payload_files'] == 66,
            'root strict positive coverage differs')
    return inputs


def check_frozen_inputs(inputs):
    initial = read(WORKER / 'inputs-initial.json')
    require(initial['head'] == initial['BASE'] == BASE, 'worker initial BASE differs')
    require(len(initial['pins']) == 8 and len(initial['current_inputs']) == 20, 'input counts differ')
    require(len({r['path'] for r in initial['pins']}) == 8, 'duplicate task pin')
    require(len({r['path'] for r in initial['current_inputs']}) == 20, 'duplicate frozen input')
    pins = {r['path']: r for r in initial['pins']}
    copied = {r['path']: r for r in initial['current_inputs']}
    require(set(pins) <= set(copied), 'task pin lacks frozen copy')
    require(len(inputs['pins_independently_rehashed']) == 8, 'capture pin count differs')
    for path, pin in pins.items():
        require(pin['matches'] is True and pin['expected'] == pin['actual'], 'worker initial pin differs')
        require(copied[path]['sha256'] == copied[path]['task_pin'] == pin['expected'], 'frozen pin binding differs')
    for record in initial['current_inputs']:
        require(digest(WORKER / 'frozen/current' / record['path']) == record['sha256'],
                'frozen current digest differs: ' + record['path'])
    task = copied[initial['task_path']]
    require(task['sha256'] == initial['task_sha256'], 'task digest binding differs')
    base = read(WORKER / 'base-inputs.json')
    require(base['BASE'] == BASE and len(base['inputs']) == 4, 'BASE input count differs')
    require(base['inputs'] == inputs['BASE_objects_independently_verified'], 'BASE capture binding differs')
    for record in base['inputs']:
        require(digest(WORKER / 'frozen/BASE' / record['path']) == record['sha256'], 'frozen BASE bytes differ')
        require(re.fullmatch(r'[0-9a-f]{40}', record['git_blob']) is not None, 'BASE object syntax differs')
    external = read(WORKER / 'external/source.json')
    require(external['BASE_sha256'] == external['official_sha256'] ==
            digest(WORKER / 'external/gallai-official.pdf'), 'external frozen PDF differs')
    require(external['byte_equal'] is True, 'external byte equality differs')


def check_coverage():
    claims = read(WORKER / 'claims.json')
    require(claims['task'] == 'N45-S-LOW2' and
            claims['delivery_status'] == 'candidate_pending_independent_adoption', 'claim scope differs')
    require([c['id'] for c in claims['claims']] == IDS, 'six claim names differ')
    require(claims['source_controls'] == [] and
            claims['source_control_evaluation'] == 'not established; not executed; no trigger count',
            'finite source coverage misclassified')
    require(claims['new_Lean'] is False and claims['source_realization'] is False, 'evidence layer differs')
    for claim in claims['claims']:
        require(claim['source_contract'] == claims['full_source_contract'], 'claim contract missing')
        require(claim['machine_proved'] is False, 'claim falsely machine proved')
        require(set(claim['dependencies']) <= set(IDS), 'claim dependency name differs')
    checks = read(WORKER / 'checks.json')
    require(checks['finite_source_controls'] == 'not established; not executed; no trigger count',
            'checks source coverage differs')
    statuses = {r['name']: r for r in checks['commands']}
    require(len(statuses) == len(checks['commands']) == 7, 'historical check count differs')
    for name, record in statuses.items():
        require(record['exit_code'] == record['expected_exit'], 'recorded historical exit differs')
        require((WORKER / record['stdout']).is_file() and (WORKER / record['stderr']).is_file(),
                'historical check log missing')
    require(statuses['retained-BASE-doc-links']['exit_code'] == 1 and
            statuses['current-whole-docgraph']['exit_code'] == 1, 'historical FAIL omitted')
    return statuses


def check_receipt(receipt_path):
    delivery = read(WORKER / 'delivery.json')
    require(delivery['BASE'] == BASE and delivery['task'] == 'N45-S-LOW2', 'delivery identity differs')
    require(delivery['excluded_exact_paths'] == sorted(EXCLUDED) and len(EXCLUDED) == 19,
            'exact excluded inventory differs')
    require(delivery['manifest_sha256'] == digest(WORKER / 'MANIFEST.sha256'),
            'delivery manifest binding differs')
    require(delivery['receipt_sha256'] == digest(receipt_path), 'delivery receipt binding differs')
    require(delivery['paper_status'] == 'candidate_pending_independent_adoption' and
            delivery['source_controls'] == 'not established; not executed; no trigger count' and
            delivery['source_realization'] is False and delivery['new_Lean'] is False,
            'delivery evidence boundary differs')
    receipt = read(receipt_path)
    require(set(receipt['metadata']) == LOGS and len(LOGS) == 16, 'receipt log inventory differs')
    for relative, sha in receipt['metadata'].items():
        require(digest(WORKER / relative) == sha, 'receipt log digest differs: ' + relative)
    require([r['name'] for r in receipt['commands']] == list(RUNS), 'receipt run names differ')
    for record in receipt['commands']:
        name = record['name']
        expected = 0 if name in RUNS[:2] else 2
        require(record['exit_code'] == record['expected_exit'] == expected, 'receipt run exit differs')
        require(record['control_classification'] == 'triggered and holds', 'artifact classification differs')
        for stream in ('stdout', 'stderr'):
            require(record[stream] == f'receipt/{name}.{stream}.log', 'receipt log path differs')
        if name in STAGES:
            require(record['rejection_stage'] == STAGES[name], 'negative stage label differs')
            require(STAGES[name] in (WORKER / record['stderr']).read_text(), 'negative stage evidence differs')
            require((WORKER / record['stdout']).read_bytes() == b'', 'negative has unexpected stdout')
        else:
            require('--payload-only' in record['command'], 'sealing positive coverage mislabeled')
    require(receipt['commands'][1]['PYTHONHASHSEED'] == '17', 'worker seed17 setting differs')
    require((WORKER / 'receipt/normal.stdout.log').read_bytes() ==
            (WORKER / 'receipt/seed17.stdout.log').read_bytes(), 'worker seed stdout differs')
    positive = read(WORKER / 'receipt/normal.stdout.log')
    require(positive['receipt_checked'] is False, 'sealing positive falsely strict')
    require(positive['payload_files'] == 66, 'sealing payload count differs')
    bad_receipt = receipt['commands'][-1]
    require(bad_receipt['command'][2] == '-c' and 'verify.read_json=lambda' in bad_receipt['command'][3],
            'bad receipt shim boundary omitted')
    require('synthetic tool probe' in receipt['bad_receipt_probe_boundary'], 'synthetic receipt scope omitted')
    require(receipt['payload_before'] == receipt['payload_after'] == digest(WORKER / 'MANIFEST.sha256'),
            'worker read-only payload identity differs')
    require(receipt['new_files_outside_audit'] == receipt['changed_preexisting_files'] == [],
            'worker scope record differs')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=WORKER / 'MANIFEST.sha256')
    parser.add_argument('--receipt', type=Path, default=WORKER / 'receipt.json')
    args = parser.parse_args()
    try:
        records = check_worker_manifest(args.manifest)
        inputs = check_full_capture()
        check_frozen_inputs(inputs)
        check_coverage()
        check_receipt(args.receipt)
        print(json.dumps({'status': 'frozen_artifact_integrity_holds', 'worker_payload_regular': len(records),
                          'worker_payload_symlinks': 0, 'worker_total_regular': 85,
                          'excluded_exact_files': 19, 'receipt_logs': 16, 'receipt_metadata_including_json': 17,
                          'BASE_objects': 4, 'task_pins': 8, 'frozen_current_inputs': 20,
                          'scope': 'frozen evidence, not current whole workspace',
                          'nested_repository_recursive_hash': False,
                          'mathematical_verdict': 'not evaluated by this tool',
                          'source_controls': 'not established; not executed; no trigger count',
                          'new_Lean': False}, sort_keys=True))
    except (OSError, ValueError, KeyError) as error:
        print('independent integrity rejection: ' + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
