"""Necessary rectangular-support closure, no rectangle search needed."""
import json
from pathlib import Path
from collections import Counter
from twohole_fast import prune_mask
from twohole_probe import bits

def closure(M,tau):
 R=[sum(1<<b for b in range(31) if not M[a][b]&~tau) for a in range(31)]
 initial=R[:];rounds=[]
 while True:
  old=R[:]
  R=[prune_mask(x) for x in R]
  cols=[sum(1<<a for a in range(31) if R[a]&(1<<b)) for b in range(31)]
  cols=[prune_mask(x) for x in cols]
  R=[sum(1<<b for b in range(31) if cols[b]&(1<<a)) for a in range(31)]
  rounds.append(R[:])
  if R==old:break
 possible=0
 for a in range(31):
  for b in bits(R[a]):possible|=M[a][b]
 return dict(initial=initial,rounds=rounds,final=R,possible=possible,missing=tau & ~possible,excluded=possible!=tau)

def run():
 records=[]
 for p in sorted(Path(__file__).parent.glob('twohole_*.json')):
  for r in json.loads(p.read_text())['records']:
   v=closure(r['matrix'],r['target'])
   res={k:r[k] for k in ('kind','pair','query','target','collar','vertices','edges','interfaces','matrix','shell_lift_counts')}
   res.update(v);records.append(res)
   if not v['excluded']:print('RESIDUAL',r['kind'],r['pair'],r['query'],v['possible'])
 Path(__file__).with_name('pair_prune_results.json').write_text(json.dumps({'records':records},indent=2))
 print('summary',Counter((r['kind'],r['excluded']) for r in records))
 print('round counts',Counter(len(r['rounds']) for r in records))
 print('final pairs',Counter(sum(v.bit_count() for v in r['final']) for r in records))
 print('possible masks',Counter(r['possible'] for r in records))
if __name__=='__main__':run()
