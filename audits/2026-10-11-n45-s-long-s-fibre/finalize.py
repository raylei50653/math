#!/usr/bin/env python3
"""Seal after retaining the actual completed final-check command output."""
import hashlib
import json
from setup import BASE, OUT, dump, run, write

if __name__=='__main__':
    # This is the actual prior tool-observed failure, not a rerun or discarded generation.
    write(OUT/'logs/seal-attempt1.stdout',b'')
    write(OUT/'logs/seal-attempt1.stderr',(
       'Traceback (most recent call last):\n'
       f'  File "{OUT}/seal.py", line 43, in <module>\n'
       '    assert not bad_links,bad_links\n'
       '           ^^^^^^^^^^^^^\n'
       "AssertionError: ['delivery.json']\n").encode())
    dump(OUT/'logs/seal-attempt1.json',{'argv':['python3','-B','audits/2026-10-11-n45-s-long-s-fibre/seal.py'],
       'cwd':str(OUT.parents[1]),'exit':1,'stdout':'logs/seal-attempt1.stdout','stderr':'logs/seal-attempt1.stderr',
       'finding':'Forward link to delivery.json checked before manifest creation.',
       'repair':'Only declared delivery metadata may be forward referenced; second attempt gets distinct logs.'})
    r=run('seal-attempt2',['python3','-B',str(OUT/'seal.py'),'--attempt','2','--check-only'])
    if r.returncode:raise SystemExit(r.returncode)
    files=[]
    for p in sorted(OUT.rglob('*')):
        if not p.is_file() or p==OUT/'delivery.json':continue
        raw=p.read_bytes();files.append({'path':str(p.relative_to(OUT)),
          'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
    manifest={'task_id':'N45-S-LONG-S-FIBRE','base':BASE,'delivery_directory':str(OUT),
       'adoption':'pending independent acceptance','files':files,'file_count':len(files),
       'metadata_exclusions':[{'path':'delivery.json','reason':'Manifest metadata itself; excluded to prevent recursive self-hash.'}],
       'other_exclusions':[],'shared_files_in_delivery':False,
       'current_authority':['REPORT.md','claims.json','inputs.json','obligations.json','certificate.json','checks.json','final-checks.json'],
       'historical_drafts':['inputs-initial.json','metadata-initial/claims.json','metadata-initial/obligations.json','metadata-initial/reviews.json']}
    dump(OUT/'delivery.json',manifest)
    # Verify emitted inventory and hashes read-only. No files are created after the manifest.
    emitted=json.loads((OUT/'delivery.json').read_text())
    inventory={str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()}
    assert inventory=={f['path'] for f in emitted['files']}|{'delivery.json'}
    for f in emitted['files']:
        assert hashlib.sha256((OUT/f['path']).read_bytes()).hexdigest()==f['sha256']
    print(json.dumps({'status':'sealed; every delivered payload hash and complete inventory verified',
       'files':len(files),'frozen_inputs':58,'claims':15,'residual_Q_schedules':24}))
