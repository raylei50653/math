#!/usr/bin/env python3
"""Independent stdlib reconstruction of C's fixed rotation and pair theorem."""
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path


def edge(a, b):
    return tuple(sorted((a, b)))


def eset(items):
    return frozenset(edge(*x) for x in items)


def canon(cycle):
    return min(tuple(cycle[i:] + cycle[:i]) for i in range(len(cycle)))


def components(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    left = set(vertices)
    result = []
    while left:
        seen = {min(left)}
        todo = list(seen)
        while todo:
            for w in adj[todo.pop()] - seen:
                seen.add(w)
                todo.append(w)
        result.append(frozenset(seen))
        left -= seen
    return result


def perfect(vertices, selected):
    return all(sum(v in e for e in selected) == 1 for v in vertices)


def all_matchings(vertices, edges):
    if not vertices:
        yield frozenset()
        return
    v = min(vertices)
    for e in sorted(edges):
        if v in e and set(e) <= vertices:
            for rest in all_matchings(vertices - set(e), edges):
                yield rest | {e}


def reconstruct(c):
    E = eset(c["edges"])
    V = set().union(*map(set, E))
    rot = {int(v): ns for v, ns in c["sphere_rotation"].items()}
    assert set(rot) == V
    assert all(set(rot[v]) == {w for e in E if v in e for w in e if w != v}
               for v in V)
    darts = {(a, b) for x, y in E for a, b in [(x, y), (y, x)]}
    seen, faces = set(), []
    for start in sorted(darts):
        if start in seen:
            continue
        walk, step = [], start
        while step not in seen:
            seen.add(step)
            a, b = step
            walk.append(a)
            ns = rot[b]
            step = (b, ns[(ns.index(a) + 1) % len(ns)])
        assert step == start and len(set(walk)) == len(walk)
        faces.append(canon(walk))
    claimed = [canon(x) for x in c["sphere_faces"]]
    assert sorted(faces) == sorted(claimed)
    assert len(faces) == len(E) - len(V) + 2
    dart_face = {}
    for i, face in enumerate(claimed):
        for j, a in enumerate(face):
            dart_face[a, face[(j + 1) % len(face)]] = i
    assert set(dart_face) == darts
    dual = {e: edge(dart_face[e], dart_face[e[::-1]]) for e in E}
    assert all(a != b for a, b in dual.values())
    for row in c["primal_edges"]:
        assert dual[edge(*row["dual_edge"])] == edge(*row["primal_edge"])
    triangles = {v: {i for i, f in enumerate(claimed) if v in f} for v in V}
    assert all(len(t) == 3 for t in triangles.values())
    assert triangles == {int(v): set(t) for v, t in c["primal_triangles"].items()}
    degrees = {i: len(f) for i, f in enumerate(claimed)}
    assert [degrees[i] for i in range(len(faces))] == c["original_primal_degrees"]
    return E, V, dual, triangles, degrees


def verify_control(c):
    E, V, dual, triangles, degrees = reconstruct(c)
    PV, PE = set(degrees), set(dual.values())
    M = eset(c["M"])
    P = {dual[e] for e in M}
    assert perfect(V, M)
    charge = lambda comp: sum(degrees[x] for x in comp) % 2
    old = components(PV, P)
    K = next(comp for comp in old if set(dual[(0, 3)]) <= comp)
    U = next(comp for comp in old
             if set(dual[edge(1, c["outer_ports"][0])]) <= comp)
    T = next(comp for comp in old if comp not in (K, U))
    assert len(old) == 3 and len(K) == 2
    assert (charge(K), charge(U), charge(T)) == (1, 0, 1)
    b = {x: int(x not in U) for x in PV}
    assert P == {e for e in PE if b[e[0]] == b[e[1]]}
    bad = {x: {v for v, tri in triangles.items()
               if x in tri and all(b[y] != b[x] for y in tri - {x})}
           for x in PV}
    for x in PV:
        assert len(bad[x]) == degrees[x] - 2 * sum(x in dual[e] for e in M)
    pm = set(all_matchings(V, E))
    rows = {eset(r["edges"]): r for r in c["matching_rows"]}
    assert len(rows) == len(c["matching_rows"]) and set(rows) == pm
    for N, row in rows.items():
        whole = components(V, E - N)
        assert all(sum(v in e for e in E - N) == 2 for v in V)
        assert sorted(map(sorted, whole)) == sorted(
            sorted(cycle) for cycle in row["complement_cycles"])
        odd = sum(len(comp) % 2 for comp in whole)
        assert odd == row["oddness"]
        primal = components(PV, {dual[e] for e in N})
        assert (odd == 0) == all(charge(comp) == 0 for comp in primal)
    safe = []
    for e in ((4, 5), (5, 6)):
        safe.append(next(x for x in dual[e] if x not in K))
    marked_vertices = set().union(*(set(dual[edge(*e)]) for e in c["marks"]))
    tested, admissible, successes = 0, 0, []
    failures = []
    for rho in safe:
        for tau in sorted(T):
            if edge(rho, tau) not in PE or {rho, tau} & marked_vertices:
                continue
            if sum(pe == edge(rho, tau) for pe in dual.values()) != 1:
                continue
            tested += 1
            X = {rho, tau}
            cut = frozenset(e for e, pe in dual.items() if len(set(pe) & X) == 1)
            N = M ^ cut
            common = {v for v, tri in triangles.items() if X <= tri}
            local = bad[rho] <= common and bad[tau] <= common
            assert local == perfect(V, N)
            if not local:
                continue
            admissible += 1
            assert len(common) == 2
            assert len(bad[rho]) + len(bad[tau]) == 2
            assert degrees[rho] % 2 == degrees[tau] % 2
            cutV = set().union(*map(set, cut))
            assert len(components(cutV, cut)) == 1
            assert all(sum(v in e for e in cut) == 2 for v in cutV)
            untouched = []
            for region, removed, opposite in [(T, tau, rho), (U, rho, tau)]:
                residual = region - {removed}
                residual_edges = {e for e in P if set(e) <= residual}
                for comp in components(residual, residual_edges):
                    if not any(edge(x, opposite) in PE for x in comp):
                        untouched.append(comp)
            predicted = all(charge(comp) == 0 for comp in untouched)
            actual = all(len(comp) % 2 == 0 for comp in components(V, E - N))
            assert predicted == actual
            detail = {
                "vertices": [rho, tau],
                "degrees": [degrees[rho], degrees[tau]],
                "bad_corner_counts": [len(bad[rho]), len(bad[tau])],
                "untouched_components": [
                    {"vertices": sorted(comp), "charge": charge(comp)}
                    for comp in untouched],
                "matching_row": rows[N]["index"],
                "complete_complement_lengths": sorted(
                    map(len, components(V, E - N))),
            }
            (successes if actual else failures).append(detail)
    return {
        "name": c["name"],
        "direct_perfect_matchings": len(pm),
        "candidate_pairs": tested,
        "admissible_pairs": admissible,
        "successful_pairs": successes,
        "admissible_parity_failures": failures,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path,
                    default=Path(__file__).resolve().parents[1] / "C/certificate.json.gz")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    data = args.certificate.read_bytes()
    decoded = gzip.decompress(data) if args.certificate.suffix == ".gz" else data
    cert = json.loads(decoded)
    assert cert["source_realizability"] == "not triggered"
    results = [verify_control(c) for c in cert["controls"]]
    missing = copy.deepcopy(cert["controls"][0])
    missing["matching_rows"].pop()
    bad_rotation = copy.deepcopy(cert["controls"][0])
    bad_rotation["sphere_rotation"]["0"] = list(
        reversed(bad_rotation["sphere_rotation"]["0"]))
    negatives = []
    for name, damaged in [("missing_matching_rejected", missing),
                          ("changed_rotation_rejected", bad_rotation)]:
        try:
            verify_control(damaged)
        except (AssertionError, KeyError, StopIteration, ValueError):
            negatives.append(name)
        else:
            raise AssertionError(name + " accepted")
    result = {
        "authority": "independent finite cross-review only",
        "source_realizability": "not triggered",
        "certificate_sha256": hashlib.sha256(data).hexdigest(),
        "controls": results,
        "perfect_matchings": sum(r["direct_perfect_matchings"] for r in results),
        "negative_checks": negatives,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x") as out:
            out.write(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
