#!/usr/bin/env python3
"""Read-only reconstruction and exhaustive check of the named ten-point local domain."""
import argparse
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVDIR = 'audits/2026-10-23-941-p-b13-6b09cd4'
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
B = ('r', 'T', 's', 'x', 'h', 'W', 'e', 'd')
V = B + ('tau', 'zeta')
PHI = dict(zip(V, [1, 0, 1, 0, 1, 3, 1, 0, 3, 2]))
J = dict(zip(V, ['N', 'M', 'N', 'K', 'B', 'B', 'B', 'K', 'N', 'K']))
H = dict(zip(V, ['C', 'Q', 'E', 'E', 'E', 'Q', 'C', 'C', 'Q', 'Q']))
PSI = {v: c ^ 2 if J[v] == 'K' else c for v, c in PHI.items()}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def edge(a, b):
    return tuple(sorted((a, b)))


BOUND = {edge(a, b) for a, b in zip(B, B[1:] + B[:1])}


def authority():
    m = json.loads((HERE / 'INPUTS.json').read_text()); require(m['base'] == BASE, 'BASE changed')
    for row in m['inputs']:
        data = (HERE / row['snapshot']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (row['bytes'], row['sha256']), 'frozen authority drift')
        require(data == (ROOT / row['path']).read_bytes(), 'live authority drift: ' + row['path'])
    for row in m['preserved_prior_outputs']:
        data = (ROOT / row['path']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (row['bytes'], row['sha256']), 'prior output drift')
    routing = []
    for row in m['routing_entry']:
        data = (HERE / row['snapshot']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (row['bytes'], row['sha256']), 'routing snapshot drift')
        routing.append(dict(path=row['path'], changed=data != (ROOT / row['path']).read_bytes()))
    return m, routing


def inherited(c, seed):
    old = json.loads((HERE / 'frozen' / PREVDIR / 'certificate-v2.json').read_text())
    require(c['complete_predecessor_certificate'] == old, 'complete predecessor fibres/lifts changed')
    spec = importlib.util.spec_from_file_location('frozen_p_b13', HERE / 'frozen' / PREVDIR / 'check.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); module.HERE = HERE
    return module.validate(old, seed)


def connected(adjacency):
    todo, seen = [next(iter(adjacency))], set()
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v); todo.extend(adjacency[v] - seen)
    return len(seen) == len(adjacency)


def face_complex(es):
    """All triangles are facial under the original empty-C3 hypothesis."""
    faces = [t for t in combinations(sorted(V), 3) if all(edge(*p) in es for p in combinations(t, 2))]
    if len(es) != 19 or len(faces) != 10 or not BOUND <= es:
        return None
    incidence = Counter(edge(*p) for f in faces for p in combinations(f, 2))
    if any(incidence[e] != (1 if e in BOUND else 2) for e in es):
        return None
    for v in V:
        link = [edge(*(w for w in f if w != v)) for f in faces if v in f]
        degree = Counter(w for p in link for w in p)
        if not degree:
            return None
        if v in B:
            if sum(n == 1 for n in degree.values()) != 2 or any(n not in (1, 2) for n in degree.values()):
                return None
        elif any(n != 2 for n in degree.values()):
            return None
        adjacency = {w: set() for w in degree}
        for a, b in link:
            adjacency[a].add(b); adjacency[b].add(a)
        if not connected(adjacency):
            return None
    # Connected manifold, one prescribed C8 boundary, chi=10-19+10=1: a disk.
    return faces


def four_cycles(es):
    result = []
    for vs in combinations(sorted(V), 4):
        a = vs[0]
        for b, c, d in permutations(vs[1:]):
            if b > d:
                continue
            cyc = (a, b, c, d)
            if all(edge(x, y) in es for x, y in zip(cyc, cyc[1:] + cyc[:1])):
                result.append(cyc)
    return result


