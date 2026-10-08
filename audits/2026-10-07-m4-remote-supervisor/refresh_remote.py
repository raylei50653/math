#!/usr/bin/env python3
"""Read current GitHub readiness facts; write only a new local evidence directory."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo, output = args.repo.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    records = []

    def call(name, argv):
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        result = subprocess.run(argv, cwd=repo, capture_output=True)
        logs = []
        for stream in ('stdout', 'stderr'):
            raw = getattr(result, stream)
            path = name + '.' + stream + '.log'
            (output / path).write_bytes(raw)
            logs.append({'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
        records.append({'name': name, 'argv': argv, 'started_utc': started,
                        'exit_code': result.returncode, 'logs': logs})
        (output / 'commands.json').write_text(json.dumps(records, indent=2) + '\n')
        assert result.returncode == 0, (name, result.stderr.decode())
        return result.stdout

    query = repo / 'audits/2026-10-07-m4-remote/pr-state-query.json'
    state = json.loads(call('pr-and-policy', ['gh', 'api', 'graphql', '--input', str(query)]))
    assert not state.get('errors'), state.get('errors')
    rules = json.loads(call('effective-main-rules', ['gh', 'api', 'repos/raylei50653/math/rules/branches/main']))
    refs = {}
    for name in ('main', 'integrate-kprime-e3'):
        data = json.loads(call('remote-' + name, ['gh', 'api', 'repos/raylei50653/math/git/ref/heads/' + name]))
        refs[name] = data['object']['sha']
    runs = {}
    for run_id in (37592725527, 37592797376, 37592841563):
        runs[str(run_id)] = json.loads(call('run-' + str(run_id), ['gh', 'api',
            'repos/raylei50653/math/actions/runs/' + str(run_id)]))
    synthetic = 'ca65f8796c6d83296fee2b22a77467d46b37ebec'
    commit = json.loads(call('synthetic-merge', ['gh', 'api', 'repos/raylei50653/math/git/commits/' + synthetic]))
    local = call('local-refs', ['git', 'rev-parse', 'HEAD', 'refs/remotes/origin/integrate-kprime-e3',
                               'refs/remotes/origin/main']).decode().splitlines()
    dirty = call('tracked-status', ['git', 'status', '--porcelain', '--untracked-files=no']).decode()
    repository = state['data']['repository']
    pr = repository['pullRequest']
    assert not pr['reviews']['pageInfo']['hasNextPage']
    assert not pr['reviewThreads']['pageInfo']['hasNextPage']
    result = {'queried_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'pr': pr, 'remote_refs': refs, 'local_refs': local,
              'main_protection': repository['ref']['branchProtectionRule'], 'effective_rules': rules,
              'runs': {key: {field: value.get(field) for field in
                    ('id', 'html_url', 'event', 'head_sha', 'head_branch', 'status', 'conclusion', 'run_attempt')}
                       for key, value in runs.items()},
              'synthetic_merge': {'sha': commit['sha'], 'parents': [p['sha'] for p in commit['parents']],
                                  'tree': commit['tree']['sha']},
              'tracked_status': dirty, 'remote_mutations': False}
    (output / 'state.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
