from pathlib import Path
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
paths=['audits/2026-10-23-three-mask-round3-cb8f859/933/'+n for n in ('REPORT.md','PROOF.md','check.py','certificate.json','INPUTS.json','VERIFICATION.json','independent.py','independent-certificate.json')]+['audits/2026-10-18-smaller-bad-e1617a2/B/PROOF.md','audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md','audits/2026-10-17-r6-active-f-seven-ffea555/B/PROOF.md','audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md','audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json']
base='cb8f8593e273a7426ecadd59797a6e643cc4768e';ledger=json.loads((P.parent/'BASE.json').read_text());inherited={e['path']:e for e in ledger['predecessors']};files=[]
for path in paths:
 d=(R/path).read_bytes();e={'path':path,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
 if path in inherited:assert e==inherited[path]
 else:assert subprocess.check_output(['git','show',base+':'+path],cwd=R)==d
 f=P/'frozen'/path;f.parent.mkdir(parents=True,exist_ok=True)
 with f.open('xb') as h:h.write(d)
 files.append(e)
routing=[]
for path in ('docs/HANDOFF.md','docs/STATUS.md','docs/c5_kempe_guide.md'):
 d=(R/path).read_bytes();routing.append({'path':path,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'authority':'routing only; drift permitted'})
with (P/'INPUTS.json').open('x') as h:json.dump({'base':base,'files':files,'routing':routing,'write_boundary':str(P.relative_to(R)),'source':'same complete original globally minimum r6/933 source'},h,indent=2);h.write('\n')
