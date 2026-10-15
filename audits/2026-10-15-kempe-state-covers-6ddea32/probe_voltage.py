from pathlib import Path
import json,itertools
H=Path(__file__).resolve().parent;S=[s for s in json.load(open(H/'frozen/audits/2026-10-15-kempe-compatibility-6ddea32/certificate.json'))['states'] if s['layer']==0];byid={s['id']:s for s in S};byrow={s['literal_row']:s['id'] for s in S}
P=list(itertools.permutations(range(4)))
def rename(s,p):return ''.join('ABCD'[p['ABCD'.index(c)]] for c in s)
def edgekey(a,b):
 ra,rb=byid[a]['literal_row'],byid[b]['literal_row']
 return min(tuple(sorted((rename(ra,p),rename(rb,p)))) for p in P)
keys=set();edges={}
for s in S:
 for j,part in enumerate(s['pairings']):
  for b in range(sum(map(len,part['terminal_parts']))):
   target=part['cube_targets_by_bitmask'][1<<b];key=edgekey(s['id'],target);keys.add(key);edges[s['id'],j,b]=key
keys=sorted(keys);index={k:i for i,k in enumerate(keys)};rows=set()
for s in S:
 for j,part in enumerate(s['pairings']):
  for a,b in itertools.combinations(range(sum(map(len,part['terminal_parts']))),2):
   x,y=part['cube_targets_by_bitmask'][1<<a],part['cube_targets_by_bitmask'][1<<b]
   ks=[edges[s['id'],j,a],edges[s['id'],j,b],edges[x,j,b],edges[y,j,a]];mask=0
   for k in ks:mask^=1<<index[k]
   rows.add(mask)
basis={}
for mask in sorted(rows):
 while mask:
  p=mask.bit_length()-1
  if p in basis:mask^=basis[p]
  else:basis[p]=mask;break
print('edge orbit vars',len(keys),'square eq',len(rows),'rank',len(basis),'dim',len(keys)-len(basis))
(H/'probe-voltage.json').write_text(json.dumps({'keys':keys,'rows':sorted(rows),'basis':basis}))
