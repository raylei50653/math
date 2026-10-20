#!/usr/bin/env python3
"""Replay positives and reject changed integer orbit entries/multiplicities."""
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse,gzip,json,subprocess,sys
D=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--record',action='store_true');args=ap.parse_args()
records=[]
def run(name,argv,expected):
    ans=subprocess.run(argv,text=True,capture_output=True)
    assert (ans.returncode==0)==expected,(name,ans.stdout,ans.stderr)
    records.append({'name':name,'returncode':ans.returncode,'expected_success':expected,
                    'last_stdout_line':ans.stdout.strip().splitlines()[-1] if ans.stdout.strip() else '',
                    'last_stderr_line':ans.stderr.strip().splitlines()[-1] if ans.stderr.strip() else ''})
run('full caps',[sys.executable,'-B',str(D/'check.py')],True)
run('full orbit deterministic replay',[sys.executable,'-B',str(D/'orbits.py')],True)
run('direct tensor negative example replay',[sys.executable,'-B',str(D/'tensor_control.py')],True)
with TemporaryDirectory(prefix='negative-',dir=D) as td:
    td=Path(td)
    meta=json.loads((D/'orbits.json').read_text());meta['coefficients_per_row']=5
    path=td/'multiplicity.json';path.write_text(json.dumps(meta))
    run('changed orbit entry multiplicity 4 to 5',[sys.executable,'-B',str(D/'orbits.py'),'--certificate',str(path)],False)
    data=json.load(gzip.open(D/'orbits.json.gz','rt'));data['columns'][0][0]+=1
    path=td/'column.json.gz'
    with gzip.open(path,'wt') as out:json.dump(data,out)
    run('changed one encoded half-row in a column',[sys.executable,'-B',str(D/'orbits.py'),'--columns-certificate',str(path)],False)
out={'status':'PASS','checks':records,'source_excluded':False}
if args.record:
    with (D/'checks.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,sort_keys=True))
