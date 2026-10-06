#!/usr/bin/env python3
"""C44': exhaustive two-private-vertex degree-(4,4) placement classification.

The colour decision uses lists left by literal boundary colours. Disk decisions
use the elementary star-sector criterion and a separately checked augmented
planar rotation. No saved Sigma and no four-colour-theorem oracle are used.
Outputs are deterministic and --check recomputes exact bytes without writes.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_excess_two_c44p"
REPS = (
    (0, 1, 0, 1, 2), (0, 1, 0, 2, 1), (0, 1, 0, 2, 3),
    (0, 1, 2, 0, 1), (0, 1, 2, 0, 2), (0, 1, 2, 0, 3),
    (0, 1, 2, 1, 2), (0, 1, 2, 1, 3), (0, 1, 2, 3, 1),
    (0, 1, 2, 3, 2),
)
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
GROUP = tuple(product((1, -1), range(5), (False, True)))


def encode(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":")) + "\n").encode()


def emit(path, data, check):
    if check:
        assert path.read_bytes() == data, f"byte replay mismatch: {path}"
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(data)
    return {"path": str(path.relative_to(ROOT)), "bytes": len(data),
            "sha256": sha256(data).hexdigest()}


def normalized(row):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in row)


def target_images():
    """Transport all five coordinates together, then apply one S4 quotient."""
    index = {q: i for i, q in enumerate(REPS)}
    answer = []
    for target, sign, rotation in product((933, 941), (1, -1), range(5)):
        frame_map = [(sign * i + rotation) % 5 for i in range(5)]
        row_map = []
        for q in REPS:
            moved = [None] * 5
            for i, c in enumerate(q):
                moved[frame_map[i]] = c
            row_map.append(index[normalized(moved)])
        assert sorted(row_map) == list(range(10))
        accepted = sorted(row_map[i] for i in range(10) if target >> i & 1)
        answer.append({"target_sigma": target, "sign": sign,
                       "rotation": rotation, "frame_map": frame_map,
                       "row_map": row_map, "accepted_rows": accepted,
                       "sigma_mask": sum(1 << i for i in accepted)})
    return answer


IMAGES = target_images()


def placement_id(adjacent, a, b):
    return f'{"AD" if adjacent else "NA"}-' + "".join(map(str, a)) + "-" + "".join(map(str, b))


def full_edges(adjacent, a, b):
    return tuple(sorted(FRAME | {(i, 5) for i in a} | {(i, 6) for i in b}
                        | ({(5, 6)} if adjacent else set())))


def color_decision(edges, row_index):
    """An independent list calculation for exactly two private vertices."""
    q = REPS[row_index]
    domains = {}
    for root in (5, 6):
        forbidden = {q[v] for e in edges if root in e
                     for v in e if v < 5}
        domains[str(root)] = [c for c in range(4) if c not in forbidden]
    linked = (5, 6) in edges
    pairs = [(c, d) for c in domains["5"] for d in domains["6"]
             if not linked or c != d]
    witness = list(q) + list(pairs[0]) if pairs else None
    if witness:
        assert all(witness[u] != witness[v] for u, v in edges)
    rejection = None
    if not pairs:
        empty = [root for root in (5, 6) if not domains[str(root)]]
        if empty:
            rejection = {"kind": "empty_root_list", "roots": empty,
                         "domains": domains}
        else:
            assert linked and domains["5"] == domains["6"] and len(domains["5"]) == 1
            rejection = {"kind": "adjacent_equal_singleton_lists",
                         "edge": [5, 6], "forced_color": domains["5"][0],
                         "domains": domains}
    return {"domains": domains, "accepted": bool(pairs),
            "accepted_witness": witness, "accepted_root_pairs": [list(p) for p in pairs],
            "rejection_witness": rejection}


def minimal_subcores(edges, row_index):
    """Enumerate all inclusion-minimal rejecting edge subgraphs (<=256)."""
    private_edges = tuple(e for e in edges if e not in FRAME)
    answer = []
    for subset in range(1 << len(private_edges)):
        chosen = tuple(e for i, e in enumerate(private_edges) if subset >> i & 1)
        candidate = tuple(sorted(FRAME | set(chosen)))
        if color_decision(candidate, row_index)["accepted"]:
            continue
        witnesses = []
        for e in chosen:
            decision = color_decision(tuple(x for x in candidate if x != e), row_index)
            if not decision["accepted"]:
                break
            witnesses.append({"edge": list(e), "accepted_witness": decision["accepted_witness"]})
        else:
            present = sorted({v for e in chosen for v in e if v >= 5})
            answer.append({"edges": [list(e) for e in candidate], "private_vertices": present,
                           "rejection_witness": color_decision(candidate, row_index)["rejection_witness"],
                           "edge_deletion_witnesses": witnesses})
    return sorted(answer, key=lambda c: c["edges"])


def star_sectors(a):
    """Closed boundary arc between consecutive contacts of the first root."""
    sectors = []
    for start, stop in zip(a, a[1:] + a[:1]):
        arc = [start]
        while arc[-1] != stop:
            arc.append((arc[-1] + 1) % 5)
        sectors.append(arc)
    return sectors


def face_walks(rotation):
    unseen = {(u, v) for u in rotation for v in rotation[u]}
    answer = []
    while unseen:
        start = min(unseen)
        dart = start
        face = []
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            face.append(u)
            around = rotation[v]
            dart = (v, around[(around.index(u) - 1) % len(around)])
            if dart == start:
                break
        answer.append(face)
    return answer


def disk_certificate(edges, a, b):
    sectors = star_sectors(a)
    eligible = [i for i, arc in enumerate(sectors) if set(b) <= set(arc)]
    graph = nx.Graph()
    graph.add_nodes_from(range(8))
    graph.add_edges_from(edges)
    graph.add_edges_from((i, 7) for i in range(5))
    planar, embedding = nx.check_planarity(graph, counterexample=True)
    assert planar == bool(eligible), (a, b, eligible, planar)
    answer = {"embeddable": planar, "criterion_sectors": sectors,
              "eligible_sector_indices": eligible}
    if not planar:
        answer["impossibility_witness"] = {
            "kind": "second_star_contacts_not_in_one_first_star_sector",
            "outside_each_sector": [sorted(set(b) - set(arc)) for arc in sectors],
            "networkx_kuratowski_subgraph_edges": [list(e) for e in sorted(tuple(sorted(e)) for e in embedding.edges())],
        }
        return answer
    embedding.check_structure()
    augmented = {v: list(embedding.neighbors_cw_order(v)) for v in range(8)}
    aug_faces = face_walks(augmented)
    assert 8 - len(graph.edges()) + len(aug_faces) == 2
    disk = {v: [u for u in augmented[v] if u != 7] for v in range(7)}
    disk_faces = face_walks(disk)
    assert 7 - len(edges) + len(disk_faces) == 2
    boundary_faces = [f for f in disk_faces if len(f) == 5 and set(f) == set(range(5))]
    assert len(boundary_faces) == 1
    answer["embedding"] = {
        "apex": 7, "augmented_rotation": {str(v): around for v, around in augmented.items()},
        "augmented_faces": aug_faces, "augmented_euler": 2,
        "disk_rotation": {str(v): around for v, around in disk.items()},
        "disk_faces": disk_faces, "disk_euler": 2, "outer_face": boundary_faces[0],
    }
    return answer


def compatibility(mask, rows):
    matching = []
    exclusions = []
    for image in IMAGES:
        missing = [i for i in image["accepted_rows"] if not (mask >> i & 1)]
        if not missing:
            matching.append(image)
        else:
            qi = missing[0]
            assert rows[qi]["rejection_witness"] is not None
            exclusions.append({**image, "missing_row_index": qi,
                               "missing_literal_row": list(REPS[qi]),
                               "rejection_witness": rows[qi]["rejection_witness"]})
    return {"compatible": bool(matching), "matching_images": matching,
            "exclusions": exclusions}


def transport(edges, sign, rotation, swap):
    def vertex(v):
        return (sign * v + rotation) % 5 if v < 5 else 11 - v if swap else v
    return tuple(sorted(tuple(sorted((vertex(u), vertex(v)))) for u, v in edges))


def group_record(element):
    sign, rotation, swap = element
    return {"sign": sign, "rotation": rotation, "root_swap": swap,
            "frame_map": [(sign * i + rotation) % 5 for i in range(5)]}


def make_placement(adjacent, a, b):
    edges = full_edges(adjacent, a, b)
    rows = []
    for qi, q in enumerate(REPS):
        decision = color_decision(edges, qi)
        row = {"row_index": qi, "literal_row": list(q), **decision}
        if not decision["accepted"]:
            deletions = []
            for e in edges:
                if e in FRAME:
                    continue
                minus = color_decision(tuple(x for x in edges if x != e), qi)
                deletions.append({"edge": list(e), "accepted": minus["accepted"],
                                  "accepted_witness": minus["accepted_witness"],
                                  "rejection_witness": minus["rejection_witness"]})
            row["edge_deletion_audit"] = deletions
            row["whole_graph_minimal"] = all(d["accepted"] for d in deletions)
            row["minimal_cores"] = minimal_subcores(edges, qi)
            assert bool(row["minimal_cores"])
            assert row["whole_graph_minimal"] == (len(row["minimal_cores"]) == 1
                                                   and row["minimal_cores"][0]["edges"] == [list(e) for e in edges])
        rows.append(row)
    accepted = [qi for qi, row in enumerate(rows) if row["accepted"]]
    rejected = [qi for qi, row in enumerate(rows) if not row["accepted"]]
    mask = sum(1 << qi for qi in accepted)
    images = [(transport(edges, *element), element) for element in GROUP]
    canonical, element = min(images, key=lambda x: (x[0], GROUP.index(x[1])))
    ca = tuple(u for u, v in canonical if v == 5 and u < 5)
    cb = tuple(u for u, v in canonical if v == 6 and u < 5)
    cid = placement_id(adjacent, ca, cb)
    return {
        "id": placement_id(adjacent, a, b), "adjacent": adjacent,
        "spokes": {"5": list(a), "6": list(b)}, "edges": [list(e) for e in edges],
        "private_vertices": [5, 6], "root_degrees": [4, 4],
        "disk": disk_certificate(edges, a, b), "rows": rows,
        "sigma_mask": mask, "accepted_rows": accepted, "rejected_rows": rejected,
        "whole_graph_minimal_rejected_rows": [qi for qi in rejected if rows[qi]["whole_graph_minimal"]],
        "compatibility": compatibility(mask, rows),
        "orbit": {"id": cid, "canonical_id": cid,
                  "size": len({es for es, element in images}),
                  "stabilizer_size": sum(es == edges for es, element in images),
                  "canonical_group_element": group_record(element)},
    }


def table(placements, orbits):
    lines = ["# Two-private-vertex (4,4) full literal placement table", "",
             "All 125 placements are kept, including the 95 disk-impossible abstract graphs. "
             "Rows refer to the fixed ten-row REPS order. W means rows for which the whole graph "
             "is inclusion-minimal. Compatibility is the necessary full-Sigma inclusion test, "
             "including every D5 image; a compatible abstract graph need not be a disk.", "",
             "| Literal placement | D5 x root-swap representative | Disk | Sigma | Rejected rows | W | Compatible | Matching targets |",
             "| --- | --- | --- | ---: | --- | --- | --- | --- |"]
    for rec in placements:
        targets = sorted({m["target_sigma"] for m in rec["compatibility"]["matching_images"]})
        lines.append("| " + " | ".join([
            rec["id"], rec["orbit"]["id"], "yes" if rec["disk"]["embeddable"] else "no",
            str(rec["sigma_mask"]), ",".join(map(str, rec["rejected_rows"])) or "empty",
            ",".join(map(str, rec["whole_graph_minimal_rejected_rows"])) or "empty",
            "yes" if rec["compatibility"]["compatible"] else "no", ",".join(map(str, targets)) or "none",
        ]) + " |")
    lines += ["", "The 12 group orbits (nine AD, three NA) are:", "",
              "| Representative | Literal count | Stabilizer | Disk | Sigma | Compatible |",
              "| --- | ---: | ---: | --- | ---: | --- |"]
    for rec in orbits:
        lines.append("| " + " | ".join([rec["id"], str(rec["literal_count"]), str(rec["stabilizer_size"]),
                                         "yes" if rec["disk"] else "no", str(rec["sigma_mask"]),
                                         "yes" if rec["compatible"] else "no"]) + " |")
    return ("\n".join(lines) + "\n").encode()


PROOF = """C44' two-private-vertex classification: paper proof and scope

