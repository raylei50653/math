#!/usr/bin/env python3
"""Five fixed C6--C8 patches: exact interfaces, Boolean D and derived locks.

No catalogue, Four Color Theorem oracle, new graph search or block-count
implementation is used. Complete original-edge enumeration independently checks
the production constraint engine. A second partition generator checks every
abstract option; same-orbit partitions remain distinct when auditing locks.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import ck_kempe_obstruction as ck
from four_color_constraints import solve_constraints
from configurations import configurations, validate_disk


def normal(row):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in row)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def all_partitions(k):
    """Independent restricted-growth generator on all boundary positions."""
    def words(prefix, maximum):
        if len(prefix) == k:
            yield tuple(tuple(i for i, value in enumerate(prefix) if value == block)
                        for block in range(maximum + 1))
            return
        for value in range(maximum + 2):
            yield from words(prefix + [value], max(maximum, value))
    return tuple(words([], -1))


def path_arrangement_topology(blocks, k):
    """Use connectivity after deleting a boundary block, not alternation tests."""
    for removed in blocks:
        remaining = set(range(k)) - set(removed)
        components = {}
        while remaining:
            start = min(remaining)
            pending = [start]
            remaining.remove(start)
            components[start] = start
            for v in pending:
                for w in ((v - 1) % k, (v + 1) % k):
                    if w in remaining:
                        remaining.remove(w)
                        components[w] = start
                        pending.append(w)
        if any(len({components[v] for v in block}) != 1
               for block in blocks if block != removed):
            return False
    return True


def independent_partition_audit():
    result = []
    for k, bell, catalan in ((5, 52, 42), (6, 203, 132), (7, 877, 429), (8, 4140, 1430)):
        partitions = all_partitions(k)
        assert len(partitions) == bell
        planar = []
        for blocks in partitions:
            noncross = path_arrangement_topology(blocks, k)
            assert noncross == ck.noncrossing(blocks)
            if noncross:
                planar.append(blocks)
        assert len(planar) == catalan
        states = ck.patterns(k)
        index = {b: j for j, b in enumerate(states)}
        option_count = 0
        checks = 0
        for j, b in enumerate(states):
            for split, pairs in enumerate(ck.PAIRS):
                side = tuple(int(c in pairs[1]) for c in b)
                mate = {c: pair[1 - q] for pair in pairs for q, c in enumerate(pair)}
                independent = set()
                for blocks in planar:
                    owner = {v: q for q, block in enumerate(blocks) for v in block}
                    if any(len({side[v] for v in block}) != 1 for block in blocks):
                        continue
                    if any(side[v] == side[(v + 1) % k]
                           and owner[v] != owner[(v + 1) % k] for v in range(k)):
                        continue
                    orbit = 0
                    for flips in product((False, True), repeat=len(blocks)):
                        changed = tuple(mate[b[v]] if flips[owner[v]] else b[v] for v in range(k))
                        assert all(changed[v] != changed[(v + 1) % k] for v in range(k))
                        orbit |= 1 << index[normal(changed)]
                    independent.add((orbit, tuple(sorted(blocks))))
                actual = set(ck.partition_options(k, j, split))
                assert actual == independent, (k, b, split)
                option_count += len(independent)
                checks += 1
        result.append(dict(k=k, bell_partitions=bell, noncrossing_partitions=catalan,
                           pattern_split_queries=checks, complete_partition_options=option_count,
                           independent_options_equal=True))
    return result


def edge_legal(configuration, assignment):
    return all(assignment[a] != assignment[b] for a, b in configuration["edges"])


def complete_interface(configuration):
    ring = configuration["ring"]
    internal = configuration["internal"]
    states = ck.patterns(len(ring))
    accepted = 0
    fibres = []
    total_checks = 0
    statuses = Counter()
    for j, boundary in enumerate(states):
        fixed = dict(zip(ring, boundary))
        count = 0
        witness = None
        for colors in product(range(4), repeat=len(internal)):
            assignment = fixed | dict(zip(internal, colors))
            if edge_legal(configuration, assignment):
                count += 1
                if witness is None:
                    witness = [assignment[v] for v in configuration["vertices"]]
        graph = dict(vertices=configuration["vertices"], edges=configuration["edges"],
                     fixed=[[v, fixed[v]] for v in ring])
        result = solve_constraints(graph, max_checks=10_000_000, max_table_rows=1_000_000,
                                   trace_limit=0, record_relations=False)
        assert result["status"] in ("colored", "unsatisfiable"), (configuration["name"], boundary)
        assert (result["status"] == "colored") == bool(count)
        if count:
            accepted |= 1 << j
            assignment = dict(zip(result["graph"]["vertices"], result["colors"]))
            assert edge_legal(configuration, assignment)
            assert all(assignment[v] == c for v, c in fixed.items())
        statuses[result["status"]] += 1
        total_checks += result["stats"]["checks"]
        fibres.append(dict(pattern_index=j, boundary=list(boundary),
                           complete_internal_extension_count=count,
                           one_original_graph_lift=witness, engine_status=result["status"]))
    return accepted, dict(fibres=fibres, literal_frame="one fixed canonical boundary row per common S4 orbit",
                          engine_statuses=dict(sorted(statuses.items())), engine_checks=total_checks,
                          engine_vs_independent_complete_interface_equal=True)


def equal_pairs(blocks):
    return {tuple(pair) for block in blocks for pair in combinations(block, 2)}


def lock_augmented_obstruction(k, accepted):
    """Reapply ALL implied same-component relations at every synchronous round."""
    states = ck.patterns(k)
    current = ((1 << len(states)) - 1) ^ accepted
    rounds = []
    residual_rows = []
    while True:
        removed = 0
        rows = []
        discarded_options = 0
        for j, boundary in enumerate(states):
            if not current >> j & 1:
                continue
            for split in range(3):
                all_options = ck.partition_options(k, j, split)
                options = [(orbit, p) for orbit, p in all_options
                           if orbit & current == orbit]
                if not options:
                    removed |= 1 << j
                    continue
                common = set.intersection(*(equal_pairs(p) for _, p in options))
                unconditional = set.intersection(*(equal_pairs(p) for _, p in all_options))
                after = [(orbit, p) for orbit, p in options if common <= equal_pairs(p)]
                discarded_options += len(options) - len(after)
                if not after:
                    removed |= 1 << j
                rows.append(dict(pattern_index=j, boundary=list(boundary), split=split,
                                 admissible_partition_count=len(options),
                                 forced_same_component_pairs=[list(pair) for pair in sorted(common)],
                                 forced_same_colour_pairs=[list(pair) for pair in sorted(common)
                                                           if boundary[pair[0]] == boundary[pair[1]]],
                                 blocking_induced_same_colour_pairs=[
                                     list(pair) for pair in sorted(common - unconditional)
                                     if boundary[pair[0]] == boundary[pair[1]]],
                                 additional_partition_deletions=len(options) - len(after)))
        assert discarded_options == 0
        if not removed:
            residual_rows = rows
            break
        rounds.append(dict(before_mask=current, removed_mask=removed, after_mask=current & ~removed,
                           additional_partition_deletions=discarded_options))
        current &= ~removed
    same_colour = sum(len(row["forced_same_colour_pairs"]) for row in residual_rows)
    all_pairs = sum(len(row["forced_same_component_pairs"]) for row in residual_rows)
    sample = next((row for row in residual_rows if row["forced_same_colour_pairs"]), None)
    blocking_induced = sum(len(row["blocking_induced_same_colour_pairs"]) for row in residual_rows)
    blocking_sample = next((row for row in residual_rows
                            if row["blocking_induced_same_colour_pairs"]), None)
    return dict(residual_mask=current, residual_count=current.bit_count(), rounds=rounds,
                residual_lock_rows=residual_rows,
                forced_same_colour_pair_occurrences=same_colour,
                forced_same_component_pair_occurrences=all_pairs,
                sample_nontrivial_same_colour_lock=sample,
                blocking_induced_same_colour_pair_occurrences=blocking_induced,
                sample_blocking_induced_same_colour_lock=blocking_sample,
                additional_partition_deletions=0, additional_state_deletions=0)


def adjacent_pair_lock_control(configuration, accepted):
    """A genuine blocking-induced lock, with a same-frame extension if broken."""
    boundary = (0, 1, 0, 2, 0, 1)
    changed = (0, 3, 0, 2, 0, 1)
    states = ck.patterns(6)
    assert not accepted >> states.index(normal(boundary)) & 1
    assert accepted >> states.index(normal(changed)) & 1
    assignment = dict(zip(configuration["ring"], changed)) | {6: 1, 7: 3}
    assert edge_legal(configuration, assignment)
    return dict(name=configuration["name"], boundary=list(boundary),
                complementary_split=[[0, 2], [1, 3]], locked_positions=[1, 5],
                lock_colour_pair=[1, 3],
                counterfactual_boundary_if_only_position_1_is_swapped=list(changed),
                complete_inner_extension_if_lock_broken=assignment,
                scope="Conditional on an actual exterior whose whole boundary relation avoids A; this is not a realized exterior.")


def geometry_negative_controls(configuration):
    controls = []
    changes = [
        ("missing_original_edge", lambda c: c["edges"].pop()),
        ("reversed_ring", lambda c: c["ring"].reverse()),
        ("missing_face", lambda c: c["faces"].pop()),
        ("duplicate_face", lambda c: c["faces"].append(c["faces"][0])),
        ("coincident_vertices", lambda c: c["positions"].__setitem__(1, c["positions"][0])),
        ("wrong_internal_identity", lambda c: c["internal"].pop()),
    ]
    for name, mutate in changes:
        changed = deepcopy(configuration)
        mutate(changed)
        try:
            validate_disk(changed)
        except ValueError:
            controls.append(dict(name=name, rejected=True))
        else:
            raise AssertionError(name)
    return controls


def single_witness_negative_control(cases):
    """One support witness cannot prove connectivity shared by all witnesses."""
    for case in cases:
        k = len(case["configuration"]["ring"])
        current = case["boolean_D"]["residual_mask"]
        for j, boundary in enumerate(ck.patterns(k)):
            if not current >> j & 1:
                continue
            for split in range(3):
                options = [(orbit, p) for orbit, p in ck.partition_options(k, j, split)
                           if orbit & current == orbit]
                common = set.intersection(*(equal_pairs(p) for _, p in options))
                for orbit, selected in options:
                    extra = equal_pairs(selected) - common
                    if extra:
                        pair = min(extra)
                        alternative_orbit, alternative = next(
                            (o, p) for o, p in options if pair not in equal_pairs(p))
                        return dict(name=case["name"], k=k, pattern_index=j,
                                    boundary=list(boundary), split=split,
                                    admissible_partition_count=len(options),
                                    chosen_orbit_mask=orbit,
                                    chosen_partition=[list(block) for block in selected],
                                    claimed_but_not_forced_pair=list(pair),
                                    alternative_orbit_mask=alternative_orbit,
                                    alternative_partition=[list(block) for block in alternative],
                                    assertion="A single admissible support partition cannot prove that its connectivity is forced across all admissible partitions.")
    raise AssertionError("expected alternative admissible connectivity")


def source_hashes():
    paths = {Path(__file__).resolve(), Path(__file__).with_name("configurations.py")}
    for name, module in tuple(sys.modules.items()):
        if name.startswith(("four_color_", "ck_kempe_", "c5_kempe_")) and getattr(module, "__file__", None):
            path = Path(module.__file__).resolve()
            if path.is_relative_to(ROOT / "scripts"):
                paths.add(path)
    return {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    base_controls = ck.controls()
    independent = independent_partition_audit()
    cases = []
    patches = configurations()
    expected = {"birkhoff_diamond": (16, 0), "adjacent_5_5": (13, 16),
                "wheel_6": (11, 20), "wheel_7": (21, 70), "wheel_8": (43, 231)}
    for configuration in patches:
        geometry = validate_disk(configuration)
        k = len(configuration["ring"])
        accepted, interface = complete_interface(configuration)
        baseline = ck.obstruction(k, accepted)
        locked = lock_augmented_obstruction(k, accepted)
        assert locked["residual_mask"] == baseline["residual_mask"]
        assert [r["removed_mask"] for r in locked["rounds"]] == [r["removed_mask"] for r in baseline["rounds"]]
        assert (accepted.bit_count(), baseline["residual_count"]) == expected[configuration["name"]]
        cases.append(dict(name=configuration["name"], configuration=configuration,
                          geometry=geometry, interface=interface,
                          boolean_D=baseline, derived_same_component_locks=locked))
    report = dict(
        schema="ck-d-derived-lock-comparison-v1", base="8d28accea79cf8c6418cdb6da4d94010c1c975bf",
        complete_finite_scope="Five named ordered disk patches, not graph-family enumeration.",
        c5_controls=base_controls, independent_partition_audit=independent, cases=cases,
        geometry_negative_controls=geometry_negative_controls(patches[0]),
        single_support_witness_negative_control=single_witness_negative_control(cases),
        blocking_induced_lock_control=adjacent_pair_lock_control(
            patches[1], cases[1]["boolean_D"]["accepted_mask"]),
        conclusion=dict(newly_excluded_D_survivors=0,
                        tested_conditions_reduce_to="Boolean D support consistency",
                        stop_condition_triggered=True, further_graph_enumeration_performed=False,
                        block_count_comparison="Not implemented or claimed: the tested conditions already reduce to Boolean D.",
                        not_ruled_out="An additional cross-split same-source structural theorem with a genuinely new constraint."),
        sources={"classical_D_vertex_definition":"https://arxiv.org/pdf/0905.0043#page=11",
                 "Birkhoff_diamond_free_completion":"https://arxiv.org/pdf/0905.0043#page=10"},
        source_sha256=source_hashes(),
        not_claimed=["4CT assumed or proved", "a new reducibility certificate", "a realization of a surviving exterior", "block-count closure implementation", "new Lean theorem"])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps([dict(name=c["name"], A=c["boolean_D"]["accepted_count"],
                           D=c["boolean_D"]["residual_count"],
                           extra=c["derived_same_component_locks"]["additional_state_deletions"])
                      for c in cases], sort_keys=True))


if __name__ == "__main__":
    main()
