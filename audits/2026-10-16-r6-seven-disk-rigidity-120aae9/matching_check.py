#!/usr/bin/env python3
"""Finite exterior/parity calibration. Never checks source realizability."""
import argparse
from itertools import product
import json
from pathlib import Path
import random


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def adjacency(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


RNG = random.Random(0)


def matchings(vertices, edges):
    vertices = set(vertices)
    adj = adjacency(vertices, [e for e in edges if set(e) <= vertices])

    def visit(left):
        if not left:
            yield ()
            return
        a = min(left)
        choices = sorted(adj[a] & left)
        RNG.shuffle(choices)
        for b in choices:
            for rest in visit(left - {a, b}):
                yield tuple(sorted((edge(a, b),) + rest))
    return sorted(visit(vertices))


def noncrossing(points):
    if not points:
        return [()]
    result = []
    for j in range(1, len(points), 2):
        for first in noncrossing(points[1:j]):
            for last in noncrossing(points[j+1:]):
                result.append(tuple(sorted(((points[0], points[j]),) + first + last)))
    return sorted(result)


def state_key(selected, paths, odd):
    return json.dumps([list(selected), [p['ports'] for p in paths],
                       [p['parity'] for p in paths], int(odd)], separators=(',', ':'))


def registry():
    states = {}
    for mask in range(128):
        chosen = [i for i in range(7) if mask & (1 << i)]
        if len(chosen) % 2 != 1:
            continue
        remaining = [i for i in range(7) if i not in chosen]
        for pairs in noncrossing(remaining):
            for parity in product((0, 1), repeat=len(pairs)):
                paths = [{'ports': list(p), 'parity': a} for p, a in zip(pairs, parity)]
                for odd in (0, 1):
                    states[state_key(chosen, paths, odd)] = []
    require(len(states) == 1206, 'all ordinary registered states')
    tight = [json.loads(k) for k in states if len(json.loads(k)[0]) == 1]
    require(len(tight) == 560, 'tight registry')
    impossible = sum(x[3] == 0 and sum(x[2]) % 2 == 1 for x in tight)
    eligible = sum(x[3] == 0 and sum(x[2]) % 2 == 0 for x in tight)
    require((impossible, eligible, len(tight)-impossible) == (140, 140, 420), 'signature bounds')
    return states


def canonical_cycle(walk):
    return min(tuple(seq[i:] + seq[:i])
               for seq in (walk, list(reversed(walk))) for i in range(len(walk)))


def complement(vertices, edges, matching, endpoint_labels):
    """Add distinct marker leaves, including two at one repeated exterior end."""
    actual = set(vertices)
    augmented = set(actual)
    residual = set(edges) - set(matching)
    marker = {}
    for label, vertex in endpoint_labels.items():
        leaf = 1000 + label
        require(leaf not in augmented, 'fresh marker')
        marker[leaf] = label
        augmented.add(leaf)
        residual.add(edge(leaf, vertex))
    adj = adjacency(augmented, residual)
    require(all(len(adj[v]) == 2 for v in actual), 'all complement vertices have two incidences')
    require(all(len(adj[v]) == 1 for v in marker), 'marker leaves')
    unseen = set(augmented)
    paths, cycles = [], []
    while unseen:
        start = min(unseen & marker.keys()) if unseen & marker.keys() else min(unseen)
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
        require(set(walk) <= unseen, 'disjoint complete components')
        unseen -= set(walk)
        if start in marker:
            require(walk[-1] in marker and len(walk) >= 3, 'two distinct marker ends')
            labels = [marker[start], marker[walk[-1]]]
            literal = walk[1:-1]
            if labels[0] > labels[1]:
                labels.reverse()
                literal.reverse()
            length = len(literal)-1
            paths.append({'ports': labels, 'vertices': literal, 'length': length, 'parity': length % 2})
        else:
            cycles.append(list(canonical_cycle(walk)))
    paths.sort(key=lambda p: p['ports'])
    cycles.sort()
    return {'paths': paths, 'cycles': cycles, 'internal_odd_cycle': any(len(c) % 2 for c in cycles)}


def tait_lifts(edges, matching, cycles):
    if any(len(c) % 2 for c in cycles):
        return []
    index = {e: i for i, e in enumerate(edges)}
    lifts = []
    for choices in product((0, 1), repeat=len(cycles)):
        colours = [None] * len(edges)
        for e in matching:
            colours[index[e]] = 0
        for cycle, bit in zip(cycles, choices):
            for j, a in enumerate(cycle):
                colours[index[edge(a, cycle[(j+1) % len(cycle)])]] = 1 + (j+bit) % 2
        require(None not in colours, 'full Tait assignments')
        lifts.append(colours)
    return lifts


def patch(name, n, chord=None, port_shift=0):
    vertices = list(range(n))
    edges = [edge(i, (i+1) % n) for i in vertices]
    if chord:
        edges.append(edge(*chord))
    edges = sorted(edges)
    ports = [v for v in vertices if chord is None or v not in chord]
    ports = ports[port_shift:] + ports[:port_shift]
    require(len(ports) == 7, 'seven distinct patch ports')
    deletion = [{'deleted_vertex': v, 'all_matchings': matchings(set(vertices)-{v}, edges)} for v in vertices]
    require(all(row['all_matchings'] for row in deletion), 'factor critical deletion witnesses')
    states, cells, lifts = registry(), [], []
    for mask in range(128):
        chosen = [i for i in range(7) if mask & (1 << i)]
        ids = []
        for matching in matchings(set(vertices)-{ports[i] for i in chosen}, edges):
            rec = complement(vertices, edges, matching, {i: ports[i] for i in range(7) if i not in chosen})
            key = state_key(chosen, rec['paths'], rec['internal_odd_cycle'])
            require(key in states, 'actual patch noncrossing state')
            r = (7-len(chosen))//2
            require((sum(p['parity'] for p in rec['paths'])+sum(len(c) % 2 for c in rec['cycles'])) % 2 == (1-r) % 2, 'edge count parity')
            ident = len(lifts)
            lifts.append({'id': ident, 'selected_ports': chosen, 'matching': matching, 'state': key, **rec})
            states[key].append(ident)
            ids.append(ident)
        cells.append({'selected_ports': chosen, 'all_internal_matching_lifts': ids})
    return {'name': name, 'vertices': vertices, 'edges': edges, 'ports': ports,
            'factor_critical_all_deletions': deletion, 'all_128_boundary_cells': cells,
            'all_1206_state_fibres': states, 'all_internal_lifts': lifts}


def exterior(crossing):
    x = [100, 101, 102, 103]
    e, g = edge(100, 101), edge(102, 103)
    if crossing:
        a, b = [104], x
        vertices = x + a
        edges = [e, g, edge(101, 104), edge(104, 102)]
        ports = [100, 100, 101, 104, 102, 103, 103]
        f = None
        s = []
    else:
        s, a = [104], [105, 106]
        b = x + s
        f = edge(105, 106)
        vertices = x + s + a
        edges = [e, g, f, edge(101, 105), edge(102, 106), edge(104, 105), edge(104, 106)]
        ports = [100, 100, 101, 104, 102, 103, 103]
    return {'case': 'crossing_f' if crossing else 'external_f', 'vertices': vertices,
            'edges': sorted(edges), 'cut_endpoints': ports, 'A': a, 'B': b, 'S': s,
            'X': x, 'e': e, 'g': g, 'f': f}


def pairing_components(left, right):
    pairs = [(p['ports'], p['parity']) for p in left['paths'] + right['paths']]
    remaining = set(range(len(pairs)))
    result = []
    while remaining:
        found, todo = {min(remaining)}, [min(remaining)]
        while todo:
            current = todo.pop()
            for other in sorted(remaining-found):
                if set(pairs[current][0]) & set(pairs[other][0]):
                    found.add(other)
                    todo.append(other)
        remaining -= found
        result.append({'ports': sorted({v for j in found for v in pairs[j][0]}),
                       'parity': sum(pairs[j][1] for j in found) % 2})
    return sorted(result, key=lambda row: row['ports'])


def control(p, ext):
    pv, pe, ports = p['vertices'], p['edges'], p['ports']
    ev, ee, ends = ext['vertices'], ext['edges'], ext['cut_endpoints']
    cut = [edge(u, v) for u, v in zip(ports, ends)]
    vertices, edges = pv + ev, sorted(pe + ee + cut)
    adj = adjacency(vertices, edges)
    require(all(len(adj[v]) == 3 for v in vertices), 'whole cubic control')
    e, g = ext['e'], ext['g']
    f = cut[3] if ext['f'] is None else ext['f']
    marks = [e, f, g]
    all_pm = matchings(vertices, edges)
    global_records = []
    global_index = {}
    for pm in all_pm:
        rec = complement(vertices, edges, pm, {})
        ident = len(global_records)
        global_index[pm] = ident
        global_records.append({'id': ident, 'matching': pm,
                               'mark_pattern': ''.join('1' if m in pm else '0' for m in marks),
                               **rec, 'all_labelled_tait_lifts': tait_lifts(edges, pm, rec['cycles'])})
    internal = {tuple(cell['selected_ports']): cell['all_internal_matching_lifts'] for cell in p['all_128_boundary_cells']}
    exterior_records, cells, joins = [], [], []
    for mask in range(128):
        chosen = [i for i in range(7) if mask & (1 << i)]
        selected = {cut[i] for i in chosen}
        removed = [ends[i] for i in chosen]
        by_pattern = {''.join(x): [] for x in product('01', repeat=3)}
        if len(set(removed)) == len(removed):
            for pm in matchings(set(ev)-set(removed), ee):
                combined = set(pm) | selected
                pattern = ''.join('1' if m in combined else '0' for m in marks)
                rec = complement(ev, ee, pm, {i: ends[i] for i in range(7) if i not in chosen})
                ident = len(exterior_records)
                exterior_records.append({'id': ident, 'selected_ports': chosen,
                                         'internal_matching': pm, 'selected_cut_edges': sorted(selected),
                                         'mark_pattern': pattern, **rec})
                by_pattern[pattern].append(ident)
                if pattern == '111':
                    require(chosen == [3], 'exact exterior support')
                    require(not rec['internal_odd_cycle'], 'exterior cycles all even')
                    require(all(q['parity'] == 0 for q in rec['paths']), 'every exterior path even')
                    require(all(ends[i] in ext['B'] for i in range(7) if i not in chosen), 'unselected ends all B')
                    if ext['f'] is None:
                        balanced = matchings(set(ext['S']) | (set(ext['A'])-{ends[3]}), ee)
                    else:
                        balanced = matchings((set(ext['S'])-{ends[3]}) | (set(ext['A'])-set(f)), ee)
                    strip = tuple(q for q in pm if q not in marks)
                    require(strip in balanced, 'literal bipartite witness')
                for iid in internal[tuple(chosen)]:
                    lift = p['all_internal_lifts'][iid]
                    whole = tuple(sorted(list(lift['matching']) + list(pm) + list(selected)))
                    require(whole in global_index, 'literal union is global matching')
                    target = global_records[global_index[whole]]
                    pair = pairing_components(lift, rec)
                    predicted_odd = sum(z['parity'] for z in pair) + sum(len(c) % 2 for c in lift['cycles']+rec['cycles'])
                    require(predicted_odd == sum(len(c) % 2 for c in target['cycles']), 'exact complement parity join')
                    require(len(pair)+len(lift['cycles'])+len(rec['cycles']) == len(target['cycles']), 'exact complement cycle count')
                    if pattern == '111':
                        eligible = not lift['internal_odd_cycle'] and all(z['parity'] == 0 for z in pair)
                        require(eligible == bool(target['all_labelled_tait_lifts']), 'specialized iff even111 join')
                    joins.append({'internal_lift': iid, 'exterior_lift': ident,
                                  'global_matching': target['id'], 'joined_pairing_components': pair})
        require(by_pattern['101'] == [], 'all 128 exterior101 cells empty')
        cells.append({'selected_ports': chosen, 'all_eight_exact_mark_fibres': by_pattern})
    require(sorted(j['global_matching'] for j in joins) == list(range(len(global_records))), 'complete disjoint restriction-union bijection')
    p111 = [r for r in global_records if r['mark_pattern'] == '111']
    require(p111, '111 nonempty calibration')
    zero_paths = sum(q['length'] == 0 for r in exterior_records if r['mark_pattern'] == '111' for q in r['paths'])
    require(zero_paths >= 2, 'repeated endpoint zero paths actually triggered')
    embedding = spherical_embedding(vertices, edges)
    return {'name': p['name'] + '__' + ext['case'], 'patch_name': p['name'], 'spherical_embedding': embedding,
            'exterior': ext, 'vertices': vertices, 'edges': edges, 'marks_e_f_g': marks,
            'actual_cut_edges': cut, 'all_128_exterior_cells': cells,
            'all_exterior_matching_lifts': exterior_records, 'all_global_pm_lifts': global_records,
            'full_restriction_union_lifts': joins,
            'summary': {'all_pm': len(global_records), 'P111': len(p111), 'P101': 0,
                        'even111': sum(bool(r['all_labelled_tait_lifts']) for r in p111),
                        'all_tait_lifts_fixed_matching_colour': sum(len(r['all_labelled_tait_lifts']) for r in global_records),
                        'exterior111_zero_length_paths': zero_paths,
                        'source_realizability': 'not triggered'}}


def support_calibration():
    s, a = [0, 1, 2, 3], [10, 11, 12]
    edges = [edge(0, 10), edge(1, 10), edge(1, 11), edge(2, 11), edge(3, 12)]
    full = matchings(s[1:] + a, edges)
    require(full, 'one fixed support witness exposing root zero')
    witness = set(full[0])
    directed = {v: set() for v in s+a}
    for x, y in edges:
        left, right = (x, y) if x in s else (y, x)
        start, end = (right, left) if (x, y) in witness else (left, right)
        directed[start].add(end)
    reached, todo = {0}, [0]
    while todo:
        v = todo.pop()
        for w in sorted(directed[v]-reached):
            reached.add(w)
            todo.append(w)
    fibres = [{'exposed_S_vertex': v, 'all_matching_lifts': matchings((set(s)-{v}) | set(a), edges)} for v in s]
    require({row['exposed_S_vertex'] for row in fibres if row['all_matching_lifts']} == reached & set(s) == {0, 1, 2}, 'nontrivial alternating support iff')
    return {'S': s, 'A_prime': a, 'edges': edges, 'fixed_matching_exposing_zero': sorted(witness),
            'directed_reachable_vertices': sorted(reached), 'all_support_fibres_including_empty': fibres,
            'source_realizability': 'not triggered'}


def spherical_embedding(vertices, edges):
    adj = adjacency(vertices, edges)
    ordered = [sorted(adj[v]) for v in vertices]
    darts = [(a, b) for a, b in edges for a, b in ((a, b), (b, a))]
    for bits in product((0, 1), repeat=len(vertices)-1):
        rotation = {v: (list(reversed(n)) if bit else n) for v, n, bit in zip(vertices, ordered, (0,)+bits)}
        successor = {(a, b): (b, rotation[b][(rotation[b].index(a)+1) % len(rotation[b])]) for a, b in darts}
        unused, faces = set(darts), []
        while unused:
            start = min(unused)
            current, face = start, []
            while True:
                require(current in unused, 'rotation face darts disjoint')
                unused.remove(current)
                face.append(current[0])
                current = successor[current]
                if current == start:
                    break
            faces.append(face)
        if len(vertices)-len(edges)+len(faces) == 2:
            return {'clockwise_rotation': [[v, rotation[v]] for v in vertices], 'all_faces': sorted(faces), 'euler_characteristic': 2}
    raise ValueError('control has no spherical rotation')


def certificate():
    patches = [patch('C7', 7), patch('theta_1_4_5_rotated', 9, (0, 4), 4)]
    controls = [control(p, exterior(cross)) for p in patches for cross in (True, False)]
    return {'schema': 'seven-disk-exterior-v1', 'base': '120aae90cab8bc4881916adc598cf344f2f20f4b',
            'paper_scope': 'M1-M5 are arbitrary-size paper proofs; these are finite algebra controls only',
            'registry': {'all_ordinary_cells': 1206, 'all_tight_cells': 560,
                         'universally_empty_tight_cells': 140, 'effective_ordinary_tight_bound': 420,
                         'eligible_even111_internal_bound': 140}, 'support_calibration': support_calibration(), 'patches': patches, 'controls': controls}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('matching_certificate-v3.json'))
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    RNG.seed(args.seed)
    expected = certificate()
    if args.write:
        with args.certificate.open('x') as stream:
            json.dump(expected, stream, indent=2)
            stream.write('\n')
    else:
        require(json.loads(args.certificate.read_text()) == json.loads(json.dumps(expected)), 'complete certificate exact replay')
    print(json.dumps({'status': 'PASS', 'seed': args.seed,
                      'controls': [{'name': c['name'], **c['summary']} for c in expected['controls']]}, sort_keys=True))


if __name__ == '__main__':
    main()
