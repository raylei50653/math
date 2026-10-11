#!/usr/bin/env python3
"""Memory-only prospective adoption seal/document corruption controls.

Valid prospective manifests must pass before corruptions are tested. No disk
seal, approved document, historical evidence, or Git state is ever modified.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    helper = runpy.run_path(str(AUDIT / 'verify.py'), run_name='adoption_negative_helper')
    documents = helper['document_records']()
    prospective = helper['seal_value'](documents, helper['inventory'](excludes={'SEAL.json'}))
    manifest = json.loads((AUDIT / 'ADOPTION_MANIFEST.json').read_text())
    protected = {AUDIT / 'ADOPTION_MANIFEST.json', AUDIT / 'verify.py', AUDIT / 'negative_controls.py'}
    protected.update(ROOT / row['path'] for row in documents)
    if (AUDIT / 'SEAL.json').exists():
        protected.add(AUDIT / 'SEAL.json')
    before = {str(path): digest(path.read_bytes()) for path in protected}
    variants = [('valid-positive', prospective, manifest, 0)]
    for name, field, value in (('parent-closed', 'parent_status', 'CLOSED'),
                               ('source-escalation', 'actual_source_status', 'triggered and holds'),
                               ('Lean-escalation', 'new_Lean_theorem', True),
                               ('closure-escalation', 'new_unconditional_closures', 1),
                               ('extra-metadata', 'unreviewed_metadata', True)):
        bad = copy.deepcopy(prospective)
        bad[field] = value
        variants.append((name, bad, manifest, 1))
    bad = copy.deepcopy(prospective)
    bad['payloads'].pop()
    bad['bundle_sha256'] = digest(canonical({'documents': bad['documents'], 'payloads': bad['payloads']}))
    variants.append(('missing-payload-rehashed', bad, manifest, 1))
    bad = copy.deepcopy(prospective)
    bad['documents'][0]['sha256'] = '0' * 64
    bad['bundle_sha256'] = digest(canonical({'documents': bad['documents'], 'payloads': bad['payloads']}))
    variants.append(('document-hash-rehashed', bad, manifest, 1))
    bad_manifest = copy.deepcopy(manifest)
    bad_manifest['parent_status'] = 'CLOSED'
    variants.append(('document-manifest-parent', prospective, bad_manifest, 1))
    bad_manifest = copy.deepcopy(manifest)
    bad_manifest['documents'].pop()
    variants.append(('document-manifest-coverage', prospective, bad_manifest, 1))
    results = []
    for name, seal_value, document_value, expected in variants:
        descriptors = [os.memfd_create('br-sd-1g-seal-control'), os.memfd_create('br-sd-1g-document-control')]
        try:
            for fd, value in zip(descriptors, (seal_value, document_value)):
                os.write(fd, canonical(value))
                os.lseek(fd, 0, os.SEEK_SET)
            argv = [sys.executable, '-B', str(AUDIT / 'verify.py'), '--validate-manifests',
                    '--seal-path', '/proc/self/fd/' + str(descriptors[0]),
                    '--adoption-manifest-path', '/proc/self/fd/' + str(descriptors[1])]
            result = subprocess.run(argv, cwd=ROOT, capture_output=True, pass_fds=descriptors,
                                    env=os.environ | {'PYTHONDONTWRITEBYTECODE': '1'})
        finally:
            for fd in descriptors:
                os.close(fd)
        row = {'name': name, 'argv': argv, 'cwd': str(ROOT), 'expected_exit_code': expected,
               'exit_code': result.returncode, 'stdout': result.stdout.decode(), 'stderr': result.stderr.decode()}
        results.append(row)
        if result.returncode != expected:
            print(json.dumps({'status': 'control failure', 'cases': results}, sort_keys=True))
            raise SystemExit(1)
        if expected:
            reasons = {'document-manifest-parent': 'scope drift',
                       'document-manifest-coverage': 'approved document inventory'}
            reason = reasons.get(name, 'adoption seal corruption')
            if reason not in result.stderr.decode():
                print(json.dumps({'status': 'rejected for wrong reason', 'cases': results}, sort_keys=True))
                raise SystemExit(1)
    unchanged = all(digest(Path(path).read_bytes()) == expected for path, expected in before.items())
    if not unchanged:
        raise SystemExit('protected bytes changed during memory controls')
    print(json.dumps({'status': 'triggered and holds', 'positive_control': 'exit0', 'negative_count': len(results) - 1,
                      'cases': results, 'protected_bytes_unchanged': unchanged,
                      'parent_status': 'OPEN', 'actual_source_status': 'not triggered', 'new_Lean_theorem': False,
                      'new_unconditional_closures': 0, 'scope': 'memory-only named manifest/byte-custody controls'}, sort_keys=True))

if __name__ == '__main__':
    main()
