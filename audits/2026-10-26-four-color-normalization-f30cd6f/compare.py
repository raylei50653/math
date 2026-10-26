#!/usr/bin/env python3
"""Compare one selected source in a fresh process; timing and checks stay separate."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, required=True)
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--repeats", type=int, default=5)
args = parser.parse_args()
assert args.repeats > 0
sys.path.insert(0, str(args.source.resolve()))
from four_color_constraints import solve_constraints
from four_color_joint_consistency import joint_supports
from four_color_lab import verify_coloring

inputs = json.loads((ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f/"
                     "propagation/inputs.json").read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def initial(graph):
    captured = {}

    class Captured(Exception):
        pass

    def returned(frame, event, answer):
        if event == "return":
            live = frame.f_back.f_locals
            captured.update(consistent=answer, domains=deepcopy(live["domains"]),
                            factors=[(f.scope, f.rows) for f in live["factors"]])
            raise Captured
        return returned

    def called(frame, event, arg):
        if (event == "call" and frame.f_code.co_name == "propagate"
                and frame.f_globals.get("__name__") == "four_color_constraints"):
            return returned
        return None

    previous = sys.gettrace()
    sys.settrace(called)
    try:
        solve_constraints(graph, **inputs["options"])
    except Captured:
        pass
    finally:
        sys.settrace(previous)
    return captured


records = []
for fixed in (True, False):
    graph = dict(inputs["graph"])
    if not fixed:
        graph["fixed"] = []
    state = initial(graph)
    assert state["consistent"]
    bucket = [factor for factor in state["factors"] if 0 in factor[0]]
    kernel_input = dict(factors=[dict(scope=scope, rows=sorted(rows)) for scope, rows in bucket],
                        domains=[sorted(values) for values in state["domains"]])
    timings = []
    for _ in range(args.repeats):
        started = time.perf_counter()
        answer = joint_supports(bucket, state["domains"], max_checks=1_000_000)
        timings.append(time.perf_counter() - started)
    assert answer["complete"] and answer["consistent"] == (not fixed)
    support = dict(rows=[sorted(rows) for rows in answer["rows"]],
                   domains={v: sorted(values) for v, values in answer["domains"].items()})
    kernel = {key: value for key, value in answer.items() if key not in ("rows", "domains")}
    kernel.update(input_sha256=digest(kernel_input), literal_support_sha256=digest(support),
                  median_seconds=statistics.median(timings), seconds=timings)

    timings = []
    previous_stats = None
    for _ in range(args.repeats):
        started = time.perf_counter()
        result = solve_constraints(graph, **dict(inputs["options"], use_joint_consistency=True))
        timings.append(time.perf_counter() - started)
        assert result["status"] == ("unsatisfiable" if fixed else "colored")
        if not fixed:
            assert verify_coloring(graph, result["colors"])
        if previous_stats is not None:
            assert result["stats"] == previous_stats
        previous_stats = result["stats"]
    conflicts = [event for event in result["events"] if event["kind"] == "conflict"]
    full = dict(status=result["status"], stats=result["stats"], colors=result["colors"],
                median_seconds=statistics.median(timings), seconds=timings,
                first_conflict=conflicts[0] if conflicts else None,
                elimination_records_sha256=digest(result["elimination_records"]))
    records.append(dict(fixed=fixed, graph=graph, kernel=kernel, full=full))
    print(json.dumps(dict(fixed=fixed, kernel_checks=kernel["checks"],
                         full_checks=full["stats"]["checks"], status=full["status"])), flush=True)

report = dict(repeats=args.repeats, cases=records,
              sources={path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                       for path in sorted(args.source.glob("four_color*.py"))},
              driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              timing_scope="Five serial repeats per case in a source-isolated process; logical counts include symmetry preparation and reconstruction. Timing is environment-specific.")
args.out.parent.mkdir(parents=True, exist_ok=True)
args.out.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
