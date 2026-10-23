#!/usr/bin/env python3
"""Read-only independent calibration of exits and complete-star counting.

The finite graphs are restrictions of the same predecessor cells.  The
existence of the exterior link exits and the complete source stars belongs
to PROOF.md; this checker does not enumerate disk or source completions.
"""
import argparse
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREV = 'audits/2026-10-23-941-gamma8-m2-stars-6b09cd4/certificate.json'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def custody():
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    require(manifest['schema'] == '941-gamma8-rootless-stars-inputs-v1', 'input schema drift')
    require(manifest['base'] == BASE, 'input BASE drift')
    for item in manifest['inputs']:
        snapshot = (HERE / item['snapshot']).read_bytes()
        require((len(snapshot), sha256(snapshot).hexdigest()) ==
                (item['bytes'], item['sha256']), 'authority snapshot drift: ' + item['path'])
        require(snapshot == (ROOT / item['path']).read_bytes(),
                'live authority drift: ' + item['path'])
    for item in manifest['preserved_prior_outputs']:
        data = (ROOT / item['path']).read_bytes()
        require((len(data), sha256(data).hexdigest()) ==
                (item['bytes'], item['sha256']), 'prior output drift: ' + item['path'])
    for item in manifest['routing_entry']:
        snapshot = (HERE / item['snapshot']).read_bytes()
        require((len(snapshot), sha256(snapshot).hexdigest()) ==
                (item['bytes'], item['sha256']), 'routing snapshot drift: ' + item['path'])
    require((len(manifest['inputs']), len(manifest['preserved_prior_outputs']),
             len(manifest['routing_entry'])) == (11, 442, 4), 'custody domain changed')
    return dict(inputs=11, prior_outputs=442, routing_snapshots=4, immutable_drift=0)


def adjacency(edges, vertices):
    result = {v: set() for v in vertices}
    for a, b in edges:
        require(a != b and a in result and b in result, 'invalid known edge')
        result[a].add(b)
        result[b].add(a)
    return result


@lru_cache(maxsize=1)
def reconstruct():
    predecessor = json.loads((HERE / 'frozen' / PREV).read_text())
    cells_certificate = predecessor['complete_predecessor_certificate']['complete_predecessor_certificate']
    boundary = cells_certificate['boundary']
    colors = cells_certificate['original_colors']
    labels = cells_certificate['original_component_labels']
    require(set(boundary) == {'r', 'T', 's', 'x', 'h', 'W', 'e', 'd'}, 'Gamma domain changed')
    require(all(colors[v] != 2 for v in boundary), 'Gamma acquired original color 2')

    cell_rows = []
    for cell in cells_certificate['candidates']:
        if cell['classification'] != 'local_necessary_type':
            continue
        adj = adjacency(cell['edges'], colors)
        require('x' not in adj['d'] and adj['x'] & adj['d'] & {'tau', 'zeta'},
                'd/x lack the interior common-neighbor obstruction')
        for center, N_endpoint, B_endpoint in [('d', 'r', 'e'), ('x', 's', 'h')]:
            require(colors[center] == 0 and labels[center] == 'K', 'exit center is not K0')
            require(colors[N_endpoint] == colors[B_endpoint] == 1 and
                    labels[N_endpoint] == 'N' and labels[B_endpoint] == 'B',
                    'exit endpoints do not leave the complete N13 component')
            require({N_endpoint, B_endpoint} <= adj[center], 'exit sector boundary edge missing')
        require(adj['T'] - set(boundary) == {'tau'}, 'T interior star changed')
        for interior in ('tau', 'zeta'):
            require(sorted(adj[interior]) == cell['full_private_stars'][interior] and
                    len(adj[interior]) == cell['full_private_degrees'][interior] >= 5,
                    'complete interior star changed')
        cell_rows.append(dict(id=cell['id'], core=cell['core'],
            blocked_exterior_common_neighbor_pair=['d', 'x'], K2_exit_centers=['d', 'x'],
            T_interior_neighbors=['tau'], boundary_without_color2=True))
    require(len(cell_rows) == 11, 'eleven-cell domain changed')

    boundary_rows = []
    for side in ('C', 'E'):
        # An M2 vertex can meet original M0, cannot meet K0 or B13, and
        # cannot merge the distinct complete psi12 components C and E.
        possible = []
        for v in boundary:
            if colors[v] == 0 and labels[v] == 'M':
                possible.append(v)
            elif labels[v] == 'N' and colors[v] == 1:
                if {'r': 'C', 's': 'E'}[v] == side:
                    possible.append(v)
        require(len(possible) == 2, 'M2 boundary-neighbor upper bound differs')
        boundary_rows.append(dict(side=side, allowed_Gamma_neighbors=sorted(possible)))

    prefix_rows = []
    for row in predecessor['prefix_rows']:
        names = {role: 'out_' + min(group) for group in row['partition'] for role in group}
        m_roles = [role for role, kind in row['kinds'].items() if kind == 'M2']
        require(len(m_roles) == 1, 'T degree-five prefix has no unique M2 role')
        m = names[m_roles[0]]
        prefix_colors = row['complete_prefix_orbit'][0]['colors']
        adj = adjacency(row['edges'], prefix_colors)
        gamma_neighbors = sorted(adj[m] & set(boundary))
        permitted = next(r['allowed_Gamma_neighbors'] for r in boundary_rows
                         if r['side'] == row['T_M2_side'])
        require(gamma_neighbors == permitted, 'known M2 Gamma contacts differ')
        require(len(adj['T']) == 5 and len(adj[m]) == 3, 'forced T/m prefix star changed')
        common = adj['T'] & adj[m]
        require(len(common) == 2 and len(common & set(boundary)) == 1,
                'two known facial common neighbors of Tm changed')
        require(all(prefix_colors[v] != 2 for v in adj[m]), 'M2 has a color-2 neighbor')
        K2_faces = sorted({names[role] for role, kind in row['kinds'].items() if kind == 'K2'})
        require(all(prefix_colors[v] == 2 and v not in adj[m] and v != m for v in K2_faces),
                'K2/m-star disjointness failed')
        prefix_rows.append(dict(id=row['id'], core=row['core'], T_M2_side=row['T_M2_side'],
            m_vertex=m, Gamma_neighbors=gamma_neighbors, known_prefix_neighbors=sorted(adj[m]),
            private_K2_face_vertices=K2_faces, minimum_external_vertices=6, opposite_cut_bound=8))
    require(len(prefix_rows) == 104, 'full prefix multiplicity changed')

    departure_rows = []
    for start in ('N1', 'N3'):
        for following in ('N1', 'N3', 'Other1', 'Other3', 'K2', 'Other2'):
            proper = int(start[-1]) != int(following[-1])
            same_13_component = following.startswith('N')
            same_02_as_center = following == 'K2'
            allowed = proper and (same_13_component or same_02_as_center)
            departure_rows.append(dict(from_kind=start, next_kind=following, allowed=allowed))
    require(sum(r['allowed'] for r in departure_rows) == 4, 'first-departure transition audit differs')
    return predecessor, cell_rows, prefix_rows, departure_rows, boundary_rows


