#!/usr/bin/env python3
"""Two C8 diamonds, exact fibres, Boolean D and common-signature B8 LP.

Default replay verifies integer certificates; --solve-lp discovers them with
SciPy. No 4CT oracle, catalogue, replacement search or unproved cut filter.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, lcm
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "audits/2026-10-26-ck-d-lock-comparison-8d28acc"))
import ck_kempe_obstruction as ck
from configurations import validate_disk
from four_color_constraints import solve_constraints
from four_color_counts_cone_verification import signatures, compatible, integrate

BASE = "e1a90fea41702d7c98747716a5960198aecbecb3"
AUDIT = ROOT / "audits/2026-10-29-bernhart-benchmark-e1a90fe"


def graph(name, spoke_counts):
    edges = {tuple(sorted((j, (j + 1) % 8))) for j in range(8)}
    edges |= {(8, 9), (9, 10), (10, 11), (8, 11), (8, 10)}
    faces = [(8, 9, 10), (8, 10, 11)]
    start = 0
    fans = []
    for v, count in zip(range(8, 12), spoke_counts):
        fan = tuple(j % 8 for j in range(start, start + count))
        fans.append(fan)
        edges |= {tuple(sorted((v, j))) for j in fan}
        faces += [(a, b, v) for a, b in zip(fan, fan[1:])]
        start += count - 1
    for j, fan in enumerate(fans):
        faces.append((fan[-1], 8 + (j + 1) % 4, 8 + j))
    return dict(name=name, vertices=list(range(12)), ring=list(range(8)),
                internal=list(range(8, 12)), edges=sorted(edges), faces=faces,
                positions=dict(enumerate(((-4, -4), (0, -6), (4, -4), (6, 0),
                                          (4, 4), (0, 6), (-4, 4), (-6, 0),
                                          (0, -2), (2, 0), (0, 2), (-2, 0)))))


def interface(g):
    rows = []
    mask = 0
    for j, b in enumerate(ck.patterns(8)):
        fibres = [list(colors) for colors in product(range(4), repeat=4)
                  if all((b + colors)[u] != (b + colors)[v] for u, v in g["edges"])]
        request = dict(vertices=g["vertices"], edges=g["edges"], fixed=list(enumerate(b)))
        solved = solve_constraints(request, max_checks=10_000_000, max_table_rows=1_000_000,
                                   trace_limit=0, record_relations=False)
        assert solved["status"] in ("colored", "unsatisfiable")
        assert bool(fibres) == (solved["status"] == "colored")
        if fibres:
            mask |= 1 << j
            lift = dict(zip(solved["graph"]["vertices"], solved["colors"]))
            assert all(lift[u] != lift[v] for u, v in g["edges"])
            assert tuple(lift[i] for i in range(8)) == b
        rows.append(dict(index=j, boundary=b, internal_fibre=fibres))
    return mask, rows


def cone_data():
    words = tuple(w for w in product((1, 2, 3), repeat=8)
                  if all(w.count(c) % 2 == 0 for c in (1, 2, 3)))
    sigs = tuple(signatures(8))
    index = {b: j for j, b in enumerate(ck.patterns(8))}
    states = [index[ck.normalize(integrate(w))] for w in words]
    rows = [(i, pair) for i in range(len(words)) for pair in combinations((1, 2, 3), 2)]
    # Explicit full columns; all three color pairs use the SAME y(S).
    columns = [tuple(r for r, (i, pair) in enumerate(rows)
                     if compatible(words[i], pair, s)) for s in sigs]
    assert len(words) == 1641 and len(rows) == 4923 and len(sigs) == 1961
    return words, sigs, states, rows, columns


def integerize(values):
    fractions = [Fraction(float(v)).limit_denominator(1_000_000) for v in values]
    denominator = lcm(*(f.denominator for f in fractions))
    integers = [int(f * denominator) for f in fractions]
    divisor = gcd(*integers)
    assert divisor > 0
    return [v // divisor for v in integers]


def solve_cone(allowed, data):
    import numpy as np
    import scipy
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    words, sigs, states, rows, columns = data
    eligible = [s for s, col in enumerate(columns)
                if col and all(allowed >> states[rows[r][0]] & 1 for r in col)]
    active = [j for j in range(274) if allowed >> j & 1]
    n_index = {j: i for i, j in enumerate(active)}
    rr, cc, vv = [], [], []
    for q, s in enumerate(eligible):
        for r in columns[s]:
            rr.append(r); cc.append(q); vv.append(1)
    for r, (i, _) in enumerate(rows):
        if states[i] in n_index:
            rr.append(r); cc.append(len(eligible) + n_index[states[i]]); vv.append(-1)
    for j in range(len(active)):
        rr.append(len(rows)); cc.append(len(eligible) + j); vv.append(1)
    matrix = coo_matrix((vv, (rr, cc)), shape=(len(rows) + 1, len(eligible) + len(active))).tocsr()
    target = np.zeros(len(rows) + 1); target[-1] = 1
    # Sum feasible vectors to collect every attainable coordinate. The final
    # exact dual certifies that no still-missing coordinate can be positive.
    values = [0] * matrix.shape[1]
    iterations = 0
    while True:
        missing = [q for q in range(len(active)) if not values[len(eligible) + q]]
        objective = np.zeros(matrix.shape[1])
        for q in missing:
            objective[len(eligible) + q] = -1
        result = linprog(objective, A_eq=matrix, b_eq=target,
                         bounds=(0, None), method="highs")
        assert result.success, (result.status, result.message)
        iterations += 1
        if result.fun > -1e-8:
            break
        new = integerize(result.x)
        assert any(new[len(eligible) + q] for q in missing)
        values = [a + b for a, b in zip(values, new)]
    fractions = [Fraction(float(v)).limit_denominator(1_000_000)
                 for v in result.eqlin.marginals]
    scale = lcm(*(f.denominator for f in fractions))
    dual = [int(f * scale) for f in fractions]
    cert = dict(signature_weights=[dict(index=s, weight=values[q])
                                   for q, s in enumerate(eligible) if values[q]],
                pattern_counts=[dict(index=j, count=values[len(eligible) + q])
                                for q, j in enumerate(active) if values[len(eligible) + q]],
                excluded_pattern_indices=[active[q] for q in missing],
                dual=dict(scale=scale, coefficients=[dict(row=r, coefficient=v)
                                                    for r, v in enumerate(dual) if v]),
                solver=dict(scipy=scipy.__version__, status=int(result.status),
                            support_collection_LPs=iterations,
                            discovery_only="floating LP; acceptance requires exact integer replay"))
    verify_cone(allowed, data, cert)
    return cert


def verify_cone(allowed, data, cert):
    words, sigs, states, rows, columns = data
    weights = {entry["index"]: entry["weight"] for entry in cert["signature_weights"]}
    counts = {entry["index"]: entry["count"] for entry in cert["pattern_counts"]}
    assert len(weights) == len(cert["signature_weights"])
    assert len(counts) == len(cert["pattern_counts"])
    assert counts and all(type(v) is int and v > 0 for v in counts.values())
    assert all(type(v) is int and v > 0 for v in weights.values())
    assert all(0 <= j < 274 and allowed >> j & 1 for j in counts)
    assert all(0 <= s < len(sigs) for s in weights)
    observed = [0] * len(rows)
    for s, weight in weights.items():
        for r in columns[s]:
            observed[r] += weight
    for r, (i, _) in enumerate(rows):
        assert observed[r] == counts.get(states[i], 0), (r, observed[r])
    excluded = set(cert["excluded_pattern_indices"])
    active = {j for j in range(274) if allowed >> j & 1}
    assert set(counts).isdisjoint(excluded) and set(counts) | excluded == active
    dual = {entry["row"]: entry["coefficient"] for entry in cert["dual"]["coefficients"]}
    scale = cert["dual"]["scale"]
    assert type(scale) is int and scale > 0
    assert all(type(v) is int and 0 <= r <= len(rows) for r, v in dual.items())
    assert dual.get(len(rows), 0) == 0  # b^T lambda = 0 exactly
    eligible = [col for col in columns
                if col and all(states[rows[r][0]] in active for r in col)]
    assert all(sum(dual.get(r, 0) for r in col) <= 0 for col in eligible)
    state_dual = {j: 0 for j in active}
    for r, (i, _) in enumerate(rows):
        if states[i] in state_dual:
            state_dual[states[i]] -= dual.get(r, 0)
    assert all(v <= (-scale if j in excluded else 0) for j, v in state_dual.items())
    support = sum(1 << j for j in counts)
    assert ck.failure(support, ck.obligations(8)) is None
    return dict(full_integer_equations=len(rows), nonzero_pattern_counts=len(counts),
                nonzero_signature_weights=len(weights), total_pattern_count=sum(counts.values()),
                exact_integer_replay=True, maximal_support_certified=True,
                dual_excluded_pattern_count=len(excluded),
                Boolean_D_stable=True, support_mask=support)


def certificate_negative_controls(allowed, data, cert):
    bad = deepcopy(cert)
    bad["signature_weights"][0]["weight"] += 1
    try:
        verify_cone(allowed, data, bad)
    except AssertionError:
        pass
    else:
        raise AssertionError("corrupt primal accepted")
    bad = deepcopy(cert)
    bad["dual"]["coefficients"].append(dict(row=len(data[3]), coefficient=1))
    try:
        verify_cone(allowed, data, bad)
    except AssertionError:
        pass
    else:
        raise AssertionError("corrupt dual accepted")
    return 2


def report(solve_lp=False):
    data = cone_data()
    cases = []
    for name, spokes, expected, rounds in (
            ("bernhart_66_diagonal", (3, 3, 3, 3), 154, (178, 170, 164, 157, 154)),
            ("alternative_55_diagonal", (2, 4, 2, 4), 160, (180, 162, 160))):
        g = graph(name, spokes)
        geometry = validate_disk(g)
        accepted, fibres = interface(g)
        d = ck.obstruction(8, accepted)
        assert accepted.bit_count() == 81 and d["initial_obstruction_count"] == 193
        assert d["residual_count"] == expected
        assert tuple(r["after_mask"].bit_count() for r in d["rounds"]) == rounds
        replacement = [j for j, b in enumerate(ck.patterns(8))
                       if b[0] == b[2] and b[4] == b[6] and b[0] != b[4]]
        assert len(replacement) == 18
        cert_path = AUDIT / f"{name}-b8-certificate.json"
        if solve_lp:
            cert = solve_cone(d["residual_mask"], data)
            cert_path.parent.mkdir(parents=True, exist_ok=True)
            cert_path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        else:
            cert = json.loads(cert_path.read_text())
        cone = verify_cone(d["residual_mask"], data, cert)
        negative_controls = certificate_negative_controls(d["residual_mask"], data, cert)
        replacement_survivors = [j for j in replacement if d["residual_mask"] >> j & 1]
        if name == "bernhart_66_diagonal":
            assert not replacement_survivors
        else:
            assert len(replacement_survivors) == 11
        cases.append(dict(name=name, graph=g, geometry=geometry, fibres=fibres,
                          accepted_mask=accepted, accepted_count=81,
                          boolean_D=d, B8=cone,
                          corrupted_certificate_controls=negative_controls,
                          B8_certificate=str(cert_path.relative_to(ROOT)),
                          replacement=dict(indices=replacement,
                                           direct_accepted=sum(bool(accepted >> j & 1) for j in replacement),
                                           D_surviving_indices=replacement_survivors,
                                           B8_surviving_indices=[j for j in replacement
                                                                if cone["support_mask"] >> j & 1])))
    sources = [Path(__file__), ROOT / "scripts/ck_kempe_obstruction.py",
               ROOT / "scripts/four_color_counts_cone_verification.py",
               ROOT / "scripts/four_color_constraints.py",
               ROOT / "audits/2026-10-26-ck-d-lock-comparison-8d28acc/configurations.py"]
    return dict(base=BASE, scope="Two literal C8 disks; exact fibres and abstract cone certificates",
                pattern_count=274, B8_words=len(data[0]), B8_signatures=len(data[1]),
                B8_equations=len(data[3]), cases=cases,
                sources={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sources},
                not_claimed=["new reducibility", "realizable surviving exterior", "4CT", "new Lean",
                             "shared-cut filter soundness", "machine-checked C-reduction topology"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solve-lp", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = report(args.solve_lp)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps([dict(name=c["name"], accepted=c["accepted_count"],
                           D=c["boolean_D"]["residual_count"], B8=c["B8"],
                           replacement_D_survivors=len(c["replacement"]["D_surviving_indices"]))
                      for c in result["cases"]], indent=2))


if __name__ == "__main__":
    main()
