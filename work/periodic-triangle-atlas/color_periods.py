#!/usr/bin/env python3
"""Exact finite periodic 4-color experiments, with full seam witnesses.

Reproduce: uv run --with python-sat==1.9.dev17 python work/periodic-triangle-atlas/color_periods.py
Only a named finite periodic quotient is decided by UNSAT, not the infinite graph.
"""
from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import pysat
from pysat.solvers import Solver

DIRECTORY = Path(__file__).resolve().parent
PERIODS = [(1, 1), (2, 1), (1, 2), (2, 2), (3, 1), (1, 3)]


def vertex_index(vertex, x, y, n, p, q):
    return (((y % q) * p + x % p) * n + vertex)


def color_var(index, color):
    return index * 4 + color + 1


def quotient(example, p, q):
    n = len(example["points"])
    edges = set()
    for y in range(q):
        for x in range(p):
            for u, v, dx, dy in example["edges"]:
                a = vertex_index(u, x, y, n, p, q)
                b = vertex_index(v, x + dx, y + dy, n, p, q)
                edges.add(tuple(sorted((a, b))))
    return sorted(edges)


def cnf(example, p, q, require_exact_axes=False):
    n = len(example["points"])
    count = n * p * q
    clauses = []
    for index in range(count):
        colors = [color_var(index, color) for color in range(4)]
        clauses.append(colors)
        clauses.extend([-a, -b] for a, b in combinations(colors, 2))
    for a, b in quotient(example, p, q):
        for color in range(4):
            clauses.append([-color_var(a, color), -color_var(b, color)])
    # This removes only global color permutations: every proper triangle can
    # have its three colors renamed 0,1,2 in this fixed vertex order.
    triangle = [vertex_index(v, dx, dy, n, p, q)
                for v, dx, dy in example["faces"][0]]
    if len(set(triangle)) == 3:
        for color, index in enumerate(triangle):
            clauses.append([color_var(index, color)])
    next_variable = count * 4 + 1
    if require_exact_axes:
        for period, direction in [(p, (1, 0)), (q, (0, 1))]:
            if period == 1:
                continue
            witnesses = []
            for y in range(q):
                for x in range(p):
                    for v in range(n):
                        a = vertex_index(v, x, y, n, p, q)
                        b = vertex_index(v, x+direction[0], y+direction[1], n, p, q)
                        different = next_variable
                        next_variable += 1
                        witnesses.append(different)
                        # different -> no common color for the selected pair.
                        for color in range(4):
                            clauses.append([-different, -color_var(a, color),
                                            -color_var(b, color)])
            # At least one spatial vertex changes under the unit translation.
            # With tested prime periods 2 or3, the axial period is then exact.
            clauses.append(witnesses)
    return clauses


def collect_models(example, p, q, exact=False, maximum=3):
    n = len(example["points"])
    witnesses = []
    with Solver(name="g3", bootstrap_with=cnf(example, p, q, exact)) as solver:
        while len(witnesses) < maximum and solver.solve():
            true_variables = {v for v in solver.get_model() if v > 0}
            colors = []
            for index in range(n*p*q):
                chosen = [c for c in range(4) if color_var(index, c) in true_variables]
                assert len(chosen) == 1
                colors.append(chosen[0])
            witnesses.append(analyze_witness(example, p, q, colors))
            solver.add_clause([-color_var(index, color)
                               for index, color in enumerate(colors)])
    return witnesses


def analyze_witness(example, p, q, flat):
    n = len(example["points"])

    def at(v, x, y):
        return flat[vertex_index(v, x, y, n, p, q)]

    checked_edges = 0
    for y in range(q):
        for x in range(p):
            for u, v, dx, dy in example["edges"]:
                assert at(u, x, y) != at(v, x+dx, y+dy)
                checked_edges += 1
    shifts, permuted = [], []
    for dy in range(q):
        for dx in range(p):
            same = True
            mapping = {}
            valid_permutation = True
            for y in range(q):
                for x in range(p):
                    for v in range(n):
                        before, after = at(v,x,y), at(v,x+dx,y+dy)
                        same &= before == after
                        if before in mapping and mapping[before] != after:
                            valid_permutation = False
                        mapping[before] = after
            if same:
                shifts.append([dx,dy])
            if valid_permutation and len(set(mapping.values())) == len(mapping):
                unused_domain = sorted(set(range(4)) - set(mapping))
                unused_range = sorted(set(range(4)) - set(mapping.values()))
                mapping.update(zip(unused_domain, unused_range))
                permutation = [mapping[c] for c in range(4)]
                assert sorted(permutation) == [0,1,2,3]
                permuted.append({"shift":[dx,dy], "permutation":permutation})
    axis_x = next(dx for dx in range(1,p+1) if [dx%p,0] in shifts)
    axis_y = next(dy for dy in range(1,q+1) if [0,dy%q] in shifts)
    assert (p*q) % len(shifts) == 0
    return {
        "colors": [[flat[(y*p+x)*n:(y*p+x+1)*n]
                    for x in range(p)] for y in range(q)],
        "axis_period": [axis_x, axis_y],
        "same_color_shifts": shifts,
        "permuted_shifts": permuted,
        "translation_index": p*q//len(shifts),
        "checks": {"all_lifted_edges_proper": True,
                   "edge_instances_checked": checked_edges,
                   "full_translation_scan": True},
    }


