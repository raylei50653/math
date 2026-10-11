"""Capture native subprocess command/stdout/stderr/exit without a shell."""
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent

def main():
    name=sys.argv[1]
    args=sys.argv[2:]
    seed17=False
    seal_final=False
    if args and args[0]=='--seal-final':
        seal_final=True
        args=args[1:]
    if args and args[0]=='--seed17':
        seed17=True
        args=args[1:]
    if args and args[0]=='--':
        args=args[1:]
    assert args and all(c.isalnum() or c in '-_' for c in name)
    logs=HERE/'logs'; logs.mkdir(exist_ok=True)
    env=os.environ.copy()
    if seed17:
        env['PYTHONHASHSEED']='17'
    cmd={'argv':args,'cwd':str(ROOT),'env_overrides':{'PYTHONHASHSEED':'17'} if seed17 else {}}
    with (logs/(name+'.command.json')).open('x') as f:
        json.dump(cmd,f,indent=2); f.write('\n')
    start=time.monotonic()
    p=subprocess.run(args,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for suffix,data in [('stdout',p.stdout),('stderr',p.stderr)]:
        with (logs/(name+'.'+suffix)).open('xb') as f:
            f.write(data)
    result={'exit_code':p.returncode,'elapsed_seconds':round(time.monotonic()-start,6),'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)}
    with (logs/(name+'.result.json')).open('x') as f:
        json.dump(result,f,sort_keys=True,indent=2); f.write('\n')
    print(json.dumps({'name':name,**result},sort_keys=True))
    if p.stdout and len(p.stdout)<3000:
        print(p.stdout.decode(errors='replace'),end='')
    if p.stderr and len(p.stderr)<3000:
        print(p.stderr.decode(errors='replace'),end='',file=sys.stderr)
    if seal_final and p.returncode==0:
        files={}
        for path in sorted(HERE.rglob('*')):
            if path.is_file():
                assert not path.is_symlink(),str(path)
                assert path!=HERE/'delivery.json','delivery collision'
                data=path.read_bytes()
                files[str(path.relative_to(HERE))]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        delivery={
            'task_id':'N45-S-LONG-S-BLOCK-TRANSFER','base':'f2692089ad4259808e27d9b7e882ac09505b180a',
            'status':'待獨立驗收','scope':'arbitrary-size full C block-tree identities and named finite interface calibration',
            'new_source_exclusions':0,'target_source':{'executed':False,'trigger_count':None,'status':'not triggered'},
            'payload_files':len(files),'payload_bytes':sum(x['bytes'] for x in files.values()),
            'files':files,'precise_metadata_exclusions':['delivery.json'],
            'exclusion_reason':'delivery.json cannot recursively hash itself; all native command/stream/result logs included',
            'final_native_validation':{'command_log':'logs/'+name+'.command.json',
                'stdout':'logs/'+name+'.stdout','stderr':'logs/'+name+'.stderr','result':'logs/'+name+'.result.json'},
            'boundary':{'shared_docs_modified':False,'prior_deliveries_modified':False,
                        'old_certificates_modified':False,'other_workers_modified':False,
                        'commit':False,'push':False,'PR':False,'external_messages':False},
            'source_realizability':False,'new_Lean':False,'general_N45_N2_E':False
        }
        with (HERE/'delivery.json').open('x') as f:
            json.dump(delivery,f,ensure_ascii=False,sort_keys=True,indent=2); f.write('\n')
        sealed=json.loads((HERE/'delivery.json').read_text())
        actual={str(x.relative_to(HERE)) for x in HERE.rglob('*') if x.is_file() and x!=HERE/'delivery.json'}
        assert actual==set(sealed['files'])
        for path,record in sealed['files'].items():
            data=(HERE/path).read_bytes()
            assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256'],path
        print(json.dumps({'delivery':'delivery.json','payload_files':len(files),
                          'delivery_sha256':hashlib.sha256((HERE/'delivery.json').read_bytes()).hexdigest(),
                          'sealed_payload_rechecked':True,'status':'待獨立驗收'},ensure_ascii=False,sort_keys=True))
    return p.returncode

if __name__=='__main__':
    raise SystemExit(main())
