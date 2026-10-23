#!/usr/bin/env python3
"""Preserve live legacy-guard failures and replay exact originals in a historical tree."""
import datetime,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path
import run as replay

HERE=replay.HERE;REPO=replay.REPO;PUBLISH=replay.PUBLISH
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
FIRST='audits/2026-10-23-three-mask-methods-cb8f859'

def execute(prefix,root,cwd,seed17,historical=False):
    argv=[sys.executable,'-B',str(root)];env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    if seed17:env['PYTHONHASHSEED']='17'
    else:env.pop('PYTHONHASHSEED',None)
    overrides={'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'17' if seed17 else None}
    if historical:
        gitdir=subprocess.check_output(['git','rev-parse','--absolute-git-dir'],cwd=REPO,text=True).strip()
        env['GIT_DIR']=gitdir;env['GIT_WORK_TREE']=str(cwd);overrides.update(GIT_DIR=gitdir,GIT_WORK_TREE=str(cwd))
    print(json.dumps({'event':'started','replay':prefix}),flush=True)
    start=replay.timestamp();clock=time.perf_counter();p=subprocess.run(argv,cwd=cwd,env=env,capture_output=True);elapsed=time.perf_counter()-clock
    for suffix,blob in [('stdout',p.stdout),('stderr',p.stderr)]:
        with (HERE/(prefix+'.'+suffix)).open('xb') as f:f.write(blob)
    result=json.loads(p.stdout) if p.returncode==0 else None
    metadata={'argv':argv,'cwd':str(cwd),'environment_overrides':overrides,'start_utc':start,'end_utc':replay.timestamp(),
              'elapsed_seconds':elapsed,'exit_code':p.returncode,'historical_view':historical,
              'stdout':{'path':prefix+'.stdout','bytes':len(p.stdout),'sha256':replay.sha(p.stdout)},
              'stderr':{'path':prefix+'.stderr','bytes':len(p.stderr),'sha256':replay.sha(p.stderr)},
              'entrypoint_sha256':replay.sha(root.read_bytes())}
    if result is not None:
        replay.require(set(result['branch_results'])=={'932','933','941'} and all(replay.verdict(v) for v in result['branch_results'].values()),'historical root missing branch PASS')
        metadata['returned_controls']=replay.special_fields(result)
    replay.write_json(prefix+'.json',metadata)
    print(json.dumps({'event':'finished','replay':prefix,'exit_code':p.returncode,'elapsed_seconds':round(elapsed,3)}),flush=True)
    return result,metadata

def view_custody(root,base):
    expected={r['path'] for r in base['audits']}
    actual={str(p.relative_to(root)) for dirname in base['audit_directories'] for p in (root/dirname).rglob('*') if p.is_file()}
    replay.require(actual==expected,'historical audit domain mismatch')
    for r in base['audits']:
        b=(root/r['path']).read_bytes();replay.require((len(b),replay.sha(b))==(r['bytes'],r['sha256']),'historical copied audit bytes/SHA')
    return {'status':'PASS','files':len(expected),'bytes':sum(r['bytes'] for r in base['audits']),'all_bytes_and_SHA_match_publication_BASE':True}

def main():
    base_blob=(PUBLISH/'BASE.json').read_bytes();base=json.loads(base_blob)
    normal=json.loads((HERE/'round1-normal.json').read_text());replay.require(normal['exit_code']!=0,'expected retained original live failure')
    _,live_seed=execute('round1-seed17',REPO/FIRST/'check.py',REPO,True)
    replay.require(live_seed['exit_code']!=0,'live seed guard unexpectedly changed during replay')
    for name in ['round1-normal.stderr','round1-seed17.stderr']:
        message=(HERE/name).read_text();replay.require('source authority drift' in message and 'docs/tasks/c5_no4ct_handoff.md' in message,'unexpected original failure')
    original={'status':'FAIL preserved','reason':'legacy ADDITIONAL_INPUTS treats later-edited routing file as immutable exact Git BASE authority',
              'historical_guard_file':'docs/tasks/c5_no4ct_handoff.md','normal_receipt':'round1-normal.json','seed17_receipt':'round1-seed17.json',
              'not_mathematical_input_drift':'publication audit domain/bytes/SHA remain unchanged; later live routing edits cause the guard'}
    replay.write_json('round1-live-guard.json',original)
    tree=Path(tempfile.mkdtemp(prefix='math-three-mask-historical-'));archive_info={};historical={};cleanup={}
    try:
        rows=subprocess.check_output(['git','ls-tree','-r','--long',BASE],cwd=REPO,text=True).splitlines()
        sizes=[int(r.split(None,4)[3]) for r in rows if r.split(None,4)[3].isdigit()]
        archive_argv=['git','archive',BASE];extract_argv=['tar','--extract','--file','-','--directory',str(tree)]
        print(json.dumps({'event':'historical_archive_started','tracked_files':len(sizes),'tracked_bytes':sum(sizes)}),flush=True)
        started=replay.timestamp();clock=time.perf_counter()
        with (HERE/'historical-archive.stderr').open('xb') as ae,(HERE/'historical-extract.stderr').open('xb') as te,(HERE/'historical-extract.stdout').open('xb') as to:
            archive=subprocess.Popen(archive_argv,cwd=REPO,stdout=subprocess.PIPE,stderr=ae)
            extract=subprocess.Popen(extract_argv,cwd=REPO,stdin=archive.stdout,stdout=to,stderr=te)
            archive.stdout.close();extract_code=extract.wait();archive_code=archive.wait()
        elapsed=time.perf_counter()-clock
        archive_info={'archive_argv':archive_argv,'extract_argv':extract_argv,'cwd':str(REPO),'start_utc':started,'end_utc':replay.timestamp(),
                      'elapsed_seconds':elapsed,'archive_exit_code':archive_code,'extract_exit_code':extract_code,'tracked_files':len(sizes),'tracked_bytes':sum(sizes),
                      'binary_archive_stdout':'streamed directly into tar, not saved as a publication artifact','temporary_tree':str(tree)}
        replay.write_json('historical-archive.json',archive_info);replay.require(archive_code==extract_code==0,'historical git archive failed')
        for r in base['audits']:
            blob=(REPO/r['path']).read_bytes();replay.require((len(blob),replay.sha(blob))==(r['bytes'],r['sha256']),'source changed before overlay')
            dest=tree/r['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(blob)
        additional=json.loads((REPO/FIRST/'932/ADDITIONAL_INPUTS.json').read_text());record=additional['inputs'][0]
        historical_doc=(REPO/FIRST/'932'/record['frozen_path']).read_bytes()
        replay.require((len(historical_doc),replay.sha(historical_doc))==(record['bytes'],record['sha256']),'original frozen routing bytes missing/wrong SHA')
        git_blob=subprocess.check_output(['git','show',BASE+':'+record['path']],cwd=REPO)
        replay.require(git_blob==historical_doc,'frozen historical routing not exact original Git BASE')
        (tree/record['path']).write_bytes(historical_doc)
        restored={'path':record['path'],'source_frozen_path':FIRST+'/932/'+record['frozen_path'],'bytes':len(historical_doc),'sha256':replay.sha(historical_doc),
                  'equals_ADDITIONAL_INPUTS_expected_hash':True,'equals_original_Git_BASE_bytes':True,'expected_hash_changed':False,'live_repo_file_changed':False}
        pre=view_custody(tree,base);replay.write_json('historical-view-custody-before.json',{'audit_custody':pre,'restored_routing':restored})
        a,ma=execute('round1-historical-normal',tree/FIRST/'check.py',tree,False,True)
        b,mb=execute('round1-historical-seed17',tree/FIRST/'check.py',tree,True,True)
        replay.require(ma['exit_code']==mb['exit_code']==0,'historical original entrypoint failed')
        comparison={'status':'PASS' if replay.normalize(a)==replay.normalize(b) else 'FAIL','raw_JSON_equal':a==b,
                    'equal_except_explicit_routing_and_seed_metadata':replay.normalize(a)==replay.normalize(b),'actual_differences':replay.differences(a,b),
                    'normal_receipt':'round1-historical-normal.json','seed17_receipt':'round1-historical-seed17.json'}
        replay.write_json('round1-historical-comparison.json',comparison);replay.require(comparison['status']=='PASS','historical normal/seed17 substantive mismatch')
        post=view_custody(tree,base);replay.write_json('historical-view-custody-after.json',{'audit_custody':post,'restored_routing':restored})
        historical={'normal':ma,'seed17':mb,'comparison':comparison,'restored_routing':restored,'audit_custody':post,
                    'checker_modified':False,'mathematical_inputs_modified':False,'historical_expected_hash_weakened':False}
    finally:
        shutil.rmtree(tree);cleanup={'temporary_tree':str(tree),'removed':not tree.exists(),'large_tree_copied_into_publication':False}
        replay.write_json('historical-cleanup.json',cleanup)
    after=replay.source_custody(base);replay.write_json('source-custody-after.json',after)
    before=json.loads((HERE/'source-custody-before.json').read_text());replay.require(before['observed_manifest_sha256']==after['observed_manifest_sha256'],'live source audit bytes changed')
    replay.require((PUBLISH/'BASE.json').read_bytes()==base_blob,'publication BASE changed')
    rounds={}
    for label,_ in replay.ROUNDS[1:]:
        ma=json.loads((HERE/(label+'-normal.json')).read_text());mb=json.loads((HERE/(label+'-seed17.json')).read_text());comparison=json.loads((HERE/(label+'-comparison.json')).read_text())
        replay.require(ma['exit_code']==mb['exit_code']==0 and comparison['status']=='PASS','retained live replay failed')
        rounds[label]={'normal':ma,'seed17':mb,'comparison':comparison}
    summary={'status':'PASS with original live legacy-guard failures preserved','publication_BASE_sha256':replay.sha(base_blob),
             'original_live_root_replays':10,'original_live_successes':8,'original_live_failures':2,'historical_original_root_replays':2,'historical_successes':2,
             'round1_original_live':original,'round1_historical_view':historical,'other_four_rounds_live':rounds,
             'source_custody_before':before,'source_custody_after':after,'historical_archive':archive_info,'temporary_tree_cleanup':cleanup,
             'negative_execution_policy':{'round1_round2':{'932':['--check','--negative'],'933':['--negative'],'941':'all negatives automatic by default; no unsupported flag added'},
                                          'round3_round4_round5':{'932':['--negative'],'933':['--negative'],'941':['--negative']}},
             'all_passing_normal_seed17_substantive_results_equal':True,
             'source_controls':'not triggered as returned by the sealed checkers; successful finite replay is not a general source exclusion',
             'scope':'five sealed root entrypoints only; no external census, source graph enumeration, unrelated tests, Git/index/shared-doc edits',
             'write_boundary':str(HERE.relative_to(REPO)),'external_write_exception':'authorized ephemeral /tmp historical tree, removed after replay',
             'general_932_933_941':'OPEN','actual_smaller_bad':'OPEN','K_infinity':'OPEN','new_Lean':False,'remote_or_commit_claim':False}
    replay.write_json('SUMMARY.json',summary)
    records=[]
    for p in sorted(HERE.rglob('*')):
        if p.is_file():
            blob=p.read_bytes();records.append({'path':str(p.relative_to(HERE)),'bytes':len(blob),'sha256':replay.sha(blob)})
    replay.write_json('MANIFEST.json',{'files':records,'excludes':['MANIFEST.json'],'source_manifest':'source-manifest.json','source_domain_files':738,'source_domain_bytes':sum(r['bytes'] for r in base['audits'])})
    print(json.dumps({'status':summary['status'],'live_successes':8,'preserved_live_failures':2,'historical_successes':2,
                      'source_files':738,'source_bytes':after['actual_bytes'],'source_drift':0,'receipt_files':len(records),'historical_tree_removed':cleanup['removed']}),flush=True)

if __name__=='__main__':main()