def small_caps(es, faces):
    face_set = {frozenset(f) for f in faces}
    if any(all(edge(*p) in es for p in combinations(vs, 2)) for vs in combinations(V, 4)):
        return False
    for a, b, c, d in four_cycles(es):
        diagonals = [edge(a, c) in es, edge(b, d) in es]
        if sum(diagonals) != 1:
            return False
        triangles = [(a, b, c), (a, c, d)] if diagonals[0] else [(b, c, d), (b, d, a)]
        if any(frozenset(t) not in face_set for t in triangles):
            return False
    return True


def local_components(es, colors, palette):
    vertices = {v for v in V if colors[v] in palette}; result = []
    while vertices:
        todo, part = [min(vertices)], set()
        while todo:
            v = todo.pop()
            if v not in part:
                part.add(v); todo.extend(w for w in vertices if edge(v, w) in es and w not in part)
        vertices -= part; result.append(sorted(part))
    return sorted(result)


def fibre(es, boundary_colors):
    good, bad = [], []
    for assignment in product(range(4), repeat=2):
        colors = dict(zip(B, boundary_colors)); colors.update(zip(['tau', 'zeta'], assignment))
        (good if all(colors[a] != colors[b] for a, b in es) else bad).append(list(assignment))
    return dict(boundary_word=boundary_colors, ordered_inner_vertices=['tau', 'zeta'], full_lifts=good,
                all_other_inner_assignments=bad)


def centers(es, faces):
    targets = [('K', 'B', 'C', 'Q'), ('K', 'B', 'E', 'Q'), ('K', 'N', 'C', 'Q'), ('K', 'N', 'E', 'Q')]
    selected, signature = [], []
    for ja, jb, ha, hb in targets:
        candidates = [e for e in es if {J[v] for v in e} == {ja, jb} and {H[v] for v in e} == {ha, hb}]
        require(len(candidates) == 1, 'joint center is not unique in this two-interior type')
        e = candidates[0]; incident = [f for f in faces if set(e) <= set(f)]
        require(len(incident) == 2, 'joint center missing actual face pair')
        thirds = [next(v for v in f if v not in e) for f in incident]
        require(len({PHI[v] for v in (*e, *thirds)}) == 4, 'tangent mistaken for true joint crossing')
        colors = {PHI[v] for v in e}; require(colors in ({0, 3}, {1, 2}), 'wrong original center colors')
        selected.append(list(e)); signature.append(int(colors == {1, 2}))
    return selected, signature


@lru_cache(maxsize=1)
def exhaustive_domain():
    """Fixed ten-point domain only; do not enumerate or infer arbitrary sources."""
    tree = {frozenset(p) for p in [('M', 'N'), ('N', 'K'), ('K', 'B')]}
    optional = []
    for a, b in combinations(V, 2):
        e = edge(a, b)
        if e in BOUND or PHI[a] == PHI[b]:
            continue
        if J[a] != J[b] and (PHI[a] % 2 == PHI[b] % 2 or frozenset((J[a], J[b])) not in tree):
            continue
        if PSI[a] in (1, 2) and PSI[b] in (1, 2) and H[a] != H[b]:
            continue
        optional.append(e)
    require(len(optional) == 15, 'fixed optional edge domain changed')
    accepted = set(); tested = 0
    for chosen in combinations(optional, 11):
        tested += 1; es = BOUND | set(chosen); fs = face_complex(es)
        if fs is None:
            continue
        degree = Counter(v for e in es for v in e)
        if min(degree['tau'], degree['zeta']) < 5 or not small_caps(es, fs):
            continue
        accepted.add(tuple(sorted(es)))
    require(tested == 1365 and len(accepted) == 11, 'fixed exhaustive domain totals changed')
    return frozenset(accepted)


