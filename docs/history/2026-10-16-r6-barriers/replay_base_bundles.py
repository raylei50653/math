#!/usr/bin/env python3
"""Replay sealed R6 bundles at their original Git BASE without editing authority.

Run this published script from any directory. It finds the source Git repository
from its own location; use --source-root when running a copy outside the repo.
All output and the temporary detached worktree stay under --output-dir (or a
unique /tmp/math-r6-publish-replay-* directory). The worktree is removed after
checking, while commands, snapshots and logs remain. This checks custody and
syntax/link contracts only; it does not verify the paper proofs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

BASE='c4c3d99c59cfe4f85b3e33f6831da955a8efcbc7'
SLUGS=('joint-zero','cap-barriers','chorded-five')
AUDITS={s:Path(f'audits/2026-10-16-r6-{s}-c4c3d99') for s in SLUGS}
ROUTING=('docs/STATUS.md','docs/c5_kempe_guide.md',
         'docs/c5_c4_triangle_core.md','docs/c5_state_guide.md')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root',type=Path)
    parser.add_argument('--output-dir',type=Path)
    args=parser.parse_args()
    locator=args.source_root.resolve() if args.source_root else Path(__file__).resolve().parent
    source=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=locator,text=True).strip())
    output=args.output_dir.resolve() if args.output_dir else Path(tempfile.mkdtemp(prefix='math-r6-publish-replay-'))
    if output==source or source in output.parents:
        raise ValueError('output directory must be outside the source repository')
    output.mkdir(parents=True,exist_ok=True)
    receipt=output/'baseline-bundle-replay.json'
    if receipt.exists():
        raise FileExistsError(f'refusing existing receipt: {receipt}')
    worktree=output/'baseline-worktree'
    if worktree.exists():
        raise FileExistsError(f'refusing existing worktree: {worktree}')
    records=[]
    copies=[]
    before={str(p.relative_to(source)):digest(p) for d in AUDITS.values()
            for p in (source/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    (output/'source-audit-hashes-before.json').write_text(json.dumps(before,indent=2,sort_keys=True)+'\n')
    def run(name,argv,cwd,expected=0):
        start=time.monotonic()
        result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        (output/(name+'.stdout')).write_text(result.stdout)
        (output/(name+'.stderr')).write_text(result.stderr)
        row=dict(name=name,argv=argv,cwd=str(cwd),returncode=result.returncode,expected_returncode=expected,
                 expected_status_met=result.returncode==expected,duration_seconds=round(time.monotonic()-start,3),
                 environment={'PYTHONDONTWRITEBYTECODE':'1'},stdout=name+'.stdout',stderr=name+'.stderr')
        records.append(row)
        print(json.dumps({k:row[k] for k in ('name','returncode','expected_status_met')}),flush=True)
        if result.returncode!=expected:
            raise RuntimeError(f'{name}: expected {expected}, got {result.returncode}; see {output}')
    added=False
    failure=None
    try:
        run('worktree-add',['git','worktree','add','--detach',str(worktree),BASE],source)
        added=True
        for slug,audit in AUDITS.items():
            shutil.copytree(source/audit,worktree/audit,ignore=shutil.ignore_patterns('__pycache__'))
            copies.append(dict(operation='copy audit without __pycache__',source=str(audit),target=str(audit)))
        for name in ROUTING:
            src=source/name
            shutil.copyfile(src,worktree/name)
            copies.append(dict(operation='copy live routing',source=name,target=name,sha256=digest(src)))
        for slug in ('cap-barriers','chorded-five'):
            run(slug+'-bundle-at-base',[sys.executable,'-B',str(AUDITS[slug]/'check_bundle.py')],worktree)
        routing=json.loads((source/AUDITS['joint-zero']/'MANIFEST.json').read_text())['routing_files']
        if set(routing)!=set(ROUTING):
            raise ValueError('unexpected JOINT sealed routing membership')
        for name,sha256 in routing.items():
            candidates=[source/AUDITS[s]/'frozen'/name for s in ('cap-barriers','chorded-five')]
            match=next((p for p in candidates if p.is_file() and digest(p)==sha256),None)
            if match is None:
                raise ValueError(f'no later frozen snapshot matches JOINT routing seal: {name}')
            shutil.copyfile(match,worktree/name)
            snapshot=output/'joint-routing-snapshots'/name
            snapshot.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(match,snapshot)
            copies.append(dict(operation='restore JOINT sealed routing',source=str(match.relative_to(source)),target=name,sha256=sha256))
        run('joint-zero-bundle-at-base',[sys.executable,'-B',str(AUDITS['joint-zero']/'check_bundle.py')],worktree)
    except BaseException as error:
        failure=f'{type(error).__name__}: {error}'
    finally:
        if added:
            try:
                run('worktree-remove',['git','worktree','remove','--force',str(worktree)],source)
            except BaseException as error:
                failure=(failure+'; ' if failure else '')+f'cleanup {type(error).__name__}: {error}'
        after={str(p.relative_to(source)):digest(p) for d in AUDITS.values()
               for p in (source/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        (output/'source-audit-hashes-after.json').write_text(json.dumps(after,indent=2,sort_keys=True)+'\n')
        if before!=after:
            failure=(failure+'; ' if failure else '')+'source audit membership or bytes changed'
        summary=dict(source_repository=str(source),source_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip(),
                     base=BASE,output_directory=str(output),copies=copies,runs=records,source_audit_files=len(before),
                     source_audit_bytes_unchanged=before==after,failure=failure,result='PASS' if failure is None else 'FAIL',
                     mathematical_proof_verified=False)
        receipt.write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps({'result':summary['result'],'receipt':str(receipt),'source_audit_bytes_unchanged':before==after,'failure':failure}),flush=True)
    return 0 if failure is None else 1


if __name__=='__main__':
    raise SystemExit(main())
