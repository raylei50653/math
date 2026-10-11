#!/usr/bin/env python3
"""Read-only independent custody checks for the fixed A/B task deliveries."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
EXPECTED = {
    'direct': {'payload': 51, 'inputs': 18, 'exclusions': {'delivery.json', 'seal-receipt.json'}},
    'fibre': {'payload': 846, 'inputs': 58, 'exclusions': {'delivery.json'}},
}
PDF_SHA = '50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea'
PDF_URL = 'https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf'
HISTORICAL = ['inputs-initial.json', 'metadata-initial/claims.json',
              'metadata-initial/obligations.json', 'metadata-initial/reviews.json']


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True).stdout


def safe(name):
    p = PurePosixPath(name)
    return not p.is_absolute() and '..' not in p.parts and str(p) == name


def inventory(folder):
    regular, directories = {}, set()

    def walk(current):
        for item in os.scandir(current):
            name = Path(item.path).relative_to(folder).as_posix()
            mode = item.stat(follow_symlinks=False).st_mode
            need(not stat.S_ISLNK(mode), 'unexpected symlink: ' + name)
            if stat.S_ISDIR(mode):
                directories.add(name)
                walk(item.path)
            else:
                need(stat.S_ISREG(mode), 'unexpected special file: ' + name)
                raw = Path(item.path).read_bytes()
                regular[name] = {'bytes': len(raw), 'sha256': sha(raw)}
    walk(folder)
    return regular, directories


def check(slug):
    folder = ROOT / ('audits/2026-10-11-n45-s-long-s-' + slug)
    expected = EXPECTED[slug]
    regular, directories = inventory(folder)
    manifest_bytes = (folder / 'delivery.json').read_bytes()
    delivery = json.loads(manifest_bytes)
    need(delivery['base'] == BASE, 'delivery BASE differs')
    names = [item['path'] for item in delivery['files']]
    exclusions = [item['path'] for item in delivery['metadata_exclusions']]
    need(len(names) == len(set(names)) == expected['payload'], 'payload count/duplicates differ')
    need(len(exclusions) == len(set(exclusions)) and set(exclusions) == expected['exclusions'],
         'precise metadata exclusion set differs')
    need(not set(names) & set(exclusions), 'metadata overlaps payload')
    need(all(safe(name) for name in names + exclusions), 'unsafe relative path')
    need(set(regular) == set(names) | set(exclusions), 'complete regular-file tree differs')
    expected_dirs = {str(parent) for name in names + exclusions
                     for parent in PurePosixPath(name).parents if str(parent) != '.'}
    need(directories == expected_dirs, 'complete directory tree differs')
    for item in delivery['files']:
        need(regular[item['path']] == {key: item[key] for key in ('bytes', 'sha256')},
             'payload bytes/hash differs: ' + item['path'])
    if slug == 'direct':
        receipt = json.loads((folder / 'seal-receipt.json').read_bytes())
        need(receipt['summary']['delivery_sha256'] == sha(manifest_bytes), 'receipt digest differs')
        need(set(receipt['excluded_metadata_exact_paths']) == expected['exclusions'],
             'receipt exclusions differ')
    else:
        need(delivery['file_count'] == len(names) and delivery['other_exclusions'] == [],
             'file count/additional exclusions differ')
        need(delivery['historical_drafts'] == HISTORICAL, 'historical draft declaration differs')
        need(set(HISTORICAL + delivery['current_authority']) <= set(names),
             'historical/current authority file missing from payload')

    inputs = json.loads((folder / 'inputs.json').read_bytes())
    need(inputs['base'] == BASE, 'input BASE differs')
    entries = inputs.get('inputs', inputs.get('entries'))
    external = inputs.get('external_inputs', inputs.get('external_dependencies'))
    need(len(entries) == expected['inputs'], 'BASE input count differs')
    seen, frozen_paths = set(), set()
    for entry in entries:
        name, frozen_path = entry['path'], entry['frozen_path']
        need(safe(name) and frozen_path == 'frozen/' + name, 'unsafe/misnamed frozen path')
        need(name not in seen, 'duplicate input: ' + name)
        seen.add(name)
        frozen_paths.add(frozen_path)
        raw = (folder / frozen_path).read_bytes()
        need(len(raw) == entry['bytes'] and sha(raw) == entry['sha256'],
             'frozen bytes/hash differs: ' + name)
        blob = git('rev-parse', BASE + ':' + name).decode().strip()
        need(blob == entry['git_blob'] and git('cat-file', 'blob', blob) == raw,
             'BASE Git blob differs: ' + name)
        need((ROOT / name).read_bytes() == raw, 'live input differs: ' + name)
    need(len(external) == 1, 'external dependency count differs')
    external_results = []
    for entry in external:
        name = entry.get('frozen_path', entry.get('path'))
        need(safe(name), 'unsafe external pin path')
        raw = (folder / name).read_bytes()
        url = entry.get('url', entry.get('source_url'))
        need(len(raw) == entry['bytes'] == 164927 and sha(raw) == entry['sha256'] == PDF_SHA,
             'external pin bytes/hash differs')
        need(entry['git_blob'] is None and url == PDF_URL, 'external authority declaration differs')
        if name.startswith('frozen/'):
            frozen_paths.add(name)
        external_results.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw),
                                 'declared_url': url, 'origin_refetched': False})
    need({name for name in regular if name.startswith('frozen/')} == frozen_paths,
         'complete frozen-input inventory differs')

    finding_name = 'findings.json' if slug == 'direct' else 'source-findings.json'
    findings = json.loads((folder / finding_name).read_bytes())
    need(len(findings) == 1, 'missing artifact finding count differs')
    finding = findings[0]
    authority = finding.get('used_as_authority', finding.get('authority_admitted'))
    need(authority is False and finding['git_blob'] is None, 'missing artifact admitted as authority')
    missing = subprocess.run(['git', 'cat-file', '-e', BASE + ':' + finding['path']],
                             cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(missing.returncode == 128, 'expected missing BASE Git blob not reproduced')
    live = ROOT / finding['path']
    need(live.is_file(), 'recorded on-disk missing-BASE artifact is absent')
    finding_result = {'id': finding['id'], 'path': finding['path'],
                      'BASE_missing_blob_exit': missing.returncode,
                      'BASE_missing_blob_stderr': missing.stderr.decode(), 'authority_admitted': authority}
    if slug == 'direct':
        snapshot_path = finding['snapshot_path']
        snapshot = (folder / snapshot_path).read_bytes()
        need(snapshot_path in names and delivery['quarantine_is_in_payload'], 'quarantine omitted')
        need(sha(snapshot) == finding['sha256_observed'] and len(snapshot) == finding['bytes_observed'],
             'quarantine snapshot recorded bytes differ')
        finding_result['quarantine_matches_current_live'] = snapshot == live.read_bytes()
    else:
        finding_result['historical_physical_hash_matches_current_live'] = (
            sha(live.read_bytes()) == finding['physical_sha256'])
    need(inventory(folder) == (regular, directories), 'target tree changed during read-only verification')
    return {'task': slug, 'status': 'passes', 'payload_files': len(names),
            'payload_bytes': sum(item['bytes'] for item in delivery['files']),
            'precise_metadata_exclusions': sorted(exclusions),
            'regular_files': len(regular), 'directories': len(directories),
            'symlinks': 0, 'special_files': 0, 'extra_files': 0, 'missing_files': 0,
            'BASE_live_frozen_inputs': len(entries), 'external_pins': external_results,
            'historical_drafts_in_payload': delivery.get('historical_drafts', []),
            'missing_artifact': finding_result, 'target_tree_changed': False,
            'delivery_sha256': sha(manifest_bytes), 'report_sha256': regular['REPORT.md']['sha256'],
            'certificate_sha256': regular.get('certificate.json', {}).get('sha256')}


if __name__ == '__main__':
    print(json.dumps({'base': BASE, 'scope': 'byte custody/provenance only; no mathematical proof',
                      'results': [check(slug) for slug in ('direct', 'fibre')]},
                     ensure_ascii=False, sort_keys=True, indent=2))
