from models import reconstruct
from collections import Counter
import json
from pathlib import Path
result=reconstruct()
with Path(__file__).with_name('explore-trace.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print('rows',len(result['rows']),'preomega',len(result['preomega']))
print(Counter(r['omega_type'] for r in result['preomega']))
for kind in ['N1','N3']:
 print(kind,{k:sum(r['stage_counts'][k] for r in result['contexts'] if r['omega_type']==kind) for k in ['initial_valid','n','v','a','b','omega']})
