exec((__import__('pathlib').Path(__file__).parent/'explore_acceptance.py').read_text().split("for name in ('Q1','Q2'):")[0])
ids=[i for i,t in enumerate(ten) if t[4]==t[6]]
E=csr_matrix(([1]*len(ids),(range(len(ids)),ids)),shape=(len(ids),n))
eq2=vstack([eq,hstack([E,csr_matrix((len(ids),k+m))])]).tocsr()
ans=linprog(np.zeros(n+k+m),A_eq=eq2,b_eq=np.zeros(eq2.shape[0]),A_ub=ub,b_ub=-np.ones(len(pos)),bounds=bounds)
print('c_degree4_qs_edge',ans.success,ans.message,flush=True)
