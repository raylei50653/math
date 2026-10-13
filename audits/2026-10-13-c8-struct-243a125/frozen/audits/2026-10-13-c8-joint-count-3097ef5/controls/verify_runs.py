#!/usr/bin/env python3
"""Execute deterministic replays and real CLI mutation failures."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CHECKER = HERE/'checker.py'


def run(name, command, expected_success, env=None, expected_error=None):
    started = time.monotonic()
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    assert (result.returncode == 0) == expected_success, (name,result.stdout,result.stderr)
    if expected_error:
        assert expected_error in result.stderr, (name,result.stderr)
    return dict(name=name,command=[str(arg) for arg in command],exit_code=result.returncode,
                expected_success=expected_success,expected_error=expected_error,
                elapsed_seconds=round(time.monotonic()-started,3),
                stdout=result.stdout,stderr=result.stderr)


def main():
    for bytecode in (HERE/'__pycache__').glob('checker.*.pyc'):
        bytecode.unlink()
    if (HERE/'__pycache__').is_dir() and not list((HERE/'__pycache__').iterdir()):
        (HERE/'__pycache__').rmdir()
    seed_certificate = HERE/'control_certificate.seed17.json'
    assert not seed_certificate.exists(), 'seed artifact already exists; do not overwrite'
    assert not (HERE/'verification.json').exists(), 'verification already exists; do not overwrite'
    seed_env = dict(os.environ,PYTHONHASHSEED='17',PYTHONDONTWRITEBYTECODE='1')
    commands = [
        ('normal_check',[sys.executable,str(CHECKER),'--check'],True,None,None),
        ('seed17_write',[sys.executable,str(CHECKER),'--write','--certificate',str(seed_certificate)],True,seed_env,None),
    ]
    with ThreadPoolExecutor(max_workers=2) as pool:
        initial = list(pool.map(lambda args:run(*args), commands))
    normal = (HERE/'control_certificate.json').read_bytes()
    seeded = seed_certificate.read_bytes()
    assert normal == seeded
    data = json.loads((ROOT/'interface.json').read_text())
    mutations = []
    rows = deepcopy(data)
    rows['pattern_order'][0],rows['pattern_order'][1] = rows['pattern_order'][1],rows['pattern_order'][0]
    mutations.append(('swapped_row_labels',rows,'mixed inner row labels',dict(indices=[0,1])))
    weights = deepcopy(data)
    weights['orbit_sizes'][0] = 24
    mutations.append(('uniform_orbit_weight',weights,'wrong orbit weights',dict(index=0,before=12,after=24)))
    transfer = deepcopy(data)
    transfer['cases'][0]['transfer'][0][0] += 1
    mutations.append(('transfer_coefficient',transfer,'literal transfer coefficient',dict(case='c00',outer=0,inner=0,delta=1)))
    preimages = deepcopy(data)
    selected = next((c,q,r) for c in preimages['cases'] for q in c['targets']
                    for r,ps in q['accepted_preimages'].items() if ps)
    c,q,r = selected
    removed = q['accepted_preimages'][r].pop()
    mutations.append(('omitted_accepted_preimage',preimages,'missing necessary accepted preimage',
                      dict(query=q['query_id'],outer=int(r),removed_inner=removed)))
    results = []
    with tempfile.TemporaryDirectory(prefix='negative-inputs-',dir=HERE) as temp:
        commands = []
        for name,mutant,error,recipe in mutations:
            path = Path(temp)/(name+'.json')
            raw = (json.dumps(mutant,sort_keys=True,separators=(',',':'))+'\n').encode()
            path.write_bytes(raw)
            command = [sys.executable,str(CHECKER),'--check','--interface',str(path)]
            commands.append((name,command,False,None,error))
            results.append(dict(name=name,mutation=recipe,mutated_interface_sha256=sha256(raw).hexdigest()))
        with ThreadPoolExecutor(max_workers=2) as pool:
            executions = list(pool.map(lambda args:run(*args), commands))
        for record,execution in zip(results,executions):
            record.update(execution)
    payload = dict(status='PASS',normal_and_seed17_byte_identical=True,
                   normal_certificate_sha256=sha256(normal).hexdigest(),
                   seed17_certificate_sha256=sha256(seeded).hexdigest(),
                   initial_replays=initial,actual_cli_negative_controls=results,
                   negative_input_retention='Temporary mutated inputs removed after exact bytes hash, mutation recipe and complete rejection output were recorded. No baseline or certificate was altered.')
    with (HERE/'verification.json').open('x') as stream:
        json.dump(payload,stream,indent=2,sort_keys=True)
        stream.write('\n')
    print(json.dumps(dict(status='PASS',byte_identical=True,actual_negative_controls=len(results),
                          certificate_sha256=sha256(normal).hexdigest()),sort_keys=True))


if __name__ == '__main__':
    main()
