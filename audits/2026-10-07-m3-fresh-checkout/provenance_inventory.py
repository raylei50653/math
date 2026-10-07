#!/usr/bin/env python3
"""Compare a conservative evidence/input inventory to the Oct 05 review head."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path('/tmp/math-m3-ba0b447')
OUT = Path(__file__).resolve().parent
REVIEW = 'a484d4cdaeb069702de0c40acf83bc6a05dea3b3'
CANDIDATE = 'ba0b447f09617591d9f2ba81c988f537af771791'


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True).stdout


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def literal_paths(script):
    tree = ast.parse((ROOT / script).read_text())
    result = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            if value.startswith(('artifacts/', 'docs/', 'scripts/', 'audits/')) and (ROOT / value).is_file():
                result.add(value)
    return result


def local_import_closure(script):
    seen = set()
    queue = [script]
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        for node in ast.walk(ast.parse((ROOT / path).read_text())):
            modules = []
            if isinstance(node, ast.Import):
                modules = [value.name for value in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module]
            for module in modules:
                local = 'scripts/' + module.replace('.', '/') + '.py'
                if (ROOT / local).is_file():
                    queue.append(local)
    return seen


def provenance_paths(value):
    """Saved leaf file paths supplement hand-inspected producer inputs."""
    result = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key.startswith(('artifacts/', 'docs/', 'scripts/', 'audits/')) and (ROOT / key).is_file():
                result.add(key)
            result |= provenance_paths(item)
    elif isinstance(value, list):
        for item in value:
            result |= provenance_paths(item)
    elif isinstance(value, str) and value.startswith(('artifacts/', 'docs/', 'scripts/', 'audits/')) and (ROOT / value).is_file():
        result.add(value)
    return result


def files(path):
    full = ROOT / path
    if full.is_file():
        return {path}
    return {p.relative_to(ROOT).as_posix() for p in full.rglob('*') if p.is_file() and '__pycache__' not in p.parts}


def main():
    assert git('rev-parse', 'HEAD').decode().strip() == CANDIDATE
    review_tree = set(git('ls-tree', '-r', '--name-only', REVIEW).decode().splitlines())
    review_manifest = json.loads(git('show', REVIEW + ':artifacts/MANIFEST.json'))['files']
    review_archive = json.loads(git('show', REVIEW + ':audits/ARCHIVE.json'))['files']
    groups = {}
    scripts = {
        'ES': 'scripts/c5_excess_two_finite_search.py',
        'ES_acceptance': 'scripts/c5_excess_two_finite_search_validation.py',
        'ER': 'scripts/c5_excess_two_independent_search.py',
        'E3_adjacent': 'scripts/c5_excess_two_e3_adjacent.py',
        'E3_degree6': 'scripts/c5_excess_two_e3_degree6.py',
        'E3_foundation': 'scripts/c5_excess_two_e3_foundation.py',
        'E3_nonadjacent': 'scripts/c5_excess_two_e3_nonadjacent.py',
        'E4_control': 'scripts/c5_excess_two_e4_control.py',
        'E4_reductions': 'scripts/c5_excess_two_e4_reductions.py',
        'E4C': 'scripts/c5_excess_two_e4c_controls.py',
        'E5_branches': 'scripts/c5_excess_two_e5_branches.py',
        'E5_controls': 'scripts/c5_excess_two_e5_controls.py',
        'E5_local': 'scripts/c5_excess_two_e5_local.py',
        'E6_controls': 'scripts/c5_excess_two_e6_controls.py',
        'E6_local_controls': 'scripts/c5_excess_two_e6_local_controls.py',
        'E6_reductions': 'scripts/c5_excess_two_e6_reductions.py',
        'Kprime': 'scripts/c5_kempe_diagonal_transport.py',
        'D8': 'audits/2026-10-04-task-d8/degree6_t1_spoke_coverage.py',
    }
    evidence = {
        'ES': ['artifacts/c5_excess_two_finite_search'],
        'ES_acceptance': ['artifacts/c5_excess_two_finite_search'],
        'ER': ['artifacts/c5_excess_two_independent_search', 'artifacts/c5_excess_two_finite_search'],
        'E3_adjacent': ['artifacts/c5_excess_two_e3/adjacent_rows.json'],
        'E3_degree6': ['artifacts/c5_excess_two_e3/degree6.json'],
        'E3_foundation': ['artifacts/c5_excess_two_e3/foundation.json'],
        'E3_nonadjacent': ['artifacts/c5_excess_two_e3/nonadjacent.json'],
        'E4_control': ['artifacts/c5_excess_two_e4/control.json'],
        'E4_reductions': ['artifacts/c5_excess_two_e4/reductions.json'],
        'E4C': ['artifacts/c5_excess_two_e4c'],
        'E5_branches': ['artifacts/c5_excess_two_e5/branches.json'],
        'E5_controls': ['artifacts/c5_excess_two_e5/controls.json'],
        'E5_local': ['artifacts/c5_excess_two_e5/local.json'],
        'E6_controls': ['artifacts/c5_excess_two_e6/controls.json'],
        'E6_local_controls': ['artifacts/c5_excess_two_e6/local_controls.json'],
        'E6_reductions': ['artifacts/c5_excess_two_e6/reductions.json'],
        'Kprime': ['artifacts/c5_kempe_diagonal_transport'],
        'D8': ['audits/2026-10-04-task-d8/degree6_t1_spoke_coverage.json'],
    }
    records = {}
    for name, script in scripts.items():
        inputs = local_import_closure(script)
        inspected = set()
        while True:
            todo = [path for path in inputs if path.endswith('.py') and path not in inspected]
            if not todo:
                break
            for local in todo:
                inspected.add(local)
                inputs |= local_import_closure(local)
                inputs |= literal_paths(local)
        products = set()
        for path in evidence[name]:
            products |= files(path)
        for path in sorted(products):
            if path.endswith('.json'):
                inputs |= provenance_paths(json.loads((ROOT / path).read_bytes()))
        # E3 degree-six reads CONTROL assembled from a root path; E4 uses E1_REL.
        if name in ('E3_degree6', 'E3_foundation', 'E5_controls', 'E5_local', 'E5_branches'):
            inputs.add('artifacts/c5_excess_two_e3/positive_control_inputs.json')
        if name == 'E4_control':
            inputs.add('artifacts/c5_excess_rejection_law/observations.json')
        if name in ('ES', 'ES_acceptance', 'ER'):
            inputs.add('artifacts/c5_cells/cells.json')
        all_paths = inputs | products
        changed = []
        missing = []
        for path in sorted(all_paths):
            if path not in records:
                raw = (ROOT / path).read_bytes()
                current = dict(bytes=len(raw), sha256=digest(raw))
                if path in review_tree:
                    old = git('show', REVIEW + ':' + path)
                    prior = dict(bytes=len(old), sha256=digest(old), reference='Git blob at review head')
                elif path in review_manifest:
                    entry = review_manifest[path]
                    prior = dict(bytes=entry['bytes'], sha256=entry['sha256'], reference='review artifacts/MANIFEST.json')
                elif path in review_archive:
                    entry = review_archive[path]
                    prior = dict(bytes=entry['bytes'], sha256=entry['sha256'], reference='review audits/ARCHIVE.json')
                else:
                    prior = None
                records[path] = dict(path=path, current=current, review=prior,
                                     equal_to_review=prior is not None and current['sha256'] == prior['sha256'] and current['bytes'] == prior['bytes'], groups=[])
            records[path]['groups'].append(name)
            if records[path]['review'] is None:
                missing.append(path)
            elif not records[path]['equal_to_review']:
                changed.append(path)
        groups[name] = dict(script=script, sources=sorted(inputs), evidence=sorted(products),
                            changed=changed, missing_review_reference=missing,
                            reuse_allowed=not changed and not missing)
    result = dict(candidate_sha=CANDIDATE, reference_review_sha=REVIEW,
                  method='Hand-inspected producer input paths, saved provenance paths, local Python import closure; ES/ER corpus inventory deliberately includes reports/logs as a conservative superset. Restored oversized bytes use the review pinned MANIFEST/ARCHIVE hashes when absent from its Git tree.',
                  files=len(records), equal_to_review=sum(r['equal_to_review'] for r in records.values()),
                  changed=[r for r in records.values() if r['review'] and not r['equal_to_review']],
                  missing_review_reference=[r['path'] for r in records.values() if r['review'] is None],
                  groups=groups, inventory=sorted(records.values(), key=lambda r:r['path']))
    with (OUT / 'dependency-inventory-v2.json').open('x') as stream:
        json.dump(result, stream, indent=2); stream.write('\n')
    print(json.dumps({key:result[key] for key in ('candidate_sha','reference_review_sha','files','equal_to_review','changed','missing_review_reference')}, indent=2))


if __name__ == '__main__':
    main()
