import sys,itertools,json,time
from collections import Counter
sys.path.insert(0,'scripts')
import four_color_three_step_kempe_escape as k
import four_color_three_step_cross_split_exclusion as old
E=old.BUFFER19_H_EDGES; faces=[f for f in old.BUFFER19_G_FACES if not set(f)&{0,1}]; opts=[]
for f in faces:
 if len(f)==4:opts.append((None,tuple(sorted((f[0],f[2]))),tuple(sorted((f[1],f[3])))))
 elif len(f)>4:raise AssertionError
base=k.enumerate_normalized(17,E);print('opts',len(opts),'base',len(base),flush=True)
summary=Counter(); stats=[]; start=time.time()
for choice in itertools.product(*opts):
 add=tuple(sorted(e for e in choice if e is not None)); edges=tuple(sorted(set(E)|set(add)))
 states=[f for f in base if all(f[u-2]!=f[v-2] for u,v in add)]
 supp={k.normalize(k.boundary(f)) for f in states};summary['graphs']+=1
 if not k.D16<=supp:summary['missing_d16_support']+=1;continue
 lookup={f:i for i,f in enumerate(states)};adj=k.adjacency(17,edges); actions=[]
 for f in states:
  actions.append([[p,sum(1<<v for v in b),lookup[k.normalize(k.swapped(f,k.PAIRS[p],b))]] for p,bs in enumerate(k.components(f,adj)) for b in bs])
 _,rec=k.distances(actions,states);summary['full_class_checks']+=1
 if len(rec['connected_component_sizes'])>1:summary['disconnected']+=1
 stats.append({'added_edges':add,'states':len(states),'summary':rec})
 if rec['d16_closed_state_orbits']:
  print('FOUND',add,rec,flush=True);open('scratch/2026-10-30-d16-closed-class/augment-found.json','w').write(json.dumps({'edges':edges,'states':states,'actions':actions,'summary':rec}));break
 if summary['full_class_checks']%10==0:print(summary,'seconds',round(time.time()-start,1),flush=True)
print('FINAL',summary,'seconds',time.time()-start,flush=True)
open('scratch/2026-10-30-d16-closed-class/augment-results.json','w').write(json.dumps({'summary':dict(summary),'cases':stats},indent=2))
