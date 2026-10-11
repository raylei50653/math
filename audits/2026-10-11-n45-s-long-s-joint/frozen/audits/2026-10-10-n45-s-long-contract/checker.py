#!/usr/bin/env python3
"""Fixed N2 relation/lift calibration for a retained-U spoke contract.

No source search, no source validator, no imports from research checkers.
All solutions are enumerated on supplied original edges; --check is read-only.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
COL = frozenset(range(4))
ROWS = tuple(tuple(map(int, s)) for s in (
    '01012', '01021', '01023', '01201', '01202',
    '01203', '01212', '01213', '01231', '01232'))
PAIRS = tuple(product(range(4), repeat=2))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def adjacency(vertices, edges):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def solutions(vertices, edges, pins):
    """Complete deterministic MRV backtracking, without interface assumptions."""
    adj, f, out = adjacency(vertices, edges), dict(pins), []
    if any(f[u] == f[v] for u, v in edges if u in f and v in f):
        return []

    def visit():
        if len(f) == len(vertices):
            out.append(tuple(f[v] for v in vertices))
            return
        choices = []
        for v in vertices:
            if v not in f:
                opts = sorted(COL - {f[w] for w in adj[v] if w in f})
                choices.append((len(opts), -len(adj[v]), v, opts))
        _, _, v, opts = min(choices)
        for c in opts:
            f[v] = c
            visit()
            del f[v]

    visit()
    return sorted(out)


def components(vertices, edges):
    adj = adjacency(vertices, [e for e in edges if set(e) <= set(vertices)])
    remaining, out = set(vertices), []
    while remaining:
        todo, found = [min(remaining)], set()
        while todo:
            v = todo.pop()
            if v in found:
                continue
            found.add(v)
            todo.extend(adj[v] - found)
        remaining -= found
        out.append(sorted(found))
    return out


def fibres(vertices, roots, lifts):
    positions = [vertices.index(r) for r in roots]
    return [{'pins': list(p), 'full_lifts': [list(f) for f in lifts
            if tuple(f[i] for i in positions) == p]} for p in PAIRS]


def inspect_graph(raw, counts):
    vertices = raw['vertices']
    edges = list(map(tuple, raw['edges']))
    adj = adjacency(vertices, edges)
    roots = sorted(v for v in vertices if v >= 5 and len(adj[v]) == 5)
    need(len(roots) == 2 and tuple(roots) not in edges, 'original roots differ')
    pc = components([v for v in vertices if v >= 5 and v not in roots], edges)
    pieces = []
    for vs in pc:
        contacts = {str(r): sorted(set(vs) & adj[r]) for r in roots}
        owners = [r for r in roots if contacts[str(r)]]
        support = sorted({w for v in vs for w in adj[v] if w < 5})
        old = next(p for p in raw['pieces'] if p['vertices'] == vs)
        need(contacts == old['contacts'] and support == old['support']
             and owners == old['owners'], 'original component reconstruction differs')
        order = old['contact_order']
        need(set(order) == set().union(*map(set, contacts.values()))
             and len(order) == len(set(order)), 'shared contact coordinate differs')
        pieces.append({'vertices': vs, 'contacts': contacts, 'contact_order': order,
                       'support': support, 'owners': owners, 'old': old, 'rows': []})
    need(sum(len(p['owners']) == 2 for p in pieces) == 2, 'fixed N2 inventory differs')
    spokes = sorted(e for e in edges if any(r in e and min(e) < 5 for r in roots))
    graphs = []
    for index, gamma in enumerate(ROWS):
        boundary = dict(enumerate(gamma))
        local_options = []
        for p in pieces:
            vs = list(range(5)) + p['vertices']
            es = [e for e in edges if set(e) <= set(vs)]
            lifts = [f[5:] for f in solutions(vs, es, boundary)]
            tuples = sorted({tuple(f[p['vertices'].index(v)] for v in p['contact_order'])
                             for f in lifts})
            record = {'index': index, 'tuples': []}
            for t in tuples:
                matching = [list(f) for f in lifts if tuple(
                    f[p['vertices'].index(v)] for v in p['contact_order']) == t]
                record['tuples'].append({'tuple': list(t), 'lifts': matching})
            need(record['tuples'] == p['old']['rows'][index]['tuples'],
                 'complete local tuples/full lifts differ')
            record['all_16_fibres'] = []
            options = {}
            for a, b in PAIRS:
                pins = dict(zip(roots, (a, b)))
                accepted = [f for f in lifts if all(
                    f[p['vertices'].index(v)] != pins[r]
                    for r in p['owners'] for v in p['contacts'][str(r)])]
                indices = [i for i, t in enumerate(tuples) if all(
                    t[p['contact_order'].index(v)] != pins[r]
                    for r in p['owners'] for v in p['contacts'][str(r)])]
                options[(a, b)] = accepted
                record['all_16_fibres'].append({'pins': [a, b], 'tuple_indices': indices,
                                               'full_lifts': [list(f) for f in accepted]})
            p['rows'].append(record)
            local_options.append(options)
            counts['piece_pin_fibres'] += 16
            counts['piece_rows'] += 1

        def joined(es):
            out = []
            for a, b in PAIRS:
                f = boundary | dict(zip(roots, (a, b)))
                if any(f[u] == f[v] for u, v in es if u in f and v in f):
                    continue
                for assignments in product(*(o[(a, b)] for o in local_options)):
                    assembled = dict(f)
                    for p, lift in zip(pieces, assignments):
                        assembled.update(zip(p['vertices'], lift))
                    need(all(assembled[u] != assembled[v] for u, v in es),
                         'joint full lift violates an original edge')
                    out.append(tuple(assembled[v] for v in vertices))
            return sorted(out)

        original = solutions(vertices, edges, boundary)
        need(original == joined(edges), 'original complete joint/direct lifts differ')
        record = {'index': index, 'literal_gamma': list(gamma),
                  'G_all_16_fibres': fibres(vertices, roots, original), 'spoke_omissions': []}
        counts['G_pin_fibres'] += 16
        for e in spokes:
            r = next(v for v in e if v in roots)
            h = next(v for v in e if v < 5)
            xe = [f for f in edges if f != e]
            xlifts = solutions(vertices, xe, boundary)
            need(xlifts == joined(xe), 'X complete joint/direct lifts differ')
            restored = [f for f in xlifts if f[vertices.index(r)] != gamma[h]]
            need(restored == original, 'spoke restoration differs at full-lift level')
            if not original and xlifts:
                need({f[vertices.index(r)] for f in xlifts} == {gamma[h]},
                     'new-row omitted-spoke forcing differs')
                counts['new_accepted_rows'] += 1
            if not original:
                counts['original_rejected_spoke_queries'] += 1
                need(bool(xlifts), 'unexpected rejecting spoke derivative in fixed domain')
            record['spoke_omissions'].append({
                'edge': list(e), 'descending_root': r, 'vertices': vertices,
                'X_edges': [list(f) for f in xe],
                'all_16_fibres': fibres(vertices, roots, xlifts),
                'restoration_colour': gamma[h]})
            counts['X_pin_fibres'] += 16
        graphs.append(record)
    for p in pieces:
        del p['old']
    counts['graphs'] += 1
    long_count = sum(len(p['owners']) == 2 and not any(
        set(p['support']) <= {i, (i + 1) % 5} for i in range(5)) for p in pieces)
    counts['long_mixed'] += long_count
    sigma = sum(1 << q['index'] for q in graphs
                if any(cell['full_lifts'] for cell in q['G_all_16_fibres']))
    need(sigma == raw['sigma'], 'direct full Sigma differs from saved mask')
    # Whole D5 transport permutes rows and preserves number of accepted rows.
    need(sigma.bit_count() > 7, 'unexpected whole-D5 target mask in fixed inventory')
    touch = sorted({v for v in range(5) if any(w >= 5 for w in adj[v])})
    if long_count:
        need(touch == [0, 1, 2, 3], 'long-control full-B-touch coverage differs')
    counts['shared_contacts'] += sum(len(set(p['contacts'][str(roots[0])]) &
                                        set(p['contacts'][str(roots[1])])) for p in pieces)
    return {'id': raw['id'], 'vertices': vertices, 'edges': raw['edges'],
            'roots': roots, 'rotation': raw['rotation'], 'full_sigma': sigma,
            'original_B_touch': touch, 'pieces': pieces, 'rows': graphs}


def arithmetic():
    masks = {}
    for label, qg in [('941', {0, 1, 3}), ('933', {0, 1, 2, 3})]:
        masks[label] = [list(q) for n in (1, 2) for q in product(range(5), repeat=n)
                        if list(q) == sorted(set(q)) and set(q) <= qg
                        and (n == 1 or (q[1] - q[0]) % 5 in (1, 4))]
    profiles = {}
    for owner in ('r', 's'):
        values = []
        for tr, ts, n, lr, ls, sr, ss in product(range(3), range(3), range(1, 4),
                                              range(1, 5), range(1, 5),
                                              range(1, 5), range(1, 5)):
            if tr == 0 or tr + lr + sr + (n if owner == 'r' else 0) != 5:
                continue
            if ts + ls + ss + (n if owner == 's' else 0) != 5:
                continue
            if (owner == 'r' and ts > 1) or (owner == 's' and tr > 1):
                continue
            values.append({'t_r': tr, 't_s': ts, 'n_U': n,
                           'L': [lr, ls], 'S': [sr, ss]})
        profiles[owner] = values
    # Exhaustive set arithmetic over every nonempty E and two raw columns.
    subsets = [set(c for c in range(4) if mask & (1 << c)) for mask in range(16)]
    count = 0
    for kr, ks in product(range(1, 5), repeat=2):
        m = kr + ks
        for e, l, s in product(subsets[1:], subsets, subsets):
            if len(e) < m or len(l) > kr or len(s) > ks:
                continue
            d_o = len(e) - m
            delta = m - len(l) - len(s)
            overlap = len(l) + len(s) - len(l | s)
            leakage = len((l | s) - e)
            need(d_o + delta + overlap + leakage == len(e - l - s),
                 'all-row cardinality/slack identity differs')
            count += 1
    return {'scope': 'abstract arithmetic only; no graph/source realizability',
            'status': 'triggered and holds', 'nonempty_Q_masks': masks,
            'pair_incidence_profiles': profiles, 'slack_set_cases': count}


def audit():
    manifest = json.loads((HERE / 'inputs.json').read_text())
    counts, results = Counter(), []
    for item in manifest['inputs']:
        path = HERE / 'frozen' / item['path']
        data = path.read_bytes()
        need(sha256(data).hexdigest() == item['sha256'], 'frozen input drift: ' + item['path'])
        blob = subprocess.check_output(['git', 'show', manifest['base'] + ':' + item['path']],
                                       cwd=HERE)
        need(blob == data, 'frozen input does not match BASE Git object')
        if item['path'].startswith('artifacts/c5_excess_two_e4c/controls/'):
            raw = json.loads(data)
            source = (HERE / 'frozen' / raw['source']).read_bytes()
            need(sha256(source).hexdigest() == raw['source_sha256'], 'original source hash differs')
            need(json.loads(source)['canonical_edges'] == raw['edges'], 'original source edges differ')
            results.append(inspect_graph(raw, counts))
    need(counts['graphs'] == 19 and counts['long_mixed'] == 4, 'fixed inventory differs')
    need(counts['original_rejected_spoke_queries'] == 47, 'spoke query coverage differs')
    return {'base': manifest['base'], 'frozen_input_count': len(manifest['inputs']),
            'finite_interface': {'status': 'triggered and holds', 'counts': dict(counts)},
            'selected_source': {'status': 'not triggered', 'missing_sufficient_premises': [
                'all four long/short controls miss original boundary vertex b4 (full B-touch)',
                'no full target Sigma933/941 source in this fixed inventory',
                'no rejecting original-spoke 45/54 beta-minimal derivative']},
            'source_exclusion': 'not established', 'new_Lean_theorem': False,
            'arithmetic': arithmetic(), 'graphs': results}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate-v2.json')
    args = ap.parse_args()
    payload = audit()
    data = encoded(payload)
    if args.check:
        need(args.certificate.read_bytes() == data, 'certificate byte mismatch')
    else:
        with args.certificate.open('xb') as f:
            f.write(data)
    print(json.dumps({'mode': 'check' if args.check else 'generate',
                      'certificate_sha256': sha256(data).hexdigest(),
                      'finite_interface': payload['finite_interface'],
                      'selected_source': payload['selected_source'],
                      'source_exclusion': 'not established'}, sort_keys=True))


if __name__ == '__main__':
    main()
