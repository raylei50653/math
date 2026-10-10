#!/usr/bin/env python3
"""Read-only bounded artifact audit and independent fixed-graph solver."""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
WORKER = ROOT / 'audits/2026-10-10-n45-s-high2'
FROZEN = OUT / 'frozen/worker'
COL = tuple(range(4))
META = {'manifest.json', 'delivery.json', 'receipts.json'}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def encoded(x):
    return (json.dumps(x, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def read(p):
    return json.loads(p.read_text())


def check_authority(frozen_only=False):
    index = read(OUT / 'input-index.json')
    for directory in [WORKER, FROZEN, Path(index['parent_frozen'])]:
        files = {p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file() or p.is_symlink()}
        assert files == set(index['fulltree']), ('worker tree inventory', str(directory))
        for name, e in index['fulltree'].items():
            p = directory / name
            st = p.lstat()
            assert stat.S_ISREG(st.st_mode), name
            assert {'kind': 'regular', 'bytes': st.st_size, 'mode': stat.S_IMODE(st.st_mode),
                    'sha256': sha(p.read_bytes())} == e, name
    authority = read(FROZEN / 'inputs-final.json')
    assert len(authority['inputs']) == 41 and len(authority['pins']) == 8
    for e in authority['inputs']:
        b = (FROZEN / e['frozen']).read_bytes()
        assert sha(b) == e['sha256'], e['path']
        if not frozen_only:
            live = ((ROOT / e['path']).read_bytes() if e['origin'] == 'current' else
                    subprocess.check_output(['git', 'show', authority['BASE'] + ':' + e['path']], cwd=ROOT))
            assert b == live, e['path']
    for e in authority['pins']:
        assert sha((FROZEN / 'frozen/current' / e['path']).read_bytes()) == e['sha256'], e['path']
        if not frozen_only:
            assert sha((ROOT / e['path']).read_bytes()) == e['sha256'], e['path']
    if not frozen_only:
        assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == authority['BASE']
    return index


def artifact_bindings(index):
    manifest = read(FROZEN / 'manifest.json')
    assert manifest['excluded_exact_top_level'] == ['delivery.json', 'manifest.json', 'receipt.json']
    excluded = set(manifest['excluded_exact_top_level'])
    assert set(manifest['payload']) == set(index['fulltree']) - excluded
    assert len(manifest['payload']) == 115
    for name, e in manifest['payload'].items():
        b = (FROZEN / name).read_bytes()
        assert e == {'bytes': len(b), 'sha256': sha(b)}, name
    assert all('negative/nested/' + name in manifest['payload'] for name in excluded)
    delivery = read(FROZEN / 'delivery.json')
    assert delivery['manifest_sha256'] == sha((FROZEN / 'manifest.json').read_bytes())
    assert delivery['inputs_sha256'] == sha((FROZEN / 'inputs-final.json').read_bytes())
    assert delivery['certificate_sha256'] == sha((FROZEN / 'certificate.json').read_bytes())
    receipt = read(FROZEN / 'receipt.json')
    for path in ['manifest.json', 'delivery.json']:
        assert receipt[path + '_sha256'] == sha((FROZEN / path).read_bytes())
    seals = receipt['read_only_payload_checks']
    assert len(seals) == 2
    for i, r in enumerate(seals):
        assert r['command'] == ['python3', '-B', str(WORKER / 'seal.py'), '--check-payload']
        assert r['cwd'] == str(ROOT) and r['exit'] == 0
        assert r['environment'] == ({'PYTHONDONTWRITEBYTECODE': '1', 'GIT_OPTIONAL_LOCKS': '0'} |
                                    ({'PYTHONHASHSEED': '17'} if i else {}))
        assert sha(r['stdout'].encode()) == r['stdout_sha256']
        assert sha(r['stderr'].encode()) == r['stderr_sha256']
    assert seals[0]['stdout'] == seals[1]['stdout'] and seals[0]['stderr'] == seals[1]['stderr'] == ''
    worker_receipts = {}
    for p in sorted((FROZEN / 'logs').glob('*.receipt.json')):
        r = read(p)
        name = p.name.removesuffix('.receipt.json')
        for stream in ['stdout', 'stderr']:
            assert sha((p.parent / (name + '.' + stream + '.txt')).read_bytes()) == r[stream + '_sha256'], name
        assert r['cwd'] == str(ROOT)
        assert r['environment'].get('PYTHONDONTWRITEBYTECODE') == '1'
        assert r['environment'].get('GIT_OPTIONAL_LOCKS') == '0'
        worker_receipts[name] = r
    assert len(worker_receipts) == 17
    for checks in ['checks.json', 'checks-final.json']:
        for r in read(FROZEN / checks)['records']:
            original = worker_receipts[r['name']]
            for key in ['command', 'cwd', 'environment', 'exit', 'stdout_sha256', 'stderr_sha256']:
                assert r[key] == original[key], (checks, r['name'], key)
            if 'receipt_sha256' in r:
                assert r['receipt_sha256'] == sha((FROZEN / 'logs' / (r['name'] + '.receipt.json')).read_bytes())
    assert worker_receipts['generation']['exit'] == 2
    assert (FROZEN / 'logs/generation.stderr.txt').read_text().startswith('BASE mapping:')
    assert worker_receipts['docgraph-whole']['exit'] == 1
    assert '62 errors, 0 notes' in (FROZEN / 'logs/docgraph-whole.stdout.txt').read_text()
    duplicate_lines = (FROZEN / 'logs/docgraph-whole.stderr.txt').read_text().splitlines()
    assert len(duplicate_lines) == 62 and all('ERROR [duplicate-id]' in line for line in duplicate_lines)
    assert worker_receipts['outside-custody-final']['exit'] == 1
    return {'worker_regular_files': 118, 'worker_payload_files': 115, 'worker_exact_top_level_metadata': 3,
            'validated_log_receipts': len(worker_receipts), 'validated_seal_subcommands': 2,
            'first_generation_mapping_failure_retained': True,
            'whole_docgraph_62_failure_retained': True, 'outside_custody_failure_retained': True}


def solve(vertices, edges, attachments, row):
    """Generic recursive solver: choose smallest remaining color domain, fixed coordinates."""
    vertices = tuple(vertices)
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        if u in adjacency and v in adjacency:
            adjacency[u].add(v)
            adjacency[v].add(u)
    initial = {v: set(COL) - {row[b] for b in attachments.get(v, [])} for v in vertices}
    output = []

    def recurse(f):
        if len(f) == len(vertices):
            output.append(tuple(f[v] for v in vertices))
            return
        domains = {v: initial[v] - {f[u] for u in adjacency[v] if u in f}
                   for v in vertices if v not in f}
        v = min(domains, key=lambda x: (len(domains[x]), -len(adjacency[x]), x))
        for color in sorted(domains[v]):
            f[v] = color
            recurse(f)
        f.pop(v, None)

    recurse({})
    return sorted(output)


def components(vertices, edges):
    left = set(vertices)
    result = []
    while left:
        c = {min(left)}
        while True:
            expanded = c | {v for u, v in edges if u in c and v in left} | {
                u for u, v in edges if v in c and u in left}
            if expanded == c:
                break
            c = expanded
        left -= c
        result.append(sorted(c))
    return result


def independent_toy(cert):
    toy = cert['toy']
    names = toy['vertices']
    edges = [tuple(e) for e in toy['X_internal_edges']]
    attach = {int(k): v for k, v in toy['X_boundary_attachments'].items()}
    r, s = names.index('r'), names.index('s')
    isolated = [v for v in range(len(names)) if v not in attach and not any(v in e for e in edges)]
    assert isolated == [names.index('I')]
    active = set(range(len(names))) - set(isolated) - {s}
    parts = components(active, edges)
    c_vertices = next(c for c in parts if r in c)
    u_vertices = next(c for c in parts if r not in c)
    assert len(parts) == 2 and c_vertices == [0, 2, 3, 4] and u_vertices == [5, 6]
    neighbors = sorted(v if u == s else u for u, v in edges if s in (u, v))
    c_contact = [v for v in neighbors if v in c_vertices]
    u_contact = [v for v in neighbors if v in u_vertices]
    assert c_contact == [2, 3] and u_contact == [5, 6]
    ga = {v: list(bs) for v, bs in attach.items()}
    added_vertex, added_boundary = toy['G_added_edge']
    assert added_vertex == 'r'
    ga[r].append(int(added_boundary[1:]))
    total_x = total_g = empty_c = empty_u = empty_pin_x = empty_pin_g = 0
    ambient_slots = empty_ambient = 0
    rows_digest = []
    canonical_data = []
    rows = [row for row in itertools.product(COL, repeat=5)
            if all(row[i] != row[(i + 1) % 5] for i in range(5))]
    assert [list(row) for row in rows] == [e['row'] for e in toy['rows']]
    for row, stored in zip(rows, toy['rows']):
        ca = solve(c_vertices, edges, attach, row)
        ua = solve(u_vertices, edges, attach, row)
        cf = [[[list(f) for f in ca if (f[1], f[2]) == pair and f[0] == color]
               for color in COL] for pair in itertools.product(COL, repeat=2)]
        uf = [[list(f) for f in ua if f == pair] for pair in itertools.product(COL, repeat=2)]
        direct_x = solve(range(len(names)), edges, attach, row)
        direct_g = solve(range(len(names)), edges, ga, row)
        joined = sorted((c[0], color_s, c[1], c[2], c[3], u[0], u[1], z)
                        for c in ca for u in ua for color_s in COL for z in COL
                        if color_s not in {row[attach[s][0]], c[1], c[2], u[0], u[1]})
        assert joined == direct_x
        assert direct_g == [f for f in direct_x if f[r] != row[int(added_boundary[1:])]]
        pins = []
        grouped = {}
        for f in direct_x:
            key = (f[0], f[1], f[2], f[3], f[5], f[6], f[7])
            grouped.setdefault(key, []).append(f)
        # Complete ambient query domain, including impossible pins/tuples/free assignments.
        for key in itertools.product(COL, repeat=7):
            local = cf[key[2] * 4 + key[3]][key[0]]
            candidate = [(key[0], key[1], f[1], f[2], f[3], key[4], key[5], key[6]) for f in map(tuple, local)
                         if key[1] != row[attach[s][0]] and key[1] not in key[2:6]
                         and uf[key[4] * 4 + key[5]]]
            assert candidate == grouped.get(key, [])
        for rr, ss in itertools.product(COL, repeat=2):
            xx = [list(f) for f in direct_x if f[:2] == (rr, ss)]
            gg = [list(f) for f in direct_g if f[:2] == (rr, ss)]
            pins.append({'r': rr, 's': ss, 'X': xx, 'G': gg})
            empty_pin_x += not xx
            empty_pin_g += not gg
        detail = {'row': row, 'C_64_ambient_fibres': cf, 'U_16_ambient_fibres': uf,
                  'all_16_root_pins': pins}
        assert sha(encoded(detail)) == stored['full_fibres_sha256']
        assert stored['X_lifts'] == len(direct_x) and stored['G_lifts'] == len(direct_g)
        seen = {}
        if tuple(seen.setdefault(c, len(seen)) for c in row) == row:
            canonical_data.append(json.loads(encoded(detail)))
        total_x += len(direct_x)
        total_g += len(direct_g)
        empty_c += sum(not cell for row_fibres in cf for cell in row_fibres)
        empty_u += sum(not cell for cell in uf)
        ambient_slots += 4 ** 7
        empty_ambient += 4 ** 7 - len(grouped)
        rows_digest.append(stored['full_fibres_sha256'])
        assert direct_g, 'toy must not be mislabeled rejecting HIGH2 source'
    assert canonical_data == toy['canonical_full_data']
    assert total_x == toy['X_full_lifts_including_I'] == 21120
    assert total_g == toy['G_full_lifts_including_I'] == 7488
    return {'status': 'triggered and holds', 'scope': 'one fixed algebra toy, no source or generic soundness',
            'proper_literal_rows': len(rows), 'canonical_full_matrices': len(canonical_data),
            'C_ambient_cells': 64 * len(rows), 'U_ambient_cells': 16 * len(rows),
            'all_root_pin_queries': 16 * len(rows), 'C_empty_cells': empty_c, 'U_empty_cells': empty_u,
            'empty_X_root_pin_queries': empty_pin_x, 'empty_G_root_pin_queries': empty_pin_g,
            'ambient_full_fibre_slots': ambient_slots, 'empty_ambient_full_fibres': empty_ambient,
            'X_full_lifts': total_x, 'G_full_lifts': total_g, 'all_rows_G_accepted': True,
            'isolated_free_factor': 'I has all four assignments in each full lift',
            'actual_C_vertices': [names[v] for v in c_vertices], 'actual_U_vertices': [names[v] for v in u_vertices],
            'all_literal_fibre_digest': sha(''.join(rows_digest).encode())}


def minor_checks(cert):
    counts = {}
    for key, parts in [('K33_schemas', [(i, j) for i in range(3) for j in range(3, 6)]),
                       ('K5_frame_arc_schemas', list(itertools.combinations(range(5), 2)))]:
        cases = cert[key]['cases']
        for case in cases:
            bags = [set(b) for b in case['bags']]
            edges = [tuple(e) for e in case['edges']]
            assert all(len(components(b, edges)) == 1 for b in bags)
            assert all(not a & b for a, b in itertools.combinations(bags, 2))
            for i, j in parts:
                witnesses = sorted([list(e) for e in edges if (e[0] in bags[i] and e[1] in bags[j]) or
                                    (e[1] in bags[i] and e[0] in bags[j])])
                stored = next(a for a in case['adjacencies'] if a['bags'] == [i, j])
                assert witnesses and witnesses == stored['edges']
        counts[key] = len(cases)
    assert counts == {'K33_schemas': 1000, 'K5_frame_arc_schemas': 180}
    sample = next(c for c in cert['K33_schemas']['cases'] if c['expanded_O'])
    bags = [set(b) for b in sample['bags']]
    bad = [e for e in sample['edges'] if e != ['s', 'U']]
    assert not any((e[0] in bags[2] and e[1] in bags[4]) or (e[1] in bags[2] and e[0] in bags[4]) for e in bad)
    counts['removed_s_U_edge'] = 'counterexample to the stated O-prime/s adjacency'
    return counts


def receipt_checks():
    actual = read(OUT / 'actual-checks.json')
    assert actual['worker_tree_byte_mode_identity'] is True
    assert (OUT / 'worker-tree-before.json').read_bytes() == (OUT / 'worker-tree-after.json').read_bytes()
    assert [e['exit'] for e in actual['executions']] == [0, 0, 0, 0, 2, 2, 2, 2, 1]
    for e in actual['executions']:
        r = read(OUT / 'runs' / (e['name'] + '.receipt.json'))
        assert r['cwd'] == str(ROOT) and r['exit'] == e['exit']
        for stream in ['stdout', 'stderr']:
            assert sha((OUT / 'runs' / r[stream + '_path']).read_bytes()) == r[stream + '_sha256'] == e[stream + '_sha256']
        if 'stdin_path' in r:
            assert sha((OUT / r['stdin_path']).read_bytes()) == r['stdin_sha256']
    for first, second in [('checker-normal', 'checker-seed17'), ('seal-normal', 'seal-seed17')]:
        for stream in ['stdout', 'stderr']:
            assert (OUT / 'runs' / (first + '.' + stream + '.txt')).read_bytes() == (OUT / 'runs' / (second + '.' + stream + '.txt')).read_bytes()
    expected = {'wrong-certificate': 'certificate byte comparison: mismatch\n',
                'wrong-input-index': 'input validation: frozen-index binding\n',
                'wrong-receipt-binding': 'metadata binding: receipt to manifest.json\n'}
    for name, text in expected.items():
        assert (OUT / 'runs' / (name + '.stderr.txt')).read_text() == text
    err = (OUT / 'runs/nested-receipt-omission.stderr.txt').read_text()
    assert json.loads(err.removeprefix('payload inventory: ')) == {'missing': ['negative/nested/receipt.json'], 'extra': [], 'drift': []}
    outside = read(OUT / 'runs/outside-custody.stdout.txt')
    assert outside['outside_drift'] == []
    assert outside['outside_new_paths'] and outside['outside_status_unchanged'] is False
    assert len(outside['unhashed_directory_markers']) == 4
    markers = {p: (ROOT / p).is_dir() for p in outside['unhashed_directory_markers']}
    assert all(markers.values())
    return {'actual_read_only_commands': 9, 'checker_normal_seed17': '0/0, same bytes',
            'seal_delivery_normal_seed17': '0/0, same bytes', 'four_formal_negative_exits': [2, 2, 2, 2],
            'outside_custody_exit': 1, 'existing_indexed_regular_symlink_drift': 0,
            'outside_indexed_paths': outside['outside_indexed_files'], 'outside_new_paths': len(outside['outside_new_paths']),
            'directory_markers_presence_only': markers, 'whole_filesystem_zero_drift_claimed': False}


def compute(frozen_only=False):
    index = check_authority(frozen_only)
    cert = read(FROZEN / 'certificate.json')
    statuses = []

    def collect(x, path='$'):
        if isinstance(x, dict):
            if 'status' in x:
                assert x['status'] in {'triggered and holds', 'not triggered', 'counterexample'}, path
                statuses.append({'path': path, 'status': x['status']})
            for key, value in x.items():
                collect(value, path + '.' + key)
        elif isinstance(x, list):
            for i, value in enumerate(x):
                collect(value, path + '[' + str(i) + ']')
    collect(cert)
    assert cert['finite_HIGH2_source'] == {'status': 'not triggered', 'established': False, 'executed': False, 'trigger_count': None}
    result = {'task': 'N45-H2C', 'scope': 'bounded artifact acceptance candidate only; paper not adjudicated',
              'artifact': artifact_bindings(index), 'independent_toy': independent_toy(cert),
              'independent_finite_minor_checks': minor_checks(cert), 'actual_replays': receipt_checks(),
              'certificate_control_classifications': statuses, 'finite_source': cert['finite_HIGH2_source'],
              'new_Lean': False, 'general_tool_soundness_claimed': False}
    return result


def own_manifest():
    manifest = read(OUT / 'manifest.json')
    actual = {p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file() or p.is_symlink()}
    assert manifest['exact_top_level_metadata_exclusions'] == sorted(META)
    assert actual - META == set(manifest['payload'])
    for name, e in manifest['payload'].items():
        p = OUT / name
        assert not p.is_symlink() and sha(p.read_bytes()) == e['sha256'] and p.stat().st_size == e['bytes'], name
    for name in ['delivery.json', 'receipts.json']:
        p = OUT / name
        if p.exists():
            m = read(p)
            assert m['manifest_sha256'] == sha((OUT / 'manifest.json').read_bytes())
            assert m['certificate_sha256'] == sha((OUT / 'artifact-certificate.json').read_bytes())
            if name == 'receipts.json':
                executions = m['executions']
                assert [e['name'] for e in executions] == ['normal', 'seed17', 'frozen-normal', 'frozen-seed17']
                for i, e in enumerate(executions):
                    assert e['exit'] == 0 and e['cwd'] == str(ROOT)
                    expected = ['python3', '-B', str(OUT / 'verifier.py')] + (['--frozen-only'] if i >= 2 else [])
                    assert e['command'] == expected
                    assert e['environment'] == ({'PYTHONDONTWRITEBYTECODE': '1', 'GIT_OPTIONAL_LOCKS': '0'} |
                                                ({'PYTHONHASHSEED': '17'} if i % 2 else {}))
                    assert sha(e['stdout'].encode()) == e['stdout_sha256']
                    assert sha(e['stderr'].encode()) == e['stderr_sha256'] and e['stderr'] == ''
                assert executions[0]['stdout'] == executions[1]['stdout']
                assert executions[2]['stdout'] == executions[3]['stdout']
    report = (OUT / 'REPORT.md').read_text()
    for target in re.findall(r'\]\(([^)]+)\)', report):
        if '://' not in target and not target.startswith('#'):
            assert (OUT / target.split('#', 1)[0]).exists(), target
    for name in ['REPORT.md', 'verifier.py', 'run_checks.py', 'negative_receipt_probe.py', 'independent-judgment.json']:
        assert all(line == line.rstrip() and '\t' not in line for line in (OUT / name).read_text().splitlines()), name


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--preflight', action='store_true')
    p.add_argument('--frozen-only', action='store_true', help='Validate frozen evidence and historical receipts; do not require live shared origins/pins/HEAD equal pre-adoption state')
    args = p.parse_args()
    try:
        result = compute(args.frozen_only)
        if args.preflight:
            print(encoded(result).decode(), end='')
        else:
            assert result == read(OUT / 'artifact-certificate.json'), 'artifact certificate mismatch'
            own_manifest()
            print(json.dumps({'task': 'N45-H2C', 'status': 'bounded artifact checks hold',
                              'certificate_sha256': sha((OUT / 'artifact-certificate.json').read_bytes()),
                              'paper_adjudicated': False, 'finite_source': 'not triggered',
                              'verification_mode': 'frozen evidence and historical pre-adoption receipts' if args.frozen_only else 'pre-adoption live origins plus frozen evidence'}, sort_keys=True))
        return 0
    except (AssertionError, OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as e:
        print('FAIL: ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
