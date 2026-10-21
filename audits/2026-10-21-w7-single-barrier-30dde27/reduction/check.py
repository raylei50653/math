#!/usr/bin/env python3
"""Tiny controls for original b=1 bridge and five-star lemmas, not source search."""

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
P = ("n", "u4", "u3", "u2", "u1", "L")
PC = dict(zip(P, (1, 2, 1, 2, 1, 2)))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def arc(profile, lengths):
    result = [("a", (0,), None)]
    if profile == 0:
        for j in reversed(range(lengths[0])):
            result.append((f"H0[{j}]", (0, 2, 3), "n"))
        result.append(("z1", (0, 3), None))
    for j, center in enumerate(P[1:], 1):
        count = lengths[j if profile == 0 else j - 1]
        for r in range(count):
            result.append((f"H{j}[{r}]", tuple(c for c in range(4) if c != PC[center]), center))
        if j < 5:
            result.append((f"z{j+1}", (0, 3), None))
    result.append(("q", (3,), None))
    return result


def one_barrier_rows(profile, lengths):
    items = arc(profile, lengths)
    rows = []
    for colors in itertools.product(*(item[1] for item in items)):
        if any(a == b for a, b in zip(colors, colors[1:])):
            continue
        barriers = [i for i, c in enumerate(colors) if c in (1, 2)]
        if len(barriers) != 1:
            continue
        j = barriers[0]
        require(items[j][2] in P, "barrier is not an H point")
        total = sum(lengths)
        require(int(colors[j-1] != colors[j+1]) == ((1-profile+total) % 2),
                "wrong arbitrary-K phase")
        # Reconstruct all 12 edges incident to the complete original P stars.
        edges = {frozenset((P[i], P[i+1])) for i in range(5)}
        for i, (name, domain, center) in enumerate(items):
            if center is not None and colors[i] in (1, 2):
                edges.add(frozenset((name, center)))
        incident_outside = [edge for edge in edges if len(edge & set(P)) == 1]
        require(incident_outside == [frozenset((items[j][0], items[j][2]))],
                "P does not attach by exactly one original 12 edge")
        prefix = [name for i, (name, domain, center) in enumerate(items)
                  if name.startswith("z") and i < j]
        suffix = [name for i, (name, domain, center) in enumerate(items)
                  if name.startswith("z") and i > j]
        if profile == 1:
            prefix.insert(0, "z1=a")
        rows.append({"barrier": items[j][0], "center": items[j][2],
                     "left_color": colors[j-1], "right_color": colors[j+1],
                     "z_prefix": prefix, "z_suffix": suffix})
    require(len(rows) == sum(lengths), "b=1 local count should be exactly K")
    return rows


def main():
    manifest = json.loads((HERE / "BASE.json").read_text())
    require(manifest["base"] == "30dde27293b5d3ad63c75fae73cda5be96db705b", "BASE changed")
    for record in manifest["inputs"]:
        frozen = (HERE / "frozen" / record["path"]).read_bytes()
        require(len(frozen) == record["bytes"], "frozen byte count changed")
        require(hashlib.sha256(frozen).hexdigest() == record["sha256"], "frozen SHA changed")
        require((ROOT / record["path"]).read_bytes() == frozen, "authority drift")
    k1 = []
    for profile in (0, 1):
        for slot in range(6 if profile == 0 else 5):
            lengths = [0] * (6 if profile == 0 else 5)
            lengths[slot] = 1
            rows = one_barrier_rows(profile, lengths)
            row = rows[0]
            degrees = [6 if profile == 0 else 5, 5, 5, 5, 5, 5]
            center_index = P.index(row["center"])
            degrees[center_index] += 1
            require(int(row["left_color"] != row["right_color"]) == profile, "K1 phase changed")
            k1.append({"profile": profile, "lengths": lengths, "P_degrees": degrees, **row})
    require(len(k1) == 11, "missing named K1 position")

    five_stars = []
    for center in (1, 2):
        barrier = 3-center
        for left, right in itertools.product((0, 3), repeat=2):
            local = []
            retained = []
            for u, v in itertools.product(range(4), repeat=2):
                # Exact link cycle around y is center,left,u,v,right.
                cycle = (center, left, u, v, right)
                if barrier in cycle or any(a == b for a, b in zip(cycle, cycle[1:] + cycle[:1])):
                    continue
                local.append([u, v])
                outer_connects_03 = all(c in (0, 3) for c in (left, u, v, right))
                if outer_connects_03:
                    continue
                retained.append([u, v])
                require((u == center) + (v == center) == 1, "five-star exterior12 multiplicity changed")
                require(set(cycle) == set(range(4)) - {barrier}, "y missing another color")
            require(len(local) == (2 if left == right else 3), "local five-star count changed")
            require(len(retained) == 2, "separated five-star count changed")
            five_stars.append({"center_color": center, "barrier_color": barrier,
                               "left": left, "right": right,
                               "locally_proper_outer_pairs": local,
                               "03_separation_retains": retained})

    k2_cases = []
    for profile, lengths in ((0, (2, 0, 0, 0, 0, 0)),
                             (0, (1, 1, 0, 0, 0, 0)),
                             (1, (2, 0, 0, 0, 0)),
                             (1, (1, 1, 0, 0, 0))):
        rows = one_barrier_rows(profile, lengths)
        items = arc(profile, lengths)
        for row in rows:
            alpha = PC[row["center"]]
            same = sum(item[2] is not None and PC[item[2]] == alpha for item in items)
            k2_cases.append({"profile": profile, "lengths": lengths, "barrier": row["barrier"],
                             "K": 2, "b": 1, "same_center_color_H_count": same})
    require(any(row["same_center_color_H_count"] == 1 for row in k2_cases),
            "K>1 conditional anchoring control absent")

    # Three explicit wrong rules are each required to fail.  The six-cycle is
    # an exact local degree-six link: center=1, y=2, endpoints=0,0,
    # exterior list=(1,0,1).  It is locally proper and contains exterior12,
    # but has no color3 neighbor, so cannot satisfy the source saturation.
    wrong_link = (1, 0, 1, 0, 1, 0)
    require(all(a != b for a, b in zip(wrong_link, wrong_link[1:] + wrong_link[:1])),
            "missing03 negative control is not locally proper")
    require(2 not in wrong_link and 1 in wrong_link[2:5],
            "missing03 negative control does not contain exterior12")
    negative = {
        "b1_implies_K1_rejected": any(row["K"] != row["b"] for row in k2_cases),
        "outside12_alone_suffices_rejected": set(wrong_link) != {0, 1, 3},
        "all03_outer_path_separated_rejected": [3, 0] not in five_stars[1]["03_separation_retains"],
    }
    require(all(negative.values()), "a negative control was not exercised")
    print(json.dumps({
        "scope": "tiny local controls only; complete941 source hypotheses not triggered by these controls",
        "base": manifest["base"], "frozen_inputs_checked": len(manifest["inputs"]),
        "K1_named_original_positions": k1, "five_star_complete_local_tables": five_stars,
        "b1_K2_controls": k2_cases, "negative_controls": negative,
        "paper_authority": "REPORT.md original-link and same-literal-rim arguments",
        "new_source_exclusion": False, "source_realizability": "OPEN",
        "smaller_legal_replacement": "OPEN", "new_Lean": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