def cases_check(rows, seed):
    domain = {(core, ix, id_) for core in ['L', 'R', 'O'] for ix, id_ in product(range(2), repeat=2)}
    require(len(rows) == 12 and {(r['core'], r['inside_ears']['xW'], r['inside_ears']['dW']) for r in rows} == domain, 'ordered twelve-candidate coverage incomplete')
    accepted, degree_tau, degree_zeta, sides, signatures = set(), Counter(), Counter(), Counter(), set()
    shuffled = list(rows); random.Random(seed).shuffle(shuffled)
    for row in shuffled:
        core = row['core']; ix = row['inside_ears']['xW']; id_ = row['inside_ears']['dW']
        require(row['id'] == f'{core}-x{ix}-d{id_}', 'ordered case identity changed')
        es = {tuple(e) for e in row['edges']}
        require(row['edges'] == [list(e) for e in sorted(es)] and all(a in V and b in V and a < b for a, b in es), 'edge set malformed')
        fs = face_complex(es); require(fs is not None, 'candidate not a ten-face disk')
        require(row['faces'] == [list(f) for f in sorted(fs)], 'actual facial triangles changed')
        require(all(PHI[a] != PHI[b] and PSI[a] != PSI[b] for a, b in es), 'same graph not proper in both named colorings')
        require((edge('x', 'W') in es) == bool(ix) and (edge('d', 'W') in es) == bool(id_), 'ear presence changed')
        require((edge('r', 'zeta') in es) == (core == 'L') and (edge('s', 'zeta') in es) == (core == 'R'), 'core chord changed')
        degree = Counter(v for e in es for v in e)
        for v in ['tau', 'zeta']:
            neighbors = sorted(b if a == v else a for a, b in es if v in (a, b))
            require(row['full_private_stars'][v] == neighbors and row['full_private_degrees'][v] == degree[v], 'full private original star changed')
        for label, colors in [('phi', PHI), ('psi', PSI)]:
            literal = fibre(es, [colors[v] for v in B])
            require(row[f'literal_{label}_boundary_fibre'] == literal, 'complete literal local fibre changed')
        rejected = core == 'O' and ix == id_ == 1
        if rejected:
            require(row['classification'] == 'excluded_private_degree4_and_C4' and degree['zeta'] == 4, 'rejected degree-four child promoted')
            cyc = ['x', 'W', 'd', 'tau']
            require(all(edge(a, b) in es for a, b in zip(cyc, cyc[1:] + cyc[:1])) and edge('x', 'd') not in es and edge('W', 'tau') not in es, 'rejected C4 obstruction lost')
            continue
        require(row['classification'] == 'local_necessary_type' and small_caps(es, fs), 'retained local type violates original small caps')
        require(len(fs) == 10 and len(four_cycles(es)) == 11, 'retained local cap coverage changed')
        require(local_components(es, PHI, {0, 2}) == sorted([['T'], ['d', 'x', 'zeta']]), 'original 02 components changed')
        require(local_components(es, PHI, {1, 3}) == sorted([['r', 's', 'tau'], ['W', 'e', 'h']]), 'original 13 components changed')
        require(local_components(es, PSI, {1, 2}) == sorted([['d', 'e', 'r'], ['h', 's', 'x']]), 'same-source C/E components merged')
        require(local_components(es, PSI, {0, 3}) == [['T', 'W', 'tau', 'zeta']], 'same-source Q not connected')
        actual_centers, signature = centers(es, fs)
        require(sorted(map(sorted, row['four_centers'])) == sorted(map(sorted, actual_centers)), 'four actual joint centers changed')
        require([sorted(e) for e in row['four_centers']] == actual_centers, 'joint centers independently permuted')
        require(row['four_center_D1_signature'] == signature == [1 - id_, 1 - ix, int(core == 'L'), int(core == 'R')], 'joint signature changed')
        require(degree['zeta'] == 4 + sum(signature) and min(degree['tau'], degree['zeta']) >= 5, 'complete-degree/signature relation changed')
        require(row['literal_phi_boundary_fibre']['full_lifts'] == [[3, 2]] and row['literal_psi_boundary_fibre']['full_lifts'] == [[3, 0]], 'literal full lifts not the named same-source pair')
        if degree['zeta'] == 5:
            original1 = [v for v in V if PHI[v] == 1 and edge(v, 'zeta') in es]
            require(len(original1) == 1, 'five-degree zeta has wrong unique original1 neighbor'); sides[H[original1[0]]] += 1
        accepted.add(tuple(sorted(es))); degree_tau[degree['tau']] += 1; degree_zeta[degree['zeta']] += 1; signatures.add(tuple(signature))
    require(accepted == exhaustive_domain(), 'canonical cells do not equal the complete fixed edge domain')
    expected_signatures = {s for s in product(range(2), repeat=4) if s[2:] != (1, 1) and any(s)}
    require(signatures == expected_signatures, 'eleven joint signatures incomplete')
    require(degree_tau == Counter({5: 8, 6: 3}) and degree_zeta == Counter({5: 4, 6: 5, 7: 2}) and sides == Counter(C=2, E=2), 'private degree or five-degree side totals changed')
    return dict(candidates=12, retained_local_types=11, excluded_core='O-x1-d1',
        exhaustive_fixed_edge_subsets=1365, optional_edges=15, C3_per_retained_type=10, C4_per_retained_type=11,
        private_tau_degree_counts=dict(sorted(degree_tau.items())), private_zeta_degree_counts=dict(sorted(degree_zeta.items())),
        zeta_degree5_unique_original1_sides=dict(sides), joint_signatures=11,
        literal_phi_and_psi_full_lifts_each=1)


