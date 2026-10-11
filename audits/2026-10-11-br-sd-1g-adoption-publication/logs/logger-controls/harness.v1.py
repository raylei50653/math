#!/usr/bin/env python3
"""Exercise the actual new logger in disposable paths; no sealed file changes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

AUDIT = Path(__file__).resolve().parent

def main():
    source = (AUDIT / 'record_check.py').read_bytes()
    cases = []
    with tempfile.TemporaryDirectory(prefix='br-sd-1g-logger-') as temporary:
        root = Path(temporary)
        outside = root / 'outside'
        outside.mkdir()
        for name, expected in [('regular-positive', 0), ('symlink-logs', 2), ('parent-escape', 2), ('sealed-refusal', 2)]:
            audit = root / 'audits' / name
            audit.mkdir(parents=True)
            script = audit / 'record_check.py'
            script.write_bytes(source)
            if name == 'symlink-logs':
                (audit / 'logs').symlink_to(outside, target_is_directory=True)
            if name == 'sealed-refusal':
                (audit / 'SEAL.json').write_text('{}\n')
            label = '../escape' if name == 'parent-escape' else 'probe'
            argv = [sys.executable, '-B', str(script), '--name', label, '--', sys.executable, '-B', '-c', 'print("control")']
            result = subprocess.run(argv, capture_output=True, text=True)
            if result.returncode != expected:
                raise SystemExit('logger control failed: ' + name)
            if expected:
                required = 'symlink' if name == 'symlink-logs' else ('simple unique name' if name == 'parent-escape' else 'final review/seal exists')
                if required not in result.stderr or (audit / 'logs/probe').exists():
                    raise SystemExit('logger failed for unexpected reason or wrote through rejected boundary: ' + name)
            else:
                receipt = json.loads((audit / 'logs/probe/receipt.json').read_text())
                if receipt['exit_code'] != 0 or (audit / 'logs/probe/stdout.txt').read_text() != 'control\n':
                    raise SystemExit('logger positive receipt mismatch')
            cases.append(dict(name=name, argv=argv, exit_code=result.returncode, expected_exit_code=expected,
                              stdout=result.stdout, stderr=result.stderr))
        if list(outside.iterdir()) or (root / 'escape').exists():
            raise SystemExit('logger control wrote outside the disposable audit')
    if (AUDIT / 'record_check.py').read_bytes() != source:
        raise SystemExit('actual logger bytes changed')
    print(json.dumps(dict(status='triggered and holds', scope='disposable logger controls only',
                          logger_sha256=hashlib.sha256(source).hexdigest(), cases=cases), sort_keys=True))

if __name__ == '__main__':
    main()