def validate(certificate, seed=0):
    predecessor, cells, prefixes, departures, boundary = reconstruct()
    require(certificate['schema'] == '941-gamma8-rootless-stars-v1' and
            certificate['base'] == BASE, 'certificate schema/BASE drift')
    require(certificate['complete_predecessor_certificate'] == predecessor,
            'complete predecessor fibres, empty rows, or lifts changed')
    for key, expected in [('cell_obligations', cells), ('prefix_audits', prefixes),
                          ('first_departure_trials', departures), ('m_boundary_audit', boundary)]:
        require(isinstance(certificate[key], list) and len(certificate[key]) == len(expected),
                key + ' domain incomplete')
        indices = list(range(len(expected)))
        random.Random(seed).shuffle(indices)
        for index in indices:
            require(certificate[key][index] == expected[index], key + ' changed at row ' + str(index))
    require(certificate['algebra_contract'] == dict(
        b_means='all original Gamma neighbors', max_b=2, min_degree=5,
        protected_bound='degree+3-b', full_M2_bound='degree+M2_size+2-b',
        adjacent_two_star_bound='T_degree+degree-4',
        nonadjacent_two_star_bound='T_degree+degree-2',
        minimum_if_M2_nonempty=6,
        minimum_if_T_degree_at_least_6_and_M2_nonempty=7,
        minimum_if_T_degree5_and_M2_not_singleton=8,
        six_vertex_residual=dict(M2_size=1, m_degree=5, Gamma_neighbors=2, T_degree=5),
        M2_empty=dict(M_singleton_T=True, T_degree_even=True)), 'algebra or six-point residual changed')
    require(certificate['paper_contract'] == dict(
        j=2, same_original_exterior=True, full_original_stars=True,
        full_M2_set_retained=True, E_may_be_rootless=True,
        first_departure_K2_from_d_and_x=True,
        first_departure_stays_in_F_when_d_is_U=True,
        distinct_exterior_K2_exits=True, private_M_star_degree_at_least=5,
        protected_exterior_bound=6, opposite_separator_exterior_bound=8,
        six_vertex_residual_uses_C3_faces=True,
        prefix_rows_are_not_complete_stars_or_disk_completions=True),
        'paper premise, privacy, or exterior bound changed')
    require(certificate['authority_boundaries'] == dict(
        finite_control='triggered and holds', original_source_control='not triggered',
        general_wrong_side='OPEN', eleven_type_exclusions=0, initial_pair_exclusions=0,
        common_k_lower_bound=23, smaller_bad=False, new_Lean=False, new_LP=False),
        'unsupported source, exclusion, or theorem promotion')
    return dict(actual_cells=len(cells), predecessor_prefix_rows=len(prefixes),
        distinct_prefix_audits=len({json.dumps(r, sort_keys=True) for r in prefixes}),
        first_departure_trials=len(departures), allowed_first_departure_transitions=4,
        M2_side_boundary_audits=len(boundary), Tm_known_facial_common_neighbor_pairs=len(prefixes),
        original_source_control='not triggered', eleven_type_exclusions=0)


