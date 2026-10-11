#!/usr/bin/env python3
"""Independent fixed N2 controls: mixed join -> actual C -> C/U -> X/G.

Standard library only. No research-checker imports, graph search, normalization,
or source-exclusion oracle. --check performs no filesystem writes.
"""
import argparse
from collections import Counter, defaultdict
import gzip
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
LITERALS = ('01012', '01021', '01023', '01201', '01202',
            '01203', '01212', '01213', '01231', '01232')
ROWS = tuple(tuple(map(int, s)) for s in LITERALS)
COL = set(range(4))
PINS = tuple(product(range(4), repeat=2))
PRIOR = 'audits/2026-10-10-n45-s-long-contract/certificate-v2.json'


def need(test, message):
    if not test:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()


def adjacency(vs, es):
    a = {v: set() for v in vs}
    for u, v in es:
        need(u in a and v in a and u != v, 'invalid original edge')
        a[u].add(v)
        a[v].add(u)
    return a


def components(vs, es):
    vset = set(vs)
    a = adjacency(vs, [e for e in es if set(e) <= vset])
    left, result = set(vs), []
    while left:
        todo, seen = [min(left)], set()
        while todo:
            v = todo.pop()
            if v not in seen:
                seen.add(v)
                todo.extend(a[v] - seen)
        left -= seen
        result.append(sorted(seen))
    return result


def assignments(vs, es, pins, direct=False):
    """Complete enumeration. Direct graph path uses fixed vertex order;
    local piece path uses MRV. Both retain all labelled colours and solutions.
    """
    a, f, out = adjacency(vs, es), dict(pins), []
    need(set(f) <= set(vs), 'pin outside actual vertex domain')
    if any(f[u] == f[v] for u, v in es if u in f and v in f):
        return []

    def visit():
        left = [v for v in vs if v not in f]
        if not left:
            out.append(tuple(f[v] for v in vs))
            return
        domains = {v: sorted(COL - {f[w] for w in a[v] if w in f}) for v in left}
        v = left[0] if direct else min(left, key=lambda w: (len(domains[w]), -len(a[w]), w))
        for c in domains[v]:
            f[v] = c
            visit()
            del f[v]

    visit()
    return sorted(out)


def local(vs, es, gamma, direct=False):
    domain = list(range(5)) + vs
    chosen = [e for e in es if set(e) <= set(domain)]
    return [f[5:] for f in assignments(domain, chosen, dict(enumerate(gamma)), direct)]


def relation(vs, contacts, lifts):
    grouped = defaultdict(list)
    for i, f in enumerate(lifts):
        grouped[tuple(f[vs.index(v)] for v in contacts)].append(i)
    return [{'tuple': list(t), 'assignment_indices': grouped[t]} for t in sorted(grouped)]


def forbidden(rel):
    need(bool(rel), 'empty unpinned local relation: covering intersection undefined')
    return sorted(set.intersection(*(set(cell['tuple']) for cell in rel)))


def bridges(vs, es):
    return [list(e) for e in es if len(components(vs, [f for f in es if f != e])) > 1]


def freeze_check():
    manifest = json.loads((HERE / 'inputs.json').read_bytes())
    need(manifest['base'] == BASE, 'task BASE changed')
    frozen = {}
    for item in manifest['inputs']:
        data = (HERE / item['frozen_path']).read_bytes()
        need(len(data) == item['bytes'] and sha256(data).hexdigest() == item['sha256'],
             'frozen input drift: ' + item['path'])
        need((ROOT / item['path']).read_bytes() == data, 'live old input drift: ' + item['path'])
        if item['authority'] == 'BASE Git blob':
            ref = BASE + ':' + item['path']
            blob = subprocess.check_output(['git', 'rev-parse', ref], cwd=ROOT, text=True).strip()
            need(blob == item['git_blob'], 'BASE blob identity changed')
            need(subprocess.check_output(['git', 'show', ref], cwd=ROOT) == data,
                 'frozen input differs from BASE Git bytes')
        else:
            need(item['authority'] == 'BASE archive payload' and item['git_blob'] is None,
                 'unrecognized input authority')
            packed_path = item['archive_blob_path']
            packed = subprocess.check_output(['git', 'show', BASE + ':' + packed_path], cwd=ROOT)
            need(sha256(packed).hexdigest() == item['archive_compressed_sha256'] and
                 gzip.decompress(packed) == data, 'BASE archived payload differs')
            need(subprocess.check_output(['git', 'rev-parse', BASE + ':' + packed_path],
                 cwd=ROOT, text=True).strip() == item['archive_git_blob'], 'archive Git blob differs')
        frozen[item['path']] = data
    archive = json.loads(frozen['audits/ARCHIVE.json'])
    need(archive['files'][PRIOR]['sha256'] == sha256(frozen[PRIOR]).hexdigest(),
         'BASE archive manifest differs')
    controls = sorted(p for p in frozen if p.startswith('artifacts/c5_excess_two_e4c/controls/'))
    need(len(controls) == 19, 'fixed control inventory changed')
    actual = {str(p.relative_to(HERE / 'frozen')) for p in
              (HERE / 'frozen/artifacts/c5_excess_two_e4c/controls').glob('*.json')}
    need(actual == set(controls), 'undeclared or missing fixed control')
    return frozen, controls


