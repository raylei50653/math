"""Simultaneous exterior equality chords, inequality chords, and face hubs.

This is a bounded grammar, NOT all budget-admissible quotient gadgets.
All names and literal colors are shared; no independently normalized joins.
"""
import argparse
import gzip
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def normalize(p):
    d = {}
    return tuple(d.setdefault(x, len(d)) for x in p)


def dissections(n):
    diagonals = [(i, j) for i in range(n) for j in range(i+2, n)
                 if (i, j) != (0, n-1)]
    def walk(i, chosen):
        if i == len(diagonals):
            yield tuple(chosen)
            return
        yield from walk(i+1, chosen)
        a, b = diagonals[i]
        if all(not (a < c < b < d or c < a < d < b) for c, d in chosen):
            yield from walk(i+1, chosen+[(a, b)])
    yield from walk(0, [])


def split_faces(chords):
    faces = [tuple(range(8))]
    for a, b in chords:
        for i, face in enumerate(faces):
            if a in face and b in face:
                x, y = sorted((face.index(a), face.index(b)))
                if y-x not in (1, len(face)-1):
                    faces[i:i+1] = [face[x:y+1], face[y:]+face[:x+1]]
                    break
        else:
            raise AssertionError('missing chord face')
    return faces


def build():
    rows = json.loads((ROOT/'frozen/audits/2026-10-13-c8-joint-count-3097ef5/interface.json').read_text())['pattern_order']
    assert rows == [list(p) for p in sorted({normalize(p) for p in itertools.product(range(4), repeat=8)
                                           if all(p[i] != p[(i+1)%8] for i in range(8))})]
    queries = [q for q in json.loads((ROOT/'frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json').read_text())['queries'] if q['status'] == 'necessary_condition_residual']
    histogram = Counter()
    minima = {q['query_id']: 275 for q in queries}
    witnesses = {}
    seen_relations = set()
    total = 0
    valid = 0
    gadgets = []
    for chords in dissections(8):
        faces = split_faces(chords)
        eligible = [f for f in faces if len(f) >= 4]
        for eq_bits in range(1 << len(chords)):
            eq = [e for i, e in enumerate(chords) if eq_bits >> i & 1]
            diff = [e for i, e in enumerate(chords) if not eq_bits >> i & 1]
            parent = list(range(8))
            def find(i):
                while parent[i] != i:
                    i = parent[i]
                return i
            for a, b in eq:
                parent[find(a)] = find(b)
            # Equality scaffold is contracted; each true inequality must survive.
            inequality = [(i, (i+1)%8) for i in range(8)]+diff
            loop = any(find(a) == find(b) for a, b in inequality)
            d = 8-len({find(i) for i in range(8)})
            for bits in range(1 << len(eligible)):
                total += 1
                if loop:
                    continue
                hubs = [f for j, f in enumerate(eligible) if bits >> j & 1]
                assert len(hubs)-d <= 5
                valid += 1
                histogram[(len(hubs), d)] += 1
                lifts = []
                for p in rows:
                    if any(p[a] != p[b] for a, b in eq) or any(p[a] == p[b] for a, b in diff):
                        lifts.append([])
                    else:
                        opts = [[c for c in range(4) if all(p[v] != c for v in f)] for f in hubs]
                        lifts.append([list(t) for t in itertools.product(*opts)])
                relation = sum(1 << i for i, f in enumerate(lifts) if f)
                assert relation, 'loopless exterior quotient unexpectedly uncolorable'
                seen_relations.add(relation)
                entry = dict(id=len(gadgets), boundary_order=list(range(8)),
                    chords=chords, equality_chords=eq, inequality_chords=diff,
                    dissection_faces=faces, hub_faces=hubs,
                    identification_reduction=d, added_vertices=len(hubs),
                    relation=relation, full_hub_lifts_by_literal_row=lifts)
                gadgets.append(entry)
                for q in queries:
                    count = (relation & q['support']).bit_count()
                    if count < minima[q['query_id']]:
                        minima[q['query_id']] = count
                        witnesses[q['query_id']] = dict(gadget_id=entry['id'],
                            intersection_rows=[i for i in range(274) if relation & q['support'] & (1 << i)])
    return dict(schema='c8-signed-chords-face-hubs-v2', boundary_rows=rows,
        summary=dict(total=total, valid=valid, invalid_inequality_loop=total-valid,
                     distinct_relations=len(seen_relations),
                     histogram={f'h{h}-d{d}':v for (h,d),v in sorted(histogram.items())},
                     minimum_intersections=minima,
                     newly_excluded=[k for k,v in minima.items() if v == 0]),
        witnesses=witnesses, gadgets=gadgets)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = build()
    target = HERE/'certificate.v2.json.gz'
    payload = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()+b'\n'
    if args.write:
        with target.open('xb') as f:
            f.write(gzip.compress(payload, mtime=0))
    else:
        assert json.loads(gzip.decompress(target.read_bytes())) == json.loads(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
