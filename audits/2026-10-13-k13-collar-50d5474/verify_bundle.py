#!/usr/bin/env python3
"""Seal and verify this exact local delivery; no mathematical recomputation."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='50d5474f2446403f3b3001d5943571184c8c9936'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def manifest():
    selected={}
    for p in sorted(HERE.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts or p.name in ('SEAL.json','plantri','plantri_min4_filter'):
            continue
        selected[str(p.relative_to(ROOT))]={'sha256':sha(p),'bytes':p.stat().st_size}
    extra=['.gitignore','audits/ARCHIVE.json','audits/README.md','docs/STATUS.md','docs/c5_c8_apex_degree.md','docs/c5_cofacial_normal_form.md','docs/c5_kempe_guide.md','docs/c5_k13_collar.md','docs/c5_neartri_boundary_collar.md','docs/c5_saturation_degree_bound.md']
    old=json.loads(subprocess.check_output(['git','show',BASE+':audits/ARCHIVE.json'],cwd=ROOT))
    current=json.loads((ROOT/'audits/ARCHIVE.json').read_text())
    extra += [r['path'] for k,r in current['blobs'].items() if k not in old['blobs']]
    for rel in extra:
        p=ROOT/rel;selected[rel]={'sha256':sha(p),'bytes':p.stat().st_size}
    return {'base':BASE,'files':selected,'scope':'exact isolated local delivery; excludes only caches and reproducible executables'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');a=ap.parse_args()
    assert a.write!=a.check
    obj=manifest();data=(json.dumps(obj,sort_keys=True,indent=2)+'\n').encode();p=HERE/'SEAL.json'
    if a.write:
        with p.open('xb') as f:f.write(data)
    else:assert p.read_bytes()==data,'delivery seal mismatch'
    print(json.dumps({'seal':'pass','files':len(obj['files']),'bytes':sum(v['bytes'] for v in obj['files'].values()),'mode':'write' if a.write else 'check'}))
