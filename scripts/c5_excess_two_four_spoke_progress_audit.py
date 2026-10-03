#!/usr/bin/env python3
"""Audit saved four-spoke progress without rewriting historical certificates.

Compare the entire singles mathematical payload and all non-document input
hashes. Keep its strict byte check separate from the documented hash drift.
Group the existing named unequal-pair frames without enumerating source graphs.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path

import c5_excess_two_mixed_core_four_spoke_singles as singles

ROOT = Path(__file__).resolve().parents[1]
PAIR = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_equal_pair/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
OUT = ROOT / 'artifacts/c5_excess_two_four_spoke_progress_audit/observations.json'


def partitions(n, maximum=None):
    if n == 0:
        yield []
        return
    for first in range(min(n, n if maximum is None else maximum), 0, -1):
        for rest in partitions(n - first, first):
            yield [first, *rest]


def incidence_profiles(spokes):
    # Each degree-five root spends one edge on the other original root.
    budgets = [5 - 1 - t for t in spokes]
    profiles = []
    for ca in range(1, budgets[0] + 1):
        for cb in range(1, budgets[1] + 1):
            for ua in partitions(budgets[0] - ca):
                for ub in partitions(budgets[1] - cb):
                    assert ca + sum(ua) == budgets[0]
                    assert cb + sum(ub) == budgets[1]
                    profiles.append(dict(mixed_incidence=[ca, cb],
                        unary_contact_partitions=[ua, ub]))
    assert len(profiles) == 4
    return dict(original_spokes=spokes, original_root_degrees=[5, 5],
        remaining_incidence_budgets=budgets, profiles=profiles,
        scope='Degree arithmetic only; not a source realization or exclusion')


def singles_audit():
    saved = json.loads(singles.OUT.read_text())
    current = json.loads(json.dumps(singles.build()))
    recorded_inputs = saved.pop('input_sha256')
    current_inputs = current.pop('input_sha256')
    assert recorded_inputs.keys() == current_inputs.keys()
    drift = [dict(path=p, recorded_sha256=digest, current_sha256=current_inputs[p])
        for p, digest in sorted(recorded_inputs.items()) if digest != current_inputs[p]]
    assert [d['path'] for d in drift] == ['docs/c5_excess_two_mixed_core_leaf_fibers.md']
    assert saved == current, 'complete singles mathematical payload differs'
    return dict(source_artifact=str(singles.OUT.relative_to(ROOT)),
        source_artifact_sha256=sha256(singles.OUT.read_bytes()).hexdigest(),
        complete_mathematical_payload_equal=True,
        all_non_document_input_hashes_equal=True,
        document_provenance_drift=drift, historical_byte_check_passed=False,
        source_artifact_rewritten=False)


def named_frontier():
    source = json.loads(SOURCE.read_text())
    pair = json.loads(PAIR.read_text())
    targets = []
    for target in pair['targets']:
        sigma = target['source_sigma']
        original = next(t for t in source['targets'] if t['source_sigma'] == sigma)
        records = original['named_spoke_skeletons']['records']
        groups = {0: [], 1: []}
        for frame in target['remaining_unequal_pair_frames']:
            item = records[frame['inherited_named_skeleton_index']]
            assert item['status'] == 'necessary_skeleton_only'
            assert frame['original_root_order'] == item['root_order']
            assert frame['original_spoke_supports'] == item['original_spoke_supports']
            assert frame['original_root_and_boundary_edges'] == item['retained_source_edges']
            assert frame['inherited_skeleton_apex_rotation'] == item['apex_rotation']
            sa, sb = frame['original_spoke_supports']
            assert len(sa) == len(sb) == 2 and sa != sb
            overlap = len(set(sa) & set(sb))
            assert overlap in groups
            groups[overlap].append(frame)
        counts = [len(groups[0]), len(groups[1])]
        assert counts == ([14, 26] if sigma == 933 else [18, 48])
        assert len({f['inherited_named_skeleton_index']
            for group in groups.values() for f in group}) == sum(counts)
        targets.append(dict(source_sigma=sigma,
            groups=[dict(shared_boundary_vertices=k, named_frames=groups[k]) for k in (0, 1)],
            counts=dict(disjoint_pairs=counts[0], one_shared_vertex=counts[1], total=sum(counts))))
    return targets


def build():
    audit = singles_audit()
    targets = named_frontier()
    inputs = [Path(__file__), Path(singles.__file__), singles.OUT, PAIR, SOURCE]
    return dict(schema=1, scope=__doc__,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        singles_provenance_audit=audit,
        degree_budget_incidence_profiles=[incidence_profiles([3, 1]), incidence_profiles([2, 2])],
        named_unequal_pair_frontier=targets,
        summary=dict(complete_singles_mathematical_payload_equal=True,
            singles_document_hash_drifts=1, singles_historical_byte_check_passed=False,
            remaining_named_frame_counts=[40, 66], disjoint_pair_counts=[14, 18],
            one_shared_boundary_vertex_counts=[26, 48],
            old_artifacts_rewritten=False, source_graph_enumeration=False,
            new_source_exclusion=False, epsilon_three_proved=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=1) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
