import hashlib,json
from pathlib import Path
p=Path('audits/2026-10-20-r6-941-j1-c11-1148ce0')
inputs=json.loads((p/'INPUTS.json').read_text())
outputs=json.loads((p/'OUTPUTS.json').read_text())
checks=json.loads((p/'checks.json').read_text())
def verify(rows,base):
 for row in rows:
  raw=(base/row['path']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
  assert len(raw)==row['bytes'],row['path']
verify(inputs,p/'frozen');verify(outputs,p)
receipts=checks['receipts'][:]
for run in checks['runs']:
 receipts.extend([run['stdout'],run['stderr']])
receipts.append(checks['lake_build']['receipt'])
verify(receipts,p)
files=[q for q in p.rglob('*') if q.is_file()]
core=[q for q in files if 'frozen' not in q.relative_to(p).parts]
sealed={q['path'] for q in outputs}
def rec(q):
 raw=q.read_bytes()
 return {'path':str(q.relative_to(p)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
print(json.dumps({'status':'PASS frozen inputs, sealed outputs, and original validation receipts','frozen_input_count':len(inputs),'sealed_output_count':len(outputs),'original_validation_receipts_checked':len(receipts),'total_files':len(files),'total_bytes':sum(q.stat().st_size for q in files),'non_frozen_files':len(core),'non_frozen_bytes':sum(q.stat().st_size for q in core),'largest_non_frozen':[rec(q) for q in sorted(core,key=lambda q:q.stat().st_size,reverse=True)[:8]],'unsealed_non_frozen':[rec(q) for q in core if str(q.relative_to(p)) not in sealed]},indent=2))
