from pathlib import Path
import hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2];out=P/'runs';out.mkdir(exist_ok=True)
cases=[('normal','check.py',[],None),('seed17','check.py',[],17),('semantic-negative','check.py',['--negative'],None),('independent-normal','independent.py',[],None),('independent-seed17','independent.py',[],17)];receipts=[]
for name,script,flags,seed in cases:
 argv=['python3','-B',str(P/script)]+flags;env=os.environ.copy()
 if seed is not None:env['PYTHONHASHSEED']=str(seed)
 run=subprocess.run(argv,cwd=R,env=env,capture_output=True)
 for suffix,data in [('stdout',run.stdout),('stderr',run.stderr)]:
  with (out/(name+'.'+suffix)).open('xb') as f:f.write(data)
 assert run.returncode==0,(name,run.stderr.decode())
 receipts.append({'name':name,'argv':argv,'seed':seed,'exit_code':run.returncode,'stdout':'runs/'+name+'.stdout','stderr':'runs/'+name+'.stderr','result':json.loads(run.stdout)})
assert receipts[0]['result']==receipts[1]['result'] and receipts[3]['result']==receipts[4]['result']
for e in json.loads((P/'INPUTS.json').read_text())['files']:
 d=(R/e['path']).read_bytes();assert len(d)==e['bytes'] and hashlib.sha256(d).hexdigest()==e['sha256']
with (P/'VERIFICATION.json').open('x') as f:json.dump({'status':'PASS','base':'cb8f8593e273a7426ecadd59797a6e643cc4768e','immutable_input_count':13,'immutable_drift':0,'routing_as_math_input':False,'read_only_replays':receipts,'semantic_negative_count':len(receipts[2]['result']['semantic_negative_controls']),'actual_complete_source_control':'not triggered'},f,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','read_only_replays':len(receipts),'semantic_negative_count':len(receipts[2]['result']['semantic_negative_controls']),'immutable_drift':0}))
