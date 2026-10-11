"""Read-only SHA256 snapshots of authority, prior deliveries and tracked state."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
PROTECTED=[
    '2026-10-10-n45-s-long-contract','2026-10-11-n45-s-long-s-direct',
    '2026-10-11-n45-s-long-s-fibre','2026-10-11-n45-s-long-s-joint',
    '2026-10-11-n45-s-long-s-joint-review','2026-10-11-n45-s-long-s-review',
    '2026-10-11-n45-s-long-s-rfibre-dispatch'
]

def snapshot():
    files={}
    for name in PROTECTED:
        folder=ROOT/'audits'/name
        for p in sorted(folder.rglob('*')):
            if p.is_file():
                assert not p.is_symlink(),str(p)
                files[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted((HERE/'authority').rglob('*')):
        if p.is_file():
            files[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    for name in ['cases.json','inputs.json','certificate.json']:
        p=HERE/name
        if p.exists():
            files[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    return {'files':files,'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'tracked_diff_sha256':hashlib.sha256(subprocess.check_output(['git','diff','HEAD','--binary'],cwd=ROOT)).hexdigest()}

def main():
    current=snapshot()
    if len(sys.argv)>1:
        old=json.loads(Path(sys.argv[1]).read_text())
        changed=[p for p,h in old['files'].items() if current['files'].get(p)!=h]
        added=[p for p in current['files'] if p not in old['files']]
        result={'protected_files':len(old['files']),'changed':changed,'added':added,
                'head_equal':current['head']==old['head'],'tracked_diff_equal':current['tracked_diff_sha256']==old['tracked_diff_sha256']}
        result['status']='passes' if not changed and result['head_equal'] and result['tracked_diff_equal'] else 'fails'
        print(json.dumps(result,sort_keys=True)); return 0 if result['status']=='passes' else 1
    print(json.dumps(current,sort_keys=True,indent=2)); return 0

if __name__=='__main__':
    raise SystemExit(main())
