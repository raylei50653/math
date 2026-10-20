exec((__import__('pathlib').Path(__file__).parent/'explore_acceptance.py').read_text().split("for name in ('Q1','Q2'):")[0])
rowids=[index[mod.canonical(t)] for t in rows]
forbidden=set(i for e in zeroT for i in T[e].indices)|set(i for i,b in enumerate(bounds[:n]) if b==(0,0))|set(i for i,t in enumerate(ten) if t[4]==t[6])
live=set(range(n))-forbidden
old=None;rounds=[]
while old!=live:
 old=set(live);good=[j for j,col in enumerate(columns) if all(rowids[r] in live for r,v in col)]
 covered=set(r for j in good for r,v in columns[j]);removed=set(rowids[r] for r in range(len(rows)) if rowids[r] in live and r not in covered);live-=removed;rounds.append(sorted(removed));print('live',len(live),'removed',len(removed),flush=True)
print('positive source remaining',{name:sorted(set(ids)&live) for name,ids in mod.source_positive_subsets(index).items()},flush=True)
print('Gsupport',mod.mask(np.array(original['G'])@T@np.array([int(i in live) for i in range(n)])),flush=True)
