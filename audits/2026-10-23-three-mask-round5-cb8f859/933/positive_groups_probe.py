exec((__import__('pathlib').Path(__file__).parent/'Aonly_probe.py').read_text().split("for row in ('01012','01202'):")[0])
results=[]
for row in ('01021','01201'):
 A,s,v,w,t=map(int,row);targets=set()
 for n,L,q in itertools.product(range(4),repeat=3):
  d=(A,n,A,L,q,A,s,v,w,t)
  if all(d[i]!=d[(i+1)%10] for i in range(10)):targets.add(di[m.canonical(d)])
 eliminated=[];survivors=[]
 for j in sorted(targets):
  counts=[]
  for split in (((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))):
   m.SPLIT=split;opts=m.options(D[j],nc);surv=[o for o in opts if not any(di[m.canonical(word)] in bad for _,word in o['complete_literal_subset_lifts'])];counts.append([len(opts),len(surv)])
  (eliminated if any(n==0 for _,n in counts) else survivors).append(j)
  results.append({'row':row,'D_id':j,'word':D[j],'option_counts':counts})
 print(row,'targets',len(targets),'eliminated',eliminated,'survivors',survivors,flush=True)
with (P/'positive-groups-probe.json').open('x') as f:json.dump({'results':results,'necessary_feasibility_claimed':False},f,indent=2)
