#!/usr/bin/env python3
"""Independent read-only artifact checks; no mathematical/source solver."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
WORKER = ROOT / 'audits/2026-10-10-n45-u-ss'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    proc = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
    assert proc.returncode == 0, (args, proc.returncode, proc.stderr.decode())
    return proc.stdout


def manifest(folder, manifest_name, excluded):
    entries = {}
    for line in (folder / manifest_name).read_text().splitlines():
        digest, rel = line.split('  ', 1)
        assert rel not in entries and re.fullmatch('[0-9a-f]{64}', digest)
        assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
        entries[rel] = digest
    actual = {str(p.relative_to(folder)) for p in folder.rglob('*')
              if p.is_file() and not excluded(str(p.relative_to(folder)))}
    assert actual == set(entries), ('exact inventory', sorted(actual ^ set(entries)))
    for rel, digest in entries.items():
        assert sha((folder / rel).read_bytes()) == digest, rel
    return len(entries)


def main():
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    inputs = json.loads((OUT / 'inputs.json').read_text())['inputs']
    base = current = missing = 0
    for item in inputs:
        if item['layer'] == 'BASE-missing':
            proc = subprocess.run(['git', 'show', BASE + ':' + item['path']],
                                  cwd=ROOT, capture_output=True)
            assert proc.returncode == item['exit_code'] == 128
            missing += 1
            continue
        frozen = (OUT / item['frozen']).read_bytes()
        assert sha(frozen) == item['sha256'], item['frozen']
        if item['layer'] == 'BASE-git-object':
            assert git('show', BASE + ':' + item['path']) == frozen
            assert git('rev-parse', BASE + ':' + item['path']).decode().strip() == item['git_blob']
            base += 1
        else:
            assert (ROOT / item['path']).read_bytes() == frozen, item['path']
            current += 1
    for args, log in [(('diff', '--binary'), 'tracked-diff'),
                      (('diff', '--cached', '--binary'), 'index-diff')]:
        assert git(*args) == (OUT / ('logs/' + log + '.stdout.log')).read_bytes()
    claims = json.loads((OUT / 'frozen/candidate/claims.json').read_text())
    judgment = json.loads((OUT / 'independent-judgment.json').read_text())
    seal = json.loads((OUT / 'judgment-seal.json').read_text())
    assert sha((OUT / seal['judgment']).read_bytes()) == seal['sha256']
    ids = [c['id'] for c in claims['claims']]
    assert len(ids) == len(set(ids)) == 11
    assert ids == [c['id'] for c in judgment['claims']]
    for original, decision in zip(claims['claims'], judgment['claims']):
        assert decision['source_contract'] == claims['source_contract']
        assert decision['branch_premises'] == original['branch_premises']
        assert all(x in original['sufficient_premises'] for x in claims['source_contract'])
        assert decision['independent_argument'] and decision['trust']
    worker_delivery = json.loads((WORKER / 'delivery.json').read_text())
    worker_count = manifest(WORKER, 'MANIFEST.sha256',
                            lambda s: s in {'MANIFEST.sha256', 'delivery.json'}
                            or s.startswith('seal-checks/'))
    assert worker_count == worker_delivery['payload_file_count']
    assert sha((WORKER / 'MANIFEST.sha256').read_bytes()) == worker_delivery['manifest_sha256']
    postseal_count = manifest(WORKER / 'seal-checks', 'MANIFEST.sha256',
                              lambda s: s == 'MANIFEST.sha256')
    report = (OUT / 'REPORT.md').read_text()
    links = 0
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', report):
        if re.match(r'^[a-z][a-z0-9+.-]*:', target):
            continue
        target = target.split('#', 1)[0]
        if target and target not in {'MANIFEST.sha256', 'delivery.json'}:
            assert (OUT / target).exists(), target
            links += 1
    authored = []
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.suffix in {'.json', '.md', '.py'}:
            raw = p.read_bytes()
            assert raw.endswith(b'\n') and all(x == x.rstrip() for x in raw.splitlines()), p.name
            if p.suffix == '.json':
                json.loads(raw)
            if p.suffix == '.py':
                compile(raw, str(p), 'exec')
            authored.append(p.name)
    print(json.dumps({'task': 'N45-SSA', 'base': BASE,
                      'scope': 'artifact bytes, Git objects, claim inventory, own text; no mathematical proof',
                      'base_git_objects': base, 'current_work_inputs': current,
                      'historical_missing_base_probe': missing,
                      'candidate_payload_exact_inventory': worker_count,
                      'candidate_postseal_exact_inventory': postseal_count,
                      'claims_metadata_matched': len(ids), 'report_local_links': links,
                      'tracked_diff_and_index_unchanged': True,
                      'authored_text_checked': authored}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
