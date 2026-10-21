#!/usr/bin/env python3
"""Verify the exact original W7 evidence from Git's staged objects and archive."""
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    evidence = json.loads((HERE / 'evidence-before.json').read_bytes())
    selection = json.loads((HERE / 'archive-selection.json').read_bytes())['paths']
    raw_archive = subprocess.check_output(['git', 'show', ':audits/ARCHIVE.json'], cwd=ROOT)
    archive = json.loads(raw_archive)
    raw_index = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=ROOT)
    index = {}
    for entry in raw_index.split(b'\0'):
        if not entry:
            continue
        metadata, name = entry.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        require(stage == b'0', 'unmerged index entry')
        index[name.decode()] = oid.decode()
    cache = {}
    batch = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    def content(path):
        require(path in index, 'evidence missing from staged source: ' + path)
        batch.stdin.write((index[path] + '\n').encode())
        batch.stdin.flush()
        header = batch.stdout.readline().split()
        require(len(header) == 3 and header[1] == b'blob', 'missing staged blob')
        raw = batch.stdout.read(int(header[2]))
        require(batch.stdout.read(1) == b'\n', 'bad git batch framing')
        return raw
    archived = 0
    direct = 0
    for row in evidence['files']:
        path = row['path']
        if path in selection:
            record = archive['files'][path]
            blob = archive['blobs'][record['sha256']]
            compressed = content(blob['path'])
            require(len(compressed) == blob['bytes'] and sha256(compressed).hexdigest() == blob['sha256'],
                    'staged archive gzip mismatch')
            raw = gzip.decompress(compressed)
            actual = (len(raw), sha256(raw).hexdigest())
            archived += 1
        else:
            require(path in index, 'original evidence not staged: ' + path)
            oid = index[path]
            if oid not in cache:
                raw = content(path)
                cache[oid] = (len(raw), sha256(raw).hexdigest())
            actual = cache[oid]
            direct += 1
        require(actual == (row['bytes'], row['sha256']), 'staged original bytes changed: ' + path)
    batch.stdin.close()
    batch.stdout.close()
    require(batch.wait() == 0, 'git staged-object reader failed')
    base = json.loads((HERE / 'BASE.json').read_bytes())
    prefixes = base['connected_audit_roots'] + [str(HERE.relative_to(ROOT))]
    allowed = {'.gitignore', 'README.md', 'audits/ARCHIVE.json', 'audits/README.md',
               'docs/STATUS.md', 'docs/c5_kempe_guide.md', 'docs/history/2026-10-21-w7-L-path-publish.md'}
    allowed.update(archive['blobs'][archive['files'][p]['sha256']]['path'] for p in selection)
    staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=ROOT).decode().split('\0')
    staged = [p for p in staged if p]
    require(all(p in allowed or any(p.startswith(prefix + '/') for prefix in prefixes) for p in staged),
            'unrelated staged path')
    require(not any('__pycache__' in p or p.endswith('.pyc') for p in staged), 'bytecode was staged')
    print(json.dumps({'result': 'PASS', 'original_source_files': len(evidence['files']),
                      'direct_staged_source_paths': direct, 'archived_source_paths': archived,
                      'all_original_bytes_recovered_from_staged_objects': evidence['total_bytes'],
                      'unrelated_staged_paths': [], 'staged_bytecode_paths': [],
                      'staged_paths': len(staged)}, sort_keys=True))


if __name__ == '__main__':
    main()
