exec((__import__('pathlib').Path(__file__).parent/'probe.py').read_text().split('for j,ds in enumerate(trs):')[0])
Ms=[]
for ds in trs[:2]:
 M=[[0]*274 for _ in o.ROWS]
 for r,word in enumerate(o.ROWS):
  x,y,a,b,c=map(int,word)
  for n,R,L,q in itertools.product(range(4),repeat=4):
   colors=dict(zip(E,(a,n,R,L,q,c,x,y)),b=b)
   if all(colors[u]!=colors[v] for u,v in base+list(ds)):M[r][index[o.canonical(tuple(colors[v] for v in E))]]+=1
 Ms.append(M)
 for ri in range(10):
  terms=[[k,c] for k,c in enumerate(M[ri]) if c and any(B[k])];v=o.mm([M[ri]],B)[0]
  single=[(k,c) for k,row in enumerate(B) if any(row) for c in (1,2,3,4,8) if all(x==c*y for x,y in zip(v,row))]
  print('candidate',len(Ms)-1,'row',o.ROWS[ri],'terms',terms,'single',single)
for ri in (1,4,6):print('same row',o.ROWS[ri],not any(o.mm([[a-b for a,b in zip(Ms[0][ri],Ms[1][ri])]],B)[0]))
S,steps,zeros=o.close_zeros(B,{k for k in range(274) if any(Ms[0][i][k] for i in (1,4,6))});print('zeros new',[i for i in zeros if any(B[i])],'steps',steps)
for target in (75,77,257,259):
 print(target,ts[target],'times-source?',[(c,not any(o.mm([[a-c*b for a,b in zip(o.local_relations(ts)[0]['G'][9],[int(k==target) for k in range(274)])]],S)[0])) for c in (1,2,4,8)])
vars=[73,76,257,259]
for target in (20,30,52,54,75,77,131,257,259):
 found=[]
 for cs in itertools.product(range(-2,3),repeat=4):
  if all(x==sum(c*B[k][i] for k,c in zip(vars,cs)) for i,x in enumerate(B[target])):found.append(cs)
 print('id',target,'relations',found)
for t,M in enumerate(Ms):
 v=o.mm([M[9]],B)[0]
 found=[]
 for cs in itertools.product(range(-4,5),repeat=4):
  if all(x==sum(c*B[k][i] for k,c in zip(vars,cs)) for i,x in enumerate(v)):found.append(cs)
 print('candidatealpha',t,'relations',found)
for t,M in enumerate(Ms):
 R=o.mm(M,S)
 print('slice',t,'identicallyzero',[o.ROWS[i] for i,row in enumerate(R) if not any(row)],'rowalpha',R[9])
 for i,row in enumerate(R):
  print('diffalpha',i,[(c,not any(a-c*b for a,b in zip(row,R[9]))) for c in (1,2,4)])
