#!/usr/bin/env python3
"""Read-only provenance verification. No mathematical checker decisions imported."""
import argparse, hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
BASE='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
S=ROOT/'audits/2026-10-09-n45-s'
U=ROOT/'audits/2026-10-09-n45-u'
J=ROOT/'audits/2026-10-09-n45-j'
SUP=ROOT/'audits/2026-10-09-n45-s-supervision'
BATCH=ROOT/'audits/2026-10-09-n45-batch-supervision'
def sha(b): return hashlib.sha256(b).hexdigest()
def js(p): return json.loads(p.read_text())
def record(p):
 st=p.stat()
 return {'bytes':st.st_size,'mtime_ns':st.st_mtime_ns,'sha256':sha(p.read_bytes())}
def inventory(directory,skip=()):
 return {str(p.relative_to(ROOT)):record(p) for p in sorted(directory.rglob('*')) if p.is_file() and not any(x in p.relative_to(directory).parts for x in skip)}
def git(*args,cwd=ROOT): return subprocess.check_output(['git',*args],cwd=cwd)
def current():
 files={}
 for directory,skip in [(S,()),(U,('source',)),(J,()),(SUP,()),(BATCH,()),(ROOT/'audits/2026-10-09-n45-j-supervision',()),(ROOT/'audits/2026-10-09-n45-a',('source','checkout'))]:
  # A is not needed as a new mathematical source; frozen authored artifacts only.
  if directory.name=='2026-10-09-n45-a': continue
  files.update(inventory(directory,skip))
 for rel in ['docs/STATUS.md','docs/c5_kempe_guide.md','docs/history/2026-10-09-n2-45-54-parallel-tasks.md']:
  files[rel]=record(ROOT/rel)
 sources=[]
 sd=js(S/'inputs.json');ud=js(U/'inputs.json')
 for group,rows,checkout in [('S',sd['base_files'],Path(sd['source_checkout'])),('U',ud['base_inputs'],U/'source')]:
  for row in rows:
   rel=row['path'];blob=git('show',BASE+':'+rel)
   readpath=Path(row['read_path']) if group=='S' else checkout/rel
   rr=record(readpath);h=sha(blob)
   sources.append({'group':group,'path':rel,'read_path':str(readpath),'declared_sha256':row['sha256'],'base_blob_sha256':h,'read':rr,'matches_BASE':rr['sha256']==h==row['sha256']})
  assert git('rev-parse','HEAD',cwd=checkout).decode().strip()==BASE
  assert not git('status','--porcelain','--untracked-files=no',cwd=checkout).decode().strip()
 return {'head':git('rev-parse','HEAD').decode().strip(),'files':files,'BASE_sources':sources}
def verify_anchors():
 anchors={S/'REPORT.md':'51ea0e8406998e0a2f8dda8edf785e3a67cbeee412cc8a5d3272430bd0138fa1',S/'checker.py':'94b3fb13e8268080e80a441f595fd3fcab449ea2c2937b2bf92c1725e5977dae',S/'certificate.json':'9acb2a6b40de32aeca60ecf9a5b33065c9cba60ad47f5243c1eccadf31f59a02',S/'inputs.json':'09aeaaa919c299c5a8c3ed44ef250e6e90a96ab1040e3fd8bea6fbc57b1e63de',U/'REPORT.md':'0c3d117f1c804bc0695fc97fd570f2ede6451d5a21ca036f337f4d11c5de72a7',U/'checker.py':'37da93a6fe6109f82287eac67db518515b6718c30013f020acfd21e6364162e3',U/'certificate-final.json':'1f7dc2f13fa372150f2d915fd10494986c2f0a3aa08fa965c8b2f013315980d0',U/'inputs.json':'ed32a320d7924af82f87fbbe78c12a667fb34222299414ac4fb4839b6895355d',J/'results/certificate.json':'ecdef656ec2eff887c6725cda21a6d205fce41e5387ce14b2270468f20a861d4'}
 a=[{'path':str(p.relative_to(ROOT)),'expected':h,'actual':sha(p.read_bytes()),'matches':sha(p.read_bytes())==h} for p,h in anchors.items()]
 sd=js(S/'delivery.json');srows=sd['files']
 assert len(srows)==21 and len(set(r['path'] for r in srows))==21
 assert set(inventory(S))=={str((S/r['path']).relative_to(ROOT)) for r in srows}|{str((S/'delivery.json').relative_to(ROOT))}
 assert all(record(S/r['path'])['sha256']==r['sha256'] and (S/r['path']).stat().st_size==r['bytes'] for r in srows)
 su=js(SUP/'inputs.json')['S_frozen_files']
 assert set(su)=={r['path'] for r in srows}|{'delivery.json'}
 assert all(record(S/rel)['sha256']==r['sha256'] for rel,r in su.items())
 uf=js(BATCH/'inputs.json')['U_all_authored_excluding_source']
 actual_u=inventory(U,('source',))
 assert len(uf)==39
 assert set(actual_u)=={str((U/rel).relative_to(ROOT)) for rel in uf}
 assert all(record(U/rel)['sha256']==r['sha256'] for rel,r in uf.items())
 assert all(r['matches'] for r in a)
 return {'anchors':a,'S_delivery_inventory':21,'S_with_delivery':22,'S_delivery_sha256':sha((S/'delivery.json').read_bytes()),'S_supervision_inputs_sha256':sha((SUP/'inputs.json').read_bytes()),'U_authored_inventory':39,'batch_inputs_sha256':sha((BATCH/'inputs.json').read_bytes())}
def write_exclusive(p,data):
 with p.open('x') as f: json.dump(data,f,ensure_ascii=False,indent=2,sort_keys=True);f.write('\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('--freeze',action='store_true');p.add_argument('--result',type=Path,required=True);p.add_argument('--initial-status',type=Path)
 args=p.parse_args();anchors=verify_anchors();now=current()
 assert now['head']==BASE
 assert len([r for r in now['BASE_sources'] if r['group']=='S'])==69
 assert len([r for r in now['BASE_sources'] if r['group']=='U'])==70
 assert all(r['matches_BASE'] for r in now['BASE_sources'])
 if args.freeze:
  data={'task':'N45-SU-A','BASE':BASE,'actual_HEAD':now['head'],'initial_git_status':args.initial_status.read_text() if args.initial_status else None,'verification':anchors,'snapshot':now,'source_role':'BASE Git objects and verified detached S/U sources; shared navigation excluded from mathematics','independence':'No supervision decisions read before independent-judgment.json is sealed; hash inspection only','publication':'no commit/push/PR/messages; only fresh SU-A output'}
 else:
  old=js(OUT/'inputs.json')['snapshot'];data={'task':'N45-SU-A','head':now['head'],'verification':anchors,'authored_or_control_file_count':len(now['files']),'BASE_source_count':len(now['BASE_sources']),'file_inventory_unchanged':set(now['files'])==set(old['files']),'file_drift':[rel for rel in set(now['files'])|set(old['files']) if now['files'].get(rel)!=old['files'].get(rel)],'BASE_source_drift':[i for i,(a,b) in enumerate(zip(old['BASE_sources'],now['BASE_sources'])) if a!=b]}
  assert data['file_inventory_unchanged'] and not data['file_drift'] and not data['BASE_source_drift']
 write_exclusive(args.result,data)
 print(json.dumps({'task':'N45-SU-A','head':now['head'],'files':len(now['files']),'S_sources':69,'U_sources':70,'result':str(args.result),'PASS':True},sort_keys=True))
if __name__=='__main__':main()
