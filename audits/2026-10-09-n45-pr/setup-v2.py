#!/usr/bin/env python3
import hashlib,json,os,subprocess,time
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
BASE='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
(OUT/'logs/setup-v2').mkdir()
def enc(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def write(name,data):
 with (OUT/name).open('xb') as f:f.write(data if isinstance(data,bytes) else enc(data))
def rec(p):
 b=p.read_bytes();return {'bytes':len(b),'mtime_ns':p.stat().st_mtime_ns,'sha256':hashlib.sha256(b).hexdigest()}
commands=[]
def run(name,argv,cwd=ROOT):
 start=time.monotonic();r=subprocess.run(argv,cwd=cwd,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 write('logs/setup-v2/'+name+'.stdout.log',r.stdout);write('logs/setup-v2/'+name+'.stderr.log',r.stderr)
 row={'argv':argv,'cwd':str(cwd),'env_override':{'PYTHONDONTWRITEBYTECODE':'1'},'exit':r.returncode,'seconds':time.monotonic()-start,'stdout':'logs/setup-v2/'+name+'.stdout.log','stderr':'logs/setup-v2/'+name+'.stderr.log'}
 commands.append(row);return r
assert run('initial-head',['git','rev-parse','HEAD']).stdout.decode().strip()==BASE
status=run('initial-status',['git','status','--porcelain=v1']).stdout.decode()
run('base-object',['git','cat-file','-e',BASE+'^{commit}'])
anchors={
'docs/c5_excess_two_nonadjacent_unit_core45.md':'d27e84297a20a14e793bd74d4d223983e67e9b4378eb22f3c6b17bfe4a895462',
'audits/2026-10-09-n45-s/REPORT.md':'51ea0e8406998e0a2f8dda8edf785e3a67cbeee412cc8a5d3272430bd0138fa1',
'audits/2026-10-09-n45-u/REPORT.md':'0c3d117f1c804bc0695fc97fd570f2ede6451d5a21ca036f337f4d11c5de72a7',
'audits/2026-10-09-n45-u/certificate-final.json':'1f7dc2f13fa372150f2d915fd10494986c2f0a3aa08fa965c8b2f013315980d0',
'audits/2026-10-09-n45-su-a/REPORT.md':'6a2fbd8d1c2225265dd053070ed59e3e4dd129d9ba825090d197ce0c088820ca',
'audits/2026-10-09-n45-su-a/independent-judgment.json':'97ba9e80fedeb1fef95c767f525b17ffde6e676cd4b06131a8b295741ac95872',
'audits/2026-10-09-n45-su-j/REPORT.md':'b09822e90beff372b54653b42674035c0568dee886b6389c14e3b98ff0ebad24',
'audits/2026-10-09-n45-su-j/certificate.json':'a4b5b4c148f823f8df22a2672700eb40516bae0fd673edf8210a477af3b508ee',
'audits/2026-10-09-n45-j/results/certificate.json':'ecdef656ec2eff887c6725cda21a6d205fce41e5387ce14b2270468f20a861d4'}
for p,d in anchors.items():assert rec(ROOT/p)['sha256']==d,p
manifest_checks=[]
for group in ['su-a','su-j']:
 folder=ROOT/('audits/2026-10-09-n45-'+group);rows={}
 for line in (folder/'MANIFEST.sha256').read_text().splitlines():
  d,p=line.split('  ',1);assert p not in rows;assert (folder/p).resolve().is_relative_to(folder.resolve());assert rec(folder/p)['sha256']==d,p;rows[p]=d
 actual={str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file()}
 assert actual==set(rows)|{'MANIFEST.sha256','delivery.json'}
 delivery=json.loads((folder/'delivery.json').read_text())
 if group=='su-a':
  assert {r['path'] for r in delivery['files']}==set(rows)|{'MANIFEST.sha256'}
  for r in delivery['files']:
   now=rec(folder/r['path']);assert now['bytes']==r['bytes'] and now['sha256']==r['sha256']
 else:assert rec(folder/'MANIFEST.sha256')['sha256']==delivery['manifest_sha256']
 manifest_checks.append({'group':group,'entries':len(rows),'exact_inventory':True,'manifest':rec(folder/'MANIFEST.sha256')})
snapshot=json.loads((ROOT/'audits/2026-10-09-n45-su-j/initial-state.json').read_text())
worker_files={}
for group in ['s','u','j']:
 folder=ROOT/('audits/2026-10-09-n45-'+group)
 actual={str(p.relative_to(folder)):rec(p) for p in folder.rglob('*') if p.is_file() and not(group=='u' and p.relative_to(folder).parts[0]=='source')}
 assert actual==snapshot['authored'][group],group
 for p,r in actual.items():worker_files[str(folder.relative_to(ROOT)/p)]=r
for group in ['su-a','su-j']:
 folder=ROOT/('audits/2026-10-09-n45-'+group)
 for p in folder.rglob('*'):
  if p.is_file():worker_files[str(p.relative_to(ROOT))]=rec(p)
shared_paths=['docs/HANDOFF.md','docs/STATUS.md','docs/DOCUMENTATION.md','docs/c5_kempe_guide.md','docs/c5_phase_b_common_lemmas.md','artifacts/c5_excess_two_e4/REPORT.md','docs/history/2026-10-09-n45-u-long-short-pair-tasks.md','docs/c5_excess_two_nonadjacent_unit_core45.md']
shared={p:rec(ROOT/p) for p in shared_paths}
selected=set(anchors)|set(shared_paths)|{'audits/2026-10-09-n45-su-supervision/REPORT.md','audits/2026-10-09-n45-su-supervision/independent-review.json','audits/2026-10-09-n45-su-supervision/checks.json','audits/2026-10-09-n45-su-j/inputs.json','audits/2026-10-09-n45-su-a/inputs.json','audits/2026-10-09-n45-u/checks.json','audits/2026-10-09-n45-su-a/MANIFEST.sha256','audits/2026-10-09-n45-su-j/MANIFEST.sha256'}
frozen={}
for p in sorted(selected):
 dest=OUT/'frozen'/p;dest.parent.mkdir(parents=True,exist_ok=True)
 with dest.open('xb') as f:f.write((ROOT/p).read_bytes())
 frozen[p]={'original':rec(ROOT/p),'copy':rec(dest),'authority':'frozen working delivery; not a BASE Git blob'}
r=run('clone',['git','clone','--shared','--no-checkout','--no-hardlinks',str(ROOT),str(OUT/'base-source')]);assert r.returncode==0
assert run('checkout',['git','checkout','--detach',BASE],OUT/'base-source').returncode==0
assert run('checkout-head',['git','rev-parse','HEAD'],OUT/'base-source').stdout.decode().strip()==BASE
assert run('checkout-status',['git','status','--porcelain=v1'],OUT/'base-source').stdout==b''
base_paths=['docs/HANDOFF.md','docs/STATUS.md','docs/DOCUMENTATION.md','docs/c5_kempe_guide.md','docs/c5_phase_b_common_lemmas.md','docs/c5_unary_shield_budget.md','artifacts/c5_cells/cells.json','artifacts/c5_excess_one_e2/REPORT.md','artifacts/c5_excess_two_e3/REPORT.md','artifacts/c5_excess_two_e3/nonadjacent_notes.md','artifacts/c5_excess_two_e4/REPORT.md','artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md','artifacts/c5_excess_two_e4/core_constraints.json','artifacts/c5_excess_two_e4/reductions.json','scripts/check_docs.py']
base_inputs={}
for p in base_paths:
 blob=run('blob-'+str(len(base_inputs)),['git','show',BASE+':'+p]);assert blob.returncode==0
 assert blob.stdout==(OUT/'base-source'/p).read_bytes(),p
 base_inputs[p]={**rec(OUT/'base-source'/p),'authority':'Git object '+BASE+':'+p}
write('inputs.json',{'task':'N45-PR','BASE':BASE,'source_HEAD':BASE,'anchors':anchors,'exact_manifests':manifest_checks,'original_worker_snapshot':worker_files,'shared_snapshot':shared,'frozen':frozen,'base_inputs':base_inputs,'initial_shared_status':status,'scope':'only this fresh directory; no subagents, commits, pushes, PRs or messages','finite_plan':'support/color transport identities and existing frozen lift calibration only; no new graph/piece search'})
write('logs/setup-v2.json',{'commands':commands,'anchors_verified':len(anchors),'exact_manifests':manifest_checks,'worker_files':len(worker_files),'base_reads':len(base_inputs),'source_initial_clean':True})
print(json.dumps({'OUT':str(OUT),'anchors':len(anchors),'manifests':[r['entries'] for r in manifest_checks],'frozen_inputs':len(frozen),'base_reads':len(base_inputs)}))
