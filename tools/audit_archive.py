#!/usr/bin/env python3
"""Publish frozen audit bytes as deduplicated gzip blobs without changing originals.

pack archives snapshots, files >= 1 MB, and historical text with whitespace
diagnostics. restore recreates their exact paths; verify checks every blob and
every original. Small audit reports and active tools remain ordinary Git files.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
INDEX = 'audits/ARCHIVE.json'
BLOBS = 'audits/.archive/blobs'
BEGIN = '# BEGIN frozen audit archive: restore with python3 tools/audit_archive.py restore'
END = '# END frozen audit archive'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def safe_path(root, relative):
    parts = PurePosixPath(relative)
    if parts.is_absolute() or '..' in parts.parts or not parts.parts:
        raise ValueError(f'Unsafe archive path: {relative}')
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Archive path escapes destination: {relative}')
    return path


def historical_whitespace(path):
    try:
        value = path.read_text()
    except UnicodeError:
        return False
    return value.endswith('\n\n') or any(line.rstrip() != line for line in value.splitlines())


def pack(root):
    index = root / INDEX
    if index.exists():
        raise ValueError('Archive index already exists; preserve the published version')
    records, sources = {}, {}
    for directory, dirs, names in os.walk(root / 'audits'):
        dirs[:] = sorted(d for d in dirs if d not in {'.archive', '__pycache__'}
                         and not (Path(directory) / d).is_symlink())
        for name in sorted(names):
            path = Path(directory) / name
            if path.is_symlink() or path.suffix == '.pyc':
                continue
            relative = path.relative_to(root).as_posix()
            stat = path.stat()
            reason = ('snapshot' if {'snapshot', '.snapshot'} & set(path.relative_to(root).parts)
                      else 'large' if stat.st_size >= 1_000_000
                      else 'historical-whitespace' if historical_whitespace(path) else None)
            if not reason:
                continue
            sha = digest(path)
            sources.setdefault(sha, path)
            records[relative] = dict(sha256=sha, bytes=stat.st_size,
                                     mode=stat.st_mode & 0o777, reason=reason)
    folder = root / BLOBS
    folder.mkdir(parents=True, exist_ok=True)

    def compress(item):
        sha, source = item
        target = folder / (sha + '.gz')
        if target.exists():
            raise ValueError(f'Blob already exists: {target}')
        with source.open('rb') as incoming, target.open('wb') as outgoing:
            with gzip.GzipFile(filename='', mode='wb', fileobj=outgoing, mtime=0,
                               compresslevel=6) as compressed:
                shutil.copyfileobj(incoming, compressed, 1 << 20)
        return sha, dict(path=target.relative_to(root).as_posix(),
                         sha256=digest(target), bytes=target.stat().st_size)

    with ThreadPoolExecutor(max_workers=4) as pool:
        blobs = dict(pool.map(compress, sorted(sources.items())))
    data = dict(schema=1, description=__doc__, files=dict(sorted(records.items())),
                blobs=dict(sorted(blobs.items())))
    index.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    ignore = root / '.gitignore'
    value = ignore.read_text()
    if BEGIN in value:
        raise ValueError('Audit ignore block already exists')
    value = value.rstrip() + '\n\n' + BEGIN + '\n'
    value += ''.join('/' + relative + '\n' for relative in sorted(records))
    ignore.write_text(value + END + '\n')
    print(json.dumps(dict(archived_paths=len(records), unique_blobs=len(blobs),
                          raw_bytes=sum(x['bytes'] for x in records.values()),
                          compressed_bytes=sum(x['bytes'] for x in blobs.values()))))


def check_blob(root, sha, record):
    path = safe_path(root, record['path'])
    if path.stat().st_size != record['bytes'] or digest(path) != record['sha256']:
        raise ValueError(f'Compressed blob changed: {path}')
    h, size = hashlib.sha256(), 0
    with gzip.open(path, 'rb') as incoming:
        for block in iter(lambda: incoming.read(1 << 20), b''):
            h.update(block)
            size += len(block)
    if h.hexdigest() != sha:
        raise ValueError(f'Uncompressed blob hash mismatch: {path}')
    return size


def replay(root, action, destination, include_artifacts=False):
    data = json.loads((root / INDEX).read_text())
    checked = {sha: check_blob(root, sha, record) for sha, record in data['blobs'].items()}
    records = dict(data['files'])
    if include_artifacts:
        manifest_path = destination / 'artifacts/MANIFEST.json'
        manifest = json.loads(manifest_path.read_text())
        for relative, record in manifest['files'].items():
            if record['sha256'] not in checked:
                raise ValueError(f'No archived bytes for manifest artifact: {relative}')
            records[relative] = dict(sha256=record['sha256'], bytes=record['bytes'], mode=0o644)
    count = 0
    for relative, record in records.items():
        if checked[record['sha256']] != record['bytes']:
            raise ValueError(f'Uncompressed size mismatch: {relative}')
        path = safe_path(destination, relative)
        if path.exists():
            if path.stat().st_size != record['bytes'] or digest(path) != record['sha256']:
                raise ValueError(f'Existing file differs; refusing to replace: {path}')
        elif action == 'restore':
            path.parent.mkdir(parents=True, exist_ok=True)
            source = safe_path(root, data['blobs'][record['sha256']]['path'])
            fd, temporary = tempfile.mkstemp(prefix='.audit-restore-', dir=path.parent)
            temporary = Path(temporary)
            try:
                with os.fdopen(fd, 'wb') as outgoing, gzip.open(source, 'rb') as incoming:
                    shutil.copyfileobj(incoming, outgoing, 1 << 20)
                if temporary.stat().st_size != record['bytes'] or digest(temporary) != record['sha256']:
                    raise ValueError(f'Restored bytes differ: {relative}')
                temporary.chmod(record['mode'])
                os.replace(temporary, path)
            finally:
                temporary.unlink(missing_ok=True)
        else:
            raise FileNotFoundError(f'Missing audit input: {path}; run restore first')
        count += 1
    print(json.dumps(dict(all_checks_passed=True, files_checked=count,
                          unique_blobs_checked=len(checked), action=action,
                          includes_manifest_artifacts=include_artifacts)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('pack', 'restore', 'verify'))
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--destination', type=Path,
                        help='Restore/verify archived paths under a separate checkout')
    parser.add_argument('--artifacts', action='store_true',
                        help='Also restore/verify live artifacts by their MANIFEST SHA256')
    args = parser.parse_args()
    root = args.repo.resolve()
    if args.action == 'pack':
        pack(root)
    else:
        replay(root, args.action, (args.destination or root).resolve(), args.artifacts)


if __name__ == '__main__':
    main()
