#!/usr/bin/env python3
"""Check new archive records and task links; optionally hydrate missing doc inputs.
Existing archive records and existing files are never replaced.
"""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import unquote,urlsplit
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='50d5474f2446403f3b3001d5943571184c8c9936'
def sha(b):return hashlib.sha256(b).hexdigest()
def module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def hydrate():
    data=json.loads((ROOT/'audits/ARCHIVE.json').read_text()); done=[]
    def primary(rel):
        record=data['files'][rel];compressed=(ROOT/data['blobs'][record['sha256']]['path']).read_bytes()
        assert sha(compressed)==data['blobs'][record['sha256']]['sha256']
        raw=gzip.decompress(compressed);assert sha(raw)==record['sha256'] and len(raw)==record['bytes']
        return record,raw
    def save(rel,record,raw):
        path=ROOT/rel;path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():assert path.read_bytes()==raw
        else:
            with path.open('xb') as f:f.write(raw)
            path.chmod(record['mode'])
        done.append({'path':rel,'sha256':sha(raw),'bytes':len(raw)})
    bootstrap='audits/2026-10-10-n45-publication/archive.json'
    if not (ROOT/bootstrap).exists():save(bootstrap,*primary(bootstrap))
    n45=json.loads((ROOT/bootstrap).read_text());helper=module(ROOT/'audits/2026-10-10-n45-publication/archive.py','n45archive')
    needed=set()
    for line in (HERE/'logs/docs.log').read_text().splitlines():
        match=re.match(r'missing path: (.*?):\d+: (.*)$',line)
        if match:
            path=((ROOT/match[1]).parent/match[2]).resolve();assert path.is_relative_to(ROOT);needed.add(str(path.relative_to(ROOT)))
    for rel in sorted(needed):
        if rel in data['files']:record,raw=primary(rel)
        else:
            record=n45['files'][rel];assert record['kind']=='regular'
            blob=n45['blobs'][record['sha256']]
            for part in blob['parts']:
                b=(ROOT/part['path']).read_bytes();assert len(b)==part['bytes'] and sha(b)==part['sha256']
            with helper.uncompressed(ROOT,blob) as f:raw=f.read()
            assert len(raw)==record['bytes'] and sha(raw)==record['sha256']
        save(rel,record,raw)
    with (HERE/'logs/docs-hydration.json').open('x') as f:json.dump({'restored_or_verified':done},f,indent=2);f.write('\n')
    print('Hydrated',len(done),'exact archived paths')

def check():
    old=json.loads(subprocess.check_output(['git','show',BASE+':audits/ARCHIVE.json'],cwd=ROOT))
    new=json.loads((ROOT/'audits/ARCHIVE.json').read_text())
    for kind in ('files','blobs'):
        assert all(new[kind].get(k)==v for k,v in old[kind].items()),'old archive mutation'
    added=set(new['files'])-set(old['files'])
    expected=json.loads((HERE/'ARCHIVE_ADDITIONS.json').read_text())
    assert added==set(expected) and all(new['files'][k]==v for k,v in expected.items())
    assert all(k.startswith(str(HERE.relative_to(ROOT))+'/') for k in added)
    with tempfile.TemporaryDirectory(prefix='k13-archive-restore-') as tmp:
        for rel in added:
            r=new['files'][rel]; b=new['blobs'][r['sha256']]; compressed=(ROOT/b['path']).read_bytes()
            assert len(compressed)==b['bytes'] and sha(compressed)==b['sha256']
            raw=gzip.decompress(compressed);assert len(raw)==r['bytes'] and sha(raw)==r['sha256']
            assert raw==(ROOT/rel).read_bytes()
            dst=Path(tmp)/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
            assert sha(dst.read_bytes())==r['sha256']
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    for rel,digest in inputs['sha256'].items():assert sha((HERE/'frozen'/rel).read_bytes())==digest
    docs=module(ROOT/'scripts/check_docs.py','doccheck');count=0;errors=[]
    files=[p for p in HERE.rglob('*.md') if 'frozen' not in p.relative_to(HERE).parts]
    for p in files:
        for line,target in docs.links(p.read_text()):
            url=urlsplit(target)
            if url.scheme or url.netloc:continue
            q=(p.parent/unquote(url.path)).resolve() if url.path else p
            count+=1
            if not q.exists():errors.append(f'{p.name}:{line}: missing {target}')
            elif url.fragment and q.suffix=='.md' and unquote(url.fragment) not in docs.anchors(q.read_text()):errors.append(f'{p.name}:{line}: anchor {target}')
    assert not errors,'\n'.join(errors)
    print(json.dumps({'old_archive_records_unchanged':True,'new_paths_restored_byte_exact':len(added),
        'new_unique_blobs':len(set(new['blobs'])-set(old['blobs'])),'frozen_hashes':'pass','audit_links_checked':count,'audit_markdown_files':len(files)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--hydrate-doc-inputs',action='store_true');a=p.parse_args()
    hydrate() if a.hydrate_doc_inputs else check()
