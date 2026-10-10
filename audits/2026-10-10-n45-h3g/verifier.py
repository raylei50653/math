#!/usr/bin/env python3
"""Read-only custody and fixed witness checks; this is not a paper-proof verifier."""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / 'audits/2026-10-10-n45-progress-management'
EXCLUSIONS = {
    'manifest.json', 'delivery.json', 'receipt-normal.json',
    'receipt-seed17.json', 'receipt-negative.json', 'receipt-final-pins.json',
}


def require(condition: bool, finding: str) -> None:
    if not condition:
        raise ValueError(finding)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(name: str):
    return json.loads((HERE / name).read_text())


def connected(vertices: set[str], edges: set[tuple[str, str]]) -> bool:
    if not vertices:
        return False
    seen = {min(vertices)}
    pending = list(seen)
    while pending:
        v = pending.pop()
        for a, b in edges:
            w = b if a == v else a if b == v else None
            if w in vertices and w not in seen:
                seen.add(w)
                pending.append(w)
    return seen == vertices


def check_control(control: dict, negative: bool = False) -> None:
    require(control['classification'] == 'triggered and holds', 'H3G-CONTROL-LABEL')
    require(control['is_complete_source'] is False, 'H3G-TOY-SOURCE-CONFLATION')
    vertices = set(control['vertices'])
    raw_edges = [tuple(edge) for edge in control['edges']]
    edges = {tuple(sorted(edge)) for edge in raw_edges}
    require(len(edges) == len(raw_edges), 'H3G-DUPLICATE-SKELETON-EDGE')
    require(all(len(edge) == 2 and edge[0] != edge[1]
                and set(edge) <= vertices for edge in edges), 'H3G-SKELETON-EDGE')
    require(tuple(sorted(control['omitted_edge'])) not in edges, 'H3G-OMITTED-E-USED')
    require(tuple(sorted(control['retained_spoke'])) in edges, 'H3G-RETAINED-SPOKE-MISSING')
    bags = {name: set(bag) for name, bag in control['bags'].items()}
    require(set(bags) == {'Z', 'V1', 'V2', 'V3', 'O'}, 'H3G-BAG-NAMES')
    require(bags['Z'] == {'s'}, 'H3G-Z-NOT-ORIGINAL-S')
    require(all(bag <= vertices and connected(bag, edges) for bag in bags.values()),
            'H3G-BAG-NONEMPTY-CONNECTED')
    require(all(not bags[a] & bags[b] for a, b in itertools.combinations(bags, 2)),
            'H3G-BAG-OVERLAP')
    missing = []
    for a, b in itertools.combinations(sorted(bags), 2):
        if not any((u in bags[a] and v in bags[b]) or
                   (u in bags[b] and v in bags[a]) for u, v in edges):
            missing.append([a, b])
    if negative and missing == [['O', 'Z']]:
        raise ValueError('H3G-NEGATIVE-ZO-REMOVED')
    require(not missing, 'H3G-TEN-ORIGINAL-ADJACENCIES')
    parity = [n % 2 for n in control['arm_lengths']]
    require(len(set(parity)) == 1, 'H3G-ARM-PARITY')
    for i, (arm, length, tether) in enumerate(zip(control['arms'],
                                                control['arm_lengths'],
                                                control['tethers']), 1):
        require(arm[0] == 'v' + str(i) and len(arm) == length + 1,
                'H3G-ZERO-ARM-ENDPOINT')
        require(set(arm) == bags['V' + str(i)], 'H3G-ARM-BAG')
        require(tuple(sorted(['s', arm[-1]])) in edges, 'H3G-ORIGINAL-CONTACT')
        require(tether[0] == arm[0] and tether[-1] in {'b' + str(k) for k in range(5)},
                'H3G-BOUNDARY-TETHER')
        require(set(tether[1:]) <= bags['O'], 'H3G-TETHER-IN-HUB')
        require(all(tuple(sorted(e)) in edges for e in zip(tether, tether[1:])),
                'H3G-TETHER-ORIGINAL-EDGES')
    path = control['external_path']
    require(path[0] == 's' and path[-2:] == ['r', 'b4'] and len(set(path)) == len(path),
            'H3G-EXTERNAL-PATH')
    require(set(path[1:]) <= bags['O'], 'H3G-EXTERNAL-PATH-IN-HUB')
    require(all(tuple(sorted(e)) in edges for e in zip(path, path[1:])),
            'H3G-EXTERNAL-PATH-ORIGINAL-EDGES')


