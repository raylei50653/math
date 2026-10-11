#!/usr/bin/env python3
"""Independent read-only task C delivery/BASE/input custody verifier; stdlib only."""
import collections
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess

ROOT = Path('/home/ray/developer/ai/math')
TASK = ROOT / 'audits/2026-10-11-n45-s-long-s-joint'
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
PRIOR = 'audits/2026-10-10-n45-s-long-contract/certificate-v2.json'
EXCLUDED = {
    'delivery-verification.json', 'delivery.json',
    'logs/delivery-create.command.json', 'logs/delivery-create.stderr.log',
    'logs/delivery-create.stdout.log', 'logs/delivery-verify.command.json',
    'logs/delivery-verify.stderr.log', 'logs/delivery-verify.stdout.log',
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True).stdout


def safe(path):
    p = PurePosixPath(path)
    return not p.is_absolute() and '..' not in p.parts and str(p) == path


def inventory():
    regular, directories = {}, set()

    def walk(folder):
        for item in os.scandir(folder):
            rel = Path(item.path).relative_to(TASK).as_posix()
            mode = item.stat(follow_symlinks=False).st_mode
            need(not stat.S_ISLNK(mode), 'unexpected symlink: ' + rel)
            if stat.S_ISDIR(mode):
                directories.add(rel)
                walk(item.path)
            else:
                need(stat.S_ISREG(mode), 'unexpected special file: ' + rel)
                data = Path(item.path).read_bytes()
                regular[rel] = {'bytes': len(data), 'sha256': sha(data)}
    walk(TASK)
    return regular, directories


def main():
    regular, directories = inventory()
    delivery_bytes = (TASK / 'delivery.json').read_bytes()
    delivery = json.loads(delivery_bytes)
    need(delivery['base'] == BASE, 'delivery BASE differs')
    names = [item['path'] for item in delivery['files']]
    exclusions = [item['path'] for item in delivery['metadata_exclusions']]
    need(len(names) == len(set(names)) == 102, 'payload duplicate/count differs')
    need(len(exclusions) == len(set(exclusions)) == 8 and set(exclusions) == EXCLUDED,
         'exact metadata exclusion set differs')
    need(not set(names) & EXCLUDED, 'payload/metadata overlap')
    need(all(safe(path) for path in names + exclusions), 'unsafe relative path')
    need(set(regular) == set(names) | EXCLUDED, 'complete regular-file tree differs')
    expected_directories = {str(parent) for path in names + exclusions
                            for parent in PurePosixPath(path).parents if str(parent) != '.'}
    need(directories == expected_directories, 'complete directory tree differs')
    for item in delivery['files']:
        need(regular[item['path']] == {key: item[key] for key in ['bytes', 'sha256']},
             'payload bytes/hash differs: ' + item['path'])

    manifest = json.loads((TASK / 'inputs.json').read_bytes())
    need(manifest['base'] == BASE and manifest['head_at_start'] == BASE,
         'input manifest BASE differs')
    inputs = manifest['inputs']
    need(len(inputs) == 51, 'frozen input count differs')
    records, authority_counts = {}, collections.Counter()
    for item in inputs:
        path, frozen_path = item['path'], item['frozen_path']
        need(safe(path) and frozen_path == 'frozen/' + path, 'unsafe/misnamed frozen path')
        need(path not in records, 'duplicate input path: ' + path)
        frozen = (TASK / frozen_path).read_bytes()
        need(len(frozen) == item['bytes'] and sha(frozen) == item['sha256'],
             'frozen bytes/hash differs: ' + path)
        need((ROOT / path).read_bytes() == frozen, 'live input differs: ' + path)
        authority_counts[item['authority']] += 1
        if item['authority'] == 'BASE Git blob':
            blob = git('rev-parse', BASE + ':' + path).decode().strip()
            need(blob == item['git_blob'] and git('cat-file', 'blob', blob) == frozen,
                 'BASE Git blob differs: ' + path)
        else:
            need(item['authority'] == 'BASE archive payload' and path == PRIOR
                 and item['git_blob'] is None, 'unexpected archive authority')
            logical_blob = subprocess.run(['git', 'cat-file', '-e', BASE + ':' + path],
                                          cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            need(logical_blob.returncode != 0, 'archive logical path unexpectedly has BASE blob')
            blob = git('rev-parse', BASE + ':' + item['archive_blob_path']).decode().strip()
            packed = git('cat-file', 'blob', blob)
            need(blob == item['archive_git_blob'], 'archive Git blob differs')
            need(sha(packed) == item['archive_compressed_sha256'], 'archive compressed hash differs')
            need(gzip.decompress(packed) == frozen, 'archive decompressed bytes differ')
            entry = json.loads(git('show', BASE + ':' + item['archive_manifest']))['files'][path]
            need(entry['sha256'] == sha(frozen) and entry['bytes'] == len(frozen),
                 'BASE archive manifest entry differs')
        records[path] = sha(frozen)
    need(dict(authority_counts) == {'BASE Git blob': 50, 'BASE archive payload': 1},
         'authority count differs')
    need({path[len('frozen/'):] for path in regular if path.startswith('frozen/')} == set(records),
         'complete frozen input set differs')
    receipt = sha(delivery_bytes)
    verification = json.loads((TASK / 'delivery-verification.json').read_bytes())
    need(verification['receipt_sha256'] == receipt, 'verification receipt digest differs')
    need(inventory() == (regular, directories), 'target audit tree changed during read-only verification')
    print(json.dumps({
        'status': 'passes', 'base': BASE,
        'payload_files': len(names), 'payload_bytes': sum(item['bytes'] for item in delivery['files']),
        'exact_metadata_exclusions': sorted(EXCLUDED),
        'actual_regular_files': len(regular), 'actual_directories': len(directories),
        'symlinks': 0, 'special_files': 0, 'missing_files': 0, 'extra_files': 0,
        'frozen_inputs': len(inputs), 'live_inputs_match': len(inputs),
        'authority_counts': dict(authority_counts), 'target_tree_changed': False,
        'prior_certificate_sha256': records[PRIOR], 'delivery_sha256': receipt,
        'certificate_sha256': regular['certificate.json']['sha256'],
    }, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
