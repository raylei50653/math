#!/usr/bin/env python3
"""C-C same-source support coverage and original saturated-path certificates."""
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
PREVIOUS = ROOT/'artifacts/c5_adjacent_degree5_no_mixed_bd/observations.json'
OUT = ROOT/'artifacts/c5_adjacent_degree5_no_mixed_cc/observations.json'
NAMES = ('Cz', 'Dz', 'Cw', 'Dw')
COMPONENTS = tuple((n, r, col, pos, 2) for pos,(n,r,col) in enumerate(
    (('Cz','z',0),('Dz','z',1),('Cw','w',0),('Dw','w',1))))

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
    for flips in product((False, True), repeat=4):
        ports = {n: (n+'_0',) for n in ('Cz','Dz','Cw','Dw')}

        for n, flip in zip(NAMES, flips):
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
        if (side_kind(z),side_kind(w)) != ('C','C'):
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
        rebuilt.update((c,a,b) for a,b in product(sides,repeat=2))
    assert len(sources)==len(rebuilt)==144 and {source_key(s) for s in sources}==rebuilt
    prior=json.loads(PREVIOUS.read_text())['next_frontier']
    assert prior['source_sha256']==sha256(SOURCE.read_bytes()).hexdigest()
    assert prior['records']==[dict(retained_join_id=s['retained_join_id'],side_ids=s['side_ids']) for s in sources]
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
            ids={n:stable_schema_ids(tuple(src[r]['forbidden'][col]),ss[pos]) for n,r,col,pos,k in COMPONENTS}
            if not all(ids.values()):
                continue
            rec=dict(id=len(records),source_id=src['id'],geometry_id=gid,supports=ss,q_schema_ids=ids)
            ctx=context(rec,src)
            fs=[c['source_forbidden'] for c in ctx['components']]
            assert not root_pairs(ctx,Q,fs)
            ev=evidence(ctx,Q,fs)
            rec.update(source_evidence=ev,status='source_excluded' if ev['eliminated'] else 'retained',
                targets=[])
            assert ev['eliminated'], 'source closure not established'
            records.append(rec)
    return records


def frame_key(w):
    r=w['route']
    return (tuple(map(tuple,w['frame_arcs'])),r['mode'],r['component'],r['landing'],tuple(r['path']))


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
            assert len(mapped)==2
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
                modes.setdefault(w['route']['mode'],(ctx,e['component'],w))
    assert set(modes)=={'same_root_component','other_root_component'}
    for ctx,k,w in modes.values():
        possible=[sorted(set(ctx['components'][k]['support']) & set(a)) for a in w['frame_arcs'][:2]]
        supply=list(product(*possible))
        for length,styles,ext,suppliers in product((1,5),product(STYLES,repeat=2),(1,3),product(supply,repeat=2)):
            saved.append(minor_control(ctx,k,w,length,styles,suppliers,ext))
            count+=1
    negatives=[]
    for name,order in (('z_pair_only',0),('w_pair_only',1)):
        missed=[r['id'] for r in records if not r['source_evidence']['components'][order]['eliminated']]
        negatives.append(dict(name=name,missed_record_ids=missed))
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
    audit_symmetries(records,sources,schemas)
    minor_certificates,minor_count,negatives=controls(records,sources,geometry)
    fibers=[dict(source_id=s['id'],retained_join_id=s['retained_join_id'],
        support_record_ids=[r['id'] for r in records if r['source_id']==s['id']]) for s in sources]
    for f in fibers:
        f['classification']='source_K5_excluded' if f['support_record_ids'] else 'no_compatible_disk_support'
    covered=set(old['coverage_extension']['covered_source_join_ids'])
    added={s['retained_join_id'] for s in sources}
    assert len(covered)==2396 and len(added)==144 and not covered&added
    covered|=added
    remaining={}
    frontier=[]
    for jid,pair in enumerate(data['abstract_conditions']['retained']):
        kinds=tuple(side_kind(data['side_normal_forms'][i]) for i in pair)
        if jid not in covered:
            remaining.setdefault('-'.join(sorted(kinds)),[]).append(jid)
        if kinds==('C','D'):
            frontier.append(dict(retained_join_id=jid,side_ids=pair))
    assert len(remaining)==4 and sum(map(len,remaining.values()))==1008
    summary=dict(original_source_joins=len(sources),geometric_supports=len(geometry),
        placements=sum(map(len,geometry.values())),rotation_templates=len(templates),
        contact_rotation_checks=16*sum(map(len,geometry.values())),necessary_support_records=len(records),
        empty_source_fibers=sum(not f['support_record_ids'] for f in fibers),source_exclusions=len(records),
        retained_support_records=0,target_queries=0,target_accepts=0,
        exclusion_patterns={str(k):v for k,v in sorted(Counter(tuple(e['eliminated'] for e in r['source_evidence']['components']) for r in records).items())},
        common_color_counts=dict(sorted(Counter(sources[r['source_id']]['z']['common'] for r in records).items())),
        literal_source_reflections=len(records),whole_root_swaps=len(records),whole_component_swaps=2*len(records),
        binary_relations_checked=65535,singleton_schemas=380,pair_schemas=6,
        minor_controls=minor_count,saved_minor_certificates=len(minor_certificates),negative_controls=len(negatives))
    assert (len(geometry),summary['placements'],len(records),len(templates))==(240,240,1176,4)
    inputs=[SOURCE,PREVIOUS,ROOT/'scripts/c5_adjacent_degree5_no_mixed_bc.py']
    inputs += [ROOT/p for p in old['inputs_sha256'] if p.startswith('scripts/')]
    return dict(schema=1,scope='necessary supports and arbitrary-size paper source exclusion; not disk realization or Lean theorem',
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sorted(set(inputs))},
        summary=summary,original_records=sources,source_fibers=fibers,
        geometries=[dict(id=i,supports=ss,placements=ps) for i,(ss,ps) in enumerate(sorted(geometry.items()))],
        rotation_templates=[dict(order=o,rotations=ts) for o,ts in sorted(templates.items())],
        q_complete_binary_schemas=schemas,records=records,minor_certificates=minor_certificates,negative_controls=negatives,
        coverage_extension=dict(covered_source_join_ids=sorted(covered),newly_covered_source_join_ids=sorted(added),
            covered_source_joins=2540,remaining_source_joins=1008,covered_unordered_cells=11,remaining_unordered_cells=4,
            remaining_cells=remaining,new_closure='source_exclusion'),
        next_frontier=dict(class_name='C-D',scope='IDs only; no support or target audit',
            source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),records=frontier,
            first_sides=[data['side_normal_forms'][i] for i in frontier[0]['side_ids']]))


def render(data):
    lines=['# C–C 四分量原路徑來源排除','','1,176 份必要支援全 source K5；0 target 查詢。必要表與 skeleton 不宣稱 disk 實現。','',
        '| ID | 原 join | Cz / Dz / Cw / Dw | z 飽和分量 K5 | w 飽和分量 K5 |',
        '| ---: | ---: | --- | --- | --- |']
    for r in data['records']:
        flags=['X' if e['eliminated'] else '—' for e in r['source_evidence']['components']]
        lines.append(f"| {r['id']} | {data['original_records'][r['source_id']]['retained_join_id']} | {' / '.join(''.join(map(str,s)) for s in r['supports'])} | {' | '.join(flags)} |")
    return '\n'.join(lines+['','[完整證書](observations.json)；[前提與證明](../../docs/c5_adjacent_degree5_no_mixed_cc.md)。',''])


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
