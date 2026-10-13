#!/usr/bin/env python3
"""Named W5 terminals: complete literal C6 fibres and paper-bounded joins."""
from pathlib import Path
from collections import Counter, defaultdict, deque
from itertools import product
import argparse
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "certificate.v2.json"
ARCHIVE = ROOT / "full_lifts.v2.json.gz"
C = tuple(f"c{i}" for i in range(8))
T = tuple(f"t{i}" for i in range(8))
B = tuple(f"b{i}" for i in range(5))
B_ROWS = ("01012", "01021", "01023", "01201", "01202", "01203",
          "01212", "01213", "01231", "01232")
QUERIES = (
    ("c15-933", (0, 1, 2, 0, 0), 933),
    ("c18-933", (0, 2, 1, 0, 0), 933),
    ("c04-941", (0, 0, 1, 0, 2), 941),
    ("c07-941", (0, 0, 2, 0, 1), 941),
    ("c15-941", (0, 1, 2, 0, 0), 941),
    ("c18-941", (0, 2, 1, 0, 0), 941),
    ("c20-941", (1, 0, 0, 0, 2), 941),
    ("c30-941", (2, 0, 0, 0, 1), 941),
)
J = tuple(f"j{i}" for i in range(6))
U = tuple(f"u{i}" for i in range(5))


def edge(a, b):
    return tuple(sorted((a, b)))


def assemble(vertices, outer, faces):
    """Check every actual oriented face, boundary edge and vertex link."""
    vertices, outer, faces = tuple(vertices), tuple(outer), tuple(map(tuple, faces))
    assert len(set(vertices)) == len(vertices)
    edges = sorted({edge(a, b) for f in faces for a, b in zip(f, f[1:] + f[:1])})
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    assert len(vertices) - len(edges) + len(faces) == 1
    assert len(edges) == 3 * (len(vertices) - len(outer)) + 2 * len(outer) - 3
    darts = {}
    for fid, f in enumerate(faces):
        assert len(set(f)) == 3
        for a, b in zip(f, f[1:] + f[:1]):
            assert (a, b) not in darts
            darts[a, b] = fid
    boundary = {edge(a, b) for a, b in zip(outer, outer[1:] + outer[:1])}
    for a, b in edges:
        assert int((a, b) in darts) + int((b, a) in darts) == (1 if edge(a, b) in boundary else 2)
    for a, b in zip(outer, outer[1:] + outer[:1]):
        assert (a, b) in darts and (b, a) not in darts
    links = {}
    for v in vertices:
        link = defaultdict(set)
        for f in faces:
            if v in f:
                a, b = [w for w in f if w != v]
                link[a].add(b)
                link[b].add(a)
        assert set(link) == adj[v]
        assert all(len(z) in (1, 2) for z in link.values())
        assert sum(len(z) == 1 for z in link.values()) == (2 if v in outer else 0)
        reached = {next(iter(link))}
        queue = list(reached)
        while queue:
            for w in link[queue.pop()] - reached:
                reached.add(w)
                queue.append(w)
        assert reached == set(link)
        links[v] = {w: sorted(z) for w, z in link.items()}
    successor = {v: {} for v in vertices}
    for f in faces + (outer[::-1],):
        for i, v in enumerate(f):
            previous, following = f[i - 1], f[(i + 1) % len(f)]
            assert previous not in successor[v]
            successor[v][previous] = following
    rotations = {}
    for v in vertices:
        start = min(adj[v])
        order = [start]
        while successor[v][order[-1]] != start:
            order.append(successor[v][order[-1]])
            assert len(order) <= len(adj[v])
        assert set(order) == adj[v]
        rotations[v] = order
    return {"vertices": vertices, "outer": outer, "faces": faces,
            "edges": edges, "adj": adj, "links": links, "rotations": rotations}


def graph_on(vertices, edges):
    vertices = tuple(vertices)
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return {"vertices": vertices, "edges": sorted(set(edges)), "adj": adj}


def patch_faces(j, u):
    c, endpoint = j[:5], j[5]
    t, center = u[:4], u[4]
    faces = [(c[i], c[i + 1], t[i]) for i in range(4)]
    faces += [(c[i], t[i], t[i - 1]) for i in range(1, 4)]
    faces += [(c[0], t[0], endpoint), (c[4], endpoint, t[3])]
    rim = (endpoint,) + t
    faces += [(center, rim[i], rim[(i + 1) % 5]) for i in range(5)]
    return faces


