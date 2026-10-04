import importlib.util, json, pathlib, sys, traceback, time
root=pathlib.Path('/home/ray/developer/ai/math')
out=pathlib.Path('/tmp/math-progress-publish-20261004-control-replays')
target=root/'scripts/c5_excess_two_e4c_controls.py'
spec=importlib.util.spec_from_file_location('e4c_readonly',target)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
old_encoded=m.encoded
captured=[]
def encoded(obj):
    raw=old_encoded(obj)
    if isinstance(obj,dict) and obj.get('schema')=='c5-e4c-controls-v1':captured.append(raw)
    return raw
m.encoded=encoded
sys.argv=[str(target),'--check']
start=time.monotonic()
try:
    code=m.main()
except Exception:
    traceback.print_exc();code=1
assert len(captured)==1, len(captured)
raw=captured[0]
with (out/'c5_excess_two_e4c-final-recomputed-summary.json').open('xb') as f:f.write(raw)
saved=json.loads((root/'artifacts/c5_excess_two_e4c/summary.json').read_bytes())
current=json.loads(raw)
def diffs(a,b,path=''):
    if type(a)!=type(b):return [dict(path=path,saved=a,current=b)]
    if isinstance(a,dict):
        result=[]
        for k in sorted(set(a)|set(b)):
            q=f'{path}/{k}'
            if k not in a or k not in b:result.append(dict(path=q,saved=a.get(k),current=b.get(k)))
            else:result.extend(diffs(a[k],b[k],q))
        return result
    if isinstance(a,list):
        if len(a)!=len(b):return [dict(path=path,saved_length=len(a),current_length=len(b))]
        result=[]
        for i,(x,y) in enumerate(zip(a,b)):result.extend(diffs(x,y,f'{path}/{i}'))
        return result
    return [] if a==b else [dict(path=path,saved=a,current=b)]
s={k:v for k,v in saved.items() if k!='source_hashes'};c={k:v for k,v in current.items() if k!='source_hashes'}
result=dict(script=str(target),artifact='artifacts/c5_excess_two_e4c/summary.json',exit_code=code,duration_seconds=round(time.monotonic()-start,3),full_json_differences=diffs(saved,current),excluded_provenance_key='source_hashes',nonprovenance_equal=s==c,semantic_differences=diffs(s,c),processed=current['processed'],expected_controls=current['expected_controls'],total_rejected_row_cores=current['total_rejected_row_cores'],counterexample=current['counterexample'])
with (out/'e4c-final-semantic-diff.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(result,sort_keys=True))
