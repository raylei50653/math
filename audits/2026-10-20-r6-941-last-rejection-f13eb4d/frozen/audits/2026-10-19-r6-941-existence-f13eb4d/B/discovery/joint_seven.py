exec(open(__file__.replace('joint_seven.py','seven.py')).read().split('poly=')[0])
z=json.load(open(HERE/'discovery/seven-results.json'));mats=z['matrices'];recs=z['compatible']
for rec in cert['joint_comparisons']:
 if not rec['not_excluded_by_zero_closure']:continue
 lives=rec['live'];possall=[]
 for j,N in enumerate(mats):
  poss=[]
  for support,_ in recs[j]:
   ll,rs=close([i for i in lives if all(not N[r][i] for r in range(10) if not support>>r&1)])
   if proj(C,ll)!=941:continue
   if support&~proj(N,ll):continue
   if any(s&~proj(n,ll) for s,n in zip(rec['exact_supports_hypothesis'],cert['candidate_matrices'])):continue
   poss.append(support)
  possall.append(poss)
 print('TYPE',rec['zero_bits'],possall,flush=True)
