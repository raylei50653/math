from pathlib import Path
import importlib.util,time
p=Path('audits/2026-10-13-c5-no4ct-frontier-6943561/terminals/check.py')
spec=importlib.util.spec_from_file_location('tk',p); tk=importlib.util.module_from_spec(spec); spec.loader.exec_module(tk)

def exterior(kind,pair,side,slot,e):
    ends=('x',) if kind=='PINCH' else ('x','y')
    vi=(pair+4*side)%8; fi=(vi+4)%8
    ve=ends[side if kind=='BRIDGE' else 0]; fe=ends[1-side if kind=='BRIDGE' else 0]
    j=tuple(tk.C[(fi+k)%8] for k in range(5))+(fe,)
    u=tuple(tk.T[(fi+k)%8] for k in range(4))+('zF',)
    vt=tuple(tk.T[(vi+k)%8] for k in range(4)); vc=tuple(tk.C[(vi+k)%8] for k in range(5))
    d=[ve]+list(vt); d.insert(slot+1,'w'); d=tuple(d)
    vf=[(vc[k],vc[k+1],vt[k]) for k in range(4)]
    wedge=[(vc[0],vt[0],ve)]+[(vc[k],vt[k],vt[k-1]) for k in range(1,4)]+[(vc[4],ve,vt[3])]
    for k,(a,b,c) in enumerate(wedge): vf.extend([(a,b,'w'),(a,'w',c)] if k==slot else [(a,b,c)])
    hf=tk.patch_faces(j,u)+vf
    if kind=='BRIDGE': hf += [(tk.C[pair],'x','y'),(tk.C[(pair+4)%8],'y','x')]
    af,names=tk.collar_faces(e); faces=af+hf
    vertices=tk.B+tk.C+tk.T+ends+('w','zF')
    edges=sorted({tk.edge(a,b) for f in faces for a,b in zip(f,f[1:]+f[:1])})
    g=tk.graph_on(vertices,edges); g['faces']=faces; g['D']=d
    sv=tuple(v for v in vertices if v not in u); skeleton=tk.graph_on(sv,[ed for ed in edges if set(ed)<=set(sv)])
    return g,skeleton,j,u,d

if __name__=='__main__':
    for kind in ('PINCH','BRIDGE'):
      g,s,j,u,d=exterior(kind,0,0,2,tk.QUERIES[0][1])
      now=time.time(); full=tk.direct(g,dict(zip(tk.B,map(int,tk.B_ROWS[0])))); print(kind,len(full),time.time()-now,flush=True)
      now=time.time(); sk=tk.direct(s,dict(zip(tk.B,map(int,tk.B_ROWS[0])))); print('skeleton',len(sk),time.time()-now,flush=True)
