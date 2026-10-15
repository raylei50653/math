from pathlib import Path
import json,time
H=Path(__file__).resolve().parent
exec((H/'probe_covers.py').read_text().split('for v in [0,Q[0],Q[1]]:')[0])
out=[];start=time.time()
for mask in range(1<<len(Q)):
 v=0
 for i,q in enumerate(Q):
  if mask>>i&1:v^=q
 r=run(v);r['class']=mask;out.append(r)
 if mask%32==0:print(mask,'elapsed',round(time.time()-start,1),'survivors',sum(x['q_reached'] for x in out),flush=True)
(H/'probe-all-covers.json').write_text(json.dumps(out,indent=2)+'\n')
print('DONE',len(out),'seconds',time.time()-start,'survivors',sum(x['q_reached'] for x in out),flush=True)