def validate(c, seed=0):
    require(c['schema'] == '941-gamma8-cells-v1' and c['base'] == BASE, 'certificate scope/base changed')
    require(c['boundary'] == list(B) and c['original_colors'] == PHI and c['exchanged_colors'] == PSI, 'literal source frame changed')
    require(c['original_component_labels'] == J and c['exchanged_component_labels'] == H, 'same-source component labels changed')
    load = c['exterior_ear_load']
    require(load == dict(private_tip_minimum_degree=5, tip_boundary_neighbors=2,
        max_common_neighbors_of_nonedge=2, already_common_boundary_neighbors=1,
        T_private3_neighbor_not_adjacent_to_e_or_h=True,
        interior_lower_bounds_by_exterior_ears=[2, 4, 6], no_sharpness_claim=True), 'exterior-ear burden/source hypothesis changed')
    inner = load['private_tip_minimum_degree'] - load['tip_boundary_neighbors']
    require([2, inner + 1, 2 * inner - (load['max_common_neighbors_of_nonedge'] - load['already_common_boundary_neighbors']) + 1] == [2, 4, 6], 'ear load arithmetic failed')
    require(c['paper_contract'] == dict(scope='same original Gamma8; exactly two strict interior vertices for eleven types',
        two_interior_vertices_are_tau3_N_Q_and_zeta2_K_Q=True,
        exterior_ears_excluded_only_in_two_interior_branch=True,
        other_rootless_and_full_outer_stars_retained=True,
        four_joint_centers_each_once_only_for_two_interior_branch=True,
        global_alpha_beta_crossing_number_not_fixed=True,
        zeta_not_preidentified_with_Z=True, tau_not_preidentified_with_X=True,
        Wstar_may_equal_q=True, x_not_preidentified_with_xprime=True, h_not_preidentified_with_b=True,
        T_degree5_outer_link_color_words=[[1, 2, 3, 1], [1, 3, 2, 1]],
        zeta_degree5_C_and_E_sides_both_retained=True,
        named_local_fibres_are_not_original_complete_Sigma=True), 'paper/source scope changed')
    require(c['authority_boundaries'] == dict(finite_control='triggered and holds', source_control='not triggered',
        local_types_not_full_source_realizations=True, initial_pair_exclusions=0, new_Lean=False, smaller_bad=False,
        no_LP_or_general_source_enumeration=True, Gamma8_two_interior_source_exclusion=False,
        general_wrong_side_and_eight_pairs='OPEN', common_k_lower_bound_unchanged=23), 'unsupported source/theorem promotion')
    return dict(inherited=inherited(c, seed), fixed_cells=cases_check(c['candidates'], seed), exterior_ear_interior_bounds=[2, 4, 6])


