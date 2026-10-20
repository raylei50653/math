#!/usr/bin/env python3
"""Independent original-hexagon full-lift replay; no source enumeration."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARSER = argparse.ArgumentParser()
PARSER.add_argument('--check', action='store_true')
PARSER.add_argument('--certificate', type=Path)
ARGS = PARSER.parse_args()
for item in json.loads((ROOT / 'INPUTS.json').read_text())['files']:
    assert hashlib.sha256((ROOT / 'frozen' / item['path']).read_bytes()).hexdigest() == item['sha256']

# Rim indexing a,b,q,L,R,n; private vertices p=6,h=7.
RIM = [(i, (i + 1) % 6) for i in range(6)]
OLD = RIM + [(6, i) for i in (0, 1, 2, 5, 7)] + [(7, i) for i in (2, 3, 4, 5)]
FAN = {'a': RIM + [(0, i) for i in (2, 3, 4)],
       'b': RIM + [(1, i) for i in (3, 4, 5)]}
QUERIES = ['01021', '01202', '01212']

def proper(c, edges):
    return all(c[u] != c[v] for u, v in edges)

def old_lifts(c):
    # Direct edge-based enumeration is independent of the set formula below.
    return [(p, h) for p, h in itertools.product(range(4), repeat=2)
            if proper(c + (p, h), OLD)]

records = []
generic_cover = 0
counts = {name: {'proper': 0, 'empty_lifts': 0, 'nonempty_lifts': 0} for name in FAN}
for c in itertools.product(range(4), repeat=6):
    if not proper(c, RIM):
        continue
    a, b, q, left, right, n = c
    lifts = old_lifts(c)
    formula = [(p, h) for p, h in itertools.product(range(4), repeat=2)
               if p not in {a, b, q, n} and h not in {q, n, left, right, p}]
    assert lifts == formula
    if len({a, b, q}) == 3:
        for p, h in lifts:
            assert h in {a, b}
            assert proper(c, FAN['a' if h == a else 'b'])
            generic_cover += 1
    for name, edges in FAN.items():
        if not proper(c, edges):
            continue
        counts[name]['proper'] += 1
        counts[name]['nonempty_lifts' if lifts else 'empty_lifts'] += 1
        assert bool(lifts) == (len({a, b, q, n}) <= 3)
        if lifts:
            centre = a if name == 'a' else b
            chosen_p = min(set(range(4)) - {a, b, q, n})
            assert (chosen_p, centre) in lifts
        records.append({'fan': name, 'rim': c, 'lifts': lifts})

# Every accepted full original cap witness chooses one fixed smaller fan.
accepted = []
for c in itertools.product(range(4), repeat=6):
    a, b, q, left, right, n = c
    if a != 2 or b != 3 or q in {2, 3}:
        continue
    for p, h in old_lifts(c):
        assert {p, q} == {0, 1}
        assert h in {a, b}
        fan = 'a' if h == a else 'b'
        assert proper(c, FAN[fan])
        accepted.append({'rim': c, 'p': p, 'h': h, 'fan': fan})
assert accepted and {r['fan'] for r in accepted} == {'a', 'b'}

# Full local rejected contexts include the original edges q-b and q-c.
negative = []
for word in QUERIES:
    _, _, a, b, outer_c = map(int, word)
    for name, edges in FAN.items():
        bad = []
        for c in itertools.product(range(4), repeat=6):
            if c[0] != a or c[1] != b or c[2] in {b, outer_c}:
                continue
            if proper(c, edges) and not old_lifts(c):
                bad.append(c)
        assert bad, (word, name)
        negative.append({'query': word, 'fan': name, 'count': len(bad), 'example': bad[0]})

# Negative control: omitting the n constraint would wrongly call each leak liftable.
for item in negative:
    a, b, q, left, right, n = item['example']
    assert set(range(4)) - {a, b, q}
    assert not (set(range(4)) - {a, b, q, n})

# Whole embedded control, constructed independently with named vertices.
VERTICES = tuple('xyabc') + ('q', 'L', 'R', 'n', 'p', 'h', 'r')
OUTER = tuple('xyabc')
NAMED_RIM = ('a', 'b', 'q', 'L', 'R', 'n')
def edge(u, v):
    return tuple(sorted((u, v)))
def cycle_edges(vs):
    return {edge(vs[i], vs[(i+1) % len(vs)]) for i in range(len(vs))}
original = cycle_edges(OUTER) | cycle_edges(NAMED_RIM)
original |= {edge('p', v) for v in ('a', 'b', 'q', 'n', 'h')}
original |= {edge('h', v) for v in ('q', 'L', 'R', 'n')}
original |= {edge('q', 'c')}
wheel = ('a', 'n', 'R', 'L', 'q', 'c', 'x', 'y')
original |= {edge('r', v) for v in wheel}
faces = [('p','a','b'), ('p','b','q'), ('p','q','h'), ('p','h','n'),
         ('p','n','a'), ('h','q','L'), ('h','L','R'), ('h','R','n'),
         ('b','c','q')]
faces += [('r', wheel[i], wheel[(i+1) % len(wheel)]) for i in range(len(wheel))]
incidences = {}
for face in faces:
    for i in range(3):
        uv = (face[i], face[(i+1) % 3])
        incidences.setdefault(edge(*uv), []).append(uv)
assert set(incidences) == original
for uv, directed in incidences.items():
    if uv in cycle_edges(OUTER):
        assert len(directed) == 1
    else:
        assert len(directed) == 2 and directed[0] == directed[1][::-1]
assert len(VERTICES) - len(original) + len(faces) == 1
assert len(original) == 28 and len(faces) == 17
assert {e for e in original if set(e) <= set(OUTER)} == cycle_edges(OUTER)
for v in ('p','h'):
    assert sum(v in e for e in original) == 5
assert sum('b' in e for e in original) == 4
reduced_vertices = tuple(v for v in VERTICES if v not in {'p', 'h'})
def construct(root):
    es = {e for e in original if not (set(e) & {'p', 'h'})}
    destinations = ('q', 'L', 'R') if root == 'a' else ('n', 'L', 'R')
    return es | {edge(root, v) for v in destinations}
graphs = {'G': (VERTICES, original),
          'G_a': (reduced_vertices, construct('a')),
          'G_b': (reduced_vertices, construct('b'))}
rows = ['01012','01021','01023','01201','01202','01203','01212','01213','01231','01232']
def fibres(vertices, es, word):
    adj = {v: set() for v in vertices}
    for u, v in es:
        adj[u].add(v); adj[v].add(u)
    colouring = dict(zip(OUTER, map(int, word)))
    result = []
    def visit():
        remaining = [v for v in vertices if v not in colouring]
        if not remaining:
            result.append(tuple(colouring[v] for v in vertices))
            return
        allowed = {v: set(range(4)) - {colouring[w] for w in adj[v] if w in colouring}
                   for v in remaining}
        v = min(remaining, key=lambda u: (len(allowed[u]), -len(adj[u]), u))
        for colour in sorted(allowed[v]):
            colouring[v] = colour
            visit()
            del colouring[v]
    visit()
    return sorted(result)
whole = {}
for name, (vertices, es) in graphs.items():
    fs = [fibres(vertices, es, word) for word in rows]
    counts_full = list(map(len, fs))
    mask = sum(1 << i for i, count in enumerate(counts_full) if count)
    whole[name] = {'vertices': vertices, 'edges': sorted(es), 'inner_vertices': len(vertices)-5,
                   'counts': counts_full, 'mask': mask,
                   'fibres_sha256': [hashlib.sha256(json.dumps(f).encode()).hexdigest() for f in fs]}
    if name != 'G':
        for i, f in enumerate(fs):
            original_fibre = set(fibres(VERTICES, original, rows[i]))
            for colours in f:
                assignment = dict(zip(vertices, colours))
                c = tuple(assignment[v] for v in NAMED_RIM)
                extensions = set()
                for pc, hc in old_lifts(c):
                    lifted = dict(assignment, p=pc, h=hc)
                    extensions.add(tuple(lifted[v] for v in VERTICES))
                expected = {g for g in original_fibre
                            if all(g[VERTICES.index(v)] == assignment[v] for v in vertices)}
                assert extensions == expected
assert [whole[n]['mask'] for n in graphs] == [863, 854, 783]
assert whole['G']['counts'] == [5,13,8,5,1,0,1,0,8,4]
assert whole['G_a']['counts'] == [0,1,1,0,1,0,1,0,1,2]
assert whole['G_b']['counts'] == [1,12,11,1,0,0,0,0,11,10]
assert all(whole[n]['counts'][9] > 0 for n in graphs)

RESULT = {'counts': counts, 'full_fibres': records, 'accepted_branch_cover': accepted,
          'generic_branch_cover_witnesses': generic_cover,
          'negative_controls': negative, 'target_source_realized': False,
          'whole_graph_control': whole, 'whole_graph_oriented_faces': faces,
          'smaller_bad_source_proved': False,
          'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
normalized = json.loads(json.dumps(RESULT))
output = ARGS.certificate or ROOT / 'certificate.json'
if ARGS.check:
    assert json.loads(output.read_text()) == normalized, 'certificate differs'
else:
    with output.open('x') as stream:
        stream.write(json.dumps(RESULT, indent=2) + '\n')
print(json.dumps({'ok': True, 'counts': counts,
                  'accepted_witnesses': len(accepted), 'negative_controls': len(negative),
                  'target_source_realized': False, 'smaller_bad_source_proved': False}))
