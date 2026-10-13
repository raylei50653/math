#!/usr/bin/env python3
"""Read-only package inventory, links, diagram maps, and receipt custody."""
import argparse
import gzip
import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    documents = sorted(p for p in HERE.rglob('*.md') if 'frozen' not in p.relative_to(HERE).parts)
    links = 0
    for path in documents:
        content = path.read_text()
        assert all(line == line.rstrip() for line in content.splitlines()), path
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', content):
            target = target.split('#', 1)[0]
            if not target or '://' in target:
                continue
            assert (path.parent / target).exists(), (path, target)
            links += 1
    cert_path = HERE / 'search/CERTIFICATE.json.gz'
    cert = json.loads(gzip.decompress(cert_path.read_bytes()))
    checker = HERE / 'review/independent_check.py'
    for name in ['INDEPENDENT_CHECK.json', 'INDEPENDENT_CHECK_SEED17.json']:
        receipt = json.loads((HERE / 'review' / name).read_text())
        assert receipt['accepted']
        assert receipt['certificate_sha256'] == digest(cert_path)
        assert receipt['checker_sha256'] == digest(checker)
        assert receipt['inputs_sha256'] == digest(HERE / 'INPUTS.json')
        assert all(v['rejected'] for v in receipt['corrupt_certificates'].values())
    figure_graphs = json.loads((HERE / 'figures/named_caps.json').read_text())
    mappings = json.loads((HERE / 'figures/MAPPINGS.json').read_text())
    caps = {c['cap_id']: c for c in cert['caps']}
    assert len(figure_graphs) == len(mappings) == 3
    for graph, record in zip(figure_graphs, mappings):
        assert graph['id'] == record['figure']
        mapping = record['figure_vertex_to_certificate_vertex']
        assert sorted(mapping) == list(range(12))
        mapped = {tuple(sorted((mapping[a], mapping[b]))) for a, b in graph['edges']}
        assert mapped == set(map(tuple, caps[record['cap_id']]['edges']))
    assert ET.parse(HERE / 'figures/three_caps.svg').getroot().tag.endswith('svg')
    return {'status': 'PASS', 'authored_documents': len(documents), 'existing_local_links': links,
            'three_diagrams_match_all_certificate_edges': True,
            'checker_receipt_hashes_match_current_artifacts': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seal', action='store_true')
    args = parser.parse_args()
    result = check()
    if args.seal:
        with (HERE / 'ARTIFACT_CHECK.json').open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
        records = []
        for path in sorted(HERE.rglob('*')):
            if path.is_file() and path.name != 'MANIFEST.json':
                records.append({'path': str(path.relative_to(HERE)), 'bytes': path.stat().st_size,
                                'sha256': digest(path)})
        with (HERE / 'MANIFEST.json').open('x') as stream:
            json.dump({'schema': 'c6-cap-package-inventory-v1', 'files': records}, stream, indent=2)
            stream.write('\n')
    else:
        manifest = json.loads((HERE / 'MANIFEST.json').read_text())
        actual = {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p.name != 'MANIFEST.json'}
        assert actual == {r['path'] for r in manifest['files']}, 'inventory set drift'
        for record in manifest['files']:
            path = HERE / record['path']
            assert path.stat().st_size == record['bytes'] and digest(path) == record['sha256'], record['path']
        result['inventory_files_verified'] = len(manifest['files'])
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
