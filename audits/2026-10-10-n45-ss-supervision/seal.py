#!/usr/bin/env python3
"""Exclusive-create final management receipts; preserve all frozen deliveries."""
import difflib, json, re
from datetime import datetime, timezone
import review as r

MODIFIED = ['docs/c5_excess_two_nonadjacent_unit_core45.md', 'docs/c5_kempe_guide.md',
            'docs/STATUS.md', 'docs/c5_phase_b_common_lemmas.md', 'artifacts/c5_excess_two_e4/REPORT.md',
            'docs/history/2026-10-10-n45-lp-adoption.md']
HISTORY = 'docs/history/2026-10-10-n45-ss-adoption.md'

def main():
    b = json.loads((r.OUT/'inputs-before.json').read_text())
    old = json.loads((r.OUT/'shared-before.json').read_text())
    assert r.git('rev-parse', 'HEAD').decode().strip() == r.BASE
    assert r.tree(r.WORKER) == b['worker']
    inc = json.loads((r.OUT/'incoming-audits.json').read_text())
    for rel, item in inc.items(): assert r.tree(r.ROOT/rel) == item['state'], rel
    changed = sorted(rel for rel, text in old.items() if (r.ROOT/rel).read_text() != text)
    assert changed == sorted(MODIFIED), changed
    after = {rel: r.sha((r.ROOT/rel).read_bytes()) for rel in changed}
    for rel, item in b['existing'].items():
        if rel not in changed: assert r.file_state(r.ROOT/rel) == item, rel
    allowed = [str(r.OUT.relative_to(r.ROOT))+'/', *[a+'/' for a in inc]]
    actual = set()
    for raw in r.git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split(b'\0'):
        if not raw: continue
        rel = raw.decode(); p = r.ROOT/rel
        if p.is_file() or p.is_symlink(): actual.add(rel)
    extra = actual-set(b['existing'])
    assert all(rel == HISTORY or any(rel.startswith(a) for a in allowed) for rel in extra), sorted(extra)
    r.put('shared-after.json', after)
    diff = ''.join(''.join(difflib.unified_diff(old[rel].splitlines(True), (r.ROOT/rel).read_text().splitlines(True),
                                              fromfile='before/'+rel, tofile='after/'+rel)) for rel in changed)
    with (r.OUT/'management.diff').open('x') as f: f.write(diff)
    logs = {p.stem: json.loads(p.read_text()) for p in sorted((r.OUT/'logs').glob('*.json'))}
    for label, item in logs.items():
        expected = 1 if label in {'baseline-docs', 'whole-docgraph-after'} else 0
        assert item['exit_code'] == expected, (label, item['exit_code'])
    for normal, seeded, ext in [('worker-normal', 'worker-seed17', 'combined.log'),
                               ('ssg-normal', 'ssg-seed17', 'stdout.log'),
                               ('ssc-normal', 'ssc-seed17', 'stdout.log')]:
        assert (r.OUT/f'logs/{normal}.{ext}').read_bytes() == (r.OUT/f'logs/{seeded}.{ext}').read_bytes()
    assert after[MODIFIED[0]] in (r.ROOT/HISTORY).read_text(), 'next task authority pin'
    r.put('integration-checks.json', {'commands': logs, 'worker_and_independent_audits_unchanged': True,
          'shared_modified': changed, 'new_files_confined_to_audits_and_history': True,
          'BASE_check_docs': 'FAIL: two historical missing paths', 'current_check_docs': 'PASS',
          'formal_docs_DocGraph': 'PASS', 'whole_worktree_DocGraph': 'FAIL: retained duplicate IDs',
          'general_N2_E': 'OPEN', 'propagation_stop': 'L2', 'next_task_started': False,
          'not_run': ['Lean build/axioms', 'PC LP checker as SS control', 'source search',
                      'all upstream source enumerations', 'remote CI']})
    links = 0
    for p in [r.OUT/'REPORT.md', r.ROOT/HISTORY]:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text()):
            if re.match(r'^[a-z][a-z0-9+.-]*:', target): continue
            target = target.split('#', 1)[0]
            if target: assert (p.parent/target).exists(), (str(p), target); links += 1
    authored = []
    for p in sorted(r.OUT.iterdir()):
        if not p.is_file() or p.suffix not in {'.md', '.json', '.py'}: continue
        raw = p.read_bytes()
        assert raw.endswith(b'\n') and all(line == line.rstrip() for line in raw.splitlines()), p.name
        if p.suffix == '.json': json.loads(raw)
        if p.suffix == '.py': compile(raw, str(p), 'exec')
        authored.append(p.name)
    r.put('output-validation.json', {'local_report_history_links': links, 'authored_text_checked': authored})
    pins = ['audits/2026-10-10-n45-ss-supervision/REPORT.md',
            'audits/2026-10-10-n45-ss-supervision/acceptance.json', MODIFIED[0], HISTORY]
    paths = sorted(p for p in r.OUT.rglob('*') if p.is_file() and p.name not in {'MANIFEST.sha256', 'delivery.json'})
    assert not any('__pycache__' in p.parts for p in paths)
    with (r.OUT/'MANIFEST.sha256').open('x') as f:
        for p in paths: f.write(r.sha(p.read_bytes())+'  '+str(p.relative_to(r.OUT))+'\n')
    r.put('delivery.json', {'task': 'N45-SS-supervision', 'BASE': r.BASE,
          'sealed_utc': datetime.now(timezone.utc).isoformat(), 'payload_files': len(paths),
          'manifest_sha256': r.sha((r.OUT/'MANIFEST.sha256').read_bytes()),
          'pinned_outputs': {rel: r.sha((r.ROOT/rel).read_bytes()) for rel in pins},
          'worker_payload_files': 6096, 'independent_audits': {rel: v['payload_files'] for rel, v in inc.items()},
          'mathematical_status': 'N45-U-SS adopted; specified N45-U identity closed by scoped composition',
          'commands_logged': len(logs), 'shared_modified': changed, 'general_N2_E': 'OPEN',
          'next_task': 'N45-S-LOW1, prepared and not started', 'propagation_stop': 'L2',
          'publication': 'no commit/push/PR/external messages', 'git_status': r.git('status', '--short').decode()})
    import verify
    verify.main()

if __name__ == '__main__': main()
