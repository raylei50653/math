#!/usr/bin/env python3
"""Independent artifact inventories and logged commands; no theorem verification."""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
WORKER = ROOT/'audits/2026-10-10-n45-s-low1'
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
SHARED = ['docs/c5_excess_two_nonadjacent_unit_core45.md', 'docs/c5_kempe_guide.md',
          'docs/STATUS.md', 'docs/c5_phase_b_common_lemmas.md', 'artifacts/c5_excess_two_e4/REPORT.md',
          'docs/history/2026-10-10-n45-ss-adoption.md', 'docs/HANDOFF.md', 'README.md',
          'docs/DOCUMENTATION.md', 'docs/c5_excess_two_root_deletions.md',
          'docs/c5_excess_two_mixed_omission.md', 'docs/c5_research_synthesis.md']
def sha(data): return hashlib.sha256(data).hexdigest()
def put(name, obj):
    path=OUT/name; path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f: json.dump(obj,f,ensure_ascii=False,indent=2,sort_keys=True); f.write('\n')
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
def file_state(p):
    s=p.lstat()
    if stat.S_ISLNK(s.st_mode): return {'kind':'symlink','target':os.readlink(p),'mtime_ns':s.st_mtime_ns}
    if stat.S_ISDIR(s.st_mode): return {'kind':'directory','recursive_hash':False}
    assert stat.S_ISREG(s.st_mode),str(p)
    return {'kind':'file','sha256':sha(p.read_bytes()),'bytes':s.st_size,'mtime_ns':s.st_mtime_ns}
def tree(p):
    return {str(f.relative_to(p)):file_state(f) for f in sorted(p.rglob('*')) if f.is_symlink() or f.is_file()}
def check_manifest(p, filename, exclude):
    lines=(p/filename).read_text().splitlines(); entries={}
    for line in lines:
        digest,rel=line.split('  ',1)
        assert len(digest)==64 and all(c in '0123456789abcdef' for c in digest)
        assert rel not in entries and not Path(rel).is_absolute() and '..' not in Path(rel).parts
        entries[rel]=digest
    actual={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and not f.is_symlink() and not exclude(str(f.relative_to(p)))}
    assert actual==set(entries),(actual-set(entries),set(entries)-actual)
    for rel,digest in entries.items(): assert sha((p/rel).read_bytes())==digest,rel
    return len(entries)
def worker():
    n=check_manifest(WORKER,'MANIFEST.final-v4.sha256',lambda r:r in {'MANIFEST.final-v4.sha256','delivery.json'} or r.startswith('seal-final-v4/'))
    d=json.loads((WORKER/'delivery.json').read_text())
    assert sha((WORKER/'MANIFEST.final-v4.sha256').read_bytes())==d['manifest_sha256']
    actual={str(p.relative_to(WORKER)) for p in (WORKER/'seal-final-v4').rglob('*') if p.is_file()}
    assert actual==set(d['seal_files'])
    for rel,digest in d['seal_files'].items(): assert sha((WORKER/rel).read_bytes())==digest,rel
    links={str(p.relative_to(WORKER)):os.readlink(p) for p in WORKER.rglob('*') if p.is_symlink()}
    assert links==json.loads((WORKER/'symlinks.json').read_text())
    inputs=json.loads((WORKER/'inputs-initial.json').read_text())['pins']
    for r in inputs:
        assert r['actual']==r['expected'] and r['matches']
        assert sha((WORKER/'frozen/current'/r['path']).read_bytes())==r['expected']
    base=json.loads((WORKER/'base-inputs.json').read_text())['inputs']
    for r in base:
        blob=git('show',BASE+':'+r['path'])
        assert sha(blob)==r['sha256']
        assert git('rev-parse',BASE+':'+r['path']).decode().strip()==r['git_blob']
        assert (WORKER/'base-source'/r['path']).read_bytes()==blob
    return {'payload_files':n,'payload_symlinks':len(links),'receipt_bound_metadata_files':len(actual),
            'BASE_inputs':len(base),'frozen_current_pins':len(inputs),'paper_proved_by_this_tool':False}
def freeze():
    assert git('rev-parse','HEAD').decode().strip()==BASE
    checked=worker(); outside={}
    for raw in git('ls-files','--cached','--others','--exclude-standard','-z').split(b'\0'):
        if not raw:continue
        rel=raw.decode(); p=ROOT/rel
        if p.is_relative_to(OUT):continue
        outside[rel]=file_state(p) if p.exists() or p.is_symlink() else {'kind':'missing'}
    put('inputs-before.json',{'BASE':BASE,'worker':tree(WORKER),'existing':outside,
                             'git_status':git('status','--short').decode(),'checks':checked})
    put('shared-before.json',{r:(ROOT/r).read_text() for r in SHARED})
    print(json.dumps(checked,sort_keys=True))
def log(label,argv,seed=False):
    env=os.environ.copy()
    if seed:env['PYTHONHASHSEED']='17'
    p=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True)
    for suffix,data in [('stdout.log',p.stdout),('stderr.log',p.stderr)]:
        path=OUT/'logs'/f'{label}.{suffix}'; path.parent.mkdir(exist_ok=True)
        with path.open('xb') as f:f.write(data)
    put(f'logs/{label}.json',{'argv':argv,'cwd':str(ROOT),'exit_code':p.returncode,'PYTHONHASHSEED':'17' if seed else None})
    print(json.dumps({'label':label,'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)}))
    return p.returncode
if __name__=='__main__':
    if sys.argv[1:]==['freeze']:freeze()
    elif sys.argv[1]=='run':
        label=sys.argv[2];argv=sys.argv[3:];seed=argv[:1]==['--seed17']
        if seed:argv=argv[1:]
        sys.exit(log(label,argv,seed))
    elif sys.argv[1:]==['worker']:print(json.dumps(worker(),sort_keys=True))
    else:raise SystemExit('expected freeze, worker or run LABEL [--seed17] COMMAND...')
