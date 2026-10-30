#!/usr/bin/env python3
"""Read-only verification of this migration's original Markdown snapshot."""
import csv
import hashlib
from pathlib import Path, PurePosixPath
import tarfile


def main():
    directory = Path(__file__).resolve().parent
    for line in (directory / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        if name not in {'original-markdown.tar.gz', 'paths.tsv'}:
            raise ValueError('unexpected checksum member: ' + name)
        actual = hashlib.sha256((directory / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError('container checksum mismatch: ' + name)
    rows = list(csv.DictReader((directory / 'paths.tsv').open(), delimiter='\t'))
    expected = {row['original_path']: row['original_sha256'] for row in rows}
    if len(rows) != len(expected):
        raise ValueError('duplicate original path in paths.tsv')
    seen = set()
    with tarfile.open(directory / 'original-markdown.tar.gz', 'r:gz') as archive:
        for member in archive:
            name = PurePosixPath(member.name)
            if (not member.isfile() or name.is_absolute() or '..' in name.parts
                    or member.name in seen or member.name not in expected):
                raise ValueError('unsafe, duplicate or unlisted member: ' + member.name)
            data = archive.extractfile(member).read()
            if hashlib.sha256(data).hexdigest() != expected[member.name]:
                raise ValueError('original checksum mismatch: ' + member.name)
            seen.add(member.name)
    if seen != set(expected):
        raise ValueError('missing original members')
    print(f'OK: container checksums, path inventory and {len(seen)} original Markdown hashes')


if __name__ == '__main__':
    main()
