#!/usr/bin/env python3
"""Read-only hash/manifest/Git-object verification. Does not import worker judgements."""
from pathlib import Path
import hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent;d=json.loads((D/'inputs.json').read_text());R=Path(d['root']);S=Path(d['source']);B=d['BASE']
sha=lambda x:hashlib.sha256(x).hexdigest()
fail=[];manifest_rows=0;deliveries=0;base_rows=0
for f in d['inputs']:
 p=(R if f['kind']=='frozen-new' else S)/f['path'];b=p.read_bytes()
 if sha(b)!=f['sha256'] or len(b)!=f['bytes']:fail.append(['input',str(p)])
 if f['kind']=='frozen-new':
  if (D/'frozen'/f['path']).read_bytes()!=b:fail.append(['frozen',f['path']])
 else:
  g=subprocess.check_output(['git','show',f"{B}:{f['path']}"],cwd=R)
  if g!=b:fail.append(['BASE-object',f['path']])
for task in ['s','u','su-a','su-j','j','su-supervision']:
 p=R/'audits'/('2026-10-09-n45-'+task)
 m=p/'MANIFEST.sha256'
 if m.exists():
  seen=set()
  for line in m.read_text().splitlines():
   if not line.strip():continue
   h,rel=line.split(None,1);rel=rel.lstrip('*')
   if rel in seen:fail.append(['duplicate-manifest',task,rel])
   seen.add(rel);q=p/rel;manifest_rows+=1
   if not q.is_file() or sha(q.read_bytes())!=h:fail.append(['manifest',task,rel])
 delivery=p/'delivery.json'
 if delivery.exists():
  dd=json.loads(delivery.read_text())
  for f in dd.get('files',[]):
   if not isinstance(f,dict) or 'path' not in f:continue
   q=p/f['path'];deliveries+=1
   if not q.is_file() or sha(q.read_bytes())!=f['sha256'] or len(q.read_bytes())!=f['bytes']:fail.append(['delivery',task,f['path']])
 for f in json.loads((p/'inputs.json').read_text()).get('base_inputs',[]) if (p/'inputs.json').exists() else []:
  bb=subprocess.check_output(['git','show',f"{B}:{f['path']}"],cwd=R);base_rows+=1
  if sha(bb)!=f['sha256'] or len(bb)!=f['bytes']:fail.append(['worker-BASE-object',task,f['path']])
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=S).decode().strip();status=subprocess.check_output(['git','status','--porcelain'],cwd=S).decode()
if head!=B or status:fail.append(['source-checkout',head,status])
print(json.dumps({'task':'N45-PG','inputs_verified':len(d['inputs']),'pinned_hashes':sum(f.get('expected_sha256') is not None for f in d['inputs']),'manifest_entries_verified':manifest_rows,'delivery_items_verified':deliveries,'worker_BASE_objects_verified':base_rows,'source_HEAD':head,'source_git_status':status,'failures':fail},indent=2));sys.exit(bool(fail))
