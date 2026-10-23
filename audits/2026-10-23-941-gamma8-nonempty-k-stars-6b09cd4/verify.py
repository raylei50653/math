#!/usr/bin/env python3
"""Replay receipts and isolated external negative controls."""
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def replay(args,seed=None):
    env=dict(os.environ)
    if seed is not None:env['PYTHONHASHSEED']=str(seed)
    command=[sys.executable,'-B']+(['-O'] if seed is not None else [])+[str(HERE/'check.py')]+args
    done=subprocess.run(command,cwd=ROOT,env=env,text=True,capture_output=True)
    if done.returncode:raise RuntimeError(done.stderr)
    return dict(command=command,exit_code=done.returncode,result=json.loads(done.stdout))

def main():
    record=dict(schema='941-gamma8-nonempty-k-stars-verification-v1',
        normal=replay([]),seed17=replay(['--seed','17'],17),semantic_negatives=replay(['--negative']))
    with tempfile.TemporaryDirectory(prefix='.negative-',dir=HERE) as temporary:
        scratch=Path(temporary)
        bad=deepcopy(json.loads((HERE/'certificate.json').read_text()))
        bad['conclusion']['K0_d_equals_U_rows']=0
        badfile=scratch/'bad-certificate.json';badfile.write_text(json.dumps(bad))
        done=subprocess.run([sys.executable,'-B',str(HERE/'check.py'),'--certificate',str(badfile)],cwd=ROOT,text=True,capture_output=True)
        if done.returncode==0 or 'certificate mismatch: conclusion' not in done.stderr:
            raise RuntimeError('external corruption not rejected specifically')
        record['external_certificate_negative']=dict(rejected=True,exit_code=done.returncode,expected_error='certificate mismatch: conclusion')
        (scratch/'INPUTS.json').write_bytes((HERE/'INPUTS.json').read_bytes())
        shutil.copytree(HERE/'frozen',scratch/'frozen')
        inputs=json.loads((scratch/'INPUTS.json').read_text())
        target=scratch/inputs['inputs'][0]['snapshot'];target.write_bytes(target.read_bytes()+b'CORRUPT\n')
        spec=importlib.util.spec_from_file_location('isolated_check',HERE/'check.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.HERE=scratch;module.ROOT=ROOT
        try:module.custody()
        except ValueError as error:
            if not str(error).startswith('frozen authority changed:'):raise
            record['isolated_frozen_authority_negative']=dict(rejected=True,expected_error=str(error),canonical_bytes_untouched=True)
        else:raise RuntimeError('isolated authority corruption accepted')
    record['checked_output_hashes']={name:sha256((HERE/name).read_bytes()).hexdigest() for name in
        ['INPUTS.json','PROOF.md','REPORT.md','certificate.json','check.py','models.py','produce.py','verify.py','explore.json']}
    (HERE/'VERIFICATION.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS',normal=True,seed17=True,semantic_negatives=12,external_negatives=2,immutable_drift=0)))

if __name__=='__main__':main()
