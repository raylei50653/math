exec((__import__('pathlib').Path(__file__).parent/'probe.py').read_text().split('for j,ds in enumerate(trs):')[0])
import ast,time
algorithm=(ROOT/'audits/2026-10-18-smaller-bad-e1617a2/kempe_consistency.py').read_text();tree=ast.parse(algorithm);option_ast=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='options'],type_ignores=[]);ns={'NONCROSSING':ps,'INDEX':index,'canonical':o.canonical};exec(compile(option_ast,'frozen-original-options','exec'),ns)
OPTIONS=[[ns['options'](t,split) for split in src['palette_splits']] for t in ts]
for j,ds in enumerate(trs[:2]):
 M=[[0]*274 for _ in o.ROWS]
 for r,word in enumerate(o.ROWS):
  x,y,a,b,c=map(int,word)
  for n,R,L,q in itertools.product(range(4),repeat=4):
   colors=dict(zip(E,(a,n,R,L,q,c,x,y)),b=b)
   if all(colors[u]!=colors[v] for u,v in base+list(ds)):M[r][index[o.canonical(tuple(colors[v] for v in E))]]+=1
 zeros={k for k in range(274) if any(M[i][k] for i in (1,4,6))};rounds=[]
 while True:
  S,steps,known=o.close_zeros(B,zeros);zeros=set(known)|({k for k,r in enumerate(S) if not any(r)} if S else set(range(274)));remove=[]
  for k in sorted(set(range(274))-zeros):
   for split,choices in enumerate(OPTIONS[k]):
    if not any(not set(orbit)&zeros for orbit,_ in choices):remove.append((k,split));break
  rounds.append({'dim':len(S[0]) if S else 0,'zeros':len(zeros),'remove':remove});print(j,rounds[-1],flush=True)
  if not remove:break
  zeros|={k for k,_ in remove}
 print('source',o.mm(o.local_relations(ts)[0]['G'],S) if S else 'empty','candidatealpha',o.mm([M[9]],S),flush=True)
 rr,piv=o.rref(list(map(list,zip(*S))));T=list(map(list,zip(*rr[:len(piv)])));print('piv',piv,'neg rows',sum(any(x<0 for x in row) for row in T),'alpha active',[k for k,v in enumerate(M[9]) if v and k not in zeros],flush=True)
 with (P/('closure-'+str(j)+'.json')).open('x') as f:json.dump({'rounds':rounds,'live':sorted(set(range(274))-zeros),'pivot':piv,'T':[[str(x) for x in r] for r in T]},f,indent=2)