Definitions and complete coverage.
Fix the ordered induced boundary C5, labelled 0,1,2,3,4. The only private
vertices are named roots r=5 and s=6, each of degree four. A finite simple
graph on these seven vertices has no other possible private edge than rs.
If rs is present, each root has exactly three distinct boundary spokes;
there are binomial(5,3)^2=100 ordered spoke pairs. If rs is absent, each
has four distinct boundary spokes, giving binomial(5,4)^2=25 pairs. Thus
the 125 literal rows cover every graph of this shape, with no source-size
or source-degree hypothesis. D5 acts simultaneously on all five boundary
positions; root swap exchanges the two complete spoke sets. Their 20
maps give all equivalences, and the edge-set minimum is only a quotient
representative. Every literal placement remains in the saved table.

Disk criterion and the nonadjacent impossibility proof.
Draw the first root's star. Its contacts occur in the fixed cyclic order.
The star divides the disk into sectors whose boundary arcs run between
consecutive star contacts; this follows by applying the Jordan theorem
to the boundary arc together with the two spokes. The second root lies
in the interior of one sector. Every one of its spokes must end on that
sector's closed boundary arc, since crossing a bounding spoke is forbidden.
Thus its spoke set must be contained in one of those arcs. Conversely,
if its contacts lie in one arc, place the second root in that sector and
draw its spokes as a fan there. When present, rs is one more fan edge to
the first root on the boundary of the same sector. This constructs the
required disk embedding and proves the exact sector criterion.