def direct(g, pins):
    vertices, adj = g["vertices"], g["adj"]
    colors = dict(pins)
    if any(colors[a] == colors[b] for a, b in g["edges"] if a in colors and b in colors):
        return []
    result = []

    def visit():
        if len(colors) == len(vertices):
            result.append("".join(str(colors[v]) for v in vertices))
            return
        options = []
        for index, v in enumerate(vertices):
            if v in colors:
                continue
            legal = tuple(c for c in range(4) if all(colors.get(w) != c for w in adj[v]))
            options.append((len(legal), -sum(w in colors for w in adj[v]), index, v, legal))
        _, _, _, v, legal = min(options)
        for c in legal:
            colors[v] = c
            visit()
            del colors[v]

    visit()
    return sorted(result)


def factor_patch(row):
    """Independent center-color and four rim-color decomposition."""
    a, endpoint = tuple(map(int, row[:5])), int(row[5])
    if any(a[i] == a[i + 1] for i in range(4)) or endpoint in (a[0], a[4]):
        return []
    result = []
    for center in range(4):
        if center == endpoint:
            continue
        domains = [tuple(c for c in range(4) if c not in (center, a[i], a[i + 1]))
                   for i in range(4)]
        for t in product(*domains):
            if endpoint in (t[0], t[3]) or any(t[i] == t[i + 1] for i in range(3)):
                continue
            result.append("".join(map(str, t + (center,))))
    return sorted(result)


def canonical(row):
    names = {}
    return "".join(str(names.setdefault(c, len(names))) for c in row)


def terminal_kernel():
    g = assemble(J + U, J, patch_faces(J, U))
    fibres = {}
    proper_hist = Counter()
    for word in product("0123", repeat=6):
        row = "".join(word)
        lifts = direct(g, dict(zip(J, map(int, row))))
        interiors = [lift[6:] for lift in lifts]
        assert interiors == factor_patch(row)
        fibres[row] = interiors
        if all(row[i] != row[(i + 1) % 6] for i in range(6)):
            proper_hist[len(interiors)] += 1
    assert len(fibres) == 4096
    assert proper_hist == {0: 288, 1: 144, 2: 300}
    assert sum(map(len, fibres.values())) == 744
    proper_orbits = {canonical(row) for row in fibres
                     if all(row[i] != row[(i + 1) % 6] for i in range(6))}
    accepted_orbits = {canonical(row) for row, lifts in fibres.items() if lifts}
    assert len(proper_orbits) == 31 and len(accepted_orbits) == 19
    return g, fibres, dict(sorted(proper_hist.items()))


def collar_faces(e):
    faces = []
    original_names = ["a0"]
    for i in range(1, 5):
        original_names += [f"y{i}_{j}" for j in range(1, e[i] + 1)] + [f"a{i}"]
    original_names += [f"y0_{j}" for j in range(1, e[0] + 1)]
    assert len(original_names) == 8
    rename = dict(zip(original_names, C))
    for i in range(5):
        faces.append((B[i], B[(i + 1) % 5], rename[f"a{i}"]))
        fan = [f"a{(i - 1) % 5}"] + [f"y{i}_{j}" for j in range(1, e[i] + 1)] + [f"a{i}"]
        faces += [(B[i], rename[b], rename[a]) for a, b in zip(fan, fan[1:])]
    return faces, original_names


def source_graph(kind, pair, e):
    endpoints = ("x",) if kind == "PINCH" else ("x", "y")
    centers = ("zL", "zR")
    inner = T + endpoints + centers
    left_j = tuple(C[(pair + j) % 8] for j in range(5)) + (endpoints[0],)
    right_j = tuple(C[(pair + 4 + j) % 8] for j in range(5)) + (endpoints[-1],)
    left_u = tuple(T[(pair + j) % 8] for j in range(4)) + (centers[0],)
    right_u = tuple(T[(pair + 4 + j) % 8] for j in range(4)) + (centers[1],)
    hfaces = patch_faces(left_j, left_u) + patch_faces(right_j, right_u)
    if kind == "BRIDGE":
        hfaces += [(C[pair], "x", "y"), (C[(pair + 4) % 8], "y", "x")]
    h = assemble(C + inner, C, hfaces)
    assert all(len(h["adj"][c]) >= 4 for c in C)
    assert all(len(h["adj"][v]) >= 5 for v in inner)
    assert all(len(h["adj"][v] & set(C)) <= 2 for v in inner)
    afaces, names = collar_faces(e)
    g = assemble(B + C + inner, B, afaces + hfaces)
    skeleton_vertices = B + C + endpoints
    skeleton_edges = [e for e in g["edges"] if set(e) <= set(skeleton_vertices)]
    skeleton = graph_on(skeleton_vertices, skeleton_edges)
    return g, skeleton, ((left_j, left_u), (right_j, right_u)), names


