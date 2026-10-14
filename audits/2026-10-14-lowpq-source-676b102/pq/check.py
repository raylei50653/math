#!/usr/bin/env python3
"""Exact original-cap arithmetic; no source realization is asserted."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = HERE.parents[2]
PINS = ('z', 's', 'r', 't', 'q', 'ell', 'm')
FACE_EDGES = (('z','s'), ('s','r'), ('r','t'), ('t','z'),
              ('z','q'), ('q','ell'), ('ell','m'), ('m','z'))
CAP_EDGES = (('p','z'), ('p','q'), ('p','ell'), ('p','m'),
             ('x','z'), ('x','s'), ('x','r'), ('x','y'),
             ('y','z'), ('y','r'), ('y','t'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authority():
    manifest_path = AUDIT / 'INPUTS.json'
    manifest = json.loads(manifest_path.read_text())
    for item in manifest['inputs']:
        path = (AUDIT / item['frozen_path'] if 'frozen_path' in item
                else ROOT / item['path'])
        if not path.is_file() or digest(path) != item['sha256']:
            raise ValueError('authority drift: ' + str(path))
    return {'base': manifest['base'],
            'input_manifest_sha256': digest(manifest_path),
            'checked_input_files': len(manifest['inputs']),
            'checker_sha256': digest(Path(__file__).resolve())}


def canonical(values):
    names = {}
    return ''.join(chr(65 + names.setdefault(c, len(names))) for c in values)


def direct_lifts(f):
    answer = []
    for values in itertools.product(range(4), repeat=3):
        g = dict(f, **dict(zip(('p','x','y'), values)))
        if all(g[a] != g[b] for a,b in CAP_EDGES):
            answer.append(list(values))
    return answer


def product_lifts(f):
    ps = [c for c in range(4) if c not in
          {f[v] for v in ('z','q','ell','m')}]
    xys = [(x,y) for x,y in itertools.product(range(4), repeat=2)
           if x not in {f['z'],f['s'],f['r'],y}
           and y not in {f['z'],f['r'],f['t'],x}]
    return [[p,x,y] for p in ps for x,y in xys]


def build():
    binding = authority()
    rows = {}
    proper = 0
    total_lifts = 0
    triple_labelled = 0
    old_labelled = 0
    for values in itertools.product(range(4), repeat=7):
        f = dict(zip(PINS, values))
        if any(f[a] == f[b] for a,b in FACE_EDGES):
            continue
        proper += 1
        direct = direct_lifts(f)
        assert direct == product_lifts(f), (values, direct)
        total_lifts += len(direct)
        word = canonical(values)
        triple = f['z'] == f['r'] == f['ell']
        old = f['z'] == f['r'] and f['q'] == f['m']
        triple_labelled += triple
        old_labelled += old
        if tuple(ord(c)-65 for c in word) != values:
            continue
        success = [lift for lift in direct
                   if {lift[0],f['q']} != set(lift[1:])]
        rows[word] = {'pins': list(values), 'full_lifts_pxy': direct,
                      'successful_target_lifts_pxy': success,
                      'all_cap_lifts_fail': not success,
                      'triple_quotient': triple, 'earlier_quotient': old}
    triple_survivors = [w for w,r in rows.items()
                        if r['triple_quotient'] and r['all_cap_lifts_fail']]
    old_survivors = [w for w,r in rows.items()
                     if r['earlier_quotient'] and r['all_cap_lifts_fail']]
    assert triple_survivors == ['ABABCAB'], triple_survivors
    assert old_survivors == ['ABABCBC'], old_survivors
    assert rows['ABABCAB']['full_lifts_pxy'] == [[3,2,3], [3,3,2]]
    assert all(rows[w]['pins'][3] == rows[w]['pins'][6]
               for w in triple_survivors)
    return {'schema': 'lowpq-original-seven-pin-full-lifts-v1',
            'binding': binding, 'pins': list(PINS),
            'face_edges': [list(e) for e in FACE_EDGES],
            'cap_edges': [list(e) for e in CAP_EDGES],
            'summary': {'all_labelled_assignments': 4**7,
                        'proper_labelled_rows': proper,
                        'canonical_rows': len(rows),
                        'all_labelled_full_cap_lifts': total_lifts,
                        'triple_quotient_labelled_rows': triple_labelled,
                        'earlier_quotient_labelled_rows': old_labelled,
                        'triple_quotient_survivors': triple_survivors,
                        'earlier_quotient_survivors': old_survivors,
                        'triple_with_mt_edge_survivors': [],
                        'genuine_target_source_controls': 0},
            'rows': rows}


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    ap.add_argument('--certificate', type=Path,
                    default=HERE / 'certificate-final.json')
    args = ap.parse_args()
    actual = build()
    if args.write:
        with args.certificate.open('x') as handle:
            json.dump(actual, handle, indent=2)
            handle.write('\n')
        print('GENERATED exclusive certificate:', args.certificate)
    else:
        expected = json.loads(args.certificate.read_text())
        if actual != expected:
            raise SystemExit('REJECT: certificate differs from complete recomputation')
        print('PASS: frozen inputs and all complete cap lifts match')
    print(json.dumps(actual['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
