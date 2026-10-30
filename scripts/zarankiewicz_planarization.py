#!/usr/bin/env python3
"""Verify a complete good K_m,n crossing pattern by its oriented planarization.

All rotations use one orientation (counterclockwise, for example). JSON schema:
  m, n: positive integers;
  rotations_A[a]: cyclic list of the B-neighbors of a;
  rotations_B[b]: cyclic list of the A-neighbors of b;
  edge_orders: one {"edge": [a,b], "crossings": [id,...]} per edge,
               ordered from A to B;
  crossings: {"id": id, "edges": [[a,b],[c,d]],
              "rotation": ["0-","1-","0+","1+"]}.
Here 0/1 refer to the listed edges, and -/+ point along the edge toward A/B.
Either alternating cyclic order is allowed at a crossing. The rotations, labels,
and orders must all describe the SAME source. An accepted packet determines a
sphere drawing up to the usual smoothing of alternating degree-four vertices.
No tensor or collection of independent marginal witnesses is accepted as input.

Without a filename, replay exact positive and negative controls. With a filename,
verify that JSON packet. Only the standard library is used.
"""
from __future__ import annotations

import argparse
import copy
import json
import random
from fractions import Fraction
from functools import cmp_to_key
from functools import lru_cache
from itertools import combinations
from pathlib import Path


