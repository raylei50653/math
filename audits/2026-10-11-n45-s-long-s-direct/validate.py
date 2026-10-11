#!/usr/bin/env python3
"""Verify audit custody and schemas, never prove a graph-source exclusion."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
METADATA = {'delivery.json', 'seal-receipt.json'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def read_json(p):
    return json.loads(p.read_text())

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def contents(input_path):
    inputs = read_json(input_path)
    require(inputs['base'] == BASE, 'wrong BASE')
    require(inputs['baseline_updated'] is False, 'baseline must remain unchanged')
    registered = set()
    for row in inputs['inputs']:
        p = row['path']
        require(p not in registered, 'duplicate input path')
        registered.add(p)
        fp = ROOT / row['frozen_path']
        require(fp.resolve().is_relative_to(ROOT / 'frozen'), 'bad frozen path')
        raw = fp.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == row['sha256'], 'input SHA256 mismatch: '+p)
        require(len(raw) == row['bytes'], 'input length mismatch: '+p)
        blob = subprocess.check_output(['git', 'rev-parse', BASE+':'+p], cwd=REPO, text=True).strip()
        require(blob == row['git_blob'], 'Git blob mismatch: '+p)
        authority = subprocess.check_output(['git', 'show', BASE+':'+p], cwd=REPO)
        require(authority == raw, 'frozen bytes differ from BASE: '+p)
        require((REPO/p).read_bytes() == raw, 'current authority drift: '+p)
    actual_frozen = {p.relative_to(ROOT/'frozen').as_posix()
                     for p in (ROOT/'frozen').rglob('*') if p.is_file()
                     and not p.relative_to(ROOT/'frozen').as_posix().startswith('external/')}
    require(actual_frozen == registered, 'frozen/input inventory mismatch')
    for row in inputs['external_inputs']:
        fp = ROOT/row['path']
        require(row['git_blob'] is None, 'external input must not be called BASE blob')
        require(digest(fp) == row['sha256'] and fp.stat().st_size == row['bytes'],
                'external byte mismatch')
    finding = read_json(ROOT/'findings.json')[0]
    require(finding['id'] == 'SOURCE-ARTIFACT-NOT-IN-BASE', 'finding missing')
    require(finding['git_blob'] is None and finding['used_as_authority'] is False,
            'quarantine artifact cannot become authority')
    require(digest(ROOT/finding['snapshot_path']) == finding['sha256_observed'],
            'quarantine snapshot mismatch')
    q = subprocess.run(['git', 'cat-file', '-e', BASE+':'+finding['path']],
                       cwd=REPO, capture_output=True, text=True)
    require(q.returncode != 0, 'finding inconsistent: rejected blob exists at BASE')
    profiles = read_json(ROOT/'profiles.json')['profiles']
    require([(p['t_s'],p['m_s'],p['n_U']) for p in profiles]
            == [(0,4,1),(0,3,2),(0,2,3),(1,3,1)], 'profile domain/order changed')
    for p in profiles:
        require(p['m_s']+p['n_U']+p['t_s'] == 5, 'bad degree profile')
        require(p['missing_mathematical_sufficient_premises'] == [], 'unreported paper gap')
        source = p['finite_source_control']
        require(source['status'] == 'not triggered' and source['executed'] is False
                and source['source_established'] is False and source['trigger_count'] is None,
                'finite-source execution/count claim is false')
        splits = p['scalar_splits']
        for s in splits:
            require(s['k_L_r']+s['k_S_r'] == s['m_r'] and s['m_r']+s['t_r'] == 5,
                    'bad original r incidence arithmetic')
            require(s['k_L_s']+s['k_S_s'] == p['m_s'], 'bad s split')
            require(min(s[k] for k in ['k_L_r','k_S_r','k_L_s','k_S_s']) >= 1,
                    'nonpositive mixed incidence')
            require(s['S_actual_support_kind'] != 'pair' or (s['t_r'],s['m_r']) == (1,4),
                    'pair PG premise mismatch')
            require(s['S_actual_support_kind'] != 'singleton' or s['k_S_r']+s['k_S_s'] >= 4,
                    'singleton S incidence mismatch')
        require(len({json.dumps(s,sort_keys=True) for s in splits}) == len(splits),
                'duplicate scalar split')
        # Exact whole arithmetic domain, not a source enumeration.
        expected = set()
        for kind in ['pair','singleton']:
            for tr,mr in [(1,4),(2,3)]:
                if kind == 'pair' and tr != 1:
                    continue
                for x in range(1,mr):
                    for y in range(1,p['m_s']):
                        if kind == 'singleton' and x+y < 4:
                            continue
                        expected.add((kind,tr,mr,mr-x,x,p['m_s']-y,y))
        got = {(s['S_actual_support_kind'],s['t_r'],s['m_r'],s['k_L_r'],s['k_S_r'],
                s['k_L_s'],s['k_S_s']) for s in splits}
        require(got == expected, 'missing or extra raw scalar split')
    claims = read_json(ROOT/'claims.json')['claims']
    ids = {c['id'] for c in claims}
    require(len(ids) == len(claims), 'duplicate claim id')
    for c in claims:
        for field in ['quantifier','premises','conclusion_type','conclusion','evidence','unresolved_obligations']:
            require(bool(c[field]), 'empty required claim field '+field)
        require(set(c['dependencies']) <= ids, 'missing dependency')
        for ref in c['evidence']['frozen_references']:
            require((ROOT/ref.split(' ')[0]).is_file(), 'missing frozen evidence '+ref)
    controls = read_json(ROOT/'finite-source-status.json')
    require(controls['finite_algebra_or_graph_controls_executed'] is False,
            'no finite algebra/graph control was run')
    report = (ROOT/'REPORT.md').read_text()
    require('q-position 2' in report and '`01201`' in report, 'q2 mapping missing')
    require('待獨立驗收' in report and 'SOURCE-ARTIFACT-NOT-IN-BASE' in report,
            'scope/finding missing')
    return {'layer':'custody/schema/symbolic-domain integrity only', 'base_inputs':len(registered),
            'claims':len(claims),'profiles':len(profiles),'finite_source_executed':False,
            'no_paper_proof_verified_by_tool':True}

def manifest(path):
    data = read_json(path)
    require(data['base'] == BASE, 'wrong manifest BASE')
    require({r['path'] for r in data['metadata_exclusions']} == METADATA,
            'metadata exclusions must be exact')
    listed = {}
    for row in data['files']:
        require(row['path'] not in listed, 'duplicate payload')
        require(row['path'] not in METADATA, 'metadata cannot hash itself')
        p = ROOT/row['path']
        require(p.resolve().is_relative_to(ROOT) and p.is_file() and not p.is_symlink(),
                'bad payload path')
        require(digest(p) == row['sha256'], 'payload hash mismatch: '+row['path'])
        require(p.stat().st_size == row['bytes'], 'payload byte length mismatch')
        listed[row['path']] = row
    all_files = set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(), 'unexpected symlink')
        if p.is_file():
            all_files.add(p.relative_to(ROOT).as_posix())
    require(all_files-METADATA == set(listed), 'payload inventory mismatch')
    return {'layer':'delivery bytes only','payload_files':len(listed),
            'metadata_exclusions':sorted(METADATA),'finite_source_executed':False}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--contents', action='store_true')
    p.add_argument('--inputs', type=Path, default=ROOT/'inputs.json')
    p.add_argument('--manifest', type=Path)
    args = p.parse_args()
    require(args.contents or args.manifest, 'select check')
    result = {}
    if args.contents:
        result['contents'] = contents(args.inputs)
    if args.manifest:
        result['delivery'] = manifest(args.manifest)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (ValueError,KeyError,FileNotFoundError,json.JSONDecodeError) as e:
        print('REJECTED: '+str(e), file=sys.stderr)
        sys.exit(1)
