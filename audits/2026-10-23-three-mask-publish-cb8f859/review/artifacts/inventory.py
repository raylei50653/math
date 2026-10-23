#!/usr/bin/env python3
"""Read-only Git/source inspection; write proposals only in this review directory."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import stat
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PUBLICATION='audits/2026-10-23-three-mask-publish-cb8f859'
SUFFIXES={'.json','.jsonl','.ndjson','.json5','.bin'}
THRESHOLD=1_000_000


def git(*args):
    return subprocess.run(['git','-C',str(ROOT),*args],capture_output=True,check=True).stdout


def names(*args):
    return [x.decode('utf-8',errors='surrogateescape') for x in git(*args).split(b'\0') if x]


def index_digest():
    p=Path(git('rev-parse','--git-path','index').decode().strip())
    if not p.is_absolute():p=ROOT/p
    return sha256(p.read_bytes()).hexdigest()


def reason(path):
    if '/frozen/' in path:
        return ('Exact frozen 933 authority snapshot retained by the five-round 932/933/941 publication; '
                'preserve sealed bytes and SHA256 for complete-fibre, empty-fibre, full-lift replay and immutable input custody.')
    if '/runs/negative-certificate.json' in path:
        return ('Retained intentionally corrupted second-round 933 certificate with its rejection receipt; '
                'preserve exact historical bytes and SHA256 as negative-control provenance, not as an active mathematical certificate.')
    if 'round3' in path:
        return ('Sealed third-round 933 same-exterior fourteen-completion certificate, including complete ten-row counts, '
                'empty fibres and all original lifts; preserve exact bytes and SHA256 for independent read-only replay.')
    if 'round4' in path:
        return ('Sealed fourth-round 933 genuine-C10 certificate with the complete 70144 cap fibres and whole-component '
                'source obligations; preserve exact bytes and SHA256 for independent read-only replay.')
    if 'round5' in path:
        return ('Sealed fifth-round 933 same-D Hstar certificate with full original Cartesian lifts, complete ten-row '
                'projections and bounded 36-target component tests; preserve exact bytes and SHA256 for independent read-only replay.')
    raise ValueError('unclassified exact frozen exception: '+path)


def inspect():
    before=index_digest()
    base_path=ROOT/PUBLICATION/'BASE.json';base=json.loads(base_path.read_text())
    policy_path=ROOT/'tools/generated_artifact_exceptions.json';policy=json.loads(policy_path.read_text())
    if policy.get('version')!=1 or not isinstance(policy.get('files'),dict):raise ValueError('wrong policy schema')
    frozen={r['path']:r for r in base['audits']}
    if len(frozen)!=738:raise ValueError('publication frozen domain is not 738 files')
    actual={p.relative_to(ROOT).as_posix() for d in base['audit_directories'] for p in (ROOT/d).rglob('*') if p.is_file() or p.is_symlink()}
    missing=sorted(set(frozen)-actual);extra=sorted(actual-set(frozen));drift=[];large=[];other_large=[]
    counts=Counter()
    for path,row in frozen.items():
        p=ROOT/path
        if not p.exists():continue
        mode=p.lstat().st_mode
        if not stat.S_ISREG(mode):raise ValueError('frozen domain unexpectedly contains nonregular file: '+path)
        data=p.read_bytes();digest=sha256(data).hexdigest()
        if len(data)!=row['bytes'] or digest!=row['sha256']:drift.append(path)
        counts[next(d for d in base['audit_directories'] if path.startswith(d+'/'))]+=1
        if row['bytes']>=THRESHOLD:
            (large if p.suffix.lower() in SUFFIXES else other_large).append(dict(row))
    if missing or extra or drift:raise ValueError(json.dumps(dict(missing=missing,extra=extra,drift=drift)))
    additions={}
    for row in sorted(large,key=lambda r:r['path']):
        path=row['path'];record=dict(kind='frozen',reason=reason(path),bytes=row['bytes'],sha256=row['sha256'])
        if path in policy['files'] and policy['files'][path]!=record:raise ValueError('existing exception collides: '+path)
        additions[path]=record
    proposed=json.loads(json.dumps(policy));proposed['files'].update(additions)
    routing=[row['path'] for row in base['routing_entry']]
    stage_prefixes=base['audit_directories']+[PUBLICATION]
    reviewed_unmodified=['docs/HANDOFF.md','README.md']
    stage_files=[p for p in routing if p not in reviewed_unmodified]+[
        'docs/history/2026-10-23-three-mask-five-rounds-publish.md',
        'tools/generated_artifact_exceptions.json']
    within=lambda p:any(p==d or p.startswith(d+'/') for d in stage_prefixes) or p in stage_files
    untracked=names('ls-files','--others','--exclude-standard','-z')
    ignored=names('ls-files','--others','--ignored','--exclude-standard','-z','--',*stage_prefixes)
    cached=names('ls-files','--cached','-z')
    tracked_changes=names('diff','--name-only','-z')
    staged_changes=names('diff','--cached','--name-only','-z')
    five_untracked=[p for p in untracked if p in frozen]
    five_cached=[p for p in cached if p in frozen]
    covered=five_untracked+five_cached+[p for p in ignored if p in frozen]
    if set(covered)!=set(frozen):raise ValueError('some frozen source file missing from Git classification')
    baseline=subprocess.run([sys.executable,'-B',str(ROOT/'tools/check_generated_artifacts.py')],cwd=ROOT,capture_output=True,text=True)
    after=index_digest()
    if before!=after:raise ValueError('Git index changed concurrently during read-only inventory')
    inventory=dict(schema='three-mask-publication-artifact-inventory-v1',base=base['head'],
        publication_BASE_sha256=sha256(base_path.read_bytes()).hexdigest(),
        frozen_domain_files=738,immutable_input_drift=drift,missing_frozen_files=missing,extra_files_under_five_audits=extra,
        per_directory_file_counts=dict(sorted(counts.items())),policy_threshold=THRESHOLD,policy_suffixes=sorted(SUFFIXES),
        policy_relevant_large_files=large,policy_relevant_large_count=len(large),policy_relevant_large_total_bytes=sum(r['bytes'] for r in large),
        other_large_files_not_in_policy_suffix_domain=other_large,
        other_large_suffix_counts=dict(Counter(Path(r['path']).suffix.lower() for r in other_large)),
        existing_policy_entries=len(policy['files']),proposed_policy_entries=len(proposed['files']),
        policy_file_sha256_before=sha256(policy_path.read_bytes()).hexdigest(),
        policy_change_required_only_in='tools/generated_artifact_exceptions.json',checker_code_change_required=False,
        git_index_sha256_before=before,git_index_sha256_after=after,git_index_unchanged=True,
        baseline_index_policy=dict(exit=baseline.returncode,stdout=baseline.stdout,stderr=baseline.stderr,
            scope='current index only; proposed six additions remain unstaged and require root post-stage replay'))
    coverage=dict(schema='three-mask-publication-stage-coverage-v1',
        proposed_directory_pathspecs=stage_prefixes,proposed_exact_file_pathspecs=stage_files,
        reviewed_unmodified_routing_not_staged=reviewed_unmodified,
        frozen_files=sorted(frozen),frozen_untracked_nonignored_count=len(five_untracked),
        frozen_already_indexed_count=len(five_cached),ignored_files_under_audits_and_publication=ignored,
        ignored_force_add_paths=ignored,untracked_snapshot_count=len(untracked),
        untracked_outside_proposed_stage_scope=sorted(p for p in untracked if not within(p)),
        tracked_changes_snapshot=tracked_changes,tracked_changes_outside_proposed_stage_scope=[p for p in tracked_changes if not within(p)],
        staged_changes_snapshot=staged_changes,stage_coverage_complete_at_snapshot=all(within(p) for p in untracked+tracked_changes),
        caveat='Publication writers are active; directory pathspec covers later files inside publication. Recheck outside-scope paths immediately before root staging.')
    return inventory,coverage,dict(version=1,files=additions),proposed


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build',action='store_true')
    parser.add_argument('--revision',default='');args=parser.parse_args()
    if args.revision and not args.revision.isalnum():raise ValueError('revision must be alphanumeric')
    suffix='-'+args.revision if args.revision else ''
    inventory,coverage,additions,proposed=inspect()
    if args.build:
        for name,data in [('inventory.json',inventory),('stage-coverage.json',coverage),
                          ('exception-additions.json',additions),('generated_artifact_exceptions.proposed.json',proposed)]:
            target=Path(name);target=target.with_name(target.stem+suffix+target.suffix)
            with (HERE/target).open('x') as f:json.dump(data,f,indent=2);f.write('\n')
        with (HERE/('stage-pathspecs'+suffix+'.paths0')).open('xb') as f:
            for path in coverage['proposed_directory_pathspecs']+coverage['proposed_exact_file_pathspecs']:f.write(path.encode()+b'\0')
    else:
        saved=json.loads((HERE/'exception-additions.json').read_text())
        if saved!=additions:raise ValueError('saved frozen exception proposals differ from live source bytes')
    print(json.dumps(dict(status='PASS',frozen_files=738,immutable_drift=0,
        proposed_frozen_exceptions=len(additions['files']),proposed_total_policy_records=len(proposed['files']),
        ignored_paths=len(coverage['ignored_force_add_paths']),
        outside_stage_scope=coverage['untracked_outside_proposed_stage_scope']+coverage['tracked_changes_outside_proposed_stage_scope'],
        index_unchanged=inventory['git_index_unchanged'],baseline_index_policy_exit=inventory['baseline_index_policy']['exit'])))


if __name__=='__main__':main()
