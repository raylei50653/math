#!/usr/bin/env python3
"""Exact original C8 s=1 terminal exterior; arbitrary L is never enumerated.

The gzip JSONL archive has one record per named exterior. Every B row contains
4096 explicit literal D fibres, including improper and proper empty entries.
Each stored string colors every vertex of P in the named vertex_order.
"""
from pathlib import Path
from collections import Counter, defaultdict
from contextlib import ExitStack
from itertools import product
import argparse
import copy
import gzip
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT.parent / 'frozen'
OLD = Path('audits/2026-10-13-c5-no4ct-frontier-6943561/terminals')
KCHECK = FROZEN / OLD / 'check.py'
KARCHIVE = FROZEN / OLD / 'full_lifts.v2.json.gz'
CERTIFICATE = ROOT / 'certificate.json.gz'
ARCHIVE = ROOT / 'full_lifts.jsonl.gz'
spec = importlib.util.spec_from_file_location('frozen_terminal', KCHECK)
tk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tk)
D_ROWS = tuple(''.join(r) for r in product('0123', repeat=6))
D_INDEX = {r: i for i, r in enumerate(D_ROWS)}
ORBITS = tuple(sorted({tk.canonical(r) for r in D_ROWS
                       if all(r[i] != r[(i+1)%6] for i in range(6))}))


def exterior(kind, pair, side, slot, e):
    """All names and half ownership are fixed before any color row is chosen."""
    ends = ('x',) if kind == 'PINCH' else ('x', 'y')
    vi = (pair + 4*side) % 8
    fi = (vi + 4) % 8
    ve = ends[side if kind == 'BRIDGE' else 0]
    fe = ends[1-side if kind == 'BRIDGE' else 0]
    j = tuple(tk.C[(fi+k)%8] for k in range(5)) + (fe,)
    u = tuple(tk.T[(fi+k)%8] for k in range(4)) + ('zF',)
    vt = tuple(tk.T[(vi+k)%8] for k in range(4))
    vc = tuple(tk.C[(vi+k)%8] for k in range(5))
    d = [ve] + list(vt)
    d.insert(slot+1, 'w')
    d = tuple(d)
    variable_faces = [(vc[k], vc[k+1], vt[k]) for k in range(4)]
    wedges = [(vc[0], vt[0], ve)]
    wedges += [(vc[k], vt[k], vt[k-1]) for k in range(1, 4)]
    wedges += [(vc[4], ve, vt[3])]
    for k, (a, b, c) in enumerate(wedges):
        variable_faces.extend([(a, b, 'w'), (a, 'w', c)] if k == slot else [(a, b, c)])
    hfaces = tk.patch_faces(j, u) + variable_faces
    if kind == 'BRIDGE':
        hfaces += [(tk.C[pair], 'x', 'y'), (tk.C[(pair+4)%8], 'y', 'x')]
    collar, original_names = tk.collar_faces(e)
    faces = collar + hfaces
    vertices = tk.B + tk.C + tk.T + ends + ('w', 'zF')
    edges = sorted({tk.edge(a, b) for f in faces for a, b in zip(f, f[1:]+f[:1])})
    g = tk.graph_on(vertices, edges)
    g.update(faces=tuple(faces), D=d, original_collar_C_names=original_names)
    sv = tuple(v for v in vertices if v not in u)
    skeleton = tk.graph_on(sv, [ed for ed in edges if set(ed) <= set(sv)])
    assert set(g['vertices']) == set(sv) | set(u)
    assert not set(u) & set(d)
    # Fill only for validating the inherited annular embedding, not as L evidence.
    fan_faces = [("embedding_dummy", d[k], d[(k+1)%6]) for k in range(6)]
    filled = tk.assemble(vertices + ('embedding_dummy',), tk.B, faces + fan_faces)
    # Remove the dummy from each cyclic rotation: this leaves the original cyclic
    # order of all P edges, and its missing sector is exactly the D interior.
    g['rotations'] = {v: [w for w in filled['rotations'][v] if w != 'embedding_dummy']
                      for v in vertices}
    assert len(vertices)-len(edges)+len(faces) == 0
    return g, skeleton, j, u, d