def check(negative: bool) -> dict:
    inputs = read_json('frozen/dispatch/inputs.json')
    pins = read_json('pin-verification.json')
    require(pins['verified'] is True and pins['BASE'] == inputs['BASE'], 'H3G-INITIAL-PINS')
    require(len(inputs['inputs']) == 14, 'H3G-NAMED-INPUT-COUNT')
    counts = {'current': 0, 'base': 0}
    for item in inputs['inputs']:
        layer, name, expected = item['layer'], item['path'], item['sha256']
        require(layer in counts, 'H3G-PIN-LAYER')
        counts[layer] += 1
        frozen = HERE / 'frozen' / layer / name
        require(digest(frozen.read_bytes()) == expected, 'H3G-OWN-FROZEN-DRIFT:' + name)
        require(digest((PARENT / item['frozen']).read_bytes()) == expected,
                'H3G-PARENT-FROZEN-DRIFT:' + name)
        if layer == 'current':
            actual = (ROOT / name).read_bytes()
        else:
            actual = subprocess.run(['git', 'show', inputs['BASE'] + ':' + name],
                                    cwd=ROOT, check=True, capture_output=True).stdout
        require(digest(actual) == expected, 'H3G-LIVE-OR-BASE-DRIFT:' + name)
    require(counts == {'current': 8, 'base': 6}, 'H3G-PIN-COUNTS')
    for name in ['common-contract.md', 'inputs.json', 'n45-h3g-task.md']:
        require((HERE / 'frozen/dispatch' / name).read_bytes() == (PARENT / name).read_bytes(),
                'H3G-DISPATCH-DRIFT:' + name)

    trust = read_json('external-trust.json')
    require(digest((HERE / 'frozen/external/gallai.pdf').read_bytes()) == trust['sha256'],
            'H3G-PRIMARY-PDF-DRIFT')
    require({v['label'] for v in trust['lemmas']} == {'Lemma 7', 'Theorem 10'},
            'H3G-EXTERNAL-TRUST-LABELS')
    manifest = read_json('manifest.json')
    require(set(manifest['metadata_exclusions']) == EXCLUSIONS, 'H3G-MANIFEST-EXCLUSIONS')
    payload = {}
    for path in HERE.rglob('*'):
        require(not path.is_symlink(), 'H3G-SYMLINK-PAYLOAD')
        if path.is_file():
            name = path.relative_to(HERE).as_posix()
            if name not in EXCLUSIONS:
                payload[name] = digest(path.read_bytes())
    require(payload == manifest['payload'], 'H3G-MANIFEST-PAYLOAD-DRIFT')

    judgment = read_json('independent-judgment.json')
    require(judgment['all_K1_K13_apply'] is True and judgment['mathematical_gap_count'] == 0,
            'H3G-JUDGMENT-SCOPE')
    require(judgment['verdict'] == 'holds under stated hypotheses', 'H3G-JUDGMENT-VERDICT')
    require(len(judgment['claims']) == 9, 'H3G-CLAIM-COUNT')
    required_fields = {'quantifier', 'claim', 'K1_K13_used', 'BASE_sections',
                       'external_trust', 'verdict', 'new_sufficient_hypotheses', 'precise_residual'}
    ids = {claim['id'] for claim in judgment['claims']}
    for claim in judgment['claims']:
        require(required_fields <= set(claim), 'H3G-CLAIM-FIELDS')
        require(set(claim['K1_K13_used']) <= {'K' + str(i) for i in range(1, 14)},
                'H3G-CLAIM-K-TAGS')
        require(set(claim['dependencies']) <= ids, 'H3G-CLAIM-DEPENDENCIES')
        require(claim['new_sufficient_hypotheses'] == [], 'H3G-NEW-PREMISE')
        require(all(ref['commit'] == inputs['BASE'] for ref in claim['BASE_sections']),
                'H3G-CLAIM-BASE')
    require(judgment['layers']['finite_source'] ==
            {'established': False, 'executed': False, 'source_trigger_count': None},
            'H3G-FINITE-SOURCE-CONFLATION')

    report = (HERE / 'REPORT.md').read_text()
    for name in re.findall(r'\]\(([^)]+)\)', report):
        if '://' not in name:
            target = name.split('#', 1)[0]
            require(bool(target) and (HERE / target).is_file(), 'H3G-AUTHORED-LINK:' + target)
    for name in ['REPORT.md', 'verifier.py']:
        data = (HERE / name).read_text()
        require(data.endswith('\n'), 'H3G-FINAL-NEWLINE:' + name)
        require(all(line == line.rstrip() for line in data.splitlines()),
                'H3G-AUTHORED-WHITESPACE:' + name)

    witness = read_json('proof-witness.json')
    require(witness['finite_source_established'] is False and witness['source_count'] is None,
            'H3G-WITNESS-SOURCE-CONFLATION')
    require(len(witness['abstract_controls']) == 4, 'H3G-ABSTRACT-CONTROL-COUNT')
    schema = witness['symbolic_proof_witness']
    require(len(schema['ten_original_adjacencies']) == 10, 'H3G-SYMBOLIC-TEN-PAIRS')
    pairs = {tuple(sorted(v[:2])) for v in schema['ten_original_adjacencies']}
    require(pairs == set(itertools.combinations(sorted(schema['bags']), 2)),
            'H3G-SYMBOLIC-PAIR-COVERAGE')
    if negative:
        broken = copy.deepcopy(witness['abstract_controls'][0])
        path = broken['external_path']
        removed = sorted(path[:2])
        broken['edges'].remove(removed)
        check_control(broken, negative=True)
        raise ValueError('H3G-NEGATIVE-FAILED-TO-REJECT')
    for control in witness['abstract_controls']:
        check_control(control)
    return {'ok': True, 'audit_id': 'N45-H3G', 'pins': counts, 'pin_drift': 0,
            'paper_claim_records_checked': 9, 'paper_proof_verified_by_code': False,
            'abstract_minor_controls': [{'id': c['id'], 'classification': c['classification']}
                                        for c in witness['abstract_controls']],
            'finite_source_established': False, 'source_trigger_count': None,
            'immutable_payload_files': len(payload),
            'manifest_sha256': digest((HERE / 'manifest.json').read_bytes()),
            'witness_sha256': digest((HERE / 'proof-witness.json').read_bytes())}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--negative-control', action='store_true')
    args = parser.parse_args()
    try:
        result = check(args.negative_control)
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({'ok': False, 'audit_id': 'N45-H3G', 'finding': str(exc)},
                         sort_keys=True, ensure_ascii=False))
        return 2
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
