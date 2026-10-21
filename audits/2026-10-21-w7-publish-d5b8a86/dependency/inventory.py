#!/usr/bin/env python3
"""Read-only connected W7 publication inventory; writes only dependency/.
No Git mutation, solver, archive append, source rewrite, or pickle load.
"""
import collections,hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
ROOTS=[ROOT/'audits'/x for x in ('2026-10-20-w7-count-cone-d5b8a86','2026-10-20-w7-count-opt-d5b8a86','2026-10-21-w7-reuse-d5b8a86')]
tracked=set(subprocess.check_output(['git','-C',str(ROOT),'ls-files','-z']).decode().split('\0'))
archive=json.loads((ROOT/'audits/ARCHIVE.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transient(p):return '__pycache__' in p.parts or 'build' in p.parts or p.suffix in ('.pyc','.so')
def whitespace(p):
 try:s=p.read_text()
 except UnicodeError:return False
 return s.endswith('\n\n') or any(t.rstrip()!=t for t in s.splitlines())
records=[];ordinary=[];large=[];strict=[];trans=[]
for root in ROOTS:
 for p in sorted(root.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(ROOT).as_posix()
  if transient(p):trans.append({'path':rel,'bytes':p.stat().st_size});continue
  reasons=[]
  if p.stat().st_size>=1000000:reasons.append('large')
  if whitespace(p):reasons.append('historical-whitespace')
  rec={'path':rel,'bytes':p.stat().st_size,'sha256':sha(p),'mode':p.stat().st_mode&0o777,
       'suggested_archive_reasons':reasons}
  records.append(rec)
  if reasons:large.append(rel)
  else:ordinary.append(rel)
  if p.stat().st_size>=1000000 and p.suffix.lower() in {'.json','.jsonl','.ndjson','.json5','.bin'}:strict.append(rel)
custody=[]
for root in (ROOTS[0],ROOTS[2]):
 base=json.loads((root/'BASE.json').read_text());missing=[];drift=[];notpublished=[]
 for rec in base['inputs']:
  p=ROOT/rec['path']
  if not p.is_file():missing.append(rec['path']);continue
  if sha(p)!=rec['sha256']:drift.append(rec['path'])
  if rec['path'] not in tracked and rec['path'] not in archive['files']:
   notpublished.append(rec['path'])
 custody.append({'base':str((root/'BASE.json').relative_to(ROOT)),'inputs':len(base['inputs']),
                 'missing':missing,'drift':drift,'inputs_not_in_existing_git_or_archive':notpublished})
# Seal closure identifies preservation obligations without executing any audit.
seal=[]
for root in (ROOTS[0],ROOTS[2]):
 data=json.loads((root/'OUTPUTS.json').read_text());files=data if isinstance(data,list) else data['files']
 if isinstance(files,dict):files=[{'path':k,**v} for k,v in files.items()]
 drift=[]
 for rec in files:
  p=root/rec['path']
  if not p.is_file() or sha(p)!=rec['sha256']:drift.append(rec['path'])
 seal.append({'seal':str((root/'OUTPUTS.json').relative_to(ROOT)),'files':len(files),'drift':drift})
summary={}
for root in ROOTS:
 prefix=root.relative_to(ROOT).as_posix()+'/'
 rr=[r for r in records if r['path'].startswith(prefix)]
 summary[root.name]={'preserve_files':len(rr),'preserve_bytes':sum(r['bytes'] for r in rr),
  'ordinary_files':sum(not bool(r['suggested_archive_reasons']) for r in rr),
  'suggested_archive_files':sum(bool(r['suggested_archive_reasons']) for r in rr)}
result={'scope':'three connected W7 audit roots; excludes only bytecode/native build outputs',
 'root_summary':summary,'preserve_count':len(records),'preserve_bytes':sum(r['bytes'] for r in records),
 'ordinary_count':len(ordinary),'suggested_archive_count':len(large),
 'suggested_archive_bytes':sum(r['bytes'] for r in records if r['path'] in large),
 'strict_generated_policy_blockers_if_staged_raw':strict,
 'transient_exclusions':trans,'custody':custody,'seals':seal,'files':records}
(HERE/'inventory.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'ordinary-paths.txt').write_text(''.join(p+'\n' for p in ordinary))
(HERE/'archive-paths.txt').write_text(''.join(p+'\n' for p in large))
(HERE/'all-connected-paths.txt').write_text(''.join(r['path']+'\n' for r in records))
print(json.dumps({k:v for k,v in result.items() if k not in ('files','transient_exclusions')},indent=2))
