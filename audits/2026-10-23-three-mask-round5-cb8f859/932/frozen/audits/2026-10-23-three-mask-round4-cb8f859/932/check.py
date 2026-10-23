#!/usr/bin/env python3
"""Independent read-only literal-first folded-separator replay; no producer import."""
import argparse,copy,gzip,hashlib,itertools,json,math,subprocess,sys
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
R3='audits/2026-10-23-three-mask-round3-cb8f859/932/'
T2='audits/2026-10-13-c9-932-source-d521163/'
SOURCE=T2+'frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz'
SPLITS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
POLICY='all complete boundary orbits; every failed split rejects every option using the same before support'

def require(ok,message):
    if not ok:raise AssertionError(message)

def norm(word):
    names={};return tuple(names.setdefault(v,len(names)) for v in word)

def bits(mask):
    while mask:
        low=mask&-mask;yield low.bit_length()-1;mask-=low

def custody(strict=False):
    ledger=json.loads((HERE/'INPUTS.json').read_text());require(ledger['base']==BASE,'input BASE')
    entry=json.loads((HERE.parent/'BASE.json').read_text());predecessors={r['path']:r for r in entry['predecessors']}
    for r in ledger['inputs']:
        blob=(HERE/r['frozen_path']).read_bytes();digest=hashlib.sha256(blob).hexdigest()
        require((len(blob),digest)==(r['bytes'],r['sha256']),'frozen bytes/SHA: '+r['path'])
        require((REPO/r['path']).read_bytes()==blob,'immutable authority drift: '+r['path'])
        if r['path'] in predecessors:
            require((r['bytes'],r['sha256'])==(predecessors[r['path']]['bytes'],predecessors[r['path']]['sha256']),'not round4 entry predecessor bytes')
        if r['authority']=='immutable exact Git BASE':
            require(subprocess.check_output(['git','show',BASE+':'+r['path']],cwd=REPO)==blob,'not exact Git BASE')
    drift=[]
    for r in ledger['routing_background']:
        blob=(HERE/r['frozen_path']).read_bytes()
        require((len(blob),hashlib.sha256(blob).hexdigest())==(r['bytes'],r['sha256']),'routing snapshot drift')
        if (REPO/r['path']).read_bytes()!=blob:drift.append(r['path'])
    if strict:require(not drift,'live routing entry drift')
    return {'immutable_files':len(ledger['inputs']),'immutable_authority_drift':[],
            'routing_background_drift':drift,'routing_policy':'strict' if strict else 'reported separately'}

def canonical_rows(n):
    result=[]
    def extend(word):
        if len(word)==n:
            if word[-1]!=word[0]:result.append(tuple(word))
            return
        for c in range(min(3,max(word,default=-1)+1)+1):
            if not word or c!=word[-1]:extend(word+[c])
    extend([]);return sorted(result)

def noncrossing_partitions():
    answer=[]
    def visit(owner):
        if len(owner)==9:
            for a,b,c,d in itertools.combinations(range(9),4):
                if owner[a]==owner[c] and owner[b]==owner[d] and owner[a]!=owner[b]:return
            blocks=tuple(sum(1<<i for i in range(9) if owner[i]==j) for j in range(max(owner)+1))
            answer.append((tuple(owner),blocks));return
        for j in range(max(owner)+2):visit(owner+[j])
    visit([0]);require(len(answer)==4862,'complete C9 NC partitions');return answer

def whole_options(rows):
    partitions=noncrossing_partitions();lookup={p:i for i,p in enumerate(rows)}
    @lru_cache(None)
    def usable(left):
        out=[]
        for owner,blocks in partitions:
            if any((block&left) not in [0,block] for block in blocks):continue
            if any(((left>>i&1)==(left>>((i+1)%9)&1)) and owner[i]!=owner[(i+1)%9] for i in range(9)):continue
            out.append((owner,blocks))
        return out
    answer=[]
    for word in rows:
        entries=[]
        for pairs in SPLITS:
            left=sum(1<<i for i,c in enumerate(word) if c in pairs[0]);swap={a:b for pair in pairs for a,b in [pair,pair[::-1]]};options=set()
            for owner,blocks in usable(left):
                orbit=0
                for selection in range(1<<len(blocks)):
                    changed=tuple(swap[c] if selection>>owner[i]&1 else c for i,c in enumerate(word))
                    orbit|=1<<lookup[norm(changed)]
                options.add(orbit)
            require(options,'actual whole option missing');entries.append(sorted(options))
        answer.append(entries)
    return answer

