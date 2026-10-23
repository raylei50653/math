from pathlib import Path
import hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parents[2];runs=P/'runs';runs.mkdir(exist_ok=True);receipts=[]
for name,script,flags,seed in [('normal','check.py',[],None),('seed17','check.py',[],17),('semantic-negative','check.py',['--negative'],None),('independent-normal','independent.py',[],None),('independent-seed17','independent.py',[],17)]:
 argv=['python3','-B',str(P/script)]+flags;env=os.environ.copy()
 if seed is not None:env['PYTHONHASHSEED']=str(seed)
 r=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True)
 for suffix,data in [('stdout',r.stdout),('stderr',r.stderr)]:
  with (runs/(name+'.'+suffix)).open('xb') as f:f.write(data)
 assert r.returncode==0,(name,r.stderr.decode())
 receipts.append({'name':name,'argv':argv,'PYTHONHASHSEED':seed,'exit_code':r.returncode,'stdout':'runs/'+name+'.stdout','stderr':'runs/'+name+'.stderr','result':json.loads(r.stdout)})
assert receipts[0]['result']==receipts[1]['result'] and receipts[3]['result']==receipts[4]['result']
for e in json.loads((P/'INPUTS.json').read_text())['files']:
 d=(ROOT/e['path']).read_bytes();assert len(d)==e['bytes'] and hashlib.sha256(d).hexdigest()==e['sha256']
with (P/'VERIFICATION.json').open('x') as f:json.dump({'status':'PASS','base':'cb8f8593e273a7426ecadd59797a6e643cc4768e','immutable_input_count':13,'immutable_input_drift':0,'routing_as_math_input':False,'read_only_replays':receipts,'semantic_negative_count':len(receipts[2]['result']['semantic_negative_controls']),'actual_complete_source_control':'not triggered'},f,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','read_only_replays':len(receipts),'semantic_negative_count':len(receipts[2]['result']['semantic_negative_controls']),'immutable_input_drift':0}))
