#!/usr/bin/env python3
"""Task B: complete fixed-domain replay, product vs independent MRV.

--write exclusively creates a new certificate. --check is read-only, including
imports. All color vectors use the explicit graph.nodes order, never a local
color normalization. No arbitrary-size source search is performed.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import topology
import independent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n'


def product_lifts(graph, beta):
    nodes = graph['nodes']
    pos = {v: i for i, v in enumerate(nodes)}
    boundary = graph['boundary']
    internal = [v for v in nodes if v not in boundary]
    out = []
    for rest in itertools.product(range(4), repeat=len(internal)):
        assignment = dict(zip(boundary, beta)) | dict(zip(internal, rest))
        colors = [assignment[v] for v in nodes]
        if all(colors[pos[u]] != colors[pos[v]] for u, v in graph['edges']):
            out.append(colors)
    return sorted(out)


def mask(rows):
    return sum(1 << i for i, row in enumerate(rows) if row)


def comparison(old, new):
    a, b = mask(old), mask(new)
    return {'source_sigma': a, 'transformed_sigma': b,
            'classification': ('equal' if a == b else 'strictly smaller' if a & b == b
                               else 'strictly larger' if a & b == a else 'incomparable'),
            'lost_rows': [i for i in range(10) if old[i] and not new[i]],
            'added_rows': [i for i in range(10) if new[i] and not old[i]],
            'difference_witnesses': [
                {'row': i, 'side': 'source' if old[i] else 'transformed',
                 'full_coloring': (old[i] or new[i])[0]}
                for i in range(10) if bool(old[i]) != bool(new[i])]}


def frozen_inputs():
    inputs = json.loads((ROOT / 'INPUTS.json').read_text())
    for entry in inputs['inputs']:
        need(digest(ROOT / entry['frozen']) == entry['sha256'], 'frozen input drift: ' + entry['path'])
    design = json.loads((ROOT / 'DESIGN.json').read_text())
    for path, sha in design['frozen_design'].items():
        need(digest(ROOT / path) == sha, 'frozen design drift: ' + path)
    return inputs, design


def certificate(seed=0):
    inputs, design = frozen_inputs()
    domain = json.loads((HERE / 'domain.json').read_text())
    need(domain == topology.build_domain(), 'fixed source/operation domain differs from reconstruction')
    independent.verify_domain(domain)
    need(domain['counts'] == design['expected'], 'preregistered expected domain counts')
    pats = domain['patterns']
    need(pats == independent.PATTERNS, 'independent canonical pattern order')
    need(len(pats) == 10 and len(domain['sources']) == 133 and len(domain['marks']) == 77,
         'fixed domain cardinalities')
    graphs = {}
    cache = {}
    rng = random.Random(seed)

    def register(name, graph):
        signature = encode({'nodes': graph['nodes'], 'boundary': graph['boundary'], 'edges': graph['edges']})
        geometry = independent.verify_graph(graph)
        if signature not in cache:
            order = list(range(10)); rng.shuffle(order)
            rows = [None] * 10
            for i in order:
                direct = product_lifts(graph, pats[i])
                backtrack = independent.enumerate_lifts(graph, pats[i])
                need(direct == backtrack, 'product/MRV complete lifts mismatch: ' + name + ':' + str(i))
                rows[i] = direct
            cache[signature] = rows
        rows = cache[signature]
        graphs[name] = {'nodes': graph['nodes'], 'boundary': graph['boundary'],
                        'sigma': mask(rows), 'embedding_check': geometry,
                        'rows': [{'index': i, 'beta': p, 'full_lifts': rows[i]} for i, p in enumerate(pats)]}
        return rows

    sources = {s['id']: s for s in domain['sources']}
    source_rows = {}
    for sid, s in sources.items():
        source_rows[sid] = register(sid, s['graph'])
        if s.get('catalogue_sigma') is not None:
            need(mask(source_rows[sid]) == s['catalogue_sigma'], 'literal catalogue sigma differs: ' + sid)

    candidates = {k: {'triggers': 0, 'holds': 0, 'counterexamples': 0, 'first_counterexample': None}
                  for k in ('D-ANY', 'D-OLD-ALL', 'F-ANY', 'F-OLD-ALL', 'Q-ANY',
                            'Q-PAIR-CENTER', 'Q-SEPARATE-JOIN',
                            'D-EXACT', 'F-EXACT', 'Q-EXACT', 'F-SOUND', 'Q-SOUND')}

    def trial(name, premise, conclusion, witness):
        if not premise:
            return
        c = candidates[name]; c['triggers'] += 1
        c['holds' if conclusion else 'counterexamples'] += 1
        if not conclusion and c['first_counterexample'] is None:
            c['first_counterexample'] = witness

    marks = []
    counts = Counter()
    for mark in domain['marks']:
        mid, sid, v, link = mark['id'], mark['source_id'], mark['v'], mark['L']
        original_graph = sources[sid]['graph']
        source = source_rows[sid]
        source_pos = {w: i for i, w in enumerate(original_graph['nodes'])}
        rest_graph = mark['deleted_center_graph']
        rest = register(mid + '/G-v', rest_graph)
        rest_pos = {w: i for i, w in enumerate(rest_graph['nodes'])}
        star_rows = []
        for i, beta in enumerate(pats):
            fibres = {}
            restored = []
            for j, color in enumerate(rest[i]):
                tau = tuple(color[rest_pos[w]] for w in link)
                available = sorted(set(range(4)) - set(tau))
                need(bool(available) == (len(set(tau)) <= 3), 'center criterion')
                fibres.setdefault(tau, []).append(j)
                for a in available:
                    assignment = dict(zip(rest_graph['nodes'], color)) | {v: a}
                    restored.append([assignment[w] for w in original_graph['nodes']])
            need(sorted(restored) == source[i], 'star full-lift reconstruction: ' + mid)
            # A lossless complete relation: all compatible L assignments are in
            # the explicitly defined product domain; absent keys have empty fibre.
            free_link = [w for w in link if w not in range(5)]
            expanded = 0
            for values in itertools.product(range(4), repeat=len(free_link)):
                assignment = dict(zip(range(5), beta)) | dict(zip(free_link, values))
                tau = tuple(assignment[w] for w in link)
                indices = fibres.get(tau, [])
                need(indices == [j for j, c in enumerate(rest[i])
                                 if tuple(c[rest_pos[w]] for w in link) == tau], 'full interface fibre')
                expanded += 1
            star_rows.append({'index': i, 'beta': beta,
                              'interface_fibre_domain_size': expanded,
                              'nonempty_fibres': [{'L_colors': list(t), 'G_minus_v_lift_indices': ids,
                                                   'center_colors': sorted(set(range(4)) - set(t))}
                                                  for t, ids in sorted(fibres.items())]})
        ops = []
        for op in mark['operations']:
            independent.verify_operation(original_graph, mark, op)
            if op['kind'] == 'quotient':
                independent.verify_graph(op['surgery']['augmented_graph'])
            oid, kind = op['id'], op['kind']
            target = register(oid, op['graph'])
            cmp = comparison(source, target)
            eq = cmp['classification'] == 'equal'
            counts[kind + '/' + cmp['classification']] += 1
            info = {'id': oid, 'kind': kind, 'graph_ref': oid, 'comparison': cmp, 'rows': []}
            premise_any = False
            old_all = True
            sound = True
            exact = True
            for i, beta in enumerate(pats):
                row = {'index': i, 'beta': beta}
                if kind in ('delete', 'flip'):
                    dgraph = op['graph'] if kind == 'delete' else {
                        'nodes': original_graph['nodes'], 'boundary': original_graph['boundary'],
                        'edges': [e for e in original_graph['edges'] if set(e) != set(op['spoke'])]}
                    # The common deleted-spoke graph is registered separately
                    # by its deletion operation, whose geometry is already checked.
                    drows = (target if kind == 'delete' else
                             next(graphs[x['id']]['rows'] for x in mark['operations']
                                  if x['kind'] == 'delete' and set(x['spoke']) == set(op['spoke'])))
                    drow = drows[i] if kind == 'delete' else drows[i]['full_lifts']
                    pos = {w: j for j, w in enumerate(dgraph['nodes'])}
                    a, b = op['spoke']
                    aflags = [c[pos[a]] != c[pos[b]] for c in drow]
                    fflags = ([True] * len(drow) if kind == 'delete' else
                              [c[pos[op['diagonal'][0]]] != c[pos[op['diagonal'][1]]] for c in drow])
                    need([c for c, flag in zip(drow, aflags) if flag] == source[i], 'original A reconstruction')
                    need([c for c, flag in zip(drow, fflags) if flag] == target[i], 'transformed F reconstruction')
                    retained = [bool(c in target[i]) for c in source[i]]
                    row.update({'common_deleted_spoke_lifts': drow, 'original_spoke_inequality_A': aflags,
                                'new_diagonal_inequality_F': fflags,
                                'joint_condition_fibres': {
                                    str(int(a)) + str(int(f)): [j for j, (x, y) in enumerate(zip(aflags, fflags))
                                                               if x == a and y == f]
                                    for a in (False, True) for f in (False, True)},
                                'all_old_lifts_retained': all(retained), 'old_lift_retention': retained})
                    common = any(a and f for a, f in zip(aflags, fflags))
                    premise_any |= common
                    old_all &= all(retained)
                    sound &= (not source[i] or common) and all(not f or a for a, f in zip(aflags, fflags))
                    exact &= bool(any(aflags)) == bool(any(fflags))
                elif kind == 'quotient':
                    partition = op['partition']
                    mapping = {int(k): w for k, w in op['vertex_map'].items()}
                    tpos = {w: j for j, w in enumerate(op['graph']['nodes'])}
                    eqflags = [all(len({c[rest_pos[w]] for w in block}) == 1 for block in partition)
                               for c in rest[i]]
                    centers = [sorted(set(range(4)) - {c[rest_pos[w]] for w in link}) for c in rest[i]]
                    pulled = sorted([[c[tpos[mapping[w]]] for w in rest_graph['nodes']] for c in target[i]])
                    need(pulled == [c for c, flag in zip(rest[i], eqflags) if flag], 'quotient two-way full lifts')
                    retained = [all(len({c[source_pos[w]] for w in block}) == 1 for block in partition)
                                for c in source[i]]
                    row.update({'G_minus_v_equality_flags': eqflags, 'center_colors_by_rest_lift': centers,
                                'quotient_pullback_full_lifts': pulled,
                                'all_old_lifts_retained': all(retained), 'old_lift_retention': retained})
                    common = any(e and bool(a) for e, a in zip(eqflags, centers))
                    premise_any |= common
                    old_all &= all(retained)
                    sound &= (not source[i] or common) and all(not e or bool(a) for e, a in zip(eqflags, centers))
                    exact &= bool(source[i]) == bool(any(eqflags))
                    constraints = sorted((min(block), w) for block in partition
                                         for w in sorted(block) if w != min(block))
                    if len(constraints) == 1:
                        for j, (e, a) in enumerate(zip(eqflags, centers)):
                            trial('Q-PAIR-CENTER', e, bool(a),
                                  {'mark': mid, 'operation': oid, 'row': i,
                                   'G_minus_v_full_coloring': rest[i][j],
                                   'L_colors': [rest[i][j][rest_pos[w]] for w in link]})
                    if len(constraints) >= 2:
                        separate = [next((j for j, c in enumerate(rest[i]) if c[rest_pos[a]] == c[rest_pos[b]]), None)
                                    for a, b in constraints]
                        trial('Q-SEPARATE-JOIN', all(j is not None for j in separate), any(eqflags),
                              {'mark': mid, 'operation': oid, 'row': i, 'constraints': constraints,
                               'separate_rest_lift_indices': separate})
                else:
                    raise ValueError('unknown operation kind: ' + kind)
                info['rows'].append(row)
            witness = {'mark': mid, 'operation': oid, 'comparison': cmp}
            if kind == 'delete':
                trial('D-ANY', premise_any, eq, witness)
                trial('D-OLD-ALL', old_all, eq, witness)
                trial('D-EXACT', exact, eq, witness)
            if kind == 'flip':
                trial('F-ANY', premise_any, eq, witness)
                trial('F-OLD-ALL', old_all, eq, witness)
                trial('F-EXACT', exact, eq, witness)
                trial('F-SOUND', sound, eq, witness)
            if kind == 'quotient':
                trial('Q-ANY', premise_any, eq, witness)
                trial('Q-EXACT', exact, eq, witness)
                trial('Q-SOUND', sound, eq, witness)
            need(exact == eq, 'exact ten-row iff differs from relation comparison')
            info['conditions'] = {'some_common_full_lift': premise_any, 'all_old_lifts_retained_all_rows': old_all,
                                  'exact_ten_row_condition': exact, 'sound_lift_condition': sound}
            ops.append(info)
        marks.append({'id': mid, 'source_ref': sid, 'v': v, 'L': link, 'G_minus_v_ref': mid + '/G-v',
                      'complete_fibre_encoding': {'ordered_B': list(range(5)), 'ordered_L': link,
                       'free_L_vertices': [w for w in link if w not in range(5)],
                       'domain': 'all 4^5 ordered L assignments; shared B identities are fixed by beta',
                       'total_ordered_L_domain_size': 1024,
                       'shared_B_L_inconsistent_assignments_have_empty_fibre': True,
                       'default_fibre_for_unlisted_L_assignment': [],
                       'lift_index_target': 'same-row G_minus_v_ref full_lifts'},
                      'rows': star_rows, 'operations': ops})
    for name, result in candidates.items():
        result['status'] = ('counterexample' if result['counterexamples'] else
                            'triggered and holds' if result['triggers'] else 'not triggered')
    need(all(candidates[k]['counterexamples'] == 0 for k in ('D-EXACT','F-EXACT','Q-EXACT','F-SOUND','Q-SOUND')),
         'paper sound condition counterexample')
    return {'schema': 'degree5-star-B-complete-v2', 'base': inputs['base'],
            'input_manifest_sha256': digest(ROOT / 'INPUTS.json'), 'design_sha256': digest(ROOT / 'DESIGN.json'),
            'domain': domain, 'graphs': graphs, 'marks': marks,
            'summary': {'operation_classifications': dict(sorted(counts.items())), 'candidates': candidates,
                        'unique_literal_graphs_colored_twice': len(cache), 'graph_records': len(graphs),
                        'graph_boundary_rows': 10 * len(graphs), 'marked_star_rows': 10 * len(marks),
                        'star_full_lift_identity': {'status': 'triggered and holds', 'rows': 10 * len(marks)},
                        'operation_full_lift_identities': {'status': 'triggered and holds',
                                                          'rows': 10 * sum(counts.values())},
                        'outside_933_941_source': {'status': 'not triggered', 'realized_sources': 0},
                        'Lean': 'not run; no new theorem', 'universal_reducibility': 'OPEN'}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', type=Path)
    mode.add_argument('--check', type=Path)
    p.add_argument('--seed', type=int, default=0)
    args = p.parse_args()
    if args.write:
        target = args.write.resolve()
        need(target.parent == HERE, 'write target must be directly in exclusive controls directory')
        need(not target.exists(), 'exclusive certificate already exists')
    actual = certificate(args.seed)
    if args.write:
        with target.open('x') as f:
            f.write(encode(actual))
        print('PASS exclusive certificate:', target)
    else:
        expected = json.loads(args.check.read_text())
        need(actual == expected, 'complete certificate differs from independent reconstruction')
        print('PASS read-only full replay:', args.check)
    print(json.dumps(actual['summary'], ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, FileExistsError, KeyError, TypeError) as e:
        print('FAIL:', e, file=sys.stderr)
        raise SystemExit(1)
