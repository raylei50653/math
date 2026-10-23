#!/usr/bin/env python3
"""Read-only independent set-partition/union-find fixed-prefix calibration."""
import argparse
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREV = 'audits/2026-10-23-941-gamma8-exterior-6b09cd4/certificate-v2.json'
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
ATTACH = {'u': {'d', 'r'}, 'a': {'r', 'T'}, 'b': {'T', 's'}, 'c': {'s', 'x'}}


def require(ok, why):
    if not ok:
        raise ValueError(why)


def edge(a, b):
    return tuple(sorted((a, b)))


def custody():
    m = json.loads((HERE / 'INPUTS.json').read_text())
    require(m['base'] == BASE, 'BASE drift')
    for r in m['inputs']:
        data = (HERE / r['snapshot']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (r['bytes'], r['sha256']), 'snapshot drift')
        require(data == (ROOT / r['path']).read_bytes(), 'live authority drift: ' + r['path'])
    for r in m['preserved_prior_outputs']:
        data = (ROOT / r['path']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (r['bytes'], r['sha256']), 'prior drift: ' + r['path'])
    for r in m['routing_entry']:
        data = (HERE / r['snapshot']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (r['bytes'], r['sha256']), 'routing snapshot drift')
    return dict(inputs=len(m['inputs']), prior_outputs=len(m['preserved_prior_outputs']), immutable_drift=0)


def partitions(seq):
    if not seq:
        yield []
        return
    first, *rest = seq
    for p in partitions(rest):
        yield sorted([[first]] + p)
        for i in range(len(p)):
            yield sorted(p[:i] + [sorted([first] + p[i])] + p[i + 1:])


def components(edges, colors, pair):
    parent = {v: v for v in colors if colors[v] in pair}
    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for a, b in edges:
        if a in parent and b in parent:
            parent[find(a)] = find(b)
    result = {}
    for v in parent:
        result.setdefault(find(v), []).append(v)
    return sorted(sorted(g) for g in result.values())


@lru_cache(maxsize=1)
def reconstruct():
    prior = json.loads((HERE / 'frozen' / PREV).read_text())
    old = prior['complete_predecessor_certificate']
    rows = []
    tested = 0
    for cell in old['candidates']:
        if cell['classification'] != 'local_necessary_type':
            continue
        es0 = {tuple(e) for e in cell['edges']}
        adj = {v: set() for v in old['original_colors']}
        for a, b in es0:
            adj[a].add(b); adj[b].add(a)
        blocked = {frozenset((a, b)) for a, b in combinations(old['boundary'], 2)
                   if edge(a, b) not in es0 and adj[a] & adj[b] & {'tau', 'zeta'}}
        for m_first, uc, cc in product([True, False], [2, 3], [2, 3]):
            kinds = dict(u='K2' if uc == 2 else 'N3', a='M2' if m_first else 'N3',
                         b='N3' if m_first else 'M2', c='K2' if cc == 2 else 'N3')
            for groups in partitions(list('uabc')):
                tested += 1
                if any(len({kinds[r] for r in g}) != 1 for g in groups):
                    continue
                if any(any(frozenset(p) in blocked for p in combinations(set().union(*(ATTACH[r] for r in g)), 2))
                       for g in groups):
                    continue
                names = {r: 'out_' + min(g) for g in groups for r in g}
                # Full r/s links would have degree four if these exterior faces coincide.
                if names['u'] == names['a'] and len(adj['r']) == 3:
                    continue
                if names['b'] == names['c'] and len(adj['s']) == 3:
                    continue
                edges = es0 | {edge(names[r], v) for r in ATTACH for v in ATTACH[r]}
                edges.add(edge(names['a'], names['b']))
                colors = dict(old['original_colors']); labels = dict(old['original_component_labels'])
                for r in kinds:
                    colors[names[r]] = int(kinds[r][1]); labels[names[r]] = kinds[r][0]
                require(all(a != b and colors[a] != colors[b] for a, b in edges), 'improper prefix')
                Tstar = {b if a == 'T' else a for a, b in edges if 'T' in (a, b)}
                require(len(Tstar) == 5, 'T full star degree drift')
                side = 'C' if m_first else 'E'
                orbit = []
                for bits in product(range(2), repeat=3):
                    co = {v: col ^ (2 if labels[v] in 'MNK' and bits['MNK'.index(labels[v])] else 0)
                          for v, col in colors.items()}
                    require(all(co[a] != co[b] for a, b in edges), 'improper whole-component restriction')
                    orbit.append(dict(action=list(bits), colors=co,
                        components={''.join(map(str, pair)): components(edges, co, pair)
                                    for pair in combinations(range(4), 2)}))
                psi = orbit[1]['colors']  # bits (0,0,1): the same whole K.
                comp12 = components(edges, psi, {1, 2})
                C = next(set(g) for g in comp12 if 'r' in g)
                E = next(set(g) for g in comp12 if 's' in g)
                require(not C & E, 'C/E merged in prefix')
                m = names['a' if m_first else 'b']
                require(m in (C if side == 'C' else E), 'T M2 side differs')
                # The proof selects an extra link vertex only when the four faces
                # supply fewer than the protected bound; its existence is paper authority.
                bound = 5 if cell['core'] == 'O' else 4
                face_count = len(groups)
                if face_count == bound:
                    rule = 'four_distinct_faces'
                elif cc == 3:
                    rule = 'x_continuation'
                elif not m_first:
                    rule = 's_gap'
                elif uc == 3:
                    rule = 'd_continuation'
                else:
                    rule = 'r_gap'
                require(face_count + int(rule != 'four_distinct_faces') == bound, 'protected count differs')
                rows.append(dict(id=cell['id'], core=cell['core'], T_M2_side=side, kinds=kinds,
                    partition=groups, edges=sorted(map(list, edges)), complete_prefix_orbit=orbit,
                    protected_private_bound=bound, avoided_M2_side='E' if side == 'C' else 'C',
                    witness_rule=rule))
    return prior, rows, tested


