#!/usr/bin/env python3
"""Read-only frozen-input and complete-relation calibration audit; no LOW1 source search."""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COLORS = tuple(range(4))
ORDER = ('r', 'u', 'p', 'q', 't')
CONTACTS = ('q', 'p', 't')
INTERNAL = (('r', 'u'), ('r', 'p'), ('r', 't'), ('p', 'q'))
ATTACHMENTS = {'r': (4,), 'u': (0,), 'p': (1,), 'q': (2,), 't': (3,)}
SPOKES = (0, 1)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def inputs_check():
    inputs = json.loads((HERE / 'inputs.json').read_bytes())
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() != inputs['base']:
        raise ValueError('HEAD differs from BASE')
    for entry in inputs['files']:
        data = (HERE / entry['frozen']).read_bytes()
        if digest(data) != entry['sha256']:
            raise ValueError('frozen input digest mismatch: ' + entry['frozen'])
        if entry['kind'] in ('worker', 'current') and not entry['source'].startswith('docs/'):
            if digest((ROOT / entry['source']).read_bytes()) != entry['sha256']:
                raise ValueError('immutable original input drift: ' + entry['source'])
        if 'git_path' in entry:
            actual = subprocess.check_output(['git', 'show', inputs['base'] + ':' + entry['git_path']], cwd=ROOT)
            if actual != data:
                raise ValueError('BASE object mismatch: ' + entry['git_path'])
    return len(inputs['files'])


def lists_for(row, attachments=ATTACHMENTS):
    return {v: set(COLORS) - {row[i] for i in attachments[v]} for v in ORDER}


def direct_c(row, attachments=ATTACHMENTS, edges=INTERNAL):
    lists = lists_for(row, attachments)
    good = set()
    for values in itertools.product(COLORS, repeat=len(ORDER)):
        f = dict(zip(ORDER, values))
        if all(f[v] in lists[v] for v in ORDER) and all(f[x] != f[y] for x, y in edges):
            good.add(values)
    return good


def local_assignments(row):
    lists = lists_for(row)
    return {
        'U': {(u,) for u in lists['u']},
        'P': {(p, q) for p in lists['p'] for q in lists['q'] if p != q},
        'Q': {(t,) for t in lists['t']},
    }


def full_join(row):
    local = local_assignments(row)
    return {
        (r, u[0], p[0], p[1], t[0])
        for r in lists_for(row)['r']
        for u, p, t in itertools.product(local['U'], local['P'], local['Q'])
        if r != u[0] and r != p[0] and r != t[0]
    }


def direct_x(row):
    # Independently enumerate all six interior coordinates, including the one shared p.
    lists = lists_for(row)
    result = set()
    for values in itertools.product(COLORS, repeat=6):
        f = dict(zip(ORDER + ('s',), values))
        if not all(f[v] in lists[v] for v in ORDER):
            continue
        if f['s'] in {row[i] for i in SPOKES}:
            continue
        if not all(f[x] != f[y] for x, y in INTERNAL):
            continue
        if not all(f[v] != f['s'] for v in CONTACTS):
            continue
        result.add(values)
    return result


def normalized(values):
    names = {}
    return tuple(names.setdefault(v, len(names)) for v in values)


def rows():
    return sorted({normalized(row) for row in itertools.product(COLORS, repeat=5)
                   if all(row[i] != row[(i + 1) % 5] for i in range(5))})


