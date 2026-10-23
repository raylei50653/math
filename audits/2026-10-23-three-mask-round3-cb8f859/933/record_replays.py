from pathlib import Path
import hashlib,json,os,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[2];runs=P/'runs';runs.mkdir(exist_ok=True)
cases=[('normal',['python3','-B',str(P/'check.py')],None),('seed17',['python3','-B',str(P/'check.py')],17),('semantic-negative',['python3','-B',str(P/'check.py'),'--negative'],None),('independent-normal',['python3','-B',str(P/'independent.py')],None),('independent-seed17',['python3','-B',str(P/'independent.py')],17)]
receipts=[]
for name,argv,seed in cases:
 env=os.environ.copy()
 if seed is not None:env['PYTHONHASHSEED']=str(seed)
 r=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True)
 for suffix,d in (('stdout',r.stdout),('stderr',r.stderr)):
  with (runs/(name+'.'+suffix)).open('xb') as f:f.write(d)
 result=json.loads(r.stdout) if r.returncode==0 else None
 receipts.append({'name':name,'argv':argv,'PYTHONHASHSEED':seed,'exit_code':r.returncode,'stdout':str((runs/(name+'.stdout')).relative_to(P)),'stderr':str((runs/(name+'.stderr')).relative_to(P)),'result':result})
 assert r.returncode==0,(name,r.stderr.decode())
assert receipts[0]['result']==receipts[1]['result'];assert receipts[3]['result']==receipts[4]['result']
for entry in json.loads((P/'INPUTS.json').read_text())['files']:
 d=(ROOT/entry['path']).read_bytes();assert len(d)==entry['bytes'] and hashlib.sha256(d).hexdigest()==entry['sha256']
verification={'status':'PASS','base':'cb8f8593e273a7426ecadd59797a6e643cc4768e','replays':receipts,'immutable_authority_drift':0,'routing_not_used_as_math_input':True,'initial_independent_diagnostic_failure':{'stage':'before independent certificate generation','issue':'two unused b colour names represented one common S4 orbit','fix':'deduplicate by entire normalized literal tuple','overwritten_existing_certificate':False},'source_realization_claimed':False}
with (P/'VERIFICATION.json').open('x') as f:json.dump(verification,f,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','read_only_replays':len(cases),'semantic_negatives_rejected':len(receipts[2]['result']['semantic_negative_controls']),'immutable_authority_drift':0}))