def rowkey(r):
    return (r['id'], r['T_M2_side'], tuple(sorted(r['kinds'].items())),
            tuple(tuple(g) for g in r['partition']))


def validate(c, seed=0):
    prior, rows, tested = reconstruct()
    require(c['schema'] == '941-gamma8-m2-stars-v1' and c['base'] == BASE, 'schema/BASE drift')
    require(c['complete_predecessor_certificate'] == prior, 'predecessor complete fibres or lifts changed')
    expected = {rowkey(r): r for r in rows}
    require(len(c['prefix_rows']) == len(expected) == 104, 'prefix domain incomplete')
    shuffled = list(c['prefix_rows']); random.Random(seed).shuffle(shuffled)
    seen = set()
    for r in shuffled:
        key = rowkey(r)
        require(key not in seen and key in expected and r == expected[key], 'prefix/orbit/witness changed')
        seen.add(key)
    require(c['paper_contract'] == dict(j=2, T_original_degree=5, same_original_exterior=True,
        full_M2_set_retained=True, E_may_be_rootless=True, protected_LR_bound=4, protected_O_bound=5,
        h_c_and_T_M2_in_E_exterior_bounds=[5, 6],
        stable_C_contact_and_rooted_E_and_T_M2_in_C_exterior_bounds=[5, 6],
        extra_separator_vertex_distinct_from_protected_set=True,
        prefix_rows_are_not_complete_stars_or_disk_completions=True), 'paper premises or bounds changed')
    require(c['authority_boundaries'] == dict(finite_control='triggered and holds',
        original_source_control='not triggered', general_wrong_side='OPEN', eleven_type_exclusions=0,
        initial_pair_exclusions=0, common_k_lower_bound=23, smaller_bad=False, new_Lean=False, new_LP=False),
        'unsupported source/theorem promotion')
    return dict(fixed_role_partition_trials=tested, necessary_prefix_rows=len(rows),
        local_orbit_states=8 * len(rows), complete_local_palette_restrictions=48 * len(rows),
        type_orientation_pairs=len({(r['id'], r['T_M2_side']) for r in rows}),
        original_source_control='not triggered', eleven_type_exclusions=0)


def negatives(c):
    mutations = [
        ('missing_prefix', lambda x: x['prefix_rows'].pop()),
        ('duplicate_prefix', lambda x: x['prefix_rows'].__setitem__(0, deepcopy(x['prefix_rows'][1]))),
        ('change_T_side', lambda x: x['prefix_rows'][0].update(T_M2_side='E')),
        ('drop_orbit_state', lambda x: x['prefix_rows'][0]['complete_prefix_orbit'].pop()),
        ('drop_rootless_component', lambda x: x['prefix_rows'][0]['complete_prefix_orbit'][0]['components']['02'].pop()),
        ('alter_literal_color', lambda x: x['prefix_rows'][0]['complete_prefix_orbit'][0]['colors'].update(T=2)),
        ('alter_witness', lambda x: x['prefix_rows'][0].update(witness_rule='r_gap')),
        ('drop_full_M2', lambda x: x['paper_contract'].update(full_M2_set_retained=False)),
        ('presume_E_rooted', lambda x: x['paper_contract'].update(E_may_be_rootless=False)),
        ('drop_T_degree_premise', lambda x: x['paper_contract'].update(T_original_degree=6)),
        ('raise_O_protected_bound', lambda x: x['paper_contract'].update(protected_O_bound=6)),
        ('lose_extra_vertex_disjointness', lambda x: x['paper_contract'].update(extra_separator_vertex_distinct_from_protected_set=False)),
        ('lose_prior_empty_fibre', lambda x: x['complete_predecessor_certificate']['complete_predecessor_certificate']['candidates'][0]['literal_phi_boundary_fibre']['all_other_inner_assignments'].pop()),
        ('promote_source', lambda x: x['authority_boundaries'].update(original_source_control='triggered and holds')),
        ('raise_global_k', lambda x: x['authority_boundaries'].update(common_k_lower_bound=24)),
        ('exclude_local_type', lambda x: x['authority_boundaries'].update(eleven_type_exclusions=1)),
    ]
    result = []
    for name, mutate in mutations:
        bad = deepcopy(c)
        mutate(bad)
        try:
            validate(bad)
        except (ValueError, KeyError, TypeError, IndexError):
            result.append(dict(name=name, status='rejected'))
        else:
            raise ValueError('accepted negative: ' + name)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--negative', action='store_true')
    a = p.parse_args()
    authority = custody()
    c = json.loads(a.certificate.read_text())
    result = dict(status='PASS', seed=a.seed, custody=authority, **validate(c, a.seed))
    if a.negative:
        result['semantic_negatives'] = negatives(c)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, IndexError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT', reason=str(exc))))
        sys.exit(1)
