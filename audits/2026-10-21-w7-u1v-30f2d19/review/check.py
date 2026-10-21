#!/usr/bin/env python3
"""Fresh independent review of A -> M -> F for the actual original u1-v.

Reads the original pinned caps and full orbit family. It does not import any
u3v/u1v discovery, closure, transport checker, or derived six-column result.
Boundary components are recovered by pairwise constant low-bit differences.
No LP, source-graph enumeration, reflection, or marginal gluing is used.
"""
from collections import defaultdict
from copy import deepcopy
import argparse
import gzip
from hashlib import sha256
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = HERE.parents[2]
SOURCE = "audits/2026-10-20-r6-941-j1-five-edge-417732f"
PARENT = "audits/2026-10-21-w7-structural-30f2d19"
IDS = [68, 69, 78, 79, 88, 89, 92, 93]
NAMES = ["a", "n", "u4", "u3", "u2", "u1", "L", "q", "c", "s", "v", "w", "t"]
A = [0, 1, 2, 1, 2, 1, 2, 3, 1, 2, 0, 1, 2]
M = [0, 1, 2, 1, 2, 1, 2, 0, 2, 1, 3, 1, 2]
F = [0, 1, 2, 1, 2, 1, 2, 0, 2, 3, 1, 3, 2]
J = [147448, 147449, 167802, 226130, 231666]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pinned_bytes(name, manifest, hashes):
    entry = next(item for item in manifest["inputs"] if item["path"] == name)
    data = (ROOT / name).read_bytes()
    digest = sha256(data).hexdigest()
    require(len(data) == entry["bytes"] and digest == entry["sha256"],
            "frozen input drift: " + name)
    hashes[name] = digest
    return data


def encode(row):
    return sum(c << (2 * (12 - i)) for i, c in enumerate(row))


def decode(code):
    return [(code >> (2 * (12 - i))) & 3 for i in range(13)]


def canonical(row):
    labels = {}
    answer = []
    for colour in row:
        if colour not in labels:
            labels[colour] = len(labels)
        answer.append(labels[colour])
    return answer


def proper_rim(row):
    return all(row[i] != row[(i + 1) % 13] for i in range(13))


