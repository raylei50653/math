#!/usr/bin/env python3
"""D-D same-source support coverage and original saturated-path certificates."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
from c5_adjacent_degree5_no_mixed_bc import side_kind, schema_audit
from c5_adjacent_degree5_no_mixed_t2_t1_bridge import frame_evidence, root_pairs, swapped, minor_control
from c5_single_spoke_cores import U, Q, PI, RHO
from c5_single_spoke_two_two_minor import verify_minor
from c5_single_spoke_two_two_external import STYLES
from c5_root_degree_excess import budget
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'artifacts/c5_adjacent_degree5_no_mixed/observations.json'
PREVIOUS = ROOT/'artifacts/c5_adjacent_degree5_no_mixed_ce/observations.json'
OUT = ROOT/'artifacts/c5_adjacent_degree5_no_mixed_dd/observations.json'
from c5_adjacent_degree5_no_mixed_cc import (
    NAMES, geometries, independent_geometries, rotations,
    context, enumerate_records, frame_key,
)


def source_key(s):
    return (s['z']['common'], tuple(map(tuple,s['z']['forbidden'])), tuple(map(tuple,s['w']['forbidden'])))


def bind_sources(data):
    sources = []
    for jid, pair in enumerate(data['abstract_conditions']['retained']):
        z,w = [data['side_normal_forms'][i] for i in pair]
        if (side_kind(z),side_kind(w)) != ('D','D'):
            continue
        bs = {r:budget(s) for r,s in (('z',z),('w',w))}
        assert all((b['D'],b['O'],b['kappa']) == (0,1,0) for b in bs.values())
        sources.append(dict(id=len(sources),retained_join_id=jid,side_ids=pair,z=z,w=w,source_budgets=bs))
    rebuilt=set()
    for c in U:
        sides=[(tuple(sorted((h,a))),tuple(sorted((h,b))))
               for h,a,b in permutations(sorted(U-{c}))]
        rebuilt.update((c,a,b) for a,b in product(sides,repeat=2))
    assert len(sources)==len(rebuilt)==144 and {source_key(s) for s in sources}==rebuilt
    prior=json.loads(PREVIOUS.read_text())['next_frontier']
    assert prior['source_sha256']==sha256(SOURCE.read_bytes()).hexdigest()
    assert prior['records']==[dict(retained_join_id=s['retained_join_id'],side_ids=s['side_ids']) for s in sources]
    assert (sources[0]['retained_join_id'],sources[0]['side_ids']) == (424,[30,30])
    return sources


def audit_symmetries(records,sources,schemas):
    source_lookup={source_key(s):s for s in sources}
    lookup={(r['source_id'],r['supports']):r for r in records}
    for r in records:
        c,az,aw=source_key(sources[r['source_id']])
        moves=[('reflection', (PI[c],tuple(tuple(sorted(PI[v] for v in f)) for f in az),
                    tuple(tuple(sorted(PI[v] for v in f)) for f in aw)),(0,1,2,3)),
               ('z_component_swap',(c,az[::-1],aw),(1,0,2,3)),
               ('w_component_swap',(c,az,aw[::-1]),(0,1,3,2)),
               ('root_swap',(c,aw,az),(2,3,0,1))]
        for name,key,order in moves:
            reflect=name=='reflection'
            ss=tuple(tuple(sorted(RHO[i] for i in r['supports'][j])) if reflect else r['supports'][j] for j in order)
            twin=lookup[source_lookup[key]['id'],ss]
            r[name+'_id']=twin['id']
            rename={NAMES[j]:NAMES[i] for i,j in enumerate(order)}
            def vertex(v):
                if v in ('z','w'):
                    return {'z':'w','w':'z'}[v] if name=='root_swap' else v
                if v.startswith('b'):
                    return 'b'+str(RHO[int(v[1:])]) if reflect else v
                return rename[v.split('_')[0]]+'_'+v.split('_',1)[1]
            for i,j in enumerate(order):
                f=sources[r['source_id']]['z' if j<2 else 'w']['forbidden'][j%2]
                fk=','.join(map(str,f))
                tf=tuple(sorted(PI[v] for v in f)) if reflect else tuple(f)
                tk=','.join(map(str,tf))
                rels={tuple(sorted(tuple(PI[v] for v in t) if reflect else tuple(t) for t in schemas[fk][sid]))
                      for sid in r['q_schema_ids'][NAMES[j]]}
                assert rels=={tuple(sorted(schemas[tk][sid])) for sid in twin['q_schema_ids'][NAMES[i]]}
            mapped=[]
            for e in r['source_evidence']['components']:
                te=next(x for x in twin['source_evidence']['components'] if x['component']==order.index(e['component']))
                assert e['eliminated']==te['eliminated']
                family={tuple(sorted(RHO[i] for i in t)) if reflect else tuple(t) for t in e['frame']['supports']}
                assert family==set(map(tuple,te['frame']['supports']))
                witnesses=set()
                for w in e['frame']['witnesses']:
                    route=w['route']
                    witnesses.add((tuple(tuple(sorted(RHO[i] for i in a)) if reflect else tuple(a) for a in w['frame_arcs']),
                        route['mode'],rename[route['component']],RHO[route['landing']] if reflect else route['landing'],
                        tuple(vertex(v) for v in route['path'])))
                assert witnesses=={frame_key(w) for w in te['frame']['witnesses']}
                mapped.append(te['component'])
            assert len(mapped)==4
        ctx=context(r,sources[r['source_id']])
        fs=[x['source_forbidden'] for x in ctx['components']]
        assert not root_pairs(swapped(ctx),Q,fs)


def controls(records,sources,geometry):
    saved=[]
    count=0
    modes={}
    for r in records:
        ctx=context(r,sources[r['source_id']])
        for e in r['source_evidence']['components']:
            assert e['frame']['supports']
            if not e['eliminated']:
                continue
            assert e['frame']['reason']=='original_path_K5'
            w=e['frame']['witnesses'][0]
            for length in (1,3,5):
                cert=minor_control(ctx,e['component'],w,length)
                count+=1
                if length==1:
                    saved.append(cert)
            for w in e['frame']['witnesses']:
                mode=w['route']['mode']
                score=lambda cw: len(set(cw[0]['components'][cw[1]]['support']) & set(cw[2]['frame_arcs'][0])) * len(set(cw[0]['components'][cw[1]]['support']) & set(cw[2]['frame_arcs'][1]))
                candidate=(ctx,e['component'],w)
                if mode not in modes or score(candidate)>score(modes[mode]):
                    modes[mode]=candidate
    for r in records:
        ctx=context(r,sources[r['source_id']])
        chosen=r['uniform_edge_witnesses'][0]
        for length in (1,3,5):
            cert=minor_control(ctx,chosen['component'],chosen['witness'],length)
            count+=1
            if length==1:
                saved.append(cert)
    assert set(modes)=={'same_root_component','other_root_component'}
    for ctx,k,w in modes.values():
        possible=[sorted(set(ctx['components'][k]['support']) & set(a)) for a in w['frame_arcs'][:2]]
        supply=list(product(*possible))
        for length,styles,ext,suppliers in product((1,5),product(STYLES,repeat=2),(1,3),product(supply,repeat=2)):
            saved.append(minor_control(ctx,k,w,length,styles,suppliers,ext))
            count+=1
    assert any(c['suppliers'][0]!=c['suppliers'][1] for c in saved)
    negatives=[]
    for name,order in tuple((n+'_only',i) for i,n in enumerate(NAMES)):
        missed=[r['id'] for r in records if not r['source_evidence']['components'][order]['eliminated']]
        assert missed
        negatives.append(dict(name=name,missed_record_ids=missed))
    r=next(r for r in records if any(not e['eliminated'] for e in r['source_evidence']['components']))
    e=next(e for e in r['source_evidence']['components'] if not e['eliminated'])
    ctx=context(r,sources[r['source_id']])
    assert all(frame_evidence(ctx,e['component'],(set(t),))['eliminated'] for t in e['frame']['supports'])
    negatives.append(dict(name='per_bag_partitions_are_not_one_fixed_partition',record_id=r['id'],component=e['component']))
    empty=frame_evidence(ctx,e['component'],())
    assert empty['reason']=='no_possible_bag' and not empty['witnesses']
    negatives.append(dict(name='empty_family_is_not_a_minor_witness'))
    ctx,k,w=modes['other_root_component']
    base=minor_control(ctx,k,w,3)
    edges=set(map(tuple,base['edges'])); bags=list(map(set,base['branch_sets']))
    route=base['expanded_external_route']
    bad=[('missing_original_zw',edges-{('w','z')},bags),
         ('missing_external_component_boundary_edge',edges-{tuple(sorted(route[-2:]))},bags),
         ('missing_original_bridge',edges-{tuple(sorted(base['path'][:2]))},bags),
         ('overlapping_branch_sets',edges,[bags[0]|bags[1],*bags[1:]])]
    for name,es,bs in bad:
        try:
            verify_minor(es,bs)
        except AssertionError:
            negatives.append(dict(name=name))
        else:
            raise AssertionError(name)
    ss=next(iter(sorted(geometry)))
    for name,invalid in (('binary_is_not_spoke',(ss[0][0],)),('span_three_impossible',(0,1,2,3))):
        assert (invalid,*ss[1:]) not in geometry
        negatives.append(dict(name=name))
    rel=((0,1),(1,0))
    assert set.intersection(*map(set,rel))=={0,1}
    assert not set.intersection(*map(set,product((0,1),repeat=2)))
    negatives.append(dict(name='pair_marginals_lose_bans'))
    for s in sources:
        residuals=[U-set().union(*map(set,s[r]['forbidden'])) for r in ('z','w')]
        assert residuals==[{s['z']['common']}]*2
        assert list(product(*residuals))==[(s['z']['common'],)*2]
    negatives.append(dict(name='zw_diagonal_must_be_deleted'))
    return saved,count,negatives


def build():
    data=json.loads(SOURCE.read_text()); old=json.loads(PREVIOUS.read_text())
    for path,obj in ((SOURCE,data),(PREVIOUS,old)):
        assert obj['source_sha256']==sha256((ROOT/'scripts'/(path.parent.name+'.py')).read_bytes()).hexdigest()
    sources=bind_sources(data); geometry=geometries(); schemas=schema_audit()
    for key,relations in schemas.items():
        if len(key.split(','))==2:
            assert len(relations)==1
            assert set(map(tuple,relations[0]))=={tuple(map(int,key.split(','))),tuple(map(int,key.split(',')))[::-1]}
    assert set(geometry)==independent_geometries()
    templates={p['order']:rotations(p['order']) for ps in geometry.values() for p in ps}
    for ss,placements in geometry.items():
        for p in placements:
            lifts=dict(zip(NAMES,p['lifts'],strict=True)); order=p['order']
            assert min(lifts['Cz'])==0 and max(lifts[order[-1]])<=5
            assert all(max(lifts[a])<=min(lifts[b]) for a,b in zip(order,order[1:]))
            assert all(1<=max(lifts[n])-min(lifts[n])<=2 for n in NAMES)
            assert ss==tuple(tuple(sorted((p['anchor']+i)%5 for i in lifts[n])) for n in NAMES)
            for t in templates[order]:
                assert len(t['neighborhood_word'])==len(set(t['neighborhood_word']))==8
                for root,other,own in (('z','w',NAMES[:2]),('w','z',NAMES[2:])):
                    assert set(t['root_rotations'][root])=={other}|{n+'_'+str(i) for n in own for i in (0,1)}
    records=enumerate_records(sources,geometry)
    # At least three supports are literal frame edges; choose a same-side
    # exterior path for the uniform arbitrary-size paper argument.
    for r in records:
        uniform=[]
        for e in r['source_evidence']['components']:
            k=e['component']; support=r['supports'][k]
            if len(support)!=2 or (support[1]-support[0])%5 not in (1,4):
                continue
            assert e['frame']['supports']==[list(support)]
            witness=next(w for w in e['frame']['witnesses']
                if w['frame_arcs'][0]==(support[0],)
                and w['frame_arcs'][1]==(support[1],)
                and w['route']['mode']=='same_root_component')
            uniform.append(dict(component=k,witness=witness))
        assert len(uniform)>=3
        r['uniform_edge_witnesses']=uniform
    audit_symmetries(records,sources,schemas)
    minor_certificates,minor_count,negatives=controls(records,sources,geometry)
    fibers=[dict(source_id=s['id'],retained_join_id=s['retained_join_id'],
        support_record_ids=[r['id'] for r in records if r['source_id']==s['id']]) for s in sources]
    for f in fibers:
        f['classification']='source_K5_excluded' if f['support_record_ids'] else 'no_compatible_disk_support'
    covered=set(old['coverage_extension']['covered_source_join_ids'])
    added={s['retained_join_id'] for s in sources}
    assert len(covered)==3116 and len(added)==144 and not covered&added
    lookup={tuple(pair):jid for jid,pair in enumerate(data['abstract_conditions']['retained'])}
    for src in sources:
        reverse=lookup[tuple(src['side_ids'][::-1])]
        assert reverse in added
        assert [data['side_normal_forms'][i] for i in data['abstract_conditions']['retained'][reverse]]==[src['w'],src['z']]
        src['root_swapped_retained_join_id']=reverse
    covered|=added
    remaining={}
    frontier=[]
    for jid,pair in enumerate(data['abstract_conditions']['retained']):
        kinds=tuple(side_kind(data['side_normal_forms'][i]) for i in pair)
        if jid not in covered:
            remaining.setdefault('-'.join(sorted(kinds)),[]).append(jid)
        if kinds==('D','E'):
            frontier.append(dict(retained_join_id=jid,side_ids=pair))
    assert len(remaining)==1 and sum(map(len,remaining.values()))==288
    summary=dict(original_source_joins=len(sources),geometric_supports=len(geometry),
        placements=sum(map(len,geometry.values())),rotation_templates=len(templates),
        contact_rotation_checks=16*sum(map(len,geometry.values())),necessary_support_records=len(records),
        empty_source_fibers=sum(not f['support_record_ids'] for f in fibers),source_exclusions=len(records),
        retained_support_records=0,target_queries=0,target_accepts=0,
        exclusion_patterns={str(k):v for k,v in sorted(Counter(tuple(e['eliminated'] for e in r['source_evidence']['components']) for r in records).items())},
        common_color_counts=dict(sorted(Counter(sources[r['source_id']]['z']['common'] for r in records).items())),
        literal_source_reflections=len(records),whole_root_swaps=len(records),whole_component_swaps=2*len(records),
        binary_relations_checked=65535,singleton_schemas=380,pair_schemas=6,
        uniform_minor_controls=3*len(records),minor_controls=minor_count,saved_minor_certificates=len(minor_certificates),negative_controls=len(negatives))
    assert (len(geometry),summary['placements'],len(records),len(templates))==(240,240,352,4)
    assert summary['empty_source_fibers']==80
    assert summary['exclusion_patterns']=={
        '(True, True, True, True)':288,
        **{str(tuple(i!=j for i in range(4))):16 for j in range(4)}}
    inputs=[SOURCE,PREVIOUS,ROOT/'scripts/c5_adjacent_degree5_no_mixed_cc.py']
    inputs += [ROOT/p for p in old['inputs_sha256'] if p.startswith('scripts/')]
    return dict(schema=1,scope='necessary supports and arbitrary-size paper source exclusion; not disk realization or Lean theorem',
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(set(inputs))},
        summary=summary,original_records=sources,source_fibers=fibers,
        geometries=[dict(id=i,supports=ss,placements=ps) for i,(ss,ps) in enumerate(sorted(geometry.items()))],
        rotation_templates=[dict(order=o,rotations=ts) for o,ts in sorted(templates.items())],
        q_complete_binary_schemas=schemas,records=records,minor_certificates=minor_certificates,negative_controls=negatives,
        coverage_extension=dict(covered_source_join_ids=sorted(covered),newly_covered_source_join_ids=sorted(added),
            covered_source_joins=3260,remaining_source_joins=288,covered_unordered_cells=14,remaining_unordered_cells=1,
            remaining_cells=remaining,new_closure='source_exclusion'),
        next_frontier=dict(class_name='D-E',scope='IDs only; no support or target audit',
            source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),records=frontier,
            first_sides=[data['side_normal_forms'][i] for i in frontier[0]['side_ids']]))


def render(data):
    lines=['# D–D 四飽和原分量來源排除','','352 份必要支援全 source K5；0 target 查詢。必要表與 skeleton 不宣稱 disk 實現。','',
        '| ID | 原 join | Cz / Dz / Cw / Dw | Cz K5 | Dz K5 | Cw K5 | Dw K5 |',
        '| ---: | ---: | --- | --- | --- | --- | --- |']
    for r in data['records']:
        flags=['X' if e['eliminated'] else '—' for e in r['source_evidence']['components']]
        lines.append(f"| {r['id']} | {data['original_records'][r['source_id']]['retained_join_id']} | {' / '.join(''.join(map(str,s)) for s in r['supports'])} | {' | '.join(flags)} |")
    lines += ['', '## 原接合纖維', '', '| 原 join | 支援 IDs | 分類 |', '| ---: | --- | --- |']
    for f in data['source_fibers']:
        lines.append(f"| {f['retained_join_id']} | {', '.join(map(str,f['support_record_ids'])) or '—'} | {f['classification']} |")
    return '\n'.join(lines+['','[完整證書](observations.json)；[前提與證明](../../docs/c5_adjacent_degree5_no_mixed_dd.md)。',''])


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    data=build()
    for p,payload in ((OUT,json.dumps(data,sort_keys=True,indent=2)+'\n'),(OUT.with_name('support_table.md'),render(data))):
        if args.check:
            assert p.read_bytes()==payload.encode(),f'certificate differs: {p}'
        else:
            p.parent.mkdir(parents=True,exist_ok=True); p.write_text(payload)
    print(json.dumps(data['summary'],sort_keys=True))


if __name__=='__main__':
    main()
