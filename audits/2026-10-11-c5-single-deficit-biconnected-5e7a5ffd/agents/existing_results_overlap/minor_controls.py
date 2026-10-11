#!/usr/bin/env python3
"""Fixed Figure 1 / complete K4 minor controls, stdlib only.

No source enumeration and no coloring claim. Every stretch subdivides its
specified bold edge twice. Only counts 0, 1, 2 are calibrated; the unbounded
claim belongs to the paper argument. Synthetic degree-completing B attachments
give displayed K5 minors, so the original disk theorem domain is not triggered.

Write once: python3 minor_controls.py --write
Replay without writing: PYTHONDONTWRITEBYTECODE=1 python3 minor_controls.py --check --seed 17
"""

import argparse
import copy
import hashlib
import itertools
import json
import pathlib
import random
import sys

BASE = "4dd11f422c6fa49265a412085116b088786d0344"
AGENT_ROOT = pathlib.Path(__file__).resolve().parent
AUDIT_ROOT = AGENT_ROOT.parent.parent
PDF = AUDIT_ROOT / "literature/cranston-rabern-2017-final.pdf"
B = ["b0", "b1", "b2", "b3", "b4"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(u, v):
    assert u != v, "loop"
    return tuple(sorted((u, v)))


def adjacency(vertices, edges):
    result = {v: set() for v in vertices}
    for u, v in edges:
        assert u in result and v in result, "edge endpoint missing"
        result[u].add(v)
        result[v].add(u)
    return result


def tree_on(bag, edges):
    members = set(bag)
    adj = adjacency(bag, [e for e in edges if set(e) <= members])
    pending = [min(bag)]
    seen = set(pending)
    tree = []
    for u in pending:
        for v in sorted(adj[u] - seen):
            seen.add(v)
            pending.append(v)
            tree.append(edge(u, v))
    assert seen == members, "bag disconnected"
    return [list(e) for e in sorted(tree)]


def minor_record(bags, edges):
    bags = [sorted(bag) for bag in bags]
    original = set(edges)
    witnesses = []
    for i, j in itertools.combinations(range(len(bags)), 2):
        choices = sorted(edge(u, v) for u in bags[i] for v in bags[j]
                         if edge(u, v) in original)
        assert choices, "missing complete-minor cross edge"
        witnesses.append({"bags": [i, j], "original_edge": list(choices[0])})
    return {"bags": bags, "bag_trees": [tree_on(bag, edges) for bag in bags],
            "cross_edge_witnesses": witnesses}


def stretched_seed(seed, counts):
    terminals = ["a0", "a1", "a2"]
    vertices = {"s", *terminals}
    triangles = {edge(u, v) for u, v in itertools.combinations(terminals, 2)}
    if seed == "D-left":
        bold = [("s", a) for a in terminals]
    elif seed == "D-middle":
        intermediate = ["u0", "u1", "u2"]
        vertices.update(intermediate)
        bold = [("s", u) for u in intermediate]
        bold += [(u, a) for u, a in zip(intermediate, terminals)]
    else:
        raise AssertionError("unknown stretched seed")
    assert len(counts) == len(bold)
    assert all(isinstance(k, int) and 0 <= k <= 2 for k in counts)
    edges = set(triangles)
    paths = []
    for index, ((u, v), count) in enumerate(zip(bold, counts)):
        inner = [f"p{index}_{i}" for i in range(2 * count)]
        vertices.update(inner)
        path = [u, *inner, v]
        edges.update(edge(x, y) for x, y in zip(path, path[1:]))
        paths.append(path)
    center = sorted(vertices - set(terminals))
    return sorted(vertices), sorted(edges), [center, ["a0"], ["a1"], ["a2"]], {
        "seed": seed, "bold_edges": [list(e) for e in bold],
        "stretch_counts": list(counts), "vertices_added_per_stretch": 2,
        "expanded_bold_paths": paths,
        "unbolded_triangle_edges": [list(e) for e in sorted(triangles)]}


def fixed_seed(seed):
    if seed == "D-spindle":
        vertices = ["s", "l0", "l1", "l2", "r0", "r1", "r2"]
        edges = set()
        for side in ("l", "r"):
            a, c, z = [f"{side}{i}" for i in range(3)]
            edges.update(edge(u, v) for u, v in
                         [("s", a), ("s", c), (a, c), (a, z), (c, z)])
        edges.add(edge("l2", "r2"))
        bags = [["s"], ["l0"], ["l1"], ["l2", "r0", "r1", "r2"]]
    elif seed == "complete-K4":
        vertices = ["s", "a0", "a1", "a2"]
        edges = {edge(u, v) for u, v in itertools.combinations(vertices, 2)}
        bags = [["s"], ["a0"], ["a1"], ["a2"]]
    else:
        raise AssertionError("unknown fixed seed")
    return sorted(vertices), sorted(edges), bags, {
        "seed": seed, "bold_edges": [], "stretch_counts": [],
        "vertices_added_per_stretch": 2, "expanded_bold_paths": [],
        "unbolded_triangle_edges": []}


def make_control(seed, counts=()):
    if seed in ("D-left", "D-middle"):
        vertices, hedges, bags, parameters = stretched_seed(seed, counts)
    else:
        vertices, hedges, bags, parameters = fixed_seed(seed)
    adj = adjacency(vertices, hedges)
    attachments = []
    for v in vertices:
        target = 5 if v == "s" else 4
        missing = target - len(adj[v])
        assert 1 <= missing <= 5, "direct original B attachment not forced"
        attachments.extend(edge(v, b) for b in B[:missing])
    bedges = {edge(B[i], B[(i + 1) % 5]) for i in range(5)}
    medges = sorted(set(hedges) | set(attachments) | bedges)
    return {
        "id": seed + ("-k" + "".join(map(str, counts)) if counts else ""),
        "parameters": parameters,
        "H_vertices": vertices,
        "H_original_edges": [list(e) for e in hedges],
        "B_order": B,
        "original_boundary_attachments": [list(e) for e in sorted(attachments)],
        "M_vertices": sorted(vertices + B),
        "M_original_edges": [list(e) for e in medges],
        "internal_degrees_H": {v: len(adj[v]) for v in vertices},
        "target_complete_degrees_M": {v: 5 if v == "s" else 4 for v in vertices},
        "K4_minor_in_H": minor_record(bags, hedges),
        "K5_minor_in_same_M": minor_record(bags + [B], medges),
        "minor_control": {"status": "triggered and holds",
                          "claim": "same-source connected disjoint K4 and K5 branch sets"},
        "original_theorem_domain": {
            "status": "not triggered",
            "reason": "displayed K5 minor proves nonplanarity, so M is not a C5 disk"},
        "coloring_claim": "none; no boundary-row rejection or extension is asserted"}


def all_controls():
    controls = [make_control("D-left", ks) for ks in itertools.product(range(3), repeat=3)]
    controls.extend(make_control("D-middle", ks) for ks in itertools.product(range(3), repeat=6))
    controls.extend([make_control("D-spindle"), make_control("complete-K4")])
    assert len(controls) == 758
    return controls


def connected(vertices, edges):
    if not vertices:
        return True
    adj = adjacency(vertices, edges)
    pending = [min(vertices)]
    seen = set(pending)
    for u in pending:
        for v in adj[u] - seen:
            seen.add(v)
            pending.append(v)
    return len(seen) == len(vertices)


def validate_minor(record, vertices, edges, size):
    assert len(record["bags"]) == len(record["bag_trees"]) == size
    original = set(edges)
    vertices = set(vertices)
    used = set()
    bags = []
    for members, tree in zip(record["bags"], record["bag_trees"]):
        assert members and len(members) == len(set(members)), "empty or duplicate bag"
        bag = set(members)
        assert bag <= vertices, "bag vertex outside original graph"
        assert not used & bag, "branch sets overlap"
        used |= bag
        tree = [tuple(e) for e in tree]
        assert len(tree) == len(bag) - 1, "bag tree wrong edge count"
        assert len(tree) == len(set(tree)), "bag tree duplicate edge"
        assert all(e in original and set(e) <= bag for e in tree), "invalid tree original edge"
        assert connected(bag, tree), "bag tree disconnected"
        bags.append(bag)
    seen_pairs = set()
    for witness in record["cross_edge_witnesses"]:
        i, j = witness["bags"]
        assert 0 <= i < j < size and (i, j) not in seen_pairs, "invalid witness pair"
        seen_pairs.add((i, j))
        e = tuple(witness["original_edge"])
        assert e in original, "cross witness is not an original edge"
        u, v = e
        assert ((u in bags[i] and v in bags[j]) or
                (v in bags[i] and u in bags[j])), "cross witness does not join claimed bags"
    assert seen_pairs == set(itertools.combinations(range(size), 2)), "missing complete-minor adjacency"


def validate_control(control):
    p = control["parameters"]
    expected_id = p["seed"] + ("-k" + "".join(map(str, p["stretch_counts"]))
                                if p["stretch_counts"] else "")
    assert control["id"] == expected_id, "named control identity changed"
    if p["seed"] in ("D-left", "D-middle"):
        vertices, hedges, _, params = stretched_seed(p["seed"], p["stretch_counts"])
    else:
        vertices, hedges, _, params = fixed_seed(p["seed"])
    assert p == params, "seed/stretch contract changed"
    assert control["H_vertices"] == vertices
    assert control["H_original_edges"] == [list(e) for e in hedges]
    assert control["B_order"] == B
    medges = [tuple(e) for e in control["M_original_edges"]]
    mvertices = control["M_vertices"]
    assert mvertices == sorted(vertices + B)
    assert medges == sorted(set(medges)), "original graph not finite simple canonical"
    madj = adjacency(mvertices, medges)
    hadj = adjacency(vertices, hedges)
    expected_bedges = {edge(B[i], B[(i + 1) % 5]) for i in range(5)}
    assert {e for e in medges if set(e) <= set(B)} == expected_bedges, "B not induced C5"
    assert {e for e in medges if set(e) <= set(vertices)} == set(hedges), "H not original induced interior"
    attachments = [tuple(e) for e in control["original_boundary_attachments"]]
    assert set(medges) == set(hedges) | set(attachments) | expected_bedges
    for v in vertices:
        target = 5 if v == "s" else 4
        assert len(madj[v]) == target, "wrong complete M degree"
        assert control["target_complete_degrees_M"][v] == target
        assert control["internal_degrees_H"][v] == len(hadj[v])
        assert madj[v] & set(B), "missing actual boundary attachment"
    assert len(vertices) >= 3 and connected(vertices, hedges)
    for v in vertices:
        remaining = set(vertices) - {v}
        assert connected(remaining, [e for e in hedges if v not in e]), "H not 2-connected"
    validate_minor(control["K4_minor_in_H"], vertices, hedges, 4)
    validate_minor(control["K5_minor_in_same_M"], mvertices, medges, 5)
    assert control["K5_minor_in_same_M"]["bags"][:4] == control["K4_minor_in_H"]["bags"]
    assert control["K5_minor_in_same_M"]["bags"][4] == B, "fifth bag is not same original B"
    assert control["minor_control"]["status"] == "triggered and holds"
    assert control["original_theorem_domain"]["status"] == "not triggered"
    assert control["coloring_claim"].startswith("none;")


def tamper_selftest(controls):
    modifications = [
        ("non-original-cross-edge", lambda c: c["K5_minor_in_same_M"]["cross_edge_witnesses"][0].update(
            original_edge=["ghost0", "ghost1"])),
        ("overlapping-branch-sets", lambda c: (
            c["K5_minor_in_same_M"]["bags"][0].append("b0"),
            c["K5_minor_in_same_M"]["bag_trees"][0].append(["b0", "s"]))),
        ("wrong-complete-degree", lambda c: c["target_complete_degrees_M"].update(s=4)),
    ]
    result = []
    for name, mutate in modifications:
        damaged = copy.deepcopy(controls[0])
        mutate(damaged)
        try:
            validate_control(damaged)
        except (AssertionError, KeyError, ValueError) as error:
            result.append({"name": name, "status": "triggered and holds",
                           "claim": "corrupted certificate rejected", "rejection": str(error)})
        else:
            raise AssertionError("tamper negative control failed: " + name)
    return result


def validate_certificate(certificate, seed):
    assert certificate["base"] == BASE
    assert certificate["script_sha256"] == sha256(pathlib.Path(__file__).resolve())
    assert certificate["formal_pdf_sha256"] == sha256(PDF)
    controls = certificate["controls"]
    assert len(controls) == 758 and len({c["id"] for c in controls}) == 758
    expected = {"D-left": 27, "D-middle": 729, "D-spindle": 1, "complete-K4": 1}
    counts = {k: sum(c["parameters"]["seed"] == k for c in controls) for k in expected}
    assert counts == expected == certificate["counts"]
    order = list(range(len(controls)))
    random.Random(seed).shuffle(order)
    for index in order:
        validate_control(controls[index])
    return tamper_selftest(controls)


def guarded_output(path):
    path = path.resolve()
    assert path.is_relative_to(AGENT_ROOT), "output must stay in exclusive agent audit directory"
    return path


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    parser.add_argument("--seed", type=int, default=17, help="read-only replay validation order")
    parser.add_argument("--output-dir", type=pathlib.Path, default=AGENT_ROOT / "minor-controls")
    args = parser.parse_args()
    out = guarded_output(args.output_dir)
    certificate_path = out / "certificates.json"
    manifest_path = out / "manifest.json"
    if args.write:
        controls = all_controls()
        certificate = {
            "schema": "fixed-figure1-minor-controls-v1", "base": BASE,
            "script_sha256": sha256(pathlib.Path(__file__).resolve()),
            "formal_pdf_sha256": sha256(PDF),
            "formal_figure": "Figure 1, published final p. 4; stretch definition p. 3",
            "runtime": {"implementation": sys.implementation.name, "python_version": sys.version},
            "scope": "fixed counts 0,1,2 per specified bold edge only; no source enumeration",
            "counts": {"D-left": 27, "D-middle": 729, "D-spindle": 1, "complete-K4": 1},
            "controls": controls}
        negatives = validate_certificate(certificate, args.seed)
        content = json_bytes(certificate)
        out.mkdir(parents=True, exist_ok=False)
        with certificate_path.open("xb") as file:
            file.write(content)
        manifest = {
            "schema": "fixed-minor-controls-manifest-v1", "base": BASE,
            "script_path": str(pathlib.Path(__file__).resolve()),
            "script_sha256": certificate["script_sha256"],
            "formal_pdf_path": str(PDF), "formal_pdf_sha256": certificate["formal_pdf_sha256"],
            "certificate_sha256": hashlib.sha256(content).hexdigest(),
            "write_argv": sys.argv, "replay_argv": ["python3", str(pathlib.Path(__file__).resolve()),
                                                       "--check", "--seed", "17"],
            "tamper_negative_controls": negatives}
        with manifest_path.open("xb") as file:
            file.write(json_bytes(manifest))
        mode = "write-exclusive"
    else:
        certificate = json.loads(certificate_path.read_bytes())
        manifest = json.loads(manifest_path.read_bytes())
        assert sha256(certificate_path) == manifest["certificate_sha256"], "certificate hash mismatch"
        negatives = validate_certificate(certificate, args.seed)
        assert negatives == manifest["tamper_negative_controls"]
        mode = "read-only-check"
    print(json.dumps({"mode": mode, "python_version": sys.version, "validation_seed": args.seed,
                      "control_count": 758, "counts": certificate["counts"],
                      "minor_claim": "triggered and holds", "original_disk_domain": "not triggered",
                      "tamper_negative_controls": negatives,
                      "script_sha256": sha256(pathlib.Path(__file__).resolve()),
                      "certificate_sha256": sha256(certificate_path)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
