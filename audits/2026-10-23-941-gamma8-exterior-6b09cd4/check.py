#!/usr/bin/env python3
"""Read-only independent union-find replay of the literal Gamma8/B14 endpoint domain."""
import argparse
from copy import deepcopy
from functools import lru_cache
import gzip
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVDIR = 'audits/2026-10-23-941-gamma8-cells-6b09cd4'
ROUND3 = 'audits/2026-10-23-three-mask-round3-cb8f859/941/certificate.json'
SIX = 'audits/2026-10-21-w7-L-path-30dde27/six_degree/certificate-v2.json.gz'
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
BOUND = ['a', 'z1', 'z2', 'z3', 'z4', 'V', 'U', 'HL_0', 'q', 'c', 's', 'v', 'w', 't']


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def edge(a, b):
    return tuple(sorted((a, b)))


def authority():
    m = json.loads((HERE / 'INPUTS.json').read_text())
    require(m['base'] == BASE, 'BASE drift')
    for r in m['inputs']:
        data = (HERE / r['snapshot']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (r['bytes'], r['sha256']), 'frozen input drift')
        require(data == (ROOT / r['path']).read_bytes(), 'live input drift: ' + r['path'])
    for r in m['preserved_prior_outputs']:
        data = (ROOT / r['path']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (r['bytes'], r['sha256']), 'predecessor drift')
    routing = []
    for r in m['routing_entry']:
        data = (HERE / r['snapshot']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (r['bytes'], r['sha256']), 'routing snapshot drift')
        routing.append(dict(path=r['path'], changed=data != (ROOT / r['path']).read_bytes()))
    return dict(frozen_inputs=len(m['inputs']), preserved_prior_outputs=len(m['preserved_prior_outputs']),
                immutable_drift=0, routing_live_drift=routing)


@lru_cache(maxsize=1)
def fixed():
    p = json.loads((HERE / 'frozen' / PREVDIR / 'certificate.json').read_text())
    rows = json.loads((HERE / 'frozen' / ROUND3).read_text())['source_rows']
    with gzip.open(HERE / 'frozen' / SIX, 'rt') as f:
        six = json.load(f)
    gates = {}
    for row in six['ordinary_C14_cases']:
        if row['split_containing_0'] == [0, 3]:
            gates[row['target']] = [r['complete_F_boundary_contacts'] for r in row['complete_specific_F_types']
                                   if r['same_initial_E_residual_gate'] and not r['forbidden_action_masks']]
            require(len(gates[row['target']]) == 2, 'original full 03 gate changed')
    require(len(rows) == 4, 'four original target/02 contracts missing')
    return p, rows, gates


def components(es, colors, palette):
    """Union-find, independent of the producer's graph walk."""
    parent = {v: v for v, c in colors.items() if c in palette}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]; v = parent[v]
        return v

    for a, b in sorted(es):
        if a in parent and b in parent:
            parent[find(a)] = find(b)
    groups = {}
    for v in parent:
        groups.setdefault(find(v), []).append(v)
    return sorted(sorted(s) for s in groups.values())


def partial_refines(es, colors, palette, gates):
    observed = [set(s) & set(BOUND) for pair in [set(palette), set(range(4)) - set(palette)]
                for s in components(es, colors, pair)]
    return any(all(any(s <= set(block) for block in gate) for s in observed if s) for gate in gates)


def colors_at(m, n, k):
    previous, _, _ = fixed()
    chosen = {label for label, active in [('M', m), ('N', n), ('K', k)] if active}
    return {v: color ^ (2 if previous['original_component_labels'][v] in chosen else 0)
            for v, color in previous['original_colors'].items()}


def join(cell, contract, att, m, n, k):
    previous, _, _ = fixed()
    names = {v: 'g_' + v for v in previous['original_colors']}
    names.update({v: contact for v, contact in zip(['d', 'e', 'h', 'W'], att) if contact is not None})
    colors = dict(contract['whole_K_successor_boundary_colors'] if k else contract['original_boundary_colors'])
    for v, color in colors_at(m, n, k).items():
        require(names[v] not in colors or colors[names[v]] == color, 'literal identity/color conflict')
        colors[names[v]] = color
    es = {edge(names[a], names[b]) for a, b in cell['edges']}
    es |= {edge(a, b) for a, b in zip(BOUND, BOUND[1:] + BOUND[:1])}
    require(all(a != b and colors[a] != colors[b] for a, b in es), 'improper joined orbit')
    return es, colors