def odd_degree_certificate(example):
    root = next(v for v,d in enumerate(example["degrees"]) if d%2)
    link = defaultdict(set)
    for face in example["faces"]:
        for k,(v,dx,dy) in enumerate(face):
            if v != root:
                continue
            others = [face[(k+1)%3],face[(k+2)%3]]
            a,b = [(w,sx-dx,sy-dy) for w,sx,sy in others]
            link[a].add(b)
            link[b].add(a)
    assert all(len(neighbors)==2 for neighbors in link.values())
    first = min(link)
    cycle = [first]
    previous,current = None,first
    while True:
        nxt = min(link[current]-({previous} if previous is not None else set()))
        if nxt == first:
            break
        assert nxt not in cycle
        cycle.append(nxt)
        previous,current = current,nxt
    assert len(cycle)==example["degrees"][root] and len(cycle)%2
    return {"status":"UNSAT", "odd_degree_vertex":root,
            "degree":len(cycle), "neighbor_cycle":cycle,
            "reason":"The center uses one color; its odd neighbor cycle cannot alternate the two remaining colors. This is a local obstruction in the infinite lift."}


def main():
    source = DIRECTORY / "crystals.json"
    catalogue = json.loads(source.read_text())
    results = []
    for example in catalogue["examples"]:
        periods = []
        for p,q in PERIODS:
            unrestricted = collect_models(example,p,q,maximum=1)
            record = {"p":p,"q":q,"status":"SAT" if unrestricted else "UNSAT"}
            if p==q==1:
                models = collect_models(example,p,q,maximum=3) if unrestricted else []
                record["exact_axis_status"] = "NOT_APPLICABLE"
                record["witness_kind"] = "unrestricted"
            elif unrestricted:
                models = collect_models(example,p,q,exact=True,maximum=3)
                record["exact_axis_status"] = "SAT" if models else "UNSAT"
                record["witness_kind"] = "exact_axes" if models else "unrestricted"
                if not models:
                    models = unrestricted
            else:
                models=[]
                record["exact_axis_status"]="UNSAT"
                record["witness_kind"]="none"
            for index,model in enumerate(models):
                model["id"] = f"{example['id']}-{p}x{q}-{index+1}"
                if record["witness_kind"]=="exact_axes":
                    assert model["axis_period"]==[p,q]
            record["witnesses"] = models
            periods.append(record)
            print(example["id"],f"{p}x{q}",record["status"],record["exact_axis_status"],len(models),flush=True)
        results.append({"id":example["id"],
                        "three_color":odd_degree_certificate(example),
                        "smallest_tested_rectangular_area":min(r["p"]*r["q"] for r in periods if r["status"]=="SAT"),
                        "periods":periods})
    payload={
        "schema":"periodic-triangle-colorings/1",
        "method":{
            "source":"crystals.json", "source_sha256":sha256(source.read_bytes()).hexdigest(),
            "solver":"Glucose3 via python-sat", "python_sat_version":pysat.__version__,
            "reproduce":"uv run --with python-sat==1.9.dev17 python work/periodic-triangle-atlas/color_periods.py",
            "colors":"Four literal vertex colors 0,1,2,3; adjacent lifted vertices differ.",
            "array_order":"colors[y][x][motif_vertex_id], with x mod p and y mod q.",
            "periods":PERIODS,
            "exact_axes":"For primes2,3, forbid invariance under each nontrivial unit axis translation, using a complete disjunction over every spatial vertex.",
            "symmetry_breaking":"Pin first lifted face modulo p,q to colors0,1,2; removes only global color permutations.",
            "witnesses":"Up to three distinct pinned-face assignments, not a complete coloring enumeration.",
            "permutation_convention":"c(v,x+dx,y+dy)=permutation[c(v,x,y)] for every lifted motif vertex.",
            "translation_index":"Number of geometric repeat cells per full literal-color translation domain: p*q / number of same_color_shifts. May be smaller than axis-period rectangle due to skew translations.",
            "scope":"SAT constructs an infinite periodic proper coloring. UNSAT decides only this finite period quotient. The six tested rectangles do not classify all periods or all sublattices.",
            "minimality":"smallest_tested_rectangular_area is among the six tested rectangles only, not a minimum over all translation subgroups.",
            "proof_scope":"CNF solved exactly; SAT assignments independently checked against every source edge in every period cell. No external four-color theorem is used. Solver UNSAT has no archived formal proof certificate.",
        },
        "examples":results,
    }
    output=DIRECTORY/"colorings.json"
    output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n")
    print("Wrote",output,flush=True)


if __name__=="__main__":
    main()
