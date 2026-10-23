from pathlib import Path
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2];base='cb8f8593e273a7426ecadd59797a6e643cc4768e'
paths=['audits/2026-10-23-three-mask-round4-cb8f859/933/'+n for n in ('REPORT.md','PROOF.md','check.py','certificate.json','INPUTS.json','VERIFICATION.json','independent.py','independent-certificate.json')]+['audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json','audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json','audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md','audits/2026-10-18-smaller-bad-e1617a2/B/PROOF.md','audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md']
ledger=json.loads((P.parent/'BASE.json').read_text());entries={e['path']:e for e in ledger['predecessors']};files=[]
for path in paths:
 d=(R/path).read_bytes();e={'path':path,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
 if path in entries:assert e==entries[path]
 else:assert subprocess.check_output(['git','show',base+':'+path],cwd=R)==d
 f=P/'frozen'/path;f.parent.mkdir(parents=True,exist_ok=True)
 with f.open('xb') as h:h.write(d)
 files.append(e)
routing=[]
for path in ('docs/HANDOFF.md','docs/STATUS.md','docs/c5_kempe_guide.md'):
 d=(R/path).read_bytes();routing.append({'path':path,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'authority':'routing only; drift permitted'})
with (P/'INPUTS.json').open('x') as f:json.dump({'base':base,'files':files,'routing':routing,'write_boundary':str(P.relative_to(R)),'source':'one complete original globally minimum r6/933 source'},f,indent=2);f.write('\n')
