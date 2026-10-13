#!/usr/bin/env python3
"""Retain original certificate; reject deliberately incomplete named evidence."""
import copy
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent.parent
original = json.loads(gzip.decompress((HERE / 'certificate.json.gz').read_bytes()))
results = []
with tempfile.TemporaryDirectory(prefix='math-k15-negative-') as temp:
    temp = Path(temp)
    for label in ['omit_lift', 'invent_empty_fibre', 'omit_row', 'omit_root', 'wrong_edge', 'wrong_pin', 'wrong_rotation']:
        data = copy.deepcopy(original)
        record = data['records'][0]
        if label == 'omit_lift':
            record['rows'][0]['lifts'].pop()
            record['rows'][0]['count'] -= 1
        elif label == 'invent_empty_fibre':
            record['rows'][0]['lifts'] = []
            record['rows'][0]['count'] = 0
        elif label == 'omit_row':
            record['rows'].pop()
        elif label == 'omit_root':
            data['records'].pop(0)
        elif label == 'wrong_edge':
            record['edges'].pop()
        elif label == 'wrong_pin':
            record['canonical_to_original'][0], record['canonical_to_original'][1] = record['canonical_to_original'][1], record['canonical_to_original'][0]
        elif label == 'wrong_rotation':
            record['rotation'][0][0], record['rotation'][0][1] = record['rotation'][0][1], record['rotation'][0][0]
        path = temp / (label + '.json.gz')
        path.write_bytes(gzip.compress(json.dumps(data).encode(), mtime=0))
        result = subprocess.run([sys.executable, '-B', str(HERE / 'independent/compare.py'), '--certificate', str(path)], capture_output=True, text=True)
        assert result.returncode != 0, 'accepted corruption: ' + label
        assert any(t in result.stderr for t in ['AssertionError', 'ValueError', 'KeyError']), result.stderr
        results.append({'case': label, 'validator': 'independent', 'rejected': True})
        if label == 'omit_lift':
            result = subprocess.run([sys.executable, '-B', str(HERE / 'check.py'), '--check', '--certificate', str(path)], capture_output=True, text=True)
            assert result.returncode != 0 and 'certificate mismatch' in result.stderr, result.stderr
            results.append({'case': label, 'validator': 'primary', 'rejected': True})
print(json.dumps({'negative_controls': results, 'original_unchanged': True}, sort_keys=True))
