#!/usr/bin/env python3
"""Full h=3 three-target interface and no-4CT necessary-count replay.

All source inputs are frozen locally. The 70 old transfer/count queries and
fixed-split certificates are independently checked without invoking their
cofacial-quotient colouring conclusion. Newly added 932 queries all fail the
full transfer/Kempe necessary condition. No graph realizability is inferred.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FROZEN = HERE / 'frozen'
JOINT = FROZEN / 'audits/2026-10-13-c8-joint-count-3097ef5'
STRUCT = FROZEN / 'audits/2026-10-13-c8-struct-243a125'
TARGETS = (932, 933, 941)


def canonical(data):
    return json.loads(json.dumps(data))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def custody():
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    for entry in manifest['inputs']:
        p = FROZEN / entry['path']
        assert p.stat().st_size == entry['bytes'], 'frozen input size'
        assert sha(p) == entry['sha256'], 'frozen input hash'
    return dict(base=manifest['base'], frozen_files=len(manifest['inputs']),
                manifest_sha256=sha(HERE / 'INPUTS.json'))


def add_actual_annulus(case, patterns, outer_patterns):
    """Preserve the original named vertices and all literal fibres, even empty."""
    labels, extras = case['boundary_order'], case['extras']
    case['joint_vertex_order'] = [f'b{i}' for i in range(5)] + labels
    case['annulus_faces'] = [[f'b{i}', f'b{(i+1)%5}', f'a{i}'] for i in range(5)]
    for i in range(5):
        fan = [f'a{(i-1)%5}'] + [f'y{i}_{j}' for j in range(1, extras[i]+1)] + [f'a{i}']
        case['annulus_faces'] += [[f'b{i}', u, v] for u,v in zip(fan,fan[1:])]
    assert len(case['annulus_faces']) == 13
    outer_index = {tuple(word): i for i,word in enumerate(outer_patterns)}
    def normalize(word):
        seen = {}
        return tuple(seen.setdefault(c,len(seen)) for c in word)
    fibres = []
    for p, lifts in zip(patterns, case['outer_lifts_for_each_named_inner_row']):
        row = [[] for _ in outer_patterns]
        for b in lifts:
            row[outer_index[normalize(b)]].append(list(b)+list(p))
        fibres.append(row)
    assert len(fibres) == 274 and all(len(row)==10 for row in fibres)
    case['joint_full_lifts_by_inner_index_then_outer_index'] = fibres


def build():
    inputs = custody()
    producer = module('frozen_c8_producer', JOINT / 'interface.py')
    original = producer.build()
    assert canonical(original) == json.loads((JOINT / 'interface.json').read_text()), 'original interface replay'
    independent = module('frozen_independent_interface', JOINT / 'controls/checker.py')
    patterns, outer, nc, independent_cases = independent.reconstruct_interface(canonical(original))
    count_checker = module('frozen_common_counts', JOINT / 'counts/checker.py')
    count_cert = json.loads((JOINT / 'counts/certificate.v2.json').read_text())
    count_summary = count_checker.verify(count_cert, canonical(original))
    assert count_summary == {'excluded_transfer':57, 'excluded_count':3,
                             'necessary_condition_residual':10}
    fixed = module('frozen_fixed_split', STRUCT / 'kempe/checker.py')
    fixed.OLD = JOINT
    ctx = fixed.load_check_cones()
    fixed_cert = json.loads((STRUCT / 'kempe/certificate.json').read_text())
    fixed_result = fixed.verify(fixed_cert, ctx)
    assert fixed_result['queries_excluded'] == 0 and fixed_result['queries_residual'] == 10
    count_queries = {(q['case_id'],q['target']):q for q in count_cert['queries']}
    residuals = {(q['case_id'],q['target']):q for q in fixed_cert['queries']}
    interface = copy.deepcopy(original)
    ledger = []
    for case, independent_case in zip(interface['cases'], independent_cases):
        new = producer.old.prune(case['column_masks'], interface['kempe_obligations'], 932)
        independently = independent.independent_pruning(independent_case['columns'],
                                                        interface['kempe_obligations'], 932)
        assert all(new[k] == v for k,v in independently.items()), '932 independent pruning'
        new['query_id'] = case['id']+'-932'
        new['accepted_preimages'] = {
            str(r):[p for p in range(274) if new['fixed_point']>>p&1 and case['transfer'][r][p]]
            for r in range(10) if 932>>r&1}
        assert new['excluded']
        case['targets'].insert(0,new)
        add_actual_annulus(case, patterns, outer)
        for q in case['targets']:
            target = q['target']
            row = dict(query_id=q['query_id'], case_id=case['id'],target=target,
                       extras=case['extras'],boundary_order=case['boundary_order'],
                       initial_size=q['initial'].bit_count(),fixed_point_size=q['fixed_point'].bit_count(),
                       fixed_point_mask=q['fixed_point'],possible_outer_union=q['possible_outer_union'],
                       accepted_preimages=q['accepted_preimages'])
            if target == 932:
                row.update(status='excluded_transfer',missing_accepted_outer_rows=[
                    r for r in range(10) if target>>r&1 and not q['accepted_preimages'][str(r)]])
                assert row['missing_accepted_outer_rows']
            else:
                prior = count_queries[case['id'], target]
                row['status'] = prior['status']
                row['common_count_query'] = prior
                if row['status'] == 'necessary_condition_residual':
                    row['fixed_split_query'] = residuals[case['id'],target]
                    row['necessary_support_size'] = row['fixed_split_query']['support'].bit_count()
                    row['source_realizability'] = 'OPEN; no actual source supplied'
            ledger.append(row)
    # The old cofacial colouring assertion is deliberately not a finite premise.
    summary = dict(named_collars=35,target_queries=105,new_932_queries=35,
                   new_932_excluded=35,new_932_empty_fixed_points=30,
                   new_932_nonempty_fixed_points_missing_accepted_rows=5,
                   transfer_kempe_exclusions=92,common_count_exclusions=3,
                   total_finite_exclusions=95,necessary_condition_residuals=10,
                   fixed_split_forced_zero_fibres=4,
                   literal_inner_assignments=6564,inner_pattern_coordinates=274,
                   noncrossing_equality_partitions=1430,fixed_split_rows=821,
                   generic_orbit_generators=1552,triangulated_orbit_generators=981)
    assert sum(r['status']=='excluded_transfer' for r in ledger)==92
    assert sum(r['status']=='excluded_count' for r in ledger)==3
    assert sum(r['status']=='necessary_condition_residual' for r in ledger)==10
    assert sum(r['target']==932 and r['fixed_point_size']==0 for r in ledger)==30
    interface['schema'] = 'c8-three-target-no4ct-interface-v1'
    interface['symmetry'] = 'No reduction: all 35 named distributions times 932,933,941.'
    return dict(schema='c8-three-target-no4ct-finite-v1',custody=inputs,summary=summary,
                interface=interface,query_ledger=ledger,
                independent_overlap=dict(old_queries=70,matched=True,
                    literal_transfer_coefficients=35*10*274,
                    old_common_counts=count_summary,fixed_split=fixed_result),
                proof_scope=dict(four_color_theorem_used=False,
                    colouring_existence_from_cofacial_quotient_used=False,
                    count_coefficients='signed equality coefficients; nonnegative actual x and orbit coefficients',
                    graph_source_search=False,actual_target_source_control='not triggered',
                    universal_necessity='conditional on the same actual named triangulated C8 inner source and exact outer target',
                    residual_status='necessary-condition residual; not an actual source, realization, or counterexample',
                    unbounded_three_branches='OPEN',main_proposition='OPEN',lean='not formalized'))


def verify_payload(got, expected):
    assert got == canonical(expected), 'complete certificate mismatch'


def negative_controls(payload):
    mutations = []
    bad = copy.deepcopy(payload);bad['interface']['cases'][0]['transfer'][0][0] += 1
    mutations.append(('changed_literal_transfer_coefficient', bad))
    bad = copy.deepcopy(payload);bad['interface']['cases'][0]['boundary_order'].reverse()
    mutations.append(('mixed_named_inner_order', bad))
    bad = copy.deepcopy(payload)
    nonempty = next(fibre for c in bad['interface']['cases']
                    for row in c['joint_full_lifts_by_inner_index_then_outer_index'] for fibre in row if fibre)
    nonempty.pop();mutations.append(('missing_joint_full_lift',bad))
    bad = copy.deepcopy(payload)
    next(r for r in bad['query_ledger'] if r['status']=='necessary_condition_residual')['fixed_split_query']['counts'][0]='1'
    mutations.append(('changed_full_count_coordinate',bad))
    bad = copy.deepcopy(payload);bad['summary']['necessary_condition_residuals']=0
    mutations.append(('false_total_closure',bad))
    bad = copy.deepcopy(payload)
    next(r for r in bad['query_ledger'] if r['target']==932)['status']='necessary_condition_residual'
    mutations.append(('reversed_932_verdict',bad))
    rejected=[]
    for name,bad in mutations:
        try: verify_payload(bad,payload)
        except AssertionError: rejected.append(name)
        else: raise AssertionError('negative control accepted: '+name)
    return dict(status='PASS',rejected=rejected)


def main():
    parser=argparse.ArgumentParser()
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true')
    parser.add_argument('--negative-controls',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=parser.parse_args()
    payload=build()
    if args.write:
        with args.certificate.open('x') as f:
            json.dump(payload,f,sort_keys=True,separators=(',',':'));f.write('\n')
    else:
        verify_payload(json.loads(args.certificate.read_text()),payload)
    print(json.dumps(dict(status='PASS',**payload['summary']),sort_keys=True))
    if args.negative_controls: print(json.dumps(negative_controls(payload),sort_keys=True))


if __name__=='__main__': main()
