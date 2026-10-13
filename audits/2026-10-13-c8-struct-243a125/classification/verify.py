#!/usr/bin/env python3
"""Record normal replay, deterministic regeneration, and CLI negative controls."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
runs = []


def call(args, seed=None):
    env = dict(os.environ)
    if seed is not None:
        env['PYTHONHASHSEED'] = str(seed)
    result = subprocess.run([sys.executable] + list(map(str, args)), env=env,
                            capture_output=True, text=True)
    runs.append(dict(command=[sys.executable] + list(map(str, args)), seed=seed,
                     returncode=result.returncode, stdout=result.stdout, stderr=result.stderr))
    assert result.returncode == 0, result.stderr


call([HERE / 'checker.py'])
call([HERE / 'checker.py'], 17)
call([HERE / 'negative_controls.py'])
call([HERE / 'quotient_checker.py'])
call([HERE / 'quotient_checker.py'], 17)
call([HERE / 'quotient_negative_controls.py'])
with tempfile.TemporaryDirectory(prefix='c8-struct-classification-replay-') as tmp:
    normal = Path(tmp) / 'normal.json'
    seeded = Path(tmp) / 'seed17.json'
    call([HERE / 'generate.py', '--output', normal])
    call([HERE / 'generate.py', '--output', seeded], 17)
    assert normal.read_bytes() == seeded.read_bytes() == (HERE / 'classification.json').read_bytes()
    digest = hashlib.sha256(normal.read_bytes()).hexdigest()
    qnormal = Path(tmp) / 'quotient.normal.json'
    qseeded = Path(tmp) / 'quotient.seed17.json'
    call([HERE / 'quotient.py', '--output', qnormal])
    call([HERE / 'quotient.py', '--output', qseeded], 17)
    assert qnormal.read_bytes() == qseeded.read_bytes() == (HERE / 'quotient.json').read_bytes()
    qdigest = hashlib.sha256(qnormal.read_bytes()).hexdigest()
report = dict(status='PASS', deterministic_byte_replay=True, classification_sha256=digest,
              quotient_sha256=qdigest, runs=runs)
(HERE / 'verification.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
print(json.dumps(dict(status='PASS', deterministic_byte_replay=True,
                     checker_runs=4, negative_controls=11, classification_sha256=digest,
                     quotient_sha256=qdigest), sort_keys=True))
