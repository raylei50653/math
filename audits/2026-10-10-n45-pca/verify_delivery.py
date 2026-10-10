#!/usr/bin/env python3
"""Read-only exact inventory verifier for the sealed PCA artifact."""
from hashlib import sha256
import json
from pathlib import Path
import stat

HOME=Path(__file__).resolve().parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    delivery=json.loads((HOME/'delivery.json').read_text())
    assert digest(HOME/'MANIFEST.sha256')==delivery['manifest_sha256']
    assert digest(HOME/'independent-judgment.json')==delivery['judgment_sha256']
    assert digest(HOME/'REPORT.md')==delivery['report_sha256']
    assert digest(HOME/'independent-certificate.json')==delivery['independent_certificate_sha256']
    records={}
    for line in (HOME/'MANIFEST.sha256').read_text().splitlines():
        h,path=line.split('  ',1)
        assert path not in records and digest(HOME/path)==h,path
        records[path]=h
    actual={str(p.relative_to(HOME)) for p in HOME.rglob('*') if stat.S_ISREG(p.lstat().st_mode)}-{'MANIFEST.sha256','delivery.json'}
    assert set(records)==actual,'missing/extra regular payload'
    assert len(records)==delivery['inventory_files']
    assert sum((HOME/path).stat().st_size for path in records)==delivery['inventory_bytes']
    print(json.dumps({'result':'holds','inventory_files':len(records),'manifest_sha256':delivery['manifest_sha256'],
                      'judgment_sha256':delivery['judgment_sha256'],'report_sha256':delivery['report_sha256']},sort_keys=True))


if __name__=='__main__':
    main()
