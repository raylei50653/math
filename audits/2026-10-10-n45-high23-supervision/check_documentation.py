#!/usr/bin/env python3
"""Record actual documentation checks without broadening the research claim."""
import ast
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def local_check():
    paths = list(json.loads((HERE/'documentation-state.json').read_text())['after'])
    paths += [str(p.relative_to(ROOT)) for p in HERE.glob('*.md')]
    for path in paths:
        p = ROOT/path
        # The retained history template uses its actual destination's links.
        link_context = ROOT/'docs/history/2026-10-10-n45-high23-adoption.md' if p == HERE/'history-draft.md' else p
        if p == HERE/'history-draft.md':
            assert p.read_bytes() == link_context.read_bytes(), 'history template/destination mismatch'
        text = p.read_text()
        for number, line in enumerate(text.splitlines(), 1):
            assert line == line.rstrip(), (path, number, 'trailing whitespace')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('https://', 'http://', '#', 'mailto:')):
                continue
            target = target.split('#',1)[0].strip('<>')
            assert (link_context.parent/target).exists(), (path, target, 'missing target')
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text(), filename=str(p))
    print(json.dumps({'current_documents': 6, 'authored_markdown_files': len(paths), 'links_whitespace_and_python_AST': 'holds'}, sort_keys=True))


def run(job):
    name, argv, expected = job
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    start = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    p = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True)
    for channel, data in [('stdout', p.stdout), ('stderr', p.stderr)]:
        with (HERE/'logs'/(name+'.'+channel+'.txt')).open('xb') as f:
            f.write(data)
    return {'name': name, 'command': argv, 'cwd': str(ROOT),
            'environment': {'PYTHONDONTWRITEBYTECODE': '1', 'GIT_OPTIONAL_LOCKS': '0'},
            'start_UTC': start, 'elapsed_seconds': round(time.monotonic()-clock, 3),
            'exit_code': p.returncode, 'expected_exit': expected,
            'stdout': 'logs/'+name+'.stdout.txt', 'stdout_sha256': sha(p.stdout),
            'stderr': 'logs/'+name+'.stderr.txt', 'stderr_sha256': sha(p.stderr)}


def main():
    jobs = [
        ('check-docs', ['python3','-B','scripts/check_docs.py'], 0),
        ('docgraph-docs', ['python3','-B','tools/docgraph','--include','docs/**/*.md','check'], 0),
        ('docgraph-whole', ['python3','-B','tools/docgraph','check'], 1),
        ('git-diff-check', ['git','diff','--check'], 0),
        ('authored-local-check', ['python3','-B',str(HERE/'check_documentation.py'),'--local-only'], 0),
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        executions = list(pool.map(run, jobs))
    whole = next(x for x in executions if x['name'] == 'docgraph-whole')
    # Keep the actual whole-worktree failure; do not remove scratch copies.
    combined = (HERE/whole['stdout']).read_text()+(HERE/whole['stderr']).read_text()
    duplicate = sum('duplicate id' in line.lower() or 'duplicate-id' in line.lower() for line in combined.splitlines())
    result = {'status': 'actual checks recorded', 'executions': executions,
              'whole_docgraph_duplicate_ids': duplicate,
              'new_Lean': False, 'lake_build': 'not run; documentation-only propagation',
              'finite_source': 'not established/not executed',
              'custody': 'immutable named workers/reviewers plus six adopted documents only; outside worktree PASS not claimed'}
    (HERE/'documentation-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'exits': {x['name']: x['exit_code'] for x in executions}, 'whole_duplicate_ids': duplicate}, sort_keys=True))
    assert all(x['exit_code'] == x['expected_exit'] for x in executions)
    assert duplicate == 62


if __name__ == '__main__':
    import sys
    local_check() if '--local-only' in sys.argv else main()
