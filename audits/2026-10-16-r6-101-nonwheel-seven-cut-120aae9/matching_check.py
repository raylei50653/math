#!/usr/bin/env python3
"""Exact finite seven-port calibration, never a source-realization check."""
import argparse
from collections import defaultdict
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def adjacency(vertices, edges):
    result = {v: set() for v in vertices}
    for a, b in edges:
        result[a].add(b)
        result[b].add(a)
    return result


def matchings(vertices, edges):
    vertices = set(vertices)
    adj = adjacency(vertices, [e for e in edges if set(e) <= vertices])

    def visit(left):
        if not left:
            yield ()
            return
        a = min(left)
        for b in sorted(adj[a] & left):
            for rest in visit(left - {a, b}):
                yield tuple(sorted((edge(a, b),) + rest))
    return sorted(visit(vertices))


def noncrossing(points):
    points = tuple(points)
    if not points:
        return [()]
    result = []
    a = points[0]
    for j in range(1, len(points), 2):
        for first in noncrossing(points[1:j]):
            for last in noncrossing(points[j+1:]):
                result.append(tuple(sorted(((a, points[j]),) + first + last)))
    return sorted(result)


def canonical_cycle(vertices):
    variants = []
    for seq in (vertices, list(reversed(vertices))):
        for j in range(len(seq)):
            variants.append(tuple(seq[j:] + seq[:j]))
    return min(variants)


def components(vertices, edges):
    adj = adjacency(vertices, edges)
    unseen = set(vertices)
    result = []
    while unseen:
        seed = min(unseen)
        found = {seed}
        stack = [seed]
        while stack:
            v = stack.pop()
            for w in sorted(adj[v] - found):
                found.add(w)
                stack.append(w)
        unseen -= found
        result.append(found)
    return adj, result


def complement_record(vertices, edges, matching, ports):
    complement = sorted(set(edges) - set(matching))
    adj, comps = components(vertices, complement)
    paths, cycles = [], []
    inverse = {v: i for i, v in enumerate(ports)}
    for comp in comps:
        ends = sorted(v for v in comp if len(adj[v]) == 1)
        require(all(len(adj[v]) in (1, 2) for v in comp), 'complement degree')
        require(len(ends) in (0, 2), 'path or cycle')
        start = ends[0] if ends else min(comp)
        walk, previous, current = [start], None, start
        while True:
            choices = sorted(adj[current] - ({previous} if previous is not None else set()))
            if not choices:
                break
            nxt = choices[0]
            if nxt == start:
                break
            walk.append(nxt)
            previous, current = current, nxt
        require(set(walk) == comp, 'complete component walk')
        if ends:
            a, b = inverse[walk[0]], inverse[walk[-1]]
            if a > b:
                walk.reverse()
                a, b = b, a
            paths.append({'ports': [a, b], 'vertices': walk,
                          'length': len(walk)-1, 'parity': (len(walk)-1) % 2})
        else:
            cycle = list(canonical_cycle(walk))
            cycles.append(cycle)
    paths.sort(key=lambda row: row['ports'])
    cycles.sort()
    return {'paths': paths, 'cycles': cycles,
            'internal_odd_cycle': any(len(c) % 2 for c in cycles)}


def state_key(selected, pairs, parities, odd):
    return json.dumps([list(selected), [list(pair) for pair in pairs],
                       list(parities), int(odd)], separators=(',', ':'))


def registry():
    result = {}
    for mask in range(128):
        selected = [i for i in range(7) if mask & (1 << i)]
        if not len(selected) % 2:
            continue
        remaining = [i for i in range(7) if i not in selected]
        for pairing in noncrossing(remaining):
            for parities in product((0, 1), repeat=len(pairing)):
                for odd in (0, 1):
                    result[state_key(selected, pairing, parities, odd)] = []
    require(len(result) == 1206, '1206 complete states')
    tight = sum(len(json.loads(key)[0]) == 1 for key in result)
    require(tight == 560, '560 tight states')
    return result