For four first-root contacts, only one boundary vertex is missing. Every
closed sector arc has at most three boundary vertices. Four second-root
contacts cannot fit in any sector. Hence all 25 nonadjacent placements
are disk-impossible, on paper, independently of the planarity software.

For three first-root contacts, the five possible consecutive triples
have one sector of four boundary vertices and two sectors of two vertices.
There are four choices of a three-set in the large sector, giving 20
placements. The other five triples have two three-vertex sectors and one
two-vertex sector. Each three-vertex sector supplies one choice, giving
10 more. Thus exactly 30 adjacent literal placements are disks. All
remaining 70 adjacent placements are excluded by the same Jordan sector
argument. Explicit genus-zero rotations are saved for all 30 disks,
and Kuratowski subgraph edges corroborate each impossibility decision.

Full relation and minimal cores.
For a literal boundary row q, let L_r be the four colours minus the
colours at r's spoke contacts, and similarly define L_s. Without rs,
extension is exactly nonemptiness of both lists. With rs, extension is
exactly existence of unequal a in L_r and b in L_s. Both assertions are
immediate since there are exactly two private vertices.

In the adjacent case each list is nonempty. Rejection occurs exactly
when both lists are the same singleton {c}. Each triple therefore sees
the same three distinct boundary colours. Every retained spoke is
essential: deleting it frees its distinct boundary colour for that root,
while the other root keeps c. Deleting rs allows both roots to take c.
Thus every rejected row of an adjacent placement has the whole graph as
its unique inclusion-minimal core. The all-edge-subsets enumeration
records this independently of the elementary minimality argument.

