#!/usr/bin/env python3
"""Create the exact connected publication inventory and deduplicated archive."""
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
PART=24_000_000


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def write(name,data):
    with (HERE/name).open('x') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')


def main():
    scope=json.loads((HERE/'scope.json').read_text())
    legacy=json.loads((ROOT/'audits/ARCHIVE.json').read_text())
    sources={};archived={};all_files={}
    for root in scope['audit_roots']:
        for directory,dirs,names in os.walk(ROOT/root,followlinks=False):
            dirs[:]=sorted(d for d in dirs if d not in {'__pycache__','.lake'} and not (Path(directory)/d).is_symlink())
            link_dirs=[p for p in Path(directory).iterdir() if p.is_symlink() and p.is_dir()]
            for p in sorted([Path(directory)/n for n in names if not n.endswith('.pyc')]+link_dirs):
                relative=p.relative_to(ROOT).as_posix()
                if relative in all_files:continue
                record={'mode':stat.S_IMODE(p.lstat().st_mode)}
                if p.is_symlink():record.update(kind='symlink',target=os.readlink(p))
                else:record.update(kind='regular',bytes=p.stat().st_size,sha256=digest(p))
                all_files[relative]=record
                source=any(relative.startswith(prefix+'/') for prefix in scope['source_prefixes'])
                frozen=any(part in {'frozen','snapshot','.snapshot'} for part in p.relative_to(ROOT).parts)
                whitespace=False
                if record['kind']=='regular' and not (source or frozen or record['bytes']>=1_000_000):
                    try:
                        text=p.read_text();whitespace=text.endswith('\n\n') or any(line.rstrip()!=line for line in text.splitlines())
                    except UnicodeError:pass
                reason='source-copy' if source else 'frozen-copy' if frozen else 'large' if record.get('bytes',0)>=1_000_000 else 'original-whitespace' if whitespace else 'non-Git-mode' if record['kind']=='regular' and record['mode'] not in {0o644,0o755} else None
                if reason:
                    archived[relative]={**record,'reason':reason}
                    if record['kind']=='regular':sources.setdefault(record['sha256'],p)
    def compress(item):
        sha,source=item
        if sha in legacy['blobs']:
            old=legacy['blobs'][sha];path=ROOT/old['path']
            assert digest(path)==old['sha256'] and path.stat().st_size==old['bytes']
            return sha,{'raw_bytes':source.stat().st_size,'compressed_sha256':old['sha256'],'compressed_bytes':old['bytes'],'parts':[old],'reused_legacy_blob':True}
        folder=ROOT/'audits/.archive/n45-2026-10-10';folder.mkdir(parents=True,exist_ok=True)
        fd,temp=tempfile.mkstemp(prefix='.gzip-',dir=folder);os.close(fd);temporary=Path(temp)
        try:
            with source.open('rb') as incoming,temporary.open('wb') as outgoing:
                with gzip.GzipFile(filename='',mode='wb',fileobj=outgoing,mtime=0,compresslevel=6) as stream:shutil.copyfileobj(incoming,stream,1<<20)
            compressed_sha=digest(temporary);compressed_size=temporary.stat().st_size;parts=[]
            with temporary.open('rb') as f:
                number=0
                while block:=f.read(PART):
                    target=folder/(sha+'.gz.part'+str(number).zfill(4))
                    with target.open('xb') as out:out.write(block)
                    parts.append({'path':target.relative_to(ROOT).as_posix(),'bytes':len(block),'sha256':hashlib.sha256(block).hexdigest()});number+=1
            return sha,{'raw_bytes':source.stat().st_size,'compressed_sha256':compressed_sha,'compressed_bytes':compressed_size,'parts':parts,'reused_legacy_blob':False}
        finally:temporary.unlink(missing_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:blobs=dict(pool.map(compress,sorted(sources.items())))
    write('archive.json',{'schema':1,'BASE':scope['BASE'],'description':'Exact immutable payload; Git stores deduplicated gzip parts and literal symlink records. Originals are retained unchanged. Restore before replay.', 'files':dict(sorted(archived.items())),'blobs':dict(sorted(blobs.items()))})
    current={p:{'bytes':(ROOT/p).stat().st_size,'mode':stat.S_IMODE((ROOT/p).stat().st_mode),'sha256':digest(ROOT/p)} for p in scope['current_documents']+scope['historical_docs']}
    write('inputs.json',{'BASE':scope['BASE'],'audit_roots':scope['audit_roots'],'files':dict(sorted(all_files.items())),'current_and_historical_documents':current,'HIGH23_fulltree':'audits/2026-10-10-n45-high23-supervision','source_prefixes':scope['source_prefixes']})
    outside=[p for p in archived if not any(p.startswith(prefix+'/') for prefix in scope['source_prefixes'])]
    ignore=ROOT/'.gitignore';original=ignore.read_text();begin='# BEGIN N45 publication archive: restore with python3 audits/2026-10-10-n45-publication/archive.py restore'
    assert begin not in original
    ignore.write_text(original.rstrip()+'\n\n'+begin+'\n'+''.join('/'+p+'/\n' for p in scope['source_prefixes'])+''.join('/'+p+'\n' for p in sorted(outside))+'# END N45 publication archive\n')
    summary={'audit_roots':len(scope['audit_roots']),'original_files':len(all_files),'archived_paths':len(archived),'archived_symlinks':sum(x['kind']=='symlink' for x in archived.values()),'unique_blobs':len(blobs),'new_blobs':sum(not x['reused_legacy_blob'] for x in blobs.values()),'raw_bytes':sum(x.get('bytes',0) for x in archived.values()),'new_compressed_bytes':sum(x['compressed_bytes'] for x in blobs.values() if not x['reused_legacy_blob']),'largest_new_part':max(p['bytes'] for x in blobs.values() if not x['reused_legacy_blob'] for p in x['parts'])}
    write('archive-summary.json',summary);print(json.dumps(summary,sort_keys=True))


if __name__=='__main__':main()
