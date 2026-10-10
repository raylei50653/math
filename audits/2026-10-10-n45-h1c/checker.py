#!/usr/bin/env python3
"""Independent frozen custody gates plus read-only fixed-domain controls.

Paper, disk realization, and HIGH1 source validity are not adjudicated here.
The audited worker arithmetic functions are executed read-only after replacing
their live-input reader with the independent frozen-input gate below. A separate
Cartesian enumerator then checks all 240 toy rows and the finite schemas.
"""
import argparse
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORKER = ROOT / 'audits/2026-10-10-n45-s-high1'
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
WORKER_INDEX_SHA = '8295f37e0b931e49cce54961439903d2b515c2909123cad7f9c96f0e0b13e5a8'
EXCLUDED = ['delivery.json', 'manifest.json', 'receipt.json']
COL = set(range(4))
Q = [(0, 1, 2, 1, 2), (0, 1, 2, 0, 2), (0, 1, 2, 0, 1),
     (0, 1, 0, 2, 1), (0, 1, 0, 1, 2)]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def sha(p):
    return digest(p.read_bytes())


def encode(d):
    return (json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def read(p):
    return json.loads(p.read_bytes())


def safe(name):
    need(isinstance(name, str) and name and '\\' not in name and '\x00' not in name,
         'unsafe relative path')
    p = PurePosixPath(name)
    need(not p.is_absolute() and all(x not in ('', '.', '..') for x in p.parts)
         and p.as_posix() == name, 'unsafe relative path: ' + name)
    return name


def inventory(folder, excluded=()):
    rows = []
    for p in sorted(folder.rglob('*')):
        need(not p.is_symlink(), 'symlink in inventory: ' + str(p))
        if p.is_file():
            name = safe(p.relative_to(folder).as_posix())
            if name not in excluded:
                rows.append(dict(path=name, sha256=sha(p), bytes=p.stat().st_size))
    return rows


def frozen_inputs(index):
    need(sha(index) == WORKER_INDEX_SHA, 'frozen input index binding')
    d = read(index)
    ours = read(HERE / 'inputs.json')
    need(d == ours['worker_input_index'], 'frozen input index content')
    need(d['BASE'] == BASE and d['HEAD'] == BASE and d['task'] == 'N45-S-HIGH1', 'input identity')
    need(len(d['inputs']) == 34 and d['pins_verified'] == 9, 'input count')
    need(len({r['frozen'] for r in d['inputs']}) == 34, 'duplicate frozen inputs')
    counts = {layer: sum(r['layer'] == layer for r in d['inputs']) for layer in ('BASE', 'current', 'external')}
    need(counts == {'BASE': 16, 'current': 17, 'external': 1}, 'input layer coverage')
    for r in d['inputs']:
        name = safe(r['frozen'])
        if r['layer'] in ('BASE', 'current'):
            original = safe(r['path'])
            need(name == 'frozen/' + r['layer'].lower() + '/' + original, 'frozen path identity')
        else:
            need(name == 'frozen/gallai.pdf' and r['url'] == 'https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf', 'external identity')
        frozen = (WORKER / name).read_bytes()
        need(digest(frozen) == r['sha256'], 'frozen input digest: ' + name)
        if r['layer'] == 'BASE':
            original = subprocess.check_output(['git', 'show', BASE + ':' + r['path']], cwd=ROOT)
            need(frozen == original, 'BASE object byte mismatch: ' + r['path'])
    pins = ours['task_pins']
    actual_pins = read(WORKER / 'frozen/current/audits/2026-10-10-n45-low2-supervision/high1-task-pins.json')
    need(pins == actual_pins and pins['BASE'] == BASE and len(pins['pins']) == 9, 'nine task pins')
    lookup = {r.get('path'): r['sha256'] for r in d['inputs'] if r['layer'] == 'current'}
    need(all(lookup[p['path']] == p['sha256'] for p in pins['pins']), 'task pin lookup')
    return d


def worker_unchanged():
    d = read(HERE / 'inputs.json')
    need(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == BASE, 'HEAD drift')
    now = inventory(WORKER)
    saved = [{k: r[k] for k in ('path', 'sha256', 'bytes')} for r in d['worker_tree']]
    need(now == saved and len(now) == 94, 'worker full tree differs from independent intake')
    need(all(stat.S_IMODE((WORKER / r['path']).stat().st_mode) == r['mode'] for r in d['worker_tree']), 'worker mode drift')
    return now


def payload_gate(path):
    d = read(path)
    need(d['task'] == 'N45-S-HIGH1' and d['excluded_exact_top_level'] == EXCLUDED, 'manifest identity/exclusions')
    rows = d['payload']
    names = [safe(r['path']) for r in rows]
    need(len(names) == len(set(names)), 'duplicate manifest path')
    need(names == sorted(names), 'manifest path order')
    actual = inventory(WORKER, EXCLUDED)
    missing = sorted({r['path'] for r in actual} - set(names))
    extra = sorted(set(names) - {r['path'] for r in actual})
    need(rows == actual, 'payload inventory/hash mismatch; missing=' + repr(missing) + '; extra=' + repr(extra))
    need(len(rows) == 91 and 'negative/nested/receipt.json' in names, '91 payload including nested homonym')
    return rows


def receipt_gate(path):
    delivery = read(WORKER / 'delivery.json')
    need(delivery['task'] == 'N45-S-HIGH1' and delivery['BASE'] == BASE, 'delivery identity')
    need(delivery['excluded_exact_top_level'] == EXCLUDED and delivery['payload_files'] == 91, 'delivery scope/count')
    for key, filename in [('manifest_sha256', 'manifest.json'), ('REPORT_sha256', 'REPORT.md'),
                          ('certificate_sha256', 'certificate.json'), ('claims_sha256', 'claims.json')]:
        need(delivery[key] == sha(WORKER / filename), 'delivery ' + key)
    need(delivery['receipt_sha256'] == sha(path), 'receipt metadata binding')
    receipt = read(path)
    need(receipt['task'] == delivery['task'] and receipt['manifest_sha256'] == delivery['manifest_sha256'], 'receipt identity')
    need(receipt['input_index_sha256'] == WORKER_INDEX_SHA and receipt['certificate_sha256'] == delivery['certificate_sha256'], 'receipt input/certificate binding')
    need(receipt['checks_sha256'] == sha(WORKER / 'checks-final.json'), 'receipt checks binding')
    checks = read(WORKER / 'checks-final.json')
    need(receipt['logs'] == checks['runs'], 'receipt exact ledger')
    expected = {'normal': 0, 'seed17': 0, 'bad-certificate': 2, 'bad-input-index': 2,
                'exclusive-create': 2, 'local-links-whitespace': 0, 'git-diff-check': 0,
                'check-docs-current': 0, 'docgraph-formal': 0, 'docgraph-whole': 1,
                'input-custody': 0, 'bad-manifest-nested-omission': 2}
    runs = checks['runs']
    need(len(runs) == 12 and {r['id'] for r in runs} == set(expected), '12 unique required runs')
    by_id = {r['id']: r for r in runs}
    for r in runs:
        need(r['actual_exit'] == r['expected_exit'] == expected[r['id']], 'actual exit scope: ' + r['id'])
        need(r['cwd'] == str(ROOT), 'actual run cwd')
        need(r['environment'] == ({'PYTHONHASHSEED': '17'} if r['id'] == 'seed17' else {}), 'actual run environment')
        for stream in ('stdout', 'stderr'):
            name = safe(r[stream + '_file'])
            need(name.startswith('logs/') and sha(WORKER / name) == r[stream + '_sha256'], '24 actual stream bindings')
        metadata_name = r['stdout_file'].replace('.stdout.txt', '.receipt.json')
        need(read(WORKER / safe(metadata_name)) == r, 'nested actual-run receipt binding')
    for stream in ('stdout', 'stderr'):
        need((WORKER / by_id['normal'][stream + '_file']).read_bytes() == (WORKER / by_id['seed17'][stream + '_file']).read_bytes(), 'worker replay byte agreement')
    checker_command = ['python3', '-B', 'audits/2026-10-10-n45-s-high1/checker.py', '--check']
    need(by_id['normal']['command'] == by_id['seed17']['command'] == checker_command, 'worker check replay commands')
    for name, environment in [('payload_check_normal', {}), ('payload_check_seed17', {'PYTHONHASHSEED': '17'})]:
        r = receipt[name]
        need(r['exit'] == 0 and r['cwd'] == str(ROOT) and r['environment'] == environment and r['stderr'] == '', 'embedded payload actual replay')
        need(r['command'] == ['python3', '-B', 'audits/2026-10-10-n45-s-high1/seal.py', '--check-payload'], 'embedded payload command')
    need(receipt['payload_check_normal']['stdout'] == receipt['payload_check_seed17']['stdout'], 'embedded seed replay bytes')
    for name, stage in [('bad-certificate', 'certificate byte comparison'),
                        ('bad-input-index', 'input validation / fixed-domain reconstruction'),
                        ('exclusive-create', 'exclusive certificate create'),
                        ('bad-manifest-nested-omission', 'payload inventory')]:
        reject = read(WORKER / by_id[name]['stderr_file'])
        need(reject['status'] == 'REJECT' and reject['stage'] == stage, 'recorded negative rejection stage')
    docfail = (WORKER / by_id['docgraph-whole']['stderr_file']).read_text()
    need(docfail.count('ERROR [duplicate-id]') == 62, 'retained 62 duplicate-ID failures')
    claims = read(WORKER / 'claims.json')
    need(len(claims['claims']) == 10 and all(not c['python_proves_arbitrary_size_claim'] and not c['new_Lean'] for c in claims['claims']), 'paper/machine evidence separation')
    need(delivery['new_Lean'] is False and delivery['general_N2_E'] == 'OPEN'
         and delivery['finite_source'] == 'not established / not executed / no trigger count', 'delivery evidence boundaries')
    local_links = 0
    for name in re.findall(r'\]\(([^\s)]+)\)', (WORKER / 'REPORT.md').read_text()):
        u = urlsplit(name)
        if not u.scheme:
            need((WORKER / unquote(u.path)).exists() and not u.fragment, 'worker report local link')
            local_links += 1
    need(local_links == 20, '20 worker report local links')
    return dict(actual_runs=12, actual_streams=24, nested_actual_run_receipts=12,
                worker_report_local_links=20, retained_duplicate_ID_errors=62)


def direct_assignments(vertices, edges, attachments, row):
    order = sorted(vertices)
    pos = {v: i for i, v in enumerate(order)}
    lists = [sorted(COL - {row[j] for j in attachments.get(v, [])}) for v in order]
    return [a for a in it.product(*lists) if all(a[pos[u]] != a[pos[v]] for u, v in edges)]


def canonical(row):
    order = []
    for x in row:
        if x not in order:
            order.append(x)
    return tuple(order.index(x) for x in row)


def independently_check_fixed_domain(cert):
    rows = [b for b in it.product(range(4), repeat=5) if all(b[i] != b[(i+1) % 5] for i in range(5))]
    need(len(rows) == 240 and len({canonical(b) for b in rows}) == 10, '240 literal / ten canonical row domain')
    rel = cert['relations']
    ce = [(5, 7), (5, 8), (5, 9), (7, 8)]
    xe = ce + [(6, 7), (6, 9), (6, 10)]
    att = {5: [2], 6: [1, 4], 7: [1], 8: [1, 2], 9: [3, 4], 10: [4, 0, 1], 11: []}
    need(rel['edges_X'] == [list(e) for e in xe] and rel['attachments_X'] == {str(k): v for k, v in att.items()}, 'toy original edge/attachment identity')
    need(rel['restored_edge'] == [5, 3] and rel['rotation'] == 'not supplied; no disk claim', 'toy omitted edge/disk boundary')
    saved = {tuple(r['boundary']): r for r in rel['ten_canonical_full_records']}
    all_rows = {tuple(r['boundary']): r for r in rel['all_240_rows']}
    need(len(saved) == 10 and len(all_rows) == 240, 'complete row coverage without duplicates')
    x_total = g_total = 0
    for b in rows:
        cs = direct_assignments([5, 7, 8, 9], ce, att, b)
        us = direct_assignments([10], [], att, b)
        xs = direct_assignments([5, 6, 7, 8, 9, 10], xe, att, b)
        ga = {**att, 5: [2, 3]}
        gs = direct_assignments([5, 6, 7, 8, 9, 10], xe, ga, b)
        queries = []
        joined = set()
        for a, c in it.product(range(4), repeat=2):
            fc = [f for f in cs if f[0] == c and f[1] != a and f[3] != a]
            fu = [f for f in us if f[0] != a]
            full = [(c, a, f[1], f[2], f[3], u[0]) for f, u in it.product(fc, fu)] if a not in {b[1], b[4]} else []
            joined.update(full)
            queries.append(dict(s_pin=a, r_pin=c, C_full=fc, U_full=fu, X_full=full,
                                G_full=[f for f in full if c != b[3]]))
        need(joined == set(xs) and {f for f in joined if f[0] != b[3]} == set(gs), 'independent full join and restored-spoke projection')
        record = dict(boundary=b, C_vertices=[5, 7, 8, 9], C_ordered_contacts=(7, 9),
                      C_tuples=sorted({(f[1], f[3]) for f in cs}),
                      C_ambient_fibres=[dict(tuple=t, r_pin=c, full=[f for f in cs if (f[1], f[3]) == t and f[0] == c]) for t in it.product(range(4), repeat=2) for c in range(4)],
                      U_ambient_fibres=[dict(contact_color=c, full=[f for f in us if f[0] == c]) for c in range(4)],
                      all_16_root_queries=queries, X_full=sorted(xs), G_full=sorted(gs),
                      free_vertex=11, free_factor_colors=list(range(4)))
        check = all_rows[b]
        need(check['X_count'] == len(xs) and check['G_count'] == len(gs)
             and check['free_X_count'] == 4 * len(xs) and check['full_record_sha256'] == digest(encode(record)), 'independent all-240 complete-record binding')
        if b in saved:
            need(encode(saved[b]) == encode(record), 'all ten saved complete ambient fibres')
        x_total += len(xs)
        g_total += len(gs)
    need((x_total, g_total) == (2160, 1560), 'toy full-lift counts')
    for example in rel['marginal_counterexamples']:
        ts = example['tuples']; a = example['s_query']
        need(all(any(t[i] != a for t in ts) for i in range(2)) and not any(all(x != a for x in t) for t in ts), 'marginal overstatement counterexample')
    for example in rel['restoring_edge_blocks_all_X_lifts']:
        need(example['X_full'] and not example['G_full'] and all(f[0] == example['lost_spoke_color'] for f in example['X_full']), 'X does not imply G counterexample')
    edges = [set((i, (i+1) % 5)) for i in range(5)]
    topo = cert['topology']; signatures = set()
    for r in topo['K33']:
        p, q, v = r['P_edge'], r['Q_edge'], r['common']
        rs, ss = r['original_r_spokes'], r['original_s_spokes']
        need(edges[p] & edges[q] == {v} and len(set(rs)) == len(set(ss)) == 2, 'K33 support/spoke schema')
        rv, sv = next(i for i in rs if i != v), next(i for i in ss if i != v)
        expected = [['P','r'],['P','s'],['P','b'+str(v)],['Q','r'],['Q','s'],['Q','b'+str(v)],['O','r',rv],['O','s',sv],['O','b'+str(v),(v+1)%5]]
        need(r['nine_adjacencies'] == expected and {rv, sv, (v+1)%5} <= set(range(5)) - {v}, 'K33 nine schema adjacency witnesses')
        need({(v+i)%5 for i in range(1,5)} == set(range(5)) - {v}, 'O original frame connectivity')
        signatures.add((p,q,tuple(rs),tuple(ss)))
    need(len(topo['K33']) == len(signatures) == 1000, '1000 distinct K33 schemas')
    for r in topo['disjoint_supports']:
        remaining = set(range(5)) - {r['P_edge'], r['Q_edge']}
        arcs = {tuple(sorted((start+k)%5 for k in range(length))) for start in range(5) for length in range(2,6) if {(start+k)%5 for k in range(length)} <= remaining}
        need(len(arcs) == 1 and tuple(r['U_shield_edges']) in arcs and len(r['U_shield_edges']) == 2, 'unique finite long-two arc metadata')
        need(r['U_actual_support'] == sorted(set().union(*(edges[i] for i in r['U_shield_edges']))), 'finite three-point support metadata')
    need(len(topo['disjoint_supports']) == 10, 'ten ordered disjoint support metadata')
    unary = cert['unary_arithmetic']
    for r in unary['stabilizers']:
        b, support = r['boundary'], r['support']
        candidates = []
        for candidate in [set()] + [{c} for c in range(4)]:
            if all({perm[c] for c in candidate} == candidate for perm in it.permutations(range(4)) if all(perm[b[i]] == b[i] for i in support)):
                candidates.append(sorted(candidate))
        need(r['stabilizer_invariant_F_with_capacity_one'] == candidates, 'independent pointwise-support S4 stabilizer arithmetic')
    need(len(unary['stabilizers']) == 1200 and len(unary['missing_position_checks']) == 100, 'finite unary arithmetic domain')
    for r in unary['missing_position_checks']:
        support = set(r['U_support']); shift, sign = r['whole_D5']
        missing = {0,1,3} if r['source_mask'] == 941 else {0,1,2,3}
        moved = {(shift+sign*i)%5 for i in missing}
        permitted = {i for i,q in enumerate(Q) if len({q[j] for j in support}) == 3}
        need(moved == set(r['source_rejection_positions']) and permitted == support == set(r['permitted_rejection_positions']) and r['forced_accepted_position'] == min(moved-support), 'whole-D5 rejection-position arithmetic')
    maps = cert['theorem_mapping']
    need(len(maps) == 70 and sum(r['source_mask'] == 933 for r in maps) == 40, '70 beta metadata includes all 933 q2 images')
    for r in maps:
        shift, sign = r['whole_D5']; k = r['original_beta_singleton']; beta = [None]*5
        for i,c in enumerate(Q[k]): beta[(shift+sign*i)%5] = c
        need(r['beta'] == beta and len(r['table']) == 10 and not r['source_instantiated'], 'whole-source metadata, not source graph')
        ns, ns_sign = r['normalize_whole_D5']; cmap = r['normalize_whole_S4']
        normalized = [None]*5
        for i,c in enumerate(beta): normalized[(ns+ns_sign*i)%5] = cmap[c]
        need(tuple(normalized) == Q[4], 'shared literal whole-D5/S4 normalization arithmetic')
        for t in r['table']:
            need(t['normalized_spokes'] == sorted((i+ns)%5 for i in t['spokes']), 'spoke-position transport')
            duplicate = beta[t['spokes'][0]] == beta[t['spokes'][1]]
            need(t['status'] == ('not triggered' if duplicate else 'triggered and holds'), 'finite spoke routing status')
    need(cert['evidence']['finite_source_established'] is False and cert['evidence']['source_trigger_count'] is None
         and cert['evidence']['new_Lean'] is False and cert['evidence']['arbitrary_size_proof_checked_by_python'] is False, 'certificate evidence boundaries')
    return dict(literal_rows=240, canonical_rows=10, C_ambient_fibres_per_canonical_row=64,
                U_ambient_fibres_per_canonical_row=4, root_queries_per_literal_row=16,
                toy_X_lifts=2160, toy_G_lifts=1560, isolated_free_factor=4,
                K33_adjacency_schemas=1000, disjoint_support_metadata=10,
                unary_stabilizer_records=1200, whole_D5_missing_checks=100,
                beta_metadata=70, HIGH1_source='not established / not executed / no trigger count')


def reconstruct(index):
    # Loading does not run worker main, mutate certificates, or consult decisions.
    # Its inputs() is never called: all authority comparisons use frozen_inputs().
    spec = importlib.util.spec_from_file_location('audited_high1_fixed_domain', WORKER / 'checker.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.inputs = frozen_inputs
    rebuilt = module.result(index)
    payload = encode(rebuilt)
    summary = independently_check_fixed_domain(json.loads(payload))
    return payload, summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate', type=Path, default=WORKER/'certificate.json')
    p.add_argument('--input-index', type=Path, default=WORKER/'inputs.json')
    p.add_argument('--manifest', type=Path, default=WORKER/'manifest.json')
    p.add_argument('--receipt', type=Path, default=WORKER/'receipt.json')
    p.add_argument('--generate-certificate', action='store_true')
    args = p.parse_args()
    stage = 'input validation / independent frozen binding'
    try:
        worker_unchanged()
        frozen_inputs(args.input_index)
        stage = 'payload inventory'
        payload_gate(args.manifest)
        stage = 'delivery/receipt exact binding'
        meta = receipt_gate(args.receipt)
        stage = 'fixed-domain reconstruction / independent Cartesian calibration'
        payload, summary = reconstruct(args.input_index)
        if args.generate_certificate:
            stage = 'exclusive certificate create'
            with args.certificate.open('xb') as f:
                f.write(payload)
        else:
            stage = 'certificate byte comparison'
            need(args.certificate.read_bytes() == payload, 'certificate bytes differ')
        print(json.dumps(dict(task='N45-H1C', status='PASS: frozen artifact integrity and fixed-domain calibration only',
                              BASE=BASE, worker_regular_files=94, worker_payload_files=91,
                              exact_top_level_metadata=EXCLUDED, frozen_inputs=34, task_pins=9,
                              certificate_bytes=len(payload), certificate_sha256=digest(payload),
                              actual_log_bindings=meta, independent_finite_domain=summary,
                              paper='not adjudicated', new_Lean=False, general_N2_E='OPEN'), sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, AssertionError) as e:
        print(json.dumps(dict(status='REJECT', stage=stage, reason=str(e)), sort_keys=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
