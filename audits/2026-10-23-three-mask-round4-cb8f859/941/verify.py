#!/usr/bin/env python3
"""Store independent-process replays, corruption rejection, and immutable drift."""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def write_new(path, data):
    with path.open('xb') as stream:
        stream.write(data)


def run(name, arguments, seed17=False, expected=0):
    env = dict(os.environ)
    if seed17:
        env['PYTHONHASHSEED'] = '17'
    command = [sys.executable,'-B']+(['-O'] if seed17 else [])+[str(HERE/'check.py')]+arguments
    result = subprocess.run(command,cwd=ROOT,env=env,capture_output=True)
    write_new(HERE/'runs'/(name+'.stdout'),result.stdout)
    write_new(HERE/'runs'/(name+'.stderr'),result.stderr)
    if result.returncode!=expected:
        raise ValueError(f'{name}: expected exit {expected}, got {result.returncode}')
    return dict(command=command,exit=result.returncode,stdout_sha256=sha256(result.stdout).hexdigest(),
                result=json.loads(result.stdout))


def main():
    (HERE/'runs').mkdir(exist_ok=True)
    normal = run('normal',[])
    seed17 = run('seed17',['--seed','17'],True)
    n,s = deepcopy(normal['result']),deepcopy(seed17['result'])
    n.pop('seed'); s.pop('seed')
    if n!=s:
        raise ValueError('normal/seed17 independent-process results differ')
    semantic = run('semantic-negative',['--negative'])
    cert = json.loads((HERE/'certificate.json').read_text())
    cert['source_rows'][0]['branch_implication']['canonical_Z'].update(in_actual_successor_Q=False)
    negative = HERE/'runs'/'negative-certificate.json'
    write_new(negative,(json.dumps(cert,sort_keys=True,separators=(',',':'))+'\n').encode())
    external = run('external-negative',['--certificate',str(negative)],expected=1)
    malformed = HERE/'runs'/'malformed-certificate.json'
    write_new(malformed,b'{"schema":"941-round4-certificate-v1"}\n')
    malformed_result = run('malformed-negative',['--certificate',str(malformed)],expected=1)
    # Recheck all source bytes after the independent processes.
    manifest = json.loads((HERE/'INPUTS.json').read_text())
    drift = []
    for row in manifest['inputs']:
        data = (ROOT/row['path']).read_bytes()
        if len(data)!=row['bytes'] or sha256(data).hexdigest()!=row['sha256']:
            drift.append(row['path'])
    if drift:
        raise ValueError('immutable post-run drift: '+repr(drift))
    verification = dict(status='PASS',normal=normal,seed17=seed17,
        normal_seed17_equal_except_seed=True,semantic_negative=semantic,
        semantic_negative_count=len(semantic['result']['semantic_negatives']),
        external_corrupt_certificate=external,malformed_certificate=malformed_result,
        immutable_input_drift=drift,routing_drift_is_separate=True,
        source_realizability='not triggered',new_pair_exclusions=0)
    write_new(HERE/'VERIFICATION.json',(json.dumps(verification,indent=2,sort_keys=True)+'\n').encode())
    print(json.dumps(dict(status='PASS',normal_seed17_equal=True,
        semantic_negatives=verification['semantic_negative_count'],external_negatives=2,immutable_input_drift=0)))


if __name__=='__main__':
    main()
