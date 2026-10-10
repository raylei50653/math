#!/usr/bin/env python3
"""Read-only named custody and abstract controls; does not certify paper or source."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import stat
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORKER = HERE / 'frozen/audits/2026-10-10-n45-s-high2'
META = {'manifest.json', 'delivery.json', 'receipt-normal.json',
        'receipt-seed17.json', 'receipt-negative.json'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(test, message):
    if not test:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def tree_index(directory):
    result = {}
    for path in sorted(directory.rglob('*')):
        require(not path.is_symlink(), 'unexpected symlink: ' + str(path))
        if path.is_file():
            data = path.read_bytes()
            result[path.relative_to(directory).as_posix()] = {
                'kind': 'regular', 'bytes': len(data),
                'mode': stat.S_IMODE(path.stat().st_mode), 'sha256': sha(data)}
    return result


def payload():
    return [{'path': name, **item} for name, item in tree_index(HERE).items()
            if name not in META]


def check_manifest(manifest):
    require(manifest['audit_id'] == 'N45-H2A', 'manifest audit ID')
    require(manifest['exact_top_level_metadata_exclusions'] == sorted(META),
            'exclusions must be exact current top-level metadata')
    require(manifest['payload'] == payload(),
            'immutable payload inventory/hash/mode mismatch; nested receipt is payload')
    return len(manifest['payload'])


def check_intake(frozen_only):
    intake = read(HERE / 'frozen/authority/intake.json')
    count = 0
    for name, item in intake['workers'].items():
        require(tree_index(HERE / 'frozen' / name) == item['fulltree'],
                'own frozen full worker bytes/modes: ' + name)
        if not frozen_only:
            require(tree_index(ROOT / name) == item['fulltree'],
                    'original worker full tree drift: ' + name)
        count += len(item['fulltree'])
    if not frozen_only:
        for path, digest in intake['shared_before'].items():
            require(sha((ROOT / path).read_bytes()) == digest, 'named shared drift: ' + path)
    require(count == 206 and read(HERE / 'initial-intake-check.json')['all_match'],
            'initial four-tree intake receipt')
    spec = read(WORKER / 'inputs-final.json')
    require(len(spec['inputs']) == 41 and len(spec['pins']) == 8, '41 inputs / 8 pins')
    for item in spec['inputs']:
        require(sha((WORKER / item['frozen']).read_bytes()) == item['sha256'],
                'own source frozen input drift: ' + item['path'])
        if item['origin'] == 'BASE':
            data = subprocess.run(['git', 'show', spec['BASE'] + ':' + item['path']],
                                  cwd=ROOT, capture_output=True, check=True).stdout
        elif not frozen_only:
            data = (ROOT / item['path']).read_bytes()
        else:
            data = (WORKER / item['frozen']).read_bytes()
        require(sha(data) == item['sha256'], 'named source input drift: ' + item['path'])
    if not frozen_only:
        for pin in spec['pins']:
            require(sha((ROOT / pin['path']).read_bytes()) == pin['sha256'],
                    'dispatch pin drift: ' + pin['path'])
    index = read(HERE / 'input-index.json')
    require(index['all_match'] and all(x['matches'] for x in index['inputs'] + index['pins']),
            'independent initial input-index receipt')
    return count


def support_lifts(support, spoke):
    positions = sorted((i - spoke) % 5 for i in support if i != spoke)
    return ([sorted(positions + [0]), sorted(positions + [5]),
             sorted(positions + [0, 5])] if spoke in support else [positions])


def check_arithmetic():
    evidence = read(HERE / 'independent-arithmetic.json')
    records = read(WORKER / 'frozen/base/artifacts/c5_single_spoke_two_two/observations.json')['records']
    q = (0, 1, 0, 1, 2)
    mapping = []
    for middle in range(5):
        triple = {(middle - 1) % 5, middle, (middle + 1) % 5}
        if len({q[i] for i in triple}) != 2:
            continue
        for j, k in itertools.product(range(5), repeat=2):
            if middle in (j, k) or q[j] == q[k] or {q[j], q[k]} != {q[i] for i in triple}:
                continue
            reflected = k not in (0, 1, 4)
            p = lambda i: (3 - i) % 5 if reflected else i
            c = lambda a: 1 - a if reflected and a in (0, 1) else a
            supports = [sorted(p(i) for i in set(range(5)) - {middle}),
                        sorted(p(i) for i in triple)]
            bans = [[c(q[j])], [2, 3]]
            spoke = p(k)
            placements = [[lc, lu] for lc, lu in itertools.product(
                support_lifts(supports[0], spoke), support_lifts(supports[1], spoke))
                if max(lc) <= min(lu) or max(lu) <= min(lc)]
            matching = [r for r in records if r['spoke'] == spoke and
                        r['supports'] == supports and r['bans'] == bans]
            require(len(matching) <= 1 and bool(matching) == bool(placements),
                    'slit placement and BASE necessary record domain')
            if matching:
                require(matching[0]['T4_status'] == 'retained' and placements ==
                        [x['lifted_supports'] for x in matching[0]['placements']],
                        'BASE actual supports/placements')
                require(all(len(x['contact_words']) == 4 for x in matching[0]['placements']),
                        'all four necessary contact word directions retained')
            mapping.append({'original_T': sorted(triple), 'retained_r_spoke': j,
                            's_spoke': k, 'whole_reflection': reflected,
                            'C_then_U_supports': supports, 'C_then_U_bans': bans,
                            'record_id': matching[0]['id'] if matching else None,
                            'slit_order_placements': placements})
    require(evidence['mapping'] == mapping and len(mapping) == 8,
            'all eight independent named mapping positions')
    require(sum(x['record_id'] is None for x in mapping) == 4, 'four slit source exclusions')
    three = [b for b in itertools.product(range(4), repeat=5) if len(set(b)) == 3
             and all(b[i] != b[(i + 1) % 5] for i in range(5))]
    singleton_count = 0
    for gamma in three:
        singleton = next(i for i in range(5) if gamma.count(gamma[i]) == 1)
        for middle in range(5):
            triple = {(middle - 1) % 5, middle, (middle + 1) % 5}
            require((len({gamma[i] for i in triple}) == 3) == (singleton in triple),
                    'proper three-color singleton versus triple domain')
            singleton_count += 1
    require(singleton_count == evidence['singleton_checks'] == 600, '600 literal checks')
    orbits = []
    for mask, rejected in ((933, {0, 1, 2, 3}), (941, {0, 1, 3})):
        for sign in (1, -1):
            for shift in range(5):
                missing = {(sign * i + shift) % 5 for i in rejected}
                for middle in range(5):
                    triple = {(middle - 1) % 5, middle, (middle + 1) % 5}
                    require(bool(missing & triple), 'all original 933/941 D5 rejects preserved')
                    orbits.append({'mask': mask, 'D5': [sign, shift], 'middle': middle,
                                   'Q': sorted(missing), 'T': sorted(triple),
                                   'contradicting_singleton_positions': sorted(missing & triple)})
    require(orbits == evidence['orbit_witnesses'] and evidence['orbit_checks'] == 100,
            '100 complete D5 reject checks')
    require(evidence['conditional_HIGH_cases'] == [[1, 2], [2, 1], [3, 0]],
            'u+t_s=3 conditional coverage')
    cases = [(u, t) for u in range(1, 6) for t in range(6) if 2 + u + t == 5]
    require(cases == [(1, 2), (2, 1), (3, 0)], 'all HIGH degree partitions')
    return {'mapping': 8, 'slit_source_exclusions': 4, 'singleton_checks': 600,
            'D5_checks': 100, 'source_triggers': None}


def check_judgment_text():
    judgment = read(HERE / 'independent-judgment.json')
    require(judgment['candidate_only'] and judgment['mathematical_source_proof_gap_count'] == 0,
            'manual paper candidate schema')
    expected = ['H2-' + name for name in ('CORE', 'COMP', 'JOIN', 'RESTORE', 'F', 'K33',
                'ARC', 'MAP', 'BRIDGE', 'SPLIT', 'PALETTE', 'EXCLUSION')]
    require([c['claim_id'] for c in judgment['claims']] == expected, 'all twelve claim IDs')
    require(all(c['all_source_hypotheses'] == ['H' + str(i) for i in range(1, 14)]
                and c['verdict'] == 'holds under stated hypotheses'
                and c['new_source_sufficient_hypotheses'] == [] for c in judgment['claims']),
            'complete H1-H13 per-claim source scope')
    finding = judgment['findings'][0]
    example = finding['scalar_counterexample']
    gamma, triple = example['gamma'], example['T']
    require(finding['id'] == 'H2A-QDOMAIN-01' and len(set(gamma)) == 4
            and all(gamma[i] != gamma[(i + 1) % 5] for i in range(5))
            and len({gamma[i] for i in triple}) == 3
            and set(range(4)) - set(gamma) == set(), 'exact construction domain refinement')
    require(judgment['conditional_scoped_composition']['conditional'] and
            not judgment['conditional_scoped_composition']['adopted'], 'no autonomous adoption')
    for name in ('REPORT.md', 'verifier.py'):
        text = (HERE / name).read_text()
        require(text.endswith('\n') and all(line == line.rstrip() for line in text.splitlines()),
                'new text whitespace: ' + name)
    links = re.findall(r'\]\(([^)]+)\)', (HERE / 'REPORT.md').read_text())
    for target in links:
        if '://' in target:
            continue
        target = target.split('#', 1)[0]
        if target in META and not (HERE / 'delivery.json').exists():
            continue  # Exact seal metadata checked once delivery has been created.
        require((HERE / target).is_file(), 'new REPORT local target: ' + target)
    return len(links)


def check_delivery_if_present():
    if not (HERE / 'delivery.json').exists():
        return
    delivery = read(HERE / 'delivery.json')
    manifest_sha = sha((HERE / 'manifest.json').read_bytes())
    require(delivery['manifest_sha256'] == manifest_sha, 'delivery manifest binding')
    names = {r['path'] for r in delivery['receipts']}
    require(names == {'receipt-normal.json', 'receipt-seed17.json', 'receipt-negative.json'},
            'three exact final receipts')
    for entry in delivery['receipts']:
        path = HERE / entry['path']
        require(sha(path.read_bytes()) == entry['sha256'], 'receipt bytes binding')
        receipt = read(path)
        require(receipt['manifest_sha256'] == manifest_sha and
                receipt['verifier_sha256'] == sha((HERE / 'verifier.py').read_bytes()),
                'receipt manifest/verifier binding')
        require(sha(receipt['stdout'].encode()) == receipt['stdout_sha256'] and
                sha(receipt['stderr'].encode()) == receipt['stderr_sha256'], 'actual stream binding')
        if receipt['stdin'] is not None:
            require(sha(receipt['stdin'].encode()) == receipt['stdin_sha256'], 'negative input binding')
        require(receipt['exit_code'] == (2 if entry['path'] == 'receipt-negative.json' else 0),
                'receipt actual exit')
    normal = read(HERE / 'receipt-normal.json')
    seed = read(HERE / 'receipt-seed17.json')
    require(normal['stdout'] == seed['stdout'] and normal['stderr'] == seed['stderr'],
            'actual normal/seed17 streams must match')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--manifest-stdin', action='store_true')
    parser.add_argument('--frozen-only', action='store_true')
    args = parser.parse_args()
    try:
        manifest = json.load(sys.stdin) if args.manifest_stdin else read(HERE / 'manifest.json')
        count = check_manifest(manifest)
        workers = check_intake(args.frozen_only)
        arithmetic = check_arithmetic()
        links = check_judgment_text()
        check_delivery_if_present()
        print(json.dumps({'audit': 'N45-H2A', 'payload': count, 'frozen_worker_regular': workers,
                          'source_inputs': 41, 'dispatch_pins': 8, 'named_input_drift': 0,
                          'abstract_controls': arithmetic, 'report_links': links,
                          'paper_verdict': 'manual independent audit, explicit query-domain refinement',
                          'candidate_only': True}, sort_keys=True))
        return 0
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
