#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,hashlib
base=Path(__file__).resolve().parent
root=base.parents[3]
commands=[
 ["git","rev-parse","HEAD"],
 ["git","status","--porcelain"],
 ["sed","-n","1,125p","docs/c5_excess_two_nonadjacent_unit_core45.md"],
 ["sed","-n","410,630p","docs/c5_excess_two_nonadjacent_unit_core45.md"],
 ["cat","audits/2026-10-11-br-sd-1g-dbdc4c35/PROOF.md"],
 ["cat","audits/2026-10-11-br-sd-1g-dbdc4c35/MAPPING.md"],
 ["cat","audits/2026-10-11-br-sd-1c-fd6e1112/PROOF.md"],
 ["cat","audits/2026-10-11-br-sd-1e-337d018b/PROOF.md"],
 ["sed","-n","70,130p","docs/c5_degree5_guide.md"],
 ["sed","-n","270,325p","docs/c5_degree5_interfaces.md"],
 ["sed","-n","145,182p","docs/c5_kempe_guide.md"],
 ["rg","-n","BR-SD-1g|BR-SD-1e|N45-S-NOU-LS-PAIR","docs/STATUS.md","docs/HANDOFF.md"],
 ["git","diff","--check"]
]
records=[]
for i,argv in enumerate(commands,1):
 r=subprocess.run(argv,cwd=root,capture_output=True)
 stem=f"read-{i:02d}"
 (base/(stem+".stdout")).write_bytes(r.stdout)
 (base/(stem+".stderr")).write_bytes(r.stderr)
 records.append({"argv":argv,"cwd":str(root),"exit_code":r.returncode,"stdout":stem+".stdout","stderr":stem+".stderr","stdout_sha256":hashlib.sha256(r.stdout).hexdigest(),"stderr_sha256":hashlib.sha256(r.stderr).hexdigest()})
(base/'READS.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+"\n")
print(json.dumps([{"argv":x["argv"],"exit_code":x["exit_code"]} for x in records],ensure_ascii=False))
