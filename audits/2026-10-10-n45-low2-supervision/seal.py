#!/usr/bin/env python3
"""Seal only this exclusive supervisory directory; never modifies older evidence."""
import json,os,subprocess,sys
from datetime import datetime,timezone
from review import OUT,sha,put,tree
from verify import SEAL_FILES
def payload():
    return {str(p.relative_to(OUT)):sha(p.read_bytes()) for p in sorted(OUT.rglob('*'))
            if p.is_file() and not p.is_symlink() and str(p.relative_to(OUT)) not in {'MANIFEST.sha256','delivery.json'}|SEAL_FILES}
def main():
    manifest=OUT/'MANIFEST.sha256'
    with manifest.open('x') as f:
        for rel,digest in payload().items():f.write(digest+'  '+rel+'\n')
    checks=OUT/'seal-checks';checks.mkdir()
    before=payload();put('seal-checks/payload-before.json',before)
    records=[];outputs={}
    for label,seed in [('normal',None),('seed17','17')]:
        argv=[sys.executable,'-B',str(OUT/'verify.py'),'--payload-only'];env=os.environ.copy()
        if seed:env['PYTHONHASHSEED']=seed
        p=subprocess.run(argv,env=env,capture_output=True)
        for suffix,data in [('stdout.log',p.stdout),('stderr.log',p.stderr)]:
            with (checks/f'{label}.{suffix}').open('xb') as f:f.write(data)
        records.append({'label':label,'argv':argv,'PYTHONHASHSEED':seed,'exit_code':p.returncode,'expected_exit':0})
        outputs[label]=p.stdout
        if p.returncode:raise SystemExit(p.stderr.decode()+f'own {label} exit {p.returncode}')
    data=manifest.read_text();broken='0'*64+data[64:]
    with (checks/'corrupted-manifest.sha256').open('x') as f:f.write(broken)
    argv=[sys.executable,'-B',str(OUT/'verify.py'),'--payload-only','--manifest',str(checks/'corrupted-manifest.sha256')]
    p=subprocess.run(argv,capture_output=True)
    for suffix,data in [('stdout.log',p.stdout),('stderr.log',p.stderr)]:
        with (checks/f'corrupted.{suffix}').open('xb') as f:f.write(data)
    records.append({'label':'corrupted','argv':argv,'exit_code':p.returncode,'expected_exit':2})
    negative=p.returncode==2 and b'manifest digest differs' in p.stderr
    require_equal=outputs['normal']==outputs['seed17']
    assert negative and require_equal
    after=payload();assert before==after
    put('seal-checks/payload-after.json',after)
    put('seal-checks/commands.json',{'commands':records,'normal_seed17_stdout_byte_equal':require_equal,'negative_digest_rejected':negative})
    metadata={str(p.relative_to(OUT)):sha(p.read_bytes()) for p in sorted(checks.rglob('*')) if p.is_file()}
    assert set(metadata)==SEAL_FILES
    put('delivery.json',{'sealed_utc':datetime.now(timezone.utc).isoformat(),'status':'accepted_LOW2_and_scoped_LOW_composition',
                         'manifest_sha256':sha(manifest.read_bytes()),'payload_file_count':len(after),
                         'manifest_scope':'All regular payload; only exact top-level MANIFEST.sha256, delivery.json and ten explicitly bound seal metadata paths excluded; nested homonyms included.',
                         'seal_files':metadata,'paper_proved_by_tool':False,'general_N2_E':'OPEN','commit_push':False})
    p=subprocess.run([sys.executable,'-B',str(OUT/'verify.py')],capture_output=True)
    if p.returncode:raise SystemExit(p.stderr.decode())
    print(p.stdout.decode().strip());print('manifest_sha256='+sha(manifest.read_bytes()))
if __name__=='__main__':main()
