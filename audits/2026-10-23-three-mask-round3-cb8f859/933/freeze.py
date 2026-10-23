from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[2]
paths=['audits/2026-10-23-three-mask-methods-cb8f859/933/'+n for n in ('REPORT.md','check.py','certificate.json','INPUTS.json')]+['audits/2026-10-23-three-mask-round2-cb8f859/933/'+n for n in ('REPORT.md','PROOF.md','check.py','certificate-v2.json','INPUTS.json')]+['audits/2026-10-18-smaller-bad-e1617a2/B/PROOF.md','audits/2026-10-18-smaller-bad-e1617a2/kempe_consistency.py','audits/2026-10-18-smaller-bad-counts-e1617a2/C/PROOF.md','audits/2026-10-18-smaller-bad-counts-e1617a2/C/certificate.json','audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json','audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json']
files=[]
for path in paths:
 d=(R/path).read_bytes();f=P/'frozen'/path;f.parent.mkdir(parents=True,exist_ok=True)
 with f.open('xb') as h:h.write(d)
 files.append({'path':path,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()})
routing=[]
for path in ('docs/HANDOFF.md','docs/STATUS.md','docs/c5_kempe_guide.md'):
 d=(R/path).read_bytes();routing.append({'path':path,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'authority':'routing only; drift permitted'})
manifest={'base':'cb8f8593e273a7426ecadd59797a6e643cc4768e','files':files,'routing':routing,'write_boundary':str(P.relative_to(R)),'immutable_predecessors':True,'source_scope':'complete original r6 two-star source, literal full support 933'}
with (P/'INPUTS.json').open('x') as h:json.dump(manifest,h,indent=2);h.write('\n')
