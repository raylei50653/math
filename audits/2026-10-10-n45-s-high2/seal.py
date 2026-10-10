#!/usr/bin/env python3
"""Exact top-level metadata exclusion, payload custody, and read-only delivery checks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
META = {'manifest.json', 'delivery.json', 'receipt.json'}


def encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inventory():
    result = {}
    for p in sorted(OUT.rglob('*')):
        rel = p.relative_to(OUT).as_posix()
        if p.is_symlink():
            raise ValueError('payload inventory: symlink ' + rel)
        if p.is_file() and rel not in META:
            result[rel] = {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
    return result


def validate_inventory(manifest):
    actual = inventory()
    listed = manifest['payload']
    missing = sorted(set(actual) - set(listed))
    extra = sorted(set(listed) - set(actual))
    drift = sorted(k for k in set(actual) & set(listed) if actual[k] != listed[k])
    if missing or extra or drift:
        raise ValueError('payload inventory: ' + json.dumps(
            {'missing': missing, 'extra': extra, 'drift': drift}, sort_keys=True))
    if manifest['excluded_exact_top_level'] != sorted(META):
        raise ValueError('metadata exclusion: incorrect exact paths')
    return len(actual)


def check_payload():
    manifest = json.loads((OUT / 'manifest.json').read_text())
    count = validate_inventory(manifest)
    delivery = json.loads((OUT / 'delivery.json').read_text())
    if delivery['manifest_sha256'] != sha((OUT / 'manifest.json').read_bytes()):
        raise ValueError('metadata binding: delivery to manifest')
    if delivery['inputs_sha256'] != sha((OUT / 'inputs-final.json').read_bytes()):
        raise ValueError('metadata binding: delivery to inputs')
    if delivery['certificate_sha256'] != sha((OUT / 'certificate.json').read_bytes()):
        raise ValueError('metadata binding: delivery to certificate')
    return count


def check_delivery():
    count = check_payload()
    receipt = json.loads((OUT / 'receipt.json').read_text())
    for path in ['manifest.json', 'delivery.json']:
        if receipt[path + '_sha256'] != sha((OUT / path).read_bytes()):
            raise ValueError('metadata binding: receipt to ' + path)
    records = receipt['read_only_payload_checks']
    expected = ['python3', '-B', str(OUT / 'seal.py'), '--check-payload']
    if len(records) != 2 or any(r['command'] != expected or r['exit'] != 0 for r in records):
        raise ValueError('metadata receipt: missing actual normal/seed17 checks')
    if records[0]['environment'].get('PYTHONHASHSEED') is not None:
        raise ValueError('metadata receipt: normal seed')
    if records[1]['environment'].get('PYTHONHASHSEED') != '17':
        raise ValueError('metadata receipt: seed17 missing')
    if records[0]['stdout'] != records[1]['stdout'] or records[0]['stderr'] != records[1]['stderr']:
        raise ValueError('metadata receipt: differing replay output')
    for r in records:
        if sha(r['stdout'].encode()) != r['stdout_sha256'] or sha(r['stderr'].encode()) != r['stderr_sha256']:
            raise ValueError('metadata receipt: output binding')
    return count


def seal():
    for path in META:
        if (OUT / path).exists():
            raise ValueError('exclusive metadata create: ' + path)
    manifest = {'task': 'N45-S-HIGH2', 'excluded_exact_top_level': sorted(META), 'payload': inventory()}
    with (OUT / 'manifest.json').open('xb') as f:
        f.write(encoded(manifest))
    delivery = {'task': 'N45-S-HIGH2', 'status': 'paper candidate pending independent adoption',
                'finite_source': 'not established; not executed; no trigger count',
                'manifest_sha256': sha((OUT / 'manifest.json').read_bytes()),
                'inputs_sha256': sha((OUT / 'inputs-final.json').read_bytes()),
                'certificate_sha256': sha((OUT / 'certificate.json').read_bytes()),
                'payload_files': len(manifest['payload']), 'metadata_files': sorted(META),
                'new_Lean': False, 'general_N2_E': 'OPEN'}
    with (OUT / 'delivery.json').open('xb') as f:
        f.write(encoded(delivery))
    records = []
    for seed in [None, '17']:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
        env.pop('PYTHONHASHSEED', None)
        if seed:
            env['PYTHONHASHSEED'] = seed
        cmd = ['python3', '-B', str(OUT / 'seal.py'), '--check-payload']
        r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
        record = {'command': cmd, 'cwd': str(ROOT), 'exit': r.returncode,
                  'stdout': r.stdout, 'stderr': r.stderr,
                  'stdout_sha256': sha(r.stdout.encode()), 'stderr_sha256': sha(r.stderr.encode()),
                  'environment': {'PYTHONDONTWRITEBYTECODE': '1', 'GIT_OPTIONAL_LOCKS': '0'}}
        if seed:
            record['environment']['PYTHONHASHSEED'] = seed
        records.append(record)
    receipt = {'task': 'N45-S-HIGH2', 'manifest.json_sha256': sha((OUT / 'manifest.json').read_bytes()),
               'delivery.json_sha256': sha((OUT / 'delivery.json').read_bytes()),
               'read_only_payload_checks': records,
               'historical_failures_retained': ['BASE missing-doc paths', 'whole-tree DocGraph duplicate IDs',
                                               'historical E4 provenance replay FAIL']}
    with (OUT / 'receipt.json').open('xb') as f:
        f.write(encoded(receipt))
    return check_delivery()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--seal', action='store_true')
    p.add_argument('--check-payload', action='store_true')
    p.add_argument('--check-delivery', action='store_true')
    p.add_argument('--check-inventory-stdin', action='store_true')
    a = p.parse_args()
    try:
        if sum([a.seal, a.check_payload, a.check_delivery, a.check_inventory_stdin]) != 1:
            p.error('select one operation')
        count = (seal() if a.seal else check_payload() if a.check_payload else
                 check_delivery() if a.check_delivery else validate_inventory(json.load(sys.stdin)))
        print(json.dumps({'task': 'N45-S-HIGH2', 'payload_files': count,
                          'status': 'artifact integrity only; paper not adjudicated'}, sort_keys=True))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