def patch(name, vertices, edges, ports, boundary, primal_faces=None):
    vertices, edges = sorted(vertices), sorted(set(edge(*e) for e in edges))
    adj = adjacency(vertices, edges)
    require(len(ports) == 7 and len(set(ports)) == 7, 'seven distinct ports')
    require({v for v in vertices if len(adj[v]) == 2} == set(ports), 'all degree-two ports')
    require(all(len(adj[v]) == (2 if v in ports else 3) for v in vertices), 'cubic internal degrees')
    require(all(edge(boundary[i], boundary[(i+1) % len(boundary)]) in edges
                for i in range(len(boundary))), 'literal simple outer boundary')
    require(len(set(boundary)) == len(boundary), 'simple outer boundary')
    require([v for v in boundary if v in ports] == ports, 'actual port cyclic order')
    require(set(ports) <= set(boundary), 'ports on same outer face')
    if primal_faces is None:
        # First two declared embeddings have only a cycle and optionally one chord.
        require(set(boundary) == set(vertices), 'outerplane control vertices')
        require(len(edges)-len(vertices) in (0, 1), 'declared simple embedding domain')
    require(all(matchings(set(vertices)-{v}, edges) for v in vertices), 'factor critical')
    states, cells, lifts = registry(), [], []
    for mask in range(128):
        selected = [i for i in range(7) if mask & (1 << i)]
        all_pm = matchings(set(vertices)-{ports[i] for i in selected}, edges)
        ids = []
        for pm in all_pm:
            rec = complement_record(vertices, edges, pm, ports)
            r = (7-len(selected))//2
            require((sum(p['parity'] for p in rec['paths']) +
                     sum(len(c) % 2 for c in rec['cycles'])) % 2 == (1-r) % 2,
                    'universal complement edge-count parity')
            pairs = [p['ports'] for p in rec['paths']]
            key = state_key(selected, pairs, [p['parity'] for p in rec['paths']],
                            rec['internal_odd_cycle'])
            require(key in states, 'noncrossing complete state')
            lift = {'id': len(lifts), 'selected_ports': selected,
                    'matching': [list(e) for e in pm], **rec, 'state': key}
            states[key].append(lift['id'])
            ids.append(lift['id'])
            lifts.append(lift)
        cells.append({'selected_ports': selected, 'all_matching_lifts': ids})
    return {'name': name, 'vertices': vertices, 'edges': [list(e) for e in edges],
            'ports_in_boundary_order': ports, 'outer_boundary': boundary,
            'declared_primal_disk_faces': primal_faces,
            'all_128_boundary_cells': cells, 'all_1206_state_fibres': states,
            'all_internal_matching_lifts': lifts,
            'empty_boundary_cells': sum(not cell['all_matching_lifts'] for cell in cells),
            'empty_state_fibres': sum(not ids for ids in states.values()),
            'factor_critical_deletion_lifts': [
                {'deleted_vertex': v,
                 'all_matching_lifts': [[list(e) for e in m] for m in matchings(set(vertices)-{v}, edges)]}
                for v in vertices]}


def joined_parities(left, right):
    links = []
    for side, lift in enumerate((left, right)):
        for path in lift['paths']:
            a, b = path['ports']
            links.append((a, b, path['parity'], side))
    unused = set(range(len(links)))
    result = []
    while unused:
        start = min(unused)
        found, todo = {start}, [start]
        while todo:
            k = todo.pop()
            endpoints = set(links[k][:2])
            for j in sorted(unused-found):
                if endpoints & set(links[j][:2]):
                    found.add(j)
                    todo.append(j)
        unused -= found
        require(len(found) % 2 == 0, 'alternating port cycle even size')
        require(sum(links[j][3] == 0 for j in found) == len(found)//2,
                'equal internal external paths')
        result.append(sum(links[j][2] for j in found) % 2)
    return sorted(result)


def tait_lifts(edges, matching, cycles):
    # Name matching colour 0; explicitly preserve every orientation of 1,2.
    if any(len(c) % 2 for c in cycles):
        return []
    index = {e: i for i, e in enumerate(edges)}
    result = []
    for bits in product((0, 1), repeat=len(cycles)):
        colours = [None]*len(edges)
        for e in matching:
            colours[index[e]] = 0
        for cycle, bit in zip(cycles, bits):
            for i, a in enumerate(cycle):
                b = cycle[(i+1) % len(cycle)]
                colours[index[edge(a, b)]] = 1 + ((i+bit) % 2)
        require(None not in colours, 'every Tait edge retained')
        result.append(colours)
    return result


def glue(control):
    n = len(control['vertices'])
    local_edges = [tuple(e) for e in control['edges']]
    ports = control['ports_in_boundary_order']
    cut = [edge(p, p+n) for p in ports]
    edges = sorted(local_edges + [edge(a+n, b+n) for a, b in local_edges] + cut)
    vertices = list(range(2*n))
    expected = matchings(vertices, edges)
    records, seen = [], []
    groups = {}
    for lift in control['all_internal_matching_lifts']:
        groups.setdefault(tuple(lift['selected_ports']), []).append(lift)
    for selected, group in sorted(groups.items()):
        for left, right in product(group, repeat=2):
            pm = tuple(sorted([tuple(e) for e in left['matching']] +
                              [edge(a+n, b+n) for a, b in right['matching']] +
                              [cut[i] for i in selected]))
            seen.append(pm)
            rec = complement_record(vertices, edges, pm, [])
            require(not rec['paths'], 'global complement only cycles')
            parity = joined_parities(left, right)
            actual_odd = sum(len(c) % 2 for c in rec['cycles'])
            predicted_odd = sum(parity) + sum(len(c) % 2 for c in left['cycles'] + right['cycles'])
            require(actual_odd == predicted_odd, 'literal parity join exact')
            actual_cycles = len(rec['cycles'])
            require(actual_cycles == len(left['cycles'])+len(right['cycles'])+len(parity), 'cycle-count join')
            tait = tait_lifts(edges, pm, rec['cycles'])
            require(bool(tait) == (actual_odd == 0), 'empty odd-colour fibre retained')
            require(not tait or len(tait) == 2**actual_cycles, 'all Tait choices')
            records.append({'selected_ports': list(selected), 'left_lift': left['id'],
                            'right_lift': right['id'], 'matching': [list(e) for e in pm],
                            'complete_complement_cycles': rec['cycles'],
                            'joined_cycle_parities': parity,
                            'all_named_Tait_edge_colour_lifts': tait})
    require(sorted(seen) == expected, 'exact direct global PM reconstruction')
    require(len(set(seen)) == len(seen), 'no duplicate matching lifts')
    require(any(not r['all_named_Tait_edge_colour_lifts'] for r in records), 'nonvacuous empty even fibres')
    return {'name': control['name']+'_double', 'vertices': vertices,
            'ordered_edges_for_Tait_lifts': [list(e) for e in edges],
            'all_global_matching_lifts': records, 'global_matching_count': len(records),
            'empty_even_colour_fibres': sum(not r['all_named_Tait_edge_colour_lifts'] for r in records)}


