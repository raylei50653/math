#!/usr/bin/env python3
"""Read-only integrated replay; finite controls do not establish a bad source."""
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def custody():
    counts = {"BASE": 0, "inherited": 0}
    for folder in (HERE, HERE / "B", HERE / "C"):
        manifest = json.loads((folder / "INPUTS.json").read_text())
        for item in manifest.get("inputs", manifest.get("files", [])):
            data = (folder / "frozen" / item["path"]).read_bytes()
            assert hashlib.sha256(data).hexdigest() == item["sha256"]
            inherited = item["provenance"].startswith("live inherited")
            if not inherited:
                assert data == subprocess.check_output(
                    ["git", "show", manifest["base"] + ":" + item["path"]], cwd=ROOT)
            elif item["path"].startswith("audits/"):
                assert data == (ROOT / item["path"]).read_bytes()
            counts["inherited" if inherited else "BASE"] += 1
    previous = ROOT / "audits/2026-10-18-abstraction-bottleneck-9f1fe84"
    for line in (previous / "OUTPUTS.sha256").read_text().splitlines():
        digest, relative = line.split("  ", 1)
        assert hashlib.sha256((previous / relative).read_bytes()).hexdigest() == digest
    return counts


def run(args):
    p = subprocess.run([sys.executable, "-B", *map(str, args)], cwd=ROOT,
                       capture_output=True, text=True)
    assert p.returncode == 0, (args, p.stdout, p.stderr)
    assert not p.stderr, (args, p.stderr)
    return {"status": "PASS", "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest()}


def independent_control():
    def edge(a, b):
        return tuple(sorted((a, b)))

    def rim(word):
        return {edge(word[i], word[(i+1) % len(word)]) for i in range(len(word))}

    outer = "xyabc"
    polygon = "abqden"
    vertices = tuple("xyabcqdenphr")
    es = rim(outer) | rim(polygon) | {edge("q", "c")}
    es |= {edge("p", v) for v in "abqnh"}
    es |= {edge("h", v) for v in "qden"}
    es |= {edge("r", v) for v in "ayxcqden"}
    cap_faces = [tuple(x) for x in ("pab", "pbq", "pqh", "phn", "pna", "hqd", "hde", "hen")]
    wheel = "anedqcxy"
    outside = [("b", "c", "q")] + [("r", wheel[i], wheel[(i+1) % 8]) for i in range(8)]
    old_faces = cap_faces + outside
    small_vertices = tuple(v for v in vertices if v not in "ph")
    reduced = {e for e in es if not set(e) & set("ph")}
    graphs = {"G": (vertices, es, old_faces)}
    for name, root, destinations in (("G_a", "a", "qde"), ("G_b", "b", "den")):
        ring = polygon[polygon.index(root):] + polygon[:polygon.index(root)]
        faces = [(root, ring[i], ring[i+1]) for i in range(1, 5)] + outside
        graphs[name] = (small_vertices, reduced | {edge(root, v) for v in destinations}, faces)
    rows = ["01012", "01021", "01023", "01201", "01202", "01203", "01212", "01213", "01231", "01232"]
    expected = {"G": [5, 13, 8, 5, 1, 0, 1, 0, 8, 4],
                "G_a": [0, 1, 1, 0, 1, 0, 1, 0, 1, 2],
                "G_b": [1, 12, 11, 1, 0, 0, 0, 0, 11, 10]}
    cert = json.loads((HERE / "C/certificate.json").read_text())["whole_graph_control"]
    known = {int(x) for x in json.loads((HERE / "frozen/artifacts/c5_cells/cells.json").read_text())["cells"]}
    assert len(known) == 132 and not any(mask & 594 == 512 for mask in known)
    result = {}
    for name, (vs, edges, faces) in graphs.items():
        # Independently check closed sphere vertex rotations, not merely Euler.
        darts, next_at = set(), {v: {} for v in vs}
        for face in faces + [tuple(reversed(outer))]:
            for i, v in enumerate(face):
                prev, nxt = face[i-1], face[(i+1) % len(face)]
                assert (v, nxt) not in darts and prev not in next_at[v]
                darts.add((v, nxt)); next_at[v][prev] = nxt
        assert {edge(*d) for d in darts} == edges
        assert all((v, u) in darts for u, v in darts)
        for v, successors in next_at.items():
            start = min(successors)
            seen, u = set(), start
            while u not in seen:
                seen.add(u); u = successors[u]
            assert u == start and seen == set(successors), v
        assert len(vs) - len(edges) + len(faces) == 1
        assert {e for e in edges if set(e) <= set(outer)} == rim(outer)
        counts, full_sets = [], []
        private = tuple(v for v in vs if v not in outer)
        for row in rows:
            fixed = dict(zip(outer, map(int, row)))
            full = []
            for colours in itertools.product(range(4), repeat=len(private)):
                c = dict(fixed, **dict(zip(private, colours)))
                if all(c[u] != c[v] for u, v in edges):
                    # C uses L,R,h where this independent reconstruction uses d,e,h.
                    rename = {"L": "d", "R": "e"}
                    full.append(tuple(c[rename.get(v, v)] for v in cert[name]["vertices"]))
            counts.append(len(full)); full_sets.append(sorted(full))
        assert counts == expected[name] == cert[name]["counts"]
        assert [hashlib.sha256(json.dumps(f).encode()).hexdigest() for f in full_sets] == cert[name]["fibres_sha256"]
        mask = sum(1 << i for i, c in enumerate(counts) if c)
        assert mask == cert[name]["mask"] and mask in known
        assert len(vs) - 5 == cert[name]["inner_vertices"]
        result[name] = {"inner": len(vs)-5, "mask": mask, "all_ten_fibres": "PASS", "plane_rotation": "PASS"}
    return result


def negative_control():
    # The actual normal checker must reject a genuinely modified certificate.
    with tempfile.TemporaryDirectory(prefix="math-smaller-source-negative-") as td:
        tmp = Path(td)
        shutil.copyfile(HERE / "A/check_hexagon_obstruction.py", tmp / "check_hexagon_obstruction.py")
        cert = json.loads((HERE / "A/hexagon_obstruction.json").read_text())
        assert cert["fan_contexts"]["01202"]["leaks"]
        cert["fan_contexts"]["01202"]["leaks"] = []
        (tmp / "hexagon_obstruction.json").write_text(json.dumps(cert, sort_keys=True, separators=(",", ":")) + "\n")
        p = subprocess.run([sys.executable, "-B", str(tmp / "check_hexagon_obstruction.py")],
                           capture_output=True, text=True)
        assert p.returncode != 0 and "finite patch certificate mismatch" in p.stderr
    return "REJECTED erased 01202 leaks"


def independent_pair_partition():
    intersection, old_count = 0, 0
    for t in itertools.product(range(4), repeat=6):
        if any(t[i] == t[(i+1) % 6] for i in range(6)):
            continue
        a, b, q, left, right, n = t
        fa = all(a != c for c in (q, left, right))
        fb = all(b != c for c in (left, right, n))
        old = [(p, h) for p, h in itertools.product(range(4), repeat=2)
               if p not in {a, b, q, n} and h not in {p, q, left, right, n}]
        if fa and fb:
            intersection += 1
            assert q == right and n == left and len({a, b, q, n}) == 4 and not old
        if len({a, b, q}) == 3:
            if old:
                assert fa != fb and len(old) == 1
                p, h = old[0]
                assert h == (a if fa else b)
                old_count += 1
            elif (fa or fb) and len({a, b, q, n}) <= 3:
                raise AssertionError("lost nonrainbow lift")
    assert intersection == 24 and old_count == 168
    return {"fan_intersection_tuples": intersection, "generic_old_unique_lifts": old_count}


def main():
    result = {"custody": custody(), "independent_completed_control": independent_control(),
              "independent_pair_partition": independent_pair_partition()}
    for name, args in (
        ("A", [HERE / "A/check_hexagon_obstruction.py"]),
        ("B", [HERE / "B/check_patches.py", "--check", HERE / "B/patches.json"]),
        ("C", [HERE / "C/check_bridge.py", "--check"]),
        ("B_independent_C_review", [HERE / "B/review_bridge_control.py"]),
    ):
        result[name] = run(args)
    result["corrupted_certificate"] = negative_control()
    seal = HERE / "OUTPUTS.sha256"
    if seal.exists():
        lines = seal.read_text().splitlines()
        for line in lines:
            digest, relative = line.split("  ", 1)
            assert hashlib.sha256((HERE / relative).read_bytes()).hexdigest() == digest, relative
        result["sealed_outputs"] = len(lines)
    result["smaller_bad_source_proved"] = False
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
