#!/usr/bin/env python3
"""Reject large generated files in the Git index without a documented exception.

Run locally after staging changes: python3 tools/check_generated_artifacts.py
CI uses the same index check. Symlinks are measured as links, not their targets.
This checks storage and producer registration; it does not run every producer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
THRESHOLD = 1_000_000
SUFFIXES = {'.json', '.jsonl', '.ndjson', '.json5', '.bin'}
EXCEPTIONS = 'tools/generated_artifact_exceptions.json'
MANIFEST = 'artifacts/MANIFEST.json'
REGULAR = {'100644', '100755'}


def git(repo, *args, data=None):
    return subprocess.run(['git', '-C', str(repo), *args], input=data,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout


def relative_path(value):
    if not isinstance(value, str) or not value:
        raise ValueError('paths must be nonempty strings')
    path = PurePosixPath(value)
    if (path.is_absolute() or '..' in path.parts or path.as_posix() != value
            or any(c in value for c in '*?[]\\')):
        raise ValueError(f'expected an exact repository-relative path: {value!r}')
    return value


def valid_sha(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def index_entries(repo):
    entries = {}
    for item in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not item:
            continue
        metadata, path = item.split(b'\t', 1)
        mode, oid, stage = metadata.decode('ascii').split()
        name = path.decode('utf-8', errors='surrogateescape')
        if stage != '0':
            raise ValueError(f'unmerged Git index entry: {name}')
        entries[name] = (mode, oid)
    return entries


def object_sizes(repo, oids):
    if not oids:
        return {}
    data = ('\n'.join(sorted(oids)) + '\n').encode('ascii')
    output = git(repo, 'cat-file', '--batch-check=%(objectname) %(objecttype) %(objectsize)', data=data)
    sizes = {}
    for line in output.decode('ascii').splitlines():
        oid, kind, size = line.split()
        if kind != 'blob':
            raise ValueError(f'expected a Git blob: {oid}')
        sizes[oid] = int(size)
    return sizes


def index_json(repo, entries, path):
    if path not in entries or entries[path][0] not in REGULAR:
        raise ValueError(f'{path}: needs a regular file in the Git index')
    return json.loads(git(repo, 'cat-file', 'blob', entries[path][1]))


def indexed_ignore_rules(repo, entries, paths):
    # git check-ignore normally reads the worktree. Materialize just the staged
    # ancestor ignore files so unstaged edits and local exclusions cannot pass CI.
    ignore_paths = set()
    for path in paths:
        parent = PurePosixPath(path).parent
        while True:
            candidate = (parent / '.gitignore').as_posix()
            if candidate in entries and entries[candidate][0] in REGULAR:
                ignore_paths.add(candidate)
            if parent == PurePosixPath('.'):
                break
            parent = parent.parent
    with tempfile.TemporaryDirectory(prefix='generated-artifact-ignore-') as temporary:
        checkout = Path(temporary)
        git(checkout, 'init', '--quiet')
        for path in sorted(ignore_paths):
            target = checkout / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(git(repo, 'cat-file', 'blob', entries[path][1]))
        data = b'\0'.join(p.encode('utf-8') for p in paths) + b'\0'
        command = ['git', '-C', str(checkout), '-c', 'core.excludesFile=/dev/null',
                   'check-ignore', '--no-index', '--verbose', '-z', '--stdin']
        result = subprocess.run(command, input=data, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, check=False)
        if result.returncode not in (0, 1):
            raise ValueError(result.stderr.decode('utf-8', errors='replace'))
        fields = result.stdout.split(b'\0')
        ignored = set()
        for offset in range(0, len(fields) - 1, 4):
            source, _, pattern, path = fields[offset:offset + 4]
            if source.endswith(b'.gitignore') and not pattern.startswith(b'!'):
                ignored.add(path.decode('utf-8', errors='surrogateescape'))
        return ignored


def check(repo):
    entries = index_entries(repo)
    generated = {p: oid for p, (mode, oid) in entries.items()
                 if mode in REGULAR and PurePosixPath(p).suffix.lower() in SUFFIXES}
    sizes = object_sizes(repo, set(generated.values()))
    policy = index_json(repo, entries, EXCEPTIONS)
    if (not isinstance(policy, dict) or policy.get('version') != 1
            or not isinstance(policy.get('files'), dict)):
        raise ValueError(f'{EXCEPTIONS}: expected version 1 and a files object')
    errors = []
    allowed = set()
    for path, record in sorted(policy['files'].items()):
        try:
            relative_path(path)
            if not isinstance(record, dict):
                raise ValueError('exception must be an object')
            if not isinstance(record.get('reason'), str) or not record['reason'].strip():
                raise ValueError('exception needs a nonempty reason')
            if path not in generated:
                raise ValueError('exception is stale or does not name a regular tracked generated file')
            if sizes[generated[path]] < THRESHOLD:
                raise ValueError('exception is stale because the file is smaller than 1 MB')
            if record.get('kind') == 'frozen':
                if (type(record.get('bytes')) is not int or record['bytes'] < 0
                        or not valid_sha(record.get('sha256'))):
                    raise ValueError('frozen exception needs bytes and a SHA256')
                oid = generated[path]
                if sizes[oid] != record['bytes']:
                    raise ValueError('frozen exception byte count differs from the Git index')
                digest = hashlib.sha256(git(repo, 'cat-file', 'blob', oid)).hexdigest()
                if digest != record['sha256']:
                    raise ValueError('frozen exception SHA256 differs from the Git index')
            elif record.get('kind') == 'metadata':
                generator = relative_path(record.get('generator'))
                if (not generator.endswith('.py') or generator not in entries
                        or entries[generator][0] not in REGULAR):
                    raise ValueError('metadata exception needs a regular tracked Python generator')
            else:
                raise ValueError('exception kind must be frozen or metadata')
            allowed.add(path)
        except ValueError as error:
            errors.append(f'{path}: {error}')

    large = {p: sizes[oid] for p, oid in generated.items() if sizes[oid] >= THRESHOLD}
    for path, size in sorted(large.items()):
        if path not in allowed:
            errors.append(f'{path}: {size:,} bytes are tracked; register a producer and ignore the output, '
                          'or document a specific exception')

    registered = {}
    if MANIFEST in entries:
        manifest = index_json(repo, entries, MANIFEST)
        if not isinstance(manifest, dict) or not isinstance(manifest.get('files'), dict):
            raise ValueError(f'{MANIFEST}: expected a files object')
        for path, record in sorted(manifest['files'].items()):
            try:
                relative_path(path)
                if not path.startswith('artifacts/'):
                    raise ValueError('manifest output must be under artifacts/')
                if not isinstance(record, dict):
                    raise ValueError('manifest record must be an object')
                if (type(record.get('bytes')) is not int or record['bytes'] < THRESHOLD
                        or not valid_sha(record.get('sha256'))):
                    raise ValueError('manifest record needs a size >= 1 MB and a SHA256')
                script = record.get('script')
                relative_path(script)
                if not script.endswith('.py'):
                    raise ValueError('manifest record needs a Python producer')
                producer = script if '/' in script else 'scripts/' + script
                if producer not in entries or entries[producer][0] not in REGULAR:
                    raise ValueError(f'producer is not a regular tracked file: {producer}')
                if path in entries:
                    raise ValueError('manifest output is still tracked by Git')
                registered[path] = record
            except ValueError as error:
                errors.append(f'{path}: {error}')
        if registered:
            ignored = indexed_ignore_rules(repo, entries, registered)
            for path in sorted(set(registered) - ignored):
                errors.append(f'{path}: manifest output needs a repository .gitignore rule')

    if errors:
        for error in errors:
            print(f'ERROR {error}', file=sys.stderr)
        return 1
    print(f'Generated artifact policy OK: {len(generated)} indexed files, '
          f'{len(large)} large files with documented exceptions, {len(registered)} registered outputs.')
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        return check(args.repo.resolve())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'ERROR {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
