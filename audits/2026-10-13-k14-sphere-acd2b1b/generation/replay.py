#!/usr/bin/env python3
"""Compile frozen plantri; replay both generation paths in a temporary directory."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent.parent
FROZEN = HERE / 'frozen'
source = FROZEN / 'artifacts/c5_excess_two_independent_search/vendor/plantri.c'
plugin = FROZEN / 'audits/2026-10-13-k13-collar-50d5474/generation'
base = json.loads((HERE / 'BASE.json').read_text())
for name, digest in base['sha256'].items():
    assert hashlib.sha256((FROZEN / name).read_bytes()).hexdigest() == digest, name
with tempfile.TemporaryDirectory(prefix='math-k14-replay-') as temp:
    temp = Path(temp)
    for label, flags, mode, target in [
        ('min5', [], '-m5', 'spheres20.pc'),
        ('min4', ['-I' + str(plugin), '-DPLUGIN=min5_filter.c'], '-m4', 'spheres20_from_min4.pc'),
    ]:
        binary = temp / label
        output = temp / target
        subprocess.run(['cc', '-O3', *flags, str(source), '-o', str(binary)], check=True)
        result = subprocess.run([str(binary), mode, '20', str(output)], capture_output=True, check=True)
        assert output.read_bytes() == (HERE / 'generation' / target).read_bytes(), label
        print(result.stderr.decode().strip())
        print('PASS', label, 'planar_code bytes', hashlib.sha256(output.read_bytes()).hexdigest())
