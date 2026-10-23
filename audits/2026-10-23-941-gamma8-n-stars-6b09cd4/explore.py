from models import reconstruct
from collections import Counter
import json
from pathlib import Path
rows=reconstruct()['rows']
p=Path(__file__).with_name('explore.json')
with p.open('x') as f:json.dump(rows,f,indent=2,sort_keys=True);f.write('\n')
print(len(rows),Counter(r['omega_type'] for r in rows),Counter((r['omega_type'],r['d_equals_U'],r['m_side']) for r in rows))
