from pathlib import Path
from hashlib import sha256
import json

root=Path(__file__).resolve().parents[2]
results=[]
errors=[]
for name in ['audits/2026-10-14-c4-mask13-joint6-fdd3e22','audits/2026-10-14-c4-c5-recursion-fdd3e22']:
 package=root/name
 manifest=json.loads((package/'MANIFEST.json').read_text())
 mismatch=[]
 for row in manifest['files']:
  path=package/row['path']
  if not path.is_file():
   mismatch.append({'path':row['path'],'error':'missing'});continue
  data=path.read_bytes()
  if len(data)!=row['bytes'] or sha256(data).hexdigest()!=row['sha256']:
   mismatch.append({'path':row['path'],'error':'manifest SHA/size mismatch'})
 inputs=json.loads((package/'INPUTS.json').read_text())
 frozen_mismatch=[]
 live_drift=[]
 for row in inputs['files']:
  path=package/'frozen'/row['path']
  if not path.is_file() or sha256(path.read_bytes()).hexdigest()!=row['sha256']:
   frozen_mismatch.append(row['path'])
  live=root/row['path']
  if not live.is_file() or sha256(live.read_bytes()).hexdigest()!=row['sha256']:
   live_drift.append(row['path'])
 generated=[p for p in package.rglob('*') if p.is_file() and not p.is_symlink() and p.suffix.lower() in {'.json','.jsonl','.ndjson','.json5','.bin'}]
 large=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size} for p in sorted(generated) if p.stat().st_size>=1_000_000]
 result={'audit':name,'seal_present':(package/'SEAL.json').exists(),'manifest_files':len(manifest['files']),'manifest_mismatches':mismatch,'frozen_inputs':len(inputs['files']),'frozen_input_mismatches':frozen_mismatch,'current_live_drift':live_drift,'generated_threshold_bytes':1_000_000,'large_generated_files':large,'largest_generated_files':[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size} for p in sorted(generated,key=lambda p:p.stat().st_size,reverse=True)[:5]]}
 results.append(result)
 if mismatch or frozen_mismatch:
  errors.append(name)
payload={'status':'FAIL' if errors else 'PASS','results':results}
print(json.dumps(payload,ensure_ascii=False,indent=2))
assert not errors,errors
