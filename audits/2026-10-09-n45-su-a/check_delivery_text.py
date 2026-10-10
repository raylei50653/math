#!/usr/bin/env python3
"""Validate the audit's delivery text and supplementary input immutability."""
import hashlib,json,re,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):
 s=p.stat();return {'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'sha256':h(p)}
s=json.loads((OUT/'supplementary-inputs.json').read_text())
for k in ('A_findings_inputs','comparison_reports'):
 for rel,r in s[k].items():assert rec(ROOT/rel)==r,(k,rel)
for row in s['additional_BASE_inputs']:
 p=Path(row['read_path']);assert rec(p)=={k:row[k] for k in ('bytes','mtime_ns','sha256')},str(p)
base=json.loads((OUT/'inputs.json').read_text())['BASE']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base
sealed=json.loads((OUT/'independent-judgment.json').read_text())
assert len(sealed['claims'])==14 and not sealed['supervision_decisions_read_before_seal']
assert h(OUT/'independent-judgment.json')==(OUT/'independent-judgment.sha256').read_text().split()[0]
assert (OUT/'input-verification.json').read_bytes()==(OUT/'input-verification-seed17.json').read_bytes()
json_count=text_count=0
for p in sorted(OUT.rglob('*')):
 if not p.is_file():continue
 if p.suffix=='.json':json.loads(p.read_text());json_count+=1
 if p.suffix in ('.md','.py','.json','.sha256'):
  raw=p.read_bytes();assert raw.endswith(b'\n'),str(p)
  for n,line in enumerate(raw.decode().splitlines(),1):assert line==line.rstrip(),(str(p),n)
  text_count+=1
text=(OUT/'REPORT.md').read_text();in_fence=False;count=0
planned={'checks.json','MANIFEST.sha256','delivery.json'}
for n,line in enumerate(text.splitlines(),1):
 if line.startswith('```'):in_fence=not in_fence;continue
 if in_fence:continue
 for ref in re.findall(r'\]\(([^\s)]+)\)',line):
  if re.match(r'https?://',ref):continue
  target=ref.split('#')[0]
  if not target:continue
  assert (OUT/target).exists() or target in planned,(n,target)
  count+=1
print(json.dumps({'task':'N45-SU-A','supplementary_BASE_inputs':len(s['additional_BASE_inputs']),'supplementary_drift':0,'sealed_claims':14,'independent_record_hash_unchanged':True,'normal_seed17_verification_byte_equal':True,'JSON_files_checked':json_count,'text_files_checked':text_count,'report_local_links_checked':count,'planned_delivery_links':sorted(planned),'PASS':True},sort_keys=True))