def reconstruct(raw, original):
    vs = raw['vertices']
    es = [tuple(e) for e in original['canonical_edges']]
    need(vs == list(range(max(v for e in es for v in e) + 1)) and
         raw['edges'] == original['canonical_edges'], 'original vertices/edges disagree')
    need(all(u < v for u, v in es) and len(set(es)) == len(es), 'not finite simple labelled graph')
    need({e for e in es if max(e) < 5} == {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)},
         'boundary is not literal induced C5')
    a = adjacency(vs, es)
    isolated = [v for v in vs if v >= 5 and not a[v]]
    effective = [v for v in vs if v >= 5 and a[v]]
    roots = sorted(v for v in effective if len(a[v]) == 5)
    need(len(roots) == 2 and roots[1] not in a[roots[0]], 'original nonadjacent roots disagree')
    need(all(len(a[v]) == 4 for v in effective if v not in roots), 'original complete degrees disagree')
    pcs = components([v for v in effective if v not in roots], es)
    pieces = []
    for pv in pcs:
        old = next(p for p in raw['pieces'] if p['vertices'] == pv)
        contacts = {str(w): sorted(a[w] & set(pv)) for w in roots}
        owners = [w for w in roots if contacts[str(w)]]
        attach = [list(e) for e in es if min(e) < 5 and max(e) in pv]
        support = sorted({min(e) for e in attach})
        internal = [e for e in es if set(e) <= set(pv)]
        order = old['contact_order']
        need(old['contacts'] == contacts and old['owners'] == owners and
             old['attachments'] == attach and old['internal_edges'] == [list(e) for e in internal]
             and old['support'] == support, 'original piece reconstruction mismatch')
        need(len(order) == len(set(order)) and set(order) == set().union(*map(set, contacts.values())),
             'ordered/shared contact coordinate mismatch')
        short = any(set(support) <= {i, (i + 1) % 5} for i in range(5))
        need(bool(support) and short == old['short'], 'actual support classification differs')
        pieces.append({'id': old['id'], 'vertices': pv, 'contacts': contacts,
                       'contact_order': order, 'owners': owners, 'attachments': attach,
                       'support': support, 'internal_edges': [list(e) for e in internal],
                       'bridges': bridges(pv, internal), 'short': short,
                       'short_support_type': ('singleton' if len(support) == 1 else 'true boundary pair')
                       if short else None,
                       'rotation_topology_verified': False, 'one_sided_verified': False})
    unary = [p for p in pieces if len(p['owners']) == 1]
    mixed = [p for p in pieces if len(p['owners']) == 2]
    need(len(pieces) == 3 and len(unary) == 1 and len(mixed) == 2,
         'fixed controls are not unary/two-mixed inventory')
    s = unary[0]['owners'][0]
    r = next(w for w in roots if w != s)
    need(raw['rotation'] == original['embedding']['disk_rotation'], 'stored original rotations differ')
    return vs, es, a, roots, r, s, pieces, unary[0], mixed, isolated


