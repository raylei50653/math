#!/usr/bin/env python3
"""Read-only publication custody check; does not verify a mathematical theorem."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ROUTING = {
    'docs/STATUS.md', 'docs/c5_c4_triangle_core.md',
    'docs/c5_kempe_guide.md', 'docs/c5_state_guide.md',
}
AUDIT_DIRECTORY = 'audits/2026-10-16-r6-319-complete-e98a1cc'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def local_path(directory, relative):
    rel = PurePosixPath(relative)
    require(not rel.is_absolute() and '..' not in rel.parts and
            str(rel) == relative and bool(rel.parts),
            'invalid relative path: ' + relative)
    path = directory
    require(not path.is_symlink(), 'unexpected symlink: ' + str(path))
    for part in rel.parts:
        path /= part
        require(not path.is_symlink(), 'unexpected symlink: ' + str(path))
    return path


def files(directory):
    require(directory.is_dir() and not directory.is_symlink(),
            'invalid audit directory: ' + str(directory))
    result = {}
    for path in directory.rglob('*'):
        require(not path.is_symlink(), 'unexpected audit symlink: ' + str(path))
        require(path.is_dir() or path.is_file(),
                'unexpected audit entry: ' + str(path))
        if path.is_file() and '__pycache__' not in path.relative_to(directory).parts:
            result[str(path.relative_to(directory))] = path
    return result


def main():
    initial = json.loads(local_path(HERE, 'initial-state.json').read_bytes())
    require(initial['audit_directory'] == AUDIT_DIRECTORY, 'unexpected audit directory')
    audit = local_path(ROOT, AUDIT_DIRECTORY)
    expected = initial['audit_files']
    current = files(audit)
    require(len(expected) == 377, 'unexpected initial audit file count')
    require(current.keys() == expected.keys(), 'audit membership drift')
    for rel, row in expected.items():
        data = local_path(audit, rel).read_bytes()
        require(len(data) == row['bytes'], 'audit byte count drift: ' + rel)
        require(digest(data) == row['sha256'], 'audit content drift: ' + rel)

    manifest = json.loads(current['MANIFEST.json'].read_bytes())
    base = json.loads(current['BASE.json'].read_bytes())
    require(base['head'] == initial['head'] == manifest['BASE'], 'research BASE mismatch')
    require(initial['source_positivity'] == manifest['source_positivity'] == 'OPEN',
            'unexpected source positivity claim')
    subprocess.run(['git', 'merge-base', '--is-ancestor', base['head'], 'HEAD'],
                   cwd=ROOT, check=True)

    # The research checker excluded every basename MANIFEST.json, including
    # seven frozen manifests. The publication inventory includes all eight.
    mapped = {rel for rel in current if PurePosixPath(rel).name != 'MANIFEST.json'}
    require(len(mapped) == 369 and mapped == set(manifest['files']),
            'research manifest membership drift')
    for rel, expected_sha in manifest['files'].items():
        require(digest(current[rel].read_bytes()) == expected_sha,
                'research manifest content drift: ' + rel)

    authority = {row['path']: row['sha256'] for row in base['authority_files']}
    require(len(authority) == len(base['authority_files']) == 245,
            'unexpected authority membership')
    frozen = {rel.removeprefix('frozen/') for rel in current if rel.startswith('frozen/')}
    require(frozen == set(authority), 'frozen authority membership drift')
    nested_manifests = {rel for rel in current if rel != 'MANIFEST.json' and
                        PurePosixPath(rel).name == 'MANIFEST.json'}
    require(len(nested_manifests) == 7 and all(
        rel.startswith('frozen/') and rel.removeprefix('frozen/') in authority
        for rel in nested_manifests), 'uncovered nested manifest')
    for rel, expected_sha in authority.items():
        frozen_data = local_path(audit / 'frozen', rel).read_bytes()
        historical_data = subprocess.check_output(
            ['git', 'show', base['head'] + ':' + rel], cwd=ROOT)
        require(frozen_data == historical_data and digest(frozen_data) == expected_sha,
                'frozen or Git authority drift: ' + rel)
        if rel not in ROUTING:
            require(digest(local_path(ROOT, rel).read_bytes()) == expected_sha,
                    'live authority drift: ' + rel)

    routing = initial['routing_at_research_delivery']
    require(set(routing) == set(manifest['routing']) == ROUTING,
            'research routing membership drift')
    for rel, row in routing.items():
        require(row['snapshot'] == 'routing-at-research/' + rel + '.snapshot',
                'unexpected routing snapshot: ' + rel)
        snapshot = local_path(HERE, row['snapshot']).read_bytes()
        require(digest(snapshot) == row['sha256'] == manifest['routing'][rel],
                'research routing snapshot drift: ' + rel)

    print(json.dumps({
        'status': 'PASS', 'research_base': base['head'],
        'sealed_files_including_manifests': len(current),
        'research_manifest_files': len(manifest['files']),
        'nested_manifests_checked_via_base': len(nested_manifests),
        'frozen_authority_files': len(authority),
        'routing_snapshots': len(routing),
        'original_audit_bytes_unchanged': True,
        'source_positivity': 'OPEN', 'mathematical_proof_verifier': False,
    }, sort_keys=True))


if __name__ == '__main__':
    main()
