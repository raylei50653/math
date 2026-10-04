#!/usr/bin/env python3
"""Export the 179 ES representatives into independently checked Lean data.

Only new files are written, using exclusive creation. --check regenerates all
three outputs in memory, reaudits the fixed source corpus, and compares every byte.
No ES implementation, planarity package, or four-colour-theorem oracle is used.
Lean checks the exported inputs independently; this Python audit establishes no
claim that the ES enumeration contains every possible orbit.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE_GLOB = 'artifacts/c5_excess_two_finite_search/*_validate/crit_orbits/orbit_*.json'
LEAN_OUTPUT = ROOT / 'Math/GeneratedExcessTwoCertificates.lean'
AUDIT_OUTPUT = ROOT / 'Math/ExcessTwoCertificatesAudit.lean'
INVENTORY_OUTPUT = ROOT / 'artifacts/c5_excess_two_lean_certificates/source_inventory.json'
ROWS = (
    (0, 1, 0, 1, 2), (0, 1, 0, 2, 1), (0, 1, 0, 2, 3),
    (0, 1, 2, 0, 1), (0, 1, 2, 0, 2), (0, 1, 2, 0, 3),
    (0, 1, 2, 1, 2), (0, 1, 2, 1, 3), (0, 1, 2, 3, 1),
    (0, 1, 2, 3, 2),
)
FRAME_EDGES = frozenset(((0, 1), (0, 4), (1, 2), (2, 3), (3, 4)))
REJECTION_ROWS = (6, 4, 3, 1, 0)
EXPECTED_BUCKETS = {
    'AD_k3_validate': 1, 'AD_k6_validate': 2, 'AD_k7_validate': 1,
    'AD_k9_validate': 5, 'D6_k4_validate': 2, 'D6_k5_validate': 9,
    'D6_k6_validate': 4, 'D6_k7_validate': 25, 'D6_k8_validate': 41,
    'D6_k9_validate': 35, 'NA_k6_validate': 3, 'NA_k7_validate': 2,
    'NA_k8_validate': 22, 'NA_k9_validate': 27,
}
SOURCE_KEYS = frozenset((
    'Q', 'Q_plus_cQ', 'accepted_colourings', 'c_Q', 'canonical_edges',
    'contains_941_triple', 'degrees', 'deletion_sigmas', 'embedding',
    'epsilon', 'orbit_size', 'sigma_mask', 'stabilizer_size', 'structure',
))


class SourceError(ValueError):
    """A source-record invariant failed before any generated output was written."""


def require(condition, message):
    if not condition:
        raise SourceError(message)


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def ints(values, minimum, maximum):
    return isinstance(values, list) and all(
        type(value) is int and minimum <= value < maximum for value in values)


def coloring_valid(colors, row, n, edges):
    return (ints(colors, 0, 4) and len(colors) == n and
            tuple(colors[:5]) == ROWS[row] and
            all(colors[a] != colors[b] for a, b in edges))


def extends(adjacency, n, row):
    """Independent MRV decision, using the literal common four-colour frame."""
    colors = dict(enumerate(ROWS[row]))

    def visit():
        if len(colors) == n:
            return True
        choices = []
        for vertex in range(5, n):
            if vertex in colors:
                continue
            options = tuple(color for color in range(4)
                            if all(colors.get(other) != color
                                   for other in adjacency[vertex]))
            if not options:
                return False
            choices.append((len(options), -len(adjacency[vertex]), vertex, options))
        _, _, vertex, options = min(choices)
        for color in options:
            colors[vertex] = color
            if visit():
                del colors[vertex]
                return True
        del colors[vertex]
        return False

    return visit()


def rotation_faces(rotation, edges):
    """Partition all directed darts under (u,v) -> (v,pred_v(u))."""
    remaining = {dart for edge in edges for dart in (edge, edge[::-1])}
    faces = []
    while remaining:
        start = min(remaining)
        dart = start
        face = []
        while not face or dart != start:
            require(dart in remaining, 'face successor repeated a noninitial dart')
            remaining.remove(dart)
            u, v = dart
            face.append(u)
            ring = rotation[v]
            incoming = ring.index(u)
            dart = (v, ring[(incoming - 1) % len(ring)])
        faces.append(face)
    return faces


def read_sources():
    paths = sorted(ROOT.glob(SOURCE_GLOB))
    require(len(paths) == 179, f'expected 179 source orbit files, found {len(paths)}')
    require(Counter(path.parent.parent.name for path in paths) == EXPECTED_BUCKETS,
            'fixed source bucket counts differ from the 179-orbit LC scope')
    records = []
    corpus = sha256()
    counts = Counter()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        try:
            raw = path.read_bytes()
            record = json.loads(raw)
            require(isinstance(record, dict) and set(record) == SOURCE_KEYS,
                    'unexpected source-record keys')
            bucket = path.parent.parent.name
            kind, size = bucket.removesuffix('_validate').split('_k')
            require(kind in ('NA', 'AD', 'D6'), 'unknown degree type')
            k = int(size)
            n = 5 + k
            edge_values = record['canonical_edges']
            require(isinstance(edge_values, list) and all(
                ints(edge, 0, n) and len(edge) == 2 and edge[0] < edge[1]
                for edge in edge_values), 'malformed canonical edge endpoints')
            edge_list = tuple(map(tuple, edge_values))
            edges = frozenset(edge_list)
            require(edge_list == tuple(sorted(edges)), 'edges are not strictly canonical')
            require({edge for edge in edges if edge[1] < 5} == FRAME_EDGES,
                    'boundary is not the exact induced C5')
            adjacency = [set() for _ in range(n)]
            for u, v in edges:
                adjacency[u].add(v)
                adjacency[v].add(u)
            degrees = [len(adjacency[v]) for v in range(5, n)]
            target = ([6] + [4] * (k - 1) if kind == 'D6'
                      else [5, 5] + [4] * (k - 2))
            require(degrees == target == record['degrees'], 'actual prescribed degree failed')
            require(sum(degree - 4 for degree in degrees) == record['epsilon'] == 2,
                    'actual excess is not two')
            require(all(sum(other < 5 for other in adjacency[v]) <= 3
                        for v in range(5, n)), 'more than three spokes at an interior vertex')
            require(kind == 'D6' or ((6 in adjacency[5]) == (kind == 'AD')),
                    'degree-five root adjacency does not match NA/AD')
            seen = {5}
            for _ in range(k):
                seen |= {v for u in seen for v in adjacency[u] if v >= 5}
            require(seen == set(range(5, n)), 'interior graph is disconnected')
            mask = record['sigma_mask']
            require(type(mask) is int and 0 <= mask < 1024 and mask & 932 == 932,
                    'invalid sigma mask or missing T4 row')
            q = [point for point, row in enumerate(REJECTION_ROWS)
                 if not (mask >> row) & 1]
            components = (1 if len(q) == 5 else
                          len(q) - sum(i in q and (i + 1) % 5 in q for i in range(5)))
            require(record['Q'] == q and q, 'wrong or empty named Q')
            require(record['c_Q'] == components and
                    record['Q_plus_cQ'] == len(q) + components <= 4,
                    'wrong Q components or rejection bound')
            accepted = record['accepted_colourings']
            require(isinstance(accepted, dict) and set(accepted) ==
                    {str(row) for row in range(10) if (mask >> row) & 1},
                    'accepted witness keys do not equal mask bits')
            for row in range(10):
                if (mask >> row) & 1:
                    require(coloring_valid(accepted[str(row)], row, n, edges),
                            f'accepted row {row} has an invalid direct witness')
                    counts['accepted_witnesses'] += 1
                else:
                    require(not extends(adjacency, n, row),
                            f'rejected row {row} actually extends')
                    counts['rejected_rows'] += 1
            deletions = record['deletion_sigmas']
            require(isinstance(deletions, list), 'deletion records are not a list')
            deletion_edges = []
            for deletion in deletions:
                require(set(deletion) == {'edge', 'new_indices', 'sigma_mask', 'witnesses'},
                        'unexpected deletion-record keys')
                require(ints(deletion['edge'], 0, n) and len(deletion['edge']) == 2,
                        'malformed deletion edge')
                edge = tuple(deletion['edge'])
                deletion_edges.append(edge)
                require(edge in edges - FRAME_EDGES, 'deletion names a frame or absent edge')
                deletion_mask = deletion['sigma_mask']
                require(type(deletion_mask) is int and 0 <= deletion_mask < 1024 and
                        deletion_mask & mask == mask and deletion_mask != mask,
                        'deletion mask has no strict gain')
                new_rows = [row for row in range(10)
                            if ((deletion_mask & ~mask) >> row) & 1]
                require(deletion['new_indices'] == new_rows, 'wrong deletion new_indices')
                witnesses = deletion['witnesses']
                require(isinstance(witnesses, list) and len(witnesses) == len(new_rows) and
                        [witness['pattern_index'] for witness in witnesses] == new_rows,
                        'deletion witnesses do not cover each claimed new row once')
                for witness in witnesses:
                    require(set(witness) == {'pattern_index', 'colouring'},
                            'unexpected deletion-witness keys')
                    row = witness['pattern_index']
                    colors = witness['colouring']
                    require(coloring_valid(colors, row, n, edges - {edge}) and
                            colors[edge[0]] == colors[edge[1]],
                            f'invalid direct deletion witness for edge {edge}, row {row}')
                    counts['deletion_witnesses'] += 1
            require(deletion_edges == sorted(edges - FRAME_EDGES),
                    'deletion records do not cover every nonframe edge exactly once')
            counts['nonframe_edges'] += len(deletion_edges)
            embedding = record['embedding']
            require(isinstance(embedding, dict) and set(embedding) ==
                    {'apex', 'augmented_rotation', 'disk_rotation', 'outer_face'},
                    'unexpected embedding-record keys')
            require(embedding['apex'] == n, 'wrong augmentation apex label')
            rings = embedding['disk_rotation']
            require(isinstance(rings, dict) and set(rings) == {str(v) for v in range(n)},
                    'rotation vertex labels do not cover the graph exactly')
            rotation = [rings[str(v)] for v in range(n)]
            require(all(ints(ring, 0, n) and len(ring) == len(set(ring)) and
                        set(ring) == adjacency[v] for v, ring in enumerate(rotation)),
                    'rotation ring is not the exact duplicate-free neighbor list')
            faces = rotation_faces(rotation, edges)
            require(n + len(faces) == len(edges) + 2, 'Euler equation failed')
            outer = embedding['outer_face']
            require(outer in ([0, 1, 2, 3, 4], [0, 4, 3, 2, 1]),
                    'outer face is not an oriented frame C5')
            require(any(outer == face[i:] + face[:i]
                        for face in faces for i in range(len(face))),
                    'recorded outer frame is not an actual rotation face')
            corpus.update(raw)
            records.append({
                'path': relative, 'sha256': sha256(raw).hexdigest(), 'size_bytes': len(raw),
                'kind': kind, 'k': k, 'orbit': int(path.stem.removeprefix('orbit_')),
                'record': record, 'rotation': rotation, 'faces': faces,
            })
        except (SourceError, KeyError, TypeError, ValueError, IndexError) as error:
            raise SourceError(f'{relative}: {error}') from error
    require(counts == {'accepted_witnesses': 1597, 'rejected_rows': 193,
                       'nonframe_edges': 4138, 'deletion_witnesses': 4271},
            f'fixed corpus witness counts changed: {dict(counts)}')
    return records, corpus.hexdigest(), dict(sorted(counts.items()))


def lean_list(values):
    return '[' + ','.join(str(value) for value in values) + ']'


def lean_edges(values):
    return '[' + ','.join(f'({u},{v})' for u, v in values) + ']'


def lean_rings(values):
    return '[' + ','.join(lean_list(value) for value in values) + ']'


def cert_name(source):
    return f"cert_{source['kind'].lower()}_k{source['k']}_orbit_{source['orbit']:04d}"


def render_lean(records):
    lines = [
        '/-', 'Copyright (c) 2026 raylei50653. All rights reserved.',
        'Released under Apache 2.0 license as described in the file LICENSE.',
        'Authors: raylei50653', '-/', 'import Math.ExcessTwoCertificates', '',
        '/-! Generated by scripts/export_excess_two_certificates.py.',
        'Each supplied ES representative has a kernel positive check and a native rejection check.',
        'Their ordinary composition proves soundness, with no enumeration-completeness claim.',
        'See docs/c5_excess_two_lean_certificates.md for the compiler trust boundary. -/',
        'set_option linter.style.nativeDecide false',
        'set_option linter.style.setOption false',
        'set_option Elab.async false',
        'set_option maxHeartbeats 0', 'set_option maxRecDepth 100000', '',
        'namespace FiveBoundary.ExcessTwo.Generated', '',
    ]
    for source in records:
        record = source['record']
        name = cert_name(source)
        lines.extend([
            f"-- Source: {source['path']}",
            f"-- Source SHA-256: {source['sha256']}",
            f'def {name} : Certificate := {{',
            f"  k := {source['k']}",
            f"  edges := {lean_edges(record['canonical_edges'])}",
            f"  kind := .{source['kind'].lower()}",
            f"  sigmaMask := {record['sigma_mask']}",
            f"  q := {lean_list(record['Q'])}",
            f"  qComponents := {record['c_Q']}",
            '  rotation := {',
            f"    rotation := {lean_rings(source['rotation'])}",
            f"    faces := {lean_rings(source['faces'])}",
            f"    outerFace := {lean_list(record['embedding']['outer_face'])} }}",
            '  accepted := fun i => match i.val with',
        ])
        for row, coloring in sorted(record['accepted_colourings'].items(), key=lambda item: int(item[0])):
            lines.append(f'    | {row} => some !{lean_list(coloring)}')
        lines.append('    | _ => none')
        lines.append('  deletions := [')
        deletion_lines = []
        for deletion in record['deletion_sigmas']:
            witnesses = ','.join(
                f"{{ row := {witness['pattern_index']}, coloring := !{lean_list(witness['colouring'])} }}"
                for witness in deletion['witnesses'])
            u, v = deletion['edge']
            deletion_lines.append(f'    {{ edge := ({u},{v}), witnesses := [{witnesses}] }}')
        lines.append(',\n'.join(deletion_lines))
        lines.extend([
            '  ]', '}',
            f'theorem {name}_positive : checkPositive {name} = true := by decide +kernel',
            f'theorem {name}_rejected : checkRejected {name} = true := by native_decide',
            f'theorem {name}_valid : check {name} = true :=',
            f'  check_from_parts {name} {name}_positive {name}_rejected', '',
        ])
    names = [cert_name(source) for source in records]
    lines.extend(['def certificates : List Certificate := [',
                  ',\n'.join(f'  {name}' for name in names), ']', '',
                  'theorem certificate_count : certificates.length = 179 := by decide +kernel', '',
                  'theorem all_certificates_valid : certificates.all check = true := by',
                  '  simp only [certificates, List.all_cons, List.all_nil,',
                  ',\n'.join(f'    {name}_valid' for name in names) + ', Bool.and_self]', '',
                  'theorem all_certificates_sound (c : Certificate) (hc : c ∈ certificates) :',
                  '    CertificateFacts c :=',
                  '  check_sound c ((List.all_eq_true.mp all_certificates_valid) c hc)', '',
                  'end FiveBoundary.ExcessTwo.Generated', ''])
    raw = '\n'.join(lines).encode()
    require(len(raw) < 1_000_000,
            f'generated Lean output exceeds the unregistered 1 MB limit: {len(raw)} bytes')
    return raw


def render_audit(records):
    lines = [
        '/-', 'Copyright (c) 2026 raylei50653. All rights reserved.',
        'Released under Apache 2.0 license as described in the file LICENSE.',
        'Authors: raylei50653', '-/', 'import Math.GeneratedExcessTwoCertificates', '',
        '/-! Generated axiom audit. Print commands leave the imported proof terms unchanged.',
        'Kernel positive checks, native rejection certificates, and the inherited native',
        'colour-orbit cover are deliberately listed separately. -/', '',
        'namespace FiveBoundary.ExcessTwo', '',
    ]
    for name in (
        'check_from_parts', 'check_finite_sound', 'check_sound', 'extends_iff_sigma',
        'accepted_sound', 'row_sound', 'boundaryRow_cover', 'rows_exact_sigma',
        'deletion_sound', 'reachInterior_sound', 'connectedInterior_sound',
        'checkShape_sound', 'checkShape_interior_paths', 'checkQ_sound',
        'checkRotation_sound', 'checkRotation_iff',
    ):
        lines.append(f'#print axioms {name}')
    lines.extend(['#print axioms FiveBoundary.edgeCheck_exact',
                  '#print axioms FiveBoundary.color_orbits_cover', '',
                  'namespace Generated', '',
                  '#print axioms certificate_count',
                  '#print axioms all_certificates_valid',
                  '#print axioms all_certificates_sound', ''])
    for source in records:
        name = cert_name(source)
        for suffix in ('positive', 'rejected', 'valid'):
            lines.append(f'#print axioms {name}_{suffix}')
    lines.extend(['', 'end Generated', 'end FiveBoundary.ExcessTwo', ''])
    return '\n'.join(lines).encode()


def generate_payloads():
    records, corpus_hash, counts = read_sources()
    lean = render_lean(records)
    audit = render_audit(records)
    inventory = {
        'schema': 'c5-excess-two-lean-source-inventory-v1',
        'scope': '179 supplied ES validate crit-orbit representatives; soundness only',
        'source_glob': SOURCE_GLOB,
        'source_count': len(records),
        'source_bytes': sum(source['size_bytes'] for source in records),
        'source_corpus_sha256': corpus_hash,
        'corpus_hash_convention': 'SHA256 of raw source bytes concatenated in sorted relative-path order',
        'bucket_counts': dict(sorted(EXPECTED_BUCKETS.items())),
        'finite_source_audit_counts': counts,
        'finite_source_audit_scope': [
            'exact induced C5; actual prescribed degrees, excess, spokes, and interior connectivity',
            'all accepted witness colorings; independent MRV absence checks for all rejected rows',
            'all named nonframe deletions; all supplied new-row witnesses checked directly',
            'exact neighbor rings; complete predecessor-dart face partition; Euler; actual outer C5 face',
        ],
        'lean_output': {
            'path': LEAN_OUTPUT.relative_to(ROOT).as_posix(),
            'sha256': sha256(lean).hexdigest(), 'size_bytes': len(lean),
            'module': 'Math.GeneratedExcessTwoCertificates',
            'certificate_theorems': len(records),
            'proof_method': 'decide +kernel positive checks; native_decide rejected rows; ordinary composition',
            'inherited_native_boundary': 'Enumeration.color_orbits_cover used only by complete raw Sigma bridge',
        },
        'audit_output': {
            'path': AUDIT_OUTPUT.relative_to(ROOT).as_posix(),
            'sha256': sha256(audit).hexdigest(), 'size_bytes': len(audit),
            'module': 'Math.ExcessTwoCertificatesAudit',
            'individual_axiom_prints': 3 * len(records),
        },
        'exporter': {
            'path': Path(__file__).resolve().relative_to(ROOT).as_posix(),
            'sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        'sources': [{key: source[key] for key in
                     ('path', 'sha256', 'size_bytes', 'kind', 'k', 'orbit')}
                    | {'lean_definition': cert_name(source)} for source in records],
    }
    return [(LEAN_OUTPUT, lean), (AUDIT_OUTPUT, audit),
            (INVENTORY_OUTPUT, json_bytes(inventory))], counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='recompute all three artifacts and require identical bytes without writing')
    args = parser.parse_args()
    try:
        payloads, counts = generate_payloads()
        if args.check:
            for path, expected in payloads:
                require(path.is_file(), f'missing replay target {path.relative_to(ROOT)}')
                require(path.read_bytes() == expected,
                        f'byte replay differs: {path.relative_to(ROOT)}')
                print(f'byte-exact: {path.relative_to(ROOT)} ({len(expected)} bytes)')
        else:
            require(all(not path.exists() for path, _ in payloads),
                    'generation requires absent targets; use --check for existing outputs')
            for path, raw in payloads:
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('xb') as stream:
                    stream.write(raw)
                print(f'exclusive-created: {path.relative_to(ROOT)} ({len(raw)} bytes)')
        print(f'179 representatives audited; {counts}')
        return 0
    except (SourceError, OSError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
