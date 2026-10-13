from prototype import *
from itertools import product
import gzip,json,collections
with gzip.open('audits/2026-10-13-c5-no4ct-frontier-6943561/terminals/full_lifts.v2.json.gz','rt') as f: kernel=json.load(f)['kernel']['complete_literal_fibres']
proper=sorted({tk.canonical(''.join(row)) for row in product('0123',repeat=6) if all(row[i]!=row[(i+1)%6] for i in range(6))})
records=[]
for kind in ('PINCH','BRIDGE'):
 for pair in range(4):
  for side in range(2):
   for slot in range(5):
    cache={}
    for query,e,target in tk.QUERIES:
     if e not in cache:
      g,s,j,u,d=exterior(kind,pair,side,slot,e)
      masks=dict.fromkeys(proper,0)
      for bi,row in enumerate(tk.B_ROWS):
       for lift in tk.direct(s,dict(zip(tk.B,map(int,row)))):
        a=dict(zip(s['vertices'],lift)); jr=''.join(a[v] for v in j)
        if kernel[jr]: masks[tk.canonical(''.join(a[v] for v in d))]|=1<<bi
      cache[e]=masks
     masks=cache[e]
     allowed={q:mask for q,mask in masks.items() if not mask & (1023^target)}
     possible=0
     for mask in allowed.values(): possible|=mask
     records.append(dict(name=f'{kind}-{pair}-{side}-{slot}-{query}',allowed=allowed,possible=possible,target=target))
    print(kind,pair,side,slot, 'allowed',collections.Counter(len(x['allowed']) for x in records[-8:]),'possible',collections.Counter(x['possible'] for x in records[-8:]),flush=True)
Path('audits/2026-10-13-c8-terminal-s1-d521163/transfer/exploration.json').write_text(json.dumps(dict(proper=proper,records=records),indent=2))
