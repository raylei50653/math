#!/usr/bin/env python3
"""Reproduce targeted corruptions in memory; never change the real certificate.

Calls the identical validation function used by checker.py --check.
--write exclusively creates NEGATIVE_CONTROLS.json; --check compares read-only.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
CERT = ROOT / 'controls/certificate.json'
OUT = ROOT / 'NEGATIVE_CONTROLS.json'


def run():
    spec = importlib.util.spec_from_file_location('cap_checker', ROOT / 'controls/checker.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    source_bytes = CERT.read_bytes()
    cert = json.loads(source_bytes)
    records = []

    def corrupt(name, target, key, replacement, diagnostic):
        old = target[key]
        target[key] = replacement
        try:
            checker.make_certificate(expected=cert)
        except ValueError as error:
            message = str(error)
            if diagnostic not in message:
                raise AssertionError((name, message, diagnostic)) from error
            records.append({'case': name, 'expected_diagnostic': diagnostic,
                            'actual_diagnostic': message,
                            'status': 'triggered and holds', 'corruption_rejected': True})
        else:
            raise AssertionError('corrupted certificate accepted: ' + name)
        finally:
            target[key] = old

    corrupt('missing ordered pair', cert, 'pairs', cert['pairs'][:-1], 'complete pair array')
    pair = cert['pairs'][0]
    corrupt('missing boundary row including its empty/nonempty fibre', pair, 'rows',
            pair['rows'][:-1], 'complete ten joint rows')
    corrupt('incorrect named pair label', pair, 'P_mask', -1, 'pair labels/order')
    row = next(row for row in pair['rows'] if row['literal_full_witness'])
    lift = row['literal_full_witness'][:]
    lift[8] = lift[0]  # center v now has the same color as actual neighbor a
    corrupt('invalid full lift on original spoke va', row, 'literal_full_witness',
            lift, 'pair certificate differs')
    rotation = [r[:] for r in pair['graph']['rotation_edge_ids']]
    rotation[8][0], rotation[8][1] = rotation[8][1], rotation[8][0]
    corrupt('incorrect central rotation', pair['graph'], 'rotation_edge_ids',
            rotation, 'pair certificate differs')
    cap = cert['caps'][0]
    fibres = [r[:] for r in cap['actual_boundary_full_private_fibres']]
    index = next(i for i, values in enumerate(fibres) if values)
    fibres[index] = fibres[index][1:]
    corrupt('omitted literal cap full lift', cap, 'actual_boundary_full_private_fibres',
            fibres, 'cap certificate differs')
    assert CERT.read_bytes() == source_bytes
    return {'schema': 'task-c-negative-controls-v1',
            'certificate_sha256': hashlib.sha256(source_bytes).hexdigest(),
            'checker_sha256': hashlib.sha256((ROOT / 'controls/checker.py').read_bytes()).hexdigest(),
            'method': 'same make_certificate(expected=...) validator as CLI --check',
            'cases': records, 'certificate_unchanged': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    if args.write:
        with OUT.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    else:
        assert json.loads(OUT.read_text()) == result
    print('PASS: six targeted corruptions rejected; real certificate unchanged')