def literal_first_grid(rows,site,equal):
    """Generate complete literal C9 words first, then classify both arc group orbits."""
    endpoint=0 if equal else 1;group=[g for g in itertools.permutations(range(4)) if g[0]==0 and g[endpoint]==endpoint]
    index={p:i for i,p in enumerate(rows)};paths=[];classes=[]
    for length,start,end in [(3,0,endpoint),(4,endpoint,0)]:
        words=[w for w in itertools.product(range(4),repeat=length) if all(a!=b for a,b in zip((start,)+w,w+(end,)))]
        paths.append(words);orbit_by_word={w:tuple(sorted({tuple(g[c] for c in w) for g in group})) for w in words}
        classes.append(sorted(set(orbit_by_word.values())))
    left={w:i for i,orbit in enumerate(classes[0]) for w in orbit};right={w:i for i,orbit in enumerate(classes[1]) for w in orbit}
    cells=[[set() for _ in classes[1]] for _ in classes[0]]
    for u,v in itertools.product(*paths):
        shifted=(0,)+u+(endpoint,)+v;literal=shifted[-site:]+shifted[:-site] if site else shifted
        cells[left[u]][right[v]].add(index[norm(literal)])
    coordinates={}
    for a,line in enumerate(cells):
        for b,options in enumerate(line):
            require(options,'empty structural OR cell')
            for p in options:
                require(p not in coordinates,'raw row occurs in two OR cells');coordinates[p]=(a,b)
    expected={i for i,row in enumerate(rows) if (row[site]==row[(site+4)%9])==equal}
    require(set(coordinates)==expected,'literal-first complete folded domain')
    require([len(classes[0]),len(classes[1]),len(coordinates)]==([4,10,210] if equal else [10,31,610]),'folded grid sizes')
    record={'site':site,'anchor_mode':'equal' if equal else 'distinct','literal_anchors':[0,endpoint],
            'whole_color_group':[list(g) for g in group],
            'left_arc_orbits':[[list(w) for w in orbit] for orbit in classes[0]],
            'right_arc_orbits':[[list(w) for w in orbit] for orbit in classes[1]],
            'row_options_grid':[[sorted(s) for s in line] for line in cells]}
    return record,([[sum(1<<p for p in opts) for opts in line] for line in cells],coordinates)

def annulus(case,rows,outer):
    proper_outer=[b for b in itertools.product(range(4),repeat=5) if all(b[i]!=b[(i+1)%5] for i in range(5))]
    output=[];columns=[]
    for row in rows:
        fibres=[[] for _ in outer]
        for b in proper_outer:
            if any(any(row[j]==b[i] for i in support) for j,support in enumerate(case['supports'])):continue
            fibres[outer.index(norm(b))].append(list(b)+list(row))
        output.append(fibres);columns.append(sum(1<<i for i,f in enumerate(fibres) if f))
    require(output==case['full_lifts_by_inner_then_outer_row'] and columns==case['column_masks'],'original full annulus fibres/lifts including empties')
    return {'fibres':len(rows)*10,'empty_fibres':sum(not f for ff in output for f in ff),'full_lifts':sum(len(f) for ff in output for f in ff)}

def prepare():
    src=json.loads(gzip.decompress((HERE/'frozen'/SOURCE).read_bytes()));rows=canonical_rows(9);outer=canonical_rows(5)
    require([list(r) for r in rows]==src['inner_pattern_order'] and len(rows)==820,'all820 original C9 rows')
    require([list(r) for r in outer]==src['outer_pattern_order'] and len(outer)==10,'all10 original C5 rows')
    options=whole_options(rows);require(options==src['kempe_obligations'],'independent complete whole-Kempe options')
    queries={q['query_id']:q for q in src['queries'] if q['target']==932 and q['geometry_id']=='induced' and q['status']=='necessary_condition_residual'}
    require(len(queries)==20,'exact20 original source contracts');cases={c['id']:c for c in src['cases']};stats=Counter()
    for q in queries.values():stats.update(annulus(cases[q['case_id']],rows,outer))
    grids=[];contexts={}
    for site in range(9):
        contexts[site]=[]
        for equal in [False,True]:
            grid,context=literal_first_grid(rows,site,equal);grids.append(grid);contexts[site].append(context)
    @lru_cache(None)
    def requirements(site,orbit):
        needed=[]
        for mode,(cells,coordinates) in enumerate(contexts[site]):
            aa=set();bb=set()
            for row in bits(orbit):
                if row in coordinates:
                    a,b=coordinates[row];aa.add(a);bb.add(b)
            for a in sorted(aa):
                for b in sorted(bb):needed.append((mode,a,b,cells[a][b]))
        return tuple(needed)
    return {'src':src,'rows':rows,'queries':queries,'cases':cases,'options':options,'grids':grids,'requirements':requirements,'annulus':dict(stats)}