def certificate():
    count = inputs_check()
    all_rows = rows()
    if len(all_rows) != 10:
        raise ValueError('canonical row count')
    records = []
    global_color_checks = 0
    whole_d5_checks = 0
    skip_u_detected = 0
    for row in all_rows:
        direct = direct_c(row)
        joined = full_join(row)
        if joined != direct:
            raise ValueError('full common-r join differs from direct full coloring')
        query = {f + (s,) for f in joined for s in COLORS
                 if s not in {row[i] for i in SPOKES}
                 and all(dict(zip(ORDER, f))[v] != s for v in CONTACTS)}
        whole = direct_x(row)
        if query != whole:
            raise ValueError('shared-coordinate s query differs from direct X lifts')
        pins = []
        for r, s in itertools.product(COLORS, repeat=2):
            expected = sorted(f for f in whole if f[0] == r and f[-1] == s)
            actual = sorted(f for f in query if f[0] == r and f[-1] == s)
            if actual != expected:
                raise ValueError('full pin fibre mismatch')
            pins.append({'r': r, 's': s, 'full_lifts': actual})
        # G has the original additional edge rb1. No lift of G-e is silently used as a G lift.
        original_g = sorted(f for f in whole if f[0] != row[1])
        fibres = []
        for ports in itertools.product(COLORS, repeat=3):
            lifts = sorted(f for f in joined if tuple(dict(zip(ORDER, f))[v] for v in CONTACTS) == ports)
            fibres.append({'tuple': ports, 'full_lifts': lifts})
        forbidden = [a for a in COLORS
                     if not any(all(dict(zip(ORDER, f))[v] != a for v in CONTACTS) for f in joined)]
        if not joined:
            raise ValueError('toy calibration unexpectedly has empty unpinned C')
        for permutation in itertools.permutations(COLORS):
            moved_row = tuple(permutation[c] for c in row)
            moved_lifts = {tuple(permutation[c] for c in f) for f in joined}
            if direct_c(moved_row) != moved_lifts:
                raise ValueError('one global S4 transport fails')
            global_color_checks += 1
        for direction in (1, -1):
            for offset in range(5):
                positions = {i: (offset + direction * i) % 5 for i in range(5)}
                moved_row = [None] * 5
                for i, c in enumerate(row):
                    moved_row[positions[i]] = c
                moved_attachments = {v: tuple(positions[i] for i in ATTACHMENTS[v]) for v in ORDER}
                if direct_c(moved_row, moved_attachments) != joined:
                    raise ValueError('whole D5 transport fails')
                whole_d5_checks += 1
        wrong = direct_c(row, edges=tuple(edge for edge in INTERNAL if edge != ('r', 'u')))
        if wrong == joined:
            raise ValueError('omitted U contact mutation escaped detection')
        skip_u_detected += 1
        records.append({'row': row, 'singleton_positions': [i for i, c in enumerate(row) if row.count(c) == 1],
                        'full_C_lifts': sorted(joined), 'ordered_contact_fibres': fibres,
                        'F_C': forbidden, 'full_pin_fibres': pins, 'full_X_lifts': sorted(whole),
                        'full_G_lifts_with_original_rb1': original_g})
    # A marginal product creates phantom contact tuples even when each projection is correct.
    exact_relation = {(0, 1), (1, 0)}
    marginal_product = set(itertools.product({x for x, _ in exact_relation}, {y for _, y in exact_relation}))
    if (0, 0) not in marginal_product - exact_relation:
        raise ValueError('marginal mutation negative control failed')
    # Splitting one original shared p into independent r/s ports fabricates a pin witness.
    shared_values = {0, 1}
    r_pin, s_pin = 0, 1
    exact_shared = {p for p in shared_values if p != r_pin and p != s_pin}
    cloned_ports = {(pr, ps) for pr in shared_values for ps in shared_values if pr != r_pin and ps != s_pin}
    if exact_shared or not cloned_ports:
        raise ValueError('shared-vertex clone mutation negative control failed')
    return {
        'task': 'N45-L1R', 'frozen_input_count': count, 'calibration_only': True,
        'paper_verdict': 'accept full LOW1 contract conditionally on BASE paper and external Gallai; not machine-proved',
        'calibration_graph': {'coordinates': ORDER, 'ordered_s_contacts': CONTACTS,
                              'shared_r_s_contact': 'p', 'internal_C_edges': INTERNAL,
                              'X_boundary_attachments': ATTACHMENTS, 's_spokes': SPOKES,
                              'G_only_original_spoke': ['r', 1],
                              'X_complete_degrees': {'r': 4, 's': 5, 'u': 2, 'p': 4, 'q': 3, 't': 3}},
        'coverage': {'canonical_rows': 10, 'root_pin_fibres': 160,
                     'contact_fibres_including_empty': 640, 'global_S4_checks': global_color_checks,
                     'whole_D5_checks': whole_d5_checks, 'contains_three_color_singleton2_row':
                     any(len(set(row)) == 3 and row.count(row[2]) == 1 for row in all_rows)},
        'calibration_controls': [
            {'name': 'complete_join_equals_direct_full_C_and_X', 'status': 'triggered and holds', 'rows': 10},
            {'name': 'deleted_original_U_contact_mutation', 'status': 'triggered and holds', 'rejected_rows': skip_u_detected},
            {'name': 'marginal_product_phantom_tuple', 'status': 'triggered and holds', 'phantom': [0, 0]},
            {'name': 'split_shared_p_coordinate', 'status': 'triggered and holds', 'phantom_ports': sorted(cloned_ports)},
        ],
        'LOW1_source_coverage': {'status': 'not triggered',
                                'reason': 'Abstract calibration has degree2/3 vertices; no complete Sigma933/941, Sigma-criticality, rejecting beta-minimality, one-sided true-framework supports, or disk rotation certificate.',
                                'new_LOW1_source_search': 'not performed', 'new_source_realization': False},
        'new_Lean': False, 'records': records,
    }


def manifest_check(path):
    if any(p.is_symlink() for p in HERE.rglob('*')):
        raise ValueError('unexpected symlink in sealed audit')
    expected = {}
    for line in path.read_text().splitlines():
        sha, rel = line.split('  ', 1)
        p = HERE / rel
        if Path(rel).is_absolute() or '..' in Path(rel).parts or rel in expected or not p.is_file() or p.is_symlink():
            raise ValueError('unsafe or duplicate manifest path: ' + rel)
        if digest(p.read_bytes()) != sha:
            raise ValueError('manifest digest mismatch: ' + rel)
        expected[rel] = sha
    actual = {p.relative_to(HERE).as_posix() for p in HERE.rglob('*')
              if p.is_file() and not p.is_symlink()
              and p.relative_to(HERE).parts[0] not in ('seal-final-v2',)
              and p.relative_to(HERE).as_posix() not in ('MANIFEST.final-v2.sha256', 'delivery.json')}
    if set(expected) != actual:
        raise ValueError('manifest inventory mismatch')
    receipt_path = HERE / 'delivery.json'
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_bytes())
        if digest((HERE / receipt['manifest_file']).read_bytes()) != receipt['manifest_sha256']:
            raise ValueError('receipt manifest binding mismatch')
        for rel, sha in receipt['seal_files'].items():
            if digest((HERE / rel).read_bytes()) != sha:
                raise ValueError('receipt metadata digest mismatch: ' + rel)
    return len(expected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--manifest', type=Path)
    args = parser.parse_args()
    try:
        actual = encoded(certificate())
        if args.emit:
            with args.certificate.open('xb') as stream:
                stream.write(actual)
        elif args.certificate.read_bytes() != actual:
            raise ValueError('certificate bytes mismatch')
        result = {'task': 'N45-L1R', 'certificate_sha256': digest(actual),
                  'frozen_inputs': 21, 'normalization': 'all deterministic sorted output',
                  'mathematical_scope': 'LOW1 conditional paper; calibration has no target source'}
        if args.manifest:
            result['manifest_payload_files'] = manifest_check(args.manifest)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print('REJECT: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
