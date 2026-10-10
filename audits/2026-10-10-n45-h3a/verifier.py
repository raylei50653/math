#!/usr/bin/env python3
"""Read-only, named-input and immutable-payload verifier; no source enumeration."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
METADATA = {
    'manifest.json', 'delivery.json', 'receipt-normal.json',
    'receipt-seed17.json', 'receipt-negative.json',
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text())


def inventory():
    entries = []
    for path in sorted(HERE.rglob('*')):
        require(not path.is_symlink(), 'payload symlink: ' + str(path))
        if path.is_file() and path.relative_to(HERE).as_posix() not in METADATA:
            entries.append({'path': path.relative_to(HERE).as_posix(),
                            'sha256': digest(path.read_bytes()),
                            'bytes': path.stat().st_size})
    return entries


def verify_inventory(manifest):
    require(manifest['audit_id'] == 'N45-H3A', 'manifest audit ID')
    require(manifest['exact_top_level_metadata_exclusions'] == sorted(METADATA),
            'metadata exclusions must be exact top-level names')
    actual = inventory()
    require(manifest['payload'] == actual,
            'immutable payload inventory/hash mismatch (nested metadata is payload)')
    return len(actual)


def verify_inputs(frozen_only):
    spec = read_json(HERE / 'frozen/authority/inputs.json')
    initial = read_json(HERE / 'initial-pin-check.json')
    require(spec['BASE'] == initial['BASE'], 'BASE mismatch')
    counts = {'current': 0, 'base': 0}
    for item in spec['inputs']:
        counts[item['layer']] += 1
        require(digest((HERE / item['frozen']).read_bytes()) == item['sha256'],
                'own frozen input drift: ' + item['path'])
        if item['layer'] == 'base':
            run = subprocess.run(['git', 'show', spec['BASE'] + ':' + item['path']],
                                 cwd=ROOT, capture_output=True, check=True)
            actual = run.stdout
        elif not frozen_only:
            actual = (ROOT / item['path']).read_bytes()
        else:
            actual = (HERE / item['frozen']).read_bytes()
        require(digest(actual) == item['sha256'], 'named input drift: ' + item['path'])
    require(counts == {'current': 8, 'base': 6}, 'expected 8 current and 6 BASE pins')
    require(initial['all_match'] and all(x['matches'] for x in initial['records']),
            'initial pin receipt failed')
    ext = read_json(HERE / 'external-index.json')
    require(digest((HERE / ext['path']).read_bytes()) == ext['sha256'],
            'external frozen PDF drift')
    return counts


def canonical(row):
    seen = {}
    result = []
    for color in row:
        if color not in seen:
            seen[color] = len(seen)
        result.append(seen[color])
    return tuple(result)


def verify_abstract_controls():
    evidence = read_json(HERE / 'transport-witness.json')
    controls = evidence['controls']
    require(all(c['status'] == 'triggered and holds' for c in controls),
            'abstract controls must carry exact coverage label')
    proper = [b for b in itertools.product(range(4), repeat=5)
              if all(b[i] != b[(i + 1) % 5] for i in range(5))]
    three = [b for b in proper if len(set(b)) == 3]
    require(len(proper) == 240 and len(three) == 120, 'literal row domain')
    transport = controls[0]
    require(transport['proper_literal_rows'] == 240 and
            transport['three_color_literal_rows'] == 120, 'transport row counts')
    require([tuple(w['beta']) for w in transport['witnesses']] == three,
            'transport must cover every proper literal three-color row exactly once')
    q = (0, 1, 0, 1, 2)
    for witness in transport['witnesses']:
        beta, rho, pi = (witness[k] for k in
                         ('beta', 'rho_output_to_old', 'pi_old_color_to_new'))
        require(sorted(pi) == list(range(4)), 'pi is one S4 permutation')
        require(any(rho == [(sign * i + shift) % 5 for i in range(5)]
                    for sign in (-1, 1) for shift in range(5)), 'rho is one D5 map')
        require(tuple(pi[beta[rho[i]]] for i in range(5)) == q,
                'whole-row beta to q witness failed')
        singleton = next(c for c in set(beta) if beta.count(c) == 1)
        require(beta[rho[4]] == singleton, 'constructive singleton normalization')
    cells = sorted({canonical(b) for b in proper})
    arithmetic = controls[1]
    require(arithmetic['canonical_cells'] == [list(b) for b in cells], 'ten cells')
    for mask in (933, 941):
        rejected = [i for i in range(10) if not (mask >> i & 1)]
        require(arithmetic['rejected_cells'][str(mask)] == rejected, 'mask rejections')
        require(all(len(set(cells[i])) == 3 for i in rejected),
                'all 933/941 rejecting literals must be three-color')
    require(arithmetic['rejected_cells']['933'] == [1, 3, 4, 6], 'retain 933 q2')
    colors = frozenset(range(4))
    subsets = [frozenset(c for c in range(4) if m >> c & 1) for m in range(16)]
    records = []
    for fc in subsets:
        for fu in subsets:
            if len(fc) <= 2 and len(fu) <= 3 and fc | fu == colors and fc - fu and fu - fc:
                require(len(fu) >= 2, 'three-contact forbidden-color lower bound')
                records.append({'F_C': sorted(fc), 'F_U': sorted(fu),
                                'private_C': sorted(fc - fu),
                                'private_U': sorted(fu - fc)})
    require(controls[2]['records'] == records and controls[2]['record_count'] == 22,
            'complete named (2,3) abstract capacity records')
    return {'three_color_literals': len(three), 'capacity_records': len(records)}


def verify_judgment_and_text():
    judgment = read_json(HERE / 'independent-judgment.json')
    require(judgment['candidate_only'] is True, 'adoption boundary')
    require(list(judgment['hypotheses']) == ['K' + str(i) for i in range(1, 14)],
            'complete K1-K13 scope')
    expected = ['H3A-CORE', 'H3A-COMPONENT', 'H3A-TRANSPORT',
                'H3A-BASE-MAP', 'H3A-EXCLUSION']
    require([c['claim_id'] for c in judgment['claims']] == expected, 'five claim IDs')
    for claim in judgment['claims']:
        require(claim['verdict'] == 'holds under stated hypotheses' and
                claim['required_scope_hypotheses'] == list(judgment['hypotheses']) and
                claim['new_sufficient_hypotheses'] == [] and claim['findings'] == [],
                'claim scope/verdict schema')
        require(claim['full_quantifier'].startswith('For every finite simple disk graph'),
                'complete arbitrary-size quantifier')
    for name in ('REPORT.md', 'verifier.py'):
        data = (HERE / name).read_text()
        require(data.endswith('\n') and all(line.rstrip() == line for line in data.splitlines()),
                'authored file whitespace: ' + name)
    report = (HERE / 'REPORT.md').read_text()
    links = re.findall(r'\]\(([^)]+)\)', report)
    for target in links:
        if '://' in target:
            continue
        plain = target.split('#', 1)[0]
        if plain in METADATA and not (HERE / 'delivery.json').exists():
            continue  # Declared seal metadata, checked after delivery is present.
        require((HERE / plain).is_file(), 'local REPORT target: ' + target)
    return len(links)


def verify_delivery_if_present():
    path = HERE / 'delivery.json'
    if not path.exists():
        return
    delivery = read_json(path)
    require(delivery['manifest_sha256'] == digest((HERE / 'manifest.json').read_bytes()),
            'delivery manifest binding')
    for entry in delivery['receipts']:
        receipt_path = HERE / entry['path']
        require(digest(receipt_path.read_bytes()) == entry['sha256'], 'delivery receipt binding')
        receipt = read_json(receipt_path)
        require(receipt['manifest_sha256'] == delivery['manifest_sha256'], 'receipt manifest binding')
        require(receipt['verifier_sha256'] == digest((HERE / 'verifier.py').read_bytes()),
                'receipt verifier binding')
        require(digest(receipt['stdout'].encode()) == receipt['stdout_sha256'] and
                digest(receipt['stderr'].encode()) == receipt['stderr_sha256'],
                'receipt stream hashes')
        require(receipt['exit_code'] == (2 if entry['path'] == 'receipt-negative.json' else 0),
                'receipt actual exit code')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--manifest-stdin', action='store_true')
    parser.add_argument('--frozen-only', action='store_true')
    args = parser.parse_args()
    try:
        manifest = (json.load(sys.stdin) if args.manifest_stdin
                    else read_json(HERE / 'manifest.json'))
        count = verify_inventory(manifest)
        inputs = verify_inputs(args.frozen_only)
        arithmetic = verify_abstract_controls()
        links = verify_judgment_and_text()
        verify_delivery_if_present()
        print(json.dumps({'audit': 'N45-H3A', 'payload': count, 'named_inputs': inputs,
                          'frozen_input_drift': 0, 'abstract_controls': arithmetic,
                          'report_links': links, 'paper_verdict': 'manual independent audit',
                          'finite_source': 'not established/not executed'}, sort_keys=True))
        return 0
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
