#!/usr/bin/env python3
"""Reconstruct every imported original from the actual Git index, then replay."""
import gzip,hashlib,json,os,subprocess,sys,tempfile,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

entries={}
for entry in subprocess.check_output(['git','ls-files','--stage','-z'],cwd=ROOT).split(b'\0'):
    if not entry: continue
    meta,name=entry.split(b'\t',1); mode,oid,stage=meta.decode().split()
    assert stage=='0', name
    entries[name.decode()]={'mode':mode,'oid':oid}
reader=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
cache={}
def indexed(name):
    oid=entries[name]['oid']
    if oid not in cache:
        reader.stdin.write((oid+'\n').encode()); reader.stdin.flush()
        header=reader.stdout.readline().decode().split(); assert header[1]=='blob',name
        cache[oid]=reader.stdout.read(int(header[2])); assert reader.stdout.read(1)==b'\n'
    return cache[oid]

imported=json.loads(indexed(str(HERE.relative_to(ROOT)/'IMPORTED.json')))
archive=json.loads(indexed('audits/ARCHIVE.json'))
restored=0
with tempfile.TemporaryDirectory(prefix='math-k15-c8-index-') as target:
    target=Path(target)
    for name,row in imported['files'].items():
        if name in entries:
            raw=indexed(name)
            assert entries[name]['mode']==('100755' if row['mode']&0o111 else '100644'),name
        else:
            frozen=archive['files'][name]
            assert all(frozen[k]==row[k] for k in ('sha256','bytes','mode')),name
            blob=archive['blobs'][row['sha256']]; packed=indexed(blob['path'])
            assert len(packed)==blob['bytes'] and sha(packed)==blob['sha256'],name
            raw=gzip.decompress(packed); restored+=1
        assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],name
        path=target/name; path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(raw); path.chmod(row['mode'])
    checks=[]
    commands=[] if "--custody-only" in sys.argv else [
        ('k15',['python3','-B','audits/2026-10-13-k15-sphere-6cafdfb/check.py','--check']),
        ('no4ct-c8',['python3','-B','audits/2026-10-13-c5-no4ct-c8-6cafdfb/verify.py','--check','--negative']),
        ('w5-construction',['python3','-B','audits/2026-10-13-w5-small-representatives-6cafdfb/construction/check.py','--check']),
    ]
    for label,cmd in commands:
        env=os.environ.copy(); env['PYTHONPATH']='/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f'; env['PYTHONDONTWRITEBYTECODE']='1'
        start=time.monotonic(); proc=subprocess.run(cmd,cwd=target,env=env,capture_output=True,text=True)
        (HERE/'validation'/('index-'+label+'.log')).write_text(proc.stdout+proc.stderr)
        checks.append({'name':label,'command':cmd,'exit_code':proc.returncode,'log':'validation/index-'+label+'.log','elapsed_seconds':round(time.monotonic()-start,3)})
        assert proc.returncode==0,(label,proc.stdout,proc.stderr)
reader.stdin.close(); reader.wait()
result={'status':'PASS','index_imported_files':len(imported['files']),'restored_from_archive':restored,'checks':checks}
(HERE/('validation/index-custody-results.json' if '--custody-only' in sys.argv else 'validation/index-results.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))
