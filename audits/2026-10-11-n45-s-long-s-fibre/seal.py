#!/usr/bin/env python3
"""Final read-only drift/inventory checks, then exclusive delivery manifest."""
import ast
import argparse
import hashlib
import json
from pathlib import Path
import re
from setup import BASE, OUT, ROOT, dump, run as logged_run

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--attempt',default='1');parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args()
    def run(name,argv):return logged_run(f'seal-{args.attempt}-{name}',argv)
    inputs=json.loads((OUT/'inputs.json').read_text());verified=[]
    for e in inputs['entries']:
        frozen=(OUT/e['frozen_path']).read_bytes();live=(ROOT/e['path']).read_bytes()
        assert hashlib.sha256(frozen).hexdigest()==e['sha256'],e['path']
        assert frozen==live,e['path']
        p=run('final-blob-'+str(len(verified)),['git','rev-parse',f"{BASE}:{e['path']}"])
        assert p.returncode==0 and p.stdout.decode().strip()==e['git_blob']
        verified.append(e['path'])
    for e in inputs['external_dependencies']:
        if 'frozen_path' in e:
            assert hashlib.sha256((OUT/e['frozen_path']).read_bytes()).hexdigest()==e['sha256']
    head=run('final-head',['git','rev-parse','HEAD'])
    assert head.stdout.decode().strip()==BASE
    diff=run('final-tracked-diff',['git','diff','--name-only'])
    assert not diff.stdout,'shared tracked files changed; preserve finding and stop'
    run('final-git-diff-check',['git','diff','--check'])
    run('final-worktree-status',['git','status','--short','--untracked-files=all'])
    claims=json.loads((OUT/'claims.json').read_text())
    assert len({c['id'] for c in claims['claims']})==len(claims['claims'])==15
    obligations=json.loads((OUT/'obligations.json').read_text())
    assert obligations['raw_schedule_count']==28 and obligations['excluded_schedules']==4 and obligations['residual_schedules']==24
    for s in obligations['schedules']:
        assert len(s['all_ten_literal_obligations'])==10
        for row in s['all_ten_literal_obligations']:
            assert len(row['pins'])==16
            assert {(p['r'],p['s']) for p in row['pins']}=={(a,b) for a in range(4) for b in range(4)}
    for p in OUT.glob('*.py'):ast.parse(p.read_text())
    report=(OUT/'REPORT.md').read_text();bad_links=[]
    for target in re.findall(r'\]\(([^)]+)\)',report):
        if target.startswith('https://'):continue
        path=target.split('#')[0]
        if path and path!='delivery.json' and not (OUT/path).exists():bad_links.append(target)
    assert not bad_links,bad_links
    certificate=(OUT/'certificate.json').read_bytes()
    assert hashlib.sha256(certificate).hexdigest()=='e06951edd8150a4f70de270fada08239799dd9ac61fb4fb3552755e667dddd93'
    findings=json.loads((OUT/'source-findings.json').read_text())
    for f in findings:
        if f.get('physical_sha256'):
            assert hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['physical_sha256']
    dump(OUT/'final-checks.json',{'base':BASE,'head':BASE,'frozen_BASE_inputs':len(verified),
       'frozen_and_worktree_drift':0,'tracked_diff_paths':[],'report_local_links':'triggered and holds',
       'claims':15,'raw_joint_Q_schedules':28,'limited_excluded_Q_schedules':4,'residual_Q_schedules':24,
       'ten_literals_and_all16_pins_per_schedule':'triggered and holds',
       'canonical_certificate_unchanged':True,'finite_source':'not established or executed; trigger_count null',
       'Lean':'not executed; no new theorem','adoption':'pending independent acceptance',
       'retained_prior_metadata':'metadata-initial/ contains superseded internal drafts, not current claims',
       'shared_docs_old_audits_other_outputs':'read only; no tracked changes',
       'commit_push_PR_external_messages':'none'})
    if args.check_only:
        print(json.dumps({'status':'final checks hold; manifest follows after actual execution logs',
            'frozen_inputs':len(verified),'residual_Q_schedules':24}))
        raise SystemExit(0)
    files=[]
    for p in sorted(OUT.rglob('*')):
        if not p.is_file() or p==OUT/'delivery.json':continue
        raw=p.read_bytes();files.append({'path':str(p.relative_to(OUT)),
             'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
    dump(OUT/'delivery.json',{'task_id':'N45-S-LONG-S-FIBRE','base':BASE,
       'delivery_directory':str(OUT),'adoption':'pending independent acceptance',
       'files':files,'file_count':len(files),
       'metadata_exclusions':[{'path':'delivery.json','reason':'Manifest metadata itself; excluded to prevent recursive self-hash.'}],
       'other_exclusions':[],'shared_files_in_delivery':False,
       'current_authority':['REPORT.md','claims.json','inputs.json','obligations.json','certificate.json','checks.json','final-checks.json'],
       'historical_drafts':['inputs-initial.json','metadata-initial/claims.json','metadata-initial/obligations.json','metadata-initial/reviews.json']})
    print(json.dumps({'files':len(files),'frozen_inputs':len(verified),'claims':15,'residual_Q_schedules':24,
       'metadata_exclusions':['delivery.json'],'status':'sealed; pending independent acceptance'}))
