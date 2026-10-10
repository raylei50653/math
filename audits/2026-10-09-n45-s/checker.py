#!/usr/bin/env python3
"""N45-S fixed controls; no imports from any research checker.

Generate with exclusive-create; --check recomputes and reads existing evidence.
This checks interface arithmetic and fixed graphs, not the paper topology proof.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"
HERE = Path(__file__).resolve().parent
COL = frozenset(range(4))


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def lift(vertices, edges, beta):
    """Independent deterministic four-colour backtracking; one complete lift."""
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    pins = dict(enumerate(beta))
    if any(pins[u] == pins[v] for u, v in edges if u in pins and v in pins):
        return None

    def visit():
        if len(pins) == len(vertices):
            return [pins[v] for v in vertices]
        choices = []
        for v in vertices:
            if v not in pins:
                available = COL - {pins[u] for u in adj[v] if u in pins}
                choices.append((len(available), -len(adj[v]), v, sorted(available)))
        _, _, v, available = min(choices)
        for c in available:
            pins[v] = c
            result = visit()
            if result is not None:
                return result
            del pins[v]
        return None

    result = visit()
    if result is not None:
        f = dict(zip(vertices, result))
        require(all(f[u] != f[v] for u, v in edges), "invalid complete lift")
        require(all(f[i] == beta[i] for i in range(5)), "literal frame drift")
    return result


def pieces(vertices, edges, roots):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    unseen = set(vertices) - set(range(5)) - set(roots)
    result = []
    while unseen:
        todo = [min(unseen)]
        found = set()
        while todo:
            v = todo.pop()
            if v in found:
                continue
            found.add(v)
            todo.extend(sorted((adj[v] & unseen) - found))
        unseen -= found
        contacts = {str(r): sorted(found & adj[r]) for r in roots}
        owners = [r for r in roots if contacts[str(r)]]
        support = sorted(set().union(*(adj[v] & set(range(5)) for v in found)))
        result.append({"vertices": sorted(found), "contacts": contacts,
                       "owners": owners, "support": support})
    return result


def orbit_table():
    # Under the stabilizer of c, every off-diagonal forbidden pair belongs
    # to exactly one of these three orbits. This is an interface domain.
    rows = []
    for c, kr, ks, mask in itertools.product(range(4), range(1, 4), range(1, 4), range(8)):
        orbits = [set(), set(), set()]
        for a, b in itertools.product(range(4), repeat=2):
            if a == b:
                continue
            idx = 0 if a == c else 1 if b == c else 2
            orbits[idx].add((a, b))
        forbidden = set().union(*(orbits[i] for i in range(3) if mask & (1 << i)))
        column_sizes = [sum(b == j for a, b in forbidden) for j in range(4)]
        row_sizes = [sum(a == i for a, b in forbidden) for i in range(4)]
        valid = max(column_sizes) <= kr and max(row_sizes) <= ks
        if valid and kr + ks <= 3:
            require(not forbidden, "singleton low-incidence claim failed")
        rows.append({"c": c, "k_r": kr, "k_s": ks, "orbit_mask": mask,
                     "forbidden_pairs": sorted(map(list, forbidden)),
                     "column_sizes": column_sizes, "row_sizes": row_sizes,
                     "status": "triggered and holds" if valid else "not triggered",
                     "missing_premises": [] if valid else ["contact bound"],
                     "universal": not forbidden})
    return rows


def capacity_model(name, er, es, forbidden, kr, ks, side_factors, side_s, spoke_colour):
    """Complete 16-pair necessary interface, explicitly without graph lifts."""
    er, es = set(er), set(es)
    forbidden = [set(map(tuple, f)) for f in forbidden]
    require(sum(kr) == len(er), name + ": derivative degree count")
    require(sum(map(len, side_factors)) + sum(kr) == 4, name + ": root degree")
    require(COL - set().union(*map(set, side_factors)) == er, name + ": side identity")
    require(sum(map(len, side_factors)) == len(set().union(*map(set, side_factors))),
            name + ": side overlap")
    require(COL - set().union(*map(set, side_s)) == es, name + ": other side identity")
    require(sum(map(len, side_s)) + sum(ks) == 5, name + ": other root degree")
    for f, cr, cs in zip(forbidden, kr, ks):
        require(all(sum(y == b for a, y in f) <= cr for b in range(4)), name + ": column bound")
        require(all(sum(x == a for x, b in f) <= cs for a in range(4)), name + ": row bound")
    columns = []
    for b in sorted(es):
        g = [{a for a in range(4) if (a, b) in f} for f in forbidden]
        union = set().union(*g)
        require(all(len(x) == k for x, k in zip(g, kr)), name + ": nonzero delta")
        require(sum(map(len, g)) == len(union), name + ": overlap")
        require(union == er, name + ": rejected derivative exact cover")
        after = er - {spoke_colour}
        overlap = int(spoke_colour not in er)
        waste = len(union - after)
        require(overlap + waste == 1, name + ": original degree-five budget")
        columns.append({"b": b, "G_P": sorted(g[0]), "G_Q": sorted(g[1]),
                        "derivative_slacks": [0, 0, 0, 0, 0],
                        "original_O": overlap, "original_lambda": waste,
                        "mixed_blocker": next((i for i, x in enumerate(g)
                                               if spoke_colour in x), None)})
    return {"id": name, "evidence_layer": "abstract necessary interface control",
            "source_graph": None, "full_lifts": None,
            "missing_source_premises": ["named disk graph", "complete component lifts",
                                         "Sigma 933/941", "Sigma-criticality", "beta-minimality"],
            "E_r_X": sorted(er), "E_s": sorted(es), "k_r": kr, "k_s": ks,
            "side_factors_X": side_factors, "side_factors_s": side_s, "spoke_colour": spoke_colour,
            "A_P": [list(p) for p in itertools.product(range(4), repeat=2)
                    if p not in forbidden[0]],
            "A_Q": [list(p) for p in itertools.product(range(4), repeat=2)
                    if p not in forbidden[1]], "columns": columns,
            "status": "triggered and holds"}


def compute(source):
    manifest = json.loads((HERE / "inputs.json").read_text())
    head = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    require(head == BASE, "HEAD differs from frozen BASE")
    for item in manifest["base_files"]:
        require(digest(source / item["path"]) == item["sha256"], "input drift: " + item["path"])
    patterns = json.loads((source / "artifacts/c5_cells/cells.json").read_text())["pattern_order"]
    graphs = []
    for path in sorted((source / "artifacts/c5_excess_two_e4c/controls").glob("*.json")):
        data = json.loads(path.read_text())
        vertices = data["vertices"]
        edges = sorted(tuple(sorted(e)) for e in data["edges"])
        degrees = {v: sum(v in e for e in edges) for v in vertices}
        roots = sorted(v for v in vertices if v >= 5 and degrees[v] == 5)
        require(len(roots) == 2, path.name + ": root shape")
        ps = pieces(vertices, edges, roots)
        if sum(len(p["owners"]) == 2 for p in ps) != 2:
            continue
        require(data["m"] == 2, "stored m disagrees with original edges")
        for p in ps:
            saved = next(x for x in data["pieces"] if x["vertices"] == p["vertices"])
            require(all(saved[k] == p[k] for k in ["contacts", "owners", "support"]),
                    path.name + ": original piece metadata drift")
        sigma = 0
        row_lifts = []
        for index, beta in enumerate(patterns):
            f = lift(vertices, edges, beta)
            if f is not None:
                sigma |= 1 << index
            row_lifts.append(f)
        require(sigma == data["sigma"], "saved complete Sigma mismatch")
        rejected = [i for i, f in enumerate(row_lifts) if f is None]
        queries = []
        for r in roots:
            for edge in edges:
                if r not in edge or not any(v < 5 for v in edge):
                    continue
                reduced = [e for e in edges if e != edge]
                for index in rejected:
                    f = lift(vertices, reduced, patterns[index])
                    require(f is not None, "unexpected N45-S positive control; audit separately")
                    i = next(v for v in edge if v < 5)
                    require(f[vertices.index(r)] == patterns[index][i], "deleted spoke not forced equal")
                    queries.append({"edge": list(edge), "root": r, "index": index,
                                    "beta": patterns[index], "full_lift": f,
                                    "status": "not triggered",
                                    "missing_premises": ["G-spoke rejects this beta"]})
        missing = ["N2 45/54 spoke-omission rejected core"]
        if sigma not in [933, 941]:
            missing.append("complete canonical Sigma 933/941")
        graphs.append({"id": data["id"], "path": str(path.relative_to(source)),
                       "input_sha256": digest(path), "vertices": vertices,
                       "edges": list(map(list, edges)), "roots": roots,
                       "original_pieces": ps, "rotation": data["rotation"],
                       "complete_relations_ref": str(path.relative_to(source)) + "#pieces/rows",
                       "sigma": sigma, "row_full_lifts": row_lifts,
                       "saved_core_degrees": [c["root_degrees"] for row in data["row_cores"]
                                              for c in row["cores"]],
                       "spoke_queries": queries, "source_status": "not triggered",
                       "missing_premises": missing})
    require(len(graphs) == 19, "frozen inventory should contain nineteen N2 controls")
    table = orbit_table()
    pairs = [(a, b) for a, b in itertools.product(range(4), repeat=2)
             if a and b and a != b]
    models = [
        capacity_model("ABSTRACT-S-SIDE-BLOCK", [0, 1], [2], [[(0, 2)], [(1, 2)]],
                       [1, 1], [1, 1], [[2], [3]], [[0], [1], [3]], 2),
        capacity_model("ABSTRACT-S-JOINT-BLOCK", [0, 1], [2], [[(0, 2)], [(1, 2)]],
                       [1, 1], [1, 1], [[2], [3]], [[0], [1], [3]], 0),
        capacity_model("ABSTRACT-S-SINGLETON22-LONG-RESIDUAL", [1, 2, 3], [1, 2],
                       [pairs, [(1, 1), (2, 2)]], [2, 1], [2, 1], [[0]], [[0], [3]], 1),
    ]
    counts = [{"m_r": mr, "m_s": ms, "E_r_X_size": mr,
               "E_s_size_lower_bound": ms - 1,
               "both_short_necessary_count_pass": mr + ms <= 5}
              for mr, ms in itertools.product(range(2, 5), range(2, 6))]
    masks = []
    for sigma in [933, 941]:
        qg = [pos for index, pos in [(6, 0), (4, 1), (3, 2), (1, 3), (0, 4)]
              if not sigma & (1 << index)]
        permitted = [list(t) for n in range(3) for t in itertools.combinations(qg, n)
                     if n <= 1 or (t[0] - t[1]) % 5 in [1, 4]]
        masks.append({"sigma_G": sigma, "Q_G_singleton_positions": qg,
                      "E2_permitted_Q_X": permitted,
                      "scope": "necessary mask identities; not source realization"})
    return {"task": "N45-S", "base": BASE, "singleton_orbit_table": table,
            "abstract_capacity_controls": models, "both_short_incidence_counts": counts,
            "cross_row_masks": masks, "fixed_graph_inventory": graphs,
            "summary": {"singleton_candidates": len(table),
                        "valid_singleton_candidates": sum(x["status"] == "triggered and holds" for x in table),
                        "fixed_N2_graphs": len(graphs), "full_sigma_queries": len(graphs) * 10,
                        "spoke_deletion_queries": sum(len(g["spoke_queries"]) for g in graphs),
                        "N45_S_source_triggered": 0, "source_counterexamples": 0,
                        "paper_proof_checked_by_this_program": False}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", type=Path, required=True)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    payload = encode(compute(args.source_root.resolve()))
    target = HERE / "certificate.json"
    if args.check:
        require(target.read_bytes() == payload, "certificate mathematical/provenance byte mismatch")
        print("PASS read-only replay; SHA256", digest(target))
    else:
        with target.open("xb") as stream:
            stream.write(payload)
        print("created certificate exclusively; SHA256", digest(target))
    print(json.loads(payload)["summary"])


if __name__ == "__main__":
    main()