In the nonadjacent case rejection means some root sees all four colours
on its four spokes. That root's four-spoke star is inclusion-minimal:
each deletion frees the formerly excluded colour. The other root can
be discarded. If both roots see all four colours, there are exactly two
such minimal stars; otherwise there is exactly one. No whole nonadjacent
placement is a minimal rejected-row core. All such abstract graphs are
already excluded by the disk proof.

The two disk orbits and compatibility.
The 30 disk placements reduce to two D5 times root-swap orbits. Their
representatives have r contacts 012 and s contacts 023 (20 literals),
or r contacts 012 and s contacts 034 (10 literals), with rs present.
For 012/023 the full relation has mask 831; its rejected row indices
are 6,7. Row 7 is a four-colour T4 row. Every D5 image of 933 and 941
contains every T4 row, so this orbit is incompatible.
For 012/034 the full relation has mask 959; its only rejected row is
index 6, q=01212. Every D5 image of 933 rejects four of the five
three-colour rows, and every D5 image of 941 rejects three. Rotations
act transitively on the five singleton positions, so there are images
of each target rejecting index 6. Each such image is contained in 959.
Therefore all 10 placements in the second orbit are compatible.

Named witness C44P-AD2-012-034.
Its nonframe edges are 05,15,25,06,36,46,56. At rejected row 01212,
the two roots each see boundary colours 0,1,2 and are forced to 3;
the root edge rejects that assignment. This graph is a disk by the
sector between first-root contacts 2 and 0 through 3 and 4. Its exact
Sigma is 959, and matching full-frame D5 target images, every accepted
colouring, seven deletion witnesses and a genus-zero rotation are saved
in named_C44P-AD2-012-034.json.

