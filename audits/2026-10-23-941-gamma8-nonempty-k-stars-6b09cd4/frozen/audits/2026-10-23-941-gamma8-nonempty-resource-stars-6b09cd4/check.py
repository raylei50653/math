#!/usr/bin/env python3
"""Exact local full-star audit; no source-completion claim.

Only same-source necessary stars of T and the unique complete M2 point are
enumerated.  The degree upper bounds deliberately allow a spare opaque point
where the original two stars do not consume all seven resource points.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREV = 'audits/2026-10-23-941-gamma8-chi-seven-6b09cd4/certificate.json'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def custody():
    data = json.loads((HERE / 'INPUTS.json').read_text())
    require(data['base'] == BASE, 'input BASE changed')
    require(len(data['immutable_inputs']) == 8 and len({r['path'] for r in data['immutable_inputs']}) == 8,
            'immutable authority domain changed')
    for row in data['immutable_inputs']:
        frozen = (HERE / row['snapshot']).read_bytes()
        require((len(frozen), sha256(frozen).hexdigest()) ==
                (row['bytes'], row['sha256']), 'frozen authority changed: ' + row['path'])
        require(frozen == (ROOT / row['path']).read_bytes(),
                'live authority changed: ' + row['path'])
    return len(data['immutable_inputs'])


def edge(a, b):
    return tuple(sorted((a, b)))


def stars(Tlink, mlink):
    edges = set()
    for center, link in [('T', Tlink), ('m', mlink)]:
        for i, a in enumerate(link):
            edges.add(edge(center, a))
            edges.add(edge(a, link[(i + 1) % len(link)]))
    return edges


def graph(edges, vertices):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def models():
    """Generate colors on actual ordered original T/m links, up to reflection.

    The r/s reflection is explicitly retained.  For T degree six the unique
    color-2 neighbor is either at an exterior endpoint or in the middle.  The
    two exterior face neighbors are then forced by the original coloring and
    C != E.  No independent palette or independent graph is selected.
    """
    rows = []
    for D, dm in [(5, 5), (5, 6), (6, 5)]:
        for a, b in [('r', 's'), ('s', 'r')]:
            variants = ['endpoint'] if D == 5 else ['endpoint', 'middle']
            for kind in variants:
                if D == 5:
                    Tlink = [a, 'tau', b, 'n', 'm']
                    mlink = [a, 'T', 'n'] + ['z' + str(i) for i in range(dm - 3)]
                    fixed = {'T': 0, 'm': 2, 'r': 1, 's': 1, 'tau': 3, 'n': 3}
                elif kind == 'endpoint':
                    Tlink = [a, 'tau', b, 'n', 'y', 'm']
                    mlink = [a, 'T', 'y', 'z0', 'z1']
                    fixed = {'T': 0, 'm': 2, 'r': 1, 's': 1, 'tau': 3, 'n': 3, 'y': 1}
                else:
                    Tlink = [a, 'tau', b, 'n', 'm', 'y']
                    mlink = ['T', 'y', 'z0', 'z1', 'n']
                    fixed = {'T': 0, 'm': 2, 'r': 1, 's': 1, 'tau': 3, 'n': 3, 'y': 3}
                unknown = [v for v in mlink if v.startswith('z')]
                for word in product((0, 1, 3), repeat=len(unknown)):
                    colors = dict(fixed, **dict(zip(unknown, word)))
                    edges = stars(Tlink, mlink)
                    if any(colors[x] == colors[y] for x, y in edges):
                        continue
                    # All resource vertices are the union of the two full
                    # original external stars, together with p_d,p_x.  tau is
                    # strictly inside and is forbidden as an exterior contact.
                    outside = sorted(set(colors) - {'T', 'r', 's', 'tau'})
                    spare = 7 - (len(outside) + 2)
                    require(spare in (0, 1), 'resource union mismatch')
                    adj = graph(edges, colors)
                    nonedges = set()
                    for x, y in combinations(colors, 2):
                        if colors[x] == colors[y]:
                            nonedges.add(edge(x, y))
                    # A complete original star forbids all nonconsecutive link
                    # chords and all additional contacts to its center.
                    for center, link in [('T', Tlink), ('m', mlink)]:
                        for x, y in combinations(link, 2):
                            if edge(x, y) not in edges:
                                nonedges.add(edge(x, y))
                        for x in colors:
                            if x != center and x not in link:
                                nonedges.add(edge(center, x))
                    zero_rows = []
                    for z in outside:
                        if colors[z] != 0:
                            continue
                        # z belongs to complete M02.  It cannot meet K2,
                        # other M0, B13, any frame, or the strict interior.
                        candidates = ['m'] + [v for v in colors if
                            v != 'tau' and colors[v] in (1, 3)]
                        allowed, rejected = [], []
                        for v in sorted(candidates):
                            trial = edges | {edge(z, v)}
                            tadj = graph(trial, colors)
                            reason = None
                            if edge(z, v) in nonedges:
                                reason = 'full-star-forbidden-edge'
                            elif {'r', 's'} <= tadj[z]:
                                reason = 'r-s-no-exterior-common-neighbor'
                            elif any(len(tadj[x] & tadj[y]) > 2 for x, y in nonedges):
                                reason = 'original-nonedge-common-neighbor-bound'
                            if reason:
                                rejected.append(dict(vertex=v, reason=reason))
                            else:
                                allowed.append(v)
                        zero_rows.append(dict(vertex=z, possible_neighbors=allowed,
                            excluded=rejected, opaque_spare_neighbors=spare,
                            full_degree_upper_bound=len(allowed) + spare))
                    rows.append(dict(id=f'{D}-{dm}-{a}-{kind}-' + ''.join(map(str, word)),
                        degree_T=D, degree_m=dm, position=kind, anchor=a,
                        T_full_link=Tlink, m_full_link=mlink, colors=colors,
                        original_edges=[list(e) for e in sorted(edges)],
                        resource_union=outside + ['p_d', 'p_x'],
                        opaque_spare_count=spare, extra_M0_stars=zero_rows,
                        status='excluded_by_M0_degree' if zero_rows else 'necessary_survivor'))
    return rows


def omega_rows():
    # These are exhaustive necessary component types, not source models.
    rows = []
    for color in range(4):
        rows.append(dict(color=color, location='R', relation='other_component',
            possible_complete_neighbors=(['r', 's', 'n', 'u', 'v'] if color in (0, 2) else []),
            full_degree_upper_bound=(4 if color in (0, 2) else 0),
            exclusion=('r-s-no-exterior-common-neighbor' if color in (0, 2)
                       else 'no-component-path-to-M-N-after-full-T-m-stars'),
            survives=False))
    for location, component, color in [('R', 'N13', 1), ('R', 'N13', 3),
                                        ('K', 'K02', 0), ('K', 'K02', 2)]:
        rows.append(dict(location=location, component=component, color=color,
            survives=True, source_realizability='not triggered'))
    return rows


def u_link_rows():
    rows = []
    for kind, color in [('N1', 1), ('N3', 3), ('K0', 0), ('K2', 2)]:
        colors = dict(n=3, m=2, v=3, p_d=2, p_x=2, U=0, omega=color)
        pool = ['p_d', 'p_x', 'U'] + ([] if color == 1 else ['omega'])
        links = []
        for length in range(2, len(pool) + 1):
            for tail in permutations(pool, length):
                link = ['n', 'm', 'v'] + list(tail)
                if all(colors[x] != colors[link[(i + 1) % len(link)]]
                       for i, x in enumerate(link)):
                    links.append(link)
        require(links, 'empty u-link ownership type')
        no_U = [link for link in links if 'U' not in link]
        rows.append(dict(omega_type=kind, all_proper_complete_u_links=links,
            links_without_U=no_U, forces_U_u_edge=not no_U,
            forces_m_C_and_d_not_U=not no_U,
            source_realizability='not triggered'))
    return rows


def N1_omega_stars():
    envelope = ['n', 'v', 'p_d', 'p_x', 'd', 'x', 'U']
    rows = []
    for size in range(5, 8):
        for values in combinations(envelope, size):
            neighbors = set(values)
            if any(pair <= neighbors for pair in [set(('n', 'v')),
                    set(('d', 'x')), set(('x', 'U'))]):
                continue
            require(size == 5 and {'p_d', 'p_x', 'd', 'U'} <= neighbors,
                    'N1 capacity did not force the five-star')
            w = next(iter(neighbors & {'n', 'v'}))
            colors = dict(d=0, p_d=2, U=0, p_x=2, **{w: 3})
            cycles = []
            for tail in permutations(['U', 'p_x', w]):
                cycle = ['d', 'p_d'] + list(tail)
                if all(colors[x] != colors[cycle[(i + 1) % len(cycle)]] and
                       edge(x, cycle[(i + 1) % len(cycle)]) != edge('d', 'p_x')
                       for i, x in enumerate(cycle)):
                    cycles.append(cycle)
            require(cycles == [['d', 'p_d', 'U', 'p_x', w]], 'N1 omega full rotation not unique')
            rows.append(dict(N3_neighbor=w, full_neighbors=sorted(neighbors),
                degree=5, full_link=cycles[0],
                omega_side='C', source_realizability='not triggered'))
    return rows


def expected():
    rows = models()
    survivors = [r for r in rows if r['status'] == 'necessary_survivor']
    require(len(survivors) == 2, 'unexpected local full-star survivors')
    require(all((r['degree_T'], r['degree_m']) == (5, 5) for r in survivors),
            'degree-six pair survived')
    require(all(z['full_degree_upper_bound'] <= 4
                for r in rows for z in r['extra_M0_stars']), 'extra M0 survived degree five')
    prior = json.loads((HERE / 'frozen' / PREV).read_text())
    return dict(schema='941-gamma8-nonempty-resource-stars-v1', base=BASE,
        paper_domain=dict(j=2, resource_count=7, M2_nonempty=True,
            same_original_G_F=True, rotation=True, literal_frame=True,
            full_original_stars=True, rooted_ownership=True),
        complete_original_star_trials=rows, omega_component_trials=omega_rows(),
        u_full_link_trials=u_link_rows(), N1_omega_full_stars=N1_omega_stars(),
        conclusion=dict(M2=['m'], M=['T', 'm'], degree_T=5, degree_m=5,
            m_link=['a1', 'T0', 'n3', 'u1', 'v3'],
            Z=['m', 'n', 'u', 'v', 'p_d', 'p_x', 'omega'],
            omega_types=['N1', 'N3', 'K0', 'K2'], m_side=['C', 'E'],
            whole_U_star_not_claimed=True, previous_60_rows_not_inherited=True),
        preserved_complete_predecessor_certificate=prior,
        authority_boundaries=dict(finite_control='triggered and holds',
            source_realizability='not triggered', eleven_type_exclusions=0,
            general_wrong_side='OPEN', common_k_lower_bound=23,
            actual_source_replacement=False, new_Lean=False, new_LP=False))


def validate(cert, seed):
    ref = expected()
    keys = list(ref)
    random.Random(seed).shuffle(keys)
    require(set(cert) == set(ref), 'certificate key domain changed')
    for key in keys:
        require(cert[key] == ref[key], 'certificate mismatch: ' + key)
    rows = ref['complete_original_star_trials']
    return dict(status='PASS', immutable_inputs=custody(), immutable_drift=0,
        full_T_m_star_trials=len(rows), necessary_survivors=2,
        extra_M0_star_trials=sum(len(r['extra_M0_stars']) for r in rows),
        maximum_extra_M0_degree=max(z['full_degree_upper_bound']
            for r in rows for z in r['extra_M0_stars']),
        omega_component_trials=len(ref['omega_component_trials']),
        u_full_link_trials=sum(len(r['all_proper_complete_u_links']) for r in ref['u_full_link_trials']),
        N1_omega_full_stars=len(ref['N1_omega_full_stars']),
        complete_predecessor_preserved=True, common_k_lower_bound=23,
        source_realizability='not triggered', eleven_type_exclusions=0)


def negatives(cert):
    attacks = [
        ('drop-full-star', lambda c: c['complete_original_star_trials'].pop()),
        ('change-complete-m-link', lambda c: c['complete_original_star_trials'][0]['m_full_link'].pop()),
        ('lose-spare-point', lambda c: c['complete_original_star_trials'][0].update(opaque_spare_count=0)),
        ('promote-degree-six', lambda c: c['conclusion'].update(degree_T=6)),
        ('drop-omega-type', lambda c: c['conclusion']['omega_types'].pop()),
        ('force-C-side', lambda c: c['conclusion'].update(m_side=['C'])),
        ('admit-new-rootless-02', lambda c: c['omega_component_trials'][0].update(survives=True)),
        ('inherit-old-60', lambda c: c['conclusion'].update(previous_60_rows_not_inherited=False)),
        ('omit-full-u-link', lambda c: c['u_full_link_trials'][0]['all_proper_complete_u_links'].pop()),
        ('lose-N1-forced-neighbor', lambda c: c['N1_omega_full_stars'][0]['full_neighbors'].pop()),
        ('claim-source', lambda c: c['authority_boundaries'].update(source_realizability='triggered and holds')),
        ('alter-full-lift', lambda c: next(r for cap in c['preserved_complete_predecessor_certificate']['caps'] for r in cap['relations'] if r['full_lifts'])['full_lifts'].pop()),
    ]
    rejected = []
    for name, mutate in attacks:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            validate(bad, 0)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('negative control accepted: ' + name)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--negative', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    cert = json.loads(args.certificate.read_text())
    result = validate(cert, args.seed)
    if args.negative:
        result['negative_controls_rejected'] = negatives(cert)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
