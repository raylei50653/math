#!/usr/bin/env python3
"""Independent enumeration of the original C edges; no transfer/checker imports.

Generation exclusively creates a new file.  Checking only reads its inputs and
compares every full assignment, named-vertex coordinate, and empty fibre.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys


LITERALS = (
    "01012", "01021", "01023", "01201", "01202",
    "01203", "01212", "01213", "01231", "01232",
)
COLOURS = (0, 1, 2, 3)
S_SPOKE_VARIANTS = (("b0",), ("b2",), ("b0", "b2"))


def degree_findings(case):
    """Report each original named vertex whose retained full degree is not 4."""
    vertices = case["vertices"]
    if len(vertices) != len(set(vertices)):
        raise ValueError(f"case={case['id']}: duplicate original vertex")
    if "r" not in vertices:
        raise ValueError(f"case={case['id']}: original vertex r is missing")
    vertex_set = set(vertices)
    neighbours = {v: set() for v in vertices}
    seen_edges = set()
    for edge in case["original_edges"]:
        if len(edge) != 2:
            raise ValueError(f"case={case['id']}: original edge is not a pair: {edge!r}")
        u, v = edge
        if u not in vertex_set or v not in vertex_set or u == v:
            raise ValueError(f"case={case['id']}: invalid original edge {edge!r}")
        key = frozenset(edge)
        if key in seen_edges:
            raise ValueError(f"case={case['id']}: duplicate original edge {edge!r}")
        seen_edges.add(key)
        neighbours[u].add(v)
        neighbours[v].add(u)
    contacts = case["s_contacts"]
    if len(contacts) != 2 or len(set(contacts)) != 2 or any(v not in vertex_set for v in contacts):
        raise ValueError(f"case={case['id']}: expected two ordered actual s contacts")
    attachments = case["boundary_attachments"]
    if set(attachments) != vertex_set:
        raise ValueError(f"case={case['id']}: boundary attachment keys differ from original vertices")
    findings = []
    for v in vertices:
        boundary = attachments[v]
        if len(boundary) != len(set(boundary)) or any(b not in {f"b{i}" for i in range(5)} for b in boundary):
            raise ValueError(f"case={case['id']}: invalid literal attachments at original vertex {v}")
        total = len(neighbours[v]) + len(boundary) + int(v in contacts)
        if total != 4:
            findings.append({
                "vertex": v,
                "deg_C": len(neighbours[v]),
                "boundary_attachment_count": len(boundary),
                "s_contact_incidence": int(v in contacts),
                "full_degree": total,
                "expected": 4,
            })
    return findings


def direct_assignments(case, literal):
    """Exhaust original named colour vectors and test original edge inequalities."""
    vertices = case["vertices"]
    indices = {v: i for i, v in enumerate(vertices)}
    edges = [(indices[u], indices[v]) for u, v in case["original_edges"]]
    allowed = []
    for v in vertices:
        forbidden = {int(literal[int(b[1:])]) for b in case["boundary_attachments"][v]}
        allowed.append(tuple(c for c in COLOURS if c not in forbidden))
    result = []
    # This is a direct Cartesian enumeration, independent of blocks and transfer.
    for assignment in itertools.product(*allowed):
        if all(assignment[i] != assignment[j] for i, j in edges):
            result.append(list(assignment))
    return result


def make_pins(assignments, r_index, contact_indices, literal, s_spokes=()):
    pins = []
    spoke_forbidden = {int(literal[int(b[1:])]) for b in s_spokes}
    for a in COLOURS:
        for b in COLOURS:
            preimages = [
                vector for vector in assignments
                if vector[r_index] == a
                and all(vector[i] != b for i in contact_indices)
                and b not in spoke_forbidden
            ]
            pins.append({
                "r": a,
                "s": b,
                "preimages": preimages,
                "restored_preimages": preimages if a != int(literal[4]) else [],
            })
    return pins


def make_row(case, literal):
    assignments = direct_assignments(case, literal)
    indices = {v: i for i, v in enumerate(case["vertices"])}
    r_index = indices["r"]
    contact_indices = [indices[v] for v in case["s_contacts"]]
    ambient = []
    for tau0 in COLOURS:
        for tau1 in COLOURS:
            for a in COLOURS:
                preimages = [
                    vector for vector in assignments
                    if vector[contact_indices[0]] == tau0
                    and vector[contact_indices[1]] == tau1
                    and vector[r_index] == a
                ]
                ambient.append({"tuple": [tau0, tau1], "r": a, "preimages": preimages})
    return {
        "literal": literal,
        "assignments": assignments,
        "ambient_fibres": ambient,
        "pins": make_pins(assignments, r_index, contact_indices, literal),
        "spoke_variants": [
            {"s_spokes": list(spokes), "pins": make_pins(assignments, r_index, contact_indices, literal, spokes)}
            for spokes in S_SPOKE_VARIANTS
        ],
    }


def enumerate_certificate(raw):
    supplied = json.loads(raw)
    cases = supplied["cases"] if isinstance(supplied, dict) else supplied
    literals = supplied.get("literals", list(LITERALS)) if isinstance(supplied, dict) else list(LITERALS)
    if tuple(literals) != LITERALS:
        raise ValueError("cases.json: shared literal rows differ from the fixed ten-row domain")
    if len(cases) > 8 or any(len(case["vertices"]) > 11 for case in cases):
        raise ValueError("cases.json: declared finite bound exceeded (at most 8 cases, 11 C vertices each)")
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("cases.json: duplicate declared case id")
    records = []
    failed = []
    for case in cases:
        findings = degree_findings(case)
        if findings:
            failed.append({"case_id": case["id"], "findings": findings})
            continue
        records.append({
            "case_id": case["id"],
            "vertices": case["vertices"],
            "rows": [make_row(case, literal) for literal in literals],
        })
    return {
        "schema": 1,
        "cases_sha256": hashlib.sha256(raw).hexdigest(),
        "cases": records,
        "failed_cases": failed,
        "target_source": {"executed": False, "trigger_count": None, "status": "not triggered"},
    }


def first_difference(expected, actual, path="certificate", vertices=()):
    """Name the first discrepant original cell and, for vectors, its vertex."""
    if type(expected) is not type(actual):
        return f"{path}: expected type {type(expected).__name__}, got {type(actual).__name__}"
    if isinstance(expected, dict):
        if "case_id" in expected:
            path += f" case={expected['case_id']}"
            vertices = expected.get("vertices", vertices)
        if "literal" in expected:
            path += f" row={expected['literal']}"
        if "tuple" in expected and "r" in expected:
            path += f" ambient cell tuple={expected['tuple']},r={expected['r']}"
        elif "r" in expected and "s" in expected:
            path += f" pin cell (r,s)=({expected['r']},{expected['s']})"
        if "s_spokes" in expected:
            path += f" s_spokes={expected['s_spokes']}"
        for key in expected:
            if key not in actual:
                return f"{path}: missing required field {key}"
            mismatch = first_difference(expected[key], actual[key], f"{path}.{key}", vertices)
            if mismatch:
                return mismatch
        for key in actual:
            if key not in expected:
                return f"{path}: unexpected field {key}"
        return None
    if isinstance(expected, list):
        if path.endswith(".vertices") and expected != actual:
            missing = [v for v in expected if v not in actual]
            if missing:
                return f"{path}: missing original vertex {missing[0]}"
        # Named lists are compared by their declared order, but diagnose an
        # absent empty fibre before a shifted neighbour obscures its identity.
        key_fields = None
        if path.endswith(".ambient_fibres"):
            key_fields = ("tuple", "r")
        elif path.endswith(".pins"):
            key_fields = ("r", "s")
        elif path.endswith(".rows"):
            key_fields = ("literal",)
        elif path.endswith(".cases") or path.endswith(".failed_cases"):
            key_fields = ("case_id",)
        elif path.endswith(".spoke_variants"):
            key_fields = ("s_spokes",)
        if key_fields is not None and all(isinstance(item, dict) for item in actual):
            def cell_key(item):
                return tuple(json.dumps(item.get(k), sort_keys=True) for k in key_fields)
            actual_keys = {cell_key(item) for item in actual}
            for item in expected:
                if cell_key(item) not in actual_keys:
                    named = ",".join(f"{k}={item[k]}" for k in key_fields)
                    return f"{path}: missing named cell {named} (empty fibres are mandatory)"
        common = min(len(expected), len(actual))
        for index in range(common):
            vector = expected[index]
            if isinstance(vector, list) and all(isinstance(c, int) for c in vector) and len(vector) == len(vertices):
                got = actual[index]
                if isinstance(got, list):
                    for coordinate in range(min(len(vector), len(got))):
                        if vector[coordinate] != got[coordinate]:
                            return f"{path}[{index}]: original vertex {vertices[coordinate]} expected colour {vector[coordinate]}, got {got[coordinate]}"
                    if len(vector) != len(got):
                        vertex = vertices[min(len(vector), len(got))] if len(got) < len(vertices) else "extra coordinate"
                        return f"{path}[{index}]: original vertex {vertex} has missing or extra coordinate"
            mismatch = first_difference(vector, actual[index], f"{path}[{index}]", vertices)
            if mismatch:
                return mismatch
        if len(expected) != len(actual):
            return f"{path}: expected {len(expected)} entries, got {len(actual)}"
        return None
    if expected != actual:
        return f"{path}: expected {expected!r}, got {actual!r}"
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    parser.add_argument("--write", type=Path, help="exclusively create a full certificate")
    parser.add_argument("--check", action="store_true", help="compare a certificate, strictly read only")
    parser.add_argument("--certificate", type=Path, help="certificate to compare with direct enumeration")
    args = parser.parse_args(argv)
    if args.write is not None and args.check:
        parser.error("--write and --check are mutually exclusive")
    if args.check and args.certificate is None:
        parser.error("--check requires --certificate")
    if args.certificate is not None and not args.check:
        parser.error("--certificate requires --check")
    try:
        expected = enumerate_certificate(args.cases.read_bytes())
        if args.check:
            actual = json.loads(args.certificate.read_bytes())
            mismatch = first_difference(expected, actual)
            if mismatch:
                print(f"REJECT: {mismatch}", file=sys.stderr)
                return 1
            print("ACCEPT: all original assignments, ambient fibres, ordered pins, literal restoration filters and original vertices agree")
        else:
            rendered = json.dumps(expected, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            if args.write is not None:
                with args.write.open("x", encoding="utf-8") as handle:
                    handle.write(rendered)
                print(f"WROTE: {args.write}")
            else:
                sys.stdout.write(rendered)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
