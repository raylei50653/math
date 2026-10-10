#!/usr/bin/env python3
"""Independent read-only integrity audit. No worker code or theorem runs."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tarfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
ORIGINAL = ROOT / 'audits/2026-10-10-n45-u-ss'
FROZEN = OUT / 'frozen/worker'
PINS = {
    'docs/c5_excess_two_nonadjacent_unit_core45.md': '3dd0a492915b5e21d31d862ba8f2c0660250c5d2ded2f075daf54aca8043c942',
    'audits/2026-10-09-n45-pr/REPORT.md': 'ebcda98bf4f243aaa171d0192724e12690d3565c45fbb6b44b1a738ebcd083da',
    'audits/2026-10-10-n45-pa/independent-judgment.json': 'dd647d8e1b09af9b43b3cf5e377ea81afb9fc75f6c38e8192bb5b78841f940ae',
    'audits/2026-10-09-n45-u/REPORT.md': '0c3d117f1c804bc0695fc97fd570f2ede6451d5a21ca036f337f4d11c5de72a7',
    'audits/2026-10-09-n45-su-a/independent-judgment.json': '97ba9e80fedeb1fef95c767f525b17ffde6e676cd4b06131a8b295741ac95872',
}
EXPECTED_IDS = ['COST', 'UNTOP', 'U3', 'U2', 'X-CORE', 'COMPONENT', 'SPOKES', 'T0', 'T1', 'T2', 'EXCLUSION']
EXPECTED_IDS = ['N45-SS-' + name for name in EXPECTED_IDS]
EXPECTED_EDGES = {
    'COST': [], 'UNTOP': ['COST'], 'U3': ['UNTOP'], 'U2': ['UNTOP'], 'X-CORE': [],
    'COMPONENT': ['X-CORE'], 'SPOKES': ['U2', 'X-CORE', 'COMPONENT'],
    'T0': ['SPOKES'], 'T1': ['SPOKES'], 'T2': ['SPOKES'],
    'EXCLUSION': ['COST', 'U3', 'U2', 'X-CORE', 'COMPONENT', 'SPOKES', 'T0', 'T1', 'T2'],
}
ALLOWED_NEW_PREFIXES = (
    'audits/2026-10-10-n45-u-ss/', 'audits/2026-10-10-n45-ss-supervision/',
    'audits/2026-10-10-n45-ssa/', 'audits/2026-10-10-n45-ssg/', 'audits/2026-10-10-n45-ssc/',
)

def require(value, reason):
    if not value:
        raise ValueError(reason)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def file_hash(path, algorithm='sha256', prefix=b''):
    h = hashlib.new(algorithm)
    h.update(prefix)
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def parse_manifest(raw):
    entries = {}
    for line in raw.decode('utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, 'malformed manifest line')
        digest, name = match.groups()
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts and str(path) == name,
                'unsafe manifest path: ' + name)
        require(name not in entries, 'duplicate manifest path: ' + name)
        entries[name] = digest
    return entries

def validate_entries(entries, observed):
    require(set(entries) == set(observed), 'manifest exact inventory mismatch')
    for name, digest in entries.items():
        require(observed[name] == digest, 'manifest digest mismatch: ' + name)

def validate_claims(doc):
    require(doc['task'] == 'N45-U-SS' and doc['base'] == BASE, 'claim provenance mismatch')
    contract = doc['source_contract']
    require(len(contract) == 8 and len(set(contract)) == 8, 'source contract clause count mismatch')
    # These clauses are inspected as the declared contract, not accepted as true.
    markers = [('Finite simple', 'ordered induced-C5'), ('933/941', 'Sigma-critical', 'epsilon(G)=2'),
               ('nonadjacent', 'degree5', 'degree4', 'full B-touch'),
               ('exactly three', 'unique unary U', 'mixed L,S', 'positive incidence'),
               ('exactly one root-contact edge rx', 'no s edge', 'inclusion-minimal', '45/54'),
               ('outside U are retained', 't_r+', 't_s+'),
               ('L is long', 'exactly one named original boundary vertex', '>=4'),
               ('one coordinate per shared vertex', 'bridges/rotation', 'empty/nonempty fibres', 'whole graph')]
    for clause, words in zip(contract, markers):
        require(all(word in clause for word in words), 'incomplete declared source clause')
    claims = doc['claims']
    ids = [c['id'] for c in claims]
    require(ids == EXPECTED_IDS, 'claim inventory/order mismatch')
    required = {'id', 'quantifier', 'sufficient_premises', 'branch_premises', 'derived_prerequisites_rule',
                'dependencies', 'paper_argument', 'evidence_layer', 'coverage', 'uncovered', 'finding', 'status'}
    graph = {}
    for c in claims:
        name = c['id']
        require(required <= c.keys(), 'incomplete claim metadata: ' + name)
        require(set(contract) <= set(c['sufficient_premises']), 'claim source premise missing: ' + name)
        require(set(c['sufficient_premises']) == set(contract + c['branch_premises']),
                'unlisted extra source premise: ' + name)
        require(len(c['sufficient_premises']) == len(set(c['sufficient_premises'])),
                'duplicate claim premise: ' + name)
        internal = [d for d in c['dependencies'] if d.startswith('N45-SS-')]
        require(all(d in ids for d in internal), 'unknown internal dependency: ' + name)
        graph[name] = internal
        require(c['status'] == 'paper_candidate_under_listed_premises', 'claim status is promoted: ' + name)
        require('arbitrary-size paper candidate' in c['evidence_layer'], 'wrong evidence layer: ' + name)
        require(c['coverage']['finite_source_controls'] == 'not computed or constructed; no SS trigger count',
                'finite SS evidence has been promoted: ' + name)
        require('empty/nonempty fibres' in c['coverage']['full_lifts'], 'fibre scope omitted: ' + name)
        require('Whole-graph' in c['coverage']['symmetries'], 'common frame scope omitted: ' + name)
        require(len(c['uncovered']) == 6 and any('epsilon>=3' in x for x in c['uncovered']) and
                any('Source realization' in x for x in c['uncovered']) and any('Lean' in x for x in c['uncovered']),
                'uncovered boundaries omitted: ' + name)
        require(all(isinstance(c[k], str) and c[k] for k in ('quantifier', 'finding', 'derived_prerequisites_rule')),
                'empty claim metadata: ' + name)
    visiting, visited, order = set(), set(), []
    def visit(node):
        require(node not in visiting, 'claim dependency cycle: ' + node)
        if node in visited:
            return
        visiting.add(node)
        for dep in sorted(graph[node]):
            visit(dep)
        visiting.remove(node)
        visited.add(node)
        order.append(node)
    for node in ids:
        visit(node)
    for node, names in EXPECTED_EDGES.items():
        require(set(graph['N45-SS-' + node]) == {'N45-SS-' + x for x in names},
                'unexpected declared DAG edges: ' + node)
    branches = {c['id']: c['branch_premises'] for c in claims}
    require(branches['N45-SS-U3'] == ['|sigma_U|=3 and |sigma_L|=2.'], 'U3 branch coverage mismatch')
    require(branches['N45-SS-U2'] == ['|sigma_U|=2 and |sigma_L| in {2,3}.'], 'U2 branch coverage mismatch')
    for t in range(3):
        require(branches['N45-SS-T' + str(t)][0] == '|sigma_U|=2 and actual t_s=' + str(t) + '.',
                'spoke branch coverage mismatch')
        require(branches['N45-SS-T' + str(t)][1].startswith('Derived in preceding claims:'),
                'branch hypotheses postulated instead of declared derived')
    require('No new finite source calculation' in doc['finite_coverage'] and 'not SS controls' in doc['finite_coverage'],
            'PC/LP finite evidence boundary lost')
    require('cannot prove the mathematics' in doc['trust_boundary'], 'artifact theorem boundary lost')
    require('pending independent' in doc['adoption_status'], 'adoption status promoted')
    return {'claims': len(ids), 'contract_clauses': len(contract), 'topological_order': order,
            'shield_branches': [[2, 2], [2, 3], [3, 2]], 'length2_spoke_branches': [0, 1, 2],
            'mathematical_validity_checked': False}

def git(*args):
    run = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
    require(run.returncode == 0, 'read-only git command failed: ' + repr(args))
    return run.stdout

def regular_paths(directory):
    return {p.relative_to(directory).as_posix(): p for p in directory.rglob('*') if p.is_file() and not p.is_symlink()}

def audit():
    require(git('rev-parse', 'HEAD').decode().strip() == BASE, 'HEAD mismatch')
    for name in ['logs/worker-normal.combined.log', 'logs/worker-normal.json',
                 'logs/worker-seed17.combined.log', 'logs/worker-seed17.json', 'inputs-before.json']:
        require((OUT / 'frozen/supervision-execution' / name).read_bytes() ==
                (ROOT / 'audits/2026-10-10-n45-ss-supervision' / name).read_bytes(),
                'supervisor pure execution input drift: ' + name)
    freeze = json.loads((OUT / 'freeze.json').read_bytes())
    before = json.loads((OUT / 'frozen/supervision-execution/inputs-before.json').read_bytes())
    observed = regular_paths(FROZEN)
    require(set(observed) == set(freeze['worker_files']), 'frozen worker full regular inventory drift')
    require(set(observed) == set(regular_paths(ORIGINAL)), 'original worker full regular inventory drift')
    for name, info in freeze['worker_files'].items():
        require(file_hash(observed[name]) == info['sha256'], 'frozen byte drift: ' + name)
        require(file_hash(ORIGINAL / name) == info['sha256'], 'original worker byte drift: ' + name)
        require(before['worker'][name]['sha256'] == info['sha256'], 'supervisor prior freeze byte mismatch: ' + name)
    links = {p.relative_to(FROZEN).as_posix(): str(p.readlink()) for p in FROZEN.rglob('*') if p.is_symlink()}
    require(links == freeze['worker_symlinks'], 'frozen worker symlink inventory drift')
    for name, target in links.items():
        require((ORIGINAL / name).is_symlink() and str((ORIGINAL / name).readlink()) == target, 'original link drift: ' + name)
        require(before['worker'][name]['link'] == target, 'supervisor prior link mismatch: ' + name)
    require(set(before['worker']) == set(observed) | set(links), 'supervisor prior worker inventory mismatch')
    entries = parse_manifest((FROZEN / 'MANIFEST.sha256').read_bytes())
    payload = {k: freeze['worker_files'][k]['sha256'] for k in observed
               if k not in {'MANIFEST.sha256', 'delivery.json'} and not k.startswith('seal-checks/')}
    validate_entries(entries, payload)
    require(len(entries) == 6096, 'worker payload count mismatch')
    receipt = json.loads((FROZEN / 'delivery.json').read_bytes())
    require(receipt['manifest_sha256'] == sha((FROZEN / 'MANIFEST.sha256').read_bytes()), 'receipt manifest mismatch')
    require(receipt['payload_file_count'] == 6096, 'receipt count mismatch')
    require(receipt['excluded_from_payload_manifest'] == ['MANIFEST.sha256', 'delivery.json', 'seal-checks/**'],
            'receipt exclusion scope mismatch')
    require(receipt['postseal_checks'] == 'seal-checks/commands.json' and receipt['postseal_manifest'] == 'seal-checks/MANIFEST.sha256',
            'receipt seal metadata references mismatch')
    for key in ['shared_changes', 'new_Lean', 'new_source_realization', 'new_finite_source_certificate',
                'commit_push_pr_external_messages_subagents']:
        require(receipt[key] is False, 'receipt scope promoted: ' + key)
    seal = parse_manifest((FROZEN / 'seal-checks/MANIFEST.sha256').read_bytes())
    seal_observed = {k.removeprefix('seal-checks/'): freeze['worker_files'][k]['sha256'] for k in observed
                     if k.startswith('seal-checks/') and k != 'seal-checks/MANIFEST.sha256'}
    validate_entries(seal, seal_observed)
    require(len(seal) == 5, 'seal metadata count mismatch')
    records = json.loads((FROZEN / 'inputs.json').read_bytes())['inputs']
    records += json.loads((FROZEN / 'inputs-additional.json').read_bytes())
    counts = {'base': 0, 'current': 0, 'pins': 0}
    missing = []
    for item in records:
        if 'frozen' not in item:
            require(item['layer'] == 'BASE-missing' and item['exit_code'] == 128, 'undeclared missing input')
            missing.append(item['path'])
            continue
        raw = (FROZEN / item['frozen']).read_bytes()
        require(sha(raw) == item['sha256'], 'declared frozen input digest mismatch: ' + item['path'])
        if item['layer'] == 'BASE-git-blob':
            require(raw == git('show', BASE + ':' + item['path']), 'BASE object bytes mismatch: ' + item['path'])
            require(git('rev-parse', BASE + ':' + item['path']).decode().strip() == item['git_blob'], 'BASE object ID mismatch')
            require(raw == (OUT / 'frozen/base-object' / item['path']).read_bytes(), 'independent BASE freeze mismatch')
            require(raw == (FROZEN / 'base-source' / item['path']).read_bytes(), 'archive BASE input mismatch')
            counts['base'] += 1
        else:
            require(raw == (ROOT / item['path']).read_bytes(), 'live current input mismatch: ' + item['path'])
            require(raw == (OUT / 'frozen/live-current' / item['path']).read_bytes(), 'independent current freeze mismatch')
            counts['current'] += 1
        if 'expected_sha256' in item:
            require(PINS.get(item['path']) == item['sha256'] == item['expected_sha256'] and item['pin_match'] is True,
                    'task pin mismatch: ' + item['path'])
            counts['pins'] += 1
    require(counts == {'base': 24, 'current': 11, 'pins': 5}, 'input inventory count mismatch')
    require(missing == ['docs/c5_weak_deletion_minimal_obstruction.md'], 'historical missing probe mismatch')
    # Full BASE archive verification binds the regular files AND the five Git symlinks.
    tree = {}
    for row in git('ls-tree', '-r', '-z', BASE).split(b'\0'):
        if not row:
            continue
        prefix, name = row.split(b'\t', 1)
        mode, kind, oid = prefix.decode().split()
        require(kind == 'blob', 'nonblob BASE archive entry')
        tree[name.decode()] = (mode, oid)
    archive_dir = FROZEN / 'base-source'
    archived_regular = regular_paths(archive_dir)
    archived_links = {p.relative_to(archive_dir).as_posix(): str(p.readlink()) for p in archive_dir.rglob('*') if p.is_symlink()}
    require(set(tree) == set(archived_regular) | set(archived_links), 'BASE archive/tree exact inventory mismatch')
    for name, (mode, oid) in tree.items():
        if mode == '120000':
            raw = archived_links[name].encode()
            actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        else:
            path = archived_regular[name]
            actual = file_hash(path, 'sha1', b'blob ' + str(path.stat().st_size).encode() + b'\0')
        require(actual == oid, 'BASE archive Git blob mismatch: ' + name)
    tar_path = FROZEN / 'logs/base-archive.stdout.log'
    tar_receipt = json.loads((FROZEN / 'base-archive.json').read_bytes())
    require(file_hash(tar_path) == tar_receipt['sha256'], 'BASE original tar receipt mismatch')
    tar_seen = set()
    with tarfile.open(tar_path, 'r:*') as archive:
        for member in archive:
            if member.isdir():
                continue
            name = member.name
            require(name not in tar_seen and name in tree, 'BASE tar inventory mismatch: ' + name)
            tar_seen.add(name)
            if member.issym():
                require(archived_links.get(name) == member.linkname, 'BASE tar symlink mismatch: ' + name)
            else:
                require(member.isfile() and name in archived_regular, 'unsupported BASE tar entry: ' + name)
                h = hashlib.sha256()
                stream = archive.extractfile(member)
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(chunk)
                require(h.hexdigest() == file_hash(archived_regular[name]), 'BASE tar regular bytes mismatch: ' + name)
    require(tar_seen == set(tree), 'BASE original tar missing Git entries')
    declared_claims = validate_claims(json.loads((FROZEN / 'claims.json').read_bytes()))
    seal_commands = json.loads((FROZEN / 'seal-checks/commands.json').read_bytes())
    require(seal_commands['normal_seed17_byte_equal'] is True, 'seal replay receipt does not claim equal outputs')
    runs = seal_commands['commands']
    require([x['id'] for x in runs] == ['verify-sealed-normal', 'verify-sealed-seed17'], 'seal command inventory mismatch')
    outputs = []
    for i, command in enumerate(runs):
        require(command['exit_code'] == 0 and command['argv'] == ['python3', '-B', str(ORIGINAL / 'verify.py')], 'seal actual command receipt mismatch')
        require(command['cwd'] == str(ROOT) and command['env'] == ({} if i == 0 else {'PYTHONHASHSEED': '17'}), 'seal environment mismatch')
        require((FROZEN / command['stderr']).read_bytes() == b'', 'sealed replay stderr is nonempty')
        outputs.append((FROZEN / command['stdout']).read_bytes())
    require(outputs[0] == outputs[1], 'sealed normal/seed17 output mismatch')
    for label, seed in [('normal', None), ('seed17', '17')]:
        source = OUT / 'frozen/supervision-execution/logs'
        run = json.loads((source / ('worker-' + label + '.json')).read_bytes())
        require(run['exit_code'] == 0 and run['before_new_audit_directories'] is True and run['PYTHONHASHSEED'] == seed,
                'supervisor pre-audit actual execution receipt mismatch')
        require(run['argv'] == ['python3', '-B', 'audits/2026-10-10-n45-u-ss/verify.py'] and run['cwd'] == str(ROOT),
                'supervisor actual execution argv mismatch')
        require((source / ('worker-' + label + '.combined.log')).read_bytes() == outputs[0], 'supervisor pre-audit output mismatch')
    output = json.loads(outputs[0])
    require(output['base_blobs_verified'] == 24 and output['current_snapshots_verified'] == 11 and
            output['sealed_payload_file_count'] == 6096 and output['claims_with_required_metadata'] == 11 and
            output['preseal_mode'] is False, 'sealed verifier output receipt mismatch')
    checks = json.loads((FROZEN / 'checks.json').read_bytes())['commands']
    require(len(checks) == 71 and len({c['id'] for c in checks}) == 71, 'historical command inventory mismatch')
    for command in checks:
        require((FROZEN / command['stdout']).is_file() and (FROZEN / command['stderr']).is_file(), 'historical command log missing')
    failures = {c['id']: c['exit_code'] for c in checks if c['exit_code'] != 0}
    require(failures == {'base-blob-12': 128, 'base-docs': 1, 'current-whole-docgraph': 1,
                        'verify-initial': 1, 'verify-preseal-normal-failure': 1}, 'historical failure receipt changed')
    require((FROZEN / 'logs/verify-initial.stderr.log').read_text().strip() == 'own REPORT link missing: checks.json', 'initial historical failure reason changed')
    require((FROZEN / 'logs/verify-preseal-normal.stderr.log').read_text().strip() == 'missing final newline: gallai-primary.txt', 'preseal historical failure reason changed')
    docs_log = (FROZEN / 'logs/base-docs.stdout.log').read_text()
    for path in ['audits/2026-10-04-task-d5/c4/scope_ledger.json', 'audits/2026-10-04-task-d2/integration_doc_changes.diff']:
        require(path in docs_log and path not in tree, 'historical BASE missing path not retained')
    require('FAIL: 62 documents, 213 relations, 5 families; 62 errors' in (FROZEN / 'logs/current-whole-docgraph.stdout.log').read_text(), 'whole-worktree DocGraph failure lost')
    require('duplicate-id' in (FROZEN / 'logs/current-whole-docgraph.stderr.log').read_text(), 'whole-worktree duplicate evidence lost')
    report = (FROZEN / 'REPORT.md').read_text()
    for phrase in ['未重播', '未跑：', '無新圖計算／有限來源證書', 'artifact verifier 通過不驗證', '沒有 SS trigger count', '不能當作 SS']:
        require(phrase in report, 'evidence boundary reporting lost: ' + phrase)
    shared = json.loads((FROZEN / 'shared-before.json').read_bytes())
    require(len(shared) == 13146, 'worker shared-before inventory mismatch')
    for name, digest in shared.items():
        require((ROOT / name).is_file() and file_hash(ROOT / name) == digest, 'preexisting shared byte drift: ' + name)
    require(git('diff', '--binary') == (FROZEN / 'logs/initial-diff.stdout.log').read_bytes(), 'tracked worktree diff drift')
    require(git('diff', '--cached', '--binary') == (FROZEN / 'logs/initial-cached-diff.stdout.log').read_bytes(), 'tracked index diff drift')
    visible = set()
    for raw in git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split(b'\0'):
        if raw:
            name = raw.decode()
            if (ROOT / name).is_file():
                visible.add(name)
    added = visible - set(shared)
    require(all(name.startswith(ALLOWED_NEW_PREFIXES) for name in added), 'unapproved new path outside this audit batch')
    # Count additions only; do not read SSA/SSG judgments or supervisor decisions.
    return {'task': 'N45-SSC', 'base': BASE, 'judgment': 'PASS_ARTIFACT_INTEGRITY_ONLY',
            'worker_regular_files': len(observed), 'worker_payload_files': len(entries), 'worker_git_symlinks': len(links),
            'seal_metadata_files': len(seal), 'inputs': counts, 'base_archive_regular_files': len(archived_regular),
            'base_archive_git_symlinks': len(archived_links), 'base_tar_git_entries': len(tar_seen),
            'declared_claim_metadata': declared_claims, 'historical_failed_commands': failures,
            'preexisting_shared_files_verified': len(shared), 'allowed_added_prefixes': list(ALLOWED_NEW_PREFIXES),
            'outside_inventory_exact_equality_currently_applicable': False,
            'original_worker_verifier_rerun_in_this_audit': False,
            'sealed_and_supervisor_pre_audit_outputs_equal': True,
            'new_finite_source_certificate': False, 'ss_trigger_count': None,
            'pc_lp_controls_are_ss_controls': False, 'paper_adoption': 'NOT_ADJUDICATED',
            'general_validator_soundness': 'NOT_TESTED'}

def component_test(kind, path):
    if kind == 'claims':
        return validate_claims(json.loads(path.read_bytes()))
    if kind == 'manifest-fixture':
        fixture = json.loads(path.read_bytes())
        validate_entries(parse_manifest(fixture['manifest'].encode()), fixture['observed'])
        return {'component': kind, 'valid': True}
    raise ValueError('unknown component test')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--component', choices=['claims', 'manifest-fixture'])
    parser.add_argument('--fixture', type=Path)
    args = parser.parse_args()
    require(bool(args.component) == bool(args.fixture), 'component and fixture must be paired')
    result = component_test(args.component, args.fixture) if args.component else audit()
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
