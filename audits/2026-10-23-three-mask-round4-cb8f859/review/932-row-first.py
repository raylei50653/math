#!/usr/bin/env python3
"""Row-first independent folded support elimination using sealed Kempe options.

Rebuilds each grid from all original C9 rows and common S4 images. It does not
import the fourth-round producer or its grids/deletion transcript. The complete
Kempe options and initial necessary supports come from the original sealed C9
authority, not from a newly chosen palette witness.
"""
import gzip
import hashlib
from itertools import permutations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SOURCE = REPO / ('audits/2026-10-13-c9-932-source-d521163/frozen/'
                 'audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz')
PERM = tuple(permutations(range(4)))


def bits(mask):
    while mask:
        one = mask & -mask
        yield one.bit_length() - 1
        mask -= one


def rebuild_grids(rows, site):
    grouped = [{}, {}]
    for idx, row in enumerate(rows):
        a, b = row[site], row[(site + 4) % 9]
        equal = a == b
        beta = 0 if equal else 1
        images = [tuple(p[c] for c in row[site:] + row[:site]) for p in PERM
                  if p[a] == 0 and p[b] == beta]
        short = min(image[1:4] for image in images)
        long = min(image[5:9] for image in images)
        key = (short, long)
        group = grouped[int(equal)]
        group[key] = group.get(key, 0) | (1 << idx)
    result = []
    for equal, groups in enumerate(grouped):
        us = sorted({u for u, v in groups})
        vs = sorted({v for u, v in groups})
        if len(groups) != len(us) * len(vs):
            raise ValueError('incomplete folded grid')
        expected = (4, 10, 210) if equal else (10, 31, 610)
        if (len(us), len(vs), sum(m.bit_count() for m in groups.values())) != expected:
            raise ValueError('wrong complete original row coverage')
        cells = [[groups[u, v] for v in vs] for u in us]
        coords = {i: (a, b) for a, line in enumerate(cells)
                  for b, mask in enumerate(line) for i in bits(mask)}
        result.append((cells, coords))
    if set(result[0][1]) & set(result[1][1]) or len(result[0][1]) + len(result[1][1]) != 820:
        raise ValueError('original row domain is not a disjoint complete cover')
    return result


def orbit_obstructed(orbit, support, grids):
    for cells, coords in grids:
        present = [coords[p] for p in bits(orbit) if p in coords]
        us = {a for a, b in present}
        vs = {b for a, b in present}
        if any(cells[a][b] & support == 0 for a in us for b in vs):
            return True
    return False


def main():
    source = json.loads(gzip.decompress(SOURCE.read_bytes()))
    rows = source['inner_pattern_order']
    grids = [rebuild_grids(rows, site) for site in range(9)]
    queries = [q for q in source['queries'] if q['target'] == 932
               and q['geometry_id'] == 'induced' and q['status'] == 'necessary_condition_residual']
    options = source['kempe_obligations']
    results = []
    for query in queries:
        for site in range(9):
            support = query['fixed_point']
            batches = []
            while support:
                removed = 0
                for p in bits(support):
                    for split_options in options[p]:
                        if not any(orbit & ~support == 0
                                   and not orbit_obstructed(orbit, support, grids[site])
                                   for orbit in split_options):
                            removed |= 1 << p
                            break
                if not removed:
                    raise ValueError('nonempty survivor: ' + query['query_id'] + '/' + str(site))
                batches.append(removed.bit_count())
                support &= ~removed
            results.append({'query_id': query['query_id'], 'site': site,
                            'initial': query['fixed_point'].bit_count(),
                            'rounds': batches, 'final': 0})
    if len(results) != 180:
        raise ValueError('wrong named case domain')
    print(json.dumps({'status': 'PASS', 'named_cases': len(results),
                      'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                      'uses_upstream_complete_kempe_options': True,
                      'grid_method': 'original-C9-row-first common S4 images',
                      'results': results}, sort_keys=True))


if __name__ == '__main__':
    main()
