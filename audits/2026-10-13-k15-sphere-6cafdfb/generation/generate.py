#!/usr/bin/env python3
"""Two complete plantri entrypoints; no source pruning. Exclusive outputs."""
import hashlib,json,subprocess,tempfile,time
from pathlib import Path
HERE=Path(__file__).resolve().parent.parent
base=json.loads((HERE/'BASE.json').read_text())
for name,digest in base['sha256'].items():
 assert hashlib.sha256((HERE/'frozen'/name).read_bytes()).hexdigest()==digest,name
source=HERE/'frozen/artifacts/c5_excess_two_independent_search/vendor/plantri.c'
plugin=HERE/'frozen/audits/2026-10-13-k13-collar-50d5474/generation'
receipts=[]
with tempfile.TemporaryDirectory(prefix='math-k15-generate-') as temp:
 for label,flags,mode,target in [('min5',[],'-m5','spheres21.pc'),('min4',['-I'+str(plugin),'-DPLUGIN=min5_filter.c'],'-m4','spheres21_from_min4.pc')]:
  binary=Path(temp)/label; output=Path(temp)/target
  compile_cmd=['cc','-O3',*flags,str(source),'-o',str(binary)]
  subprocess.run(compile_cmd,check=True)
  command=[str(binary),mode,'21',str(output)]
  t=time.monotonic(); result=subprocess.run(command,capture_output=True,check=True)
  data=output.read_bytes()
  with (HERE/'generation'/target).open('xb') as stream: stream.write(data)
  receipt=dict(label=label,compile=compile_cmd,command=command,elapsed=time.monotonic()-t,stdout=result.stdout.decode(),stderr=result.stderr.decode(),sha256=hashlib.sha256(data).hexdigest())
  receipts.append(receipt); print(json.dumps(receipt),flush=True)
with (HERE/'generation/receipt.json').open('x') as stream:json.dump(receipts,stream,indent=2);stream.write('\n')
