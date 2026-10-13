#!/usr/bin/env python3
"""K15 complete rooted-sphere audit. All ten fibres, no source pruning.

Fixed-order exhaustive four-colour search; frozen plantri supplies generation.
Certificates use exclusive creation. --check is read only.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORDS = ['01012', '01021', '01023', '01201', '01202',
         '01203', '01212', '01213', '01231', '01232']


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def freeze_check():
    base = json.loads((HERE / 'BASE.json').read_text())
    for name, digest in base['sha256'].items():
        need(sha((HERE / 'frozen' / name).read_bytes()) == digest,
             'frozen input drift: ' + name)
    return base


def read_pc(path):
    data = path.read_bytes()
    header = b'>>planar_code<<'
    need(data.startswith(header), 'planar_code header')
    pos = len(header)
    result = []
    while pos < len(data):
        n = data[pos]
        pos += 1
        need(n == 21, 'sphere order must be 21')
        rotation = []
        for _ in range(n):
            end = data.index(0, pos)
            rotation.append([v - 1 for v in data[pos:end]])
            pos = end + 1
        result.append(rotation)
    return result


def cycle_key(face):
    return min(tuple(face[i:] + face[:i]) for i in range(len(face)))


def topology(rotation):
    n = len(rotation)
    for u, ns in enumerate(rotation):
        need(u not in ns and len(ns) == len(set(ns)), 'simple graph')
        need(all(0 <= v < n and u in rotation[v] for v in ns), 'reciprocal edges')
    visited = {0}
    stack = [0]
    while stack:
        for v in rotation[stack.pop()]:
            if v not in visited:
                visited.add(v)
                stack.append(v)
    need(len(visited) == n, 'connected graph')
    edges = [[u, v] for u, ns in enumerate(rotation) for v in ns if u < v]
    todo = {(u, v) for u, ns in enumerate(rotation) for v in ns}
    faces = []
    while todo:
        first = min(todo)
        dart = first
        face = []
        while True:
            need(dart in todo, 'face reuses dart')
            todo.remove(dart)
            u, v = dart
            face.append(u)
            ns = rotation[v]
            dart = (v, ns[(ns.index(u) + 1) % len(ns)])
            if dart == first:
                break
        need(len(face) == len(set(face)), 'simple face')
        faces.append(list(cycle_key(face)))
    need(n - len(edges) + len(faces) == 2, 'genus zero')
    return sorted(edges), sorted(faces)


def lifts(rotation, word):
    n = len(rotation)
    colors = list(map(int, word)) + [-1] * (n - 5)
    if any(colors[u] == colors[v] >= 0
           for u, ns in enumerate(rotation) for v in ns):
        return []
    order = sorted(range(5, n), key=lambda v: (-len(rotation[v]), v))
    result = []

    def visit(i):
        if i == len(order):
            result.append(''.join(map(str, colors)))
            return
        v = order[i]
        excluded = {colors[w] for w in rotation[v]}
        for color in range(4):
            if color not in excluded:
                colors[v] = color
                visit(i + 1)
        colors[v] = -1

    visit(0)
    return sorted(result)


def normalize(word):
    names = {}
    return ''.join(str(names.setdefault(c, len(names))) for c in word)


def frames(mapping, rows):
    result = []
    for sign in (1, -1):
        for start in range(5):
            indices = [(start + sign * i) % 5 for i in range(5)]
            permutation = [WORDS.index(normalize([p[i] for i in indices])) for p in WORDS]
            need(sorted(permutation) == list(range(10)), 'D5 row permutation')
            counts = [0] * 10
            for i, j in enumerate(permutation):
                counts[j] = rows[i]['count']
            result.append(dict(start=start, sign=sign,
                               canonical_to_original=[mapping[i] for i in indices] + mapping[5:],
                               base_to_frame_rows=permutation, counts=counts,
                               mask=sum(1 << i for i, count in enumerate(counts) if count)))
    return result


def embedded_keys(rotations):
    # Reuse the frozen K13 whole-embedding canonicalizer only for generation
    # comparison; neither topology nor colouring code uses it.
    source = HERE / 'frozen/audits/2026-10-13-k13-collar-50d5474/generation/generate.py'
    spec = importlib.util.spec_from_file_location('frozen_canonicalizer', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return [module.canonical_embedding(r) for r in rotations]


def calculate():
    base = freeze_check()
    catpath = HERE / 'frozen/artifacts/c5_cells/cells.json'
    cat = json.loads(catpath.read_text())
    need(cat['pattern_order'] == [list(map(int, p)) for p in WORDS], 'literal pattern order')
    known = set(map(int, cat['cells']))
    need(len(known) == 132, 'K132 cardinality')
    primary = read_pc(HERE / 'generation/spheres21.pc')
    secondary = read_pc(HERE / 'generation/spheres21_from_min4.pc')
    primary_keys, secondary_keys = embedded_keys(primary), embedded_keys(secondary)
    need(len(primary_keys) == len(set(primary_keys)), 'duplicate min5 embedding')
    need(len(secondary_keys) == len(set(secondary_keys)), 'duplicate min4 embedding')
    need(set(primary_keys) == set(secondary_keys), 'min4/min5 generation mismatch')
    for rot in secondary:
        es, fs = topology(rot)
        need(len(es) == 57 and len(fs) == 38 and all(len(f) == 3 for f in fs), 'secondary sphere')
        need(min(map(len, rot)) >= 5, 'secondary degree')
    records = []
    histogram = Counter()
    mask_histogram = Counter()
    total = 0
    for sid, rot in enumerate(primary):
        sphere_edges, sphere_faces = topology(rot)
        need(len(sphere_edges) == 57 and len(sphere_faces) == 38
             and all(len(f) == 3 for f in sphere_faces), 'sphere triangulation')
        need(min(map(len, rot)) >= 5, 'sphere minimum degree five')
        for z in range(21):
            if len(rot[z]) != 5:
                continue
            mapping = rot[z] + sorted(set(range(21)) - set(rot[z]) - {z})
            inverse = {v: i for i, v in enumerate(mapping)}
            rr = [[inverse[v] for v in rot[u] if v != z] for u in mapping]
            es, fs = topology(rr)
            need(len(es) == 52 and len(fs) == 34, 'root deletion dimensions')
            outer = [f for f in fs if len(f) != 3]
            need(outer == [list(cycle_key(list(range(4, -1, -1))))], 'literal ordered outer B')
            degree = list(map(len, rr))
            need(min(degree[:5]) >= 4 and min(degree[5:]) >= 5, 'complete source degree')
            h = sum(degree[:5]) - 20
            need(sum(d == 5 for d in degree[5:]) ==
                 6 + h + sum(max(0, d - 6) for d in degree[5:]), 'curvature')
            rs = []
            for p in WORDS:
                full = lifts(rr, p)
                rs.append(dict(pattern=p, count=len(full), lifts=full))
                total += len(full)
            mask = sum(1 << i for i, row in enumerate(rs) if row['count'])
            d5 = frames(mapping, rs)
            need(mask in known and all(f['mask'] in known for f in d5), 'catalogue-outside source')
            records.append(dict(id=f's{sid:03d}-z{z:02d}', sphere=sid, root=z,
                                canonical_to_original=mapping, edges=es, rotation=rr,
                                faces=fs, outer_face=outer[0], degree=degree, h=h,
                                rows=rs, mask=mask, frames=d5))
            histogram[h] += 1
            mask_histogram[mask] += 1
    summary = dict(spheres=len(primary), rooted_disks=len(records),
                   literal_rows=10 * len(records), full_lifts=total,
                   h_histogram=dict(sorted(histogram.items())),
                   mask_histogram=dict(sorted(mask_histogram.items())),
                   generation_agreement=True, frozen_drift=0,
                   actual_933_941='not triggered', all_root_relations_in_K132=True)
    return dict(schema='k15-rooted-sphere-full-fibres-v1', base=base['base'],
                input_sha256={str(p.relative_to(HERE)): sha(p.read_bytes()) for p in
                              [catpath, HERE / 'generation/spheres21.pc',
                               HERE / 'generation/spheres21_from_min4.pc']},
                pattern_order=WORDS, summary=summary, records=records)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json.gz')
    args = parser.parse_args()
    result = calculate()
    data = (json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n').encode()
    if args.write:
        with args.certificate.open('xb') as stream:
            stream.write(gzip.compress(data, mtime=0))
        with (HERE / 'summary.json').open('x') as stream:
            json.dump(result['summary'], stream, indent=2, sort_keys=True)
            stream.write('\n')
    else:
        need(gzip.decompress(args.certificate.read_bytes()) == data, 'certificate mismatch')
    print(json.dumps(result['summary'], sort_keys=True))
    print('PASS full-fibre payload SHA256', sha(data))


if __name__ == '__main__':
    main()
