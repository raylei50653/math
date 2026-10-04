"""D5 B4 audit-only helpers, adapted from immutable D4 B3 independent_core.

No production imports. D5 adds independent full coloring witnesses.
"""
from collections import Counter
from itertools import combinations, permutations, product
B=set(range(5))
U=set(range(4))
COUNTS=Counter()

def edge(v, w):
    assert v != w
    return tuple(sorted((v, w)))


FRAME = {edge(h, (h + 1) % 5) for h in B}


def edges(values):
    result = [edge(*e) for e in values]
    assert len(result) == len(set(result)), 'duplicate serialized edge'
    return set(result)


def unique(values):
    assert len(values) == len(set(values)), 'duplicate serialized array member'
    return set(values)


def normalize(values):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in values)


def powerset(values):
    vs = sorted(values)
    return [tuple(t) for n in range(len(vs) + 1) for t in combinations(vs, n)]


def connected(vs, es):
    vs = set(vs)
    if not vs:
        return False
    reached = {min(vs)}
    while True:
        more = reached | {w for v, w in es if v in reached and w in vs}
        more |= {v for v, w in es if w in reached and v in vs}
        if reached == more:
            return reached == vs
        reached = more


def solve_witnesses(vs, es, beta, ports, pinned=None):
    """Fresh MRV enumeration; fixed colors stay in one literal frame."""
    vs = set(vs)
    assert B <= vs and all({v, w} <= vs for v, w in es)
    adj = {v: set() for v in vs}
    for v, w in es:
        adj[v].add(w)
        adj[w].add(v)
    f = dict(enumerate(beta))
    for v, c in (pinned or {}).items():
        if v in f and f[v] != c:
            return {}
        f[v] = c
    assert set(f) <= vs
    if any(f[v] == f[w] for v, w in es if v in f and w in f):
        return {}
    remaining = vs - set(f)
    result = {}
    order = sorted(vs)

    def visit():
        if not remaining:
            result.setdefault(tuple(f[v] for v in ports), [f[v] for v in order])
            return
        domains = {v: U - {f[w] for w in adj[v] if w in f} for v in remaining}
        v = min(remaining, key=lambda z: (len(domains[z]), -len(adj[z]), z))
        if not domains[v]:
            return
        remaining.remove(v)
        for c in sorted(domains[v]):
            f[v] = c
            visit()
        f.pop(v)
        remaining.add(v)

    visit()
    return result


def solve(vs, es, beta, ports, pinned=None):
    return set(solve_witnesses(vs, es, beta, ports, pinned))


def witness(order, values, es, beta, ports, t):
    assert len(order) == len(values) and len(unique(order)) == len(order)
    f = dict(zip(order, values, strict=True))
    assert all(c in U for c in f.values())
    assert all(f[h] == beta[h] for h in B)
    assert all(f[v] != f[w] for v, w in es)
    assert tuple(f[v] for v in ports) == tuple(t)
    return f


def stored_relation(items, order, es, beta, ports, count_key):
    ts = [tuple(x['tuple']) for x in items]
    unique(ts)
    for item in items:
        witness(order, item['coloring'], es, beta, ports, item['tuple'])
        COUNTS[count_key] += 1
    return set(ts)


def rotation_faces(rotation, es, require_sphere=True):
    vs = {v for e in es for v in e}
    assert set(rotation) == vs
    for v, ring in rotation.items():
        assert len(unique(ring)) == len(ring)
        assert set(ring) == {w if z == v else z for z, w in es if v in (z, w)}
    darts = {(v, w) for v, w in es} | {(w, v) for v, w in es}
    visited, result = set(), []
    for start in sorted(darts):
        if start in visited:
            continue
        dart, face = start, []
        while dart not in visited:
            visited.add(dart)
            v, w = dart
            face.append(v)
            ring = rotation[w]
            dart = (w, ring[(ring.index(v) - 1) % len(ring)])
        assert dart == start
        result.append(face)
    assert visited == darts
    if require_sphere:
        assert len(vs) - len(es) + len(result) == 2
    return result


def rotation_key(rot):
    result = []
    for v, ring in sorted(rot.items()):
        i = ring.index(min(ring))
        result.append((v, tuple(ring[i:] + ring[:i])))
    return tuple(result)


def exhaustive_disk_rotations(es):
    vs = sorted({v for e in es for v in e})
    choices = []
    for v in vs:
        ns = sorted(w if z == v else z for z, w in es if v in (z, w))
        choices.append([[ns[0], *p] for p in permutations(ns[1:])])
    all_keys, n = set(), 0
    for rings in product(*choices):
        n += 1
        rot = dict(zip(vs, rings, strict=True))
        fs = rotation_faces(rot, es, require_sphere=False)
        if len(vs) - len(es) + len(fs) != 2:
            continue
        outers = [f for f in fs if len(f) == 5 and set(f) == B]
        if len(outers) == 1:
            all_keys.add(rotation_key(rot))
    return n, all_keys


def transport(beta, move):
    moved = [None] * 5
    for h in B:
        moved[move[h]] = beta[h]
    target = normalize(moved)
    cp = dict(zip(moved, target))
    cp.update(zip(sorted(U - set(cp)), sorted(U - set(cp.values()))))
    perm = [cp[c] for c in range(4)]
    assert sorted(perm) == list(range(4))
    assert all(target[move[h]] == perm[beta[h]] for h in B)
    return target, perm


def renamed_rotation(rot, rename):
    return {rename(v): [rename(w) for w in ring] for v, ring in rot.items()}


def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk(value)
