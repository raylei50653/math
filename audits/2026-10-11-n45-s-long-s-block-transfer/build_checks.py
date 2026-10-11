"""Collect retained native evidence without rerunning any finite controls."""
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent

def main():
    logs=HERE/'logs'; commands=[]
    for p in sorted(logs.glob('*.command.json')):
        name=p.name.removesuffix('.command.json')
        result_path=logs/(name+'.result.json')
        if not result_path.exists():
            continue # this collector's still-running native capture is finalized by wrapper
        command=json.loads(p.read_text()); result=json.loads(result_path.read_text())
        expected=128 if name.startswith('missing-') else 1 if 'negative-' in name else 0
        code=result.get('exit_code')
        if code is None:
            code=result.get('exit',result.get('original_exit_code'))
        historical_tool=name.startswith(('direct-agent-','local-review-agent-','transfer-paper-agent-'))
        if code is not None:
            assert code==expected,(name,result)
        else:
            assert historical_tool,(name,'missing native exit')
        commands.append({'name':name,'command':str(p.relative_to(HERE)),
            'result':str(result_path.relative_to(HERE)), 'expected_exit':expected,
            'actual_exit':code,'expected_result_observed':code==expected,
            'capture_method':result.get('capture_method',result.get('capture','native subprocess split streams')),
            'stdout':str((logs/(name+'.stdout')).relative_to(HERE)) if (logs/(name+'.stdout')).exists() else None,
            'stderr':str((logs/(name+'.stderr')).relative_to(HERE)) if (logs/(name+'.stderr')).exists() else None,
            'merged_output':next((str((logs/(name+suffix)).relative_to(HERE)) for suffix in ['.merged-output','.merged-output.txt'] if (logs/(name+suffix)).exists()),None)})
    pairs=[]
    for a,b in [('check-normal','check-seed17'),('direct-normal','direct-seed17')]:
        streams={}
        for suffix in ['stdout','stderr']:
            da=(logs/(a+'.'+suffix)).read_bytes(); db=(logs/(b+'.'+suffix)).read_bytes()
            assert da==db
            streams[suffix]={'byte_equal':True,'sha256':hashlib.sha256(da).hexdigest()}
        pairs.append({'normal':a,'seed17':b,'streams':streams})
    data={'task_id':'N45-S-LONG-S-BLOCK-TRANSFER','status':'待獨立驗收',
        'commands':commands,'normal_seed17':pairs,
        'collector_native_log':'logs/build-checks.*',
        'final_native_log':'logs/seal-final.* (captured after collector; included in delivery manifest)',
        'capture_limitations':['initial agent tool calls retain their actual original capture limitations; merged streams, truncated displayed output or unavailable native exit are explicitly recorded in each historical result; all formal root finite controls use complete split native capture'],
        'negative_certificates_preserved':True,
        'old_controls_reexecuted':False,'target_source':{'executed':False,'trigger_count':None,'status':'not triggered'}}
    mode='x'
    if '--refresh' in sys.argv:
        with (HERE/'checks-initial.json').open('xb') as f:
            f.write((HERE/'checks.json').read_bytes())
        mode='w'
    with (HERE/'checks.json').open(mode) as f:
        json.dump(data,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({'completed_commands':len(commands),'seed17_pairs':len(pairs),'expected_negative_rejections':6},sort_keys=True))

if __name__=='__main__':
    main()
