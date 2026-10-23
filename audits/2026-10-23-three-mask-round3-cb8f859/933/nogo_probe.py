exec((__import__('pathlib').Path(__file__).parent/'probe.py').read_text().split('for j,ds in enumerate(trs):')[0])
for j,ds in enumerate(trs):
 M=[[0]*274 for _ in o.ROWS]
 for r,word in enumerate(o.ROWS):
  x,y,a,b,c=map(int,word)
  for n,R,L,q in itertools.product(range(4),repeat=4):
   colors=dict(zip(E,(a,n,R,L,q,c,x,y)),b=b)
   if all(colors[u]!=colors[v] for u,v in base+list(ds)):M[r][index[o.canonical(tuple(colors[v] for v in E))]]+=1
 active=[k for k,c in enumerate(M[6]) if c and any(B[k])];witness=None
 for size in (1,2,3):
  for js in itertools.combinations_with_replacement(active,size):
   if all(x==sum(B[k][i] for k in js) for i,x in enumerate(B[30])):witness=js;break
  if witness:break
 print(j,'active',active,'witness',witness,'dim/signs',[(len(S[0]) if S else 0,len(st)) for S,st,z in [o.close_zeros(B,active)]])