def expand(g, skeleton, j, u, kernel, beta):
    result = []
    for partial in tk.direct(skeleton, dict(zip(tk.B, map(int, beta)))):
        assignment = dict(zip(skeleton['vertices'], partial))
        jrow = ''.join(assignment[v] for v in j)
        for private in kernel[jrow]:
            full = assignment | dict(zip(u, private))
            result.append(''.join(full[v] for v in g['vertices']))
    assert len(result) == len(set(result))
    return sorted(result)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def normalized(value):
    return json.loads(encode(value))


def get_kernel():
    with gzip.open(KARCHIVE, 'rt') as source:
        kernel = json.load(source)['kernel']['complete_literal_fibres']
    _, independently_checked, histogram = tk.terminal_kernel()
    assert kernel == independently_checked
    return kernel


def compute_exterior(kind, pair, side, slot, e, kernel):
    g, skeleton, j, u, d = exterior(kind, pair, side, slot, e)
    archive_rows = {}
    masks = dict.fromkeys(ORBITS, 0)
    row_counts, empty_counts = {}, {}
    di = tuple(g['vertices'].index(v) for v in d)
    for bi, beta in enumerate(tk.B_ROWS):
        full = tk.direct(g, dict(zip(tk.B, map(int, beta))))
        # One direct MRV search on ALL P vertices versus independent literal W5
        # kernel reconstruction from the complementary original skeleton.
        assert full == expand(g, skeleton, j, u, kernel, beta)
        fibres = [[] for _ in D_ROWS]
        for lift in full:
            gamma = ''.join(lift[i] for i in di)
            fibres[D_INDEX[gamma]].append(lift)
            masks[tk.canonical(gamma)] |= 1 << bi
        assert sum(map(len, fibres)) == len(full)
        archive_rows[beta] = fibres
        row_counts[beta] = len(full)
        empty_counts[beta] = sum(not values for values in fibres)
    payload = {'vertex_order': g['vertices'], 'D_order': d,
               'B_order': tk.B, 'D_literal_order': D_ROWS,
               'complete_B_D_fibres': archive_rows}
    graph = {k: g[k] for k in ('vertices', 'edges', 'faces', 'D', 'rotations',
                              'original_collar_C_names')}
    return payload, graph, masks, row_counts, empty_counts, (j, u)


def chord_control(g, d, slot, beta, exterior_fibres):
    """Exact W5+endpoint ear filling, only as a separately named calibration."""
    assert slot in (0, 4)
    rim = d[1:]  # endpoint d[0] is the triangular ear vertex.
    faces = list(g['faces']) + [(d[0], d[1], d[-1])]
    faces += [('zL', rim[k], rim[(k+1)%5]) for k in range(5)]
    filled = tk.assemble(g['vertices'] + ('zL',), tk.B, faces)
    full = tk.direct(filled, dict(zip(tk.B, map(int, beta))))
    joined = []
    pi = {v: i for i, v in enumerate(g['vertices'])}
    for fibres in exterior_fibres:
        for lift in fibres:
            if lift[pi[d[1]]] == lift[pi[d[-1]]]:
                continue
            for c in '0123':
                if all(c != lift[pi[v]] for v in rim):
                    joined.append(lift+c)
    assert full == sorted(joined)
    return full


def compare_payload(actual, expected):
    """The same fail-closed archive validator is used by replay and mutations."""
    assert set(actual) == set(expected), 'archive record fields differ'
    for field in expected:
        if field != 'complete_B_D_fibres':
            assert actual[field] == normalized(expected[field]), ('archive field mismatch', field)
    actual_rows = actual['complete_B_D_fibres']
    expected_rows = expected['complete_B_D_fibres']
    assert set(actual_rows) == set(expected_rows), 'B row set differs'
    for beta in tk.B_ROWS:
        assert len(actual_rows[beta]) == 4096, ('literal D fibre omitted', beta)
        assert actual_rows[beta] == expected_rows[beta], ('full P fibre mismatch', beta)


def require_rejected(actual, expected):
    try:
        compare_payload(actual, expected)
    except AssertionError:
        return
    raise AssertionError('semantic corruption passed the archive validator')


