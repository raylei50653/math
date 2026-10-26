#!/usr/bin/env python3
"""Verify normalized inference against the preserved original-edge counterexamples."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f"
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_constraints import solve_constraints
from four_color_lab import solve, verify_coloring
from four_color_serialization import json_dumps, json_loads


def original_solutions(graph):
    neighbors = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        neighbors[u].add(v)
        neighbors[v].add(u)
    assignment = dict(graph.get("fixed", []))

    def visit():
        if len(assignment) == len(neighbors):
            yield assignment.copy()
            return
        choices = {v: set(range(4)) - {assignment[w] for w in neighbors[v] if w in assignment}
                   for v in neighbors if v not in assignment}
        v = min(choices, key=lambda v: (len(choices[v]), -len(neighbors[v]), v))
        for c in sorted(choices[v]):
            assignment[v] = c
            yield from visit()
        assignment.pop(v, None)

    if not any(u in assignment and v in assignment and assignment[u] == assignment[v]
               for u, v in graph["edges"]):
        yield from visit()


def initial_state(graph, options):
    state = {}

    class Captured(Exception):
        pass

    def trace_return(frame, event, answer):
        if event == "return":
            live = frame.f_back.f_locals
            state.update(consistent=answer, domains=deepcopy(live["domains"]),
                         factors=[(f.scope, f.rows) for f in live["factors"]],
                         stats=deepcopy(live["stats"]))
            raise Captured
        return trace_return

    def trace_call(frame, event, arg):
        if (event == "call" and frame.f_code.co_name == "propagate"
                and frame.f_globals.get("__name__") == "four_color_constraints"):
            return trace_return
        return None

    previous = sys.gettrace()
    sys.settrace(trace_call)
    try:
        solve_constraints(graph, **options)
    except Captured:
        pass
    finally:
        sys.settrace(previous)
    return state


def digest(value):
    return hashlib.sha256(json_dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    inputs = json.loads((BASE / "propagation/inputs.json").read_text())
    graph, original_options = inputs["graph"], inputs["options"]
    options = dict(original_options, use_joint_consistency=True)
    assert initial_state(graph, original_options)["consistent"]
    fixed = solve_constraints(graph, **options)
    assert not initial_state(graph, options)["consistent"]
    assert fixed["status"] == "unsatisfiable" and not fixed["elimination_records"]
    assert fixed["stats"]["candidate_checks"] == fixed["stats"]["eliminations"] == 0
    assert list(original_solutions(graph)) == []

    bare = dict(graph, fixed=[])
    solutions = list(original_solutions(bare))
    assert len(solutions) == 624
    state = initial_state(bare, options)
    assert state["consistent"]
    checks = 0
    for coloring in solutions:
        assert all(coloring[v] in state["domains"][v] for v in bare["vertices"])
        for scope, rows in state["factors"]:
            assert tuple(coloring[v] for v in scope) in rows
            checks += 1
    unequal = {(a, b) for a in range(4) for b in range(4) if a != b}
    learned = [(scope, rows) for scope, rows in state["factors"] if 9 in scope and 11 in scope
               and {(row[scope.index(9)], row[scope.index(11)]) for row in rows} == unequal]
    assert learned
    bare_result = solve_constraints(bare, **options)
    assert bare_result["status"] == "colored" and verify_coloring(bare, bare_result["colors"])
    for record in bare_result["elimination_records"]:
        supports = {tuple(row["boundary"]): set(row["colors"]) for row in record["rows"]}
        for coloring in solutions:
            assert coloring[record["vertex"]] in supports[tuple(coloring[v] for v in record["scope"])]
            checks += 1

    grid = json.loads((BASE / "grid_6x7.json").read_text())
    current = solve_constraints(grid)
    raised = solve_constraints(grid, max_table_rows=1_000_000)
    limited = solve_constraints(grid, max_table_rows=100_000)
    assert current == raised
    assert current["status"] == "colored" and verify_coloring(grid, current["colors"])
    assert limited["status"] == "limit" and limited["stats"]["writebacks"] == 0

    labels = []
    conversion_limit = sys.get_int_max_str_digits()
    for engine in (solve, solve_constraints):
        big = 10 ** 4300
        example = dict(vertices=[big, big + 1, -big], edges=[[big, big + 1]])
        result = engine(example, trace_limit=0)
        assert result["status"] == "colored" and verify_coloring(example, result["colors"])
        assert json_loads(json_dumps(result))["graph"]["vertices"] == example["vertices"]
        labels.append(dict(engine=engine.__name__, status=result["status"],
                           exact_integer_roundtrip=True))
    assert sys.get_int_max_str_digits() == conversion_limit

    def compact(result):
        return {key: result[key] for key in ("status", "stats", "max_checks", "max_table_rows")}

    report = dict(
        baseline_commit="f30cd6f166ed0eb05935ee08c6784bb2f8115cc6",
        baseline_files_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted(BASE.rglob("*")) if p.is_file()},
        source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted((ROOT / "scripts").glob("four_color*.py"))},
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        options=options, fixed=compact(fixed), bare=compact(bare_result),
        bare_solution_count=len(solutions), all_solution_checks=checks,
        inferred_pair=dict(vertices=[9, 11], rows=sorted(map(list, unequal)),
                           existing_factors_with_exact_pair=len(learned)),
        grid_default=compact(current), grid_explicit_old_capacity=compact(limited),
        grid_complete_records_sha256=digest(current["elimination_records"]),
        labels=labels, interpreter_decimal_limit=conversion_limit,
        limitations=["Joint support is opt-in and may cover the whole graph (14 vertices here).",
                     "Unfinished optional queries commit no restrictions; exact elimination continues.",
                     "The main check limit remains authoritative; a resource limit is inconclusive.",
                     "Storage default increased; this is not an algorithmic memory reduction.",
                     "Finite regression evidence is not a universal propagation or implementation proof."])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print(json.dumps(dict(fixed_status=fixed["status"],
                         fixed_joint_checks=fixed["stats"]["joint_consistency_checks"],
                         bare_status=bare_result["status"], bare_solutions=len(solutions),
                         grid_status=current["status"], labels="pass")))


if __name__ == "__main__":
    main()
