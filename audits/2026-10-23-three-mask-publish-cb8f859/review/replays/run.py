#!/usr/bin/env python3
"""Read-only five-round publication replays; writes receipts only beside this file."""
import concurrent.futures,datetime,hashlib,json,os,subprocess,sys,time
from pathlib import Path

HERE=Path(__file__).resolve().parent
PUBLISH=HERE.parents[1]
REPO=PUBLISH.parents[1]
ROUNDS=[('round1','2026-10-23-three-mask-methods-cb8f859'),('round2','2026-10-23-three-mask-round2-cb8f859'),
        ('round3','2026-10-23-three-mask-round3-cb8f859'),('round4','2026-10-23-three-mask-round4-cb8f859'),
        ('round5','2026-10-23-three-mask-round5-cb8f859')]
ROUTING_KEYS={'routing','routing_live_drift','routing_background_drift','routing_drift'}

def require(ok,message):
    if not ok:raise AssertionError(message)

def packed(data):return json.dumps(data,sort_keys=True,separators=(',',':')).encode()
def sha(blob):return hashlib.sha256(blob).hexdigest()
def timestamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write_json(name,data):
    with (HERE/name).open('x') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n')

def source_custody(base):
    expected={r['path']:r for r in base['audits']}
    actual={str(p.relative_to(REPO)) for dirname in base['audit_directories'] for p in (REPO/dirname).rglob('*') if p.is_file()}
    changed=[];observed=[]
    for path in sorted(actual):
        blob=(REPO/path).read_bytes();record={'path':path,'bytes':len(blob),'sha256':sha(blob)};observed.append(record)
        if path in expected and any(record[k]!=expected[path][k] for k in ('bytes','sha256')):changed.append(path)
    result={'status':'PASS' if actual==set(expected) and not changed else 'FAIL','checked_utc':timestamp(),
            'expected_files':len(expected),'actual_files':len(actual),'actual_bytes':sum(r['bytes'] for r in observed),
            'expected_bytes':sum(r['bytes'] for r in expected.values()),'missing':sorted(set(expected)-actual),
            'extra':sorted(actual-set(expected)),'bytes_or_SHA_drift':changed,'observed_manifest_sha256':sha(packed(observed))}
    require(result['status']=='PASS','publication source domain/bytes/SHA drift: '+str(result));return result

def verdict(result):
    return result.get('status') in ('PASS','passed') or result.get('result')=='PASS' or result.get('ok') is True

def normalize(value):
    if isinstance(value,dict):return {k:normalize(v) for k,v in value.items() if k not in ROUTING_KEYS and k!='seed'}
    if isinstance(value,list):return [normalize(v) for v in value]
    return value