def negatives(c):
    tests = [
        ('lose_ordered_case', lambda x: x['candidates'].pop()),
        ('promote_local_type_to_source', lambda x: x['authority_boundaries'].update(source_control='triggered and holds')),
        ('exclude_eight_pairs', lambda x: x['authority_boundaries'].update(initial_pair_exclusions=1)),
        ('claim_two_interior_source_excluded', lambda x: x['authority_boundaries'].update(Gamma8_two_interior_source_exclusion=True)),
        ('delete_general_exterior_ears', lambda x: x['paper_contract'].update(exterior_ears_excluded_only_in_two_interior_branch=False)),
        ('fix_global_crossings', lambda x: x['paper_contract'].update(global_alpha_beta_crossing_number_not_fixed=False)),
        ('identify_zeta_with_Z', lambda x: x['paper_contract'].update(zeta_not_preidentified_with_Z=False)),
        ('drop_q_exception', lambda x: x['paper_contract'].update(Wstar_may_equal_q=False)),
        ('drop_outer_stars', lambda x: x['paper_contract'].update(other_rootless_and_full_outer_stars_retained=False)),
        ('lose_T5_outer_link_side', lambda x: x['paper_contract']['T_degree5_outer_link_color_words'].pop()),
        ('allow_two_shared_inside_neighbors', lambda x: x['exterior_ear_load'].update(already_common_boundary_neighbors=0)),
        ('lower_double_exterior_bound', lambda x: x['exterior_ear_load'].update(interior_lower_bounds_by_exterior_ears=[2, 4, 5])),
        ('invent_sharpness', lambda x: x['exterior_ear_load'].update(no_sharpness_claim=False)),
        ('retain_degree_four_case', lambda x: next(r for r in x['candidates'] if r['id'] == 'O-x1-d1').update(classification='local_necessary_type')),
        ('erase_private_star_neighbor', lambda x: x['candidates'][0]['full_private_stars']['zeta'].pop()),
        ('change_joint_center_signature', lambda x: x['candidates'][0]['four_center_D1_signature'].__setitem__(0, 0)),
        ('delete_a_full_literal_lift', lambda x: x['candidates'][0]['literal_phi_boundary_fibre']['full_lifts'].pop()),
        ('delete_excluded_literal_assignment', lambda x: x['candidates'][0]['literal_psi_boundary_fibre']['all_other_inner_assignments'].pop()),
        ('merge_C_with_E', lambda x: x['exchanged_component_labels'].update(s='C')),
        ('erase_original_empty_fibres', lambda x: x['complete_predecessor_certificate']['complete_predecessor_certificate']['complete_predecessor_certificate']['upstream_complete_fibre_custody'].update(empty_seven_point_fibres=0)),
    ]
    result = []
    for name, mutate in tests:
        bad = deepcopy(c); mutate(bad)
        try:
            validate(bad)
        except (ValueError, KeyError, TypeError, IndexError):
            result.append(dict(name=name, status='rejected'))
        else:
            raise ValueError('corrupt certificate accepted: ' + name)
    return result


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--negative', action='store_true'); parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args(); manifest, routing = authority()
    c = json.loads(args.certificate.read_text()); stats = validate(c, args.seed)
    result = dict(status='PASS', seed=args.seed, frozen_authorities=len(manifest['inputs']),
        preserved_prior_outputs=len(manifest['preserved_prior_outputs']), immutable_input_drift=0,
        routing_live_drift=routing, source_control='not triggered', initial_pair_exclusions=0,
        general_ear_bounds_and_completeness='paper proof; fixed-domain checker is calibration', **stats)
    if args.negative:
        result['semantic_negatives'] = negatives(c)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, IndexError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT', reason=str(exc)))); sys.exit(1)
