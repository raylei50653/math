#!/usr/bin/env python3
"""Read-only adoption check; read exact sealed bytes from disk or audit archive.

--check checks receipts/custody and rebuilds C6 Kempe rules. --replay additionally
recomputes all 64 shells, literal lifts, and maximal rectangles. --negative
exercises original certificate mutations and the added named-slot coverage guard.
The historical audit remains immutable; only two named adopted live documents
may differ from BASE after adoption.
"""
import argparse
import ast
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = '77fbd5da7ba273f0af7c75175dc08376d2282f46'
SEAL_SHA256 = '9e546e2ba778fed50a0e498a5cc3c87fe940ea097878873d6336a2ca09a996a6'
ADOPTED_DOCUMENTS = {'docs/c5_c8_peeling.md', 'docs/tasks/c5_no4ct_handoff.md'}
ARCHIVE = None
CANDIDATE = 'candidate-original/t1_broad_probe/'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_repo(relative):
    global ARCHIVE
    path = REPO / relative
    if path.is_file():
        return path.read_bytes()
    if ARCHIVE is None:
        ARCHIVE = json.loads((REPO/'audits/ARCHIVE.json').read_text())
    item = ARCHIVE['files'].get(relative)
    if item is None:
        raise FileNotFoundError(relative)
    blob = ARCHIVE['blobs'][item['sha256']]
    packed = (REPO/blob['path']).read_bytes()
    assert len(packed) == blob['bytes'] and sha(packed) == blob['sha256'], relative
    data = gzip.decompress(packed)
    assert len(data) == item['bytes'] and sha(data) == item['sha256'], relative
    return data


def read(relative):
    return read_repo(str((HERE/relative).relative_to(REPO)))


def obj(relative):
    return json.loads(read(relative))


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, HERE/relative)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def normalize(value):
    return json.loads(json.dumps(value))


def validate_slot(records, kind, pair, queries):
    assert len(records) == len(queries)
    assert [r['query'] for r in records] == [q[0] for q in queries]
    for r, (name, e, target) in zip(records, queries):
        assert (r['kind'],r['pair'],r['query'],r['collar'],r['target']) == (kind,pair,name,list(e),target)


