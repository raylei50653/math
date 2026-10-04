#!/usr/bin/env python3
"""Compare source and snapshot to the pre-audit manifest without writing either."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();baseline=json.loads(args.baseline.read_text())
    result={'checked_utc':datetime.now(timezone.utc).isoformat(),'baseline_head':baseline['head'],
            'baseline_time_utc':baseline['time_utc'],'monitored_baseline_file_count':len(baseline['files'])}
    for label in ('snapshot','source'):
        root=Path(baseline[label]);changes=[]
        for rel,record in baseline['files'].items():
            p=root/rel
            current=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
            if current!=record['sha256']:
                changes.append(dict(path=rel,baseline_sha256=record['sha256'],current_sha256=current))
        result[label+'_baseline_file_differences']=changes
        paths={str(p.relative_to(root)) for name in ('scripts','docs','tools','artifacts')
               for p in (root/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        result[label+'_added_monitored_paths']=sorted(paths-set(baseline['files']))
    result['source_current_head']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=baseline['source'],text=True).strip()
    result['source_current_git_status']=subprocess.check_output(['git','status','--short'],cwd=baseline['source'],text=True)
    diff=subprocess.run(['git','diff','--check'],cwd=baseline['source'],capture_output=True,text=True)
    result['source_git_diff_check']={'returncode':diff.returncode,'stdout':diff.stdout,'stderr':diff.stderr}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_current_git_status'},ensure_ascii=False,sort_keys=True))

if __name__=='__main__':main()
