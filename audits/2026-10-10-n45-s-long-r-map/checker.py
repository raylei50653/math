#!/usr/bin/env python3
"""Read-only fixed-graph check of the actual sole-C/r-fibre mapping.

No theorem oracle or source search. Rebuild from original edges and retain
every C assignment, contact tuple, r colour, and empty ambient fibre.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COL = set(range(4))
ROWS = [tuple(map(int, s)) for s in (
    '01012', '01021', '01023', '01201', '01202',
    '01203', '01212', '01213', '01231', '01232')]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encode(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def adjacency(vs, es):
    adj = {v: set() for v in vs}
    for u, v in es:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def components(vs, es):
    a = adjacency(vs, [e for e in es if set(e) <= set(vs)])
    remaining, result = set(vs), []
    while remaining:
        todo, found = [min(remaining)], set()
        while todo:
            v = todo.pop()
            if v in found:
                continue
            found.add(v)
            todo.extend(a[v] - found)
        remaining -= found
        result.append(sorted(found))
    return result


def colorings(vs, es, pins):
    a, f, result = adjacency(vs, es), dict(pins), []
    if any(f[u] == f[v] for u, v in es if u in f and v in f):
        return []

    def recurse():
        if len(f) == len(vs):
            result.append(tuple(f[v] for v in vs))
            return
        candidates = [(len(opts := sorted(COL - {f[w] for w in a[v] if w in f})),
                       -len(a[v]), v, opts) for v in vs if v not in f]
        _, _, v, opts = min(candidates)
        for c in opts:
            f[v] = c
            recurse()
            del f[v]

    recurse()
    return sorted(result)


def audit():
    manifest = json.loads((HERE / 'inputs.json').read_text())
    for item in manifest['frozen']:
        data = (HERE / 'frozen' / item['path']).read_bytes()
        need(sha256(data).hexdigest() == item['sha256'], 'frozen input drift')
        if item['authority'] == 'BASE Git blob':
            need(data == subprocess.check_output(['git', 'show', manifest['base'] + ':' + item['path']],
                                                 cwd=ROOT), 'BASE blob mismatch')
    prior = ROOT / manifest['prior_certificate']['path']
    need(sha256(prior.read_bytes()).hexdigest() == manifest['prior_certificate']['sha256'],
         'prior complete-lift calibration drift')
    saved = {g['id']: g for g in json.loads(prior.read_text())['graphs']}
    declared_controls = {HERE / 'frozen' / item['path'] for item in manifest['frozen']
                         if item['path'].startswith('artifacts/c5_excess_two_e4c/controls/')}
    actual_controls = set((HERE / 'frozen/artifacts/c5_excess_two_e4c/controls').glob('*.json'))
    need(actual_controls == declared_controls and len(declared_controls) == 19,
         'fixed control inventory differs from manifest')
    counts, profiles, result = Counter(), Counter(), []
    for path in sorted(declared_controls):
        raw = json.loads(path.read_text())
        vs, es = raw['vertices'], list(map(tuple, raw['edges']))
        adj = adjacency(vs, es)
        roots = sorted(v for v in vs if v >= 5 and len(adj[v]) == 5)
        need(len(roots) == 2, 'fixed original root identity differs')
        pcs = components([v for v in vs if v >= 5 and v not in roots], es)
        unary = [p for p in pcs if sum(bool(set(p) & adj[r]) for r in roots) == 1]
        need(len(unary) == 1, 'not the selected fixed U inventory')
        r = next(r for r in roots if set(unary[0]) & adj[r])
        s = next(s for s in roots if s != r)
        C = [v for v in vs if v >= 5 and v != s]
        need(components(C, es) == [C], 'X minus s is not the actual sole C')
        order = [v for p in raw['pieces'] for v in p['contact_order'] if s in adj[v]]
        need(set(order) == adj[s] & set(C) and len(order) == len(set(order)),
             'actual s-contact identity/order differs')
        t_s = len(adj[s] & set(range(5)))
        need(len(order) == 5 - t_s, 's incidence equation differs')
        for h in sorted(adj[r] & set(range(5))):
            edge = tuple(sorted((r, h)))
            xe = [e for e in es if e != edge]
            xa = adjacency(vs, xe)
            need(len(xa[r]) == 4 and len(xa[s]) == 5 and
                 all(len(xa[v]) == 4 for v in C), 'own X complete degrees differ')
            local_vs = list(range(5)) + C
            local_es = [e for e in xe if s not in e]
            rows = []
            for index, gamma in enumerate(ROWS):
                local = colorings(local_vs, local_es, dict(enumerate(gamma)))
                full = colorings(vs, xe, dict(enumerate(gamma)))
                need(bool(local), 'contact-slack complete C relation empty')
                assignments = [f[5:] for f in local]
                tuples = sorted({tuple(f[C.index(v)] for v in order) for f in assignments})
                F = sorted(set.intersection(*(set(t) for t in tuples)))
                ambient = []
                for pin, tau in product(range(4), product(range(4), repeat=len(order))):
                    ambient.append({'r_colour': pin, 's_contact_tuple': list(tau),
                                    'C_lift_indices': [i for i, f in enumerate(assignments)
                                                      if f[C.index(r)] == pin and
                                                      tuple(f[C.index(v)] for v in order) == tau]})
                cells = []
                old = next(x for x in saved[raw['id']]['rows'][index]['spoke_omissions']
                           if tuple(x['edge']) == edge)
                for a, b in product(range(4), repeat=2):
                    found = []
                    if b not in {gamma[v] for v in xa[s] if v < 5}:
                        for lift in assignments:
                            if lift[C.index(r)] == a and all(lift[C.index(v)] != b for v in order):
                                f = dict(enumerate(gamma)) | {s: b} | dict(zip(C, lift))
                                found.append(tuple(f[v] for v in vs))
                    found.sort()
                    direct = [f for f in full if f[vs.index(r)] == a and f[vs.index(s)] == b]
                    need(found == direct, 'C/r-fibre union differs from direct X lifts')
                    pair = [a, b] if roots == [r, s] else [b, a]
                    oldcell = next(c for c in old['all_16_fibres'] if c['pins'] == pair)
                    need([list(f) for f in found] == oldcell['full_lifts'],
                         'prior original-root fibre comparison differs')
                    restored = found if a != gamma[h] else []
                    original = [f for f in colorings(vs, es, dict(enumerate(gamma)))
                                if f[vs.index(r)] == a and f[vs.index(s)] == b]
                    need(restored == original, 'restoration loses r coordinate')
                    cells.append({'r_s_pins': [a, b], 'X_lift_count': len(found),
                                  'G_restored_lift_count': len(restored)})
                if not full:
                    counts['rejecting_X_rows'] += 1
                rows.append({'index': index, 'literal_gamma': list(gamma),
                             'C_assignments': [list(f) for f in assignments],
                             'R_C': [list(t) for t in tuples], 'F_C': F,
                             'all_ambient_r_tuple_fibres': ambient,
                             'all_16_root_pin_fibres': cells})
                counts['rows'] += 1
                counts['root_pin_fibres'] += 16
                counts['ambient_r_tuple_fibres'] += len(ambient)
            result.append({'id': raw['id'], 'r': r, 's': s, 'omitted_edge': list(edge),
                           'C_vertices': C, 'C_internal_edges': [list(e) for e in local_es
                                                               if min(e) >= 5],
                           'ordered_s_contacts': order, 't_s': t_s, 'rows': rows})
            profiles[str(t_s)] += 1
            counts['owner_r_spoke_omissions'] += 1
    need(counts['rejecting_X_rows'] == 0, 'unexpected target rejection in fixed calibration')
    need(counts['owner_r_spoke_omissions'] == 26 and counts['rows'] == 260,
         'fixed omission/row inventory differs')
    return {'base': manifest['base'], 'scope': 'supplied fixed graphs; complete C/r-fibre calibration',
            'counts': dict(counts), 't_s_profile_counts': dict(profiles), 'cases': result,
            'finite_interface': 'triggered and holds',
            'selected_source': {'status': 'not triggered',
                                'missing_sufficient_premises': ['no rejecting X row',
                                                              'no original target Sigma/full-B-touch source']},
            'paper_scope': 'owner-r source exclusion uses the separately stated arbitrary-size proof',
            'new_Lean_theorem': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = ap.parse_args()
    data = audit()
    payload = encode(data)
    if args.check:
        need(args.certificate.read_bytes() == payload, 'certificate byte mismatch')
    else:
        with args.certificate.open('xb') as f:
            f.write(payload)
    print(json.dumps({'counts': data['counts'], 't_s_profile_counts': data['t_s_profile_counts'],
                      'finite_interface': data['finite_interface'], 'source_status': 'not triggered',
                      'certificate_sha256': sha256(payload).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
