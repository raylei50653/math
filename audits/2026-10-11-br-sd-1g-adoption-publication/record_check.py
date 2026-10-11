#!/usr/bin/env python3
"""Capture one actual command without altering any historical evidence."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True)
    parser.add_argument('--expected', type=int, default=0)
    parser.add_argument('--seed17', action='store_true')
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not argv or '/' in args.name or args.name in ('.', '..'):
        parser.error('need command and simple unique name')
    if (AUDIT / 'SEAL.json').exists() or (AUDIT / 'proof/ACCEPTANCE.json').exists():
        parser.error('final review/seal exists; receipts must be external now')
    folder = AUDIT / 'logs' / args.name
    if AUDIT.is_symlink() or (AUDIT / 'logs').is_symlink() or folder.resolve().parent != (AUDIT / 'logs').resolve():
        parser.error('receipt path escapes the new audit or uses a symlink')
    folder.mkdir(exist_ok=False)
    changes = {'PYTHONDONTWRITEBYTECODE': '1'}
    if args.seed17:
        changes['PYTHONHASHSEED'] = '17'
    began = datetime.now(timezone.utc).isoformat()
    timer = time.monotonic()
    result = subprocess.run(argv, cwd=ROOT, env={**os.environ, **changes}, capture_output=True)
    row = dict(name=args.name, argv=argv, cwd=str(ROOT), environment=changes,
               started_utc=began, elapsed_seconds=time.monotonic()-timer,
               exit_code=result.returncode, expected_exit_code=args.expected)
    for kind, data in [('stdout', result.stdout), ('stderr', result.stderr)]:
        target = folder / (kind + '.txt')
        target.write_bytes(data)
        row[kind + '_path'] = str(target.relative_to(ROOT))
        row[kind + '_sha256'] = hashlib.sha256(data).hexdigest()
    (folder / 'receipt.json').write_text(json.dumps(row, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(row, ensure_ascii=False, sort_keys=True))
    if result.returncode != args.expected:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
