#!/usr/bin/env python3
"""Complete local C6 no-go; standard library only, no imported main checker."""
import argparse
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def certificate():
    colors = range(4)
    rows = [t for t in itertools.product(colors, repeat=6)
            if all(t[i] != t[(i + 1) % 6] for i in range(6))]
    fibres = {}
    for t in rows:
        # Full original edges: C6 and p-{0,1,2,3,q}, q-{0,3,4,5}.
        lifts = [list(t) + [p, q] for p, q in itertools.product(colors, repeat=2)
                 if p != q and all(p != t[i] for i in (0, 1, 2, 3))
                 and all(q != t[i] for i in (0, 3, 4, 5))]
        fibres[''.join(map(str, t))] = lifts
    accepted = {t for t in rows if fibres[''.join(map(str, t))]}
    chords = [(i, j) for i, j in itertools.combinations(range(6), 2)
              if j - i not in (1, 5)]
    chord_counterexamples = []
    for i, j in chords:
        t = next((t for t in rows if t in accepted and t[i] == t[j]), None)
        assert t is not None, ('unexpected sound chord', i, j)
        chord_counterexamples.append({'edge': [i, j], 'boundary': list(t),
                                     'source_lifts': fibres[''.join(map(str, t))]})
    star_counterexamples = []
    for mask in range(64):
        neighbours = [i for i in range(6) if mask >> i & 1]
        def star_accepts(t):
            return any(all(c != t[i] for i in neighbours) for c in colors)
        t = next((t for t in rows if star_accepts(t) != (t in accepted)), None)
        assert t is not None, ('unexpected equivalent star', neighbours)
        star_counterexamples.append({
            'neighbours': neighbours, 'boundary': list(t),
            'source_lifts': fibres[''.join(map(str, t))],
            'star_lifts': [list(t) + [c] for c in colors
                           if all(c != t[i] for i in neighbours)],
        })
    return {
        'schema': 'rank2-local-c6-no-one-inner-representative-v1',
        'scope': 'Full literal C6 relation only; not a no-go for full-annulus Sigma reduction.',
        'boundary_order': ['x', 'b0', 'b1', 'y', 'u1', 'u0'],
        'vertex_order': ['x', 'b0', 'b1', 'y', 'u1', 'u0', 'p', 'q'],
        'edges': sorted([sorted((i, (i + 1) % 6)) for i in range(6)]
                        + [[i, 6] for i in (0, 1, 2, 3)]
                        + [[i, 7] for i in (0, 3, 4, 5)] + [[6, 7]]),
        'proper_boundary_rows': len(rows), 'accepted_rows': len(accepted),
        'empty_rows': len(rows) - len(accepted),
        'full_lift_count': sum(map(len, fibres.values())),
        'fibres': fibres,
        'unsound_chord_witnesses': chord_counterexamples,
        'inequivalent_star_witnesses': star_counterexamples,
        'status': 'triggered and holds on the stated local patch',
        'minimal_933_941_source': 'not triggered',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    got = certificate()
    path = HERE / 'local_patch.json'
    if args.write:
        with path.open('x') as out:
            json.dump(got, out, sort_keys=True, indent=2)
            out.write('\n')
    else:
        assert json.loads(path.read_text()) == got, 'local patch certificate mismatch'
    print(json.dumps({k: got[k] for k in
                      ('proper_boundary_rows', 'accepted_rows', 'empty_rows',
                       'full_lift_count', 'status')}, sort_keys=True))


if __name__ == '__main__':
    main()
