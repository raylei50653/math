#!/usr/bin/env python3
"""Exclusive-create the bounded two-patch role calibration; no source search."""
from copy import deepcopy
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = 'audits/2026-10-23-three-mask-round5-cb8f859/941/certificate.json'
CYCLE = (0, 2, 3, 1)
DIAGONALS = ((0, 3), (2, 1))


def schemas():
    rows = []
    for shared in combinations(range(4), 2):
        roles = [{c: f'{c}a' for c in range(4)},
                 {c: f'{c}a' if c in shared else f'{c}b' for c in range(4)}]
        for ds in product(range(2), repeat=2):
            edges, centers, faces = set(), [], []
            for role, d in zip(roles, ds):
                edges.update(tuple(sorted((role[a], role[b])))
                             for a, b in zip(CYCLE, CYCLE[1:] + CYCLE[:1]))
                center = tuple(sorted(role[c] for c in DIAGONALS[d]))
                centers.append(list(center)); edges.add(center)
                triples = ((0, 2, 3), (0, 3, 1)) if d == 0 else ((0, 2, 1), (2, 3, 1))
                faces.extend([[role[c] for c in t] for t in triples])
            vertices = sorted(set(roles[0].values()) | set(roles[1].values()))
            k4 = next((list(vs) for vs in combinations(vertices, 4)
                       if all(tuple(sorted(e)) in edges for e in combinations(vs, 2))), None)
            if centers[0] == centers[1]:
                kind = 'same_center'
            elif k4:
                kind = 'K4'
            elif shared in ((0, 3), (1, 2)):
                kind = 'C4_two_nonedges'
            else:
                kind = 'common_cycle_edge'
            row = dict(shared_colors=list(shared), diagonal_choices=list(ds),
                       roles=[{str(c): v for c, v in r.items()} for r in roles],
                       edges=[list(e) for e in sorted(edges)], faces=faces,
                       centers=centers, classification=kind)
            if kind == 'K4':
                row['blocker'] = k4
            elif kind == 'C4_two_nonedges':
                missing = next(c for c in range(4) if c not in shared)
                row['blocker'] = [roles[0][shared[0]], roles[0][missing],
                                  roles[0][shared[1]], roles[1][missing]]
            elif kind == 'common_cycle_edge':
                interface, side = {(0, 2): ('beta', 'K'), (1, 3): ('beta', 'B'),
                                   (0, 1): ('alpha', 'C'), (2, 3): ('alpha', 'Q')}[shared]
                row.update(consecutive_interface=interface, intervening_side=side,
                           partial_disk_only=True,
                           private_shared_vertex_link={
                               str(c): dict(incident_centers=sum(c in DIAGONALS[d] for d in ds),
                                            union_neighbors=3 + sum(c in DIAGONALS[d] for d in ds),
                                            degree_lower_bound=max(5, 4 + sum(c in DIAGONALS[d] for d in ds)))
                               for c in shared})
            rows.append(row)
    return rows


def main():
    previous = json.loads((HERE / 'frozen' / PREV).read_text())
    cert = dict(schema='941-patch-order-v1',
                base='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd',
                complete_predecessor_certificate=deepcopy(previous),
                exact_two_shared_schemas=schemas(),
                paper_claims=dict(
                    transverse_crossings_even_at_least_two=True,
                    tangencies_separated_locally_preserving_markers=True,
                    alpha_marked_pair='Q excursion containing P last K exit midpoint',
                    beta_marked_pair='Omega excursion containing marked u-minus Z midpoint',
                    marked_pairs_may_differ=True,
                    alpha_pair_allowed_two_shared_colors=[[0, 2], [1, 3]],
                    beta_pair_allowed_two_shared_colors=[[0, 1], [0, 2], [2, 3]],
                    beta_pair_shared02_is_marked_u_minus_Z=True,
                    alpha_pair_shared13_forces_at_least_four_crossings=True,
                    ear_lens_exists_but_need_not_contain_marker=True,
                    ear_lens_may_be_C_or_Q=True,
                    other_complete_component_interfaces_retained=True),
                boundaries=dict(source_control='not triggered', finite_calibration='triggered and holds',
                    new_initial_pair_exclusions=0, source_realized=False, smaller_bad=False,
                    new_Lean=False, no_source_enumeration_or_LP=True,
                    R_r_not_identified=True, M_L_not_identified=True,
                    K0_not_assumed_all_C=True, boundary_tip_and_rootless_retained=True,
                    original_degree5_sides_and_high_degree_retained=True,
                    original_P_and_B13_joint_realization='OPEN'))
    with (HERE / 'certificate.json').open('x') as stream:
        json.dump(cert, stream, ensure_ascii=False, indent=2, sort_keys=True); stream.write('\n')
    print(json.dumps(dict(status='CREATED', bounded_schemas=24)))


if __name__ == '__main__':
    main()
