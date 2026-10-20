#!/usr/bin/env python3
"""Verify original research bytes, append-only archive records and staged scope."""
from pathlib import Path
import argparse,gzip,hashlib,json,subprocess
D=Path(__file__).resolve().parent
ROOT=D.parents[1]
AUDIT='audits/2026-10-20-r6-941-j1-five-edge-417732f/'
PUB='audits/2026-10-20-j1-five-edge-publication-417732f/'
HISTORY='docs/history/2026-10-20-j1-five-edge-progress-publish.md'

def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--index',action='store_true');a=ap.parse_args()
 entries={}
 for item in git('ls-files','--stage','-z').split(b'\0'):
  if not item:continue
  meta,p=item.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0'
  entries[p.decode()]=(mode,oid)
 def read(p):
  if not a.index:return (ROOT/p).read_bytes()
  assert p in entries,('missing indexed file',p)
  return git('cat-file','blob',entries[p][1])
 source=json.loads(gzip.decompress(read(PUB+'SOURCE_FILES.json.gz')))
 before=json.loads(gzip.decompress(read(PUB+'archive-before.json.gz')))
 archive=json.loads(read('audits/ARCHIVE.json'))
 for kind in ('files','blobs'):
  assert all(archive[kind].get(k)==v for k,v in before[kind].items()),('old archive records changed',kind)
 checked={};counts={'git':0,'archive':0}
 for rec in source:
  p=rec['path'];assert p.startswith(AUDIT)
  local=ROOT/p
  if local.exists():
   b=local.read_bytes();assert len(b)==rec['bytes'] and sha(b)==rec['sha256'],('local source changed',p)
  if p in archive['files']:
   r=archive['files'][p]
   assert all(r[k]==rec[k] for k in ('bytes','sha256','mode')),('archive source changed',p)
   digest=r['sha256']
   if digest not in checked:
    blob=archive['blobs'][digest];raw=read(blob['path'])
    assert len(raw)==blob['bytes'] and sha(raw)==blob['sha256'],('gzip drift',blob['path'])
    b=gzip.decompress(raw);assert sha(b)==digest
    checked[digest]=len(b)
   assert checked[digest]==rec['bytes'];counts['archive']+=1
   if a.index:assert p not in entries,('archived source also tracked',p)
  else:
   b=read(p);assert len(b)==rec['bytes'] and sha(b)==rec['sha256'],('git source changed',p)
   if a.index:assert entries[p][0]==('100755' if rec['mode']&0o111 else '100644')
   counts['git']+=1
 if a.index:
  added_blobs={v['path'] for k,v in archive['blobs'].items() if k not in before['blobs']}
  exact={'.gitignore','audits/ARCHIVE.json','docs/STATUS.md','docs/c5_kempe_guide.md','docs/c5_state_guide.md',HISTORY}
  paths=git('diff','--cached','--name-only','-z').decode().split('\0')
  assert all(not p or p in exact or p in added_blobs or p.startswith(AUDIT) or p.startswith(PUB) for p in paths),'unrelated staged file'
 print(json.dumps({'status':'PASS source custody','indexed':a.index,'source_files':len(source),
  'source_raw_bytes':sum(r['bytes'] for r in source),'storage':counts,
  'unique_source_blobs_verified':len(checked),'old_archive_records_unchanged':True,
  'new_archive_paths':len(archive['files'])-len(before['files']),
  'new_archive_blobs':len(archive['blobs'])-len(before['blobs'])},sort_keys=True))
if __name__=='__main__':main()
