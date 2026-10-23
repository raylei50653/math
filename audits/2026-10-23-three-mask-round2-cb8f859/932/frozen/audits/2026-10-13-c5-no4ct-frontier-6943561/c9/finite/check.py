#!/usr/bin/env python3
"""Named h=4 annulus interface; conditional necessary screen, never a source search."""
import argparse
from collections import Counter
import copy
import gzip
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
OLD = AUDIT / 'frozen/audits/2026-10-13-c8-joint-count-3097ef5/frozen/audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/collar_checker.py'
spec = importlib.util.spec_from_file_location('frozen_generic_collar', OLD)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
TARGETS = (932, 933, 941)


def canonical(value):
    return json.loads(json.dumps(value))


def custody():
    data = json.loads((AUDIT / 'INPUTS.json').read_text())
    for entry in data['inputs']:
        payload = (AUDIT / 'frozen' / entry['path']).read_bytes()
        assert len(payload) == entry['bytes'], entry['path']
        assert hashlib.sha256(payload).hexdigest() == entry['sha256'], entry['path']
    return data['base']


def nc_partitions():
    result = []
    for blocks in old.partitions(tuple(range(9))):
        owners = {v: j for j, block in enumerate(blocks) for v in block}
        if any(owners[a] == owners[c] and owners[b] == owners[d]
               and owners[a] != owners[b] for a,b,c,d in combinations(range(9), 4)):
            continue
        if any(owners[i] == owners[(i+1)%9] for i in range(9)):
            continue
        result.append(old.norm(tuple(owners[i] for i in range(9))))
    return sorted(result)


def prune(columns, obligations, target, geometry_mask):
    allowed = geometry_mask & sum(1 << i for i, col in enumerate(columns)
                                  if not col & ~target)
    initial = allowed
    rounds = []
    while True:
        removals = []
        for p in range(len(columns)):
            if not (allowed >> p & 1):
                continue
            bad = [s for s, opts in enumerate(obligations[p])
                   if all(orbit & ~allowed for orbit in opts)]
            if bad:
                removals.append({'pattern_index':p, 'split_indices':bad})
        if not removals:
            break
        rounds.append({'before':allowed, 'removals':removals})
        allowed &= ~sum(1 << r['pattern_index'] for r in removals)
    union = 0
    for p, col in enumerate(columns):
        if allowed >> p & 1:
            union |= col
    return {'target':target, 'initial':initial, 'rounds':rounds,
            'fixed_point':allowed, 'possible_outer_union':union,
            'excluded_transfer':union != target}


