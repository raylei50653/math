#!/usr/bin/env python3
"""Create this audit's exclusive receipt or verify it read-only."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXCLUDED = {
    'delivery.json': 'Self-referential receipt metadata; excluded from its own payload hash list.',
    'delivery-verification.json': 'Post-seal verification receipt metadata.',
    'logs/delivery-create.command.json': 'Receipt-generation command metadata written after the receipt.',
    'logs/delivery-create.stdout.log': 'Receipt-generation stdout metadata written after the receipt.',
    'logs/delivery-create.stderr.log': 'Receipt-generation stderr metadata written after the receipt.',
    'logs/delivery-verify.command.json': 'Post-seal verification command metadata.',
    'logs/delivery-verify.stdout.log': 'Post-seal verification stdout metadata.',
    'logs/delivery-verify.stderr.log': 'Post-seal verification stderr metadata.',
}


def encode(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()


def inventory():
    return [{'path': str(p.relative_to(HERE)), 'bytes': p.stat().st_size,
             'sha256': sha256(p.read_bytes()).hexdigest()}
            for p in sorted(HERE.rglob('*')) if p.is_file() and str(p.relative_to(HERE)) not in EXCLUDED]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    payload = inventory()
    checks = json.loads((HERE / 'checks.json').read_bytes())
    if not checks['fixed_calibration_checks_pass']:
        raise ValueError('fixed calibration failed')
    value = {'task_id': 'N45-S-LONG-S-JOINT', 'base': checks['base'],
             'independent_acceptance': 'pending', 'source_status': 'not triggered',
             'scope': 'fixed finite interface calibration only', 'files': payload,
             'metadata_exclusions': [{'path': p, 'reason': reason} for p, reason in sorted(EXCLUDED.items())]}
    path = HERE / 'delivery.json'
    if args.check:
        if path.read_bytes() != encode(value):
            raise ValueError('delivery bytes, hashes or complete inventory mismatch')
    else:
        with path.open('xb') as f:
            f.write(encode(value))
    print(json.dumps({'payload_files': len(payload), 'payload_bytes': sum(z['bytes'] for z in payload),
                      'delivery_sha256': sha256(path.read_bytes()).hexdigest(),
                      'metadata_exclusion_count': len(EXCLUDED), 'independent_acceptance': 'pending',
                      'source_status': 'not triggered'}, sort_keys=True))


if __name__ == '__main__':
    main()