@lru_cache(maxsize=1)
def finite_domain():
    previous, contracts, gates03 = fixed()
    cells = [r for r in previous['candidates'] if r['classification'] == 'local_necessary_type']
    orbits, barriers, attachments = [], [], []
    for cell in cells:
        es = {tuple(e) for e in cell['edges']}
        states = []
        for m, n, k in product(range(2), repeat=3):
            colors = colors_at(m, n, k)
            require(all(colors[a] != colors[b] for a, b in es), 'local full-component action improper')
            states.append(dict(M02=m, N13=n, K02=k, colors=colors,
                six_palette_components={''.join(map(str, pair)): components(es, colors, pair)
                                        for pair in combinations(range(4), 2)}))
        orbits.append(dict(id=cell['id'], rows=states))
        neigh = {v: set() for v in previous['original_colors']}
        for a, b in es:
            neigh[a].add(b); neigh[b].add(a)
        blocked = [dict(pair=[a, b], strict_interior_common=sorted(neigh[a] & neigh[b] & {'tau', 'zeta'}))
                   for a, b in combinations(previous['boundary'], 2)
                   if edge(a, b) not in es and neigh[a] & neigh[b] & {'tau', 'zeta'}]
        require(any(r['pair'] == ['r', 's'] for r in blocked), 'r/s exterior separator lost')
        require(any(set(r['pair']) == {'x', 'd'} for r in blocked), 'x/d exterior separator lost')
        barriers.append(dict(id=cell['id'], forbidden_exterior_common_neighbors=blocked))
        for contract in contracts:
            old = contract['complete_predecessor_record']
            for att in product([None, 'U'], [None, 'V', 'HL_0'], [None, 'c'], [None, 'q']):
                failures = []
                for m, n, k in product(range(2), repeat=3):
                    joined, colors = join(cell, contract, att, m, n, k)
                    if k:
                        if not partial_refines(joined, colors, {0, 3}, [old['full_03_successor_boundary_contacts']]):
                            failures.append([m, n, k, 'unique_successor'])
                    else:
                        for pair, gate, label in [({0, 3}, gates03[contract['target']], 'initial03'),
                                ({0, 1}, old['complete_initial_01_gate'], 'initial01'),
                                ({0, 2}, [old['complete_initial_02_contacts']], 'initial02')]:
                            if not partial_refines(joined, colors, pair, gate):
                                failures.append([m, n, k, label])
                joined, _ = join(cell, contract, att, 0, 0, 0)
                nn = lambda v: {b if a == v else a for a, b in joined if v in (a, b)}
                for a, b, allowed in [('U', 'z4', {'V'}), ('HL_0', 'V', {'U'})]:
                    if (nn(a) & nn(b)) - allowed:
                        failures.append(['fixed_common_neighbor', a, b])
                d, e, h, w = att
                paper_allowed = not (e == 'V' and w == 'q') and not (h == 'c' and (d == 'U' or e is not None))
                paper_allowed &= not (d == 'U' and w == 'q' and any(cell['inside_ears'].values()))
                require(bool(paper_allowed) == (not failures), 'paper endpoint lemmas do not cover finite filter')
                attachments.append(dict(id=cell['id'], target=contract['target'], type02=contract['initial_02_type'],
                    ordered_d_e_h_W=list(att), failures=failures,
                    classification='necessary_endpoint_row' if not failures else 'excluded_endpoint_row'))
    return orbits, barriers, attachments


