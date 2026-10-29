"""Derive literal C5 constraints from its five edges and current domains.

This module builds no catalogue or index of cycle colourings.  For each possible
colour at position 0, it joins the four-edge path by dynamic programming and
requires the last colour to differ from the anchor.  A forward path and a
backward path meet only at their shared position, so intersecting their colour
sets gives its exact support.  These are local C5 consequences, not a theorem
excluding a class of larger graphs.

``op_count`` counts charged DP stages, support unions, rule inspections, and
preview path extensions.  ``charge`` runs before each such operation; an
exception propagates without modifying the supplied domains.
"""

from __future__ import annotations


def _colours(mask):
    return [colour for colour in range(4) if mask & (1 << colour)]


def derive_c5(domain_masks, *, charge=None):
    """Return exact supports and counts derived from cyclic inequalities.

    Positions are ordered 0 through 4; edges are 01, 12, 23, 34, and 40.
    Domain masks use the four literal colours 0 through 3.  Explanations retain
    the anchor cases and both path directions so a viewer can display why a
    colour lacks support.  At most six witnesses are reconstructed directly
    from these paths, solely as a bounded preview.
    """
    masks = list(domain_masks)
    if len(masks) != 5 or any(type(mask) is not int or not 0 <= mask <= 15
                              for mask in masks):
        raise ValueError("C5 requires five four-colour domain masks in 0..15")
    if charge is not None and not callable(charge):
        raise ValueError("charge must be callable")
    op_count = 0

    def step():
        nonlocal op_count
        if charge is not None:
            charge()
        op_count += 1

    supports = [0] * 5
    row_count = 0
    anchor_cases = []
    for anchor in _colours(masks[0]):
        step()
        anchor_bit = 1 << anchor
        counts = [0] * 4
        counts[anchor] = 1
        forward = [anchor_bit, 0, 0, 0, 0]
        for position in range(1, 5):
            step()
            total = sum(counts)
            following = [total - counts[colour] if masks[position] & (1 << colour)
                         else 0 for colour in range(4)]
            forward[position] = sum(1 << colour for colour in range(4)
                                    if following[colour])
            counts = following

        step()
        count = sum(counts[colour] for colour in range(4) if colour != anchor)
        backward = [0, 0, 0, 0, masks[4] & (15 ^ anchor_bit)]
        for position in range(3, -1, -1):
            step()
            following = backward[position + 1]
            # One next colour forbids that colour; two distinct next colours
            # support every current colour.  An empty suffix supports none.
            compatible = (15 if following.bit_count() >= 2 else
                          15 ^ following if following else 0)
            backward[position] = (anchor_bit if position == 0 else masks[position]) & compatible
        for position in range(5):
            step()
            supports[position] |= forward[position] & backward[position]
        step()
        row_count += count
        anchor_cases.append({"anchor": anchor, "row_count": count,
                             "forward_masks": forward, "backward_masks": backward})

    rules = []
    step()
    union = 0
    for mask in masks:
        union |= mask
    if union.bit_count() <= 2:
        rules.append({
            "id": "odd_cycle_two_colors", "name": "奇環不能只用兩色",
            "vertices": list(range(5)), "pair": _colours(union),
            "condition": "五點的候選色合起來至多兩色。",
            "conclusion": "沿五條不等色邊交替會在閉環處相撞，故共同關係為空。",
        })
    for vertex in range(5):
        step()
        others = 0
        for position, mask in enumerate(masks):
            if position != vertex:
                others |= mask
        removed = masks[vertex] & others
        if others.bit_count() == 2 and removed and masks[vertex] & (15 ^ others):
            rules.append({
                "id": "odd_cycle_unique_escape", "name": "奇環唯一離開兩色的位置",
                "vertices": list(range(5)), "vertex": vertex,
                "pair": _colours(others), "removed_colors": _colours(removed),
                "condition": "其餘四點的候選全部包含在同一對顏色內。",
                "conclusion": "這一點也選該對顏色就成為兩色奇環，因此只能保留該對之外的顏色；其餘邊仍須相容。",
            })
    for first in range(5):
        second = (first + 1) % 5
        for singleton, neighbor in ((first, second), (second, first)):
            step()
            mask = masks[singleton]
            if mask.bit_count() == 1 and masks[neighbor] & mask:
                rules.append({
                    "id": "adjacent_singleton", "name": "相鄰單色排除",
                    "vertices": [singleton, neighbor], "edge": [first, second],
                    "vertex": neighbor, "fixed_vertex": singleton,
                    "color": mask.bit_length() - 1,
                    "removed_colors": _colours(mask),
                    "condition": "邊的一端只剩一種候選色。",
                    "conclusion": "另一端不能使用相同的顏色。",
                })
    step()
    rules.append({
        "id": "cycle_path_consistency", "name": "閉環路徑相容推導",
        "vertices": list(range(5)), "domain_masks": masks[:],
        "supports": supports[:], "row_count": row_count,
        "anchor_cases": anchor_cases,
        "condition": "逐一固定第 0 點，沿四邊路徑計數，再要求末點異於起點。",
        "conclusion": "每點的前向與後向可行色交集是該起點的完整支援；合併全部起點後，刪去沒有支援的顏色。",
    })

    preview = []

    def reconstruct(path, backward):
        if len(preview) >= 6:
            return
        position = len(path)
        if position == 5:
            step()
            preview.append(path[:])
            return
        allowed = backward[position] & (15 ^ (1 << path[-1]))
        for colour in _colours(allowed):
            step()
            reconstruct(path + [colour], backward)
            if len(preview) >= 6:
                return

    if row_count:
        for case in anchor_cases:
            if case["row_count"]:
                step()
                reconstruct([case["anchor"]], case["backward_masks"])
            if len(preview) >= 6:
                break
    return {"supports": supports, "row_count": row_count, "op_count": op_count,
            "method": "cycle-path-consistency", "rules": rules,
            "relation_preview": preview}