def verify(data,ctx):
    require(data['schema']=='C9-folded-separator-exclusion-v1' and data['base']==BASE,'certificate identity')
    expected={'original_distance_four_centres':0,'original_case_pair_hypotheses_excluded':180,
              'original_case_pair_multiplicity_hypotheses_excluded':360,'remaining_contact_templates_each_collar':1,
              'remaining_named_zero_pair_templates':20,'new_unconditional_C9_row_deletions':0,
              'zero_pair_h4_branch':'OPEN','general_932':'OPEN','h_ge_5':'OPEN','smaller_bad':'OPEN','K_infinity':'OPEN',
              'new_Lean':False,'k_common_minimum_inherited':23,'new_k_bound':False,'source_graph_controls':'not triggered'}
    require(data['conclusions']==expected,'claim boundary');require(data['whole_option_policy']==POLICY,'whole orbit or OR-cell semantics lost')
    require(data['grids']==ctx['grids'],'literal-first folded OR map/group multiplicities')
    prior=json.loads((HERE/'frozen'/R3/'certificate.json').read_text())
    require(data['case_bindings']==prior['case_bindings'],'inherited original names/rotation/attachments bindings')
    for binding in data['case_bindings']:
        query=ctx['queries'][binding['query_id']];case=ctx['cases'][query['case_id']]
        digest=hashlib.sha256(json.dumps(case,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        require(binding['retained_frozen_case_sha256']==digest and binding['C9_original_names']==case['boundary_order'],'complete original case SHA/order')
    require(len(data['traces'])==180,'missing original case/pair hypothesis');seen=set();rounds=deletions=0;rejections=Counter()
    def reason(orbit,support,site):
        if orbit&~support:return 'whole orbit has an absent row'
        for mode,a,b,mask in ctx['requirements'](site,orbit):
            if not(mask&support):return 'complete folded OR cell is empty'
        return None
    for trace in data['traces']:
        key=trace['query_id'],trace['site'];require(key[0] in ctx['queries'] and key[1] in range(9) and key not in seen,'duplicate/foreign hypothesis');seen.add(key)
        require(trace['original_center_multiplicities']==[1,2],'one/two-center coverage')
        support=ctx['queries'][key[0]]['fixed_point'];require(support and trace['initial']==support,'empty/altered original query initial support')
        for turn in trace['rounds']:
            require(turn['before']==support,'batch current-support premise');expected_remove=[]
            for row in bits(support):
                failed=[]
                for split,options in enumerate(ctx['options'][row]):
                    reasons=[reason(orbit,support,key[1]) for orbit in options]
                    if all(r is not None for r in reasons):failed.append(split);rejections.update(reasons)
                if failed:expected_remove.append({'row':row,'failed_splits':failed})
            require(turn['removals']==expected_remove and expected_remove,'invalid/incomplete simultaneous necessary row deletion')
            support&=~sum(1<<r['row'] for r in expected_remove)
            require(turn['after']==support,'wrong batch after support');rounds+=1;deletions+=len(expected_remove)
        require(support==trace['fixed_point']==0,'distance-four source support survived')
        require(trace['verdict']=='both original distance-four centre hypotheses excluded','hypothesis verdict')
    require(seen==set(itertools.product(ctx['queries'],range(9))),'incomplete20x9 hypothesis domain')
    return {'original_collars':20,'original_pair_positions_each':9,'case_pair_hypotheses_excluded':180,
            'case_pair_multiplicity_hypotheses_excluded':360,'synchronous_deletion_rounds':rounds,'conditional_row_deletions':deletions,
            'whole_option_rejections_in_failed_splits':dict(rejections),'independent_NC_partitions':4862,
            'independent_whole_Kempe_options':sum(len(s) for r in ctx['options'] for s in r),
            'folded_maps':18,'distinct_anchor_shape':[10,31],'equal_anchor_shape':[4,10],
            'complete_original_annulus':ctx['annulus'],'remaining_named_zero_pair_templates':20,
            'new_unconditional_C9_row_deletions':0,'source_realizability':'not triggered','zero_pair_h4_branch':'OPEN',
            'k_common_minimum_inherited':23,'new_k_bound':False,'new_Lean':False}

def full_lifts(vertices,edges,fixed):
    adj={v:set() for v in vertices}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    colors=dict(fixed);result=[]
    def extend():
        if len(colors)==len(vertices):result.append(tuple(colors[v] for v in vertices));return
        v=max((v for v in vertices if v not in colors),key=lambda v:(len({colors[w] for w in adj[v] if w in colors}),len(adj[v]),v))
        forbidden={colors[w] for w in adj[v] if w in colors}
        for c in range(4):
            if c not in forbidden:colors[v]=c;extend();del colors[v]
    extend();return result

def control(mesh,equal,grid):
    two=len(mesh['distance_four_vertices'])==2;y='y' if two else 'x';vertices=mesh['boundary']+mesh['private_vertices']
    edges={tuple(sorted((a,b))) for f in mesh['oriented_faces'] for a,b in zip(f,f[1:]+f[:1])};anchors={'c0':0,'c4':0 if equal else 1}
    plus=['c'+str(i) for i in range(5)]+['x']+['t'+str(i) for i in range(4)]+['s0']
    minus=['c'+str(i) for i in [4,5,6,7,8,0]]+[y]+['t'+str(i) for i in range(4,9)]+['s1']
    ep={e for e in edges if set(e)<=set(plus)};em={e for e in edges if set(e)<=set(minus)}
    require(ep|em|({('x','y')} if two else set())==edges,'original separator attachments lost')
    available=[c for c in range(4) if c not in anchors.values()];left={};right={};joined=set()
    for c in available:
        left[c]=full_lifts(plus,ep,{**anchors,'x':c});right[c]=full_lifts(minus,em,{**anchors,y:c})
    for k in available:
        for l in available:
            if (k!=l)!=two:continue
            for a,b in itertools.product(left[k],right[l]):
                coloring=dict(zip(plus,a));other=dict(zip(minus,b))
                require(all(coloring[v]==other[v] for v in set(plus)&set(minus)),'independent literal frame')
                coloring.update(other);joined.add(tuple(coloring[v] for v in vertices))
    direct=set(full_lifts(vertices,edges,anchors));require(joined==direct,'Cartesian sector union versus direct whole full tuples')
    raw=Counter()
    for lift in direct:
        u=tuple(lift[vertices.index('c'+str(i))] for i in [1,2,3]);v=tuple(lift[vertices.index('c'+str(i))] for i in [5,6,7,8]);raw[u,v]+=1
    def arc_counts(lifts,names,graph_vertices):
        return Counter(tuple(t[graph_vertices.index(v)] for v in names) for t in lifts)
    aa=sum((arc_counts(lifts,['c1','c2','c3'],plus) for lifts in left.values()),Counter())
    bb=sum((arc_counts(lifts,['c5','c6','c7','c8'],minus) for lifts in right.values()),Counter())
    coefficient=math.factorial(len(available)-1)*(len(available)-1 if two else 1);averaged=[]
    for uorbit in grid['left_arc_orbits']:
        u=tuple(uorbit[0]);line=[]
        for vorbit in grid['right_arc_orbits']:
            v=tuple(vorbit[0]);value=sum(raw[u,tuple(g[c] for c in v)] for g in grid['whole_color_group'])
            require(value==coefficient*aa[u]*bb[v],'group-average factorization with orbit multiplicities')
            line.append(value)
        averaged.append(line)
    pivot=next(( (i,j) for i,line in enumerate(averaged) for j,v in enumerate(line) if v),None);require(pivot is not None,'empty full-lift control')
    a,b=pivot
    require(all(averaged[i][j]*averaged[a][b]==averaged[i][b]*averaged[a][j] for i in range(len(averaged)) for j in range(len(averaged[0]))),'folded averaged matrix not rank one')
    all_u=[tuple(w) for orbit in grid['left_arc_orbits'] for w in orbit];all_v=[tuple(w) for orbit in grid['right_arc_orbits'] for w in orbit]
    def boundary_fibres(lifts):
        answer=defaultdict(set);positions=[vertices.index(c) for c in mesh['boundary']]
        for t in lifts:answer[tuple(t[i] for i in positions)].add(t)
        return answer
    direct_fibres=boundary_fibres(direct);joined_fibres=boundary_fibres(joined);empty=0
    for u,v in itertools.product(all_u,all_v):
        word=(0,)+u+(anchors['c4'],)+v;actual=direct_fibres[word];assembled=joined_fibres[word]
        require(actual==assembled,'complete boundary fibre including empties');empty+=not actual
    raw_minor=None
    if not equal:
        u,u1=(1,0,2),(1,0,3);v,v1=(0,1,0,1),(0,2,0,3)
        minor=[[raw[x,y] for y in [v,v1]] for x in [u,u1]];det=minor[0][0]*minor[1][1]-minor[0][1]*minor[1][0]
        require(det in [16,-16],'raw rank-one counterexample');raw_minor={'status':'counterexample','matrix':minor,'determinant':det}
    return {'status':'triggered and holds','complete_source':'not triggered','anchors':anchors,'whole_full_lifts':len(direct),
            'complete_boundary_fibres':len(all_u)*len(all_v),'empty_boundary_fibres':empty,'group_size':len(grid['whole_color_group']),
            'group_average_coefficient':coefficient,'averaged_folded_shape':[len(averaged),len(averaged[0])],
            'group_average_rank_one':True,'direct_join_full_tuple_set_equal':True,'raw_rank_one_inference':raw_minor}

def controls(ctx):
    prior=json.loads((HERE/'frozen'/R3/'certificate.json').read_text());result={}
    for mesh in prior['geometric_controls']:
        result[mesh['id']]={}
        for equal in [False,True]:
            grid=next(g for g in ctx['grids'] if g['site']==0 and g['anchor_mode']==('equal' if equal else 'distinct'))
            result[mesh['id']][grid['anchor_mode']]=control(mesh,equal,grid)
    return result

def negatives(data,ctx):
    changed=[]
    def mutate(name,fn):
        d=copy.deepcopy(data);fn(d);changed.append((name,d))
    mutate('missing_equal_anchor_group',lambda d:d['grids'].pop())
    mutate('OR_cell_loses_one_literal_option',lambda d:next(x for g in d['grids'] for line in g['row_options_grid'] for x in line if len(x)>1).pop())
    mutate('independent_sector_color_permutation',lambda d:d['grids'][0]['whole_color_group'][1].reverse())
    mutate('orbit_multiplicities_erased',lambda d:d['grids'][1]['whole_color_group'].pop())
    mutate('OR_cell_read_as_each_member_positive',lambda d:d.update(whole_option_policy='every member of every OR cell is positive'))
    mutate('initial_query_support_omitted',lambda d:d['traces'][0].update(initial=0))
    mutate('batch_uses_future_support',lambda d:d['traces'][0]['rounds'][0].update(before=0))
    mutate('missing_whole_orbit_failed_split',lambda d:d['traces'][0]['rounds'][0]['removals'][0]['failed_splits'].pop())
    mutate('wrong_batch_after',lambda d:d['traces'][0]['rounds'][0].update(after=0))
    mutate('missing_original_case_pair',lambda d:d['traces'].pop())
    mutate('one_center_only_coverage',lambda d:d['traces'][0].update(original_center_multiplicities=[1]))
    mutate('source_control_overclaimed',lambda d:d['conclusions'].update(source_graph_controls='triggered and holds'))
    mutate('zero_pair_branch_overexcluded',lambda d:d['conclusions'].update(zero_pair_h4_branch='excluded'))
    mutate('original_order_changed',lambda d:d['case_bindings'][0]['C9_original_names'].reverse())
    rejected=[]
    for name,d in changed:
        try:verify(d,ctx)
        except (AssertionError,KeyError,ValueError,TypeError,IndexError):rejected.append({'name':name,'status':'counterexample','result':'rejected as required'})
        else:raise AssertionError('negative accepted: '+name)
    proc=subprocess.run([sys.executable,'-B',str(HERE/'check.py'),'--source',str(HERE/'certificate.json.gz')],capture_output=True)
    require(proc.returncode==2 and b'unrecognized arguments: --source' in proc.stderr,'unsupported source proposal accepted')
    rejected.append({'name':'unsupported_named_source','status':'counterexample','result':'rejected as required'})
    return rejected

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--negative',action='store_true')
    parser.add_argument('--check-entry-shared',action='store_true');args=parser.parse_args()
    inputs=custody(args.check_entry_shared);ctx=prepare();data=json.loads(gzip.decompress((HERE/'certificate.json.gz').read_bytes()))
    result=verify(data,ctx);result['complete_full_lift_group_average_controls']=controls(ctx)
    if args.negative:result['semantic_negative_controls']=negatives(data,ctx)
    print(json.dumps({'status':'PASS','frozen_input_check':inputs,**result},sort_keys=True))

if __name__=='__main__':main()