def private_witnesses(vs, xe, gamma, s, C, U, c_order, u_order, fc, fu):
    """Called only for an actually rejecting row; no synthetic triggers."""
    boundary = dict(enumerate(gamma))
    witnesses = []
    for e in xe:
        if max(e) < 5:
            continue
        full = assignments(vs, [f for f in xe if f != e], boundary, direct=True)
        witnesses.append({'edge': list(e), 'witness': list(full[0]) if full else None})
    minimal = all(w['witness'] is not None for w in witnesses)
    evidence = []
    if minimal:
        for w in witnesses:
            if s not in w['edge']:
                continue
            v = next(v for v in w['edge'] if v != s)
            f = dict(zip(vs, w['witness']))
            colour = f[s]
            need(colour == f[v], 'deleted incidence witness does not force its original endpoint colour')
            if v < 5:
                need(colour not in set(fc) | set(fu), 'spoke witness lacks private colour')
                owner = 'spoke'
            elif v in C:
                need(colour in set(fc) - set(fu) - {gamma[b] for b in adjacency(vs, xe)[s] if b < 5},
                     'C incidence witness lacks private colour')
                need(all(f[w] != colour for w in c_order if w != v) and
                     all(f[w] != colour for w in u_order), 'C witness has extra matching contact')
                owner = 'C'
            else:
                need(v in U and colour in set(fu) - set(fc) -
                     {gamma[b] for b in adjacency(vs, xe)[s] if b < 5}, 'U lacks private colour')
                need(all(f[w] != colour for w in u_order if w != v) and
                     all(f[w] != colour for w in c_order), 'U witness has extra matching contact')
                owner = 'U'
            evidence.append({'edge': w['edge'], 'factor': owner, 'colour': colour,
                             'full_witness': w['witness']})
    return {'status': 'triggered and holds' if minimal else 'not triggered',
            'actual_rejection': True, 'own_edge_minimality_verified': minimal,
            'retained_edge_witnesses': witnesses, 'private_incidence_witnesses': evidence}


