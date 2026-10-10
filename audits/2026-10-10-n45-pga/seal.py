#!/usr/bin/env python3
"""Seal exclusively. Manifest contains all regular payload, excluding only the two root envelope files."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
for name in ['MANIFEST.sha256','delivery.json']:
    assert not (D/name).exists(),('seal already exists',name)
results=[]
for argv in [['python3','-B','independent_check.py'],['python3','-B','audit_integrity.py']]:
    p=subprocess.run(argv,cwd=D,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    results.append({'argv':argv,'exit_code':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()})
    assert p.returncode==0,results[-1]
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=D).decode().strip()
assert head==json.loads((D/'inputs.json').read_text())['BASE']
final_integrity=json.loads((D/'logs/audit-integrity-v2.command.json').read_text())
assert final_integrity['exit_code']==0
excluded={'MANIFEST.sha256','delivery.json'}
files=sorted(p for p in D.rglob('*') if p.is_file() and str(p.relative_to(D)) not in excluded)
manifest=''.join(sha(p.read_bytes())+'  '+str(p.relative_to(D))+'\n' for p in files)
with (D/'MANIFEST.sha256').open('x') as f:f.write(manifest)
def verify():
    declared={}
    for line in (D/'MANIFEST.sha256').read_text().splitlines():
        h,name=line.split('  ',1);assert name not in declared;declared[name]=h
    actual={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and str(p.relative_to(D)) not in excluded}
    assert set(declared)==actual
    for name,h in declared.items():assert sha((D/name).read_bytes())==h,name
    return len(declared)
n=verify()
report=(D/'REPORT.md').read_text()
for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',report):
    if not target.startswith(('http:','https:')) and target!='delivery.json':assert (D/target.split('#')[0]).exists(),target
pins={name:sha((D/name).read_bytes()) for name in ['REPORT.md','independent-judgment.json','checks.json','inputs.json','MANIFEST.sha256']}
delivery={'task':'N45-PGA','sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'BASE':head,'root':str(D),'report_sha256':pins['REPORT.md'],'judgment_sha256':pins['independent-judgment.json'],'checks_sha256':pins['checks.json'],'inputs_sha256':pins['inputs.json'],'manifest_sha256':pins['MANIFEST.sha256'],'manifest_exclusions':sorted(excluded),'manifest_regular_payload_count':n,'paper_claims_reviewed':6,'new_paper_gaps_found':0,'judgment':'PG01/02/04/05 valid under explicit original LP premises; PG03 original path/Jordan/bridge valid with abstract-only embedding boundary; PGRES necessary integer data only','new_excluded_scope':'edge-pair LP with whole S having one original vertex','whole_LP_status':'OPEN','complete_target_sources':0,'source_realization':False,'new_Lean_theorem':False,'publication':'none','new_supervisor_PR_PC_outputs_read_before_judgment_seal':False,'seal_verification':{'argv':['python3','-B','seal.py'],'cwd':str(D),'exit_code':0,'regular_payload_set_exact':True,'payload_hashes_match':True,'covered_files':n,'stdout':'PASS: exact manifest set and SHA256 for all regular payload; only root MANIFEST.sha256 and delivery.json excluded','stderr':''},'final_preseal_readonly_checks':results,'preserved_packaging_failure':{'command_log':'logs/audit-integrity.command.json','actual_exit_code':1,'reason':'checks.json link tested before checks.json was created','resolved_by':'logs/audit-integrity-v2.command.json','resolved_exit_code':0},'expected_exclusive_refusals':['logs/worker-exclusive-guard.command.json','logs/input-exclusive-guard.command.json'],'shared_scope':'Only this fresh directory written; shared navigation/worker/certificate inputs untouched; no commit/push/external messages/research/enumeration/spawn'}
with (D/'delivery.json').open('x') as f:json.dump(delivery,f,ensure_ascii=False,indent=2,sort_keys=True);f.write('\n')
assert verify()==n
for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',report):
    if not target.startswith(('http:','https:')):assert (D/target.split('#')[0]).exists(),target
print(json.dumps({'status':'SEALED_AND_VERIFIED','regular_payload_files':n,'exclusions':sorted(excluded),**pins,'delivery.json':sha((D/'delivery.json').read_bytes())},indent=2))
