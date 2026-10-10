#!/usr/bin/env python3
"""Independent HIGH1 fixed relation and C5 arithmetic calibration, not a source audit."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import stat
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
COLORS = tuple(range(4))
NAMES = ('r', 's', 'p0', 'p1', 'q0', 'u0')
# Read as an explicit graph, then evaluated by Cartesian assignments and factor checks.
C_NAMES = ('r', 'p0', 'p1', 'q0')
C_EDGES = (('r', 'p0'), ('r', 'p1'), ('r', 'q0'), ('p0', 'p1'))
X_EDGES = C_EDGES + (('s', 'p0'), ('s', 'q0'), ('s', 'u0'))
ATT = {'r': (2,), 's': (1, 4), 'p0': (1,), 'p1': (1, 2),
       'q0': (3, 4), 'u0': (4, 0, 1)}
LOST = 3


def encoded(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def need(value, reason):
    if not value:
        raise ValueError(reason)


def inputs():
    index = json.loads((HERE / 'inputs.json').read_bytes())
    need(index['BASE'] == BASE and index['worker_regular_files'] == 94, 'frozen identity')
    need(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                 text=True).strip() == BASE, 'HEAD changed')
    for row in index['worker_files']:
        saved = HERE / 'frozen/worker' / row['path']
        need(saved.is_file() and not saved.is_symlink(), 'frozen worker file kind')
        need(sha(saved.read_bytes()) == row['sha256'], 'frozen worker digest: ' + row['path'])
        live = ROOT / index['worker'] / row['path']
        need(live.is_file() and not live.is_symlink(), 'original worker file kind')
        need(sha(live.read_bytes()) == row['sha256'], 'original worker drift: ' + row['path'])
        need(stat.S_IMODE(live.stat().st_mode) == row['mode'], 'original worker mode drift')
    actual = {p.relative_to(HERE / 'frozen/worker').as_posix()
              for p in (HERE / 'frozen/worker').rglob('*') if p.is_file()}
    need(actual == {r['path'] for r in index['worker_files']}, 'frozen inventory')
    live_files = {p.relative_to(ROOT / index['worker']).as_posix()
                  for p in (ROOT / index['worker']).rglob('*') if p.is_file() or p.is_symlink()}
    need(live_files == actual, 'original worker inventory')
    for rec in index['source_inputs']:
        saved = HERE / 'frozen/worker' / rec['frozen']
        need(sha(saved.read_bytes()) == rec['sha256'], 'source frozen digest')
        if rec['layer'] == 'BASE':
            raw = subprocess.check_output(['git', 'show', BASE + ':' + rec['path']], cwd=ROOT)
            need(sha(raw) == rec['sha256'], 'BASE bytes changed')
            blob = subprocess.check_output(['git', 'rev-parse', BASE + ':' + rec['path']],
                                           cwd=ROOT, text=True).strip()
            need(blob == rec['git_blob'], 'BASE blob changed')
    return index


def factors(names, edges):
    # This direct product algorithm does not use worker search or elimination code.
    answer = []
    for values in itertools.product(COLORS, repeat=len(names)):
        f = dict(zip(names, values))
        if all(f[u] != f[v] for u, v in edges):
            answer.append(values)
    return tuple(answer)


def colored(names, assignments, boundary, attachments):
    return {f for f in assignments
            if all(f[k] != boundary[b] for k, name in enumerate(names)
                   for b in attachments.get(name, ())) }


def boundary_rows():
    return tuple(b for b in itertools.product(COLORS, repeat=5)
                 if all(b[i] != b[(i + 1) % 5] for i in range(5)))


def normal(b):
    names = {}
    for c in b:
        if c not in names:
            names[c] = len(names)
    return tuple(names[c] for c in b)


def relation_control(worker):
    whole_factors = factors(NAMES, X_EDGES)
    free_names = NAMES + ('I',)
    free_factors = factors(free_names, X_EDGES)
    c_factors = factors(C_NAMES, C_EDGES)
    rows = boundary_rows()
    own_records = []
    all_values = {}
    marginal_failures, restore_failures = [], []
    for b in rows:
        cf = colored(C_NAMES, c_factors, b, ATT)
        uf = colored(('u0',), factors(('u0',), ()), b, ATT)
        direct = colored(NAMES, whole_factors, b, ATT)
        att_g = dict(ATT, r=(2, LOST))
        original = colored(NAMES, whole_factors, b, att_g)
        need(colored(free_names, free_factors, b, ATT) ==
             {(*f, d) for f in direct for d in COLORS}, 'full original isolated factor')
        by_join = set()
        queries = []
        for a, c in itertools.product(COLORS, repeat=2):
            c_fibre = {f for f in cf if f[0] == c and f[1] != a and f[3] != a}
            u_fibre = {f for f in uf if f[0] != a}
            query = {(c, a, f[1], f[2], f[3], u[0]) for f in c_fibre for u in u_fibre
                     if a not in {b[1], b[4]}}
            restored_query = {f for f in query if c != b[LOST]}
            need(query == {f for f in direct if f[0] == c and f[1] == a}, 'full X pin fibre')
            need(restored_query == {f for f in original if f[0] == c and f[1] == a}, 'full G pin fibre')
            by_join.update(query)
            queries.append({'s_pin': a, 'r_pin': c, 'C_full': sorted(c_fibre),
                            'U_full': sorted(u_fibre), 'X_full': sorted(query),
                            'G_full': sorted(restored_query)})
        need(by_join == direct, 'restriction/union misses assignments')
        need({f for f in direct if f[0] != b[LOST]} == original, 'restored edge equivalence')
        # An independent P/Q join holds all r contacts on the same assignment.
        pf = colored(('p0', 'p1'), factors(('p0', 'p1'), (('p0', 'p1'),)), b, ATT)
        qf = colored(('q0',), factors(('q0',), ()), b, ATT)
        cpq = {(r, p[0], p[1], q[0]) for r in COLORS for p in pf for q in qf
               if r != b[2] and r != p[0] and r != p[1] and r != q[0]}
        need(cpq == cf, 'P/Q same r union')
        tuples = sorted({(f[1], f[3]) for f in cf})
        c_ambient = [{'tuple': t, 'r_pin': r,
                      'full': sorted(f for f in cf if (f[1], f[3]) == t and f[0] == r)}
                     for t in itertools.product(COLORS, repeat=2) for r in COLORS]
        u_ambient = [{'contact_color': d, 'full': sorted(f for f in uf if f[0] == d)}
                     for d in COLORS]
        for a in COLORS:
            projection_claim = all(any(t[k] != a for t in tuples) for k in range(2))
            real = any(all(c != a for c in t) for t in tuples)
            if projection_claim and not real:
                marginal_failures.append({'boundary': b, 's_query': a, 'tuples': tuples,
                                          'marginal_product_would_accept': True})
        if direct and not original:
            restore_failures.append({'boundary': b, 'X_full': sorted(direct), 'G_full': [],
                                    'all_X_r_colors': sorted({f[0] for f in direct}),
                                    'lost_spoke_color': b[LOST]})
        record = {'boundary': b, 'C_ambient_fibres': c_ambient, 'U_ambient_fibres': u_ambient,
                  'all_16_root_queries': queries, 'C_tuples': tuples,
                  'X_full': sorted(direct), 'G_full': sorted(original)}
        own_records.append(record)
        all_values[b] = direct, original
    need(len(rows) == 240, 'literal row coverage')
    canonical = {normal(b) for b in rows}
    need(len(canonical) == 10, 'canonical row coverage')
    # Compare individual full semantic fields, never worker PASS/decision fields.
    own_lookup = {tuple(r['boundary']): json.loads(encoded(r)) for r in own_records}
    compared = []
    for reference in worker['relations']['ten_canonical_full_records']:
        own = own_lookup[tuple(reference['boundary'])]
        for field in ('C_ambient_fibres', 'U_ambient_fibres', 'all_16_root_queries',
                      'C_tuples', 'X_full', 'G_full'):
            need(own[field] == reference[field], 'worker toy field differs: ' + field)
        compared.append(reference['boundary'])
    need({tuple(b) for b in compared} == canonical, 'worker canonical fields coverage')
    need(json.loads(encoded(marginal_failures[:1])) == worker['relations']['marginal_counterexamples'],
         'worker marginal negative differs')
    need(json.loads(encoded(restore_failures[:1])) == worker['relations']['restoring_edge_blocks_all_X_lifts'],
         'worker restore negative differs')
    # Transport both the entire graph and the whole literal color frame.
    transports = 0
    for b in sorted(canonical):
        x, g = all_values[b]
        for shift, direction in itertools.product(range(5), (-1, 1)):
            moved_att = {name: tuple((shift + direction * i) % 5 for i in ports)
                         for name, ports in ATT.items()}
            lost = (shift + direction * LOST) % 5
            for pi in itertools.permutations(COLORS):
                moved_b = tuple(pi[b[(direction * (j - shift)) % 5]] for j in range(5))
                moved_x = colored(NAMES, whole_factors, moved_b, moved_att)
                moved_g_att = dict(moved_att, r=moved_att['r'] + (lost,))
                moved_g = colored(NAMES, whole_factors, moved_b, moved_g_att)
                need({tuple(pi[v] for v in f) for f in x} == moved_x, 'whole D5/S4 X transport')
                need({tuple(pi[v] for v in f) for f in g} == moved_g, 'whole D5/S4 G transport')
                transports += 1
    swap = lambda name: {'r': 's', 's': 'r'}.get(name, name)
    swapped_names = tuple(swap(v) for v in NAMES)
    swapped_edges = tuple((swap(u), swap(v)) for u, v in X_EDGES)
    swapped_att = {swap(v): a for v, a in ATT.items()}
    swapped_factors = factors(swapped_names, swapped_edges)
    for b in rows:
        sx = colored(swapped_names, swapped_factors, b, swapped_att)
        sg = colored(swapped_names, swapped_factors, b, dict(swapped_att, s=(2, LOST)))
        need((sx, sg) == all_values[b], 'whole root renaming differs')
    return {'status': 'triggered and holds', 'kind': 'one fixed abstract calibration; no source',
            'algorithm': 'Cartesian complete assignments filtered by explicit inequality factors',
            'literal_rows': 240, 'canonical_rows': 10, 'records': own_records,
            'whole_D5_S4_transports': transports, 'whole_root_renamings': 240,
            'free_isolated_factor': {'vertices': ['I'], 'colors': list(COLORS),
                                    'operation': 'Cartesian free factor with four full assignments per retained lift'},
            'marginal_counterexample': {'status': 'counterexample', **marginal_failures[0]},
            'X_extension_implies_G_counterexample': {'status': 'counterexample', **restore_failures[0]}}


def metadata(worker):
    rows = boundary_rows()
    canonical = {normal(b) for b in rows}
    q = {}
    for b in canonical:
        if len(set(b)) == 3:
            single = [k for k in range(5) if b.count(b[k]) == 1]
            need(len(single) == 1, 'three-color singleton uniqueness')
            q[single[0]] = b
    need(len(q) == 5, 'all five q rows')
    # Derive masks from sorted canonical cell indices; do not import source Q sets.
    ordered = sorted(canonical)
    rejected = {mask: {next(k for k in range(5) if row.count(row[k]) == 1)
                       for i, row in enumerate(ordered) if not ((mask >> i) & 1)}
                for mask in (933, 941)}
    need(rejected == {933: {0, 1, 2, 3}, 941: {0, 1, 3}}, 'full masks / 933 q2')
    edges = [{i, (i + 1) % 5} for i in range(5)]
    k33 = []
    disjoint = []
    for p, qedge in itertools.permutations(range(5), 2):
        common = edges[p] & edges[qedge]
        if common:
            v = next(iter(common))
            outside = set(range(5)) - {v}
            # BFS on the actual B-v induced path, rather than checking a named formula.
            reached, frontier = {min(outside)}, [min(outside)]
            while frontier:
                at = frontier.pop()
                for nb in ((at - 1) % 5, (at + 1) % 5):
                    if nb in outside and nb not in reached:
                        reached.add(nb); frontier.append(nb)
            need(reached == outside, 'O=B-v not connected')
            for rs, ss in itertools.product(itertools.combinations(range(5), 2), repeat=2):
                need(bool(set(rs) & outside) and bool(set(ss) & outside), 'two original spokes exterior')
                k33.append({'P_edge': p, 'Q_edge': qedge, 'common': v,
                            'original_r_spokes': rs, 'original_s_spokes': ss})
        else:
            available = set(range(5)) - {p, qedge}
            candidates = [(start, length) for start in range(5) for length in range(2, 6)
                          if {(start + n) % 5 for n in range(length)} <= available]
            need(len(candidates) == 1 and candidates[0][1] == 2, 'U remaining arc length')
            start, length = candidates[0]
            arc = sorted((start + n) % 5 for n in range(length))
            support = sorted(set().union(*(edges[i] for i in arc)))
            disjoint.append({'P_edge': p, 'Q_edge': qedge, 'U_shield_edges': arc,
                             'U_actual_support': support})
    need(len(k33) == 1000 and len(disjoint) == 10, 'topology schema counts')
    for rec, saved in zip(k33, worker['topology']['K33']):
        for field in rec:
            need(json.loads(encoded(rec[field])) == saved[field], 'worker K33 schema differs')
        pairs = [tuple(x[:2]) for x in saved['nine_adjacencies']]
        need(set(pairs) == {(left, right) for left in ('P', 'Q', 'O')
                           for right in ('r', 's', 'b' + str(rec['common']))}, 'nine original bags adjacencies')
        for left, right, *endpoint in saved['nine_adjacencies']:
            if left == 'O' and right in ('r', 's'):
                need(endpoint[0] in rec['original_' + right + '_spokes'], 'original spoke witness')
                need(endpoint[0] != rec['common'], 'witness not in O')
    for rec, saved in zip(disjoint, worker['topology']['disjoint_supports']):
        for field in rec:
            need(rec[field] == saved[field], 'worker disjoint arc differs')
    stabilizers = []
    countersets = []
    for start in range(5):
        support = sorted((start + k) % 5 for k in range(3))
        for b in rows:
            seen = {b[i] for i in support}
            # Stabilizer orbits are singleton seen colors plus the full absent-color orbit.
            fixed = seen | (set(COLORS) - seen if len(set(COLORS) - seen) == 1 else set())
            options = [[]] + [[c] for c in sorted(fixed)]
            if len(set(b)) == 3 and len(seen) < 3:
                d = next(c for c in COLORS if c not in b)
                need(all(d not in option for option in options), 'unused D can be forbidden')
            stabilizers.append({'support': support, 'boundary': b,
                                'stabilizer_invariant_F_with_capacity_one': options})
        permitted = {k for k, row in q.items() if len({row[i] for i in support}) == 3}
        need(permitted == set(support), 'three-point support singleton criterion')
        for mask in (941, 933):
            for shift, direction in itertools.product(range(5), (1, -1)):
                bad = {(shift + direction * i) % 5 for i in rejected[mask]}
                need(not bad <= permitted, 'source Q is contained in T')
                countersets.append({'mask': mask, 'D5': [shift, direction], 'support': support,
                                    'rejected_positions': sorted(bad),
                                    'forced_accepted_rejected_position': min(bad - permitted)})
    need(json.loads(encoded(stabilizers)) == worker['unary_arithmetic']['stabilizers'],
         'worker stabilizer arithmetic differs')
    route = {(0, 1): 'K5', (1, 2): 'K5', (2, 3): 'K5', (3, 4): 'X all-row only',
             (0, 4): 'X all-row only', (1, 4): 'X pA/pB only', (2, 4): 'X pA/pB only',
             (0, 3): 'sector exclusion'}
    mappings = []
    for rec in worker['theorem_mapping']:
        mask = rec['source_mask']; shift, direction = rec['whole_D5']
        old = q[rec['original_beta_singleton']]
        need(rec['original_beta_singleton'] in rejected[mask], 'not an original rejected beta')
        moved = tuple(old[(direction * (j - shift)) % 5] for j in range(5))
        need(list(moved) == rec['beta'], 'common D5 beta mapping')
        bad = sorted((shift + direction * i) % 5 for i in rejected[mask])
        need(bad == rec['missing_singletons'], 'whole missing set transport')
        single = next(k for k in range(5) if moved.count(moved[k]) == 1)
        rotate = (4 - single) % 5
        rb = tuple(moved[(j - rotate) % 5] for j in range(5))
        permutations = [pi for pi in itertools.permutations(COLORS)
                        if tuple(pi[c] for c in rb) == q[4]]
        need(len(permutations) == 1, 'joint normal frame is not unique')
        pi = permutations[0]
        need([rotate, 1] == rec['normalize_whole_D5'] and list(pi) == rec['normalize_whole_S4'],
             'normal frame differs')
        routes = []
        for entry, spokes in zip(rec['table'], itertools.combinations(range(5), 2)):
            pair = tuple(sorted((i + rotate) % 5 for i in spokes))
            need(list(spokes) == entry['spokes'] and list(pair) == entry['normalized_spokes'],
                 'spoke-pair whole transport')
            if moved[spokes[0]] == moved[spokes[1]]:
                need(entry['status'] == 'not triggered' and entry['retained_r_spoke_candidates'] == [],
                     'duplicate spoke metadata')
                routes.append('duplicate beta colors')
            else:
                c = next(c for c in set(moved) if c not in {moved[i] for i in spokes})
                candidate = [j for j, color in enumerate(moved) if color == c]
                need(candidate == entry['retained_r_spoke_candidates'], 'retained r pin metadata')
                routes.append(route[pair])
        mappings.append({'mask': mask, 'D5': [shift, direction], 'old_beta': rec['original_beta_singleton'],
                         'routes': routes})
    need(len(mappings) == 70 and sum(r['mask'] == 933 for r in mappings) == 40,
         'source beta coverage / q2')
    return {'status': 'triggered and holds', 'scope': 'fixed metadata, not graph sources',
            'K33_schemas': k33, 'disjoint_support_schemas': disjoint,
            'stabilizer_records': stabilizers, 'Q_support_contradictions': countersets,
            'source_mask_derivation': {str(k): sorted(v) for k, v in rejected.items()},
            'theorem_route_records': mappings}


def reconstruction():
    index = inputs()
    worker = json.loads((HERE / 'frozen/worker/certificate.json').read_bytes())
    return {'task': 'N45-H1R', 'BASE': BASE, 'frozen_inputs_sha256': sha(encoded(index)),
            'relations': relation_control(worker), 'metadata': metadata(worker),
            'evidence': {'finite_source_established': False, 'finite_source_executed': False,
                         'finite_source_status': 'not triggered', 'source_trigger_count': None,
                         'Python_proves_arbitrary_size_paper': False, 'new_Lean': False,
                         'general_N2_E': 'OPEN'}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--create', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'calibration.json')
    args = parser.parse_args()
    try:
        result = reconstruction()
        raw = encoded(result)
        if args.create:
            with args.certificate.open('xb') as file:
                file.write(raw)
        else:
            need(args.certificate.read_bytes() == raw, 'independent calibration bytes differ')
        print(json.dumps({'task': 'N45-H1R', 'status': 'PASS artifact calibration only',
                          'certificate_sha256': sha(raw), 'literal_rows': 240,
                          'full_D5_S4_transports': result['relations']['whole_D5_S4_transports'],
                          'source': 'not established; not executed; no trigger count'}, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, AssertionError) as error:
        print('REJECT: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
