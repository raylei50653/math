import importlib.util,json,gzip
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('audit',HERE/'check.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
m=a.load(a.MODEL,'m');z=json.loads(gzip.decompress((HERE/'certificate.json.gz').read_bytes()));K=m.kempe(10,[tuple(t) for t in z['core_states']]);cl=a.Closure(K,len(z['core_states']))
C=z['original_matrix'];Hs=z['H_matrices'];Ss=z['S_matrices']
for jr in [z['general_c5']]+[r for r in z['old_joint_comparisons'] if r['not_excluded']]:
 zb=jr.get('zero_bits',-1);live=jr['live'];poss=[r['possible_catalogue_supports'] for r in z['seven_graph_comparisons']] if zb<0 else next(t['individual_S_support_options'] for t in z['seven_vs_eight_tests'] if t['zero_bits']==zb)
 unions=[__import__('functools').reduce(int.__or__,ss) for ss in poss]
 seed=[i for i in live if all(not Ss[j][r][i] for j,u in enumerate(unions) for r in range(10) if not u>>r&1)]
 ll,rs=cl.close(seed)
 print(zb,len(live),len(seed),len(ll),'C',a.projection(C,ll),'newzeros',[(j,jr['S_uppers'][j]&~u) for j,u in enumerate(unions) if jr['S_uppers'][j]&~u],flush=True)