def build():
    base = custody()
    patterns = old.patterns(9)
    assert len(patterns) == 820
    by_colors = Counter(len(set(p)) for p in patterns)
    assert by_colors == {3:85, 4:735}
    obligations = old.kempe_table(9)
    partitions = nc_partitions()
    assert len(partitions) == 232
    quotient_masks = []
    for part in partitions:
        mask = sum(1 << p for p, word in enumerate(patterns)
                   if all(word[a] == word[b] for a in range(9) for b in range(a)
                          if part[a] == part[b]))
        assert mask
        quotient_masks.append(mask)
    cases = []
    ledger = []
    for idx, extras in enumerate(old.compositions(4,5)):
        supports = old.collar_supports(extras)
        labels = []
        for i in range(5):
            labels.append(f'a{i}')
            labels.extend(f'y{(i+1)%5}_{j}' for j in range(1,extras[(i+1)%5]+1))
        assert len(labels) == 9
        columns, lifts = old.columns(extras)
        fibres = []
        for p, words in zip(patterns, lifts):
            row = [[] for _ in old.P5]
            for b in words:
                row[old.I5[old.norm(b)]].append(list(b)+list(p))
            fibres.append(row)
        edges = [[f'b{i}',f'b{(i+1)%5}'] for i in range(5)]
        edges += [[labels[i],labels[(i+1)%9]] for i in range(9)]
        edges += [[f'b{i}',labels[j]] for j,support in enumerate(supports) for i in support]
        faces = [[f'b{i}',f'b{(i+1)%5}',f'a{i}'] for i in range(5)]
        for i in range(5):
            fan = [f'a{(i-1)%5}']+[f'y{i}_{j}' for j in range(1,extras[i]+1)]+[f'a{i}']
            faces += [[f'b{i}',v,u] for u,v in zip(fan,fan[1:])]
        assert len(faces) == 14
        darts = Counter((a,b) for face in faces for a,b in zip(face,face[1:]+face[:1]))
        assert all(count==1 for count in darts.values())
        outer_darts={(f'b{i}',f'b{(i+1)%5}') for i in range(5)}
        inner_darts={(labels[(i+1)%9],labels[i]) for i in range(9)}
        assert {(a,b) for a,b in darts if (b,a) not in darts}==outer_darts|inner_darts
        rotation_paths={}
        for vertex in [f'b{i}' for i in range(5)]+labels:
            after={}
            for face in faces:
                if vertex in face:
                    pos=face.index(vertex);a,b=face[(pos+1)%3],face[(pos+2)%3]
                    assert a not in after
                    after[a]=b
            starts=set(after)-set(after.values())
            assert len(starts)==1
            path=[starts.pop()]
            while path[-1] in after:path.append(after[path[-1]])
            assert len(path)==len(after)+1 and len(path)==len(set(path))
            rotation_paths[vertex]=path
        geometries = [{'id':'induced', 'short_arc':None, 'chord':None,
                       'boundary_mask':(1<<820)-1, 'quotient_indices':list(range(232))}]
        for start in range(9):
            arc = [(start+j)%9 for j in range(5)]
            if not all(labels[j].startswith('a') for j in arc[1:4]):
                continue
            u,v = arc[0],arc[-1]
            mask = sum(1<<p for p,word in enumerate(patterns)
                       if word[u] != word[v] and len({word[j] for j in arc}) == 3)
            quotients = [q for q,part in enumerate(partitions) if part[u] != part[v]]
            geometries.append({'id':f'ear{start}', 'short_arc':arc, 'chord':[u,v],
                               'boundary_mask':mask, 'quotient_indices':quotients})
        for geometry in geometries:
            for target in TARGETS:
                check = prune(columns, obligations, target, geometry['boundary_mask'])
                missing = [q for q in geometry['quotient_indices']
                           if not (check['fixed_point'] & quotient_masks[q])]
                status = ('excluded_transfer_kempe' if check['excluded_transfer'] else
                          'excluded_relative_quotient' if missing else
                          'necessary_condition_residual')
                ledger.append({'query_id':f'c{idx:02d}-{geometry["id"]}-{target}',
                               'case_id':f'c{idx:02d}', 'geometry_id':geometry['id'],
                               'extras':list(extras), **check, 'status':status,
                               'missing_quotient_indices':missing,
                               'necessary_support_size':check['fixed_point'].bit_count()})
        cases.append({'id':f'c{idx:02d}', 'extras':list(extras), 'boundary_order':labels,
                      'supports':supports,'annulus_edges':edges,'annulus_faces':faces,
                      'annulus_rotation_paths':rotation_paths,
                      'joint_vertex_order':[f'b{i}' for i in range(5)]+labels,
                      'column_masks':columns, 'full_lifts_by_inner_then_outer_row':fibres,
                      'geometries':geometries})
    assert len(cases)==70
    assert sum(len(c['geometries'])-1 for c in cases)==75
    summary = {'named_collars':70,'named_geometries':145,'target_queries':435,
               'inner_orbits':820,'literal_inner_assignments':3**9-3,
               'independent_noncrossing_partitions':232,
               'annulus_fibres':70*820*10,
               'annulus_empty_fibres':sum(not f for c in cases for row in c['full_lifts_by_inner_then_outer_row'] for f in row),
               'annulus_full_lifts':sum(len(f) for c in cases for row in c['full_lifts_by_inner_then_outer_row'] for f in row),
               'by_target':{str(t):dict(Counter(q['status'] for q in ledger if q['target']==t)) for t in TARGETS},
               'by_geometry_type':{typ:dict(Counter(q['status'] for q in ledger if (q['geometry_id']=='induced')==(typ=='induced'))) for typ in ('induced','one_w5_ear')}}
    return canonical({'schema':'c9-no4ct-frontier-v2','base':base,'color_frame':[0,1,2,3],
                      'outer_pattern_order':old.P5,'inner_pattern_order':patterns,
                      'kempe_obligations':obligations,'quotient_partitions':partitions,
                      'quotient_masks':quotient_masks,'cases':cases,'queries':ledger,
                      'summary':summary,'scope':{'four_colour_theorem_used':False,
                      'unbounded_input_size':True,'actual_target_source':'not triggered',
                      'residuals':'necessary conditions only; source realizability OPEN',
                      'main_proposition':'OPEN','lean':'not formalized',
                      'quotient_colourability':'source-relative N=k-9+q <= k, independent in actual boundary graph'}})


def verify(actual, expected):
    assert actual == expected, 'complete literal-interface certificate mismatch'


def negatives(payload):
    rejected=[]
    mutations=[]
    bad=copy.deepcopy(payload);bad['cases'][0]['boundary_order'].reverse()
    mutations.append(('changed_named_boundary_order',bad))
    bad=copy.deepcopy(payload);bad['cases'][0]['annulus_rotation_paths']['b0'].reverse()
    mutations.append(('changed_original_rotation_path',bad))
    bad=copy.deepcopy(payload)
    next(f for c in bad['cases'] for row in c['full_lifts_by_inner_then_outer_row'] for f in row if f).pop()
    mutations.append(('deleted_annulus_full_lift',bad))
    bad=copy.deepcopy(payload)
    next(g for c in bad['cases'] for g in c['geometries'] if g['chord'])['boundary_mask']=(1<<820)-1
    mutations.append(('removed_w5_ear_condition',bad))
    bad=copy.deepcopy(payload)
    next(q for q in bad['queries'] if q['status']=='necessary_condition_residual')['status']='excluded_transfer_kempe'
    mutations.append(('false_source_exclusion',bad))
    for label,bad in mutations:
        try:verify(bad,payload)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('accepted corrupt certificate '+label)
    return rejected


def main():
    parser=argparse.ArgumentParser()
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true')
    parser.add_argument('--negative',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.v2.json.gz')
    args=parser.parse_args()
    payload=build()
    if args.write:
        with args.certificate.open('xb') as raw:
            with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as stream:
                stream.write((json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode())
    else:
        with gzip.open(args.certificate,'rt') as stream:verify(json.load(stream),payload)
    result={'status':'PASS',**payload['summary']}
    if args.negative:result['negative_controls_rejected']=negatives(payload)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
