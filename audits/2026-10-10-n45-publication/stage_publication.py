#!/usr/bin/env python3
"""Stage only the connected declared bundle, excluding archived raw originals."""
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


def main():
    scope=json.loads((HERE/'scope.json').read_text())
    paths=['.gitignore',*scope['current_documents'],*scope['historical_docs'],
           'docs/history/2026-10-10-n45-progress-publish.md',*scope['audit_roots'],
           str(HERE.relative_to(ROOT)),'audits/.archive/n45-2026-10-10']
    subprocess.run(['git','add','--',*paths],cwd=ROOT,check=True)
    added=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).split(b'\0')
    staged=[p.decode() for p in added if p]
    modes=subprocess.check_output(['git','ls-files','--stage'],cwd=ROOT).decode().splitlines()
    assert not any(s.startswith('160000 ') for s in modes),'Git gitlink would omit immutable payload'
    with (HERE/'staged-paths-initial.json').open('x') as f:json.dump({'explicit_whitelist':paths,'staged_paths':staged,'gitlinks':0},f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({'staged_paths':len(staged),'gitlinks':0},sort_keys=True))


if __name__=='__main__':main()
