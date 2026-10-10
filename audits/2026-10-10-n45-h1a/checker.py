#!/usr/bin/env python3
"""Read-only identity/scope/arithmetic checker; the arbitrary-size proof is paper."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from controls import calculate

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
META={'MANIFEST.sha256','delivery.json','receipt.json',
      'seal-checks/normal.stdout.txt','seal-checks/normal.stderr.txt',
      'seal-checks/seed17.stdout.txt','seal-checks/seed17.stderr.txt',
      'seal-checks/bad-digest.stdout.txt','seal-checks/bad-digest.stderr.txt',
      'seal-checks/commands.json','seal-checks/payload-before.json',
      'seal-checks/payload-after.json'}

def sha(b): return hashlib.sha256(b).hexdigest()
def encoded(x): return (json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
def need(ok,s):
    if not ok: raise ValueError(s)
def files(p):
    rows={}
    for f in sorted(p.rglob('*')):
        need(not f.is_symlink(),'symlink: '+str(f))
        if f.is_file(): rows[str(f.relative_to(p))]=sha(f.read_bytes())
    return rows
def payload(): return {k:v for k,v in files(HERE).items() if k not in META}
def validate_manifest(path):
    rows={}
    for line in path.read_text().splitlines():
        need(bool(re.fullmatch(r'[0-9a-f]{64}  .+',line)),'manifest syntax')
        digest,name=line.split('  ',1); p=PurePosixPath(name)
        need(not p.is_absolute() and '..' not in p.parts and str(p)==name,
             'unsafe manifest path')
        need(name not in rows and name not in META,'duplicate/excluded manifest path')
        rows[name]=digest
    actual=payload()
    need(set(rows)==set(actual),'manifest exact inventory')
    for name,digest in rows.items(): need(actual[name]==digest,'manifest digest: '+name)
    return rows

def validate_inputs():
    data=json.loads((HERE/'inputs.json').read_bytes())
    need(data['BASE']==BASE and data['HEAD']==BASE,'frozen BASE/HEAD')
    need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE,
         'live HEAD')
    W=ROOT/data['worker']; actual=files(W)
    expected={str(Path(x['path']).relative_to(data['worker'])):x['sha256']
              for x in data['worker_full_tree']}
    need(actual==expected,'whole immutable worker tree')
    for row in data['frozen_inputs']:
        raw=(HERE/row['frozen']).read_bytes()
        need(sha(raw)==row['sha256'],'frozen input: '+row['frozen'])
        if row['layer']=='BASE':
            rawgit=subprocess.check_output(['git','show',BASE+':'+row['path']],cwd=ROOT)
            need(rawgit==raw,'BASE bytes: '+row['path'])
            blob=subprocess.check_output(['git','rev-parse',BASE+':'+row['path']],cwd=ROOT,text=True).strip()
            need(blob==row['git_blob'],'BASE blob: '+row['path'])
        if row.get('live_immutable_audit'):
            need(sha((ROOT/row['path']).read_bytes())==row['sha256'],
                 'old immutable audit: '+row['path'])
    # Original current shared bytes are intentionally frozen, permitting authorized adoption.
    need(len(data['frozen_inputs'])==34 and len(actual)==94,'input coverage')
    return data

def validate_scope():
    j=json.loads((HERE/'independent-judgment.json').read_bytes())
    w=json.loads((HERE/'frozen/worker/claims.json').read_bytes())
    ids=['HIGH1-'+x for x in ('CORE','COMP','JOIN','RESTORE','F','MAP','K33','ARC','REJECT','EXCLUSION')]
    need([x['id'] for x in j['claims']]==ids,'claim identities')
    need([x['id'] for x in w['claims']]==ids,'worker identities')
    h=j['full_source_contract'];need(set(h)=={f'H{i}' for i in range(1,14)},'H1-H13')
    for c in j['claims']:
        need(c['full_source_contract']==h,'complete claim contract')
        need(c['verdict']=='holds' and not c['additional_premises'],'paper verdict metadata')
        need(not c['machine_proved'] and not c['new_Lean'],'claim evidence layer')
    need(j['decision']=='accepted_HIGH1_with_full_H1_H13','scoped decision')
    need(not j['machine_proved'] and not j['new_Lean'] and not j['shared_adoption'],'evidence boundary')
    need(not j['finite_source']['established'] and not j['finite_source']['executed']
         and j['finite_source']['trigger_count'] is None,'no source trigger claim')
    need(j['general_N2_E']=='OPEN','general stop')
    expected=encoded(calculate())
    need((HERE/'arithmetic-controls.json').read_bytes()==expected,'arithmetic control bytes')
    local_links=0
    for name in ('REPORT.md','proof-reconstruction.md'):
        txt=(HERE/name).read_text()
        need(not any(line.rstrip()!=line for line in txt.splitlines()),'authored whitespace: '+name)
        for link in re.findall(r'\]\(([^)]+)\)',txt):
            if link.startswith(('https://','http://','#')): continue
            path=link.split('#',1)[0]
            need((HERE/path).exists(),'local link: '+link);local_links+=1
    return len(ids),local_links

def validate_receipt():
    d=json.loads((HERE/'delivery.json').read_bytes())
    need(d['manifest_sha256']==sha((HERE/'MANIFEST.sha256').read_bytes()),'delivery manifest binding')
    need(d['receipt_bound_files']['receipt.json']==sha((HERE/'receipt.json').read_bytes()),'delivery receipt binding')
    r=json.loads((HERE/'receipt.json').read_bytes())
    need(set(r['files'])==META-{'MANIFEST.sha256','delivery.json','receipt.json'},'receipt exact metadata')
    need(d['receipt_bound_files']==dict(r['files'],**{'receipt.json':sha((HERE/'receipt.json').read_bytes())}),
         'delivery exact metadata')
    for name,digest in r['files'].items(): need(sha((HERE/name).read_bytes())==digest,'receipt bytes: '+name)
    before=json.loads((HERE/'seal-checks/payload-before.json').read_bytes())
    after=json.loads((HERE/'seal-checks/payload-after.json').read_bytes())
    need(before==after==payload(),'seal read-only payload')
    logs=json.loads((HERE/'seal-checks/commands.json').read_bytes())
    need([x['id'] for x in logs]==['normal','seed17','bad-digest'],'receipt commands')
    for x in logs:
        need(x['actual_exit']==x['expected_exit'],'receipt actual exit')
        for stream in ('stdout','stderr'):
            need(sha((HERE/x[stream+'_file']).read_bytes())==x[stream+'_sha256'],'command stream')
    need((HERE/'seal-checks/normal.stdout.txt').read_bytes()==(HERE/'seal-checks/seed17.stdout.txt').read_bytes(),
         'normal seed17 stdout')
    need((HERE/'seal-checks/normal.stderr.txt').read_bytes()==(HERE/'seal-checks/seed17.stderr.txt').read_bytes(),
         'normal seed17 stderr')
    need(b'manifest digest' in (HERE/'seal-checks/bad-digest.stderr.txt').read_bytes(),'negative stage')

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true')
    p.add_argument('--unsealed',action='store_true');p.add_argument('--payload-only',action='store_true')
    p.add_argument('--manifest',type=Path); a=p.parse_args()
    try:
        data=validate_inputs();claims,links=validate_scope()
        manifest_count=None
        if not a.unsealed:
            manifest_count=len(validate_manifest(a.manifest or HERE/'MANIFEST.sha256'))
            if not a.payload_only: validate_receipt()
        print(json.dumps({'task':'N45-H1A','claims_bound':claims,'all_H1_H13':True,
                          'immutable_worker_files':len(data['worker_full_tree']),
                          'frozen_inputs':34,'BASE_blobs':16,'old_audit_live_hashes':9,
                          'local_links':links,'manifest_payload_files':manifest_count,
                          'fixed_arithmetic_calibration':'triggered and holds',
                          'finite_HIGH1_source':'not performed; no trigger count',
                          'paper_machine_proved':False,'new_Lean':False},sort_keys=True))
        return 0
    except (ValueError,KeyError,FileNotFoundError,AssertionError) as e:
        print('integrity rejection: '+str(e),file=sys.stderr);return 2

if __name__=='__main__': sys.exit(main())
