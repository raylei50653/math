#!/usr/bin/env python3
"""Independent inventories and command logging; no mathematical theorem verifier."""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
WORKER = ROOT / 'audits/2026-10-10-n45-u-ss'
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
SHARED = ['docs/c5_excess_two_nonadjacent_unit_core45.md', 'docs/c5_kempe_guide.md',
          'docs/STATUS.md', 'docs/c5_phase_b_common_lemmas.md', 'artifacts/c5_excess_two_e4/REPORT.md',
          'docs/history/2026-10-10-n45-lp-adoption.md', 'docs/HANDOFF.md', 'README.md',
          'docs/DOCUMENTATION.md', 'docs/c5_excess_two_root_deletions.md',
          'docs/c5_excess_two_mixed_omission.md', 'docs/c5_research_synthesis.md']
def sha(data): return hashlib.sha256(data).hexdigest()
def put(name, obj):
    with (OUT/name).open('x') as f: json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True); f.write('\n')
def git(*args):
    p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, check=True)
    return p.stdout
def file_state(p):
    s = p.lstat()
    if stat.S_ISLNK(s.st_mode): return {'link': os.readlink(p), 'mtime_ns': s.st_mtime_ns}
    assert stat.S_ISREG(s.st_mode), str(p)
    return {'sha256': sha(p.read_bytes()), 'bytes': s.st_size, 'mtime_ns': s.st_mtime_ns}
def tree(p):
    return {str(f.relative_to(p)): file_state(f) for f in sorted(p.rglob('*'))
            if f.is_symlink() or f.is_file()}
def manifest(p, exclude):
    lines = (p/'MANIFEST.sha256').read_text().splitlines()
    entries = dict((rel, digest) for digest, rel in (line.split('  ', 1) for line in lines))
    assert len(entries) == len(lines)
    actual = {str(f.relative_to(p)) for f in p.rglob('*') if f.is_file()
              and not exclude(str(f.relative_to(p)))}
    assert actual == set(entries), (actual-set(entries), set(entries)-actual)
    for rel, digest in entries.items(): assert sha((p/rel).read_bytes()) == digest, rel
    return len(entries)
def worker():
    n = manifest(WORKER, lambda r: r in {'MANIFEST.sha256', 'delivery.json'} or r.startswith('seal-checks/'))
    d = json.loads((WORKER/'delivery.json').read_text())
    assert n == d['payload_file_count'] == 6096
    assert sha((WORKER/'MANIFEST.sha256').read_bytes()) == d['manifest_sha256']
    metadata = WORKER/'seal-checks'
    meta_count = manifest(metadata, lambda r: r == 'MANIFEST.sha256')
    records = json.loads((WORKER/'inputs.json').read_text())['inputs']
    records += json.loads((WORKER/'inputs-additional.json').read_text())
    counts = {'BASE': 0, 'current': 0, 'pins': 0, 'probe_missing': []}
    for r in records:
        if 'frozen' not in r: counts['probe_missing'].append(r['path']); continue
        data = (WORKER/r['frozen']).read_bytes()
        assert sha(data) == r['sha256']
        if r['layer'] == 'BASE-git-blob':
            assert git('show', BASE+':'+r['path']) == data
            assert git('rev-parse', BASE+':'+r['path']).decode().strip() == r['git_blob']
            counts['BASE'] += 1
        else:
            assert (ROOT/r['path']).read_bytes() == data
            counts['current'] += 1
        if 'expected_sha256' in r:
            assert sha(data) == r['expected_sha256']; counts['pins'] += 1
    return {'payload_files': n, 'seal_metadata_files': meta_count, 'inputs': counts}
def freeze():
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    checked = worker()
    outside = {}
    for raw in git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split(b'\0'):
        if not raw: continue
        rel = raw.decode(); p = ROOT/rel
        if p.is_relative_to(OUT) or not (p.is_file() or p.is_symlink()): continue
        outside[rel] = file_state(p)
    put('inputs-before.json', {'BASE': BASE, 'worker': tree(WORKER), 'existing': outside,
                              'git_status': git('status', '--short').decode(), 'checks': checked})
    put('shared-before.json', {r: (ROOT/r).read_text() for r in SHARED})
    print(json.dumps(checked, ensure_ascii=False, sort_keys=True))
def log(label, argv, seed=False):
    logs = OUT/'logs'; logs.mkdir(exist_ok=True)
    env = os.environ.copy()
    if seed: env['PYTHONHASHSEED'] = '17'
    p = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True)
    for suffix, data in [('stdout.log', p.stdout), ('stderr.log', p.stderr)]:
        with (logs/f'{label}.{suffix}').open('xb') as f: f.write(data)
    put(f'logs/{label}.json', {'argv': argv, 'cwd': str(ROOT), 'exit_code': p.returncode,
                             'PYTHONHASHSEED': '17' if seed else None})
    print(json.dumps({'label': label, 'exit_code': p.returncode, 'stdout_bytes': len(p.stdout),
                      'stderr_bytes': len(p.stderr)}))
    return p.returncode
if __name__ == '__main__':
    if sys.argv[1:] == ['freeze']: freeze()
    elif sys.argv[1] == 'run':
        label = sys.argv[2]; argv = sys.argv[3:]; seed = argv[:1] == ['--seed17']
        if seed: argv = argv[1:]
        sys.exit(log(label, argv, seed))
    else: raise SystemExit('expected freeze or run LABEL [--seed17] COMMAND...')