def negatives(certificate):
    mutations = [
        ('missing_cell', lambda c: c['cell_obligations'].pop()),
        ('lose_interior_common_neighbor_ban', lambda c: c['cell_obligations'][0].update(
            blocked_exterior_common_neighbor_pair=['r', 's'])),
        ('lose_d_exit', lambda c: c['cell_obligations'][0]['K2_exit_centers'].pop(0)),
        ('missing_prefix', lambda c: c['prefix_audits'].pop()),
        ('alter_m_contact', lambda c: c['prefix_audits'][0]['Gamma_neighbors'].append('s')),
        ('lose_known_m_neighbor', lambda c: c['prefix_audits'][0]['known_prefix_neighbors'].pop()),
        ('alter_K2_face_identity', lambda c: c['prefix_audits'][0]['private_K2_face_vertices'].append('T')),
        ('admit_other_13_component', lambda c: c['first_departure_trials'][2].update(allowed=True)),
        ('admit_foreign_02_component', lambda c: c['first_departure_trials'][5].update(allowed=True)),
        ('drop_transition', lambda c: c['first_departure_trials'].pop()),
        ('allow_both_C_E_neighbors', lambda c: c['m_boundary_audit'][0]['allowed_Gamma_neighbors'].append('s')),
        ('allow_three_Gamma_neighbors', lambda c: c['algebra_contract'].update(max_b=3)),
        ('drop_degree_five', lambda c: c['algebra_contract'].update(min_degree=4)),
        ('drop_complete_M2_count', lambda c: c['algebra_contract'].update(full_M2_bound='degree+3-b')),
        ('weaken_adjacent_two_star_bound', lambda c: c['algebra_contract'].update(adjacent_two_star_bound='T_degree+degree-5')),
        ('miscount_nonadjacent_star_overlap', lambda c: c['algebra_contract'].update(nonadjacent_two_star_bound='T_degree+degree-3')),
        ('lose_non_singleton_M2_bound', lambda c: c['algebra_contract'].update(minimum_if_T_degree5_and_M2_not_singleton=7)),
        ('lose_six_vertex_T_degree', lambda c: c['algebra_contract']['six_vertex_residual'].update(T_degree=6)),
        ('make_empty_M2_have_two_vertices', lambda c: c['algebra_contract']['M2_empty'].update(M_singleton_T=False)),
        ('drop_d_U_privacy', lambda c: c['paper_contract'].update(first_departure_stays_in_F_when_d_is_U=False)),
        ('drop_complete_original_stars', lambda c: c['paper_contract'].update(full_original_stars=False)),
        ('shrink_full_M2', lambda c: c['paper_contract'].update(full_M2_set_retained=False)),
        ('presume_E_rooted', lambda c: c['paper_contract'].update(E_may_be_rootless=False)),
        ('raise_protected_bound', lambda c: c['paper_contract'].update(protected_exterior_bound=7)),
        ('lose_C3_premise', lambda c: c['paper_contract'].update(six_vertex_residual_uses_C3_faces=False)),
        ('lose_prior_empty_fibre', lambda c: c['complete_predecessor_certificate']
            ['complete_predecessor_certificate']['complete_predecessor_certificate']['candidates'][0]
            ['literal_phi_boundary_fibre']['all_other_inner_assignments'].pop()),
        ('promote_source', lambda c: c['authority_boundaries'].update(original_source_control='triggered and holds')),
        ('exclude_local_type', lambda c: c['authority_boundaries'].update(eleven_type_exclusions=1)),
        ('raise_global_k', lambda c: c['authority_boundaries'].update(common_k_lower_bound=24)),
    ]
    results = []
    for name, mutation in mutations:
        bad = deepcopy(certificate)
        mutation(bad)
        try:
            validate(bad)
        except (ValueError, KeyError, TypeError, IndexError):
            results.append(dict(name=name, status='rejected'))
        else:
            raise ValueError('accepted negative: ' + name)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate-v2.json')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    authority = custody()
    certificate = json.loads(args.certificate.read_text())
    result = dict(status='PASS', seed=args.seed, custody=authority, **validate(certificate, args.seed))
    if args.negative:
        result['semantic_negatives'] = negatives(certificate)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, IndexError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT', reason=str(exc))))
        sys.exit(1)
