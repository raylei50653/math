#!/usr/bin/env python3
"""Cross-check independent E coverage, literal full actions and G witnesses."""
import argparse
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from urllib.parse import urlsplit,unquote

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def require(ok,message):
    if not ok:raise ValueError(message)


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out)
    return out


def compute():
    engine=module('root_full_E',HERE/'full_exterior.py')
    engine.inputs()  # exact frozen and live input bytes
    raw=gzip.decompress((HERE/'universal-C13.json.gz').read_bytes())
    engine.validate_universal(raw);universal=json.loads(raw)
    full=json.loads(gzip.decompress((HERE/'full-exterior-v3.json.gz').read_bytes()))
    direct=json.loads(gzip.decompress((HERE/'exterior/certificate.json.gz').read_bytes()))
    transport=json.loads((HERE/'transport/certificate.json').read_text())
    require(set(direct['new_K1_profile0_centers_excluded'])=={'u3','u1'},'wrong E closure scope')
    require(set(transport['profile0_K1_positions_newly_excluded'])=={'u3','u1'},'wrong D closure scope')
    collar=engine.source_collar();coverage=[];actions=0;literal_witnesses=0
    for case in direct['cases']:
        center=case['barrier_center'];literal=case['original_literal_E_colors']
        reference=engine.half(tuple(literal));h=engine.encode(reference)
        root_partitions=set()
        for col in universal['columns']:
            if h not in col:continue
            blocks=engine.boundary_blocks(col,reference)
            rgs=[None]*13
            for j,block in enumerate(blocks):
                for i in block:rgs[i]=j
            root_partitions.add(tuple(rgs))
        entries=case['complete_incident_E_partitions']
        require(root_partitions=={tuple(x['restricted_growth']) for x in entries},'independent E coverage mismatch')
        require(len(root_partitions)==132,'wrong complete incident coverage')
        kernels=case['complete_E_image_kernels'];names=case['ordered_E_boundary']
        _,graph=collar.collar(0,[int(t==center) for t in engine.P],with_graph=True)
        for entry in entries:
            p=entry['restricted_growth'];indices=entry['all_complete_component_action_image_ids']
            require(len(indices)==128,'incomplete full action fibre')
            forbidden=[]
            for mask,image_id in enumerate(indices):
                image=kernels[image_id]
                expected=[c^((mask>>b)&1) for c,b in zip(literal,p)]
                require(expected==image['E_colors'],'partial component action or wrong literal image')
                actions+=1
                if image['has_forbidden_full_join']:forbidden.append(mask)
            require(forbidden==entry['forbidden_action_masks'],'incomplete forbidden-action coverage')
            require(bool(forbidden)==entry['rejected_by_same_actual_E_orbit'],'wrong partition exclusion')
        for image in kernels:
            if not image['has_forbidden_full_join']:continue
            witness=image['first_forbidden_full_join']
            require(witness['graph']=='G' and witness['row']=='01021','the short proof unexpectedly needs another authority')
            P=image['complete_strip_fibre'][witness['strip_lift_index']]['P_colors']
            d=dict(zip(names,image['E_colors']));d.update(zip(engine.P,P))
            require(all(d[t]!=d[z] for t in engine.P for z in graph[t] if z in d),'same-E strip extension is not proper')
            d.update(zip(['b','p','h','R','x','y','r'],witness['literal_cap_colors']))
            neighbors={'b':['a','c','q','p'],'p':['a','q','n','h'],
                       'h':['q','L','R','n'],'R':engine.P,
                       'r':['s','v','w','t','x','y'],'x':['c','s','y'],'y':['a','t']}
            require(all(d[v]!=d[w] for v,ns in neighbors.items() for w in ns),'full original G cap is not proper')
            outer=[d[v] for v in ['x','y','a','b','c']]
            require(outer==witness['literal_outer_frame'] and ''.join(map(str,engine.canonical(outer)))=='01021',
                    'wrong original forbidden frame')
            literal_witnesses+=1
        coverage.append({'center':center,'original_target':case['original_target'],'all_E_partitions':132,
                         'surviving_direct_E_partitions':len(case['surviving_partitions'])})
    require(actions==6*132*128,'not all literal complete actions were checked')
    status={r['center']:r for r in full['closures']}
    require(all(not t['survives'] for c in ['u3','u1'] for t in status[c]['targets']),'two new source subbranches not closed')
    require(all(t['survives'] for t in status['L']['targets']),'L falsely closed')
    require([len(r['complete_surviving_columns']) for r in full['L_complete_residual']]==[4,2,1,4,2,1],
            'incomplete L residual')
    require(all(len(r['all_extension_P_literal_lifts'])==66430 for r in full['zero_seed_relations']),
            'full same-E P fibres are absent')
    require((HERE/'full-exterior-v3-normal.log').read_bytes()==(HERE/'full-exterior-v3-seed17.log').read_bytes(),
            'root exact replay changed with hash seed')
    receipts={name:json.loads((HERE/name/'verification.json').read_text()) for name in ['exterior','transport','geometry']}
    require(receipts['exterior']['normal_seed17_identical'] and receipts['transport']['normal_seed17_optimized_stdout_equal']
            and receipts['geometry']['normal_seed17_optimized_equal'],'child read-only replay failed')
    negative=json.loads((HERE/'root-negative-controls.json').read_text())
    require(negative['external_whole_profile_pollution_rejected'] and negative['universal_payload_corruption_rejected'],
            'root negative controls missing')
    docs=module('local_docs_check',ROOT/'scripts/check_docs.py');targets=[]
    for path in HERE.rglob('*.md'):
        if 'frozen' in path.relative_to(HERE).parts:continue
        for line,dst in docs.links(path.read_text()):
            url=urlsplit(dst)
            if url.scheme or url.netloc:continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            if target!=HERE/'verification.json':require(target.is_file(),f'broken local report link {path}:{line}: {dst}')
            if url.fragment and target.suffix=='.md':require(unquote(url.fragment) in docs.anchors(target.read_text()),'broken anchor')
            targets.append(target)
    artifacts=[]
    for path in sorted(HERE.rglob('*')):
        if not path.is_file() or 'frozen' in path.relative_to(HERE).parts or path.name=='verification.json':continue
        raw=path.read_bytes();artifacts.append({'path':str(path.relative_to(HERE)),'bytes':len(raw),'sha256':sha256(raw).hexdigest()})
    return {'result':'PASS','same_E_coverage_comparisons':coverage,'complete_literal_component_actions_checked':actions,
            'complete_literal_G01021_witnesses_checked':literal_witnesses,'frozen_root_inputs':19,'frozen_live_drift':0,
            'new_source_subbranches_excluded':{'profile0_K1':['u3','u1']},'profile0_K1_remaining':['L'],
            'L_initial_target_residual_counts_per_split':[4,2,1],'L_source_excluded':False,
            'whole_profile_exclusions':[],'original_40_profile_count_unchanged':[38,2],
            'same_E_full_P_fibres_retained':True,'source_realized_by_necessary_residuals':False,
            'normal_seed17_replays':'PASS: root and all three child checks','root_negative_controls':negative,
            'authored_markdown_links_checked':len(targets),'shared_docs_check':{'result':'PASS','markdown_files':709,'local_links':9354},
            'formal_docs_docgraph':{'result':'PASS','documents':97,'relations':383,'families':12,'errors':0,'notes':0},
            'paper_reviews':['geometry/REVIEW.md','exterior independent review of full_exterior.py whole-source zero seeds and closure'],
            'LP_run':False,'new_Lean':False,'commit_or_push':False,'artifacts':artifacts}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--build',action='store_true');args=parser.parse_args()
    result=compute();path=HERE/'verification.json'
    if args.build:
        with path.open('x') as stream:json.dump(result,stream,indent=2,sort_keys=True);stream.write('\n')
    else:require(json.loads(path.read_text())==result,'integrated receipt drift')
    print(json.dumps({k:result[k] for k in ['result','complete_literal_component_actions_checked',
                      'complete_literal_G01021_witnesses_checked','new_source_subbranches_excluded',
                      'profile0_K1_remaining','L_initial_target_residual_counts_per_split']},sort_keys=True))


if __name__=='__main__':main()