def compressed(g, skeleton, patches, kernel, pins):
    result = []
    for lift in direct(skeleton, pins):
        assignment = dict(zip(skeleton["vertices"], map(int, lift)))
        factors = []
        for j, u in patches:
            row = "".join(str(assignment[v]) for v in j)
            factors.append((u, kernel[row]))
        for left, right in product(factors[0][1], factors[1][1]):
            joined = dict(assignment)
            for (u, _), interior in zip(factors, (left, right)):
                assert not set(u) & set(joined)
                joined.update(zip(u, map(int, interior)))
            result.append("".join(str(joined[v]) for v in g["vertices"]))
    assert len(result) == len(set(result))
    return sorted(result)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def freeze_graph(g):
    return {key: g[key] for key in ("vertices", "outer", "edges", "faces", "links", "rotations")}


def cap_check(g):
    """Original face-dual separation, not a graph-size or cycle-count shortcut."""
    adj, faces = g["adj"], g["faces"]
    cycles = set()

    def visit(start, path):
        for w in sorted(adj[path[-1]]):
            if w == start and len(path) >= 3:
                if path[1] < path[-1]:
                    cycles.add(tuple(path))
            elif len(path) < 5 and w > start and w not in path:
                visit(start, path + [w])

    for v in sorted(g["vertices"]):
        visit(v, [v])
    incident = defaultdict(list)
    for i, f in enumerate(faces):
        for a, b in zip(f, f[1:] + f[:1]):
            incident[edge(a, b)].append(i)
    outer = g["outer"]
    for a, b in zip(outer, outer[1:] + outer[:1]):
        incident[edge(a, b)].append(-1)
    dual = defaultdict(list)
    for e, fl in incident.items():
        assert len(fl) == 2
        a, b = fl
        dual[a].append((b, e))
        dual[b].append((a, e))
    counts = Counter()
    for cycle in sorted(cycles):
        barriers = {edge(a, b) for a, b in zip(cycle, cycle[1:] + cycle[:1])}
        reached, queue = {-1}, deque([-1])
        while queue:
            for fid, e in dual[queue.popleft()]:
                if e not in barriers and fid not in reached:
                    reached.add(fid)
                    queue.append(fid)
        interior_faces = [f for i, f in enumerate(faces) if i not in reached]
        inside = set().union(*map(set, interior_faces)) - set(cycle)
        if len(cycle) in (3, 4):
            assert not inside, (cycle, inside)
        else:
            assert len(inside) <= 1, (cycle, inside)
            if inside:
                center = next(iter(inside))
                assert adj[center] == set(cycle)
        counts[f"C{len(cycle)}_{'W5' if inside else 'empty'}"] += 1
    return dict(sorted(counts.items()))


def negative_controls(kernel):
    """Semantic failures: proper empties, lost lift, independent endpoint copies."""
    zero = "010102"
    assert kernel[zero] == [] and all(zero[i] != zero[(i + 1) % 6] for i in range(6))
    damaged = dict(kernel)
    damaged[zero] = ["12121"]
    assert damaged[zero] != factor_patch(zero)
    row = next(row for row, lifts in sorted(kernel.items()) if len(lifts) == 2)
    damaged = dict(kernel)
    damaged[row] = kernel[row][:-1]
    assert damaged[row] != factor_patch(row)
    # Both sides extend individually, while they pin the same original x differently.
    left_row, right_row = next((left, right)
                              for left, ll in sorted(kernel.items()) if ll and left[5] == "0"
                              for right, rr in sorted(kernel.items()) if rr and right[5] == "1"
                              if left[0] == right[4] and left[4] == right[0])
    assert kernel[left_row] and kernel[right_row]
    assert left_row[5] != right_row[5]
    assert left_row[0] == right_row[4] and left_row[4] == right_row[0]
    return {"proper_empty_rejected": {"row": zero},
            "lost_full_lift_rejected": {"row": row, "true_count": len(kernel[row])},
            "independent_endpoint_copy_rejected": {"left_J_row": left_row,
                                                   "right_J_row": right_row,
                                                   "same_original_x_join": 0}}


