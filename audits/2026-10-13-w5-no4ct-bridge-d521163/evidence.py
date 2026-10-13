#!/usr/bin/env python3
"""Read-only custody and bridge bookkeeping; never re-enumerates colourings."""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
BASE = 'd5211633ba80c2b10cb12eaa8189421e35a31cc3'
PACKAGES = [
    'w5-three-support-19209f4c', 'w5-private-unicyclic-3097ef5',
    'w5-rank2-243a125', 'w5-rank3-essential-45bc1c3',
    'w5-rank3-contractible-50d5474', 'w5-rank4-contractible-acd2b1b',
    'w5-rank4-essential-acd2b1b',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=REPO)


class Reader:
    def __init__(self):
        self.archive = json.loads(git_bytes('audits/ARCHIVE.json'))
        self.archived = set()

    def read(self, path):
        record = self.archive['files'].get(path)
        if record:
            blob = self.archive['blobs'][record['sha256']]
            packed = (REPO / blob['path']).read_bytes()
            assert sha(packed) == blob['sha256'] and len(packed) == blob['bytes'], path
            data = gzip.decompress(packed)
            assert sha(data) == record['sha256'] and len(data) == record['bytes'], path
            self.archived.add(path)
        else:
            data = (REPO / path).read_bytes()
        return data


def seal_records(reader):
    records, seals = [], []
    for name in PACKAGES:
        prefix = 'audits/2026-10-13-' + name + '/'
        path = prefix + ('MANIFEST.json' if name == 'w5-rank3-essential-45bc1c3' else 'DELIVERY.json')
        raw = reader.read(path)
        seal = json.loads(raw)
        seals.append({'path': path, 'sha256': sha(raw), 'bytes': len(raw),
                      'original_base': seal.get('base', seal.get('BASE'))})
        for item in seal.get('files', seal.get('entries')):
            original = item['path']
            path = original if original.startswith(('audits/', 'docs/')) else prefix + original
            storage = path
            # The original rank3-C seal also bound shared docs. Publication kept
            # those historical bytes separately; never compare them to today's docs.
            historical_gzip = path.startswith('docs/')
            if historical_gzip:
                storage = 'audits/2026-10-13-k13-rank3-publication/source-docs/rank3/' + path + '.gz'
            records.append({'seal': seals[-1]['path'], 'path': path,
                            'storage': storage, 'historical_gzip': historical_gzip,
                            'sha256': item['sha256'], 'bytes': item['bytes']})
    return seals, records


def canonical(row):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in row)


def check(inputs_path):
    reader = Reader()
    manifest = json.loads(inputs_path.read_text())
    assert manifest['base'] == BASE
    for item in manifest['proof_inputs']:
        packed = (ROOT / item['frozen']).read_bytes()
        assert sha(packed) == item['stored_sha256'], item['path']
        raw = gzip.decompress(packed)
        assert sha(raw) == item['sha256'] and len(raw) == item['bytes'], item['path']
        assert raw == git_bytes(item['path']), item['path']
    seals, records = seal_records(reader)
    assert seals == manifest['original_seals'], 'original seal changed'
    assert records == manifest['original_records'], 'original record inventory changed'
    for item in records:
        raw = reader.read(item['storage'])
        if item['historical_gzip']:
            raw = gzip.decompress(raw)
        assert sha(raw) == item['sha256'] and len(raw) == item['bytes'], item['path']
        if not item['historical_gzip'] and (REPO / item['path']).exists():
            assert sha((REPO / item['path']).read_bytes()) == item['sha256'], item['path']

    raw = git_bytes('artifacts/c5_cells/cells.json')
    assert sha(raw) == manifest['catalogue_sha256']
    catalogue = json.loads(raw)
    masks = set(map(int, catalogue['cells']))
    rows = sorted({canonical(t) for t in itertools.product(range(4), repeat=5)
                   if all(t[i] != t[(i+1) % 5] for i in range(5))})
    assert len(masks) == 132 and list(map(list, rows)) == catalogue['pattern_order']
    actions = [[rows.index(canonical([beta[(offset+sign*i) % 5] for i in range(5)]))
                for beta in rows] for sign in (1, -1) for offset in range(5)]
    assert all(sum(1 << action[i] for i in range(10) if m & (1 << i)) in masks
               for m in masks for action in actions)
    assert all(m not in masks for m in (932, 933, 941))
    groups = []
    for name in PACKAGES:
        prefix = 'audits/2026-10-13-' + name + '/'
        summary_path = prefix + ('forest/summary.json' if name.startswith('w5-three') else 'controls/summary.json')
        summary = json.loads(reader.read(summary_path))
        assert set(map(int, summary['masks'])) <= masks
        assert sum(summary['masks'].values()) == summary['templates']
        if name.startswith('w5-three'):
            subset = 0  # paper inequality: r >= 10 and r <= 10-2c <= 8
        else:
            by_size = summary.get('types', summary.get('by_r'))
            subset = sum(n for key, n in by_size.items()
                         if int(key.split('_r')[1].split('_')[0] if '_r' in key else key) >= 10)
        metadata_masks = None
        if name in PACKAGES[1:5]:
            templates = json.loads(reader.read(prefix + 'controls/templates.json'))
            selected = [row for row in templates
                        if row.get('r', row.get('parameters', {}).get('r', -1)) >= 10]
            assert len(selected) == subset
            metadata_masks = dict(sorted(Counter(row['Sigma'] for row in selected).items()))
            assert set(metadata_masks) <= masks
            if name in PACKAGES[1:3]:
                assert set(metadata_masks) == {1023}
        groups.append({'package': name, 'old_templates': summary['templates'],
                       'r_ge_10_metadata_subset': subset,
                       'r_ge_10_index_masks': metadata_masks,
                       'masks': summary['masks'],
                       'mathematical_sha256': summary.get('mathematical_sha256'),
                       'summary_sha256': sha(reader.read(summary_path))})
    assert [g['r_ge_10_metadata_subset'] for g in groups] == [0, 252, 70, 790, 484, 2955, 2368]
    return {'status': 'PASS', 'base': BASE, 'proof_inputs': len(manifest['proof_inputs']),
            'original_seals': len(seals), 'sealed_records': len(records),
            'archived_paths_verified': len(reader.archived), 'old_evidence_drift': 0,
            'K132_D5_closed': True, 'groups': groups,
            'old_templates': sum(g['old_templates'] for g in groups),
            'r_ge_10_metadata_subset': sum(g['r_ge_10_metadata_subset'] for g in groups),
            'colouring_enumeration_replayed': False,
            'coverage_proof': 'PROOF.md and independent branch reviews; not proved by this script',
            'actual_minimum_source': 'not triggered', 'new_Lean_theorem': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', type=Path, default=ROOT / 'INPUTS.json')
    args = parser.parse_args()
    print(json.dumps(check(args.inputs), sort_keys=True, indent=2))