def compute():
    seven = patch('cycle7', range(7), [edge(i, (i+1) % 7) for i in range(7)], list(range(7)), list(range(7)))
    boundary = [0, 2, 3, 4, 5, 1, 6, 7, 8]
    theta = patch('theta_1_5_4', range(9),
                  [edge(boundary[i], boundary[(i+1) % 9]) for i in range(9)] + [(0, 1)],
                  [2, 3, 4, 5, 6, 7, 8], boundary)
    faces = [['a', 'b', 'U'], ['b', 'c', 'U'], ['c', 'd', 'U'],
             ['d', 'e', 'B'], ['e', 'f', 'B'], ['f', 'g', 'C'],
             ['g', 'a', 'C'], ['d', 'U', 'A'], ['d', 'A', 'B'],
             ['a', 'C', 'A'], ['a', 'A', 'U'], ['f', 'B', 'C'], ['A', 'B', 'C']]
    incidence = defaultdict(list)
    for i, face in enumerate(faces):
        for j, a in enumerate(face):
            incidence[edge(a, face[(j+1) % 3])].append(i)
    require(all(len(ids) in (1, 2) for ids in incidence.values()), 'literal face incidence')
    primal_boundary = 'abcdefg'
    boundary_edges = [edge(primal_boundary[i], primal_boundary[(i+1) % 7]) for i in range(7)]
    require(set(e for e, ids in incidence.items() if len(ids) == 1) == set(boundary_edges), 'actual seven boundary edges')
    interior_dual_edges = [tuple(ids) for ids in incidence.values() if len(ids) == 2]
    primal_adj = adjacency(set(sum(faces, [])), list(incidence))
    require(all(len(primal_adj[v]) == 5 for v in 'UABC'), 'four complete interior degree-five vertices')
    thirteen = patch('thirteen_face_triangle_pendant_disk', range(13), interior_dual_edges,
                     [incidence[e][0] for e in boundary_edges],
                     [0, 1, 2, 7, 8, 3, 4, 11, 5, 6, 9, 10], primal_faces=faces)
    controls = [seven, theta, thirteen]
    return {'schema': 'R6-101-seven-port-exact-matching-interface-v1',
            'scope': 'three declared local patches and their doubled seven-edge gluings only',
            'source_realization': {'status': 'not triggered', 'genuine_sources': 0,
                                   'paper_source_proof_by_this_checker': False},
            'finite_registry': {'all_ordinary_states': 1206, 'tight_states': 560,
                                'even_boundary_patterns_retained_as_empty': 64},
            'controls': controls, 'complete_glued_controls': [glue(c) for c in controls]}


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    parser.add_argument('--negative', choices=['path-parity', 'missing-empty', 'odd-cycle-flag'])
    args = parser.parse_args()
    result = compute()
    if args.write:
        require(args.negative is None, 'negative mode only compares certificates')
        with args.write.open('x') as stream:
            json.dump(result, stream, sort_keys=True, separators=(',', ':'))
            stream.write('\n')
    else:
        expected = json.loads(args.check.read_text())
        if args.negative == 'path-parity':
            lift = next(x for x in expected['controls'][0]['all_internal_matching_lifts'] if x['paths'])
            lift['paths'][0]['parity'] ^= 1
        elif args.negative == 'missing-empty':
            states = expected['controls'][0]['all_1206_state_fibres']
            del states[next(key for key, values in states.items() if not values)]
        elif args.negative == 'odd-cycle-flag':
            lift = next(x for x in expected['controls'][0]['all_internal_matching_lifts'] if x['internal_odd_cycle'])
            lift['internal_odd_cycle'] = False
        require(result == expected, 'complete certificate mismatch')
    print(json.dumps({'status': 'PASS', 'source_realization': 'not triggered',
                      'ordinary_states': 1206, 'tight_states': 560,
                      'patches': [{'name': c['name'], 'internal_lifts': len(c['all_internal_matching_lifts']),
                                   'empty_boundary_cells': c['empty_boundary_cells'],
                                   'empty_state_fibres': c['empty_state_fibres']} for c in result['controls']],
                      'glued_counts': [c['global_matching_count'] for c in result['complete_glued_controls']]},
                     sort_keys=True))


if __name__ == '__main__':
    main()
