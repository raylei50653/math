#!/usr/bin/env python3
"""Complete RIP at common retained endpoints, with original-rotation correction.

The general disk lemma is a paper proof. This finite replay completes precisely
the 16 and 2,992 pairs left uncovered by the frozen retained-parity certificates.
It does not exclude a Bernhart count ray or identify y with ordinary PM counts.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import ck_bernhart_ray_local_witnesses as local
import ck_retained_intersection_parity as rip

ROOT = Path(__file__).resolve().parents[1]
OLD_DIR = ROOT / "audits/2026-10-29-bernhart-retained-parity"
DEFAULT = ROOT / "audits/2026-10-29-bernhart-endpoint-ray/endpoint-parity.json"


def closed_disk_topology(edges, rotations):
    """Close the ordered original terminal leaves at a common exterior vertex.

    Both frozen source families number terminal leaves in their actual positive
    boundary order. Including this order is stronger than the open graph genus.
    """
    leaves = sorted(v for v, rr in rotations.items() if len(rr) == 1)
    exterior = max(rotations) + 1
    closed_edges = [tuple(exterior if v in leaves else v for v in edge) for edge in edges]
    closed_rotations = {v: rr for v, rr in rotations.items() if v not in leaves}
    closed_rotations[exterior] = [rotations[v][0] for v in reversed(leaves)]
    return rip.ribbon_faces(closed_edges, closed_rotations)


def endpoint_parity(edges, labels, rotations, first, second, a, b, c,
                    positive_boundary_order, cut_ports):
    """Check the two equivalent endpoint-complete RIP formulas.

    The boundary order is oriented with the cut disk on its LEFT. At a shared
    cut port the rotation-induced split is P,Q if epsilon=+1 and Q,P otherwise.
    An original degree-one c leaf uses the canonical split P,Q. Every common
    original c edge is counted once, including a single-edge shared component.
    """
    shared = sorted(set(first["ends"]) & set(second["ends"]))
    assert shared and not first["cycle"] and not second["cycle"]
    assert set(first["ends"] + second["ends"]) <= set(positive_boundary_order)
    assert len(positive_boundary_order) == len(set(positive_boundary_order))
    eps = rip.epsilon(edges, labels, rotations, a, b, c)
    common = sorted(set(first["edges"]) & set(second["edges"]))
    assert all(labels[e] == c for e in common)
    for v in shared:
        # Both mixed systems end along the SAME original third-colour dart.
        incident = [e for e in common if v in edges[e]]
        assert len(incident) == 1
        assert v in cut_ports if v in eps else len(rotations[v]) == 1
    def expanded(rotation_induced):
        answer = []
        for v in positive_boundary_order:
            tags = [j for j, part in enumerate((first, second)) if v in part["ends"]]
            if rotation_induced and v in shared and v in cut_ports and eps[v] == -1:
                tags.reverse()
            answer.extend((v, tag) for tag in tags)
        assert len(answer) == 4 and len(set(answer)) == 4
        return answer
    p_ends = [(v, 0) for v in first["ends"]]
    q_ends = [(v, 1) for v in second["ends"]]
    canonical, natural = expanded(False), expanded(True)
    alt_canonical = rip.alternating(canonical, p_ends, q_ends)
    alt_rotation = rip.alternating(natural, p_ends, q_ends)
    # Original leaves have no original cubic epsilon: their explicit cap has +1.
    raw_sign = lambda v: eps.get(v, 1)
    pushed_sign = lambda v: 1 if v in shared else raw_sign(v)
    raw = sum(raw_sign(u) == raw_sign(v) for e in common for u, v in [edges[e]]) % 2
    pushed = sum(pushed_sign(u) == pushed_sign(v)
                 for e in common for u, v in [edges[e]]) % 2
    correction_ports = [v for v in shared if v in cut_ports and eps[v] == -1]
    correction = len(correction_ports) % 2
    assert pushed == raw ^ correction
    assert alt_rotation == alt_canonical ^ correction
    return dict(shared_endpoints=shared, shared_edges=common,
                raw_intersection=raw, boundary_correction=correction,
                negative_epsilon_shared_ports=correction_ports,
                canonical_endpoint_order=canonical, rotation_endpoint_order=natural,
                canonical_alternation=alt_canonical, rotation_alternation=alt_rotation,
                pushed_intersection=pushed,
                passed=(raw ^ correction) == alt_canonical and raw == alt_rotation)


def replay_action(edges, labels, rotations, action):
    """The frozen side orders follow S forward on BOTH sides.

    Their side=1 has retained interior on the left; side=0 has it on the right.
    This follows from the original CCW incoming/outgoing/c rotation. Reverse
    only side=0 to obtain the positive orders required by endpoint_parity.
    """
    a, b = action["pair"]
    c = 6 - a - b
    path = action["path"]
    ports = path["vertices"][1:-1]
    assert ports == [r["vertex"] for r in action["ordered_ports"]]
    for i, v in enumerate(ports):
        incoming, outgoing = path["edges"][i:i + 2]
        rr = rotations[v]
        side = int((rr.index(outgoing) - rr.index(incoming)) % 3 == 1)
        assert side == action["ordered_ports"][i]["side"]
        assert labels[incoming] != labels[outgoing] and {labels[incoming], labels[outgoing]} == {a, b}
    orders = [list(reversed(action["cut_side_vertex_orders"][0])),
              list(action["cut_side_vertex_orders"][1])]
    side_of = {v: side for side, order in enumerate(orders) for v in order}
    assert sum(map(len, orders)) == len(side_of)
    rows, histogram, negatives = [], Counter(), []
    for old in action["parity_checks"]:
        p_index, q_index = old["first_component"], old["second_component"]
        first = action["retained"][0]["components"][p_index]
        second = action["retained"][1]["components"][q_index]
        if old["status"] == "checked":
            # Recompute every previously covered pair with its frozen actual order.
            same = (not first["ends"] or not second["ends"] or
                    side_of[first["ends"][0]] == side_of[second["ends"][0]])
            order = orders[side_of[first["ends"][0]]] if first["ends"] and same else None
            check = rip.intersection_parity(edges, labels, rotations, first, second,
                                            a, b, c, order, opposite_sides=not same)
            assert check["passed"] and check["lhs"] == old["lhs"] and check["rhs"] == old["rhs"]
            histogram["previously_covered_rechecked"] += 1
            continue
        assert old["status"] == "uncovered_shared_endpoint"
        side = side_of[first["ends"][0]]
        check = endpoint_parity(edges, labels, rotations, first, second, a, b, c,
                                orders[side], set(ports))
        assert check["passed"]
        kinds = sorted("cut_port" if v in ports else "original_leaf" for v in check["shared_endpoints"])
        histogram["+".join(kinds)] += 1
        # Compact lossless check table: endpoints/edge identities come from frozen action.
        rows.append([p_index, q_index, side, check["shared_endpoints"], check["shared_edges"],
                     check["raw_intersection"], check["boundary_correction"],
                     check["canonical_alternation"], check["rotation_alternation"]])
        for v in sorted({v for e in check["shared_edges"] for v in edges[e]} - set(ports)):
            if len(rotations[v]) != 3:
                continue
            changed = {w: rr.copy() for w, rr in rotations.items()}
            changed[v].reverse()
            bad = endpoint_parity(edges, labels, changed, first, second, a, b, c,
                                  orders[side], set(ports))
            assert not bad["passed"]
            negatives.append(dict(vertex=v, original_rotation=rotations[v], changed_rotation=changed[v],
                                  first_component=p_index, second_component=q_index,
                                  positive=check, negative=bad,
                                  unchanged="Original graph, colours, full retained components, cut ports, boundary orders.",
                                  changed_ribbon_topology=rip.ribbon_faces(edges, changed),
                                  changed_boundary_closure_topology=closed_disk_topology(edges, changed)))
            break
    return dict(positive_side_orders=orders, checks=rows, histogram=dict(sorted(histogram.items()))), negatives


def report():
    receipt = json.loads((OLD_DIR / "RECEIPT.json").read_text())
    frozen = {}
    for filename in ("ray-local.json", "rotation-controls.json"):
        path = OLD_DIR / filename
        assert sha256(path.read_bytes()).hexdigest() == receipt["sources_sha256"][str(path.relative_to(ROOT))]
        frozen[filename] = json.loads(path.read_text())
    # Complete source replay: the new checker does not silently trust old pair tables.
    assert json.loads(json.dumps(rip.report())) == frozen["rotation-controls.json"]
    assert json.loads(json.dumps(local.report())) == frozen["ray-local.json"]
    sources, controls, negatives = [], [], []
    for group in frozen["rotation-controls.json"]["plane_controls"]:
        rotations = {int(v): rr for v, rr in group["dual_rotations"].items()}
        assert closed_disk_topology(group["dual_edges"], rotations)["genus"] == 0
        actions, histogram = [], Counter()
        for ai, action in enumerate(group["actions"]):
            labels = group["states"][action["state"]]["dual_edge_colors"]
            result, bad = replay_action(group["dual_edges"], labels, rotations, action)
            histogram.update(result["histogram"])
            actions.append(dict(action=ai, **result))
            if bad and not any(r["source"] == group["graph"]["name"] for r in negatives):
                negatives.append(dict(source=group["graph"]["name"], action=ai, **bad[0]))
        controls.append(dict(source=group["graph"]["name"], actions=actions,
                             histogram=dict(sorted(histogram.items()))))
    for ray in frozen["ray-local.json"]["rays"]:
        edges = [tuple(int(v[1:]) if v.startswith("v") else local.F+int(v[1:])
                       for v in row["ends"]) for row in ray["source"]["edges"]]
        labels = [row["color"] for row in ray["source"]["edges"]]
        rotations = {int(v[1:]) if v.startswith("v") else local.F+int(v[1:]): rr
                     for v, rr in ray["source"]["original_edge_id_rotations"].items()}
        assert closed_disk_topology(edges, rotations)["genus"] == 0
        actions, histogram = [], Counter()
        for ai, saved in enumerate(ray["actions"]):
            action = saved["retained_intersection_parity"]
            result, bad = replay_action(edges, labels, rotations, action)
            histogram.update(result["histogram"])
            actions.append(dict(action=ai, **result))
            if bad and not any(r["source"] == f"ray_{ray['ray']}_local" for r in negatives):
                negatives.append(dict(source=f"ray_{ray['ray']}_local", action=ai, **bad[0]))
        sources.append(dict(source=f"ray_{ray['ray']}_local", actions=actions,
                            histogram=dict(sorted(histogram.items()))))
    def counts(groups):
        histogram = sum((Counter(r["histogram"]) for r in groups), Counter())
        previous = histogram.pop("previously_covered_rechecked")
        return dict(previously_covered_rechecked=previous, shared_endpoints_completed=sum(histogram.values()),
                    endpoint_kinds=dict(sorted(histogram.items())))
    totals = dict(local=counts(sources), wheel_and_stack=counts(controls))
    assert totals["local"]["previously_covered_rechecked"] == 40
    assert totals["local"]["shared_endpoints_completed"] == 16
    assert totals["wheel_and_stack"]["previously_covered_rechecked"] == 7124
    assert totals["wheel_and_stack"]["shared_endpoints_completed"] == 2992
    assert len(negatives) == 4
    assert all(r["changed_boundary_closure_topology"]["genus"] > 0 for r in negatives)
    dependencies = [Path(__file__), Path(rip.__file__), Path(local.__file__),
                    OLD_DIR / "ray-local.json", OLD_DIR / "rotation-controls.json", OLD_DIR / "RECEIPT.json"]
    return dict(date="2026-10-29", scope="Endpoint-complete RIP paper lemma; exact finite replay of all old uncovered pairs.",
                contract=dict(positive_boundary="Disk interior on left; reverse frozen side-0 order only.",
                              natural_push_off="Shared cut port: P,Q for epsilon=+1; Q,P for epsilon=-1. Original leaf: P,Q.",
                              canonical_push_off="P,Q at every common endpoint in the positive boundary direction.",
                              leaf_epsilon="Artificial cap epsilon=+1; no epsilon claimed for an original degree-one vertex.",
                              raw="L=sum_common_c_edges [bar_epsilon(u)=bar_epsilon(v)] mod 2; bar_epsilon=epsilon at cubic vertices, +1 at leaves.",
                              correction="B=sum_shared_cut_ports [epsilon(v)=-1] mod 2.",
                              formulas=["L=Alt_rotation mod 2", "L+B=Alt_canonical mod 2"],
                              table_columns=["first_component", "second_component", "side", "shared_endpoints", "shared_edges", "L", "B", "Alt_canonical", "Alt_rotation"]),
                old_certificates_replayed_exactly=True, local_controls=sources, plane_controls=controls,
                reversed_rotation_negative_controls=negatives, totals=totals,
                excluded_full_lift_rays=[], excluded_coordinates=[], new_Lean=False,
                sources_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.check.read_text() == payload, "Endpoint parity certificate differs"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(dict(totals=result["totals"], rotation_negatives=len(result["reversed_rotation_negative_controls"]),
                          excluded_full_lift_rays=[], excluded_coordinates=[]), sort_keys=True))


if __name__ == "__main__":
    main()
