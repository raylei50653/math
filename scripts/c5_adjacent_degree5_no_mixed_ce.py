#!/usr/bin/env python3
"""C-E same-source support coverage and original saturated-path certificates."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
from c5_adjacent_degree5_no_mixed_bc import side_kind, schema_audit, stable_schema_ids
from c5_adjacent_degree5_no_mixed_t2_t1_bridge import frame_evidence, root_pairs, swapped, minor_control
from c5_adjacent_degree5_singleton_long_arc import valid_q_support
from c5_single_spoke_frame_arc import admissible_supports
from c5_single_spoke_cores import U, Q, PI, RHO
from c5_single_spoke_two_two_minor import verify_minor
from c5_single_spoke_two_two_external import STYLES
from c5_root_degree_excess import budget
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'artifacts/c5_adjacent_degree5_no_mixed/observations.json'
PREVIOUS = ROOT/'artifacts/c5_adjacent_degree5_no_mixed_cd/observations.json'
OUT = ROOT/'artifacts/c5_adjacent_degree5_no_mixed_ce/observations.json'
NAMES = ('Cz', 'Dz', 'Cw', 'Dw', 'Ew')
COMPONENTS = (('Cz','z',0,0,2), ('Dz','z',1,1,2),
              ('Cw','w',0,2,2), ('Dw','w',1,3,1), ('Ew','w',2,4,1))

def cardinalities(name):
    return range(2, 6)


def geometries():
    choices = {name: [s for k in cardinalities(name) for s in combinations(range(6), k)
                      if max(s) - min(s) < 5] for name in NAMES}
    orders = set()
    for z, w in product(permutations(NAMES[:2]), permutations(NAMES[2:])):
        order = z + w
        i = order.index("Cz")
        orders.add(order[i:] + order[:i])
    result = {}
    for order in sorted(orders):
        def visit(j, end, assigned):
            if j == len(NAMES):
                for anchor in range(5):
                    supports = tuple(tuple(sorted((anchor + i) % 5 for i in assigned[n]))
                                     for n in NAMES)
                    result.setdefault(supports, []).append(dict(
                        order=order, anchor=anchor, lifts=tuple(assigned[n] for n in NAMES)))
                return
            for support in choices[order[j]]:
                if min(support) >= end and (j or min(support) == 0):
                    visit(j + 1, max(support), assigned | {order[j]: support})
        visit(0, 0, {})
    return result


def independent_geometries():
    """Actual support hulls on each whole side, with disjoint frame-edge masks."""
    sides = []
    for names in (NAMES[:2], NAMES[2:]):
        found = set()
        choices = [[s for k in cardinalities(n) for s in combinations(range(5), k)] for n in names]
        for supports in product(*choices):
            for anchor in set().union(*map(set, supports)):
                lifts = [sorted((i - anchor) % 5 for i in s) for s in supports]
                if any(not (a[-1] <= b[0] or b[-1] <= a[0])
                       for a, b in combinations(lifts, 2)):
                    continue
                span = max(s[-1] for s in lifts)
                mask = sum(1 << ((anchor + j) % 5) for j in range(span))
                found.add((supports, mask))
        sides.append(found)
    # Group by masks to avoid an unnecessarily large all-pairs product.
    groups = []
    for side in sides:
        by_mask = {}
        for supports, mask in side:
            by_mask.setdefault(mask, set()).add(supports)
        groups.append(by_mask)
    return {a + b for ma, aa in groups[0].items() for mb, bb in groups[1].items()
            if not ma & mb for a, b in product(aa, bb)}


def rotations(order):
    result = []
    for flips in product((False, True), repeat=3):
        ports = {n: (n+'_0',) for n in NAMES}

        for n, flip in zip(NAMES[:3], flips):
            ports[n] = (n+'_0', n+'_1')[::(-1 if flip else 1)]
        roots = {}
        for r, other, own in (('z','w',NAMES[:2]), ('w','z',NAMES[2:])):
            start = next(i for i,n in enumerate(order) if n in own and order[i-1] not in own)
            units = tuple(order[(start+j)%len(NAMES)] for j in range(len(own)))
            assert set(units) == set(own)
            roots[r] = (other,) + tuple(p for n in units for p in ports[n])
            assert len(roots[r]) == len(set(roots[r])) == 5
        result.append(dict(flips=flips, root_rotations=roots,
            neighborhood_word=tuple(p for n in order for p in ports[n])))
    return result


def context(rec, src):
    return dict(record_id=rec['id'], root_boundary={r: src[r]['root_boundary'] for r in ('z','w')},
        components=[dict(name=n, root=r, support=rec['supports'][pos],
            contacts=[f'{n}_{i}' for i in range(k)], source_forbidden=src[r]['forbidden'][col])
            for n,r,col,pos,k in COMPONENTS])



def source_key(s):
    return (s['z']['common'], tuple(map(tuple,s['z']['forbidden'])), tuple(map(tuple,s['w']['forbidden'])))


def bind_sources(data):
    sources = []
    for jid, pair in enumerate(data['abstract_conditions']['retained']):
        z,w = [data['side_normal_forms'][i] for i in pair]
        if (side_kind(z),side_kind(w)) != ('C','E'):
            continue
        bs = {r:budget(s) for r,s in (('z',z),('w',w))}
        assert all((b['D'],b['O'],b['kappa']) == (1,0,0) for b in bs.values())
        sources.append(dict(id=len(sources),retained_join_id=jid,side_ids=pair,z=z,w=w,source_budgets=bs))
    rebuilt=set()
    for c in U:
        sides=[]
        for h in U-{c}:
            pair=tuple(sorted(U-{c,h}))
            sides.extend((((h,),pair),(pair,(h,))))
        rebuilt.update((c,a,tuple((h,) for h in b)) for a,b in product(sides,permutations(sorted(U-{c}))))
    assert len(sources)==len(rebuilt)==144 and {source_key(s) for s in sources}==rebuilt
    prior=json.loads(PREVIOUS.read_text())['next_frontier']
    assert prior['source_sha256']==sha256(SOURCE.read_bytes()).hexdigest()
    assert prior['records']==[dict(retained_join_id=s['retained_join_id'],side_ids=s['side_ids']) for s in sources]
    assert (sources[0]['retained_join_id'],sources[0]['side_ids'])==(12,[16,64])
    return sources


def evidence(ctx, row, bans):
    entries=[]
    for k,c in enumerate(ctx['components']):
        if len(c['source_forbidden'])!=2 or len(bans[k])!=2:
            continue
        family=admissible_supports(tuple(row),tuple(c['support']),tuple(bans[k]))
        frame=frame_evidence(ctx,k,family)
        entries.append(dict(component=k,name=c['name'],ordered_contacts=c['contacts'],
            forbidden=bans[k],frame=frame,eliminated=frame['eliminated']))
    return dict(components=entries,eliminated=any(e['eliminated'] for e in entries))


def enumerate_records(sources,geometry):
    records=[]
    for gid,(ss,ps) in enumerate(sorted(geometry.items())):
        for src in sources:
            if not all(len({Q[i] for i in ss[pos]})>=2 and valid_q_support(ss[pos],tuple(src[r]['forbidden'][col])) for n,r,col,pos,k in COMPONENTS):
                continue
            ids={n:stable_schema_ids(tuple(src[r]['forbidden'][col]),ss[pos]) for n,r,col,pos,k in COMPONENTS if k==2}
            if not all(ids.values()):
                continue
            rec=dict(id=len(records),source_id=src['id'],geometry_id=gid,supports=ss,q_schema_ids=ids)
            rec['q_single_contact_relations']={n:((src[r]['forbidden'][col][0],),) for n,r,col,pos,k in COMPONENTS if k==1}
            ctx=context(rec,src)
            fs=[c['source_forbidden'] for c in ctx['components']]
            assert not root_pairs(ctx,Q,fs)
            ev=evidence(ctx,Q,fs)
            rec.update(source_evidence=ev,status='source_excluded' if ev['eliminated'] else 'retained',
                targets=[])
            assert ev['eliminated'], 'source closure not established'
            e=ev['components'][0]
            support=ss[e['component']]
            assert e['frame']['supports']==[list(support)]
            # One common partition works for every original path bag.
            arcs=[[support[0]],[support[1]],sorted(set(range(5))-set(support))]
            rec['edge_partition_witness']=next(w for w in e['frame']['witnesses']
                if [list(a) for a in w['frame_arcs']]==arcs and w['route']['mode']=='same_root_component')
            records.append(rec)
    return records


def frame_key(w):
    r=w['route']
    return (tuple(map(tuple,w['frame_arcs'])),r['mode'],r['component'],r['landing'],tuple(r['path']))


def audit_symmetries(records,sources,schemas):
    by_source={source_key(s):s for s in sources}
    lookup={(r['source_id'],r['supports']):r for r in records}
    for rec in records:
        c,az,aw=source_key(sources[rec['source_id']])
        moves=[('reflection',(PI[c],tuple(tuple(sorted(PI[v] for v in f)) for f in az),
                 tuple(tuple(PI[v] for v in f) for f in aw)),tuple(range(5))),
               ('z_component_swap',(c,az[::-1],aw),(1,0,2,3,4)),
               ('w_unary_swap',(c,az,(aw[0],aw[2],aw[1])),(0,1,2,4,3))]
        for name,key,order in moves:
            ref=name=='reflection'
            ss=tuple(tuple(sorted(RHO[v] for v in rec['supports'][j])) if ref else rec['supports'][j] for j in order)
            twin=lookup[by_source[key]['id'],ss]
            rec[name+'_id']=twin['id']
            rename={NAMES[j]:NAMES[i] for i,j in enumerate(order)}
            def vertex(v):
                if v in ('z','w'): return v
                if v.startswith('b'): return 'b'+str(RHO[int(v[1:])]) if ref else v
                return rename[v.split('_')[0]]+'_'+v.split('_',1)[1]
            def relations(record,src,j):
                n,r,col,pos,k=COMPONENTS[j]
                if k==1: return [record['q_single_contact_relations'][n]]
                f=','.join(map(str,src[r]['forbidden'][col]))
                return [schemas[f][i] for i in record['q_schema_ids'][n]]
            for i,j in enumerate(order):
                rels=relations(rec,sources[rec['source_id']],j)
                moved={tuple(sorted(tuple(PI[v] for v in t) if ref else tuple(t) for t in rel)) for rel in rels}
                assert moved=={tuple(sorted(rel)) for rel in relations(twin,sources[twin['source_id']],i)}
                assert {tuple(sorted(tuple(reversed(t)) for t in rel)) for rel in rels}=={tuple(sorted(rel)) for rel in rels}
            e=rec['source_evidence']['components'][0]
            te=twin['source_evidence']['components'][0]
            assert te['component']==order.index(e['component'])
            assert {tuple(sorted(RHO[v] for v in t)) if ref else tuple(t) for t in e['frame']['supports']}==set(map(tuple,te['frame']['supports']))
            witnesses=set()
            for w in e['frame']['witnesses']:
                route=w['route']
                witnesses.add((tuple(tuple(sorted(RHO[v] for v in a)) if ref else tuple(a) for a in w['frame_arcs']),
                    route['mode'],rename[route['component']],RHO[route['landing']] if ref else route['landing'],
                    tuple(vertex(v) for v in route['path'])))
            assert witnesses=={frame_key(w) for w in te['frame']['witnesses']}
        ctx=context(rec,sources[rec['source_id']]); fs=[c['source_forbidden'] for c in ctx['components']]
        assert not root_pairs(swapped(ctx),Q,fs)
        moved=json.loads(json.dumps(rec['source_evidence']))
        for e in moved['components']:
            for w in e['frame']['witnesses']:
                w['route']['path']=[{'z':'w','w':'z'}.get(v,v) for v in w['route']['path']]
        assert moved==json.loads(json.dumps(evidence(swapped(ctx),Q,fs)))


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
            w=r['edge_partition_witness']
            for length in (1,3,5):
                cert=minor_control(ctx,e['component'],w,length)
                count+=1
                if length==1:
                    saved.append(cert)
            for w in e['frame']['witnesses']:
                modes.setdefault(w['route']['mode'],(ctx,e['component'],w))
    assert set(modes)=={'same_root_component','other_root_component'}
    for ctx,k,w in modes.values():
        possible=[sorted(set(ctx['components'][k]['support']) & set(a)) for a in w['frame_arcs'][:2]]
        supply=list(product(*possible))
        for length,styles,ext,suppliers in product((1,5),product(STYLES,repeat=2),(1,3),product(supply,repeat=2)):
            saved.append(minor_control(ctx,k,w,length,styles,suppliers,ext))
            count+=1
    negatives=[]
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
    for name,invalid in (('binary_is_not_spoke',(ss[0][0],)),('span_two_impossible',(0,1,2))):
        assert (invalid,*ss[1:]) not in geometry
        negatives.append(dict(name=name))
    for j in (3,4):
        bad=list(ss); bad[j]=(ss[j][0],)
        assert tuple(bad) not in geometry
        negatives.append(dict(name=NAMES[j]+'_is_not_spoke'))
    empty=frame_evidence(ctx,k,())
    assert not empty['witnesses'] and empty['reason']=='no_possible_bag'
    negatives.append(dict(name='empty_family_is_not_a_minor_witness'))
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
    assert set(geometry)==independent_geometries()
    templates={p['order']:rotations(p['order']) for ps in geometry.values() for p in ps}
    for ss,placements in geometry.items():
        for p in placements:
            lifts=dict(zip(NAMES,p['lifts'],strict=True)); order=p['order']
            assert min(lifts['Cz'])==0 and max(lifts[order[-1]])<=5
            assert all(max(lifts[a])<=min(lifts[b]) for a,b in zip(order,order[1:]))
            assert all(max(lifts[n])-min(lifts[n])==1 for n in NAMES)
            assert ss==tuple(tuple(sorted((p['anchor']+i)%5 for i in lifts[n])) for n in NAMES)
            for t in templates[order]:
                assert len(t['neighborhood_word'])==len(set(t['neighborhood_word']))==8
                for root,other,own in (('z','w',NAMES[:2]),('w','z',NAMES[2:])):
                    assert set(t['root_rotations'][root])=={other}|{n+'_'+str(i) for n,r,col,pos,k in COMPONENTS if n in own for i in range(k)}
    records=enumerate_records(sources,geometry)
    audit_symmetries(records,sources,schemas)
    minor_certificates,minor_count,negatives=controls(records,sources,geometry)
    fibers=[dict(source_id=s['id'],retained_join_id=s['retained_join_id'],
        support_record_ids=[r['id'] for r in records if r['source_id']==s['id']]) for s in sources]
    for f in fibers:
        f['classification']='source_K5_excluded' if f['support_record_ids'] else 'no_compatible_disk_support'
    covered=set(old['coverage_extension']['covered_source_join_ids'])
    lookup={tuple(pair):jid for jid,pair in enumerate(data['abstract_conditions']['retained'])}
    for src in sources:
        src['root_swapped_retained_join_id']=lookup[tuple(src['side_ids'][::-1])]
        assert [data['side_normal_forms'][i] for i in data['abstract_conditions']['retained'][src['root_swapped_retained_join_id']]]==[src['w'],src['z']]
    added={s['retained_join_id'] for s in sources}|{s['root_swapped_retained_join_id'] for s in sources}
    assert len(covered)==2828 and len(added)==288 and not covered&added
    covered|=added
    remaining={}
    frontier=[]
    for jid,pair in enumerate(data['abstract_conditions']['retained']):
        kinds=tuple(side_kind(data['side_normal_forms'][i]) for i in pair)
        if jid not in covered:
            remaining.setdefault('-'.join(sorted(kinds)),[]).append(jid)
        if kinds==('D','D'):
            frontier.append(dict(retained_join_id=jid,side_ids=pair))
    assert len(remaining)==2 and sum(map(len,remaining.values()))==432
    summary=dict(original_source_joins=len(sources),geometric_supports=len(geometry),
        placements=sum(map(len,geometry.values())),rotation_templates=len(templates),
        contact_rotation_checks=8*sum(map(len,geometry.values())),necessary_support_records=len(records),
        empty_source_fibers=sum(not f['support_record_ids'] for f in fibers),source_exclusions=len(records),
        retained_support_records=0,target_queries=0,target_accepts=0,
        exclusion_patterns={str(k):v for k,v in sorted(Counter(tuple(e['eliminated'] for e in r['source_evidence']['components']) for r in records).items())},
        common_color_counts=dict(sorted(Counter(sources[r['source_id']]['z']['common'] for r in records).items())),
        literal_source_reflections=len(records),whole_root_swaps=len(records),whole_component_swaps=2*len(records),
        binary_relations_checked=65535,singleton_schemas=380,pair_schemas=6,
        minor_controls=minor_count,saved_minor_certificates=len(minor_certificates),negative_controls=len(negatives))
    assert (len(geometry),summary['placements'],len(templates))==(60,60,12)
    assert len(records)==96 and summary['empty_source_fibers']==108
    assert summary['common_color_counts']=={3:96}
    assert all(len(r['source_evidence']['components'])==1 for r in records)
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
            covered_source_joins=3116,remaining_source_joins=432,covered_unordered_cells=13,remaining_unordered_cells=2,
            remaining_cells=remaining,new_closure='source_exclusion'),
        next_frontier=dict(class_name='D-D',scope='IDs only; no support or target audit',
            source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),records=frontier,
            first_sides=[data['side_normal_forms'][i] for i in frontier[0]['side_ids']]))


def render(data):
    lines=['# C–E 五正跨度與飽和原路徑來源排除','','全部必要支援全 source K5；0 target 查詢。必要表不宣稱 disk 實現。','',
        '| ID | 原 join | Cz / Dz / Cw / Dw / Ew | 飽和原分量 |',
        '| ---: | ---: | --- | --- |']
    for r in data['records']:
        e=r['source_evidence']['components'][0]
        lines.append(f"| {r['id']} | {data['original_records'][r['source_id']]['retained_join_id']} | {' / '.join(''.join(map(str,s)) for s in r['supports'])} | {e['name']} |")
    lines+=['','## 原 ID 纖維','','| 原 join | 支援數 | 分類 |','| ---: | ---: | --- |']
    for f in data['source_fibers']:
        lines.append(f"| {f['retained_join_id']} | {len(f['support_record_ids'])} | {f['classification']} |")
    return '\n'.join(lines+['','[完整證書](observations.json)；[前提與證明](../../docs/c5_adjacent_degree5_no_mixed_ce.md)。',''])


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
