#!/usr/bin/env python3
"""Exclusive BASE capture. Missing blobs are findings, never replacements."""
import hashlib
import json
from pathlib import Path
import subprocess

BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(data)

def dump(path, data):
    write(path, (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)+'\n').encode())

def run(name, argv, env=None):
    p = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True)
    write(OUT/'logs'/f'{name}.stdout', p.stdout)
    write(OUT/'logs'/f'{name}.stderr', p.stderr)
    dump(OUT/'logs'/f'{name}.json', {'argv':argv,'cwd':str(ROOT),'exit':p.returncode,
         'stdout':f'logs/{name}.stdout','stderr':f'logs/{name}.stderr'})
    return p

if __name__ == '__main__':
    paths = ['docs/HANDOFF.md','docs/STATUS.md',
        'audits/2026-10-10-n45-s-long-contract/REPORT.md',
        'audits/2026-10-10-n45-s-long-r-map/REPORT.md',
        'audits/2026-10-09-n45-s/REPORT.md',
        'artifacts/c5_excess_one_e2/REPORT.md',
        'artifacts/c5_single_spoke_two_two/observations.json',
        'artifacts/c5_single_spoke_residual_locality/support_table.md',
        'scripts/c5_single_spoke_residual_locality.py']
    names = '''excess_two_nonadjacent_unit_core45 degree5_interfaces degree5_tree_components
single_spoke_two_two single_spoke_residual_locality single_spoke_first_bridge
single_spoke_two_arc single_spoke_cross_row single_spoke_frame_arc
single_spoke_two_two_minor single_spoke_two_two_external single_spoke_bridge_path
single_spoke_branch_palettes single_spoke_two_contact_bounds single_spoke_cores
single_spoke_four single_spoke_three_one degree5_two_spoke_sectors
two_spoke_adjacent_21 two_spoke_middle_21 two_spoke_nonadjacent two_spoke_reflection
two_spoke_split_support root_degree_excess excess_rejection_law k4_blocks
multi_odd_cycles unary_shield_budget phase_b_common_lemmas'''.split()
    paths += [f'docs/c5_{n}.md' for n in names]
    control_dir = 'audits/2026-10-10-n45-s-long-contract/frozen/artifacts/c5_excess_two_e4c/controls'
    ls = run('control-inventory', ['git','ls-tree','-r','--name-only',BASE,control_dir])
    paths += ls.stdout.decode().splitlines()
    head = run('head', ['git','rev-parse','HEAD']).stdout.decode().strip()
    run('status-before-capture',['git','status','--short','--untracked-files=all'])
    entries=[]
    for i,path in enumerate(sorted(set(paths))):
        p=run(f'input-{i:03}', ['git','show',f'{BASE}:{path}'])
        if p.returncode:
            raise RuntimeError(f'authority mismatch: {path}; retained failure, stop')
        blob=run(f'blob-{i:03}', ['git','rev-parse',f'{BASE}:{path}']).stdout.decode().strip()
        live=(ROOT/path).read_bytes()
        if live != p.stdout:
            raise RuntimeError(f'worktree does not match BASE: {path}')
        frozen='frozen/'+path
        write(OUT/frozen,p.stdout)
        entries.append({'path':path,'base':BASE,'git_blob':blob,
           'sha256':hashlib.sha256(p.stdout).hexdigest(),'bytes':len(p.stdout),
           'frozen_path':frozen,'worktree_matches_base':True,'kind':'BASE Git blob'})
    missing='artifacts/c5_single_spoke_residual_locality/observations.json'
    p=run('missing-final-json',['git','show',f'{BASE}:{missing}'])
    assert p.returncode != 0
    physical=ROOT/missing
    finding={'id':'BASE-FINAL-JSON-MISSING','path':missing,'git_blob':None,
       'base':BASE,'exit':p.returncode,'on_disk':physical.exists(),
       'authority_admitted':False,'replacement_used':False,
       'physical_sha256':hashlib.sha256(physical.read_bytes()).hexdigest() if physical.exists() else None,
       'physical_read_note':'Root exploratory read preceded Git admission check; excluded from every claim and control.',
       'consequence':'No BASE final JSON replay; use BASE paper reports and tracked final support_table only.'}
    dump(OUT/'source-findings.json',[finding])
    dump(OUT/'inputs.json',{'task_id':'N45-S-LONG-S-FIBRE','base':BASE,'head_observed':head,
       'entries':entries,'non_authoritative_findings':'source-findings.json',
       'external_dependencies':[{'url':'https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf',
         'name':'Dvorak, List coloring and Gallai trees, Lemma 7 and Theorem 10',
         'git_blob':None,'evidence_layer':'external theorem; live primary PDF read on 2026-10-11'}]})
    print(f'Frozen {len(entries)} BASE inputs; missing final JSON retained as finding.')