def differences(a,b,path='$'):
    if type(a) is not type(b):return [{'path':path,'normal':a,'seed17':b}]
    if isinstance(a,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:out.append({'path':path+'.'+k,'normal':a.get(k),'seed17':b.get(k)})
            else:out.extend(differences(a[k],b[k],path+'.'+k))
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [{'path':path,'normal_length':len(a),'seed17_length':len(b)}]
        return [d for i,(x,y) in enumerate(zip(a,b)) for d in differences(x,y,path+'['+str(i)+']')]
    return [] if a==b else [{'path':path,'normal':a,'seed17':b}]

def special_fields(value,path='$'):
    found={'negative_controls':[],'not_triggered':[]}
    def visit(v,p):
        if isinstance(v,dict):
            for k,w in v.items():
                q=p+'.'+k
                if 'negative' in k and isinstance(w,(int,list,dict)):
                    found['negative_controls'].append({'path':q,'count':len(w) if isinstance(w,(list,dict)) else w})
                visit(w,q)
        elif isinstance(v,list):
            for i,w in enumerate(v):visit(w,p+'['+str(i)+']')
        elif v=='not triggered':found['not_triggered'].append(p)
    visit(value,path);return found

def run_one(label,directory,phase):
    root=REPO/'audits'/directory/'check.py';argv=[sys.executable,'-B',str(root)]
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    if phase=='seed17':env['PYTHONHASHSEED']='17'
    else:env.pop('PYTHONHASHSEED',None)
    print(json.dumps({'event':'started','round':label,'phase':phase}),flush=True)
    start=timestamp();clock=time.perf_counter();run=subprocess.run(argv,cwd=REPO,env=env,capture_output=True);elapsed=time.perf_counter()-clock;end=timestamp()
    prefix=label+'-'+phase
    for suffix,blob in [('stdout',run.stdout),('stderr',run.stderr)]:
        with (HERE/(prefix+'.'+suffix)).open('xb') as f:f.write(blob)
    result=json.loads(run.stdout) if run.returncode==0 else None
    metadata={'argv':argv,'cwd':str(REPO),'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'17' if phase=='seed17' else None},
              'start_utc':start,'end_utc':end,'elapsed_seconds':elapsed,'exit_code':run.returncode,
              'stdout':{'path':prefix+'.stdout','bytes':len(run.stdout),'sha256':sha(run.stdout)},
              'stderr':{'path':prefix+'.stderr','bytes':len(run.stderr),'sha256':sha(run.stderr)},
              'entrypoint_documentation':'audits/'+directory+'/REPORT.md','entrypoint_sha256':sha(root.read_bytes())}
    if result is not None:metadata['returned_controls']=special_fields(result)
    write_json(prefix+'.json',metadata)
    require(run.returncode==0,prefix+' failed; retained full stdout/stderr')
    require(set(result['branch_results'])=={'932','933','941'} and all(verdict(v) for v in result['branch_results'].values()),prefix+' missing branch PASS')
    print(json.dumps({'event':'finished','round':label,'phase':phase,'exit_code':run.returncode,'elapsed_seconds':round(elapsed,3)}),flush=True)
    return result,metadata

def run_round(item):
    label,directory=item;a,ma=run_one(label,directory,'normal');b,mb=run_one(label,directory,'seed17')
    diff=differences(a,b);same=normalize(a)==normalize(b)
    comparison={'status':'PASS' if same else 'FAIL','raw_JSON_equal':a==b,'equal_except_explicit_routing_and_seed_metadata':same,
                'ignored_routing_keys':sorted(ROUTING_KEYS),'ignored_seed_field':'seed only','actual_differences':diff,
                'normal_receipt':label+'-normal.json','seed17_receipt':label+'-seed17.json',
                'note':'PYTHONHASHSEED=17 inherited by all branch subprocesses; branch CLI --seed flags are unchanged from each sealed root entrypoint'}
    write_json(label+'-comparison.json',comparison);require(same,label+' substantive normal/seed17 mismatch')
    return label,{'normal':ma,'seed17':mb,'comparison':comparison}

def main():
    blob=(PUBLISH/'BASE.json').read_bytes();base=json.loads(blob);require(len(base['audits'])==738,'publication domain count')
    manifest={'publication_BASE':'audits/'+PUBLISH.name+'/BASE.json','publication_BASE_sha256':sha(blob),
              'audit_directories':base['audit_directories'],'files':base['audits'],'files_count':len(base['audits']),
              'bytes':sum(r['bytes'] for r in base['audits'])}
    write_json('source-manifest.json',manifest);before=source_custody(base);write_json('source-custody-before.json',before)
    results={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures=[executor.submit(run_round,item) for item in ROUNDS]
        for future in concurrent.futures.as_completed(futures):
            label,result=future.result();results[label]=result
    require((PUBLISH/'BASE.json').read_bytes()==blob,'publication BASE changed during replay')
    after=source_custody(base);write_json('source-custody-after.json',after)
    require(before['observed_manifest_sha256']==after['observed_manifest_sha256'],'source bytes changed during replay')
    summary={'status':'PASS','publication_BASE_sha256':sha(blob),'root_replays':10,'branch_replays':30,'rounds':results,
             'source_custody_before':before,'source_custody_after':after,
             'negative_execution_policy':{'round1_round2':{'932':['--check','--negative'],'933':['--negative'],'941':'negative controls run automatically by default; no unsupported flag added'},
                                          'round3_round4_round5':{'932':['--negative'],'933':['--negative'],'941':['--negative']}},
             'write_boundary':str(HERE.relative_to(REPO)),
             'scope':'sealed five-round root entrypoints only; no census, source graph search, unrelated tests, Git/index edits or shared-doc edits',
             'source_realizability':'not triggered; finite successful replays do not realize or exclude general sources',
             'general_932_933_941':'OPEN','actual_smaller_bad':'OPEN','new_Lean':False,'remote_or_commit_claim':False}
    write_json('SUMMARY.json',summary)
    files=[]
    for p in sorted(HERE.rglob('*')):
        if p.is_file():
            data=p.read_bytes();files.append({'path':str(p.relative_to(HERE)),'bytes':len(data),'sha256':sha(data)})
    write_json('MANIFEST.json',{'files':files,'excludes':['MANIFEST.json'],'source_manifest':'source-manifest.json','source_domain_files':738,'source_domain_bytes':manifest['bytes']})
    print(json.dumps({'status':'PASS','root_replays':10,'source_files':738,'source_bytes':manifest['bytes'],'source_drift':0,'receipt_files':len(files)}),flush=True)

if __name__=='__main__':main()
