#!/usr/bin/env python3
"""Finalize this fresh PG delivery once; never replace prior evidence."""
from pathlib import Path
import hashlib,json,subprocess,sys,time
D=Path(__file__).resolve().parent;I=json.loads((D/'inputs.json').read_text());R=Path(I['root']);S=Path(I['source'])
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
 b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode() if not isinstance(obj,bytes) else obj
 with (D/name).open('xb') as f:f.write(b)
def run(label,argv,cwd):
 r=subprocess.run(argv,cwd=cwd,capture_output=True)
 put('logs/'+label+'.stdout.log',r.stdout);put('logs/'+label+'.stderr.log',r.stderr)
 put('logs/'+label+'.command.json',{'argv':argv,'cwd':str(cwd),'exit_code':r.returncode})
 return r
for f in ['checks.json','delivery.json','MANIFEST.sha256','final-state.json']:
 assert not (D/f).exists(),('exclusive-create guard',f)
v=run('seal-input-verification',[sys.executable,'-B',str(D/'verify_inputs.py')],R);assert v.returncode==0
head=run('final-source-head',['git','rev-parse','HEAD'],S);assert head.stdout.decode().strip()==I['BASE']
st=run('final-source-status',['git','status','--porcelain'],S);assert not st.stdout
main=run('final-main-status',['git','status','--short'],R)
records=[]
expected_one={'bootstrap-initial','base-docs','whole-docgraph','exclusive-create-refusal'}
for p in sorted((D/'logs').glob('*.command.json')):
 q=json.loads(p.read_text());label=p.name.removesuffix('.command.json')
 expected=1 if label in expected_one else 0
 assert q['exit_code']==expected,(label,q)
 records.append({'label':label,'command_record':str(p.relative_to(D)),'stdout_log':str((D/'logs'/(label+'.stdout.log')).relative_to(D)) if (D/'logs'/(label+'.stdout.log')).exists() else None,'stderr_log':str((D/'logs'/(label+'.stderr.log')).relative_to(D)) if (D/'logs'/(label+'.stderr.log')).exists() else None,'actual_exit_code':q['exit_code'],'classification':'expected refusal; protected existing certificate' if label=='exclusive-create-refusal' else ('preserved historical documentation failure' if label in ['base-docs','whole-docgraph'] else ('recovered setup failure' if label=='bootstrap-initial' else 'passed'))})
sha=digest(D/'certificate.json');assert sha=='75544f2ba3aec74e8c4ccb2f51a42f5fb022009f4a864d76d2d73a2064efd30d'
for p in D.iterdir():
 if p.is_file() and p.suffix in ['.py','.md','.json','.svg']:
  text=p.read_text();assert text.endswith('\n') and all(x.rstrip()==x for x in text.splitlines()),p
state={'BASE':I['BASE'],'source_HEAD':head.stdout.decode().strip(),'source_git_status':st.stdout.decode(),'main_status':main.stdout.decode(),'own_scope':str(D),'publication':'none; no commit/push/PR/external messages','shared_change_note':'main already had tracked edits; independently running PC/PR directories appeared during PG. No shared tracked file was written by PG; full input bytes remain pinned.','only_owned_output_mutated':True}
put('final-state.json',state)
checks={'task':'N45-PG','command_results':records,'certificate':{'path':'certificate.json','bytes':(D/'certificate.json').stat().st_size,'sha256':sha,'normal_exact_byte_replay':True,'seed17_exact_byte_replay':True,'read_only_replays':True,'exclusive_create_refusal_kept':True,'hash_after_refusal_equal':True},'claims':{'PG-01':'arbitrary-size necessary partition/outside identity','PG-02':'arbitrary-size K3,3 bag proof restricting spokes','PG-03':'original paths/bridge identity; contracted embedding is abstract only','PG-04':'arbitrary-size strict-slack lemma plus accepted same-beta capacity','PG-05':'excludes only one-vertex edge-pair-supported S','PG-RES':'OPEN-PORT; no whole LP exclusion or source existence'},'finite_coverage':json.loads((D/'certificate.json').read_text())['counts'],'source_coverage':'not triggered; no complete N45-U-LP source in this delivery','historical_failures':{'E4_provenance':'inherited; not rerun; historical and BASE E3 hashes differ; original evidence unchanged','fresh_BASE_docs':'exit1; the two old missing paths retained','whole_worktree_DocGraph':'exit1; 62 duplicate IDs retained including all source copies'},'not_run':['upstream E3/E4 enumeration','S/U/SU-J finite full replay','U1-U4','lake build or Lean theorem audit'],'scope_rules':{'no_subagents':True,'no_shared_document_edits':True,'no_source_graph_search':True,'no_k_bound_expansion':True,'no_colouring_replacement_by_minor':True,'no_commit_push_PR_or_external_message':True},'manifest_rule':'MANIFEST.sha256 inventories every regular file beneath this output including the retained BASE checkout and frozen sources, except itself.'}
put('checks.json',checks)
delivery={'task':'N45-PG','executor_status':'complete narrow paper lemma/profile delivery; awaiting independent paper review','BASE':I['BASE'],'actual_source_HEAD':state['source_HEAD'],'delivery_commit':None,'output_root':str(D),'report_sha256':digest(D/'REPORT.md'),'checker_sha256':digest(D/'checker.py'),'certificate_sha256':sha,'inputs_sha256':digest(D/'inputs.json'),'new_paper_findings':['r spokes only U shield endpoints','s spokes only L/S shared endpoint','s contacts cannot attach boundary colours in E_s','one-vertex edge-pair S excluded'],'whole_LP_status':'OPEN','source_realization':'not established','evidence_layers':['arbitrary-size necessary paper topology/strict-slack proofs','finite named templates and local full lifts'],'Lean':'no new theorem or build claim','input_manifest_verification':json.loads(v.stdout),'publication':'none'}
put('delivery.json',delivery)
# Final text/JSON/local paths check now includes the sealed records. Manifest is the only forward path.
t=run('sealed-delivery-text',[sys.executable,'-B',str(D/'validate_payload.py')],R);assert t.returncode==0
# The seal command is saved before the inventory; its observed exit is printed to the tool transcript.
put('logs/seal-command.json',{'argv':[sys.executable,'-B',str(D/'finalize.py')],'cwd':str(R),'completion_evidence':'actual exit and final manifest read-back in the tool transcript; inventory itself is self-excluded'})
files=sorted(p for p in D.rglob('*') if p.is_file() and p.name!='MANIFEST.sha256')
# Keep frozen upstream manifest files in the complete inventory; only this output manifest is self-excluded.
files=sorted(p for p in D.rglob('*') if p.is_file() and p!=D/'MANIFEST.sha256')
b=''.join(digest(p)+'  '+str(p.relative_to(D))+'\n' for p in files).encode();put('MANIFEST.sha256',b)
for p in files:assert digest(p)==next(h for h,rel in (line.split('  ',1) for line in b.decode().splitlines()) if rel==str(p.relative_to(D)))
print(json.dumps({'task':'N45-PG','delivery':'sealed','manifest_entries':len(files),'manifest_sha256':digest(D/'MANIFEST.sha256'),'report_sha256':digest(D/'REPORT.md'),'certificate_sha256':sha,'source_clean':not bool(st.stdout),'whole_LP_status':'OPEN','new_excluded_subtype':'one-vertex edge-pair-supported S'},ensure_ascii=False,indent=2))
