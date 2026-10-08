#!/usr/bin/env python3
"""Restore only the M2 inherited input from candidate archived bytes, exclusively."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REL = 'artifacts/c5_excess_two_mixed_omission/observations.json'


def main():
    record = json.loads((ROOT / 'artifacts/MANIFEST.json').read_text())['files'][REL]
    archive = json.loads((ROOT / 'audits/ARCHIVE.json').read_text())
    blob_record = archive['blobs'][record['sha256']]
    blob = (ROOT / blob_record['path']).read_bytes()
    assert len(blob) == blob_record['bytes']
    assert hashlib.sha256(blob).hexdigest() == blob_record['sha256']
    raw = gzip.decompress(blob)
    assert len(raw) == record['bytes']
    assert hashlib.sha256(raw).hexdigest() == record['sha256']
    target = ROOT / REL
    if target.exists():
        assert target.read_bytes() == raw, 'Existing input differs; refusing replacement'
        action = 'verified existing bytes'
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(raw)
        action = 'exclusive restore'
    print(json.dumps(dict(action=action, path=REL, **record, blob=blob_record), sort_keys=True))


if __name__ == '__main__':
    main()
