exec((__import__('pathlib').Path(__file__).parent/'Aonly_probe.py').read_text().split("for row in ('01012','01202'):")[0])
targets=set()
for row in ('01012','01202'):
 A,s,v,w,t=map(int,row)
 for n,L,q in itertools.product(range(4),repeat=3):
  d=(A,n,A,L,q,A,s,v,w,t)
  if all(d[i]!=d[(i+1)%10] for i in range(10)):
   j=di[m.canonical(d)]
   if j not in bad:targets.add(j)
allopts={}
for j in targets:
 allopts[j]=[]
 for split in (((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))):
  m.SPLIT=split;allopts[j].append([{di[m.canonical(word)] for _,word in o['complete_literal_subset_lifts']} for o in m.options(D[j],nc)])
rounds=[]
while True:
 removed=[]
 for j in targets-zeros:
  if any(all(orbit&zeros for orbit in opts) for opts in allopts[j]):removed.append(j)
 print('remove',sorted(removed),flush=True);rounds.append(sorted(removed))
 if not removed:break
 zeros.update(removed)
print('remain',sorted(targets-zeros))
with (P/'Aonly-closure.json').open('x') as f:json.dump({'rounds':rounds,'remaining':sorted(targets-zeros),'necessary_feasibility_claimed':False},f,indent=2)
