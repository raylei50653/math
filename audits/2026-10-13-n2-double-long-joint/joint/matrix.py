"""Exact capacity-one rejection-assignment screen; no graph replacement.

Rows and columns retain literal original root colors.  A feasible assignment
is only an abstract obstruction to this sufficient joint test, not a coloring
or an actual rejecting source.  Safe cells must have original full lifts.
"""
from itertools import product


def analyze(rows, columns, kp_r, kp_s, safe_p, safe_q):
    rows, columns = tuple(rows), tuple(columns)
    grid = set(product(rows, columns))
    safe_p, safe_q = set(map(tuple, safe_p)), set(map(tuple, safe_q))
    if not rows or not columns or len(set(rows)) != len(rows) or len(set(columns)) != len(columns):
        raise ValueError("nonempty distinct literal colors required")
    if len(rows) > 4 or len(columns) > 4:
        raise ValueError("four-color interface only")
    if any(type(c) is not int or c not in range(4) for c in rows + columns):
        raise ValueError("literal root colors must be integers 0..3")
    if not (1 <= kp_r <= len(rows) and 1 <= kp_s <= len(columns)):
        raise ValueError("positive mixed incidences and original55 degree identity required")
    if not safe_p <= grid or not safe_q <= grid:
        raise ValueError("safe cells outside original external factor")
    overlap = sorted(safe_p & safe_q)
    if overlap:
        return {"feasible": False, "common_safe_cells": overlap,
                "assignment": None, "count": 0, "violated_cut": None}
    forced_p = safe_q  # Q accepts: any rejection must be assigned to P.
    forced_q = safe_p
    free = sorted(grid - forced_p - forced_q)
    row_forced = {r: sum((r, c) in forced_p for c in columns) for r in rows}
    col_forced = {c: sum((r, c) in forced_p for r in rows) for c in columns}
    lo_r = {r: max(0, kp_s - 1 - row_forced[r]) for r in rows}
    hi_r = {r: kp_s - row_forced[r] for r in rows}
    lo_c = {c: max(0, kp_r - 1 - col_forced[c]) for c in columns}
    hi_c = {c: kp_r - col_forced[c] for c in columns}
    first, count = None, 0
    # At most 2^16 assignments. Each is checked with the original row labels.
    for bits in product((0, 1), repeat=len(free)):
        ones = forced_p | {cell for cell, bit in zip(free, bits) if bit}
        if not all(kp_s - 1 <= sum((r, c) in ones for c in columns) <= kp_s for r in rows):
            continue
        if not all(kp_r - 1 <= sum((r, c) in ones for r in rows) <= kp_r for c in columns):
            continue
        count += 1
        if first is None:
            first = [[int((r, c) in ones) for c in columns] for r in rows]
    cut = None
    for label, uppers in (("row", hi_r), ("column", hi_c)):
        for color, upper in uppers.items():
            if upper < 0:
                cut = {"kind": "forced_upper_exceeded", "axis": label,
                       "color": color, "remaining_upper": upper}
                break
        if cut:
            break
    if cut is None:
        for rx in product((0, 1), repeat=len(rows)):
            x = {r for r, bit in zip(rows, rx) if bit}
            for cy in product((0, 1), repeat=len(columns)):
                y = {c for c, bit in zip(columns, cy) if bit}
                inequalities = [
                    ("row_lower", sum(lo_r[r] for r in x),
                     sum(hi_c[c] for c in y) + sum(r in x and c not in y for r, c in free)),
                    ("column_lower", sum(lo_c[c] for c in y),
                     sum(hi_r[r] for r in x) + sum(r not in x and c in y for r, c in free)),
                ]
                for kind, lhs, rhs in inequalities:
                    if lhs > rhs:
                        cut = {"kind": kind, "rows": sorted(x), "columns": sorted(y),
                               "lhs": lhs, "rhs": rhs}
                        break
                if cut:
                    break
            if cut:
                break
    if cut is not None and count:
        raise AssertionError("counting cut contradicts an explicit feasible matrix")
    return {"feasible": bool(count), "common_safe_cells": [], "assignment": first,
            "count": count, "violated_cut": cut}
