#!/usr/bin/env python3
"""Read-only replay of the connected J1 original W5 partial reduction."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

D = Path(__file__).resolve().parent
COMMANDS = (
    'geometry/check.py',
    'interface/check.py',
    'review/check.py',
    'review/check_interface.py',
    'review/chord_check.py',
    'review/diamond_check.py',
    'replacement/reduction_check.py',
    'review/diamond_reduction_check.py',
    'review/catalog_check.py',
    'replacement/long_case.py',
)


def verify(rows, base):
    for row in rows:
        raw = (base/row['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['sha256'], ('sealed drift', row['path'])
        if 'bytes' in row:
            assert len(raw) == row['bytes'], ('sealed size drift', row['path'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seal', type=Path, default=D/'OUTPUTS.json')
    args = ap.parse_args()
    inputs = json.loads((D/'INPUTS.json').read_text())
    verify(inputs,D/'frozen')
    outputs = json.loads(args.seal.read_text())
    verify(outputs,D)
    results = []
    for relative in COMMANDS:
        run = subprocess.run([sys.executable,'-B',str(D/relative)],capture_output=True,text=True)
        if run.returncode:
            raise RuntimeError(relative+'\n'+run.stdout+run.stderr)
        try:
            result = json.loads(run.stdout)
        except json.JSONDecodeError:
            result = run.stdout
        results.append({'checker':relative,'result':result})
    verify(inputs,D/'frozen')
    verify(outputs,D)
    print(json.dumps({'status':'PASS','frozen_inputs':len(inputs),'sealed_outputs':len(outputs),
                      'results':results,'n5_source_excluded':True,'n_ge_6_induced_C11':'OPEN',
                      'entire_W5_branch_closed':False,'all_J1_J2_closed':False,
                      'new_Lean':False},sort_keys=True))


if __name__ == '__main__':
    main()
