#!/usr/bin/env python3
"""Read-only face/zero-line reconstruction. General topology is a paper proof."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
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
PREVDIR = 'audits/2026-10-23-three-mask-round5-cb8f859/941'
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def edge(a, b):
    return tuple(sorted((a, b)))


def authority():
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    require(manifest['base'] == BASE, 'BASE changed')
    for row in manifest['inputs']:
        data = (HERE / row['snapshot']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (row['bytes'], row['sha256']), 'frozen drift')
        require(data == (ROOT / row['path']).read_bytes(), 'live authority drift: ' + row['path'])
    routing = []
    for row in manifest['routing_entry']:
        data = (HERE / row['snapshot']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (row['bytes'], row['sha256']), 'routing snapshot drift')
        routing.append(dict(path=row['path'], changed=data != (ROOT / row['path']).read_bytes()))
    return manifest, routing


def inherited(c, seed):
    previous = json.loads((HERE / 'frozen' / PREVDIR / 'certificate.json').read_text())
    require(c['complete_predecessor_certificate'] == previous, 'complete predecessor fibres/lifts changed')
    spec = importlib.util.spec_from_file_location('frozen_round5', HERE / 'frozen' / PREVDIR / 'check.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    module.HERE = HERE
    return module.validate(previous, seed)


def local_check(records, seed):
    domain = {(shared, ds) for shared in combinations(range(4), 2) for ds in product(range(2), repeat=2)}
    require(len(records) == 24 and {(tuple(r['shared_colors']), tuple(r['diagonal_choices'])) for r in records} == domain,
            'exactly-two-shared domain incomplete')
    counts, orders, degree_bounds = Counter(), Counter(), Counter()
    shuffled = list(records); random.Random(seed).shuffle(shuffled)
    for row in shuffled:
        shared = tuple(row['shared_colors']); ds = row['diagonal_choices']
        maps = [{c: f'{c}a' for c in range(4)}, {c: f'{c}a' if c in shared else f'{c}b' for c in range(4)}]
        require(row['roles'] == [{str(c): v for c, v in r.items()} for r in maps], 'same-source roles changed')
        # Build the complex from triangles, rather than the producer's edge union.
        faces, centers = [], []
        for role, d in zip(maps, ds):
            ends = (0, 3) if d == 0 else (1, 2)
            centers.append(edge(*(role[c] for c in ends)))
            faces.extend(tuple(sorted([role[ends[0]], role[ends[1]], role[c]]))
                         for c in range(4) if c not in ends)
        incidence = Counter(e for f in faces for e in combinations(f, 2))
        edges = set(incidence); vertices = set(v for f in faces for v in f)
        require(len(vertices) == 6, 'two-shared schemas must have six original vertices')
        require(row['edges'] == [list(e) for e in sorted(edges)], 'original edge union changed')
        require(sorted(tuple(sorted(f)) for f in row['faces']) == sorted(faces), 'actual original triangles changed')
        require([tuple(e) for e in row['centers']] == centers, 'center changed')
        k4s = [vs for vs in combinations(sorted(vertices), 4) if all(edge(*e) in edges for e in combinations(vs, 2))]
        if centers[0] == centers[1]:
            kind = 'same_center'
        elif k4s:
            kind = 'K4'
            require(tuple(row['blocker']) in k4s, 'false K4 blocker')
        elif shared in ((0, 3), (1, 2)):
            kind = 'C4_two_nonedges'; cycle = row['blocker']
            require(len(set(cycle)) == 4 and all(edge(a, b) in edges for a, b in zip(cycle, cycle[1:] + cycle[:1])), 'false C4 blocker')
            require(edge(cycle[0], cycle[2]) not in edges and edge(cycle[1], cycle[3]) not in edges, 'C4 diagonal exists')
            require(cycle[0][0] != cycle[2][0] and cycle[1][0] == cycle[3][0], 'C4 nonedge reasons changed')
            require(edge(cycle[0], cycle[2]) == edge(*(maps[0][c] for c in shared)), 'missing patch diagonal changed')
        else:
            kind = 'common_cycle_edge'
            # Four triangles glued in a dual path, with all six vertices on one outer C6.
            require(len(set(faces)) == 4 and len(edges) == 9 and max(incidence.values()) == 2, 'not a four-face patch disk')
            boundary = [e for e, n in incidence.items() if n == 1]
            require(len(boundary) == 6 and Counter(v for e in boundary for v in e) == Counter({v: 2 for v in vertices}), 'not one six-vertex outer boundary')
            dual = {i: {j for j in range(4) if i != j and len(set(faces[i]) & set(faces[j])) == 2} for i in range(4)}
            seen, todo = set(), [0]
            while todo:
                i = todo.pop()
                if i not in seen:
                    seen.add(i); todo.extend(dual[i] - seen)
            require(len(seen) == 4 and sorted(map(len, dual.values())) == [1, 1, 2, 2], 'triangle dual is not a path')
            require({tuple(sorted(t)) for t in combinations(vertices, 3) if all(edge(*e) in edges for e in combinations(t, 2))} == set(faces), 'extra separating triangle in local disk')
            common = edge(*(maps[0][c] for c in shared))
            require(incidence[common] == 2, 'shared edge has no two original faces')
            # Reconstruct J/H zero segments from the actual three face colors.
            colors = {v: c for r in maps for c, v in r.items()}
            chains = {}
            for name, group in [('alpha', lambda c: c % 2), ('beta', lambda c: int(c in (0, 1)))]:
                graph = defaultdict(set)
                for f in faces:
                    mids = [e for e in combinations(f, 2) if group(colors[e[0]]) != group(colors[e[1]])]
                    require(len(mids) == 2, 'not a unique zero segment in original triangle')
                    graph[mids[0]].add(mids[1]); graph[mids[1]].add(mids[0])
                chains[name] = graph
            expected_interface = 'beta' if shared in ((0, 2), (1, 3)) else 'alpha'
            require(chains[expected_interface][common] == set(centers), 'centers not directly consecutive through shared edge')
            require(common not in chains['alpha' if expected_interface == 'beta' else 'beta'], 'shared edge lies on both interfaces')
            side = {(0, 2): 'K', (1, 3): 'B', (0, 1): 'C', (2, 3): 'Q'}[shared]
            require(row['consecutive_interface'] == expected_interface and row['intervening_side'] == side, 'interface order/side changed')
            require(row['partial_disk_only'] is True, 'partial disk promoted to source')
            orders[(expected_interface, side)] += 1
            for c in shared:
                v = maps[0][c]; link_edges = [edge(*(w for w in f if w != v)) for f in faces if v in f]
                link_inc = Counter(w for e in link_edges for w in e)
                ends = [w for w, n in link_inc.items() if n == 1]
                require(len(ends) == 2 and colors[ends[0]] == colors[ends[1]] and edge(*ends) not in edges, 'private link closure must retain same-color distinct ends')
                m = sum(v in center for center in centers)
                expected = dict(incident_centers=m, union_neighbors=len(link_inc), degree_lower_bound=max(5, len(link_inc) + 1))
                require(len(link_inc) == 3 + m and row['private_shared_vertex_link'][str(c)] == expected, 'private full-link degree obligation changed')
                degree_bounds[expected['degree_lower_bound']] += 1
        require(row['classification'] == kind, 'wrong two-shared classification'); counts[kind] += 1
    require(counts == Counter(common_cycle_edge=16, same_center=2, K4=4, C4_two_nonedges=2), 'wrong complete schema totals')
    return dict(schemas=24, classifications=dict(sorted(counts.items())),
                direct_zero_chains={f'{k[0]}_{k[1]}': v for k, v in sorted(orders.items())},
                private_shared_link_degree_bounds={str(k): v for k, v in sorted(degree_bounds.items())})


def validate(c, seed=0):
    require(c['schema'] == '941-patch-order-v1' and c['base'] == BASE, 'scope/base changed')
    expected_claims = dict(transverse_crossings_even_at_least_two=True,
        tangencies_separated_locally_preserving_markers=True,
        alpha_marked_pair='Q excursion containing P last K exit midpoint',
        beta_marked_pair='Omega excursion containing marked u-minus Z midpoint',
        marked_pairs_may_differ=True, alpha_pair_allowed_two_shared_colors=[[0, 2], [1, 3]],
        beta_pair_allowed_two_shared_colors=[[0, 1], [0, 2], [2, 3]],
        beta_pair_shared02_is_marked_u_minus_Z=True, alpha_pair_shared13_forces_at_least_four_crossings=True,
        ear_lens_exists_but_need_not_contain_marker=True, ear_lens_may_be_C_or_Q=True,
        other_complete_component_interfaces_retained=True)
    require(c['paper_claims'] == expected_claims, 'paper scope/marker identity changed (paper proof required)')
    require(c['boundaries'] == dict(source_control='not triggered', finite_calibration='triggered and holds',
        new_initial_pair_exclusions=0, source_realized=False, smaller_bad=False, new_Lean=False,
        no_source_enumeration_or_LP=True, R_r_not_identified=True, M_L_not_identified=True,
        K0_not_assumed_all_C=True, boundary_tip_and_rootless_retained=True,
        original_degree5_sides_and_high_degree_retained=True, original_P_and_B13_joint_realization='OPEN'), 'source boundary changed')
    return dict(inherited=inherited(c, seed), local=local_check(c['exact_two_shared_schemas'], seed))


def negatives(c):
    tests = [
        ('lose_two_shared_schema', lambda x: x['exact_two_shared_schemas'].pop()),
        ('invent_source', lambda x: x['boundaries'].update(source_realized=True)),
        ('exclude_initial_pair', lambda x: x['boundaries'].update(new_initial_pair_exclusions=1)),
        ('identify_marked_pairs', lambda x: x['paper_claims'].update(marked_pairs_may_differ=False)),
        ('allow_alpha_marked_common23', lambda x: x['paper_claims']['alpha_pair_allowed_two_shared_colors'].append([2, 3])),
        ('lose_marked_Z_identity', lambda x: x['paper_claims'].update(beta_pair_shared02_is_marked_u_minus_Z=False)),
        ('force_ear_to_contain_marker', lambda x: x['paper_claims'].update(ear_lens_exists_but_need_not_contain_marker=False)),
        ('delete_rootless', lambda x: x['boundaries'].update(boundary_tip_and_rootless_retained=False)),
        ('lose_empty_fibres', lambda x: x['complete_predecessor_certificate']['upstream_complete_fibre_custody'].update(empty_seven_point_fibres=0)),
        ('reverse_shared_edge_side', lambda x: next(r for r in x['exact_two_shared_schemas'] if r['classification'] == 'common_cycle_edge').update(intervening_side='unproved')),
        ('promote_local_disk', lambda x: next(r for r in x['exact_two_shared_schemas'] if r['classification'] == 'common_cycle_edge').update(partial_disk_only=False)),
        ('erase_private_link_extra_neighbor', lambda x: next(r for r in x['exact_two_shared_schemas'] if r['classification'] == 'common_cycle_edge')['private_shared_vertex_link']['0'].update(union_neighbors=0)),
    ]
    out = []
    for name, mutate in tests:
        bad = deepcopy(c); mutate(bad)
        try:
            validate(bad)
        except (ValueError, KeyError, TypeError, IndexError):
            out.append(dict(name=name, status='rejected'))
        else:
            raise ValueError('corrupted certificate accepted: ' + name)
    return out


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--negative', action='store_true'); parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args(); manifest, routing = authority()
    c = json.loads(args.certificate.read_text()); stats = validate(c, args.seed)
    result = dict(status='PASS', seed=args.seed, frozen_inputs=len(manifest['inputs']), immutable_input_drift=0,
                  routing_live_drift=routing, source_control='not triggered', new_initial_pair_exclusions=0,
                  general_topology_authority='paper proof; finite checks calibrate only local schemas', **stats)
    if args.negative:
        result['semantic_negatives'] = negatives(c)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, IndexError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT', reason=str(exc)))); sys.exit(1)
