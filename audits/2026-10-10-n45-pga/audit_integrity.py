#!/usr/bin/env python3
import hashlib,json,re,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent
for p in D.rglob('*.json'):
    json.loads(p.read_text())
j=json.loads((D/'independent-judgment.json').read_text())
assert len(j['claims'])==6 and not j['new_supervisor_PR_PC_outputs_read_before_seal']
assert j['LP_status']=='OPEN' and j['counts']['complete_target_sources']==0
text=(D/'REPORT.md').read_text()
assert not any(line.rstrip()!=line for line in text.splitlines())
for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
    if not target.startswith(('http:','https:')) and target not in ['MANIFEST.sha256','delivery.json']:
        assert (D/target.split('#')[0]).exists(),target
assert (D/'logs/pg-normal.stdout.log').read_bytes()==(D/'logs/pg-seed17.stdout.log').read_bytes()
assert (D/'logs/independent-normal.stdout.log').read_bytes()==(D/'logs/independent-seed17.stdout.log').read_bytes()
for name in ['worker-exclusive-guard','input-exclusive-guard']:
    c=json.loads((D/'logs'/f'{name}.command.json').read_text())
    assert c['exit_code']==1 and b'FileExistsError' in (D/'logs'/f'{name}.stderr.log').read_bytes()
for e in json.loads((D/'inputs.json').read_text())['entries']:
    assert hashlib.sha256((D/e['frozen']).read_bytes()).hexdigest()==e['sha256']
print('PASS: JSON, six sealed claims, OPEN boundary, report local links, whitespace, replay bytes, expected exclusive-create refusals and immutable inputs')
