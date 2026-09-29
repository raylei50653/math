#!/usr/bin/env python3
"""B-C necessary supports and saturated-component original-path certificates."""
import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
from c5_adjacent_degree5_no_mixed_ee import side_kind
from c5_adjacent_degree5_no_mixed_t2_t0_pairs import schema_audit, stable_schema_ids, evidence
from c5_adjacent_degree5_no_mixed_t2_t1_bridge import root_pairs, swapped, minor_control
from c5_adjacent_degree5_singleton_long_arc import component_options, valid_q_support
from c5_root_degree_excess import budget
from c5_single_spoke_cores import U, Q, TARGETS, PI, RHO
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'artifacts/c5_adjacent_degree5_no_mixed/observations.json'
PREVIOUS = ROOT/'artifacts/c5_adjacent_degree5_no_mixed_ee/observations.json'
OUT = ROOT/'artifacts/c5_adjacent_degree5_no_mixed_bc/observations.json'
NAMES = ('Cz', 'Dz', 'z0', 'Cw', 'Dw')
COMPONENTS = (('Cz','z',0,0,2), ('Dz','z',1,1,1), ('Cw','w',0,3,2), ('Dw','w',1,4,2))

def cardinalities(name):
    return range(2, 6) if name != "z0" else (1,)


def geometries():
    choices = {name: [s for k in cardinalities(name) for s in combinations(range(6), k)
                      if max(s) - min(s) < 5] for name in NAMES}
    orders = set()
    for z, w in product(permutations(NAMES[:3]), permutations(NAMES[3:])):
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
    for names in (NAMES[:3], NAMES[3:]):
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
        ports = {n: (n+'_0',) for n in ('Cz','Dz','Cw','Dw')}
        ports['z0'] = ('z0',)
        for n, flip in zip(('Cz','Cw','Dw'), flips):
            ports[n] = (n+'_0', n+'_1')[::(-1 if flip else 1)]
        roots = {}
        for r, other, own in (('z','w',NAMES[:3]), ('w','z',NAMES[3:])):
            start = next(i for i,n in enumerate(order) if n in own and order[i-1] not in own)
            units = tuple(order[(start+j)%5] for j in range(len(own)))
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


def row_evidence(ctx, row):
    options = [component_options(len(c['contacts']), tuple(c['support']), tuple(c['source_forbidden']), tuple(row))
               for c in ctx['components']]
    joins = []
    for fs in product(*(c['options'] for c in options)):
        ez = U-{row[i] for i in ctx['root_boundary']['z']}-set(fs[0])-set(fs[1])
        ew = U-set(fs[2])-set(fs[3])
        pairs = sorted((a,b) for a,b in product(ez,ew) if a != b)
        assert pairs == root_pairs(ctx,row,fs)
        assert sorted((b,a) for a,b in pairs) == root_pairs(swapped(ctx),row,fs)
        ev = evidence(ctx,row,fs) if not pairs else None
        joins.append(dict(forbidden_sets=fs, residuals=(sorted(ez),sorted(ew)), root_pairs=pairs,
                          evidence=ev))
    return dict(row=row, components=options, joins=joins,
        initial_status='accept' if all(j['root_pairs'] for j in joins) else 'unresolved',
        status='accept' if all(j['root_pairs'] or j['evidence']['eliminated'] for j in joins) else 'unresolved')