def rejection_controls(payload, graph, kernel):
    """In-memory semantic mutations only; evidence files are never altered."""
    beta = tk.B_ROWS[0]
    damaged = copy.deepcopy(payload)
    damaged['complete_B_D_fibres'][beta].pop()
    require_rejected(normalized(damaged), payload)
    damaged = copy.deepcopy(payload)
    nonempty = next(f for f in damaged['complete_B_D_fibres'][beta] if f)
    nonempty.pop()
    require_rejected(normalized(damaged), payload)
    damaged = copy.deepcopy(payload)
    empty = next(f for f in damaged['complete_B_D_fibres'][beta] if not f)
    empty.append('0' * len(payload['vertex_order']))
    require_rejected(normalized(damaged), payload)
    damaged = copy.deepcopy(payload)
    damaged['D_order'] = tuple(reversed(damaged['D_order']))
    require_rejected(normalized(damaged), payload)
    # The original edge xy is tested as a literal inequality, independently of
    # any marginal endpoint palette. This local witness passes separate pins.
    assert tk.edge('x', 'y') in graph['edges']
    bridge = tk.graph_on(('x', 'y'), [tk.edge('x', 'y')])
    assert not tk.direct(bridge, {'x': 0, 'y': 0})
    assert tk.direct(tk.graph_on(('x', 'y'), []), {'x': 0, 'y': 0})
    controls = tk.negative_controls(kernel)
    controls.update(dropped_literal_D_fibre_rejected=True,
                    dropped_full_P_lift_rejected=True,
                    false_nonempty_fibre_rejected=True,
                    omitted_bridge_inequality_rejected=True,
                    independently_reordered_D_names_rejected=True)
    return controls


