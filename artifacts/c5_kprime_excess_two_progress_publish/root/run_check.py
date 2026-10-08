import json
import os
from pathlib import Path
import subprocess
import sys
from time import perf_counter

name, cwd, *argv = sys.argv[1:]
out = Path(__file__).parent
env = os.environ.copy()
env['PYTHONDONTWRITEBYTECODE'] = '1'
start = perf_counter()
with (out / f'{name}.log').open('xb') as log:
    result = subprocess.run(argv, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
record = dict(name=name, cwd=cwd, argv=argv, exit_code=result.returncode,
              wall_seconds=round(perf_counter() - start, 3), log=f'{name}.log')
with (out / f'{name}.json').open('x') as meta:
    json.dump(record, meta, ensure_ascii=False, indent=2)
    meta.write('\n')
print(json.dumps(record), flush=True)
print((out / f'{name}.log').read_text(errors='replace')[-1200:], flush=True)
sys.exit(result.returncode)