Trust and stop point.
Completeness of the 125 placements, the disk criterion, nonadjacent
impossibility, the list extension criterion, minimality arguments and
the two orbit descriptions are elementary finite paper arguments.
The full named tables, exact transported target images and rotations
are Python certificates, cross-checked by a separate implementation.
NetworkX planarity is corroborative, since disk decisions have the
sector proof and embeddable cases have explicit rotations. No four-
colour-theorem oracle, new source search, Lean formalization, or claim
of realization inside a full-Sigma=933/941 source is made. Compatibility
is a necessary inclusion condition, never a realizability certificate.
The all-incompatible branch fails: no no-two-private-core lemma and no
arbitrary-size no-two-root-(4,4)-core theorem follows. Stop generalizing.
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    placements = []
    for adjacent in (True, False):
        contacts = tuple(combinations(range(5), 3 if adjacent else 4))
        for a, b in product(contacts, repeat=2):
            placements.append(make_placement(adjacent, a, b))
    assert len(placements) == 125
    by_id = {rec["id"]: rec for rec in placements}
    counts = Counter(rec["orbit"]["id"] for rec in placements)
    orbits = []
    for cid, count in sorted(counts.items()):
        rec = by_id[cid]
        assert count == rec["orbit"]["size"]
        assert count * rec["orbit"]["stabilizer_size"] == 20
        orbits.append({"id": cid, "literal_count": count,
                       "stabilizer_size": rec["orbit"]["stabilizer_size"],
                       "disk": rec["disk"]["embeddable"], "sigma_mask": rec["sigma_mask"],
                       "compatible": rec["compatibility"]["compatible"],
                       "members": [r["id"] for r in placements if r["orbit"]["id"] == cid]})
    summary = {}
    for adjacent, label in ((True, "AD"), (False, "NA")):
        pop = [r for r in placements if r["adjacent"] == adjacent]
        disk = [r for r in pop if r["disk"]["embeddable"]]
        summary[label] = {
            "placements": len(pop), "orbits": len({r["orbit"]["id"] for r in pop}),
            "disk_placements": len(disk), "disk_orbits": len({r["orbit"]["id"] for r in disk}),
            "compatible_abstract_placements": sum(r["compatibility"]["compatible"] for r in pop),
            "compatible_disk_placements": sum(r["compatibility"]["compatible"] for r in disk),
            "compatible_disk_orbits": len({r["orbit"]["id"] for r in disk if r["compatibility"]["compatible"]}),
            "whole_minimal_disk_placements": sum(bool(r["whole_graph_minimal_rejected_rows"]) for r in disk),
            "whole_minimal_disk_row_occurrences": sum(len(r["whole_graph_minimal_rejected_rows"]) for r in disk),
        }
    assert summary["AD"]["disk_placements"] == 30
    assert summary["AD"]["compatible_disk_placements"] == 10
    assert summary["NA"]["disk_placements"] == 0
    witness = by_id["AD-012-034"]
    assert witness["sigma_mask"] == 959 and witness["rejected_rows"] == [6]
    payload = {"schema": "c5-c44p-two-private-v1", "frame": list(range(5)),
               "roots": [5, 6], "row_order": [list(q) for q in REPS],
               "target_images": IMAGES, "networkx_version": nx.__version__,
               "summary": summary, "orbits": orbits, "placements": placements,
               "branch": "compatible_core_stop_generalizing",
               "named_core": "C44P-AD2-012-034"}
    named = {"schema": "c5-c44p-named-core-v1", "name": "C44P-AD2-012-034",
             "placement": witness, "scope": "necessary Sigma compatibility; target-source realization not proved"}
    emitted = [
        emit(OUT / "two_private.json", encode(payload), args.check),
        emit(OUT / "two_private_table.md", table(placements, orbits), args.check),
        emit(OUT / "two_private_proof.txt", PROOF.encode(), args.check),
        emit(OUT / "named_C44P-AD2-012-034.json", encode(named), args.check),
    ]
    print(json.dumps({"summary": summary, "outputs": emitted, "byte_replay": args.check}, sort_keys=True))


if __name__ == "__main__":
    main()