def compute():
    patch, kernel, histogram = terminal_kernel()
    archives = {"kernel": {"J_order": J, "U_order": U, "complete_literal_fibres": kernel},
                "sources": {}}
    records = []
    for kind in ("PINCH", "BRIDGE"):
        for pair in range(4):
            for query, e, target in QUERIES:
                name = f"{kind}-{pair}-{query}"
                g, skeleton, patches, collar_names = source_graph(kind, pair, e)
                # Check the inner disk only: the original B=C5 cap is excluded.
                h = assemble(tuple(v for v in g["vertices"] if v not in B), C,
                             [f for f in g["faces"] if not set(f) & set(B)])
                cap_counts = cap_check(h)
                row_fibres = {}
                for row in B_ROWS:
                    pins = dict(zip(B, map(int, row)))
                    full = direct(g, pins)
                    transferred = compressed(g, skeleton, patches, kernel, pins)
                    assert full == transferred, (name, row)
                    row_fibres[row] = full
                sigma = sum(1 << i for i, row in enumerate(B_ROWS) if row_fibres[row])
                assert sigma == 1023, (name, sigma)
                archives["sources"][name] = {"vertex_order": g["vertices"],
                                            "complete_B_row_fibres": row_fibres}
                records.append({"name": name, "kind": kind, "pair_index": pair,
                                "original_query": query, "e": e, "target": target,
                                "original_collar_C_names": collar_names,
                                "graph": freeze_graph(g),
                                "inner_small_cap_counts": cap_counts,
                                "anchored_patches": [{"J": j, "U": u} for j, u in patches],
                                "row_counts": {row: len(lifts) for row, lifts in row_fibres.items()},
                                "Sigma": sigma,
                                "source_status": "paper-classified control; target not triggered"})
    cert = {"kernel_graph": freeze_graph(patch), "literal_assignments": 4096,
            "proper_assignments": 732, "proper_count_histogram": histogram,
            "empty_literal_fibres": sum(not lifts for lifts in kernel.values()),
            "kernel_full_lifts": 744, "proper_S4_orbits": 31, "accepted_S4_orbits": 19,
            "source_controls": records, "negative_controls": negative_controls(kernel),
            "full_archive_sha256": hashlib.sha256(encode(archives)).hexdigest()}
    summary = {"literal_terminal_fibres": 4096, "terminal_full_lifts": 744,
               "source_graphs": len(records), "source_B_fibres": 10 * len(records),
               "source_full_lifts": sum(sum(r["row_counts"].values()) for r in records),
               "all_source_Sigma": 1023, "semantic_negative_controls": 3, "status": "PASS"}
    return cert, archives, summary


def normalized(value):
    return json.loads(json.dumps(value))


def run(write=False, negative=False):
    if write:
        assert not CERTIFICATE.exists() and not ARCHIVE.exists(), "exclusive evidence files already exist"
    cert, archives, summary = compute()
    if write:
        with CERTIFICATE.open("x") as out:
            out.write(json.dumps(cert, sort_keys=True, indent=2) + "\n")
        with ARCHIVE.open("xb") as raw:
            with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as out:
                out.write(encode(archives))
    else:
        saved = json.loads(CERTIFICATE.read_text())
        with gzip.open(ARCHIVE, "rt") as source:
            saved_archive = json.load(source)
        assert normalized(cert) == saved
        assert normalized(archives) == saved_archive
        if negative:
            corrupted = json.loads(json.dumps(saved_archive))
            corrupted["kernel"]["complete_literal_fibres"]["010102"] = ["12121"]
            assert corrupted != normalized(archives)
            corrupted = json.loads(json.dumps(saved_archive))
            first = next(iter(corrupted["sources"].values()))
            row = next(row for row, lifts in first["complete_B_row_fibres"].items() if lifts)
            first["complete_B_row_fibres"][row].pop()
            assert corrupted != normalized(archives)
            summary["archive_corruptions_rejected"] = 2
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    run(write=args.write, negative=args.negative)