def run(replay=False, negative=False):
    seal_bytes = read('SEAL.json')
    assert sha(seal_bytes) == SEAL_SHA256
    seal = json.loads(seal_bytes)
    assert seal['base'] == BASE and len(seal['files']) == 161
    for name, record in seal['files'].items():
        data = read(name)
        assert len(data) == record['bytes'] and sha(data) == record['sha256'], name
    inputs = obj('INPUTS.json')
    assert inputs['base'] == BASE
    live_drift = []
    for item in inputs['inputs']:
        path = item['path']
        data = read('frozen/'+path)
        assert sha(data) == item['sha256']
        base = subprocess.check_output(['git','show',BASE+':'+path],cwd=REPO)
        assert base == data
        if read_repo(path) != data:
            assert path in ADOPTED_DOCUMENTS, ('unapproved live input drift',path)
            live_drift.append({'path':path,'base_sha256':sha(data),'current_sha256':sha(read_repo(path))})
    assert sha(read('frozen/T1_generalization_candidate.zip')) == inputs['candidate_archive']['sha256']
    assert read('frozen/T1_generalization_notes.md') == read(CANDIDATE+'T1_generalization_notes.md')
    manifest = obj(CANDIDATE+'MANIFEST.json')
    assert len(manifest) == 41
    for name, record in manifest.items():
        data = read(CANDIDATE+name)
        assert sha(data) == record['sha256'] and len(data) == record['bytes']
    normal, seeded = obj('replay-normal/REPLAY.json'), obj('replay-seed17/REPLAY.json')
    assert normal['status'] == seeded['status'] == 'PASS'
    hashes = normal['byte_identical_outputs']
    assert hashes == seeded['byte_identical_outputs'] and len(hashes) == 25
    for name, digest in hashes.items():
        for directory in ('replay-normal/','replay-seed17/',CANDIDATE):
            assert sha(read(directory+name)) == digest
    for name in ('certificate.json.gz','summary.json'):
        assert read('finite/'+name) == read('finite/seed17/'+name)
    finite = obj('finite/summary.json')
    assert finite['counts'] == {'cases':32,'maximal_safe_rectangles':512568,'full_lifts_with_named_query_multiplicity':25348}
    comparison = obj('finite/candidate_comparison.json')
    assert comparison['status'] == 'PASS'
    assert comparison['certificate_sha256'] == sha(read('finite/certificate.json.gz'))
    assert obj('VERIFICATION.json')['status'] == 'PASS_FOR_SCOPED_ADOPTION'
    tree = ast.parse(read('frozen/audits/2026-10-13-c8-terminal-s1-d521163/review/independent_transfer.py'))
    queries = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign)
                   and any(isinstance(t,ast.Name) and t.id=='QUERIES' for t in n.targets))
    verifier = module('t1_original_independent',CANDIDATE+'independent_verify.py')
    rules = module('t1_review_rules','review/kempe_controls.py')
    assert queries == verifier.QUERIES
    assert [''.join(map(str,r)) for r in rules.rows] == verifier.R
    assert normalize(rules.rules) == normalize(verifier.OPS)
    controls = rules.control_report()
    assert normalize(controls) == obj('review/kempe_controls.json') and controls['status'] == 'PASS'
    counts = {'cases':0,'rectangles':0,'literal_shell_lifts':0}
    examples = {}
    for kind in ('PINCH','BRIDGE'):
        for pair in range(4):
            data = obj(CANDIDATE+f'twohole_{kind}_{pair}.json')
            assert data['rows'] == verifier.R
            validate_slot(data['records'],kind,pair,queries)
            receipts = obj(CANDIDATE+f'independent_{kind}_{pair}.json')
            full = gzip.decompress(read(CANDIDATE+f'independent_full_lifts_{kind}_{pair}.jsonl.gz')).splitlines()
            assert len(full) == len(receipts['records']) == 8
            examples.setdefault(kind,data['records'][0])
            for record, receipt, packed in zip(data['records'],receipts['records'],full):
                assert receipt['query'] == record['query'] and receipt['kind'] == kind and receipt['pair'] == pair
                assert receipt['target'] == record['target']
                assert receipt['rectangles'] == len(record['rectangles']) == record['intersections']
                assert receipt['shell_full_lifts'] == sum(record['shell_lift_counts'])
                assert receipt['full_lifts_sha256'] == sha(packed)
                assert record['excluded'] and not record['incomplete']
                assert all(not r[4]&512 and r[5]&512 for r in record['rectangles'])
                if replay:
                    actual, actual_full = verifier.check_record(record)
                    assert normalize(actual) == receipt and actual_full == packed
                counts['cases'] += 1
                counts['rectangles'] += receipt['rectangles']
                counts['literal_shell_lifts'] += receipt['shell_full_lifts']
    assert counts == {'cases':64,'rectangles':701020,'literal_shell_lifts':59156}
    rejected = []
    if negative:
        mutations = {
            'matrix':lambda r:r['matrix'][0].__setitem__(0,r['matrix'][0][0]^1),
            'rectangle_missing':lambda r:r['rectangles'].pop(),
            'pruning':lambda r:r['rectangles'][0].__setitem__(2,r['rectangles'][0][2]^1),
            'coverage':lambda r:r['rectangles'][0].__setitem__(4,r['target']),
            'interface_order':lambda r:r['interfaces'][0].reverse(),
            'split_shared_x':lambda r:r['interfaces'][1].__setitem__(0,'split_x'),
            'lift_count':lambda r:r['shell_lift_counts'].__setitem__(0,r['shell_lift_counts'][0]+1),
            'bridge_missing':lambda r:r['edges'].remove(['x','y']),
        }
        for label, mutate in mutations.items():
            record = copy.deepcopy(examples['BRIDGE' if label=='bridge_missing' else 'PINCH'])
            mutate(record)
            try:
                verifier.check_record(record)
            except (AssertionError,KeyError,ValueError):
                rejected.append(label)
            else:
                raise AssertionError(('mutation accepted',label))
        records = obj(CANDIDATE+'twohole_PINCH_0.json')['records']
        for label in ('wrong_kind','wrong_pair','duplicate_query','missing_query'):
            damaged = copy.deepcopy(records)
            if label=='wrong_kind': damaged[0]['kind']='BRIDGE'
            elif label=='wrong_pair': damaged[0]['pair']=1
            elif label=='duplicate_query': damaged[1]=copy.deepcopy(damaged[0])
            else: damaged.pop()
            try:
                validate_slot(damaged,'PINCH',0,queries)
            except AssertionError:
                rejected.append(label)
            else:
                raise AssertionError(('coverage mutation accepted',label))
        assert len(rejected) == 12
    return {'status':'PASS','base':BASE,'sealed_files':len(seal['files']),
            'sealed_bytes_unchanged':True,'source_inputs':len(inputs['inputs']),
            'permitted_adopted_document_drift':sorted(live_drift,key=lambda r:r['path']),'candidate_manifest_files':41,
            'mode':'full independent replay' if replay else 'custody and saved receipts with regenerated Kempe rules',
            'counts':counts,'positive_disk_controls':7,'negative_controls_rejected':rejected,
            'new_Lean_theorem':False,'scope':'T1-CROSSCUT under the adopted no4ct globally minimum source contract'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--replay',action='store_true')
    parser.add_argument('--negative',action='store_true')
    args = parser.parse_args()
    print(json.dumps(run(args.replay,args.negative),sort_keys=True))
