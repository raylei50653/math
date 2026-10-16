#!/usr/bin/env python3
"""Compare the new J predicate with the frozen original all-r transfer table."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ORIGINAL = ROOT / 'audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/transfer.json'


def check():
    original = json.loads(ORIGINAL.read_text())
    new = json.loads((HERE / 'full-j-certificate.json').read_text())
    table = {r['boundary']: set(r['ordered_pq']) for r in original['table']}
    counts = {}
    for record in new['proper_rows']:
        m, v, w, z, p, q = record['literal_row']
        boundary = (z, m, v, w, m)
        colours = list(dict.fromkeys(boundary))
        colours += [c for c in range(4) if c not in colours]
        frame = {c: 'ABCD'[i] for i, c in enumerate(colours)}
        key = ''.join(frame[c] for c in boundary)
        pair = frame[p] + frame[q]
        accepted = pair in table[key]
        assert accepted == record['source_allowed']
        counts.setdefault(key, {'proper': 0, 'allowed': 0})
        counts[key]['proper'] += 1
        counts[key]['allowed'] += accepted
    assert sum(v['proper'] for v in counts.values()) == 432
    assert sum(v['allowed'] for v in counts.values()) == 240
    return {'status': 'PASS', 'literal_rows_checked': 432, 'allowed': 240,
            'by_original_frame': counts,
            'original_path': str(ORIGINAL.relative_to(ROOT)),
            'original_sha256': hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),
            'new_certificate_sha256': hashlib.sha256((HERE / 'full-j-certificate.json').read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True))
