#!/usr/bin/env python3
"""Replay local palettes and leaf minors for the arbitrary-length 3703 proof.

No sector enumeration, planarity oracle, or abstract-profile deletion.
The passage from arbitrary disk graphs to this interface is a paper proof.
"""
import argparse
from collections import deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_sector_3703_structure import ROWS, REJECT, available, edge, frame, minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_sector_3703_exclusion/observations.json'


def lists(a):
    return tuple(available(a, ROWS[i]) for i in REJECT)


def audit():
    tight = {n: [a for a in combinations(range(5), n)
                 if all(len(s) == 4-n for s in lists(a))] for n in (1, 2, 3)}
    transitions = []
    # Each state is the three singleton palettes of the incoming bridge.
    for a in tight[2]:
        for incoming in product(*[sorted(s) for s in lists(a)]):
            outgoing = tuple(next(iter(s-{p})) for s, p in zip(lists(a), incoming))
            transitions.append(dict(kind='vertex', attachments=[a], incoming=incoming,
                                    outgoing=outgoing, b0_cost=int(0 in a)))
    # x,w,y is a triangle; x,y are its two cuts and w is private.
    for a, w, b in product(tight[1], tight[2], tight[1]):
        palettes = lists(w)
        if not all(p <= x and p <= y for p, x, y in zip(palettes, lists(a), lists(b))):
            continue
        incoming = tuple(next(iter(x-p)) for x, p in zip(lists(a), palettes))
        outgoing = tuple(next(iter(y-p)) for y, p in zip(lists(b), palettes))
        # Independent coloring check across the incoming bridge and triangle.
        for i, p, q in zip(REJECT, incoming, outgoing):
            roots = {z for x, y, z in product(available(a, ROWS[i]),
                                             available(w, ROWS[i]), available(b, ROWS[i]))
                     if x != p and len({x, y, z}) == 3}
            assert roots == {q}
        transitions.append(dict(kind='triangle', attachments=[a, w, b], incoming=incoming,
                                outgoing=outgoing, b0_cost=sum(0 in s for s in (a, w, b))))
    assert len(transitions) == 89
    # Leaf 012 uses one b0 incidence. The leaf minor forbids any further b1 incidence.
    start = ((3, 3, 3), 1)
    goal = ((3, 0, 0), 2)  # Required by terminal leaf 234 and exactly two b0 spokes.
    seen = {start}
    queue = deque([start])
    steps = []
    while queue:
        incoming, count = queue.popleft()
        for index, t in enumerate(transitions):
            if t['incoming'] != incoming or any(1 in a for a in t['attachments']):
                continue
            if count + t['b0_cost'] > 2:
                continue
            target = (t['outgoing'], count + t['b0_cost'])
            steps.append(dict(source=[incoming, count], transition=index, target=target))
            if target not in seen:
                seen.add(target)
                queue.append(target)
    assert seen == {start, ((1, 1, 1), 2)} and goal not in seen
    assert len(steps) == 1
    certificates = []
    for a in [(0, 1, 2), (0, 2, 4)]:
        # t is the contracted connected branch set C-u, not a claimed degree-4 graph.
        es = frame() | {edge('u', 't')}
        es |= {edge(v, b) for v in ['u', 't'] for b in a}
        certificates.append(minor('leaf_' + ''.join(map(str, a)), es,
                                  [['u'], ['h'], ['t']] + [[b] for b in a], 'K33'))
    paths = [Path(__file__).resolve(), ROOT / 'scripts/c5_sector_3703_structure.py',
             ROOT / 'artifacts/c5_sector_3703_structure/observations.json']
    return dict(scope='Local palette closure and leaf minors; arbitrary-size lifting is in the report.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                              for p in paths}, rows=ROWS, rejected_indices=REJECT,
                transitions=transitions, reachable_states=sorted(seen), steps=steps,
                terminal_state=goal, leaf_minors=certificates,
                summary=dict(vertex_transitions=56, triangle_transitions=33,
                             reachable_states=len(seen), terminal_reachable=False,
                             saved_minors=len(certificates), profile_deletions=0,
                             fixed_point_recomputed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = audit()
    data = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
