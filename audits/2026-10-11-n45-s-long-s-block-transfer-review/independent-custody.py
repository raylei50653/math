#!/usr/bin/env python3
"""Independent D inventory/authority/custody verifier, stdout only."""
import hashlib
import json
from pathlib import Path
import stat
import subprocess

REPO = Path(__file__).resolve().parents[2]
TARGET = REPO / 'audits/2026-10-11-n45-s-long-s-block-transfer'
DISPATCH = REPO / 'audits/2026-10-11-n45-s-long-s-rfibre-dispatch'
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'


def read(path):
    return json.loads(path.read_bytes())


def pin(path):
    assert stat.S_ISREG(path.lstat().st_mode), str(path)
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def relative(name):
    p = Path(name)
    assert not p.is_absolute() and '..' not in p.parts and p.parts and p.as_posix() == name
    return p


def inventory():
    files, dirs = {}, []
    todo = [TARGET]
    while todo:
        d = todo.pop()
        for p in sorted(d.iterdir()):
            n = p.relative_to(TARGET).as_posix()
            mode = p.lstat().st_mode
            if stat.S_ISDIR(mode):
                dirs.append(n); todo.append(p)
            elif stat.S_ISREG(mode):
                files[n] = pin(p)
            else:
                raise AssertionError('symlink/special: ' + n)
    return files, sorted(dirs)


def main():
    files, dirs = inventory()
    delivery = read(TARGET / 'delivery.json')
    assert delivery['base'] == BASE and delivery['status'] == '待獨立驗收'
    assert delivery['task_id'] == 'N45-S-LONG-S-BLOCK-TRANSFER'
    assert delivery['precise_metadata_exclusions'] == ['delivery.json']
    assert set(files) == set(delivery['files']) | {'delivery.json'}
    assert len(delivery['files']) == delivery['payload_files'] == 170
    assert sum(v['bytes'] for v in delivery['files'].values()) == delivery['payload_bytes'] == 24839641
    for name, value in delivery['files'].items():
        relative(name)
        assert files[name] == value, name

    inputs = read(TARGET / 'inputs.json')
    dispatch = read(DISPATCH / 'input-pins.json')
    assert inputs['base'] == dispatch['base'] == BASE
    assert inputs['dispatch_pin']['path'] == str(DISPATCH / 'input-pins.json')
    assert inputs['dispatch_pin']['sha256'] == pin(DISPATCH / 'input-pins.json')['sha256']
    authorities = []
    for key, count in [('BASE_blobs', 12), ('sealed_audit_SHA256', 11)]:
        records = inputs[key]
        assert len(records) == count
        for record in records:
            name = record['path']
            relative(name); relative(record['frozen_path'])
            declared = {k: record[k] for k in ('bytes', 'sha256')}
            matched = [r for r in dispatch['inputs'] if r['path'] == name]
            assert len(matched) == 1 and matched[0] == record, 'dispatch identity: ' + name
            assert pin(REPO / name) == pin(TARGET / record['frozen_path']) == pin(DISPATCH / record['frozen_path']) == declared
            if key == 'BASE_blobs':
                blob = subprocess.check_output(['git', 'rev-parse', BASE + ':' + name], cwd=REPO, text=True).strip()
                raw = subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=REPO)
                assert blob == record['git_blob'] and raw == (TARGET / record['frozen_path']).read_bytes()
                assert record['authority'] == 'BASE Git blob'
            else:
                assert record['git_blob'] is None and record['included_in_BASE_claimed'] is False
                assert record['authority'] == 'sealed audit physical SHA256'
            authorities.append({'path': name, 'authority': record['authority'], **declared})

    earlier = read(TARGET / 'logs/custody-before.stdout')
    guarded = read(TARGET / 'logs/custody-certificate-before.stdout')
    assert len(earlier['files']) == 1204 and len(guarded['files']) == 1205
    assert all(guarded['files'][name] == digest for name, digest in earlier['files'].items())
    assert set(guarded['files']) - set(earlier['files']) == {str((TARGET / 'certificate.json').relative_to(REPO))}
    for name, digest in guarded['files'].items():
        assert pin(REPO / relative(name))['sha256'] == digest, 'old input drift: ' + name
    for name, count in [('custody-after', 1204), ('custody-certificate-after', 1205)]:
        record = read(TARGET / f'logs/{name}.stdout')
        assert record['protected_files'] == count and record['changed'] == [] and record['status'] == 'passes'
        assert record['head_equal'] and record['tracked_diff_equal']
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    diff = subprocess.check_output(['git', 'diff', '--binary', 'HEAD'], cwd=REPO)
    assert head == BASE and diff == b''
    missing = []
    for name in ['artifacts/c5_no_spoke_exterior/observations.json',
                 'artifacts/c5_single_spoke_residual_locality/observations.json']:
        result = subprocess.run(['git', 'show', BASE + ':' + name], cwd=REPO, capture_output=True)
        assert result.returncode == 128 and result.stdout == b'' and b'not in' in result.stderr
        record = next(r for r in inputs['missing_BASE_findings'] if r['path'] == name)
        assert record['authority_admitted'] is False and record['finite_replay']['executed'] is False
        missing.append({'path': name, 'exit': 128, 'physical_or_quarantine_admitted': False,
                        'dependent_finite_replay_executed': False, 'stderr': result.stderr.decode().strip()})
    external = inputs['external_theorem_pins']
    assert len(external) == 1 and external[0]['git_blob'] is None
    assert external[0]['origin_refetched'] is False and external[0]['recurrence_dependency'] is False
    assert inventory() == (files, dirs), 'target changed during read-only check'
    print(json.dumps({'status': 'independent D custody passes', 'base': BASE,
                      'delivery': pin(TARGET / 'delivery.json'), 'payload_files': 170, 'payload_bytes': 24839641,
                      'target_regular_files': len(files), 'target_directories': dirs,
                      'metadata_exclusions': ['delivery.json'], 'authority_inputs': authorities,
                      'earlier_protected_files': 1204, 'certificate_guarded_files': 1205,
                      'certificate': pin(TARGET / 'certificate.json'),
                      'original_input_old_certificate_drift': [], 'head': head, 'tracked_diff_bytes': 0,
                      'expected_missing_BASE_blobs': missing, 'external_dependency': external,
                      'target_source_executed': False, 'writes': []}, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
