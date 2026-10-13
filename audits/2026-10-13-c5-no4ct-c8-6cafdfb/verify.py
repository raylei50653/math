#!/usr/bin/env python3
"""Read-only standard-library replay of the no-4CT C8 dependency integration."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True


def check_inputs(folder):
    entries = json.loads((folder / 'INPUTS.json').read_text())['files']
    assert len({e['frozen'] for e in entries}) == len(entries)
    for e in entries:
        data = (folder / e['frozen']).read_bytes()
        assert len(data) == e['bytes'], e['frozen']
        assert hashlib.sha256(data).hexdigest() == e['sha256'], e['frozen']
    return len(entries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    custody = {name: check_inputs(HERE / name) for name in ('.', 'geometry')}
    commands = [
        ('three-target-full-interface', 'finite/check.py', ['--check']),
        ('independent-full-interface', 'review/check.py',
         ['--producer', str(HERE / 'finite/certificate.json')]),
        ('source-geometry-and-quotient-interface',
         'frozen/audits/2026-10-13-c8-struct-243a125/check.py', []),
        ('same-source-consumer-binding', 'integrate.py', ['--check']),
        ('apex-degree', 'frozen/audits/2026-10-13-c8-apex-degree-45bc1c3/check.py', ['--check']),
        ('m9-full-fibres', 'frozen/audits/2026-10-13-c8-followup-6cafdfb/check.py', ['--check']),
        ('m10-full-fibres', 'frozen/audits/2026-10-13-c8-peeling-6cafdfb/check.py', ['--check']),
    ]
    checks = []
    for name, path, flags in commands:
        if args.negative:
            if name == 'three-target-full-interface':
                flags += ['--negative-controls']
            elif name in {'same-source-consumer-binding', 'm9-full-fibres', 'm10-full-fibres'}:
                flags += ['--negative']
        result = subprocess.run([sys.executable, '-B', str(HERE / path), *flags],
                                capture_output=True, text=True)
        if result.returncode:
            sys.stderr.write(result.stdout + result.stderr)
            raise RuntimeError(name + ' failed')
        checks.append({'name': name, 'stdout': result.stdout.strip()})
    print(json.dumps(dict(status='PASS', frozen_inputs=custody, checks=checks,
                          h3_queries=105, excluded=97, necessary_residuals=8,
                          no4ct_932_bounds={'h': 4, 'n5': 10},
                          h3_k_lower_bound=19, actual_source_status='not triggered',
                          unbounded_three_branches='OPEN', general_theorem='OPEN'),
                     sort_keys=True))


if __name__ == '__main__':
    main()