def graph_record(raw, original, prior, counts):
    vs, es, adj, roots, r, s, pieces, unary, mixed, iso = reconstruct(raw, original)
    counts['graphs'] += 1
    counts['original_shared_contact_vertices'] += sum(len(set(p['contacts'][str(r)]) &
                                                         set(p['contacts'][str(s)])) for p in mixed)
    C = sorted([r] + [v for p in mixed for v in p['vertices']])
    U = unary['vertices']
    cp = [v for p in mixed for v in p['contact_order'] if v in adj[s]]
    up = [v for v in unary['contact_order'] if v in adj[s]]
    need(len(cp) == len(set(cp)) and set(cp) == set(C) & adj[s], 'actual C contacts differ')
    need(set(up) == set(U) & adj[s], 'actual U contacts differ')
    ts = len(adj[s] & set(range(5)))
    need(len(cp) + len(up) + ts == 5, 'm_s+n_U+t_s != 5')
    omissions = sorted(adj[r] & set(range(5)))
    need(omissions, 'fixed graph lacks eligible non-owner r spoke')
    counts['graphs_with_one_long_mixed'] += int(sum(not p['short'] for p in mixed) == 1)
    counts['graphs_with_two_short_mixed'] += int(all(p['short'] for p in mixed))
    whole_g = [assignments(vs, es, dict(enumerate(gamma)), direct=True) for gamma in ROWS]
    sigma = sum(1 << i for i, f in enumerate(whole_g) if f)
    need(sigma == raw['sigma'] == original['sigma_mask'], 'direct original Sigma differs')
    # D5 permutes the ten S4-normalized rows; cardinality alone excludes this inventory.
    target_sigma = sigma.bit_count() in ((933).bit_count(), (941).bit_count())
    need(not target_sigma, 'unexpected target Sigma control: re-audit exact D5 transport')
    touch = sorted({v for v in range(5) if any(w >= 5 for w in adj[v])})
    full_touch = touch == list(range(5))
    missing = ['K2: full Sigma is neither 933/941 nor any whole-D5 image',
               'K7/K12: all eligible X accept all ten rows; no rejecting beta-minimal X',
               'K1/K9: rotation bytes retained but disk topology not independently verified',
               'K2/K11: original nonboundary Sigma-critical witnesses not independently verified',
               'K4: original one-sided embedding not independently verified']
    if not full_touch:
        missing.append('K3: original full B-touch fails at ' + str(sorted(set(range(5)) - set(touch))))
    if all(p['short'] for p in mixed):
        missing.append('K5: both original mixed components are short; no long L')
    g = {'id': raw['id'], 'vertices': vs, 'original_edges': [list(e) for e in es],
         'original_root_order': roots, 'root_order': [r, s], 'U_owner': s,
         'whole_root_transport_to_prior': [ [r, s].index(w) for w in roots],
         'pieces': pieces, 'mixed_ids': [p['id'] for p in mixed], 'U_id': unary['id'],
         'C_vertices': C, 'U_vertices': U, 'C_s_contact_order': cp, 'U_s_contact_order': up,
         'isolated_vertices': iso, 'isolated_assignments': [list(x) for x in product(range(4), repeat=len(iso))],
         'original_rotation': original['embedding']['disk_rotation'],
         'source_coverage': {'status': 'not triggered', 'direct_sigma': sigma, 'accepted_row_indices':
                           [i for i, f in enumerate(whole_g) if f], 'whole_D5_target': False,
                           'B_touch': touch, 'full_B_touch': full_touch,
                           'effective_H_connected': len(components([v for v in vs if v >= 5 and v not in iso], es)) == 1,
                           'epsilon': sum(len(adj[v]) - 4 for v in vs if v >= 5 and v not in iso),
                           'complete_degrees': {str(v): len(adj[v]) for v in vs if v >= 5},
                           'missing_or_unverified_premises': missing}, 'cases': []}
    for h in omissions:
        e = tuple(sorted((r, h)))
        xe = [f for f in es if f != e]
        xa = adjacency(vs, xe)
        need(components([v for v in vs if v >= 5 and v not in iso and v != s], xe) ==
             sorted([C, U], key=lambda p: p[0]), 'H_X-s actual components differ from C/U')
        need(len(xa[r]) == 4 and len(xa[s]) == 5 and all(len(xa[v]) == 4 for v in C + U),
             'actual X complete degrees differ')
        counts['eligible_cases'] += 1
        counts['cases_t_s_' + str(ts)] += 1
        counts['r_first_in_prior' if roots[0] == r else 'r_second_in_prior'] += 1
        case = {'omitted_edge': list(e), 'X_edges': [list(f) for f in xe],
                'retained_r_spokes': sorted(xa[r] & set(range(5))),
                'retained_s_spokes': sorted(xa[s] & set(range(5))),
                'm_s': len(cp), 'n_U': len(up), 't_s': ts,
                'X_B_touch': sorted(v for v in range(5) if any(w >= 5 for w in xa[v])), 'rows': []}
        for q, gamma in enumerate(ROWS):
            cc = local(C, xe, gamma, direct=True)
            uu = local(U, xe, gamma, direct=True)
            rc, ru = relation(C, cp, cc), relation(U, up, uu)
            fc, fu = forbidden(rc), forbidden(ru)
            mixed_records = []
            for p in mixed:
                mm = local(p['vertices'], es, gamma)
                rr = relation(p['vertices'], p['contact_order'], mm)
                saved_piece = next(z for z in prior['pieces'] if z['vertices'] == p['vertices'])
                expected = [{'tuple': z['tuple'], 'lifts': [list(mm[i]) for i in z['assignment_indices']]} for z in rr]
                need(expected == saved_piece['rows'][q]['tuples'], 'mixed full relation differs from prior')
                by_r = [{'r_colour': a, 'assignment_indices': [i for i, f in enumerate(mm) if
                        all(f[p['vertices'].index(v)] != a for v in p['contacts'][str(r)])]} for a in range(4)]
                local_pins = [{'pins_r_s': [a, b], 'assignment_indices': [i for i, f in enumerate(mm) if
                              all(f[p['vertices'].index(v)] != a for v in p['contacts'][str(r)]) and
                              all(f[p['vertices'].index(v)] != b for v in p['contacts'][str(s)])]}
                              for a, b in PINS]
                mixed_records.append({'id': p['id'], 'vertices': p['vertices'], 'assignments':
                                      [list(f) for f in mm], 'relation': rr, 'all_r_fibres': by_r,
                                      'all_16_original_root_pin_fibres': local_pins})
            joined, provenance = [], []
            for a in range(4):
                if a in {gamma[v] for v in xa[r] if v < 5}:
                    continue
                for i, j in product(mixed_records[0]['all_r_fibres'][a]['assignment_indices'],
                                    mixed_records[1]['all_r_fibres'][a]['assignment_indices']):
                    f = {r: a}
                    for rec, idx in zip(mixed_records, (i, j)):
                        f.update(zip(rec['vertices'], rec['assignments'][idx]))
                    joined.append(tuple(f[v] for v in C))
                    provenance.append((tuple(f[v] for v in C), [a, i, j]))
            need(sorted(joined) == cc, 'original mixed same-r join differs from direct complete C')
            ci = {f: i for i, f in enumerate(cc)}
            join_indices = [None] * len(cc)
            for f, origin in provenance:
                need(join_indices[ci[f]] is None, 'duplicate natural-join C assignment')
                join_indices[ci[f]] = origin
            urel = relation(U, unary['contact_order'], uu)
            saved_u = next(z for z in prior['pieces'] if z['vertices'] == U)
            need([{'tuple': z['tuple'], 'lifts': [list(uu[i]) for i in z['assignment_indices']]} for z in urel]
                 == saved_u['rows'][q]['tuples'], 'complete U relation differs from prior')
            grouped = defaultdict(list)
            for i, f in enumerate(cc):
                grouped[(f[C.index(r)], tuple(f[C.index(v)] for v in cp))].append(i)
            ambient = [{'r_colour': a, 'C_contact_tuple': list(t), 'C_assignment_indices': grouped[(a, t)]}
                       for a in range(4) for t in product(range(4), repeat=len(cp))]
            ugrouped = defaultdict(list)
            for i, f in enumerate(uu):
                ugrouped[tuple(f[U.index(v)] for v in up)].append(i)
            uambient = [{'U_contact_tuple': list(t), 'U_assignment_indices': ugrouped[t]}
                        for t in product(range(4), repeat=len(up))]
            counts['ambient_C_fibres'] += len(ambient)
            counts['empty_ambient_C_fibres'] += sum(not z['C_assignment_indices'] for z in ambient)
            counts['ambient_U_fibres'] += len(uambient)
            counts['empty_ambient_U_fibres'] += sum(not z['U_assignment_indices'] for z in uambient)
            xx = assignments(vs, xe, dict(enumerate(gamma)), direct=True)
            gg = whole_g[q]
            spoke_colours = sorted({gamma[v] for v in xa[s] if v < 5})
            covered = set(fc) | set(fu) | set(spoke_colours) == COL
            need(covered == (not xx), 'true F_C/F_U/spokes covering differs from direct rejection')
            cells = []
            for a, b in PINS:
                indices, full = [], []
                for i, f in enumerate(cc):
                    if f[C.index(r)] != a or any(f[C.index(v)] == b for v in cp):
                        continue
                    for j, u in enumerate(uu):
                        if b in spoke_colours or any(u[U.index(v)] == b for v in up):
                            continue
                        for k, z in enumerate(g['isolated_assignments']):
                            assignment = dict(enumerate(gamma)) | {s: b} | dict(zip(C, f)) | dict(zip(U, u)) | dict(zip(iso, z))
                            need(all(assignment[v] != assignment[w] for v, w in xe), 'assembled X violates edge')
                            full.append(tuple(assignment[v] for v in vs))
                            indices.append([i, j, k])
                dx = sorted(f for f in xx if (f[vs.index(r)], f[vs.index(s)]) == (a, b))
                dg = sorted(f for f in gg if (f[vs.index(r)], f[vs.index(s)]) == (a, b))
                need(sorted(full) == dx, 'C/U joint differs from direct X full lifts')
                restored = dx if a != gamma[h] else []
                need(restored == dg, 'per-pin original G restoration equation differs')
                oldpin = [dict(zip((r, s), (a, b)))[w] for w in roots]
                prior_row = prior['rows'][q]
                oldx = next(z for z in prior_row['spoke_omissions'] if z['edge'] == list(e))
                need([list(f) for f in dx] == next(z['full_lifts'] for z in oldx['all_16_fibres'] if z['pins'] == oldpin),
                     'whole ordered root transport to prior X differs')
                need([list(f) for f in dg] == next(z['full_lifts'] for z in prior_row['G_all_16_fibres'] if z['pins'] == oldpin),
                     'whole ordered root transport to prior G differs')
                cells.append({'pins_r_s': [a, b], 'prior_pins': oldpin, 'X_lift_indices_C_U_isolated': indices,
                              'G_lift_indices_C_U_isolated': indices if a != gamma[h] else []})
                counts['root_pin_cells'] += 1
                counts['empty_X_root_pin_cells'] += int(not dx)
                counts['restoration_pin_checks'] += 1
                counts['prior_X_G_full_lift_comparisons'] += 2
            new = bool(xx) and not gg
            if new:
                need({f[vs.index(r)] for f in xx} == {gamma[h]}, 'all new X lifts fail omitted-spoke forcing')
                counts['new_accepted_rows'] += 1
            if not xx:
                private = private_witnesses(vs, xe, gamma, s, C, U, cp, up, fc, fu)
                counts['actual_rejected_X_rows'] += 1
                counts['private_cover_triggers'] += int(private['status'] == 'triggered and holds')
            else:
                private = {'status': 'not triggered', 'actual_rejection': False,
                           'own_edge_minimality_verified': False, 'minimal_witnesses_execution':
                           'not executed: direct X accepts this row', 'retained_edge_witnesses': []}
            case['rows'].append({'index': q, 'literal': LITERALS[q], 'mixed': mixed_records,
                                 'C_assignments': [list(f) for f in cc], 'C_from_mixed_indices': join_indices,
                                 'U_assignments': [list(f) for f in uu], 'R_C': rc, 'R_U': ru,
                                 'all_ambient_C_r_tuple_fibres': ambient, 'all_ambient_U_tuple_fibres': uambient,
                                 'F_C': fc, 'F_U': fu,
                                 's_spoke_colours': spoke_colours, 'cover_equals_rejection': True,
                                 'cover_all_four': covered, 'all_16_root_pin_cells': cells,
                                 'restoration_colour': gamma[h], 'new_accepted_row': new,
                                 'private_cover': private})
            counts['literal_rows'] += 1
            counts['C_assignments'] += len(cc)
            counts['U_assignments'] += len(uu)
            counts['mixed_to_C_full_assignment_checks'] += 1
            counts['covering_equivalence_checks'] += 1
        case['X_sigma'] = sum(1 << row['index'] for row in case['rows'] if
                             any(c['X_lift_indices_C_U_isolated'] for c in row['all_16_root_pin_cells']))
        need(case['X_sigma'] == 1023, 'unexpected rejected X source: fixed calibration scope changed')
        g['cases'].append(case)
    return g


