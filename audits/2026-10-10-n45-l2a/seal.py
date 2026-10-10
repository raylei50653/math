#!/usr/bin/env python3
"""Exclusive first seal; run only once. Failed records must remain for a new-version seal."""
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('l2a_integrity', HERE / 'verify.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def write(rel, b):
    p = HERE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as stream:
        stream.write(b)


def js(rel, value):
    write(rel, (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode())


files, links = module.inventory()
assert not links
before = {rel: module.sha(HERE / rel) for rel in files}
write('MANIFEST.sha256', ''.join(before[rel] + '  ' + rel + '\n' for rel in files).encode())
commands = {}
for label in ('normal', 'seed17'):
    env = os.environ.copy()
    if label == 'seed17':
        env['PYTHONHASHSEED'] = '17'
    argv = [sys.executable, '-B', str(HERE / 'verify.py'), '--payload-only']
    proc = subprocess.run(argv, cwd=module.ROOT, env=env, capture_output=True)
    write('seal/' + label + '.stdout.log', proc.stdout)
    write('seal/' + label + '.stderr.log', proc.stderr)
    commands[label] = {'argv': argv, 'cwd': str(module.ROOT), 'phase': 'payload_only_before_receipt',
                       'PYTHONHASHSEED': env.get('PYTHONHASHSEED'), 'exit': proc.returncode,
                       'stdout_sha256': hashlib.sha256(proc.stdout).hexdigest(),
                       'stderr_sha256': hashlib.sha256(proc.stderr).hexdigest()}
js('seal/commands.json', commands)
after = {rel: module.sha(HERE / rel) for rel in module.inventory()[0]}
js('receipt.json', {'commands': commands, 'payload_before': before, 'payload_after': after,
                    'phase': 'Actual payload-only normal/seed17; final full-receipt default replay performed separately'})
assert all(c['exit'] == 0 for c in commands.values()), 'failed actual replay retained; do not overwrite'
assert before == after, 'payload drift retained; do not overwrite'
assert (HERE / 'seal/normal.stdout.log').read_bytes() == (HERE / 'seal/seed17.stdout.log').read_bytes()
js('delivery.json', {'task': 'N45-L2A', 'BASE': module.BASE, 'payload_files': len(files),
                    'manifest_file': 'MANIFEST.sha256', 'manifest_sha256': module.sha(HERE / 'MANIFEST.sha256'),
                    'receipt_bound_metadata': {rel: module.sha(HERE / rel) for rel in sorted(module.META)},
                    'excluded': sorted(module.EXCLUDED),
                    'manifest_scope': 'All regular payload; exact top-level current manifest/delivery plus six explicit receipt-bound metadata excluded. Nested homonyms included.',
                    'symlinks': links, 'decision': 'six full LOW2 claims and separately scoped LOW coverage hold',
                    'sealed_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    'source_control_evaluation': 'not established; not executed; no trigger count',
                    'new_Lean': False, 'commit_push_PR': False, 'peer_judgments_read': False})
print(json.dumps(module.verify(), sort_keys=True))
