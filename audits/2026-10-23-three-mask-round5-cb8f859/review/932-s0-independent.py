#!/usr/bin/env python3
"""Q-first complete fixed zero-single-contact annulus relation.

Enumerates only the original fixed C9--Q9 annulus, not interior graphs.
Every C lift of the same complete J colouring is retained. Whole-Kempe options
are read from the sealed original C9 authority, with the same ordered row list.
"""
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SOURCE = REPO / ('audits/2026-10-13-c9-932-source-d521163/frozen/'
                 'audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz')


def canonical(word):
    rename = {}
    return tuple(rename.setdefault(c, len(rename)) for c in word)


def words(prefix=(0,)):
    if len(prefix) == 9:
        if prefix[-1] != prefix[0]:
            yield prefix
        return
    for c in range(min(4, max(prefix) + 2)):
        if c != prefix[-1]:
            yield from words(prefix + (c,))


def bits(mask):
    while mask:
        one = mask & -mask
        yield one.bit_length() - 1
        mask -= one


def main():
    source = json.loads(gzip.decompress(SOURCE.read_bytes()))
    rows = list(words())
    if rows != [tuple(r) for r in source['inner_pattern_order']]:
        raise ValueError('original ordered C9 row domain mismatch')
    index = {word: i for i, word in enumerate(rows)}
    lifts = []
    images = []
    for q in rows:
        lists = [tuple(c for c in range(4) if c not in {q[i-1], q[i]}) for i in range(9)]
        full = [list(c) for c in product(*lists)
                if all(c[i] != c[(i+1) % 9] for i in range(9))]
        lifts.append(full)
        images.append({index[canonical(c)] for c in full})
    results = []
    for case in source['queries']:
        if case['target'] != 932 or case['geometry_id'] != 'induced' or case['status'] != 'necessary_condition_residual':
            continue
        allowed = {j for j, image in enumerate(images)
                   if all(case['fixed_point'] >> c & 1 for c in image)}
        initial = sorted(allowed)
        batches = []
        while allowed:
            removed = [j for j in sorted(allowed)
                       if any(not any(set(bits(orbit)) <= allowed for orbit in opts)
                              for opts in source['kempe_obligations'][j])]
            if not removed:
                break
            batches.append(removed)
            allowed.difference_update(removed)
        results.append({'query_id': case['query_id'], 'initial_Q_ids': initial,
                        'deletion_batches': batches, 'final_Q_ids': sorted(allowed),
                        's0_excluded_by_this_test': not allowed})
    if len(results) != 20:
        raise ValueError('wrong named collar domain')
    print(json.dumps({'status': 'PASS', 'method': 'Q-first literal lists and all C lifts',
                      'ordered_Q_rows': len(rows), 'full_annulus_lifts': sum(map(len, lifts)),
                      'empty_annulus_Q_fibres': sum(not r for r in lifts),
                      'literal_lift_list_sha256': hashlib.sha256(json.dumps(lifts, separators=(',', ':')).encode()).hexdigest(),
                      'complete_Q_to_C_images': [sorted(i) for i in images],
                      'case_results': results,
                      'all_s0_cases_excluded_by_this_test': all(r['s0_excluded_by_this_test'] for r in results),
                      'general_932_excluded': False, 'source_realized': False}, sort_keys=True))


if __name__ == '__main__':
    main()
