#!/usr/bin/env python3
"""Restore this complete research audit using only staged blobs, then replay."""
from pathlib import Path
import gzip,hashlib,json,subprocess,sys,tempfile
D=Path(__file__).resolve().parent
ROOT=D.parents[1]
AUDIT='audits/2026-10-20-r6-941-j1-five-edge-417732f'
PUB=D.relative_to(ROOT).as_posix()

def get(p):return subprocess.check_output(['git','-C',str(ROOT),'show',':'+p])
def main():
 source=json.loads(gzip.decompress(get(PUB+'/SOURCE_FILES.json.gz')))
 archive=json.loads(get('audits/ARCHIVE.json'));cache={};archived=0
 with tempfile.TemporaryDirectory(prefix='math-j1-five-edge-index-') as temporary:
  dest=Path(temporary)
  for rec in source:
   p=rec['path'];assert p.startswith(AUDIT+'/')
   if p in archive['files']:
    archived+=1;sha=rec['sha256']
    if sha not in cache:
     blob=archive['blobs'][sha];raw=get(blob['path'])
     assert len(raw)==blob['bytes'] and hashlib.sha256(raw).hexdigest()==blob['sha256']
     cache[sha]=gzip.decompress(raw)
    data=cache[sha]
   else:data=get(p)
   assert len(data)==rec['bytes'] and hashlib.sha256(data).hexdigest()==rec['sha256']
   out=dest/p;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data);out.chmod(rec['mode'])
  run=subprocess.run([sys.executable,'-B',str(dest/AUDIT/'check.py')],cwd=dest,capture_output=True,text=True)
  (D/'checks/fresh-research.log').write_text(run.stdout+run.stderr)
  assert run.returncode==0,(run.returncode,run.stdout,run.stderr)
  result=json.loads(run.stdout);assert result['status']=='PASS connected exact W7 audit'
  summary={'status':'PASS staged fresh-checkout replay','restored_source_files':len(source),
    'archive_paths':archived,'research_subcheckers':len(result['results']),
    'frozen_inputs':result['frozen_inputs'],'general_J1_excluded':False}
  (D/'checks/fresh-replay.json').write_text(json.dumps(summary,indent=2)+'\n')
  print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