def run(write=False, negative=False):
    if write:
        assert not CERTIFICATE.exists() and not ARCHIVE.exists(), 'exclusive evidence files exist'
    kernel = get_kernel()
    records, chord_records = [], []
    counts = Counter()
    all_archive_hash = hashlib.sha256()
    negative_result = None
    with ExitStack() as stack:
        if write:
            raw = stack.enter_context(ARCHIVE.open('xb'))
            stream = stack.enter_context(gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0))
        else:
            stream = stack.enter_context(gzip.open(ARCHIVE, 'rb'))
        for kind in ('PINCH', 'BRIDGE'):
            for pair in range(4):
                for side in range(2):
                    for slot in range(5):
                        cache = {}
                        chord_cache = {}
                        for query, e, target in tk.QUERIES:
                            if e not in cache:
                                cache[e] = compute_exterior(kind, pair, side, slot, e, kernel)
                            payload, graph, masks, row_counts, empty_counts, patch = cache[e]
                            name = f'{kind}-{pair}-{side}-{slot}-{query}'
                            line = encode({'name': name, **payload}) + b'\n'
                            all_archive_hash.update(line)
                            if write:
                                stream.write(line)
                            else:
                                stored_line = stream.readline()
                                compare_payload(json.loads(stored_line), {'name': name, **payload})
                                assert stored_line == line, ('noncanonical archive encoding', name)
                            allowed = {q: mask for q, mask in masks.items() if not mask & (1023 ^ target)}
                            possible = 0
                            for mask in allowed.values():
                                possible |= mask
                            missing = target & ~possible
                            assert missing, (name, 'no exclusion')
                            missing_i = next(i for i in range(10) if missing & (1 << i))
                            # A per-orbit implication witness: every P orbit that
                            # reaches the chosen positive row reaches a forbidden row.
                            implications = {}
                            for q, mask in masks.items():
                                if mask & (1 << missing_i):
                                    forbidden_i = next(i for i in range(10)
                                                       if mask & (1 << i) and not target & (1 << i))
                                    implications[q] = tk.B_ROWS[forbidden_i]
                            records.append({'name': name, 'kind': kind, 'pair': pair,
                                            'variable_side': side, 'singleton_slot': slot,
                                            'original_query': query, 'e': e, 'target': target,
                                            'graph': graph, 'fixed_kernel_J': patch[0],
                                            'fixed_kernel_U': patch[1],
                                            'row_full_lift_counts': row_counts,
                                            'row_empty_literal_fibre_counts': empty_counts,
                                            'D_orbit_B_masks': masks,
                                            'allowed_D_orbits': allowed,
                                            'maximal_allowed_B_mask': possible,
                                            'missing_target_mask': missing,
                                            'chosen_missing_B_row': tk.B_ROWS[missing_i],
                                            'orbit_forbidden_row_witnesses': implications,
                                            'archive_record_sha256': hashlib.sha256(line).hexdigest(),
                                            'source_status': 'excluded by exact exterior for every S4-invariant L relation'})
                            counts['exteriors'] += 1
                            counts['full_P_lifts'] += sum(row_counts.values())
                            counts['explicit_empty_B_D_fibres'] += sum(empty_counts.values())
                            counts['chosen_missing_'+tk.B_ROWS[missing_i]] += 1
                            if slot in (0, 4):
                                if e not in chord_cache:
                                    g, _, _, _, d = exterior(kind, pair, side, slot, e)
                                    rows = {beta: chord_control(g, d, slot, beta,
                                                               payload['complete_B_D_fibres'][beta])
                                            for beta in tk.B_ROWS}
                                    chord_cache[e] = rows
                                rows = chord_cache[e]
                                sigma = sum(1 << i for i, beta in enumerate(tk.B_ROWS) if rows[beta])
                                # The minimum-degree filtering is separate from
                                # this full-plane control: retain whichever Sigma occurs.
                                chord_records.append({'name': name+'-endpoint-ear', 'Sigma': sigma,
                                                      'row_full_lift_counts': {b: len(v) for b,v in rows.items()},
                                                      'complete_full_lifts_sha256': hashlib.sha256(encode(rows)).hexdigest()})
                                assert sigma != target
                                counts['chord_calibrations'] += 1
                            if negative and negative_result is None and kind == 'BRIDGE':
                                negative_result = rejection_controls(payload, graph, kernel)
                        print(json.dumps({'completed_kind': kind, 'pair': pair,
                                          'variable_side': side, 'slot': slot,
                                          'verified_exteriors': counts['exteriors']}), flush=True)
        if not write:
            assert stream.read() == b'', 'extra archive records'
    certificate = {'schema': 1, 'domain': 'h=3; p in {1,2}; s=1; arbitrary remaining original C6 disk',
                   'frozen_kernel_checker_sha256': hashlib.sha256(KCHECK.read_bytes()).hexdigest(),
                   'frozen_kernel_archive_sha256': hashlib.sha256(KARCHIVE.read_bytes()).hexdigest(),
                   'B_rows': tk.B_ROWS, 'proper_D_S4_orbits': ORBITS,
                   'literal_D_assignments_per_B_row': 4096,
                   'exteriors': records, 'chord_calibrations': chord_records,
                   'archive_uncompressed_sha256': all_archive_hash.hexdigest(),
                   'summary': dict(sorted(counts.items())),
                   'theorem': 'All 640 anchored exteriors exclude their original target 933 or 941 for every S4-invariant remaining-D relation.'}
    if write:
        with CERTIFICATE.open('xb') as raw:
            with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as out:
                out.write((json.dumps(certificate, sort_keys=True, indent=2)+'\n').encode())
    else:
        with gzip.open(CERTIFICATE, 'rt') as source:
            assert normalized(certificate) == json.load(source), 'certificate mismatch'
    if negative:
        assert negative_result is not None
    print(json.dumps({'status': 'PASS', **dict(sorted(counts.items())),
                      'explicit_B_D_fibres': counts['exteriors'] * 10 * 4096,
                      'semantic_negative_controls': 8 if negative else 0,
                      'source_exclusions': counts['exteriors'],
                      'remaining_C6_interior_size_bound': None}, sort_keys=True))


def negative_only():
    """Validate fresh actual P against archive, then use its actual parser on mutations."""
    kernel = get_kernel()
    kind, pair, side, slot = 'BRIDGE', 0, 0, 0
    query, e, target = tk.QUERIES[0]
    name = f'{kind}-{pair}-{side}-{slot}-{query}'
    payload, graph, masks, row_counts, empty_counts, patch = compute_exterior(
        kind, pair, side, slot, e, kernel)
    found = False
    with gzip.open(ARCHIVE, 'rb') as source:
        for line in source:
            stored = json.loads(line)
            if stored['name'] == name:
                compare_payload(stored, {'name': name, **payload})
                found = True
                break
    assert found, 'missing anchored archive record'
    controls = rejection_controls(payload, graph, kernel)
    print(json.dumps({'status': 'PASS', 'mode': 'negative-only',
                      'fresh_direct_and_kernel_exterior': name,
                      'semantic_negative_controls': len(controls),
                      'controls': controls}, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--negative-only', action='store_true')
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    if args.negative_only:
        negative_only()
    else:
        run(write=args.write, negative=args.negative)
