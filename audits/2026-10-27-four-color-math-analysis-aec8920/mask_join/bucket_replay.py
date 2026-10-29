"""Replay frozen exact buckets; this is NOT a modified whole-solver benchmark."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from math import prod
from pathlib import Path

from audit import Factor, projected_prefix, validate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--case", action="append")
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    source_report = json.loads(args.report.read_text())
    groups = []
    totals = {"literal": Counter(), "mask": Counter()}
    stats = Counter()
    for group in source_report["cases"]:
        if args.case and group["name"] not in args.case:
            continue
        assert len(group["results"]) == 1
        metadata = next(iter(group["results"].values()))
        path = args.report.parent / metadata["full_record"]
        compressed_hash = sha256(path.read_bytes()).hexdigest()
        assert compressed_hash == metadata["compressed_record_sha256"]
        record = json.loads(gzip.decompress(path.read_bytes()))
        buckets = []
        for index, bucket in enumerate(record["elimination_records"]):
            assert bucket["complete"] is True
            owner, boundary = bucket["vertex"], tuple(bucket["scope"])
            domains = {entry["vertex"]: tuple(entry["colors"]) for entry in bucket["source_domains"]}
            factors = [Factor(tuple(f["scope"]), frozenset(map(tuple, f["rows"])))
                       for f in bucket["input_relations"]]
            validate(owner, boundary, domains, factors)
            expected = {tuple(row["boundary"]): sum(1 << c for c in row["colors"])
                        for row in bucket["rows"]}
            anchor = min(range(len(factors)), key=lambda i: len(factors[i].rows) * prod(
                len(domains[v]) for v in boundary if v not in factors[i].scope)) if factors else None
            old = projected_prefix(owner, boundary, domains, factors, anchor, masks=False)
            new = projected_prefix(owner, boundary, domains, factors, anchor, masks=True)
            assert old[0] == new[0] == expected, (group["name"], index, "complete fibre maps")
            assert old[2] == new[2] and old[3] == new[3], (group["name"], index, "prefix projections")
            for field in ("candidate_attempts", "ready_factor_lookups", "attempted_prefix_visits",
                          "surviving_prefix_visits", "output_updates"):
                assert new[1][field] <= old[1][field], (group["name"], index, field)
            # A transparent charge model, solely for separating row preparation
            # from online work. It excludes tuple construction, bit ops, domain
            # tests, sorting, allocations and trace instrumentation from BOTH.
            old_charge = (old[1]["literal_anchor_rows_scanned"] + old[1]["candidate_attempts"]
                          + old[1]["ready_factor_lookups"])
            new_charge = (new[1]["preprocess_input_rows"] + new[1]["candidate_attempts"]
                          + new[1]["ready_factor_lookups"])
            domain_size = prod(len(domains[v]) for v in boundary)
            assert len(expected) <= domain_size
            buckets.append(dict(index=index, owner=owner, boundary_points=len(boundary),
                                boundary_domain_size=domain_size, nonempty_fibres=len(expected),
                                empty_fibres=domain_size-len(expected),
                                anchor_index=anchor, literal_stats=dict(old[1]), mask_stats=dict(new[1]),
                                row_visit_extension_lookup_charge=dict(literal=old_charge, mask=new_charge),
                                exact_saved_complete_fibre_map_equal=True,
                                all_depth_prefix_projection_equal=True))
            totals["literal"].update(old[1])
            totals["mask"].update(new[1])
            stats.update(buckets=1, nonempty_fibres=len(expected), empty_fibres=domain_size-len(expected),
                         colour_choices=sum(value.bit_count() for value in expected.values()),
                         input_rows=sum(len(f.rows) for f in factors),
                         literal_charge=old_charge, mask_charge=new_charge)
            stats["charge_improved" if new_charge < old_charge else
                  "charge_tied" if new_charge == old_charge else "charge_increased"] += 1
        groups.append(dict(name=group["name"], graph_sha256=group["graph_sha256"],
                           full_record=str(path), compressed_record_sha256=compressed_hash,
                           source_status=record["status"], buckets=buckets))
        print(f"PASS {group['name']}: {len(buckets)} frozen buckets")
    if args.case:
        assert {g["name"] for g in groups} == set(args.case)
    output = dict(schema="frozen-owner-mask-bucket-replay-v1",
                  source_report=str(args.report), source_report_sha256=sha256(args.report.read_bytes()).hexdigest(),
                  source_solver_kind=source_report["solver_source_kind"],
                  prototype_sources={p.name: sha256(p.read_bytes()).hexdigest()
                                     for p in (Path(__file__), Path(__file__).with_name("audit.py"))},
                  groups=groups, case_count=len(groups), totals=dict(stats),
                  literal_online_and_anchor_totals=dict(totals["literal"]),
                  mask_preprocessing_and_online_totals=dict(totals["mask"]),
                  limitations=["Fixed frozen buckets only; no changed propagation, elimination schedule or whole solve.",
                               "Large buckets checked against frozen complete recorded fibres; independent Cartesian oracle belongs to audit.py small inputs.",
                               "Same literal-selected anchor and same free/ready order for the prefix projection theorem.",
                               "The row-visit/extension/lookup charge is a hypothetical model, not main checks, CPU or a speed claim.",
                               "Complete trace projection equality is measured with expensive audit instrumentation, not optimized code timing.",
                               "Preparation scans every input row again in each bucket; no index sharing across buckets."])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(dict(case_count=len(groups), **stats), sort_keys=True))


if __name__ == "__main__":
    main()