def audit():
    frozen, controls = freeze_check()
    old = {g['id']: g for g in json.loads(frozen[PRIOR])['graphs']}
    counts = Counter({k: 0 for k in ('cases_t_s_0', 'cases_t_s_1', 'cases_t_s_2',
                                    'actual_rejected_X_rows', 'private_cover_triggers', 'target_source_triggers')})
    graphs = []
    for p in controls:
        raw = json.loads(frozen[p])
        source = frozen[raw['source']]
        need(sha256(source).hexdigest() == raw['source_sha256'], 'original source digest differs')
        graphs.append(graph_record(raw, json.loads(source), old[raw['id']], counts))
    need(counts['graphs'] == 19 and counts['eligible_cases'] == 21 and counts['literal_rows'] == 210 and
         counts['root_pin_cells'] == 3360, 'fixed eligible coverage incomplete')
    return {'task_id': 'N45-S-LONG-S-JOINT', 'base': BASE, 'schema': 1,
            'fixed_inputs_count': len(frozen), 'literal_rows': list(LITERALS), 'ordered_pins': [list(p) for p in PINS],
            'lift_reconstruction': 'For each cell [ci,ui,zi], union literal B, s=b, C[ci], U[ui], isolated[zi] in graph.vertices order. C contains r=a. Every index combination is stored; no lift multiplicity is discarded.',
            'finite_interface': {'status': 'triggered and holds', 'counts': dict(sorted(counts.items()))},
            'target_source': {'status': 'not triggered', 'finite_target_source_triggers': 0,
                              'scope': 'Only these 19 controls; no satisfying target source established or executed',
                              'source_exclusion': 'not established', 'source_realizability': 'not established'},
            'private_cover': {'status': 'not triggered', 'triggers': counts['private_cover_triggers']},
            'new_Lean_theorem': False, 'independent_acceptance': 'pending', 'graphs': graphs}


def first_difference(a, b, path='certificate'):
    if type(a) is not type(b):
        return path + ': type differs'
    if isinstance(a, dict):
        if set(a) != set(b):
            return path + ': keys differ'
        for k in sorted(a):
            d = first_difference(a[k], b[k], path + '.' + k)
            if d:
                return d
    elif isinstance(a, list):
        if len(a) != len(b):
            return path + ': length differs'
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_difference(x, y, path + '[' + str(i) + ']')
            if d:
                return d
    elif a != b:
        return path + ': value differs'
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    need(args.certificate.resolve().is_relative_to(HERE), 'certificate must stay inside exclusive audit directory')
    payload = audit()
    data = encoded(payload)
    if args.check:
        saved = args.certificate.read_bytes()
        if saved != data:
            difference = first_difference(json.loads(saved), payload)
            raise ValueError('certificate rejected: ' + (difference or 'noncanonical bytes'))
    else:
        with args.certificate.open('xb') as f:
            f.write(data)
    print(json.dumps({'certificate_sha256': sha256(data).hexdigest(),
                      'finite_interface': payload['finite_interface'], 'target_source': payload['target_source'],
                      'private_cover': payload['private_cover']}, sort_keys=True))


if __name__ == '__main__':
    main()
