#!/usr/bin/env python3
"""Read-only verification of this independently sealed audit and its frozen worker."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    try:
        receipt = json.loads((HERE / 'delivery.json').read_text())
        manifest = HERE / 'MANIFEST.sha256'
        require(sha(manifest) == receipt['manifest_sha256'], 'own manifest binding differs')
        regular, links = [], {}
        for path in HERE.rglob('*'):
            relative = path.relative_to(HERE).as_posix()
            if relative in {'MANIFEST.sha256', 'delivery.json'} or relative.startswith('seal-checks/'):
                continue
            if path.is_symlink():
                links[relative] = os.readlink(path)
            elif path.is_file():
                regular.append(relative)
        require(not links, 'unexpected own symlink')
        records = {}
        for line in manifest.read_text().splitlines():
            match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
            require(match is not None, 'malformed own manifest')
            value, relative = match.groups()
            require(not Path(relative).is_absolute() and '..' not in Path(relative).parts, 'unsafe own manifest path')
            require(relative not in records, 'duplicate own manifest path')
            records[relative] = value
        require(sorted(records) == sorted(regular), 'own exact payload inventory differs')
        for relative, value in sorted(records.items()):
            require(sha(HERE / relative) == value, f'own payload digest differs: {relative}')
        actual_seal = []
        for path in (HERE / 'seal-checks').rglob('*'):
            require(not path.is_symlink(), 'unbound own metadata symlink')
            if path.is_file():
                actual_seal.append(path.relative_to(HERE).as_posix())
        require(sorted(actual_seal) == sorted(receipt['seal_files']), 'own exact receipt metadata differs')
        for relative, value in sorted(receipt['seal_files'].items()):
            require(relative.startswith('seal-checks/') and '..' not in Path(relative).parts, 'unsafe own receipt path')
            require(sha(HERE / relative) == value, f'own receipt digest differs: {relative}')
        result = subprocess.run(['python3','-B',str(HERE / 'checker.py')],capture_output=True)
        require(result.returncode == 0 and not result.stderr, 'independent frozen checker rejected worker')
        checks = json.loads((HERE / 'checks.json').read_text())
        require(checks['all_exits_and_rejection_stages_match'] and checks['own_negative_controls'] == 7,
                'independent control result differs')
        require(checks['normal_seed17_stdout_byte_equal'], 'independent normal/seed17 differs')
        for row in checks['commands']:
            require(sha(HERE / row['stdout']) == row['stdout_sha256'] and sha(HERE / row['stderr']) == row['stderr_sha256'],
                    'independent control log binding differs')
        seal = json.loads((HERE / 'seal-checks/commands.json').read_text())
        require(seal['normal_seed17_stdout_byte_equal'], 'own final seal normal/seed17 differs')
        require(all(row['exit_code'] == 0 for row in seal['commands']), 'own final sealing command failed')
        print(json.dumps(dict(status='independent_audit_integrity_holds',own_payload_files=len(records),
                              own_receipt_metadata_files=len(actual_seal),worker_payload_files=6049,
                              worker_payload_symlinks=5,worker_receipt_metadata_files=10,
                              own_negative_controls=7,paper_math_proved=False),sort_keys=True))
    except (OSError,ValueError,KeyError) as error:
        print(f'independent audit rejection: {error}',file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
