#!/usr/bin/env python3
import hashlib,json,re,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent
BASE='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def rec(p):
 b=p.read_bytes();return {'bytes':len(b),'mtime_ns':p.stat().st_mtime_ns,'sha256':sha(b)}
def need(x,m):
 if not x:raise ValueError(m)
inputs=read(OUT/'inputs.json');drift=[]
for rel,old in inputs['original_worker_snapshot'].items():
 now=rec(ROOT/rel)
 if now!=old:drift.append({'path':rel,'old':old,'new':now})
need(not drift,'original frozen worker drift')
shared_drift=[]
for rel,old in inputs['shared_snapshot'].items():
 now=rec(ROOT/rel)
 if now!=old:shared_drift.append({'path':rel,'old':old,'new':now,'reason':'external change possible; this task writes only its own directory'})
for rel,row in inputs['frozen'].items():need(rec(OUT/'frozen'/rel)==row['copy'],'frozen copy drift')
for rel,row in inputs['base_inputs'].items():need(rec(OUT/'base-source'/rel)=={k:row[k] for k in ('bytes','mtime_ns','sha256')},'BASE input drift')
for row in read(OUT/'supplementary-inputs.json')['base_inputs']:need(rec(OUT/'base-source'/row['path'])=={k:row[k] for k in ('bytes','mtime_ns','sha256')},'BASE supplementary drift')
need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=OUT/'base-source',text=True).strip()==BASE,'source head mismatch')
need(subprocess.check_output(['git','status','--porcelain=v1'],cwd=OUT/'base-source')==b'','source checkout not clean')
cert=read(OUT/'certificate-final.json');need(sha((OUT/'certificate-final.json').read_bytes())=='d7d59397814d3007067374e9cb5fc737589d6bfdd33c9f609924bc645b663827','official certificate drift')
for name in ['final-normal','final-seed17']:
 row=read(OUT/'logs'/(name+'.json'));need(row['exit']==0,'official replay failed')
need(read(OUT/'logs/guard-refusal.json')['exit']==1,'exclusive guard not rejected')
need(read(OUT/'logs/corrupted-refusal.json')['exit']==1,'corrupt certificate not rejected')
text_errors=[];links=[];json_count=0;files=[]
for p in sorted(OUT.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(OUT)
 if rel.parts[0] in {'base-source','frozen'}:continue
 files.append(str(rel))
 if p.suffix=='.json':read(p);json_count+=1
 if p.suffix in {'.md','.py','.json','.sha256'}:
  for n,line in enumerate(p.read_text().splitlines(),1):
   if line.endswith((' ','\t')):text_errors.append([str(rel),n,'trailing whitespace'])
  if p.read_bytes() and not p.read_bytes().endswith(b'\n'):text_errors.append([str(rel),'final newline'])
need(not text_errors,'own output whitespace errors')
for match in re.finditer(r'\[[^\]]*\]\(([^\)]+)\)',(OUT/'REPORT.md').read_text()):
 target=match.group(1)
 if '://' in target:continue
 local=target.split('#')[0];need(bool(local),'empty local link')
 # Seals are created immediately after validation and listed explicitly here.
 if local in {'checks.json','MANIFEST.sha256','delivery.json'}:links.append({'target':target,'status':'final seal created after validation'});continue
 need((OUT/local).exists(),'missing report link: '+local);links.append({'target':target,'status':'exists'})
base_tracked=subprocess.check_output(['git','ls-files','-z'],cwd=OUT/'base-source').decode().split('\0')[:-1]
status=subprocess.check_output(['git','status','--porcelain=v1'],cwd=ROOT,text=True)
result={'task':'N45-PR','BASE':BASE,'source_HEAD':BASE,'source_clean':True,'original_worker_files_checked':len(inputs['original_worker_snapshot']),'original_worker_bytes_and_mtime_drift':drift,'frozen_copies_checked':len(inputs['frozen']),'shared_bytes_and_mtime_drift':shared_drift,'base_reads_checked':len(inputs['base_inputs'])+len(read(OUT/'supplementary-inputs.json')['base_inputs']),'jsons_parsed':json_count,'output_whitespace_errors':text_errors,'report_local_links':links,'base_tracked_files':len(base_tracked),'main_status_final':status,'own_authored_files_at_validation':files,'official_certificate_sha256':sha((OUT/'certificate-final.json').read_bytes()),'paper_status':'LP arbitrary-size exclusion candidate awaiting independent adoption','finite_status':'PASS fixed controls only; LP source contract not triggered','no_shared_writes_by_task':True}
with (OUT/'output-validation.json').open('x') as f:json.dump(result,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({k:result[k] for k in ['source_clean','original_worker_files_checked','original_worker_bytes_and_mtime_drift','shared_bytes_and_mtime_drift','base_reads_checked','jsons_parsed','base_tracked_files','official_certificate_sha256']},sort_keys=True))
