#!/usr/bin/env python3
"""Exact remaining C6 cap enumeration and complete same-frame fibre replay.

The complete embedding domain depends on frozen plantri.  Outputs are exclusive;
--check regenerates the domain, complete fibres and original C8 intersections.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
COLOURS = tuple(range(4))


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canon(row):
    frame = list(dict.fromkeys(row))
    normal = tuple(frame.index(c) for c in row)
    # Missing colours can occur on private vertices: keep a TOTAL bijection.
    frame.extend(c for c in COLOURS if c not in frame)
    return normal, tuple(frame)


def proper(row):
    return all(row[i] != row[(i + 1) % len(row)] for i in range(len(row)))


def faces(rotation):
    seen, result = set(), []
    for u, ns in enumerate(rotation):
        for v in ns:
            if (u, v) in seen:
                continue
            a, b, face = u, v, []
            while (a, b) not in seen:
                seen.add((a, b))
                face.append(a)
                a, b = b, rotation[b][(rotation[b].index(a) + 1) % len(rotation[b])]
            assert (a, b) == (u, v)
            result.append(face)
    return result


def parse(line):
    n, words = line.split()
    rotation = [[ord(x) - ord('a') for x in word] for word in words.split(',')]
    assert int(n) == len(rotation) == 12
    return rotation


def fibre(rotation, literal, tie_order):
    colours = dict(enumerate(literal))
    result = []
    ranks = {v: i for i, v in enumerate(tie_order)}

    def rec(remaining):
        if not remaining:
            result.append(tuple(colours[v] for v in range(6, 12)))
            return
        v = max(remaining, key=lambda x: (sum(u in colours for u in rotation[x]),
                                         len(rotation[x]), ranks[x]))
        forbidden = {colours[u] for u in rotation[v] if u in colours}
        for c in COLOURS:
            if c not in forbidden:
                colours[v] = c
                rec(remaining - {v})
                del colours[v]

    if any(literal[u] == literal[v] for u in range(6) for v in rotation[u] if v < 6):
        return []
    rec(set(range(6, 12)))
    return sorted(result)


def load_inputs():
    manifest = json.loads((AUDIT / 'INPUTS.json').read_text())
    hashes = {}
    for record in manifest['inputs']:
        data = (AUDIT / 'frozen' / record['path']).read_bytes()
        assert len(data) == record['bytes']
        assert sha(data) == record['sha256']
        hashes[record['path']] = record['sha256']
    frozen = AUDIT / 'frozen'
    prior = json.loads(gzip.decompress(next(frozen.rglob('CERTIFICATE.json.gz')).read_bytes()))
    interface = json.loads(next((frozen / 'predecessor-authority').rglob('interface.json')).read_text())
    source = json.loads(next((frozen / 'predecessor-authority').rglob('RESULTS.json')).read_text())
    rows = interface['pattern_order']
    queries = [q for q in source['queries'] if q['status'] == 'necessary_condition_residual']
    assert rows == prior['original_C8_pattern_order']
    assert queries == prior['original_U_queries']
    assert rows == [list(row) for row in sorted({canon(x)[0] for x in itertools.product(COLOURS, repeat=8) if proper(x)})]
    assert len(rows) == 274 and len(queries) == 8
    literals = interface['literal_assignments']
    literal_indices = interface['literal_to_pattern']
    assert literals == [list(x) for x in itertools.product(COLOURS, repeat=8) if proper(x)]
    frames = []
    for literal, p in zip(literals, literal_indices):
        norm, frame = canon(literal)
        assert list(norm) == rows[p]
        frames.append(frame)
    assert len(literals) == len(literal_indices) == 6564
    literal_codec = {'literal_order': literals, 'canonical_indices': literal_indices,
                     'canonical_to_literal_total_permutations': frames,
                     'decoder': 'For literal l, take canonical fibre at canonical_indices[l]; replace each private colour c by canonical_to_literal_total_permutations[l][c] and sort the resulting tuples. This includes every empty fibre and every complete lift in the literal row frame.',
                     'digest_encoding': 'For l=0..6563, append compact sorted-key JSON [l,decoded_fibre] followed by ASCII newline to SHA256.'}
    return manifest, hashes, rows, queries, literal_codec


def make_cap(index, source, patterns, rows, queries, literal_codec, rng):
    outer = next(face for face in faces(source) if len(face) == 6)
    private = sorted(set(range(12)) - set(outer))
    order = outer + private
    rename = {old: new for new, old in enumerate(order)}
    rotation = [[rename[v] for v in source[u]] for u in order]
    edges = sorted((u, v) for u, ns in enumerate(rotation) for v in ns if u < v)
    deep = [v for v in range(6, 12) if all(u >= 6 for u in rotation[v])]
    core_edges = [(u, v) for u, v in edges if u >= 6]
    ties = list(range(6, 12))
    rng.shuffle(ties)
    c6_fibres = [fibre(rotation, row, ties) for row in patterns]
    c6_index = {row: p for p, row in enumerate(patterns)}
    cap = {'cap_id': f'cap-{index:05d}', 'source_line_index_0based': index,
           'source_rotation': source, 'source_outer_face': outer,
           'old_to_named': [rename[v] for v in range(12)],
           'rotation': rotation, 'edges': edges,
           'named_boundary': list(range(6)), 'private_order': list(range(6, 12)),
           'boundary_degrees': [len(rotation[v]) for v in range(6)],
           'private_degrees': [len(rotation[v]) for v in range(6, 12)],
           'core_edges': core_edges,
           'boundary_private_edges': [(u, v) for u, v in edges if u < 6 <= v],
           'core_type': 'deep_W5' if deep else 'maximal_outerplane',
           'deep_centers': deep,
           'deep_wheel_rings': [rotation[v] for v in deep],
           'all_31_C6_fibres': c6_fibres,
           'C6_support_indices': [p for p, f in enumerate(c6_fibres) if f],
           'attachments': []}
    assert len(edges) == 27
    assert all(d >= 5 for d in cap['private_degrees'])
    if not deep:
        assert len(core_edges) == 9
        assert cap['private_degrees'] == [5] * 6
    for eq in range(8):
        pair = [eq, (eq + 2) % 8]
        long = [eq] + [(eq + j) % 8 for j in range(3, 8)]
        for direction in (1, -1):
            for shift in range(6):
                mapping = [long[(shift + direction * j) % 6] for j in range(6)]
                inverse = [-1] * 8
                for j, original in enumerate(mapping):
                    inverse[original] = j
                inverse[pair[1]] = inverse[pair[0]]
                full, transfers = [], []
                for p, row in enumerate(rows):
                    if row[pair[0]] != row[pair[1]]:
                        full.append([])
                        continue
                    literal = tuple(row[v] for v in mapping)
                    norm, frame = canon(literal)
                    idx = c6_index[norm]
                    lifted = sorted(tuple(frame[c] for c in lift) for lift in c6_fibres[idx])
                    # A second whole-cap DFS checks the total colour-frame pullback.
                    assert lifted == fibre(rotation, literal, ties)
                    full.append(lifted)
                    transfers.append({'original_C8_index': p, 'literal_cap_C6_row': literal,
                                      'normalized_C6_index': idx,
                                      'normalized_to_original_total_colour_permutation': frame})
                intersections = []
                for query in queries:
                    selected = [p for p, f in enumerate(full) if f and query['support'] >> p & 1]
                    witness = None if not selected else {
                        'original_C8_index': selected[0], 'original_C8_row': rows[selected[0]],
                        'private_lift': full[selected[0]][0]}
                    intersections.append({'query_id': query['query_id'],
                                          'original_C8_indices': selected,
                                          'first_witness': witness})
                literal_digest = hashlib.sha256()
                literal_lifts = 0
                for li, (p, frame) in enumerate(zip(literal_codec['canonical_indices'],
                                                   literal_codec['canonical_to_literal_total_permutations'])):
                    decoded = sorted(tuple(frame[c] for c in lift) for lift in full[p])
                    literal_digest.update(encoded([li, decoded]) + b'\n')
                    literal_lifts += len(decoded)
                cap['attachments'].append({
                    'attachment_id': f"{cap['cap_id']}:eq{eq}:dir{direction}:shift{shift}",
                    'short_eq_index': eq, 'identified_original_pair': pair,
                    'long_pocket_original_order': long, 'direction': direction, 'shift': shift,
                    'cap_boundary_to_original': mapping, 'original_C8_to_cap_boundary': inverse,
                    'private_original_order': list(range(8, 14)),
                    'all_92_Eq_row_transfers': transfers, 'all_274_C8_fibres': full,
                    'all_6564_literal_fibres_sha256': literal_digest.hexdigest(),
                    'literal_fibre_count': 6564, 'literal_lift_count': literal_lifts,
                    'C8_support_indices': [p for p, f in enumerate(full) if f],
                    'query_intersections': intersections})
    return cap


def produce(seed):
    manifest, hashes, rows, queries, literal_codec = load_inputs()
    patterns = sorted({canon(row)[0] for row in itertools.product(COLOURS, repeat=6) if proper(row)})
    assert len(patterns) == 31
    vendor = AUDIT / 'frozen/audits/2026-10-13-c8-joint-gadgets-6943561/search/vendor'
    with tempfile.TemporaryDirectory(prefix='c6-six-caps-') as scratch:
        binary = Path(scratch) / 'plantri'
        generated = Path(scratch) / 'all-c6-n12.ascii'
        subprocess.run(['cc', '-O3', '-o', str(binary), str(vendor / 'plantri.c')], check=True)
        subprocess.run([str(binary), '-aP6c2m2', '12', str(generated)],
                       check=True, capture_output=True)
        raw = generated.read_bytes()
    counts, candidates = collections.Counter(), []
    for index, line in enumerate(raw.decode().splitlines()):
        rotation = parse(line)
        fs = faces(rotation)
        outer_faces = [f for f in fs if len(f) == 6]
        assert len(outer_faces) == 1 and len(fs) == 17
        assert all(len(f) in (3, 6) for f in fs)
        outer = outer_faces[0]
        bs = set(outer)
        boundary_edges = {tuple(sorted((outer[j], outer[(j + 1) % 6]))) for j in range(6)}
        chords = {(min(u, v), max(u, v)) for u in outer for v in rotation[u]
                  if v in bs and tuple(sorted((u, v))) not in boundary_edges}
        counts['all_disk_embeddings'] += 1
        if chords:
            counts['boundary_chord_rejected'] += 1
            continue
        counts['chordless_embeddings'] += 1
        private = set(range(12)) - bs
        if any(len(rotation[v]) < 5 for v in private):
            counts['private_degree_below_five_rejected'] += 1
            continue
        candidates.append((index, rotation))
    rng = random.Random(seed)
    rng.shuffle(candidates)
    caps = [make_cap(index, rotation, patterns, rows, queries, literal_codec, rng) for index, rotation in candidates]
    caps.sort(key=lambda cap: cap['source_line_index_0based'])
    for cap in caps:
        counts[cap['core_type']] += 1
    counts['accepted_caps'] = len(caps)
    result = {'schema': 'c6-six-private-complete-caps-v1', 'base': manifest['base'],
              'input_sha256': hashes, 'colour_frame': list(COLOURS),
              'original_C8_pattern_order': rows, 'original_U_queries': queries,
              'C8_literal_expansion': literal_codec,
              'C6_pattern_order': patterns,
              'generator': {'command': 'plantri -aP6c2m2 12',
                            'raw_count': counts['all_disk_embeddings'], 'raw_bytes': len(raw),
                            'raw_sha256': sha(raw), 'raw_gzip': 'all-c6-n12.ascii.gz',
                            'completeness_dependency': 'Frozen plantri generator and disk mode guide; no independent generator claim.'},
              'filter_counts': dict(counts), 'caps': caps,
              'attachment_count': sum(len(c['attachments']) for c in caps),
              'attachment_convention': 'cap boundary j maps to long_pocket_original_order[(shift+direction*j)%6]; all 12 alignments, including mirror, are retained with duplicates. Both Eq pins share the same cap pin. The omitted digon pin remains in every original C8 row.',
              'fibre_convention': 'Each stored fibre is the complete sorted list of six private colours. Empty fibres are explicit. C6 private order is 6..11; C8 attachment private order is 8..13 in the same order. All C8 tuples use exactly the original canonical C8 row colour frame. The transfer colour permutation is total on 0..3.',
              'four_colour_theorem_assumed': False, 'new_Lean_theorem': False,
              'source_realizability': 'OPEN', 'general_theorem': 'OPEN'}
    summary = {'schema': 'c6-six-private-summary-v1', 'filter_counts': dict(counts),
               'caps': [{'cap_id': c['cap_id'], 'core_type': c['core_type'],
                         'C6_support_size': len(c['C6_support_indices']),
                         'C6_fibre_lift_count': sum(map(len, c['all_31_C6_fibres']))} for c in caps],
               'attachment_count_with_duplicates': result['attachment_count'],
               'complete_C6_fibres': len(caps) * 31,
               'complete_C8_fibres': result['attachment_count'] * 274,
               'complete_C8_lifts': sum(len(f) for c in caps for a in c['attachments'] for f in a['all_274_C8_fibres']),
               'complete_C8_literal_fibres_via_lossless_codec': result['attachment_count'] * 6564,
               'complete_C8_literal_lifts_via_lossless_codec': sum(a['literal_lift_count'] for c in caps for a in c['attachments']),
               'newly_excluded': [], 'query_results': [],
               'generator_completeness_dependency_retained': True,
               'source_realizability': 'OPEN', 'general_theorem': 'OPEN',
               'new_Lean_theorem': False}
    for qi, query in enumerate(queries):
        cells = [(cap, a, a['query_intersections'][qi]) for cap in caps for a in cap['attachments']]
        minimum = min(len(cell['original_C8_indices']) for _, _, cell in cells)
        attaining = [{'attachment_id': a['attachment_id'], 'original_C8_indices': cell['original_C8_indices'],
                      'first_witness': cell['first_witness']} for c, a, cell in cells
                     if len(cell['original_C8_indices']) == minimum]
        singleton = [x for x in attaining if minimum == 1]
        summary['query_results'].append({'query_id': query['query_id'],
                                         'minimum_original_C8_intersection': minimum,
                                         'attaining_attachments': attaining,
                                         'singleton_intersections': singleton,
                                         'singleton_forced_original_indices': sorted({x['original_C8_indices'][0] for x in singleton})})
        if minimum == 0:
            summary['newly_excluded'].append(query['query_id'])
    result['summary'] = summary
    return json.loads(encoded(result)), json.loads(encoded(summary)), raw


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    certificate, summary, raw = produce(args.seed)
    outputs = {'CERTIFICATE.json.gz': gzip.compress(encoded(certificate), mtime=0),
               'RESULTS.json': (json.dumps(summary, indent=2, sort_keys=True) + '\n').encode(),
               'all-c6-n12.ascii.gz': gzip.compress(raw, mtime=0)}
    if args.check:
        assert json.loads(gzip.decompress((HERE / 'CERTIFICATE.json.gz').read_bytes())) == certificate
        assert json.loads((HERE / 'RESULTS.json').read_text()) == summary
        assert gzip.decompress((HERE / 'all-c6-n12.ascii.gz').read_bytes()) == raw
    else:
        assert not any((HERE / name).exists() for name in outputs)
        for name, data in outputs.items():
            with (HERE / name).open('xb') as target:
                target.write(data)
    print(json.dumps({'status': 'PASS', 'mode': 'check' if args.check else 'write', 'seed': args.seed,
                      'certificate_sha256': sha(encoded(certificate)), 'counts': summary['filter_counts'],
                      'attachments': summary['attachment_count_with_duplicates'],
                      'complete_C8_fibres': summary['complete_C8_fibres'],
                      'complete_C8_lifts': summary['complete_C8_lifts'],
                      'minimum_intersections': {q['query_id']: q['minimum_original_C8_intersection'] for q in summary['query_results']},
                      'newly_excluded': summary['newly_excluded']}, sort_keys=True))


if __name__ == '__main__':
    main()