class InvalidPattern(ValueError):
    """The packet does not define the specified good crossing pattern."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InvalidPattern(message)


def analyze(packet: dict) -> dict:
    """Check the complete packet; malformed packets raise InvalidPattern.

    A well-formed packet can define an embedding of positive genus. Such a
    packet returns plane=False, accepted=False, and its Euler/genus diagnostics.
    """
    m, n = packet["m"], packet["n"]
    require(type(m) is int and type(n) is int and m > 0 and n > 0,
            "m and n must be positive integers")
    edges = [(a, b) for a in range(m) for b in range(n)]
    edge_set = set(edges)
    ra, rb = packet["rotations_A"], packet["rotations_B"]
    require(len(ra) == m and len(rb) == n, "missing original-vertex rotation")
    for row in ra:
        require(len(row) == n and set(row) == set(range(n)),
                "A rotation must list each B neighbor once")
    for row in rb:
        require(len(row) == m and set(row) == set(range(m)),
                "B rotation must list each A neighbor once")

    orders = {}
    for row in packet["edge_orders"]:
        edge = tuple(row["edge"])
        require(edge in edge_set and edge not in orders, "invalid/repeated original edge")
        word = row["crossings"]
        require(len(word) == len(set(word)), "an edge meets one crossing twice")
        orders[edge] = list(word)
    require(set(orders) == edge_set, "missing original-edge order")
    crosses = {}
    edge_pairs = set()
    for crossing in packet["crossings"]:
        cid = crossing["id"]
        require(type(cid) is int and cid >= 0 and cid not in crosses,
                "crossing ids must be distinct nonnegative integers")
        pair = tuple(tuple(e) for e in crossing["edges"])
        require(len(pair) == 2 and all(e in edge_set for e in pair),
                "crossing must list two original edges")
        e, f = pair
        require(e[0] != f[0] and e[1] != f[1], "adjacent edges cannot cross")
        key = frozenset(pair)
        require(key not in edge_pairs, "two original edges cross more than once")
        edge_pairs.add(key)
        ports = crossing["rotation"]
        require(len(ports) == 4 and set(ports) == {"0-", "0+", "1-", "1+"},
                "crossing must contain its four distinct signed ports")
        require(all(ports[i][0] != ports[(i + 1) % 4][0] for i in range(4)),
                "strands do not alternate at crossing")
        crosses[cid] = crossing
    occurrences = {cid: [] for cid in crosses}
    for edge, word in orders.items():
        for cid in word:
            require(cid in crosses, "edge order references an unknown crossing")
            occurrences[cid].append(edge)
    for cid, crossing in crosses.items():
        require(set(occurrences[cid]) == {tuple(e) for e in crossing["edges"]}
                and len(occurrences[cid]) == 2,
                "crossing labels and the two edge orders disagree")

    # Dart d^1 is its reverse. A segment of an original edge retains that edge's
    # identity even if two different segments have the same endpoint vertices.
    tails, heads = [], []
    outgoing = {}
    ends = {}
    signed_ports = {}
    for edge in edges:
        a, b = edge
        word = orders[edge]
        path = [("A", a)] + [("X", cid) for cid in word] + [("B", b)]
        forward = []
        for u, v in zip(path, path[1:]):
            d = len(tails)
            tails.extend((u, v))
            heads.extend((v, u))
            outgoing.setdefault(u, []).append(d)
            outgoing.setdefault(v, []).append(d ^ 1)
            forward.append(d)
        ends[("A", a, b)] = forward[0]
        ends[("B", b, a)] = forward[-1] ^ 1
        for k, cid in enumerate(word):
            signed_ports[(cid, edge, "-")] = forward[k] ^ 1
            signed_ports[(cid, edge, "+")] = forward[k + 1]

    rotations = {}
    for a in range(m):
        rotations[("A", a)] = [ends[("A", a, b)] for b in ra[a]]
    for b in range(n):
        rotations[("B", b)] = [ends[("B", b, a)] for a in rb[b]]
    for cid, crossing in crosses.items():
        pair = [tuple(e) for e in crossing["edges"]]
        rotations[("X", cid)] = [signed_ports[(cid, pair[int(p[0])], p[1])]
                                    for p in crossing["rotation"]]
    sigma = {}
    for vertex, darts in rotations.items():
        require(set(darts) == set(outgoing[vertex]), "incomplete local dart rotation")
        sigma.update(zip(darts, darts[1:] + darts[:1]))
    require(set(sigma) == set(range(len(tails))), "missing dart in rotation permutation")

    reached = {("A", 0)}
    stack = list(reached)
    while stack:
        vertex = stack.pop()
        for d in outgoing[vertex]:
            if heads[d] not in reached:
                reached.add(heads[d])
                stack.append(heads[d])
    require(len(reached) == len(rotations), "planarization is disconnected")
    phi = {d: sigma[d ^ 1] for d in sigma}
    unused = set(phi)
    faces = []
    while unused:
        d = min(unused)
        face = []
        current = d
        while current in unused:
            unused.remove(current)
            face.append(current)
            current = phi[current]
        require(current == d, "face permutation has an invalid orbit")
        faces.append(face)
    vertices, segments = len(rotations), len(tails) // 2
    chi = vertices - segments + len(faces)
    require(chi <= 2 and chi % 2 == 0, "invalid connected oriented Euler characteristic")
    ca = [[0] * m for _ in range(m)]
    cb = [[0] * n for _ in range(n)]
    for crossing in crosses.values():
        (a, b), (c, d) = crossing["edges"]
        ca[a][c] += 1
        ca[c][a] += 1
        cb[b][d] += 1
        cb[d][b] += 1
    total = len(crosses)
    require(sum(map(sum, ca)) == sum(map(sum, cb)) == 2 * total,
            "crossing matrix accounting failure")
    return {"accepted": chi == 2, "plane": chi == 2,
            "m": m, "n": n, "crossings": total,
            "vertices": vertices, "segments": segments, "faces": len(faces),
            "face_lengths": sorted(map(len, faces)),
            "euler_characteristic": chi, "orientable_genus": (2 - chi) // 2,
            "pair_crossings_A": ca, "pair_crossings_B": cb,
            "star_crossings_A": list(map(sum, ca)),
            "star_crossings_B": list(map(sum, cb))}


def determinant(u, v):
    return u[0] * v[1] - u[1] * v[0]


def subtract(u, v):
    return u[0] - v[0], u[1] - v[1]


def angle_compare(left, right):
    def half(v):
        return 0 if v[1] > 0 or (v[1] == 0 and v[0] > 0) else 1
    hl, hr = half(left[1]), half(right[1])
    if hl != hr:
        return -1 if hl < hr else 1
    cross = determinant(left[1], right[1])
    require(cross != 0, "coincident rays in straight-line control")
    return -1 if cross > 0 else 1


def straight_line_packet(m: int, n: int, seed: int) -> dict:
    """Construct a control packet from exact rational straight segments.

    Randomness chooses only integer vertex positions; intersections, order, and
    cyclic rotations are computed exactly. Degeneracies reject this seed.
    """
    rng = random.Random(seed)
    points = [(rng.randrange(100000), rng.randrange(100000)) for _ in range(m + n)]
    require(len(set(points)) == m + n, "coincident control vertices")
    for p, q, r in combinations(points, 3):
        require(determinant(subtract(q, p), subtract(r, p)) != 0,
                "three collinear control vertices")
    aa, bb = points[:m], points[m:]
    edges = [(a, b) for a in range(m) for b in range(n)]
    hits = {e: [] for e in edges}
    crossing_points = set()
    crosses = []
    for e, f in combinations(edges, 2):
        a, b = e
        c, d = f
        if a == c or b == d:
            continue
        p, q = aa[a], bb[b]
        r, s = aa[c], bb[d]
        v, w, offset = subtract(q, p), subtract(s, r), subtract(r, p)
        den = determinant(v, w)
        if den == 0:
            continue
        t = Fraction(determinant(offset, w), den)
        u = Fraction(determinant(offset, v), den)
        if not (0 < t < 1 and 0 < u < 1):
            continue
        point = p[0] + t * v[0], p[1] + t * v[1]
        require(point not in crossing_points, "multiple crossing in control")
        crossing_points.add(point)
        cid = len(crosses)
        hits[e].append((t, cid))
        hits[f].append((u, cid))
        rays = [("0-", (-v[0], -v[1])), ("0+", v),
                ("1-", (-w[0], -w[1])), ("1+", w)]
        ports = [p for p, _ in sorted(rays, key=cmp_to_key(angle_compare))]
        crosses.append({"id": cid, "edges": [list(e), list(f)], "rotation": ports})
    ra = [[b for b, _ in sorted([(b, subtract(bb[b], aa[a])) for b in range(n)],
                                key=cmp_to_key(angle_compare))] for a in range(m)]
    rb = [[a for a, _ in sorted([(a, subtract(aa[a], bb[b])) for a in range(m)],
                                key=cmp_to_key(angle_compare))] for b in range(n)]
    return {"m": m, "n": n, "rotations_A": ra, "rotations_B": rb,
            "control_coordinates": {"A": aa, "B": bb},
            "edge_orders": [{"edge": list(e), "crossings": [cid for _, cid in sorted(hits[e])]}
                            for e in edges], "crossings": crosses}


def planar_two_side(n: int) -> dict:
    return {"m": 2, "n": n, "rotations_A": [list(range(n)), list(reversed(range(n)))],
            "rotations_B": [[0, 1] for _ in range(n)],
            "edge_orders": [{"edge": [a, b], "crossings": []}
                            for a in range(2) for b in range(n)], "crossings": []}


@lru_cache(maxsize=None)
def cyclic_orders(size: int):
    # Support both direct script use and import as scripts.<module>.
    try:
        from .zarankiewicz_rotation_budget import CyclicOrders
    except ImportError:
        from zarankiewicz_rotation_budget import CyclicOrders
    return CyclicOrders(size)


def woodall_summary(packet: dict, result: dict) -> dict:
    """Compute both budgets from one accepted source, where odd size permits.

    These are finite checks of Woodall's identities on the control packets,
    not a proof of the external theorem or general unavoidability.
    """
    require(result["accepted"], "Woodall controls require an accepted plane source")
    summary = {}
    for side, opposite_size in (("A", packet["n"]), ("B", packet["m"])):
        if opposite_size < 3 or opposite_size % 2 == 0:
            summary[side] = {"checked": False,
                             "reason": "opposite-side size must be odd and at least three"}
            continue
        co = cyclic_orders(opposite_size)
        rotations = packet[f"rotations_{side}"]
        count = len(rotations)
        crossings = result[f"pair_crossings_{side}"]
        delta = [[0] * count for _ in range(count)]
        excess = [[0] * count for _ in range(count)]
        antisum = total_excess = 0
        for u, v in combinations(range(count), 2):
            distance = co.antipath_summary(rotations[u], rotations[v])[0]
            remainder = crossings[u][v] - distance
            assert remainder >= 0 and remainder % 2 == 0
            units = remainder // 2
            delta[u][v] = delta[v][u] = distance
            excess[u][v] = excess[v][u] = units
            antisum += distance
            total_excess += units
        assert result["crossings"] == antisum + 2 * total_excess
        summary[side] = {"checked": True, "opposite_side_size": opposite_size,
                         "delta": delta, "excess_units": excess,
                         "antisum": antisum, "total_excess_units": total_excess,
                         "C_equals_antisum_plus_twice_excess": True}
    return summary


def replay(output_dir: Path | None = None) -> dict:
    positive = {}
    packets = {}
    for n in (2, 3, 7):
        packet = planar_two_side(n)
        result = analyze(packet)
        assert result["accepted"] and result["crossings"] == 0
        result["woodall_budget"] = woodall_summary(packet, result)
        positive[f"planar_K2_{n}"] = result
        packets[f"planar_K2_{n}"] = packet
    for m, n, seed in ((3, 3, 7), (3, 4, 10), (5, 5, 4), (7, 7, 5)):
        packet = straight_line_packet(m, n, seed)
        result = analyze(packet)
        assert result["accepted"]
        result["woodall_budget"] = woodall_summary(packet, result)
        positive[f"straight_K{m}_{n}_seed{seed}"] = result
        packets[f"straight_K{m}_{n}_seed{seed}"] = packet
    negative = {}
    base = packets["straight_K3_3_seed7"]
    bad = copy.deepcopy(base)
    bad["crossings"][0]["rotation"] = ["0-", "0+", "1-", "1+"]
    try:
        analyze(bad)
        raise AssertionError("nonalternating control was accepted")
    except InvalidPattern as error:
        negative["nonalternating_crossing"] = str(error)
    bad = copy.deepcopy(base)
    cid = bad["crossings"][0]["id"]
    row = next(row for row in bad["edge_orders"] if cid in row["crossings"])
    row["crossings"].remove(cid)
    try:
        analyze(bad)
        raise AssertionError("one-sided crossing label was accepted")
    except InvalidPattern as error:
        negative["one_sided_crossing_label"] = str(error)
    bad = copy.deepcopy(planar_two_side(3))
    bad["rotations_A"][1].reverse()
    result = analyze(bad)
    assert not result["accepted"] and result["orientable_genus"] == 1
    negative["same_K2_3_rotations_on_torus"] = result
    base = packets["straight_K5_5_seed4"]
    for k, row in enumerate(base["edge_orders"]):
        if len(row["crossings"]) < 2:
            continue
        bad = copy.deepcopy(base)
        word = bad["edge_orders"][k]["crossings"]
        word[0], word[1] = word[1], word[0]
        result = analyze(bad)
        if not result["accepted"]:
            negative["one_edge_order_transposition"] = result
            break
    assert "one_edge_order_transposition" in negative
    report = {"scope": "complete labelled finite patterns; oriented planarization check",
              "positive_controls": positive, "negative_controls": negative,
              "general_unavoidability": "OPEN"}
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        for name, packet in packets.items():
            (output_dir / f"{name}.json").write_text(json.dumps(packet, indent=2) + "\n")
        (output_dir / "planarization.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", nargs="?", type=Path)
    parser.add_argument("--write-controls", type=Path)
    args = parser.parse_args()
    if args.packet is None:
        result = replay(args.write_controls)
    else:
        try:
            result = analyze(json.loads(args.packet.read_text()))
        except (InvalidPattern, KeyError, TypeError, ValueError) as error:
            result = {"accepted": False, "error": str(error)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.packet is not None and not result.get("accepted", False):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
