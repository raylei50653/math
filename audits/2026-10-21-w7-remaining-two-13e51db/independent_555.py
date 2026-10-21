#!/usr/bin/env python3
"""Direct graph backtracking review of the complete 555 local relations."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / '2026-10-21-w7-profile1-13e51db/certificate.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def extensions(boundary, edges, count):
    neighbours = [set() for _ in range(6 + count)]
    for a, b in edges:
        require(a != b and 0 <= a < len(neighbours) and 0 <= b < len(neighbours),
                'invalid graph edge')
        neighbours[a].add(b)
        neighbours[b].add(a)
    colours = list(boundary) + [-1] * count
    if any(colours[a] == colours[b] for a, b in edges if a < 6 and b < 6):
        return []
    result = []

    def visit(vertex):
        if vertex == len(colours):
            result.append(colours[6:].copy())
            return
        forbidden = {colours[w] for w in neighbours[vertex] if colours[w] >= 0}
        for colour in range(4):
            if colour not in forbidden:
                colours[vertex] = colour
                visit(vertex + 1)
        colours[vertex] = -1

    visit(6)
    return result


def main():
    raw = SOURCE.read_bytes()
    cert = json.loads(raw)
    states = cert['states']
    source = [extensions(row, cert['source_edges'], 3) for row in states]
    require(source == cert['source_full_fibres'], 'source fibres differ')
    source_mask = sum(1 << i for i, fibre in enumerate(source) if fibre)
    require(source_mask == cert['source_relation'], 'source relation differs')
    counts = [0, 0, 0]
    minimum_extra = len(states)
    for candidate in cert['candidates']:
        count = candidate['inner_count']
        require(count in [0, 1, 2], 'not a strict smaller local candidate')
        counts[count] += 1
        mask = sum(1 << i for i, row in enumerate(states)
                   if extensions(row, candidate['edges'], count))
        require(mask == candidate['relation'], 'candidate relation differs')
        extra = (mask & ~source_mask).bit_count()
        require(extra == candidate['extra_rows'] and extra > 0, 'subset result differs')
        minimum_extra = min(minimum_extra, extra)
    require(counts == [14, 84, 504], 'candidate list incomplete')
    require(cert['source_realizability'] == 'not triggered' and
            cert['profile1_exclusion'] == 'OPEN', 'source scope promoted')
    print(json.dumps(dict(status='PASS', method='independent adjacency-list backtracking',
                         certificate_sha256=hashlib.sha256(raw).hexdigest(),
                         proper_rows=len(states), source_nonempty=source_mask.bit_count(),
                         candidate_counts=counts, minimum_extra_rows=minimum_extra,
                         arbitrary_patch_coverage='paper classification reviewed separately',
                         profile1='OPEN'), sort_keys=True))


if __name__ == '__main__':
    main()
