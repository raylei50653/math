#!/usr/bin/env python3
"""Parse frozen planar_code; retain every degree-five root and all collar chords.

This is a transparent postprocessor, not the exhaustive sphere generator.
plantri's two separately selected recursions are launched by replay.py.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def parse_pc(data):
    header = b">>planar_code<<"
    assert data.startswith(header)
    p = len(header)
    out = []
    while p < len(data):
        n = data[p]
        p += 1
        assert 0 < n < 256, "small planar_code only"
        rot = []
        for _ in range(n):
            row = []
            while data[p]:
                row.append(data[p] - 1)
                p += 1
            p += 1
            rot.append(row)
        out.append(rot)
    assert p == len(data)
    return out

def edges(rot):
    items = rot.items() if isinstance(rot, dict) else enumerate(rot)
    return sorted([u, v] for u, ns in items for v in ns if u < v)

def faces(rot):
    items = rot.items() if isinstance(rot, dict) else enumerate(rot)
    todo = {(u, v) for u, ns in items for v in ns}
    out = []
    while todo:
        start = min(todo)
        dart = start
        face = []
        while True:
            assert dart in todo, (start, dart)
            todo.remove(dart)
            u, v = dart
            face.append(u)
            ns = rot[v]
            dart = (v, ns[(ns.index(u) - 1) % len(ns)])
            if dart == start:
                break
        m = min(range(len(face)), key=face.__getitem__)
        out.append(face[m:] + face[:m])
    return sorted(out)

def validate_sphere(rot):
    n = len(rot)
    for u, ns in enumerate(rot):
        assert u not in ns and len(ns) == len(set(ns))
        assert all(0 <= v < n and u in rot[v] for v in ns)
    es, fs = edges(rot), faces(rot)
    assert n - len(es) + len(fs) == 2
    assert len(es) == 3*n - 6 and all(len(f) == 3 for f in fs)
    assert min(map(len, rot)) >= 5
    return es, fs

def canonical_embedding(rot, with_mapping=False, fixed_root=None):
    """Complete embedded-isomorphism key, both global orientations.

    An initial directed edge and orientation fixes a deterministic breadth-first
    discovery: root neighbor first, thereafter each parent neighbor first.
    For each discovered vertex encode its cyclic order beginning at parent.
    Taking the minimum over all initial darts and both orientations forgets
    labels and only one whole-embedding orientation. This is not a WL hash.
    """
    result = None
    for root, ns in enumerate(rot):
        if fixed_root is not None and root != fixed_root:
            continue
        for first in ns:
            for sign in (1, -1):
                seen, order, parent = {root: 0}, [root], {root: first}
                code = []
                for u in order:
                    row = rot[u]
                    k = row.index(parent[u])
                    ring = [row[(k + sign*i) % len(row)] for i in range(len(row))]
                    encoded = []
                    for v in ring:
                        if v not in seen:
                            seen[v] = len(order)
                            order.append(v)
                            parent[v] = u
                        encoded.append(seen[v])
                    code.append(tuple(encoded))
                assert len(order) == len(rot)
                code = tuple(code)
                if result is None or code < result:
                    result = code
                    best_order, best_sign = order[:], sign
    return (result, best_order, best_sign) if with_mapping else result

def root_record(sid, rot, z):
    B = rot[z][:]
    assert len(B) == 5
    V = [v for v in range(len(rot)) if v != z]
    r = {v: [w for w in rot[v] if w != z] for v in V}
    es, fs = edges(r), faces(r)
    canonical = B + sorted(set(V) - set(B))
    deg = {v: len(r[v]) for v in V}
    e = [deg[v] - 4 for v in B]
    h = sum(e)
    assert len(es) == 46 and len(V) == 18
    # Full sphere generation means no source is discarded for collar failure.
    rec = dict(id=f"S{sid:03d}-z{z:02d}", sphere_id=sid, z=z,
               B=B, vertices=V, edges=es, rotation=r, faces=fs,
               degree=deg, h=h, e=e, canonical_to_original=canonical)
    rec["d5_frames"] = [dict(shift=s, direction=t,
        B=[B[(s+t*i)%5] for i in range(5)],
        canonical_to_original=[B[(s+t*i)%5] for i in range(5)]+canonical[5:])
        for t in (1,-1) for s in range(5)]
    rec["B_chords"] = [edge for edge in es if set(edge) <= set(B)
        and (B.index(edge[0])-B.index(edge[1]))%5 not in (1,4)]
    try:
        assert not rec["B_chords"], "B has chord"
        nontri = [f for f in fs if len(f) != 3]
        assert len(nontri) == 1 and set(nontri[0]) == set(B), "wrong B face"
        apex = []
        for i in range(5):
            bs = {B[i], B[(i+1)%5]}
            incident = [f for f in fs if len(f) == 3 and bs <= set(f)]
            assert len(incident) == 1
            apex.append(next(iter(set(incident[0])-bs)))
        assert len(set(apex)) == 5, "repeated apex"
        HV = sorted(set(V) - set(B))
        hr = {v:[w for w in r[v] if w in HV] for v in HV}
        hf = faces(hr)
        outer = [f for f in hf if len(f) != 3]
        assert len(outer) == 1, "H outer not unique"
        C = outer[0]
        assert len(C) == len(set(C)) == 5+h, "H outer not simple collar"
        assert set(apex) <= set(C)
        p = C.index(apex[0]); C = C[p:] + C[:p]
        attachments = {v:[i for i,b in enumerate(B) if b in r[v]] for v in HV}
        assert all(attachments[apex[i]] == sorted([i,(i+1)%5]) for i in range(5))
        y = [v for v in C if v not in apex]
        assert len(y) == h and all(len(attachments[v]) == 1 for v in y)
        assert all(not attachments[v] for v in HV if v not in C)
        assert [sum(attachments[v] == [i] for v in y) for i in range(5)] == e
        Cedges = {tuple(sorted([C[i],C[(i+1)%len(C)]])) for i in range(len(C))}
        chords = [edge for edge in edges(hr) if set(edge) <= set(C)
                  and tuple(edge) not in Cedges]
        I = sorted(set(HV)-set(C))
        assert len(I) == 8-h and len(edges(hr)) == 31-h
        assert all(len(hr[v]) >= 3 for v in apex)
        assert all(len(hr[v]) >= 4 for v in y)
        assert all(len(hr[v]) >= 5 for v in I)
        rec.update(collar_status="holds", C=C, apex=apex, y=y, I=I,
                   attachments=attachments, H_rotation=hr, H_edges=edges(hr),
                   H_faces=hf, C_chords=chords, H_degree={v:len(hr[v]) for v in HV})
    except AssertionError as exc:
        rec.update(collar_status="not_applicable", collar_reason=str(exc))
    return rec

def dump(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, indent=2)+"\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--directory", type=Path, default=HERE)
    args = ap.parse_args()
    d = args.directory
    raw = (d/"spheres19.pc").read_bytes()
    rotations = parse_pc(raw)
    spheres = []
    roots = []
    for sid, rot in enumerate(rotations):
        es, fs = validate_sphere(rot)
        assert len(rot) == 19
        spheres.append(dict(id=sid, rotation=rot, edges=es, faces=fs, degree=list(map(len,rot))))
        roots += [root_record(sid,rot,z) for z in range(19) if len(rot[z]) == 5]
    dump(d/"spheres19.json", spheres)
    dump(d/"rooted_sources.json", roots)
    summary = dict(spheres=len(spheres), degree5_roots=len(roots),
        h_counts=dict(sorted(Counter(r["h"] for r in roots).items())),
        collar_counts=dict(Counter(r["collar_status"] for r in roots)),
        h_collar_counts=dict(sorted(Counter(r["h"] for r in roots if r["collar_status"]=="holds").items())),
        chord_counts=dict(sorted(Counter(len(r["C_chords"]) for r in roots if r["collar_status"]=="holds").items())),
        raw_sha256=hashlib.sha256(raw).hexdigest())
    alternate = d/"spheres19_from_min4.pc"
    if alternate.exists() and len(parse_pc(alternate.read_bytes())) == len(spheres):
        alts = parse_pc(alternate.read_bytes())
        primary_keys = [canonical_embedding(r) for r in rotations]
        alt_keys = [canonical_embedding(r) for r in alts]
        assert len(set(primary_keys)) == len(primary_keys)
        assert len(set(alt_keys)) == len(alt_keys)
        assert set(primary_keys) == set(alt_keys)
        summary["min4_complete_embedded_set_agreement"] = True
        dump(d/"min4_to_min5.json", [dict(min4_ordinal=i, min5_ordinal=primary_keys.index(k),
            embedding_key_sha256=hashlib.sha256(repr(k).encode()).hexdigest()) for i,k in enumerate(alt_keys)])
    dump(d/"generation_summary.json", summary)
    print(json.dumps(summary,sort_keys=True))

if __name__ == "__main__":
    main()
