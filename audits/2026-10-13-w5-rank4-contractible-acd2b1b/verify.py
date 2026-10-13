#!/usr/bin/env python3
"""Read-only frozen BASE, local seal, and original-evidence verification."""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
def sha(raw): return hashlib.sha256(raw).hexdigest()
def main():
    base=json.loads((ROOT/'BASE.json').read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==base['base']
    for rec in base['inputs']:
        stored=(ROOT/rec['stored']).read_bytes()
        assert sha(stored)==rec['stored_sha256'],rec['path']
        raw=gzip.decompress(stored) if rec['stored'].endswith('.gz') else stored
        assert len(raw)==rec['bytes'] and sha(raw)==rec['sha256'],rec['path']
        assert raw==subprocess.check_output(['git','show',base['base']+':'+rec['path']],cwd=REPO),rec['path']
    seal=json.loads((ROOT/'DELIVERY.json').read_text())
    exclusions=set(seal['excluded_postseal_receipts'])|{'DELIVERY.json'}
    actual={str(p.relative_to(REPO)) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and str(p.relative_to(ROOT)) not in exclusions}
    assert actual=={r['path'] for r in seal['files']}, 'unsealed file drift'
    for rec in seal['files']:
        raw=(REPO/rec['path']).read_bytes()
        assert len(raw)==rec['bytes'] and sha(raw)==rec['sha256'],rec['path']
        if rec['path'].endswith('.gz'):
            with gzip.open(REPO/rec['path'],'rb') as f:
                for _ in iter(lambda:f.read(1<<20),b''):pass
    assert not subprocess.check_output(['git','diff','--name-only',base['base'],'--','audits','artifacts/MANIFEST.json','.gitignore'],cwd=REPO)
    assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=REPO)
    print(json.dumps({'status':'PASS','base':base['base'],'frozen_inputs':len(base['inputs']),'sealed_files':len(seal['files']),'old_evidence_unchanged':True,'real_index_unchanged':True,'new_Lean_theorem':False},sort_keys=True))
if __name__=='__main__':main()
