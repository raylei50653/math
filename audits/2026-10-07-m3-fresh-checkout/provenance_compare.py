#!/usr/bin/env python3
"""Keep historical byte failures and compare only explicitly named leaves."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path('/tmp/math-m3-ba0b447')
OUT = Path(__file__).resolve().parent
REVIEW = 'a484d4cdaeb069702de0c40acf83bc6a05dea3b3'
CANDIDATE = 'ba0b447f09617591d9f2ba81c988f537af771791'
sys.path.insert(0, str(ROOT / 'scripts'))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def inventory(path):
    raw = path.read_bytes()
    return dict(bytes=len(raw), sha256=digest(raw))


def diff(saved, current, path=''):
    if type(saved) is not type(current):
        return [dict(path=path, saved=saved, current=current)]
    if isinstance(saved, dict):
        result = []
        for key in sorted(saved.keys() | current.keys()):
            if key not in saved or key not in current:
                result.append(dict(path=path+'/'+key, saved=saved.get(key), current=current.get(key)))
            else:
                result.extend(diff(saved[key], current[key], path+'/'+key))
        return result
    if isinstance(saved, list):
        if len(saved) != len(current):
            return [dict(path=path, saved_length=len(saved), current_length=len(current))]
        return [item for i,(left,right) in enumerate(zip(saved,current)) for item in diff(left,right,path+'/'+str(i))]
    return [] if saved == current else [dict(path=path, saved=saved, current=current)]


def git_bytes(ref, path):
    return subprocess.run(['git','show',ref+':'+path], cwd=ROOT, check=True, capture_output=True).stdout


def main():
    # This producer has no output argument; invoke its unchanged build function.
    script = ROOT / 'scripts/c5_excess_two_e5_branches.py'
    spec = importlib.util.spec_from_file_location('m3_e5_branches', script)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    raw = (json.dumps(module.build(),sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    with (OUT/'provenance/e5_branches.json').open('xb') as stream:
        stream.write(raw)
    specs = [
        ('E4_reductions','artifacts/c5_excess_two_e4/reductions.json','provenance/e4_reductions.json',
         {'/sources/artifacts/c5_excess_two_e3/REPORT.md/bytes','/sources/artifacts/c5_excess_two_e3/REPORT.md/sha256'},'historical byte FAIL remains FAIL'),
        ('E5_controls','artifacts/c5_excess_two_e5/controls.json','provenance/e5_controls.json',
         {'/source_sha256/artifacts/c5_excess_two_e3/REPORT.md'},'historical byte FAIL remains FAIL'),
        ('E4C','artifacts/c5_excess_two_e4c/summary.json','provenance/e4c/summary.json',
         {'/source_hashes/docs/c5_kempe_guide.md'},'historical byte FAIL remains FAIL; current guide hash changes its named provenance leaf'),
        ('E5_branches','artifacts/c5_excess_two_e5/branches.json','provenance/e5_branches.json',
         {'/sources_sha256/docs/c5_excess_two_mixed_core_spokes.md'},'new strict byte FAIL from a changed document input, recorded separately from the three historical failures'),
    ]
    comparisons = []
    for name, source, fresh, allowed, status in specs:
        differences = diff(json.loads((ROOT/source).read_bytes()),json.loads((OUT/fresh).read_bytes()))
        observed = {d['path'] for d in differences}
        entry = dict(name=name, source=source, fresh=fresh, source_inventory=inventory(ROOT/source),
                     fresh_inventory=inventory(OUT/fresh), differences=differences,
                     allowed_leaf_paths=sorted(allowed), exact_leaf_allowlist_match=observed==allowed,
                     mathematical_payload_equal=observed==allowed, strict_byte_status='FAIL', status=status)
        comparisons.append(entry)
        assert entry['exact_leaf_allowlist_match'], (name, differences)
    fresh_control_paths = sorted((OUT/'provenance/e4c/controls').glob('*.json'))
    saved_control_paths = sorted((ROOT/'artifacts/c5_excess_two_e4c/controls').glob('*.json'))
    assert [p.name for p in fresh_control_paths] == [p.name for p in saved_control_paths]
    control_records = [dict(path='controls/'+left.name, saved=inventory(left), fresh=inventory(right),
                            byte_equal=left.read_bytes()==right.read_bytes())
                       for left,right in zip(saved_control_paths,fresh_control_paths)]
    assert len(control_records)==54 and all(r['byte_equal'] for r in control_records)

    # Compare the entire raw check output and list exact path/line exceptions.
    import gzip
    historical = gzip.decompress((ROOT/'artifacts/c5_integrate_branch_review/logs/branch_whitespace.log.gz').read_bytes())
    current = (OUT/'logs/provenance_branch_whitespace.stdout.log').read_bytes()
    historical_diags = [dict(path=m[1],line=int(m[2]),message=m[3]) for line in historical.decode().splitlines()
                        if (m:=re.match(r'^(.+):(\d+): (.+)$',line))]
    current_diags = [dict(path=m[1],line=int(m[2]),message=m[3]) for line in current.decode().splitlines()
                     if (m:=re.match(r'^(.+):(\d+): (.+)$',line))]
    paths = sorted({d['path'] for d in current_diags})
    source_bytes = []
    for path in paths:
        prior = git_bytes(REVIEW,path); candidate = git_bytes(CANDIDATE,path)
        source_bytes.append(dict(path=path,review=dict(bytes=len(prior),sha256=digest(prior)),
                                 candidate=dict(bytes=len(candidate),sha256=digest(candidate)),byte_equal=prior==candidate))
    assert all(r['byte_equal'] for r in source_bytes)
    assert len(historical_diags)==86 and current==historical
    whitespace = dict(base_sha='2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090', candidate_sha=CANDIDATE,
                      historical_raw=dict(bytes=len(historical),sha256=digest(historical)),
                      current_raw=dict(bytes=len(current),sha256=digest(current)),
                      historical_count=len(historical_diags),current_count=len(current_diags),
                      exact_raw_equal=current==historical,new_diagnostics=[],resolved_diagnostics=[],
                      exceptions=current_diags,unchanged_exception_source_bytes=source_bytes,
                      full_branch_exit_code=2,candidate_parent_diff_exit_code=0)
    with (OUT/'whitespace-comparison.json').open('x') as stream:
        json.dump(whitespace,stream,indent=2);stream.write('\n')
    deps = json.loads((OUT/'dependency-inventory-v2.json').read_bytes())
    strict_commands = {name:json.loads((OUT/'commands'/('provenance_'+name+'_strict.json')).read_bytes())
                       for name in ('e4_reductions','e5_controls','e4c_controls','e5_branches')}
    historical_review = json.loads((ROOT/'artifacts/c5_integrate_branch_review/semantic_comparison.json').read_bytes())
    result = dict(candidate_sha=CANDIDATE,reference_review_sha=REVIEW,
                  dependency_inventory='dependency-inventory-v2.json',
                  initial_inventory_note='dependency-inventory.json was a conservative first pass including the whole D8 delivery metadata. v2 narrows D8 to its actual checker/certificate and static helper closure; both fresh outputs are retained.',
                  dependency_files=deps['files'],dependency_equal_to_review=deps['equal_to_review'],
                  dependency_changes=deps['changed'],missing_review_reference=deps['missing_review_reference'],
                  groups=deps['groups'],strict_commands=strict_commands,
                  historical_review_leaf_comparison=historical_review,comparisons=comparisons,
                  e4c_control_bytes_equal=54,e4c_control_inventory=control_records,
                  new_finding=dict(id='M3-PROV-E5-BRANCHES',classification='document provenance only; strict byte replay FAIL',
                      path='/sources_sha256/docs/c5_excess_two_mixed_core_spokes.md',
                      trigger='candidate changed a document that the unchanged E5 branch checker hashes',
                      required_action='record this candidate-specific exception separately in the merge findings ledger; preserve the original E5 certificate and the Oct05 three-failure record'),
                  whitespace='whitespace-comparison.json',
                  not_rerun=['ES full search and seed17 corpus search','ES acceptance','ER full search and seed17','E3 four ordinary checkers','E4 control','E5 local','E6 three ordinary checkers','Kprime','D8'],
                  reuse_reason='Every actual source/checker/corpus hash for these groups equals the Oct05 review hash. This reuses the stated prior finite validation scope only, with no k expansion or paper/Lean/topology claim.',
                  original_source_or_certificate_overwritten=False)
    with (OUT/'provenance-summary.json').open('x') as stream:
        json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(dependency_files=deps['files'],dependency_equal_to_review=deps['equal_to_review'],
                         changed=[r['path'] for r in deps['changed']],comparisons=[dict(name=c['name'],leaves=c['differences'],payload_equal=c['mathematical_payload_equal'],strict_byte_status=c['strict_byte_status']) for c in comparisons],
                         e4c_controls_byte_equal=54,whitespace_diagnostics=86,whitespace_raw_equal=True),indent=2))


if __name__=='__main__':
    main()
