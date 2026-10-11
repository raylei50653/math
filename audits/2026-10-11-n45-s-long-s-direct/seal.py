#!/usr/bin/env python3
"""Prepare check summary or exclusively seal payload and capture final verification."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
META = ['delivery.json', 'seal-receipt.json']

def read(p):
    return json.loads((ROOT/p).read_text())

def write_new(p, obj):
    with (ROOT/p).open('x') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def prepare():
    n = read('logs/contents-normal.json')
    s = read('logs/contents-seed17.json')
    ni = read('logs/negative-inputs.json')
    nm = read('logs/negative-manifest.json')
    assert n['exit_code'] == s['exit_code'] == 0
    assert n['stdout'] == s['stdout'] and n['stderr'] == s['stderr'] == ''
    assert ni['exit_code'] == nm['exit_code'] == 1
    assert ni['expected_exit_matched'] and nm['expected_exit_matched']
    assert 'input SHA256 mismatch' in ni['stderr']
    assert 'payload hash mismatch' in nm['stderr']
    assert read('logs/external-text.json')['exit_code'] == 0
    mismatch = read('SOURCE-MISMATCH-additional.json')
    assert mismatch['exit_code'] == 128
    summary = {
        'task_id':'N45-S-LONG-S-DIRECT',
        'layer':'delivery integrity checks, not graph-source/paper/Lean validation',
        'normal_seed17_stdout_stderr_byte_equal':True,
        'checks':[
            {'id':'contents-normal','status':'triggered and holds','exit_code':0,
             'log':'logs/contents-normal.json'},
            {'id':'contents-seed17','status':'triggered and holds','exit_code':0,
             'log':'logs/contents-seed17.json'},
            {'id':'corrupted-input-hash-negative','status':'triggered and holds',
             'actual_exit_code':1,'expected_exit_code':1,'log':'logs/negative-inputs.json'},
            {'id':'corrupted-payload-hash-negative','status':'triggered and holds',
             'actual_exit_code':1,'expected_exit_code':1,'log':'logs/negative-manifest.json'}],
        'retained_setup_failure':{'finding':'SOURCE-ARTIFACT-NOT-IN-BASE',
                                  'git_exit_code':128,'log':'logs/freeze-additional.json'},
        'finite_source':{'status':'not triggered','established':False,'executed':False,
                         'trigger_count':None},
        'source_exclusion_proved_by_tool':False,
        'lean_executed':False,
        'adoption_status':'pending independent acceptance'
    }
    write_new('checks.json', summary)
    print(json.dumps({'check_summary_created':True,'normal_seed17_equal':True,
                      'negative_controls_expected_rejection':True,'finite_source_executed':False}))

def seal():
    if any((ROOT/p).exists() for p in META):
        raise ValueError('refuse to overwrite delivery metadata')
    inventory=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_symlink():
            raise ValueError('unexpected symlink')
        if p.is_file() and p.relative_to(ROOT).as_posix() not in META:
            inventory.append({'path':p.relative_to(ROOT).as_posix(),
                              'sha256':sha(p),'bytes':p.stat().st_size})
    delivery={
        'task_id':'N45-S-LONG-S-DIRECT','base':BASE,
        'acceptance_status':'pending independent acceptance',
        'files':inventory,
        'metadata_exclusions':[
            {'path':'delivery.json','reason':'Manifest self-reference; SHA256 separately bound in seal-receipt.json.'},
            {'path':'seal-receipt.json','reason':'Records post-manifest actual verification commands/streams/exit; metadata, not mathematical payload.'}],
        'metadata_exclusions_are_exact_paths':True,
        'quarantine_is_in_payload':True,
        'finite_source_established_or_executed':False,
        'source_finding':'SOURCE-ARTIFACT-NOT-IN-BASE'
    }
    write_new('delivery.json',delivery)
    results=[]
    for seed in [None,'17']:
        command=['python3','-B','validate.py','--contents','--manifest','delivery.json']
        env=os.environ.copy()
        if seed is not None:
            env['PYTHONHASHSEED']=seed
        began=datetime.datetime.now(datetime.timezone.utc).isoformat()
        r=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True)
        results.append({'command':command,'cwd':str(ROOT),
                        'environment_override':{} if seed is None else {'PYTHONHASHSEED':seed},
                        'started_utc':began,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        'stdout':r.stdout,'stderr':r.stderr,'exit_code':r.returncode})
    equal=results[0]['stdout']==results[1]['stdout'] and results[0]['stderr']==results[1]['stderr']
    success=all(r['exit_code']==0 for r in results) and equal
    summary={'payload_files':len(inventory),'all_final_checks_hold':success,
             'normal_seed17_streams_byte_equal':equal,'finite_source_executed':False,
             'delivery_sha256':sha(ROOT/'delivery.json')}
    write_new('seal-receipt.json',{
        'task_id':'N45-S-LONG-S-DIRECT','base':BASE,
        'generation_command':['python3','-B','seal.py','--seal'],
        'checks':results,'summary':summary,
        'excluded_metadata_exact_paths':META,
        'independent_acceptance':False,
        'no_paper_source_or_lean_proof_by_this_receipt':True})
    print(json.dumps(summary,sort_keys=True))
    return 0 if success else 1

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--prepare',action='store_true')
    p.add_argument('--seal',action='store_true')
    a=p.parse_args()
    if a.prepare == a.seal:
        p.error('select exactly one operation')
    if a.prepare:
        prepare()
        return 0
    return seal()

if __name__=='__main__':
    try:
        sys.exit(main())
    except (ValueError,AssertionError,FileExistsError) as e:
        print('REJECTED: '+str(e),file=sys.stderr)
        sys.exit(1)