def validate(c, seed=0):
    previous, _, _ = fixed()
    require(c['schema'] == '941-gamma8-exterior-v1' and c['base'] == BASE, 'schema/BASE mismatch')
    require(c['complete_predecessor_certificate'] == previous, 'complete predecessor fibres/lifts lost')
    orbits, barriers, attachments = finite_domain()
    require(c['complete_local_orbits'] == orbits, 'complete eight-state six-palette orbit changed')
    require(c['exterior_barriers'] == barriers, 'original interior/exterior common-neighbor barrier changed')
    expected = {(r['id'], r['target'], r['type02'], tuple(r['ordered_d_e_h_W'])): r for r in attachments}
    rows = c['endpoint_rows']; require(len(rows) == len(expected) == 1056, 'finite attachment domain incomplete')
    seen = set(); shuffled = list(rows); random.Random(seed).shuffle(shuffled)
    for r in shuffled:
        key = (r['id'], r['target'], r['type02'], tuple(r['ordered_d_e_h_W']))
        require(key in expected and key not in seen and r == expected[key], 'endpoint row missing, repeated or changed')
        seen.add(key)
    require(c['paper_contract'] == dict(whole_original_M_N_and_same_K=True, M_N_rootless_full_stars_preserved=True,
        old_C_E_paths_not_assumed_to_survive=True, full_M2_separator_not_single_T_neighbor=True,
        B14_order_and_literal_frame_preserved=True, arbitrary_Gamma8_interior_for_endpoint_lemmas=True,
        four_exterior_private_points_only_under_j2=True, strict_exterior_private_lower_bound=4,
        O_core_strict_exterior_private_lower_bound=5,
        strict_off_Gamma_private_lower_bound=6, no_sharpness_claim=True, Wstar_q_exception_retained=True,
        d_U_exception_retained=True, h_c_exception_retained=True, eleven_types_all_retained=True,
        endpoint_rows_not_complete_exterior_collars=True), 'paper domain or source boundary changed')
    require(c['authority_boundaries'] == dict(finite_control='triggered and holds', original_source_control='not triggered',
        eleven_type_exclusions=0, initial_pair_exclusions=0, general_wrong_side='OPEN', smaller_bad=False,
        new_Lean=False, new_LP=False, common_k_lower_bound=23), 'unsupported theorem/source promotion')
    return dict(local_graphs=11, same_graph_orbit_states=88, complete_local_palette_components=528,
        finite_endpoint_rows=1056, necessary_endpoint_rows=sum(not r['failures'] for r in rows),
        excluded_endpoint_rows=sum(bool(r['failures']) for r in rows),
        four_contracts='two targets times initial02 13/36; original03 4/9 kept as joint two-choice gate',
        exterior_private_bound='L/R >=4, O >=5; paper proof, not source enumeration', original_source_control='not triggered')


def inherited(seed):
    spec = importlib.util.spec_from_file_location('frozen_gamma8', HERE / 'frozen' / PREVDIR / 'check.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); module.HERE = HERE
    return module.validate(fixed()[0], seed)


def negatives(c):
    tests = [
        ('lose_endpoint_row', lambda x: x['endpoint_rows'].pop()),
        ('lose_complete_orbit', lambda x: x['complete_local_orbits'][0]['rows'].pop()),
        ('drop_palette_component', lambda x: x['complete_local_orbits'][0]['rows'][0]['six_palette_components']['02'].pop()),
        ('change_literal_color', lambda x: x['complete_local_orbits'][0]['rows'][0]['colors'].update(T=2)),
        ('erase_exterior_barrier', lambda x: x['exterior_barriers'][0]['forbidden_exterior_common_neighbors'].pop()),
        ('retain_forbidden_attachment', lambda x: next(r for r in x['endpoint_rows'] if r['failures']).update(failures=[])),
        ('lose_prior_full_lift', lambda x: x['complete_predecessor_certificate']['candidates'][0]['literal_phi_boundary_fibre']['full_lifts'].pop()),
        ('claim_one_neighbor_separator', lambda x: x['paper_contract'].update(full_M2_separator_not_single_T_neighbor=False)),
        ('presume_old_C_paths_survive', lambda x: x['paper_contract'].update(old_C_E_paths_not_assumed_to_survive=False)),
        ('drop_q_exception', lambda x: x['paper_contract'].update(Wstar_q_exception_retained=False)),
        ('promote_finite_to_source', lambda x: x['authority_boundaries'].update(original_source_control='triggered and holds')),
        ('exclude_a_local_type', lambda x: x['authority_boundaries'].update(eleven_type_exclusions=1)),
        ('raise_common_k', lambda x: x['authority_boundaries'].update(common_k_lower_bound=24)),
        ('lose_O_five_point_bound', lambda x: x['paper_contract'].update(O_core_strict_exterior_private_lower_bound=4)),
    ]
    result = []
    for name, mutate in tests:
        bad = deepcopy(c); mutate(bad)
        try:
            validate(bad)
        except (ValueError, KeyError, IndexError, TypeError):
            result.append(dict(name=name, status='rejected'))
        else:
            raise ValueError('accepted negative: ' + name)
    return result


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--negative', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate-v2.json')
    args = parser.parse_args(); custody = authority()
    c = json.loads(args.certificate.read_text()); stats = validate(c, args.seed)
    result = dict(status='PASS', seed=args.seed, custody=custody, inherited=inherited(args.seed), **stats)
    if args.negative:
        result['semantic_negatives'] = negatives(c)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, IndexError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT', reason=str(exc)))); sys.exit(1)