def build():
    original, previous = [json.loads(p.read_text()) for p in (SOURCE,PREVIOUS)]
    for path, data in ((SOURCE, original), (PREVIOUS, previous)):
        script = ROOT/'scripts'/(path.parent.name+'.py')
        assert data['source_sha256'] == sha256(script.read_bytes()).hexdigest()
    sources = []
    for jid,(i,j) in enumerate(original['abstract_conditions']['retained']):
        z,w = [original['side_normal_forms'][k] for k in (i,j)]
        if (side_kind(z),side_kind(w)) != ('B','C'):
            continue
        bs = {r: budget(s) for r,s in (('z',z),('w',w))}
        assert all((b['D'],b['O'],b['kappa']) == (1,0,0) for b in bs.values())
        sources.append(dict(id=len(sources), retained_join_id=jid, side_ids=(i,j), z=z,w=w,source_budgets=bs))
    def key(s):
        return (tuple(s['z']['root_boundary']),s['z']['common'],tuple(map(tuple,s['z']['forbidden'])),tuple(map(tuple,s['w']['forbidden'])))
    rebuilt = set()
    for i in range(5):
        for c in U-{Q[i]}:
            for az in permutations(sorted(U-{Q[i],c})):
                for a in U-{c}:
                    pair = tuple(sorted(U-{c,a}))
                    for aw in (((a,),pair),(pair,(a,))):
                        rebuilt.add(((i,),c,tuple((v,) for v in az),aw))
    assert len(sources) == len(rebuilt) == 180 and {key(s) for s in sources} == rebuilt
    assert previous['next_frontier']['records'] == [dict(retained_join_id=s['retained_join_id'],side_ids=list(s['side_ids'])) for s in sources]
    assert previous['next_frontier']['source_sha256'] == sha256(SOURCE.read_bytes()).hexdigest()
    geometry = geometries()
    assert set(geometry) == independent_geometries()
    schemas = schema_audit()
    templates = {p['order']: rotations(p['order']) for ps in geometry.values() for p in ps}
    records, gs = [], []
    for ss, ps in sorted(geometry.items()):
        gid = len(gs)
        for p in ps:
            lifts = dict(zip(NAMES,p['lifts']))
            assert min(lifts['Cz']) == 0
            assert all(max(lifts[a]) <= min(lifts[b]) for a,b in zip(p['order'],p['order'][1:]))
            assert max(lifts[p['order'][-1]]) <= 5
            assert all(1 <= max(lifts[n])-min(lifts[n]) <= 2 for n in NAMES if n != 'z0')
            for n,support in zip(NAMES,ss):
                assert support == tuple(sorted((p['anchor']+x)%5 for x in lifts[n]))
        gs.append(dict(id=gid,supports=ss,placements=ps))
        for src in sources:
            if ss[2] != tuple(src['z']['root_boundary']):
                continue
            if not all(len({Q[i] for i in ss[pos]})>=2 and valid_q_support(ss[pos],tuple(src[r]['forbidden'][col])) for n,r,col,pos,k in COMPONENTS):
                continue
            ids = {n: stable_schema_ids(tuple(src[r]['forbidden'][col]),ss[pos]) for n,r,col,pos,k in COMPONENTS if k==2}
            if not all(ids.values()):
                continue
            rec = dict(id=len(records),source_id=src['id'],geometry_id=gid,supports=ss,q_schema_ids=ids,
                       q_unary_relation=[src['z']['forbidden'][1]])
            ctx = context(rec,src)
            bans = [c['source_forbidden'] for c in ctx['components']]
            assert root_pairs(ctx,Q,bans)==[]
            rec['source_evidence'] = evidence(ctx,Q,bans)
            rec['targets'] = [] if rec['source_evidence']['eliminated'] else [row_evidence(ctx,row) for row in TARGETS]
            rec['status'] = 'source_excluded' if rec['source_evidence']['eliminated'] else 'retained'
            records.append(rec)
    # Same-source reflection and whole-component role exchange, without quotienting IDs.
    by_source = {key(s):s['id'] for s in sources}
    lookup = {(r['source_id'],r['supports']):r for r in records}
    transport_checks = minor_checks = reflection_checks = 0
    minor_certificates = []
    for rec in records:
        src = sources[rec['source_id']]
        i,c,az,aw = key(src)
        reflected = by_source[(tuple(RHO[x] for x in i),PI[c],tuple(tuple(sorted(PI[x] for x in f)) for f in az),tuple(tuple(sorted(PI[x] for x in f)) for f in aw))]
        twin = lookup[reflected,tuple(tuple(sorted(RHO[x] for x in s)) for s in rec['supports'])]
        assert twin['status']==rec['status']
        rec['reflected_id']=twin['id']
        exchanged = by_source[(i,c,az,aw[::-1])]
        other = lookup[exchanged,rec['supports'][:3]+rec['supports'][3:][::-1]]
        assert other['status']==rec['status']
        rec['w_component_swapped_id']=other['id']
        ctx = context(rec,src)
        evs = [rec['source_evidence']]
        for t in rec['targets']:
            raw = tuple(PI[t['row'][RHO[j]]] for j in range(5))
            tr = row_evidence(context(twin,sources[reflected]),raw)
            assert t['status']==tr['status']
            moved_joins = {
                tuple(tuple(sorted(PI[c] for c in f)) for f in j['forbidden_sets']):
                sorted((PI[a],PI[b]) for a,b in j['root_pairs']) for j in t['joins']}
            assert moved_joins == {tuple(j['forbidden_sets']):j['root_pairs'] for j in tr['joins']}
            reflection_checks += 1
            evs.extend(j['evidence'] for j in t['joins'] if j['evidence'])
            for comp, opt in zip(ctx['components'],t['components']):
                if not opt['exact']:
                    continue
                f = comp['source_forbidden']
                rels = ([rec['q_unary_relation']] if len(comp['contacts'])==1 else
                    [schemas[','.join(map(str,f))][sid] for sid in rec['q_schema_ids'][comp['name']]])
                for rel in rels:
                    moved = [tuple(opt['permutation'][v] for v in tup) for tup in rel]
                    assert tuple(sorted(set.intersection(*map(set,moved))))==opt['options'][0]
                    transport_checks+=1
        for ev in evs:
            if ev['eliminated'] and ev['frame']['witnesses']:
                for length in (1,3,5):
                    certificate = minor_control(ctx,ev['component'],ev['frame']['witnesses'][0],length=length)
                    if length == 1:
                        minor_certificates.append(certificate)
                    minor_checks+=1
    fibers = [dict(source_id=s['id'],retained_join_id=s['retained_join_id'],
        support_record_ids=[r['id'] for r in records if r['source_id']==s['id']]) for s in sources]
    for f in fibers:
        f['classification']='necessary_supports_present' if f['support_record_ids'] else 'no_compatible_disk_support'
    targets = [t for r in records for t in r['targets']]
    summary = dict(original_source_joins=len(sources),geometric_supports=len(geometry),
        placements=sum(map(len,geometry.values())),necessary_support_records=len(records),
        empty_source_fibers=sum(not f['support_record_ids'] for f in fibers),
        source_exclusions=sum(r['status']=='source_excluded' for r in records),
        retained_supports=sum(r['status']=='retained' for r in records),target_queries=len(targets),
        direct_accepts=sum(t['initial_status']=='accept' for t in targets),
        target_accepts=sum(t['status']=='accept' for t in targets),unresolved_queries=sum(t['status']!='accept' for t in targets),
        minor_controls=minor_checks,whole_relation_transports=transport_checks,literal_target_reflections=reflection_checks)
    assert (len(geometry), len(records), summary['source_exclusions'], len(targets)) == (780,608,584,48)
    assert summary['unresolved_queries'] == 0
    joins = {tuple(pair):i for i,pair in enumerate(original['abstract_conditions']['retained'])}
    swaps = [dict(source_id=s['id'],side_ids=s['side_ids'][::-1],retained_join_id=joins[s['side_ids'][::-1]]) for s in sources]
    old = set(previous['coverage_extension']['covered_source_join_ids'])
    added = {s['retained_join_id'] for s in sources+swaps}
    assert len(old)==1676 and len(added)==360 and not old & added
    covered = old|added
    remaining = {}
    for jid,(i,j) in enumerate(original['abstract_conditions']['retained']):
        label = '-'.join(sorted(side_kind(original['side_normal_forms'][k]) for k in (i,j)))
        if jid not in covered:
            remaining.setdefault(label,[]).append(jid)
    assert len(remaining)==6 and sum(map(len,remaining.values()))==1512
    frontier = [dict(retained_join_id=jid,side_ids=(i,j)) for jid,(i,j) in enumerate(original['abstract_conditions']['retained'])
        if (side_kind(original['side_normal_forms'][i]),side_kind(original['side_normal_forms'][j]))==('B','D')]
    assert len(frontier)==180
    # Controls against loss of a real component, support span, relation, or zw.
    ss = next(iter(sorted(geometry)))
    bad = list(ss); bad[1]=(ss[1][0],)
    assert tuple(bad) not in geometry
    bad = list(ss); bad[0]=(0,1,2,3)
    assert tuple(bad) not in geometry
    pair_relation=((0,1),(1,0))
    assert set.intersection(*map(set,pair_relation))=={0,1}
    assert set.intersection(*map(set,product({0,1},repeat=2)))==set()
    for src in sources:
        ez = U-{Q[i] for i in src['z']['root_boundary']}-set().union(*map(set,src['z']['forbidden']))
        ew = U-set().union(*map(set,src['w']['forbidden']))
        assert ez == ew == {src['z']['common']}
        assert list(product(ez,ew)) == [(src['z']['common'],src['z']['common'])]
        assert not [(a,b) for a,b in product(ez,ew) if a != b]
    negatives=['unary_is_not_spoke','four_positive_spans_limit_each_to_two','pair_relation_not_marginals','zw_diagonal_must_be_deleted']
    inputs = [SOURCE,PREVIOUS]+[ROOT/'scripts'/f'{n}.py' for n in (
        'c5_adjacent_degree5_no_mixed_ee','c5_adjacent_degree5_no_mixed_t2_t0_pairs',
        'c5_adjacent_degree5_no_mixed_t2_t1_bridge','c5_adjacent_degree5_singleton_long_arc',
        'c5_single_spoke_frame_arc','c5_single_spoke_two_two_minor','c5_root_degree_excess',
        'c5_single_spoke_cores','c5_adjacent_degree5_mixed_edge_shared','c5_single_spoke_two_two_external')]
    return dict(schema=1,scope='necessary supports and paper reduction; no realization or Lean theorem',
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in inputs},
        summary=summary,original_records=sources,root_swapped_sources=swaps,
        minor_certificates=minor_certificates,negative_controls=negatives,
        coverage_extension=dict(covered_source_join_ids=sorted(covered),newly_covered_source_join_ids=sorted(added),
            covered_source_joins=len(covered),remaining_source_joins=1512,covered_unordered_cells=9,
            remaining_unordered_cells=6,remaining_cells=remaining),
        next_frontier=dict(class_name='B-D',source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),records=frontier),source_fibers=fibers,geometries=gs,
        rotation_templates=[dict(order=o,rotations=r) for o,r in sorted(templates.items())],
        q_complete_binary_schemas=schemas,records=records,
        open_queries=[dict(record_id=r['id'],row=t['row']) for r in records for t in r['targets'] if t['status']!='accept'])


def render(data):
    lines=['# B–C 必要支援與原路徑證書','','必要表不是 disk 實現；空纖維不計作 target 接受。','',
           '| ID | 原 join | 支援 Cz/Dz/z0/Cw/Dw | source | targets |','| ---: | ---: | --- | --- | --- |']
    for r in data['records']:
        lines.append(f"| {r['id']} | {data['original_records'][r['source_id']]['retained_join_id']} | {' / '.join(''.join(map(str,s)) for s in r['supports'])} | {r['status']} | {', '.join(t['status'] for t in r['targets'])} |")
    lines += ['','[完整證書](observations.json)；[前提與界線](../../docs/c5_adjacent_degree5_no_mixed_bc.md)。','']
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data=build()
    for p,payload in ((OUT,json.dumps(data,sort_keys=True,indent=2)+'\n'),(OUT.with_name('support_table.md'),render(data))):
        if args.check:
            assert p.read_bytes()==payload.encode(),f'certificate differs: {p}'
        else:
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(payload)
    print(json.dumps(data['summary'],sort_keys=True))

if __name__=='__main__':
    main()
