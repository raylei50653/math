#!/usr/bin/env python3
"""Read-only calibration of source-forced complete links, not source completions."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREV = 'audits/2026-10-23-941-gamma8-rootless-stars-6b09cd4'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def custody():
    data = json.loads((HERE / 'INPUTS.json').read_text())
    require(data['schema'] == '941-gamma8-six-equality-inputs-v1' and data['base'] == BASE,
            'input schema/BASE drift')
    for row in data['inputs'] + data['routing_entry']:
        raw = (HERE / row['snapshot']).read_bytes()
        require((len(raw), sha256(raw).hexdigest()) == (row['bytes'], row['sha256']),
                'snapshot drift: ' + row['path'])
    for row in data['inputs'] + data['preserved_prior_outputs']:
        raw = (ROOT / row['path']).read_bytes()
        require((len(raw), sha256(raw).hexdigest()) == (row['bytes'], row['sha256']),
                'immutable live drift: ' + row['path'])
    require((len(data['inputs']), len(data['preserved_prior_outputs']),
             len(data['routing_entry'])) == (8, 490, 4), 'custody coverage drift')
    return dict(inputs=8, prior_outputs=490, routing_snapshots=4, immutable_drift=0)


def predecessor():
    return json.loads((HERE / 'frozen' / PREV / 'certificate-v2.json').read_text())


def cells(prior):
    c = prior
    for _ in range(3):
        c = c['complete_predecessor_certificate']
    return c, [row for row in c['candidates'] if row['classification'] == 'local_necessary_type']


def graph(contract, cell, extra_colors, extra_labels, extra_edges, alias_U=False):
    colors = dict(contract['original_colors'], **extra_colors)
    labels = dict(contract['original_component_labels'], **extra_labels)
    if not alias_U:
        colors['U'] = 0
        labels['U'] = 'K'
    adj = {v: set() for v in colors}
    for a, b in cell['edges'] + extra_edges:
        require(a in adj and b in adj and a != b, 'bad restricted edge')
        require(colors[a] != colors[b], 'improper original edge')
        adj[a].add(b)
        adj[b].add(a)
    return colors, labels, adj, 'd' if alias_U else 'U'


def possible(a, b, colors, labels, adj, psi_sides, full_m_link=None):
    if a == b or colors[a] == colors[b]:
        return False
    if {labels[a], labels[b]} == {'M', 'B'}:
        return False  # the entire J-K branch containing M is rootless
    if {colors[a], colors[b]} <= {0, 2} and labels[a] != labels[b]:
        return False
    if {colors[a], colors[b]} <= {1, 3} and labels[a] != labels[b]:
        return False
    psi = {v: 2 - c if labels[v] == 'K' and c in (0, 2) else c for v, c in colors.items()}
    if {psi[a], psi[b]} == {1, 2} and a in psi_sides and b in psi_sides:
        if psi_sides[a] != psi_sides[b]:
            return False
    # Every triangle through the complete degree-five m is facial.
    if full_m_link and a in full_m_link and b in full_m_link:
        i, j = full_m_link.index(a), full_m_link.index(b)
        if (i - j) % len(full_m_link) not in (1, len(full_m_link) - 1):
            return False
    trial = {v: set(n) for v, n in adj.items()}
    trial[a].add(b)
    trial[b].add(a)
    # Same-colored vertices are certified original nonedges.  Three common
    # neighbors contradict the inherited C3/C4 source lemma.
    for v, w in combinations(trial, 2):
        if colors[v] == colors[w] and len(trial[v] & trial[w]) > 2:
            return False
    return True


def complete_links(center, left, right, fixed_middle, allowed, colors):
    """Enumerate all cyclic links with the already facial left-middle-right arc."""
    extras = sorted(set(allowed) - {left, right, fixed_middle})
    result = []
    for size in range(2, len(extras) + 1):  # original degree at least five
        for chosen in combinations(extras, size):
            for order in permutations(chosen):
                cycle = [left, fixed_middle, right, *order]
                if all(colors[a] != colors[b] for a, b in zip(cycle, cycle[1:] + cycle[:1])):
                    result.append(cycle)
    return sorted(result)


def reconstruct(prior):
    contract, actual = cells(prior)
    require(len(actual) == 11, 'eleven-cell domain changed')
    gamma = set(contract['boundary'])
    sides = dict(r='C', d='C', e='C', s='E', x='E', h='E')
    equality, aliases, empty = [], [], []
    for cell in actual:
        for side, endpoint, other in [('C', 'r', 's'), ('E', 's', 'r')]:
            for uc, vc in [(0, 3), (1, 0), (1, 3)]:
                extra_colors = dict(m=2, n=3, u=uc, v=vc, p_d=2, p_x=2)
                extra_labels = dict(m='M', n='N', u='M' if uc == 0 else 'N',
                                    v='M' if vc == 0 else 'N', p_d='K', p_x='K')
                edges = [('T', 'm'), ('T', 'n'), ('m', endpoint), ('m', 'n'),
                         ('m', 'u'), ('m', 'v'), ('n', 'u'), ('u', 'v'),
                         ('v', endpoint), ('n', other), ('d', 'p_d'), ('x', 'p_x')]
                colors, labels, adj, U = graph(contract, cell, extra_colors, extra_labels, edges)
                ps = dict(sides, m=side, U='C')
                if uc == 1:
                    ps['u'] = side
                if vc == 0:
                    ps['u'] = side  # u1 is adjacent to m2
                mlink = [endpoint, 'T', 'n', 'u', 'v']
                target = 'u' if uc == 0 or vc == 3 else 'v'
                pool = gamma | set(extra_colors) | {U}
                allowed = sorted(w for w in pool
                                 if possible(target, w, colors, labels, adj, ps, mlink))
                links = complete_links('u', 'n', 'v', 'm', allowed, colors) if uc == 1 and vc == 3 else []
                # The full source-star envelope is proved in PROOF.md.  Its
                # finite consequences here are derived from actual edges.
                equality.append(dict(cell=cell['id'], core=cell['core'], side=side,
                    u_color=uc, v_color=vc, tested_vertex=target,
                    allowed_neighbors=allowed, complete_u_links=links))
                if uc == 1 and vc == 3:
                    colors, labels, adj, U = graph(contract, cell, extra_colors, extra_labels, edges, True)
                    ps = dict(sides, m=side, u=side)
                    allowed = sorted(w for w in gamma | set(extra_colors)
                                     if possible('u', w, colors, labels, adj, ps, mlink))
                    aliases.append(dict(cell=cell['id'], side=side, U_equals_d=True,
                        allowed_neighbors=allowed,
                        complete_u_links=complete_links('u', 'n', 'v', 'm', allowed, colors)))
        # M={T}, D(T)=6 and |X|=5: the actual complete T-link is fixed.
        for alias in (False, True):
            colors, labels, adj, U = graph(contract, cell,
                dict(a=3, y=1, b=3, p_d=2, p_x=2),
                dict(a='N', y='N', b='N', p_d='K', p_x='K'),
                [('T', 'a'), ('T', 'y'), ('T', 'b'), ('r', 'a'),
                 ('a', 'y'), ('y', 'b'), ('b', 's'), ('d', 'p_d'), ('x', 'p_x')], alias)
            pool = gamma | {'a', 'y', 'b', 'p_d', 'p_x', U}
            ps = dict(sides)
            if not alias:
                ps['U'] = 'C'
            allowed = sorted(w for w in pool if possible('y', w, colors, labels, adj, ps))
            links = complete_links('y', 'a', 'b', 'T', allowed, colors)
            empty.append(dict(cell=cell['id'], core=cell['core'], U_equals_d=alias,
                              allowed_neighbors=allowed, complete_y_links=links,
                              O_already_excluded=cell['core'] == 'O'))
    return equality, aliases, empty


def validate(certificate, seed=0):
    prior = predecessor()
    require(certificate['schema'] == '941-gamma8-six-equality-v1' and certificate['base'] == BASE,
            'certificate schema/BASE drift')
    require(certificate['complete_predecessor_certificate'] == prior,
            'predecessor complete fibres/empty rows/full lifts changed')
    expected = reconstruct(prior)
    for key, rows in zip(('six_point_cases', 'd_U_alias_cases', 'empty_M2_five_point_cases'), expected):
        require(isinstance(certificate[key], list) and len(certificate[key]) == len(rows),
                key + ' incomplete')
        order = list(range(len(rows)))
        random.Random(seed).shuffle(order)
        for i in order:
            require(certificate[key][i] == rows[i], key + ' drift at ' + str(i))
    require(certificate['paper_contract'] == dict(j=2, same_original_graph_and_frame=True,
        all_source_stars_complete=True, rootless_neighbors_have_only_U_frame_exception=True,
        C_not_equal_E=True, E_may_be_rootless=True, full_M2_retained=True,
        six_point_M2_singleton=True, six_point_M_equals_T_m=True,
        six_point_side='C', six_point_d_not_U=True, six_point_u_degree_options=[5, 6],
        empty_M2_five_points_requires_U_y=True, empty_M2_five_points_d_not_U=True,
        minimum_when_M2_empty_T6_d_U=6), 'paper contract drift')
    require(certificate['authority_boundaries'] == dict(
        finite_control='triggered and holds', source_realizability='not triggered',
        excluded_conditional_branches=['six_points_m_in_E', 'six_points_d_U',
                                       'empty_M2_T6_five_points_d_U'],
        six_point_C_completion='OPEN', empty_M2_L_R_completion='OPEN',
        eleven_type_exclusions=0, general_wrong_side='OPEN', common_k_lower_bound=23,
        new_Lean=False, new_LP=False, smaller_bad=False), 'unsupported promotion')
    equality, aliases, empty = expected
    require(sum(bool(r['complete_u_links']) for r in equality) == 11, 'equality survivor coverage')
    require(sum(len(r['complete_u_links']) for r in equality) == 66, 'six link domain')
    require(all(not r['complete_u_links'] for r in aliases), 'd=U branch survived')
    require(all(not r['complete_y_links'] for r in empty if r['U_equals_d']), 'empty alias survived')
    return dict(six_point_color_cases=len(equality), d_U_alias_cases=len(aliases),
        surviving_cell_side_cases=11, complete_u_link_restrictions=66,
        empty_M2_cases=len(empty), empty_L_R_link_restrictions=sum(
            len(r['complete_y_links']) for r in empty if not r['O_already_excluded']),
        source_realizability='not triggered', eleven_type_exclusions=0)


def negatives(certificate):
    mutations = [
        ('missing_color_case', lambda c: c['six_point_cases'].pop()),
        ('missing_alias_case', lambda c: c['d_U_alias_cases'].pop()),
        ('missing_empty_case', lambda c: c['empty_M2_five_point_cases'].pop()),
        ('wrong_m_side', lambda c: c['six_point_cases'][0].update(side='E')),
        ('allow_K_neighbor_for_M0', lambda c: c['six_point_cases'][0]['allowed_neighbors'].append('p_d')),
        ('drop_U_exception', lambda c: c['six_point_cases'][2]['allowed_neighbors'].remove('U')),
        ('lose_complete_link', lambda c: c['six_point_cases'][2]['complete_u_links'].pop()),
        ('allow_same_color_link_edge', lambda c: c['six_point_cases'][2]['complete_u_links'][0].__setitem__(3, 'p_x')),
        ('drop_E_case_rejection', lambda c: c['six_point_cases'][5]['complete_u_links'].append(['n','m','v','U','p_d'])),
        ('allow_d_U', lambda c: c['d_U_alias_cases'][0]['complete_u_links'].append(['n','m','v','d','p_d'])),
        ('allow_empty_d_U', lambda c: c['empty_M2_five_point_cases'][1]['complete_y_links'].append(['a','T','b','d','p_d'])),
        ('presume_E_rooted', lambda c: c['paper_contract'].update(E_may_be_rootless=False)),
        ('drop_complete_M2', lambda c: c['paper_contract'].update(full_M2_retained=False)),
        ('invent_seven_point_bound', lambda c: c['paper_contract'].update(minimum_when_M2_empty_T6_d_U=7)),
        ('close_C_completion', lambda c: c['authority_boundaries'].update(six_point_C_completion='CLOSED')),
        ('exclude_eleven_type', lambda c: c['authority_boundaries'].update(eleven_type_exclusions=1)),
        ('promote_source', lambda c: c['authority_boundaries'].update(source_realizability='triggered and holds')),
        ('raise_k', lambda c: c['authority_boundaries'].update(common_k_lower_bound=24)),
        ('lose_predecessor_fibre', lambda c: c['complete_predecessor_certificate']
            ['complete_predecessor_certificate']['complete_predecessor_certificate']
            ['complete_predecessor_certificate']['candidates'][0]
            ['literal_phi_boundary_fibre']['all_other_inner_assignments'].pop()),
    ]
    result = []
    for name, mutate in mutations:
        bad = deepcopy(certificate)
        mutate(bad)
        try:
            validate(bad)
        except (ValueError, KeyError, IndexError, TypeError):
            result.append(dict(name=name, status='rejected'))
        else:
            raise ValueError('accepted negative: ' + name)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
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
    except (ValueError, KeyError, TypeError, IndexError, OSError) as exc:
        print(json.dumps(dict(status='REJECT', reason=str(exc))))
        sys.exit(1)
