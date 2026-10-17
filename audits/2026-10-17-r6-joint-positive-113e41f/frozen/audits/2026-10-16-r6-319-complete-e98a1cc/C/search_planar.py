#!/usr/bin/env python3
"""Finite independent search for weak marked sphere controls; no source claim."""
import argparse
import itertools
import json
import subprocess
from pathlib import Path


def edge(u, v):
    return tuple(sorted((u, v)))


def decode(line):
    n, data = line.split()
    rot = [[ord(c) - 97 for c in word] for word in data.split(',')]
    assert len(rot) == int(n)
    edges = sorted({edge(u, v) for u, nbrs in enumerate(rot) for v in nbrs})
    faces = set()
    for u, nbrs in enumerate(rot):
        for v, w in zip(nbrs, nbrs[1:] + nbrs[:1]):
            assert w in rot[v]
            faces.add(tuple(sorted((u, v, w))))
    assert len(faces) == 2 * int(n) - 4
    return rot, edges, sorted(faces)


def colours(rot, faces):
    fixed = dict(zip(faces[0], range(3)))
    result = []
    def visit():
        if len(fixed) == len(rot):
            result.append(tuple(fixed[i] for i in range(len(rot))))
            return
        left = [i for i in range(len(rot)) if i not in fixed]
        u = max(left, key=lambda i: (len({fixed[v] for v in rot[i] if v in fixed}), len(rot[i]), -i))
        forbidden = {fixed[v] for v in rot[u] if v in fixed}
        for c in range(4):
            if c not in forbidden:
                fixed[u] = c
                visit()
        fixed.pop(u, None)
    visit()
    return result


def scan(rot, edges, faces):
    cs = colours(rot, faces)
    assert cs
    seq = {uv: tuple(c[uv[0]] ^ c[uv[1]] for c in cs) for uv in edges}
    opp = {u: [] for u in range(len(rot))}
    for face in faces:
        for u in face:
            opp[u].append(tuple(v for v in face if v != u))
    for m, z in edges:
        for m, z in ((m, z), (z, m)):
            g = edge(m, z)
            for e in opp[m]:
                if z in e:
                    continue
                equal_eg = tuple(a == b for a, b in zip(seq[e], seq[g]))
                if not any(equal_eg):
                    continue
                for f in opp[z]:
                    if len({m, z, *e, *f}) != 6:
                        continue
                    if all((a == b) == flag for a, b, flag in zip(seq[e], seq[f], equal_eg)):
                        incident = {uv: [] for uv in edges}
                        for i, face in enumerate(faces):
                            for u, v in itertools.combinations(face, 2):
                                incident[edge(u, v)].append(i)
                        blocked = set(incident[e] + incident[g])
                        adj = {i: [] for i in range(len(faces)) if i not in blocked}
                        for uv, (u, v) in incident.items():
                            if uv != f and u in adj and v in adj:
                                adj[u].append(v)
                                adj[v].append(u)
                        def pm(left):
                            if not left:
                                return []
                            u = min(left, key=lambda u: len(set(adj[u]) & left))
                            for v in adj[u]:
                                if v in left:
                                    rest = pm(left - {u, v})
                                    if rest is not None:
                                        return [(u, v)] + rest
                            return None
                        ordinary = pm(set(adj))
                        if ordinary is None:
                            continue
                        return {'rotation': rot, 'edges': edges, 'faces': faces,
                                'pins': dict(m=m, z=z, v=e[0], w=e[1], p=f[0], q=f[1]),
                                'normalized_colourings': cs,
                                'ordinary_101': ordinary, 'source': 'not triggered'}
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--plantri', required=True)
    p.add_argument('--min-n', type=int, default=6)
    p.add_argument('--max-n', type=int, default=14)
    p.add_argument('--out', required=True)
    args = p.parse_args()
    counts = []
    found = []
    for n in range(args.min_n, args.max_n + 1):
        result = subprocess.run([args.plantri, '-c4', '-a', str(n)], capture_output=True, text=True, check=True)
        count = 0
        for line in result.stdout.splitlines():
            rot, edges, faces = decode(line)
            control = scan(rot, edges, faces)
            count += 1
            if control is not None:
                found.append(control)
                print(json.dumps({'n': n, 'graphs': count, 'found': control['pins']}), flush=True)
                break
        counts.append({'n': n, 'graphs': count, 'generation_stderr': result.stderr})
        print(json.dumps({'n': n, 'graphs': count, 'controls': len(found)}), flush=True)
        if found:
            break
    Path(args.out).write_text(json.dumps({'scope': 'finite weak planar controls only', 'counts': counts, 'controls': found}, indent=2) + '\n')


if __name__ == '__main__':
    main()
