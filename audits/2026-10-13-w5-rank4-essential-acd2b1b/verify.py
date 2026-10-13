#!/usr/bin/env python3
"""Read-only frozen-byte and delivery integrity validation."""
from pathlib import Path
import gzip,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent

def sha(data):return hashlib.sha256(data).hexdigest()
def main():
 base=json.loads((ROOT/'BASE.json').read_text());assert base['base']=='acd2b1beea6c909edade565a00eeeeac05d2b3a7'
 checked=0
 for group in ('tracked_inputs','working_tree_inputs'):
  for row in base[group]:
   stored=(ROOT/row['frozen']).read_bytes();assert sha(stored)==row['stored_sha256'],row['frozen']
   raw=gzip.decompress(stored) if row['path'].endswith('.md') else stored
   assert sha(raw)==row['sha256'] and len(raw)==row['bytes'],row['path']
   if group=='tracked_inputs':
    actual=subprocess.check_output(['git','show',base['base']+':'+row['path']],cwd=REPO)
    blob=subprocess.check_output(['git','rev-parse',base['base']+':'+row['path']],cwd=REPO,text=True).strip()
    assert blob==row['git_blob']
   else:actual=(REPO/row['path']).read_bytes()
   assert actual==raw,'input drift: '+row['path'];checked+=1
 delivery=json.loads((ROOT/'DELIVERY.json').read_text())
 actual_paths={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ('DELIVERY.json',)}
 expected_paths={x['path'] for x in delivery['files']};assert actual_paths==expected_paths,'delivery path drift'
 for row in delivery['files']:
  data=(ROOT/row['path']).read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256'],'delivery byte drift: '+row['path']
 summary=json.loads((ROOT/'controls/summary.json').read_text())
 with gzip.open(ROOT/'controls/certificate.jsonl.gz','rb') as stream:
  digest=hashlib.file_digest(stream,'sha256').hexdigest()
 assert digest==summary['mathematical_sha256']
 print(json.dumps({'status':'PASS','frozen_inputs':checked,'delivery_files':len(delivery['files']),'input_drift':0,'certificate_sha256':digest},sort_keys=True))
if __name__=='__main__':main()
