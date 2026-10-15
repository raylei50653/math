import hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6ddea32a81349821ad3724ae1652bddb9c6a7b04'
files=['docs/HANDOFF.md','docs/STATUS.md','audits/2026-10-15-route-research-6ddea32/REPORT.md','audits/2026-10-15-r6-seven-pin-6ddea32/REPORT.md','audits/2026-10-15-r6-seven-pin-6ddea32/PROOF.md','audits/2026-10-15-r6-seven-pin-6ddea32/check.py','audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/check_transfer.py','audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md','audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/counts.json','audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/REPORT.md','audits/2026-10-14-cofacial-fibres-676b102/r6/PROOF.md','audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md']
records=[]
for name in files:
 data=(ROOT/name).read_bytes();dest=HERE/'frozen'/name;dest.parent.mkdir(parents=True,exist_ok=True)
 with dest.open('xb') as f:f.write(data)
 tracked=subprocess.run(['git','cat-file','-e',BASE+':'+name],cwd=ROOT,capture_output=True).returncode==0
 if tracked:
  assert subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)==data
 records.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),'provenance':'BASE tracked' if tracked else 'first-round uncommitted frozen input'})
with (HERE/'INPUTS.json').open('x') as f:json.dump({'BASE':BASE,'authority':'isolated audit only; no commit/push; tracked inputs from BASE, first-round outputs frozen as working-tree inputs','inputs':records},f,indent=2);f.write('\n')