def components_from_constant_differences(column):
    """Same-palette vertices coflip iff their low-bit difference is constant.

    This uses pairwise relations rather than the transport checker's variation
    profile keys. All independent component flips must be present; regeneration
    below checks the resulting complete normalized coset exactly.
    """
    rows = [decode(code) for code in column]
    reference = rows[0]
    require(all([x // 2 for x in row] == [x // 2 for x in reference] for row in rows),
            "a full column changes palette membership")
    parent = list(range(13))

    def find(i):
        while parent[i] != i:
            i = parent[i]
        return i

    for i in range(13):
        for j in range(i):
            if reference[i] // 2 == reference[j] // 2:
                differences = {(row[i] ^ row[j]) & 1 for row in rows}
                if len(differences) == 1:
                    parent[find(i)] = find(j)
    groups = defaultdict(list)
    for i in range(13):
        groups[find(i)].append(i)
    blocks = sorted(groups.values(), key=min)
    anchors = {next(b for b, block in enumerate(blocks)
                    if reference[block[0]] // 2 == side) for side in (0, 1)}
    generated = [column[0]]
    for b, block in enumerate(blocks):
        if b not in anchors:
            mask = sum(1 << (2 * (12 - i)) for i in block)
            generated += [code ^ mask for code in generated]
    require(sorted(generated) == column,
            "recovered components fail to regenerate the complete coset")
    return [[NAMES[i] for i in block] for block in blocks]


def containing(blocks, vertex):
    found = [block for block in blocks if vertex in block]
    require(len(found) == 1, "a vertex lacks a unique recovered component")
    return found[0]


def flip(row, vertices, palette):
    answer = list(row)
    for name in vertices:
        i = NAMES.index(name)
        require(answer[i] in palette, "wrong actual palette for the proposed component")
        answer[i] = palette[1] if answer[i] == palette[0] else palette[0]
    return answer


def proposal():
    return dict(
        scope="strict original W7 source; same full D fibres; original u1-v",
        required_extra_edges=[["u1", "v"]], profile_ids=IDS,
        all_complete_D_fibres=True,
        A_support=[306985], M_support=J,
        first_q_component=["q", "v"], first_c_component=["c", "s"],
        second_v_component=["s", "v", "w"],
        middle_state=44111, terminal_state=44127,
        zero_columns=[48617, 67755])


def verify(cert, facts):
    require(cert["scope"] == "strict original W7 source; same full D fibres; original u1-v",
            "source scope changed")
    require(cert["all_complete_D_fibres"] is True,
            "the argument was restricted to an unproved invariant subfamily")
    require(cert["profile_ids"] == IDS, "eight-profile coverage changed")
    require(cert["required_extra_edges"] == [["u1", "v"]],
            "the proof acquired another extra-edge prerequisite")
    for profile in facts["profiles"]:
        require(all(edge in profile["original_chords"] for edge in cert["required_extra_edges"]),
                "a covered original profile lacks a required extra edge")
    require(cert["A_support"] == facts["incidence"][12302027] == [306985],
            "A's complete original incidence was not used")
    require(cert["M_support"] == facts["incidence"][10064313] == J,
            "M's complete original incidence was not used")
    first = facts["columns"][306985]["boundary_components"]
    require(cert["first_q_component"] == containing(first, "q") == ["q", "v"] and
            cert["first_c_component"] == containing(first, "c") == ["c", "s"],
            "first operation does not use whole actual boundary components")
    for j in J:
        require(cert["second_v_component"] == containing(facts["columns"][j]["boundary_components"], "v")
                == ["s", "v", "w"],
                "second operation does not cover every complete middle partition")
    require(facts["caps"]["states"][cert["middle_state"]] == M and
            facts["caps"]["states"][cert["terminal_state"]] == F,
            "middle or terminal literal state changed")
    image = flip(flip(A, cert["first_q_component"], (0, 3)),
                 cert["first_c_component"], (1, 2))
    require(image == M and proper_rim(image), "first whole-component operation has the wrong image")
    require(flip(flip(M, cert["first_c_component"], (1, 2)),
                 cert["first_q_component"], (0, 3)) == A,
            "the first boundary action is not reversible")
    require(flip(M, cert["second_v_component"], (1, 3)) == F and
            flip(F, cert["second_v_component"], (1, 3)) == M,
            "the second whole-component action has the wrong image or inverse")
    require(12301211 in facts["raw_columns"][306985], "the first common full row was lost")
    require(all(10064365 in facts["raw_columns"][j] for j in J),
            "the common terminal full row was lost")
    edge_positions = (NAMES.index("u1"), NAMES.index("v"))
    require(F[edge_positions[0]] == F[edge_positions[1]],
            "the terminal state is proper on the actual original edge")
    B = facts["caps"]["states"][44466]
    require(B[edge_positions[0]] == B[edge_positions[1]],
            "the other witness is proper on the actual original edge")
    require(cert["zero_columns"] == [48617, 67755] and
            all(6712710 in facts["raw_columns"][j] for j in cert["zero_columns"]),
            "the requested two columns lack their zero-A witness")


def controls(cert, facts):
    cases = [
        ("missing_middle_partition", lambda x: x["M_support"].pop()),
        ("boundary_only_v_swap", lambda x: x.__setitem__("second_v_component", ["v"])),
        ("proper_middle_as_edge_zero", lambda x: x.__setitem__("terminal_state", 44111)),
        ("hidden_u3v_prerequisite", lambda x: x["required_extra_edges"].append(["u3", "v"])),
        ("history_restricted_fibres", lambda x: x.__setitem__("all_complete_D_fibres", False)),
        ("wrong_requested_columns", lambda x: x.__setitem__("zero_columns", [66582, 67755])),
    ]
    rejected = []
    for name, mutate in cases:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            verify(bad, facts)
        except (ValueError, KeyError, IndexError):
            rejected.append(name)
    require(len(rejected) == len(cases), "a corrupt proof passed review")
    boundary_only = flip(M, ["v"], (1, 3))
    require(not proper_rim(boundary_only), "flipping v alone unexpectedly preserves even the rim")
    return rejected


def compute(seed):
    manifest = json.loads((AUDIT / "BASE.json").read_text())
    hashes = {}
    for name in (SOURCE + "/SOURCE_CONTRACT.md", SOURCE + "/counting/PROOF.md"):
        pinned_bytes(name, manifest, hashes)
    caps = json.loads(gzip.decompress(pinned_bytes(SOURCE + "/counting/caps.json.gz", manifest, hashes)))
    orbit = json.loads(gzip.decompress(pinned_bytes(SOURCE + "/counting/orbits.json.gz", manifest, hashes)))
    old_profiles = json.loads(pinned_bytes(PARENT + "/review/profile_orbits.json", manifest, hashes))
    require(caps["ordered_rim"] == NAMES, "the original ordered rim changed")
    require([caps["states"][s] for s in (44459, 44111, 44127)] == [A, M, F],
            "the three literal tuples changed")
    require(A[5] == M[5] == F[5] == 1 and A[3] == M[3] == F[3] == 1,
            "u1/u3 were not both kept at their original colour")
    table = {p["original_profile_id"]: p for p in old_profiles["profiles"]}
    profiles = [table[i] for i in IDS]
    require(all(["u1", "v"] in p["original_chords"] and
                ["u3", "v"] not in p["original_chords"] for p in profiles),
            "the fixed u1v profiles acquired an unproved u3v assumption")
    require(all(p["retained_columns"]["44459_only"] == [48617, 67755] for p in profiles),
            "the eight fixed profile supports changed")
    row_state = dict(orbit["rowids"])
    targets = {12302027: 44459, 12301211: 44111, 10064313: 44111, 10064365: 44127, 6712710: 44459}
    for row, state in targets.items():
        require(row_state[row] == state and canonical(decode(row)) == caps["states"][state],
                "an independently decoded literal half-row maps to the wrong state")
    incidence = {row: [] for row in targets}
    order = list(range(len(orbit["columns"])))
    random.Random(seed).shuffle(order)
    for j in order:
        for row in targets.keys() & set(orbit["columns"][j]):
            incidence[row].append(j)
    incidence = {row: sorted(ids) for row, ids in incidence.items()}
    six = [306985] + J
    columns = {j: {"column_id": j, "complete_halfrows": orbit["columns"][j],
                   "boundary_components": components_from_constant_differences(orbit["columns"][j])}
               for j in six}
    facts = dict(caps=caps, profiles=profiles, incidence=incidence,
                 columns=columns, raw_columns=orbit["columns"])
    cert = proposal()
    verify(cert, facts)
    rejected = controls(cert, facts)
    return dict(
        status="PASS; independent original-u1v complete-source exclusion review",
        audit_base=manifest["base"], mathematical_base=manifest["mathematical_base"],
        input_sha256=hashes, proof=cert,
        all_original_columns_scanned=len(orbit["columns"]),
        complete_incidence={str(row): ids for row, ids in incidence.items()},
        six_complete_column_records=list(columns.values()),
        first_image=M, second_image=F,
        terminal_u1_equals_v=True, u1_and_u3_fixed_at_1=True,
        no_u3v_edge_used=True, no_u3v_audit_output_consumed=True,
        all_eight_profiles_lack_u3v=True,
        full_D_fibre_injections=True,
        fixed_original_G_cap_assignment_invariance_claimed=False,
        source_count_chain="0<=Z44459<=Z44111<=Z44127=0; Z44466=0",
        zero_columns=[48617, 67755], excluded_original_profiles=IDS,
        negative_controls_rejected=rejected,
        source_scope="only the named strict original W7 u1v branch; parent W7/J1/J2 OPEN",
        no_symmetry_or_reflection_assumption=True,
        no_LP=True, no_new_original_graph_enumeration=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    result = compute(args.seed)
    target = HERE / "result.json"
    if args.build:
        with target.open("x") as output:
            json.dump(result, output, indent=2, sort_keys=True)
            output.write("\n")
    else:
        require(json.loads(target.read_text()) == result, "independent review result differs")
    print(json.dumps(dict(status=result["status"], seed=args.seed,
                          all_original_columns_scanned=result["all_original_columns_scanned"],
                          no_u3v_edge_used=True, zero_columns=result["zero_columns"],
                          excluded_original_profiles=IDS,
                          negative_controls_rejected=result["negative_controls_rejected"]), indent=2))


if __name__ == "__main__":
    main()
