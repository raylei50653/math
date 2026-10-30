#!/usr/bin/env python3
"""Read-only audit of one saved B8 lift and its missing cross-split data.

All controls are exact and finite. Formal extensions are NOT graph witnesses.
The two wheel disks are literal graph witnesses, outside Bernhart's support.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, lcm
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ck_bernhart_benchmark as benchmark
import ck_kempe_obstruction as ck
from four_color_counts_cone_verification import compatible, integrate
from configurations import validate_disk

CERT = ROOT / "audits/2026-10-29-bernhart-benchmark-e1a90fe/bernhart_66_diagonal-b8-certificate.json"
OLD_REPORT = ROOT / "audits/2026-10-29-bernhart-benchmark-e1a90fe/report.json"
DEFAULT = ROOT / "audits/2026-10-29-bernhart-cross-split-e1a90fe/verification.json"
COLOR_PAIRS = tuple(combinations((1, 2, 3), 2))


def load():
    receipt = json.loads((CERT.parent / "verification.json").read_text())
    for source in (CERT, OLD_REPORT):
        assert sha256(source.read_bytes()).hexdigest() == receipt["source_sha256"][str(source.relative_to(ROOT))]
    data = benchmark.cone_data()
    cert = json.loads(CERT.read_text())
    old = json.loads(OLD_REPORT.read_text())["cases"][0]
    benchmark.verify_cone(old["boolean_D"]["residual_mask"], data, cert)
    y = {e["index"]: e["weight"] for e in cert["signature_weights"]}
    n = {e["index"]: e["count"] for e in cert["pattern_counts"]}
    assert len(y) == 88 and len(n) == 76
    return data, y, n


def validate_lift(data, y, n):
    _, _, states, rows, columns = data
    actual = [0] * len(rows)
    for s, value in y.items():
        assert value >= 0
        for r in columns[s]:
            actual[r] += value
    assert all(actual[r] == n.get(states[wi], 0) for r, (wi, _) in enumerate(rows))


def lift_echelon(data, y, n):
    """Restrict the COMPLETE common-signature equations to positive columns."""
    _, _, states, rows, columns = data
    ys, ns = sorted(y), sorted(n)
    yi = {s: q for q, s in enumerate(ys)}
    ni = {s: len(ys) + q for q, s in enumerate(ns)}
    raw = [dict() for _ in rows]
    for s in ys:
        for r in columns[s]:
            raw[r][yi[s]] = 1
    for r, (wi, _) in enumerate(rows):
        if states[wi] in ni:
            raw[r][ni[states[wi]]] = -1
    unique = sorted({tuple(sorted(r.items())) for r in raw if r})
    echelon = {}
    for row in unique:
        current = {j: Fraction(v) for j, v in row}
        while current:
            pivot = min(current)
            if pivot not in echelon:
                factor = current[pivot]
                echelon[pivot] = {j: v / factor for j, v in current.items()}
                break
            factor = current[pivot]
            for j, value in echelon[pivot].items():
                value = current.get(j, 0) - factor * value
                if value:
                    current[j] = value
                elif j in current:
                    del current[j]
    return ys, ns, unique, echelon


def decompose(data, y, n):
    """Exact sparse Gaussian elimination; prove non-extremality in n-space."""
    ys, ns, unique, echelon = lift_echelon(data, y, n)
    width = len(ys) + len(ns)
    basis, parts = [], []
    for free in sorted(set(range(width)) - set(echelon)):
        h = [Fraction(0)] * width
        h[free] = 1
        for pivot, row in sorted(echelon.items(), reverse=True):
            h[pivot] = -sum(value * h[j] for j, value in row.items() if j != pivot)
        scale = lcm(*(v.denominator for v in h))
        h = [int(v * scale) for v in h]
        divisor = gcd(*h)
        h = [v // divisor for v in h]
        assert all(v >= 0 for v in h)
        yy = {s: h[q] for q, s in enumerate(ys) if h[q]}
        nn = {s: h[len(ys) + q] for q, s in enumerate(ns) if h[len(ys) + q]}
        validate_lift(data, yy, nn)
        py, pn, prows, pechelon = lift_echelon(data, yy, nn)
        assert len(py) + len(pn) - len(pechelon) == 1
        basis.append(h)
        parts.append(dict(signature_weights=[dict(index=s, weight=v) for s, v in yy.items()],
                          pattern_counts=[dict(index=s, count=v) for s, v in nn.items()],
                          positive_columns=len(py) + len(pn), rank=len(pechelon),
                          nonzero_rows=len(prows), full_lift_extreme=True,
                          projected_n_extreme="not established"))
    original = [y[s] for s in ys] + [n[s] for s in ns]
    assert len(basis) == 2 and len(echelon) == 162
    assert all(sum(h[j] for h in basis) == v for j, v in enumerate(original))
    a = {e["index"]: e["count"] for e in parts[0]["pattern_counts"]}
    b = {e["index"]: e["count"] for e in parts[1]["pattern_counts"]}
    separation = next((i, j) for i, j in combinations(ns, 2)
                      if a.get(i, 0) * b.get(j, 0) != a.get(j, 0) * b.get(i, 0))
    return dict(active_columns=width, distinct_nonzero_rows=len(unique), rank=len(echelon),
                kernel_dimension=len(basis), parts=parts, nonproportional_coordinates=separation,
                projected_count_vector_is_not_extreme=True,
                scope="Original projected count vector is not extreme; two parts are extreme in the full lift cone only.")


def marginal_couplings(data, y, n):
    words, sigs, states, rows, columns = data
    positive = {s: set(columns[s]) for s in y}
    observations, flexibility = [], Counter()
    witness = None
    for wi, word in enumerate(words):
        value = n.get(states[wi], 0)
        if not value:
            continue
        choices = [[s for s in sorted(y) if wi * 3 + split in positive[s]] for split in range(3)]
        tokens = [[s for s in ss for _ in range(y[s])] for ss in choices]
        assert all(len(t) == value for t in tokens)
        joints = Counter(zip(*tokens))
        for split, ss in enumerate(choices):
            marginal = Counter()
            for triple, mass in joints.items():
                marginal[triple[split]] += mass
            assert marginal == Counter({s: y[s] for s in ss})
        flexible = [split for split, ss in enumerate(choices) if len(ss) > 1]
        flexibility[len(flexible)] += 1
        observations.append(dict(word_index=wi, word=word, pattern_index=states[wi], count=value,
                                 split_signature_weights=[[dict(index=s, weight=y[s]) for s in ss]
                                                          for ss in choices],
                                 one_formal_joint=[dict(signatures=t, mass=m) for t, m in sorted(joints.items())]))
        if witness is None and len(flexible) >= 2:
            alternate = [list(t) for t in tokens]
            alternate[flexible[0]].reverse()
            other = Counter(zip(*alternate))
            assert other != joints
            assert all(Counter({s: sum(m for t, m in other.items() if t[split] == s)
                                for s in ss}) == Counter({s: y[s] for s in ss})
                       for split, ss in enumerate(choices))
            witness = dict(word_index=wi, word=word, pattern_index=states[wi],
                           first=[dict(signatures=t, mass=m) for t, m in sorted(joints.items())],
                           second=[dict(signatures=t, mass=m) for t, m in sorted(other.items())],
                           signatures={str(s): sigs[s] for ss in choices for s in ss},
                           scope="Two algebraic couplings with identical one-split marginals; neither is asserted to come from a graph.")
    assert witness is not None
    return dict(nonzero_words=len(observations), total_word_mass=sum(r["count"] for r in observations),
                row_incidence_mass=3 * sum(r["count"] for r in observations),
                flexibility_histogram=dict(sorted(flexibility.items())), rows=observations,
                same_observation_different_joint=witness,
                projection_result="Formal per-word three-split transport adds no condition beyond common marginal sums.")


def masks():
    return tuple(i for i in range(256) if i.bit_count() % 2 == 0)


def six_term_tests(z):
    rows = []
    for four in combinations(range(8), 4):
        fm = sum(1 << v for v in four)
        a, b, c, d = four
        for base in masks():
            if base & fm:
                continue
            ac, bd = (1 << a) | (1 << c), (1 << b) | (1 << d)
            ab, cd = (1 << a) | (1 << b), (1 << c) | (1 << d)
            ad, bc = (1 << a) | (1 << d), (1 << b) | (1 << c)
            lhs = z[base] * z[base | fm] + z[base | ac] * z[base | bd]
            rhs = z[base | ab] * z[base | cd] + z[base | ad] * z[base | bc]
            rows.append(dict(base=base, four=four, lhs=lhs, rhs=rhs))
    assert len(rows) == 560
    return rows


def formal_pm_extensions(data, y):
    _, sigs, _, _, _ = data
    g, lower = Counter(), Counter()
    for s, value in y.items():
        covered = sum(1 << v for a, b, _ in sigs[s] for v in (a, b))
        g[covered] += value  # a FORMAL all-zero-cycle atom assignment
        lower[covered] += value.bit_count()  # a valid ordinary-PM lower bound
    level = max(g.values())
    assert level == 3
    extensions = []
    for size in (level, level + 1):
        z = {i: size for i in masks()}
        equations = six_term_tests(z)
        assert all(r["lhs"] == r["rhs"] for r in equations)
        assert all(z[i] >= lower[i] for i in masks())
        extensions.append(dict(level=size, Z=[dict(exposed_mask=i, count=z[i],
                                                   formal_good_zero_cycle_atoms=g[i],
                                                   formal_hidden_odd_atoms=size - g[i],
                                                   proved_lower_bound=lower[i]) for i in masks()],
                               six_term_equations=len(equations)))
    bad = {i: level for i in masks()}
    bad[0] += 1
    failed = [r for r in six_term_tests(bad) if r["lhs"] != r["rhs"]]
    assert failed
    return dict(positive_covered_sets=len(g), positive_signature_weights=len(y),
                coverage_size_histogram=dict(sorted(Counter(2 * len(sigs[s]) for s in y).items())),
                proved_PM_lower_bound="Z_I >= sum_{S:cover(S)=I} popcount(y_S), conditional on actual graph counts",
                extensions=extensions, same_y_incompatible_extension_control=dict(
                    change="Z_empty=4; all other Z=3; same formal good atoms and nonnegative odd slack",
                    failed_equations=len(failed), first_failure=failed[0]),
                scope="Algebraic PM-table extensions only; no graph realization, extremality or shared-cut data.")


def graph_control(stacked):
    ring = list(range(8))
    outer = [(-4, -4), (0, -6), (4, -4), (6, 0),
             (4, 4), (0, 6), (-4, 4), (-6, 0)]
    faces = [(j, (j + 1) % 8, 8) for j in ring]
    points = outer + [(0, 0)]
    if stacked:
        faces = [(0, 1, 9), (1, 8, 9), (8, 0, 9)] + faces[1:]
        points += [(-1, -3)]
    edges = sorted({tuple(sorted((u, v))) for f in faces for u, v in zip(f, f[1:] + f[:1])})
    graph = dict(name="C8_wheel_stacked" if stacked else "C8_wheel", vertices=list(range(len(points))),
                 ring=ring, internal=list(range(8, len(points))), edges=edges, faces=faces,
                 positions=dict(enumerate(points)))
    geometry = validate_disk(graph)
    incidence = {e: [] for e in edges}
    for fi, f in enumerate(faces):
        for u, v in zip(f, f[1:] + f[:1]):
            incidence[tuple(sorted((u, v)))].append(fi)
    for j in ring:
        incidence[tuple(sorted((j, (j + 1) % 8)))].append(len(faces) + j)
    assert all(len(e) == 2 for e in incidence.values())
    dual = [tuple(incidence[e]) for e in edges]
    return graph, geometry, dual, len(faces)


def components(edges, selected):
    adj = defaultdict(list)
    for e in selected:
        u, v = edges[e]
        adj[u].append((v, e)); adj[v].append((u, e))
    unseen, result = set(adj), []
    while unseen:
        root = min(unseen)
        queue, es = [root], set()
        unseen.remove(root)
        for u in queue:
            for v, e in adj[u]:
                es.add(e)
                if v in unseen:
                    unseen.remove(v); queue.append(v)
        ends = sorted(v for v in queue if len(adj[v]) == 1)
        assert len(ends) in (0, 2)
        result.append(dict(vertices=queue, edges=sorted(es), ends=ends, cycle=not ends))
    return result


def perfect_matchings(edges, interior_count, exposed):
    free = set(range(interior_count + 8)) - {interior_count + i for i in range(8) if exposed >> i & 1}
    incident = defaultdict(list)
    for e, (u, v) in enumerate(edges):
        incident[u].append((v, e)); incident[v].append((u, e))
    found = []
    def visit(todo, selected):
        if not todo:
            found.append(selected)
            return
        u = min(todo, key=lambda v: (sum(w in todo for w, _ in incident[v]), v))
        for v, e in incident[u]:
            if v in todo:
                visit(todo - {u, v}, selected + [e])
    visit(free, [])
    return found


def inspect_plane_control(stacked, data):
    words, sigs, states, rows, columns = data
    graph, geometry, edges, f = graph_control(stacked)
    signature_index = {s: i for i, s in enumerate(sigs)}
    y, z, matching_rows = Counter(), {}, []
    for exposed in masks():
        ms = perfect_matchings(edges, f, exposed)
        z[exposed] = len(ms)
        for m in ms:
            parts = components(edges, set(range(len(edges))) - set(m))
            odd = [p for p in parts if p["cycle"] and len(p["edges"]) % 2]
            cycles = sum(p["cycle"] for p in parts)
            signature = tuple(sorted((p["ends"][0] - f, p["ends"][1] - f,
                                      -1 if len(p["edges"]) % 2 else 1)
                                     for p in parts if not p["cycle"]))
            if not odd:
                y[signature_index[signature]] += 2 ** cycles
            matching_rows.append(dict(exposed_mask=exposed, matching=m,
                                      odd_cycles=[p["edges"] for p in odd],
                                      cycles=cycles, signature=signature,
                                      even_complement=not odd))
    # Independent original-primal-edge enumeration, one literal b0=0 per word.
    literal_counts = []
    for w in words:
        boundary = integrate(w)
        count = sum(all((boundary + colors)[u] != (boundary + colors)[v]
                        for u, v in graph["edges"])
                    for colors in product(range(4), repeat=len(graph["internal"])))
        literal_counts.append(count)
    n = {}
    for wi, count in enumerate(literal_counts):
        j = states[wi]
        if j in n:
            assert n[j] == count
        n[j] = count
    n = {j: count for j, count in n.items() if count}
    validate_lift(data, y, n)
    assert all(r["lhs"] == r["rhs"] for r in six_term_tests(z))
    return dict(graph=graph, geometry=geometry, dual_edges=edges, dual_interior_count=f,
                PM_counts=[dict(exposed_mask=i, count=z[i]) for i in masks()],
                matchings=matching_rows,
                n=[dict(index=j, count=v) for j, v in sorted(n.items())],
                y=[dict(index=s, weight=v) for s, v in sorted(y.items())],
                ordinary_matchings=len(matching_rows),
                good_matchings=sum(r["even_complement"] for r in matching_rows),
                six_term_equations=560)


def plane_projection_control(data):
    a, b = [inspect_plane_control(stacked, data) for stacked in (False, True)]
    assert a["n"] == b["n"] and a["y"] == b["y"]
    za, zb = [{r["exposed_mask"]: r["count"] for r in g["PM_counts"]} for g in (a, b)]
    differences = [dict(exposed_mask=i, old=za[i], new=zb[i]) for i in masks() if za[i] != zb[i]]
    target = (1 << 1) | (1 << 7)
    assert za[target] == 0 and zb[target] == 1
    special = next(r for r in b["matchings"] if r["exposed_mask"] == target)
    assert not special["even_complement"] and special["odd_cycles"]
    return dict(controls=[a, b], same_n=True, same_y=True,
                changed_PM_families=differences, target_exposed=[1, 7],
                extra_odd_matching=special,
                scope="Two literal plane C8 disks related by one face stack; neither has Bernhart blocking support.")


def report():
    data, y, n = load()
    joints = marginal_couplings(data, y, n)
    decomposition = decompose(data, y, n)
    formal = formal_pm_extensions(data, y)
    plane = plane_projection_control(data)
    files = [Path(__file__), CERT, OLD_REPORT,
             ROOT / "scripts/ck_bernhart_benchmark.py",
             ROOT / "scripts/ck_kempe_obstruction.py",
             ROOT / "scripts/four_color_counts_cone_verification.py",
             ROOT / "audits/2026-10-26-ck-d-lock-comparison-8d28acc/configurations.py"]
    return dict(base="e1a90fea41702d7c98747716a5960198aecbecb3", date="2026-10-29",
                observation=dict(boundary_patterns=len(n), positive_signatures=len(y),
                                 pattern_count_mass=sum(n.values()), signature_weight_mass=sum(y.values()),
                                 pattern_count_histogram=dict(sorted(Counter(n.values()).items())),
                                 signature_weight_histogram=dict(sorted(Counter(y.values()).items()))),
                marginal_couplings=joints, exact_nonextremality=decomposition,
                formal_PM_extensions=formal, plane_projection_control=plane,
                excluded_Bernhart_coordinates=0,
                not_claimed=["Bernhart plane realization or nonrealization", "extremality of projected n decomposition parts",
                             "a shared-cut history from y", "new reducibility", "4CT", "new Lean"],
                sources={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.check.read_text() == payload, "Cross-split audit differs"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(dict(observation=result["observation"],
                          lift_rank=result["exact_nonextremality"]["rank"],
                          non_extreme=result["exact_nonextremality"]["projected_count_vector_is_not_extreme"],
                          positive_words=result["marginal_couplings"]["nonzero_words"],
                          formal_PM_equations_each=560,
                          plane_PM_changes=len(result["plane_projection_control"]["changed_PM_families"]),
                          excluded_Bernhart_coordinates=0), sort_keys=True))


if __name__ == "__main__":
    main()
