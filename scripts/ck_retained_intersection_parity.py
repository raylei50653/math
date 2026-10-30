#!/usr/bin/env python3
"""Exact retained-path intersection parity; no count-ray exclusion.

The parity lemma is proved on paper. This script checks named ribbon graphs,
the theta positive/negative rotation controls, and every boundary path action
of every normalized coloring of the two existing C8 wheel disks.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "audits/2026-10-26-ck-d-lock-comparison-8d28acc/configurations.py"
sys.path.insert(0, str(CONFIG.parent))
from configurations import validate_disk

OLD = ROOT / "audits/2026-10-29-bernhart-cross-split-e1a90fe/verification.json"
RECEIPT = OLD.parent / "RECEIPT.json"
DEFAULT = ROOT / "audits/2026-10-29-bernhart-retained-parity/rotation-controls.json"
PAIRS = ((1, 2), (1, 3), (2, 3))


def epsilon(edges, labels, rotations, a, b, c):
    """Vertex orientation signs from ORIGINAL edge-ID rotations.

    Rotations are cyclic, consistently oriented surface rotations. Degree-one
    boundary leaves have no epsilon; every degree-three vertex must be proper.
    """
    assert {a, b, c} == {1, 2, 3}
    incident = defaultdict(list)
    for eid, (u, v) in enumerate(edges):
        assert u != v
        incident[u].append(eid)
        incident[v].append(eid)
    assert set(rotations) == set(incident)
    answer = {}
    for v, rotation in rotations.items():
        assert sorted(rotation) == sorted(incident[v])
        if len(rotation) == 1:
            continue
        assert len(rotation) == 3
        colors = [labels[e] for e in rotation]
        assert set(colors) == {a, b, c}
        j = colors.index(a)
        answer[v] = 1 if colors[(j + 1) % 3] == b else -1
    return answer


def ribbon_faces(edges, rotations):
    """Face permutation on edge darts, preserving parallel edge identities."""
    incident = defaultdict(list)
    for eid, (u, v) in enumerate(edges):
        assert u != v
        incident[u].append(eid)
        incident[v].append(eid)
    assert set(rotations) == set(incident)
    successor = {}
    for v, es in rotations.items():
        assert sorted(es) == sorted(incident[v])
        for j, e in enumerate(es):
            successor[v, e] = es[(j + 1) % len(es)]
    pending = {(e, side) for e in range(len(edges)) for side in (0, 1)}
    faces = []
    while pending:
        root = min(pending)
        current, face = root, []
        while current not in face:
            assert current in pending
            pending.remove(current)
            face.append(current)
            eid, side = current
            arrival = edges[eid][1 - side]
            following = successor[arrival, eid]
            current = (following, edges[following].index(arrival))
        assert current == root
        faces.append(face)
    reached = {min(incident)}
    todo = list(reached)
    for u in todo:
        for e in incident[u]:
            v = edges[e][1] if edges[e][0] == u else edges[e][0]
            if v not in reached:
                reached.add(v)
                todo.append(v)
    assert reached == set(incident)
    chi = len(incident) - len(edges) + len(faces)
    assert (2 - chi) % 2 == 0 and chi <= 2
    return dict(faces=faces, vertices=len(incident), edges=len(edges),
                face_count=len(faces), euler_characteristic=chi, genus=(2 - chi) // 2)


def components(edges, labels, pair, removed=()):
    """Complete ordered degree-at-most-two paths AND closed components."""
    removed = set(removed)
    adj = defaultdict(list)
    for eid, ((u, v), color) in enumerate(zip(edges, labels)):
        if color in pair and eid not in removed:
            adj[u].append((eid, v))
            adj[v].append((eid, u))
    assert all(len(es) in (1, 2) for es in adj.values())
    pending, result = set(adj), []
    while pending:
        root = min(pending)
        reached, todo = {root}, [root]
        for u in todo:
            for _, v in adj[u]:
                if v not in reached:
                    reached.add(v)
                    todo.append(v)
        pending -= reached
        ends = sorted(v for v in reached if len(adj[v]) == 1)
        assert len(ends) in (0, 2)
        start = ends[0] if ends else min(reached)
        current, vertices, used, ordered = start, [start], set(), []
        while True:
            options = sorted((e, v) for e, v in adj[current] if e not in used)
            if not options:
                break
            e, v = options[0]
            used.add(e)
            ordered.append(e)
            vertices.append(v)
            current = v
        assert len(used) == sum(len(adj[v]) for v in reached) // 2
        assert (vertices[0] == vertices[-1]) == (not ends)
        result.append(dict(ends=ends, vertices=vertices, edges=ordered, cycle=not ends))
    return result


def alternating(order, first, second):
    assert len(first) == len(second) == 2 and len(set(first + second)) == 4
    a, b = sorted(order.index(v) for v in first)
    c, d = sorted(order.index(v) for v in second)
    return int(a < c < b < d or c < a < d < b)


def intersection_parity(edges, labels, rotations, first, second, a, b, c,
                        boundary_order=None, opposite_sides=False):
    """Check one pair of retained mixed components with disjoint endpoints.

    first belongs to {a,c}; second to {b,c}. A closed component has RHS zero.
    Four distinct path endpoints require their actual cut-side boundary order.
    A shared endpoint is explicitly uncovered, not silently accepted.
    """
    assert all(labels[e] in (a, c) for e in first["edges"])
    assert all(labels[e] in (b, c) for e in second["edges"])
    common = sorted(set(first["edges"]) & set(second["edges"]))
    assert all(labels[e] == c for e in common)
    if set(first["ends"]) & set(second["ends"]):
        return dict(status="uncovered_shared_endpoint", shared_edges=common)
    signs = epsilon(edges, labels, rotations, a, b, c)
    local = []
    for e in common:
        u, v = edges[e]
        # Distinct component endpoints exclude shared c edges incident to leaves
        # or cut ports; both attachment vertices are original cubic vertices.
        assert u in signs and v in signs
        local.append(dict(edge=e, endpoints=[u, v], epsilon=[signs[u], signs[v]],
                          crossing=int(signs[u] == signs[v])))
    lhs = sum(r["crossing"] for r in local) % 2
    if not first["ends"] or not second["ends"]:
        rhs, kind = 0, "closed_component"
    elif opposite_sides:
        assert not common
        rhs, kind = 0, "different_cut_sides"
    else:
        assert boundary_order is not None
        rhs = alternating(boundary_order, first["ends"], second["ends"])
        kind = "four_distinct_endpoints"
    return dict(status="checked", kind=kind, shared_edges=common, local_crossings=local,
                lhs=lhs, rhs=rhs, passed=lhs == rhs)


def theta_controls():
    edges, labels = [(0, 1)] * 3, [1, 2, 3]
    first = components(edges, labels, (1, 3))[0]
    second = components(edges, labels, (2, 3))[0]
    rows = []
    for reversed_second in (True, False):
        rotations = {0: [0, 1, 2], 1: [0, 2, 1] if reversed_second else [0, 1, 2]}
        topology = ribbon_faces(edges, rotations)
        parity = intersection_parity(edges, labels, rotations, first, second, 1, 2, 3)
        assert topology["genus"] == int(not reversed_second)
        assert parity["passed"] == reversed_second
        rows.append(dict(name="sphere_positive" if reversed_second else "torus_negative",
                         edges=edges, edge_colors=labels, rotations=rotations,
                         retained=[first, second], topology=topology, parity=parity))
    return dict(controls=rows, same_graph_and_coloring=True,
                claim="Rejects a fixed non-sphere rotation, not the unembedded theta graph or a count ray.")


def normalized_colorings(graph):
    """All proper primal colorings modulo ONE global S4 action, no ring quotient."""
    n = len(graph["vertices"])
    assert graph["vertices"] == list(range(n))
    previous = [[] for _ in range(n)]
    for u, v in graph["edges"]:
        previous[max(u, v)].append(min(u, v))
    values, result = [], []
    def visit():
        v = len(values)
        if v == n:
            result.append(tuple(values))
            return
        forbidden = {values[u] for u in previous[v]}
        for color in range(min(3, max(values, default=-1) + 1) + 1):
            if color not in forbidden:
                values.append(color)
                visit()
                values.pop()
    visit()
    assert all(all(f[u] != f[v] for u, v in graph["edges"]) for f in result)
    return result


def source_dual(graph):
    edges = [tuple(e) for e in graph["edges"]]
    faces, k = graph["faces"], len(graph["ring"])
    f = len(faces)
    by_edge = {e: i for i, e in enumerate(edges)}
    incidence = [[] for _ in edges]
    rotations = {}
    for v, face in enumerate(faces):
        rr = [by_edge[tuple(sorted((x, y)))] for x, y in zip(face, face[1:] + face[:1])]
        rotations[v] = rr
        for e in rr:
            incidence[e].append(v)
    boundary = []
    for j in range(k):
        e = by_edge[tuple(sorted((j, (j + 1) % k)))]
        incidence[e].append(f + j)
        rotations[f + j] = [e]
        boundary.append(e)
    assert all(len(vs) == 2 for vs in incidence)
    dual = [tuple(vs) for vs in incidence]
    # Closing all marked leaves to the exterior primal-face vertex verifies
    # both sphere topology and the specified terminal order.
    closed = [tuple(v if v < f else f for v in e) for e in dual]
    closed_rotations = {v: es for v, es in rotations.items() if v < f}
    closed_rotations[f] = list(reversed(boundary))
    topology = ribbon_faces(closed, closed_rotations)
    assert topology["genus"] == 0 and topology["face_count"] == len(graph["vertices"])
    return dual, rotations, topology


def cut_action(edges, labels, rotations, f, k, pair, strand):
    a, b = pair
    c = 6 - a - b
    start, end = [v - f for v in strand["ends"]]
    assert 0 <= start < end < k
    internal = strand["vertices"][1:-1]
    assert all(v < f for v in internal) and len(set(internal)) == len(internal)
    names = {v: "t%d" % i for i, v in enumerate(internal)}
    names.update({f + j: "e%d" % j for j in range(k)})
    side, ports = {}, []
    for i, v in enumerate(internal):
        incoming, outgoing = strand["edges"][i:i + 2]
        rr = rotations[v]
        z = int((rr.index(outgoing) - rr.index(incoming)) % 3 == 1)
        third = [e for e in rr if labels[e] == c]
        assert len(third) == 1 and third[0] not in strand["edges"]
        side[v] = z
        ports.append(dict(name=names[v], vertex=v, side=z, third_edge=third[0],
                          third_edge_endpoints=edges[third[0]]))
    arcs = [list(reversed(range(start + 1, end))),
            list(range(end + 1, k)) + list(range(start))]
    for z, arc in enumerate(arcs):
        side.update({f + j: z for j in arc})
    orders = [[v for v in internal if side[v] == z] + [f + j for j in arc]
              for z, arc in enumerate(arcs)]
    retained = [components(edges, labels, (x, c), strand["edges"]) for x in (a, b)]
    for system in retained:
        endpoints = [v for p in system for v in p["ends"]]
        assert len(endpoints) == len(set(endpoints))
        assert set(internal) <= set(endpoints)
        assert all(side[p["ends"][0]] == side[p["ends"][1]] for p in system if p["ends"])
        for z, order in enumerate(orders):
            paths = [p for p in system if p["ends"] and side[p["ends"][0]] == z]
            assert all(not alternating(order, p["ends"], q["ends"]) for p, q in combinations(paths, 2))
    checks = []
    for pi, p in enumerate(retained[0]):
        for qi, q in enumerate(retained[1]):
            same = (not p["ends"] or not q["ends"] or side[p["ends"][0]] == side[q["ends"][0]])
            order = orders[side[p["ends"][0]]] if p["ends"] and same else None
            check = intersection_parity(edges, labels, rotations, p, q, a, b, c,
                                        order, opposite_sides=not same)
            assert check["status"] != "checked" or check["passed"]
            checks.append(dict(first_component=pi, second_component=qi, **check))
    systems = []
    for x, system in zip((a, b), retained):
        systems.append(dict(pair=sorted((x, c)), components=[dict(
            p, named_ends=[names[v] for v in p["ends"]]) for p in system]))
    return dict(pair=pair, boundary_ends=[start, end], path=strand,
                ordered_ports=ports, boundary_arcs=arcs,
                cut_side_orders=[[names[v] for v in order] for order in orders],
                cut_side_vertex_orders=orders, retained=systems, parity_checks=checks)


def disk_control(saved):
    graph = saved["graph"]
    graph["positions"] = {int(v): p for v, p in graph["positions"].items()}
    geometry = validate_disk(graph)
    edges, rotations, topology = source_dual(graph)
    assert edges == [tuple(e) for e in saved["dual_edges"]]
    f, k = len(graph["faces"]), len(graph["ring"])
    states, actions = [], []
    for sid, colors in enumerate(normalized_colorings(graph)):
        labels = [colors[u] ^ colors[v] for u, v in graph["edges"]]
        epsilon(edges, labels, rotations, 1, 2, 3)
        states.append(dict(index=sid, primal_colors=colors, dual_edge_colors=labels))
        for pair in PAIRS:
            for path in components(edges, labels, pair):
                if path["ends"]:
                    action = cut_action(edges, labels, rotations, f, k, pair, path)
                    action["state"] = sid
                    actions.append(action)
    assert len(states) == 43 and len(actions) == 344
    histogram = Counter(c["status"] for row in actions for c in row["parity_checks"])
    kinds = Counter(c.get("kind", "uncovered_shared_endpoint") for row in actions for c in row["parity_checks"])
    assert histogram["checked"] > 0
    return dict(graph=graph, geometry=geometry, dual_edges=edges, dual_rotations=rotations,
                terminal_vertices=list(range(f, f + k)), closure_topology=topology,
                states=states, actions=actions, normalized_colorings=len(states),
                boundary_path_actions=len(actions), parity_status_histogram=dict(sorted(histogram.items())),
                parity_kind_histogram=dict(sorted(kinds.items())))


def report():
    receipt = json.loads(RECEIPT.read_text())
    assert sha256(OLD.read_bytes()).hexdigest() == receipt["sources_sha256"][str(OLD.relative_to(ROOT))]
    old = json.loads(OLD.read_text())
    controls = [disk_control(saved) for saved in old["plane_projection_control"]["controls"]]
    sources = [Path(__file__), CONFIG, OLD, RECEIPT]
    return dict(date="2026-10-29", scope="Named fixed ribbon realizations and two existing actual plane C8 controls; no Bernhart count-ray exclusion.",
                parity_contract=dict(formula="sum over common c edges uv of [epsilon(u)=epsilon(v)] = endpoint-alternation (mod 2)",
                                     epsilon="+1 for cyclic (a,b,c), -1 for its reverse, from original edge-ID rotations",
                                     covered="Retained mixed components with disjoint endpoints, including closed components.",
                                     uncovered="Shared endpoints need a separately proved endpoint push-off rule."),
                theta=theta_controls(), plane_controls=controls,
                excluded_Bernhart_coordinates=0, excluded_Bernhart_full_lift_rays=0,
                sources_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sources})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.check.read_text() == payload, "Retained parity certificate differs"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(dict(theta_genera=[r["topology"]["genus"] for r in result["theta"]["controls"]],
                          plane_controls=[dict(name=r["graph"]["name"], colorings=r["normalized_colorings"],
                                               actions=r["boundary_path_actions"], checks=r["parity_status_histogram"])
                                          for r in result["plane_controls"]],
                          excluded_Bernhart_coordinates=0), sort_keys=True))


if __name__ == "__main__":
    main()
