#!/usr/bin/env python3
"""Independent, read-only fixed-boundary replay; never imports the producer.

Rebuilds all proper C9 rows, all noncrossing boundary component partitions,
whole Kempe orbits, literal three-anchor grids, complete annulus fibres, and
each current-support deletion. Arbitrary source proposals are unsupported.
"""
import argparse,copy,gzip,hashlib,itertools,json,subprocess,sys
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
PRED='audits/2026-10-23-three-mask-methods-cb8f859/932/'
SOURCE=PRED+'frozen/audits/2026-10-13-c9-932-source-d521163/frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz'
SPLITS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))

def require(ok,message):
    if not ok:raise AssertionError(message)

def norm(word):
    seen={};return tuple(seen.setdefault(v,len(seen)) for v in word)

def indices(mask):
    return [i for i in range(820) if mask>>i&1]

def custody(strict=False):
    ledger=json.loads((HERE/'INPUTS.json').read_text())
    require(ledger['base']==BASE,'BASE mismatch')
    for record in ledger['inputs']:
        blob=(HERE/record['frozen_path']).read_bytes()
        require(len(blob)==record['bytes'] and hashlib.sha256(blob).hexdigest()==record['sha256'],'frozen bytes/SHA: '+record['path'])
        require((REPO/record['path']).read_bytes()==blob,'immutable authority drift: '+record['path'])
        if record['authority'].startswith('immutable exact Git'):
            require(subprocess.check_output(['git','show',BASE+':'+record['path']],cwd=REPO)==blob,'not exact Git BASE')
    drift=[rec['path'] for rec in ledger['routing_background'] if hashlib.sha256((REPO/rec['path']).read_bytes()).hexdigest()!=rec['sha256']]
    if strict:require(not drift,'entry routing drift')
    return {'immutable_frozen_files':len(ledger['inputs']),'immutable_authority_drift':[],'routing_background_drift':drift,'routing_policy':'strict' if strict else 'reported separately'}

def canonical_rows(n):
    result=[]
    def extend(word):
        if len(word)==n:
            if word[-1]!=word[0]:result.append(tuple(word))
            return
        for color in range(min(3,max(word,default=-1)+1)+1):
            if not word or color!=word[-1]:extend(word+[color])
    extend([])
    return sorted(result)

def component_partitions():
    """Restricted-growth generation, unlike producer's frozen orbit lookup."""
    result=[]
    def extend(owner):
        if len(owner)==9:
            for a,b,c,d in itertools.combinations(range(9),4):
                if owner[a]==owner[c] and owner[b]==owner[d] and owner[a]!=owner[b]:return
            blocks=[sum(1<<i for i in range(9) if owner[i]==j) for j in range(max(owner)+1)]
            result.append((tuple(owner),tuple(blocks)))
            return
        for label in range(max(owner)+2):extend(owner+[label])
    extend([0])
    require(len(result)==4862,'all C9 noncrossing partitions')
    return result

def rebuild_obligations(rows):
    partitions=component_partitions();index={p:i for i,p in enumerate(rows)}
    @lru_cache(None)
    def options(left):
        valid=[]
        for owner,blocks in partitions:
            if any((block&left) not in (0,block) for block in blocks):continue
            if any(((left>>i&1)==(left>>((i+1)%9)&1)) and owner[i]!=owner[(i+1)%9] for i in range(9)):continue
            valid.append((owner,blocks))
        return valid
    table=[]
    for row in rows:
        record=[]
        for pairs in SPLITS:
            left=sum(1<<i for i,c in enumerate(row) if c in pairs[0])
            swap={a:b for pair in pairs for a,b in (pair,pair[::-1])};orbits=set()
            for owner,blocks in options(left):
                orbit=0
                for chosen in range(1<<len(blocks)):
                    word=tuple(swap[c] if chosen>>owner[i]&1 else c for i,c in enumerate(row))
                    orbit|=1<<index[norm(word)]
                orbits.add(orbit)
            require(orbits,'missing actual component option')
            record.append(sorted(orbits))
        table.append(record)
    return table

def annulus(case,rows,outer):
    result=[];columns=[]
    for row in rows:
        fibres=[[] for _ in outer]
        for b in itertools.product(range(4),repeat=5):
            if any(b[i]==b[(i+1)%5] for i in range(5)):continue
            if any(any(row[j]==b[i] for i in support) for j,support in enumerate(case['supports'])):continue
            fibres[outer.index(norm(b))].append(list(b)+list(row))
        result.append(fibres);columns.append(sum(1<<i for i,f in enumerate(fibres) if f))
    require(result==case['full_lifts_by_inner_then_outer_row'],'complete annulus fibres/full lifts including empties')
    require(columns==case['column_masks'],'annulus columns')
    return {'fibres':len(rows)*10,'empty_fibres':sum(not f for fs in result for f in fs),'full_lifts':sum(len(f) for fs in result for f in fs)}

def grid_for(rows,site):
    """Build each literal row from two paths first; normalize whole C9 last."""
    index={p:i for i,p in enumerate(rows)}
    # Enumerate ordered length-four paths between the fixed literal anchors.
    def paths(start,end):
        return [p for p in itertools.product(range(4),repeat=3) if all(a!=b for a,b in zip((start,)+p,p+(end,)))]
    aa=paths(1,2);bb=paths(2,0);grid=[]
    for a in aa:
        line=[]
        for b in bb:
            shifted=(0,1)+a+(2,)+b
            original=shifted[-site:]+shifted[:-site] if site else shifted
            line.append(index[norm(original)])
        grid.append(line)
    require(len(aa)==len(bb)==20 and len({x for line in grid for x in line})==400,'literal grid bijection')
    return {'triple_index':site,'literal_anchors':[0,1,2],'literal_t_color':3,'left_arc_words':[list(x) for x in aa],'right_arc_words':[list(x) for x in bb],'row_grid':grid}

def closure_maps(obligations,matrices):
    all_orbits={m for row in obligations for split in row for m in split};result=[]
    for matrix in matrices:
        grid=matrix['row_grid'];coords={p:(a,b) for a,line in enumerate(grid) for b,p in enumerate(line)}
        closed={}
        for orbit in all_orbits:
            places=[coords[p] for p in indices(orbit) if p in coords]
            aset={a for a,b in places};bset={b for a,b in places}
            mixed=sum(1<<grid[a][b] for a in aset for b in bset)
            closed[orbit]=orbit|mixed
        result.append(closed)
    return result

def ordinary_fixed_point(initial,obligations):
    current=initial
    while True:
        remove=[p for p in indices(current) if any(all(orbit&~current for orbit in opts) for opts in obligations[p])]
        if not remove:return current
        current&=~sum(1<<p for p in remove)

def prepare():
    source=json.loads(gzip.decompress((HERE/'frozen'/SOURCE).read_bytes()))
    rows=canonical_rows(9);require(len(rows)==820 and [list(r) for r in rows]==source['inner_pattern_order'],'all820 original C9 rows')
    outer=canonical_rows(5);require(len(outer)==10 and [list(r) for r in outer]==source['outer_pattern_order'],'all10 original C5 rows')
    obligations=rebuild_obligations(rows)
    require(obligations==source['kempe_obligations'],'independent whole Kempe orbit reconstruction')
    queries={q['query_id']:q for q in source['queries'] if q['target']==932 and q['geometry_id']=='induced' and q['status']=='necessary_condition_residual'}
    cases={c['id']:c for c in source['cases']};require(len(queries)==20,'exact original collar domain')
    fibre_stats=Counter()
    for q in queries.values():
        case=cases[q['case_id']];fibre_stats.update(annulus(case,rows,outer))
        initial=sum(1<<p for p,column in enumerate(case['column_masks']) if not column&~932)
        require(q['initial']==initial,'original transfer initial support')
        require(ordinary_fixed_point(initial,obligations)==q['fixed_point'],'inherited ordinary Kempe fixed point')
    matrices=[grid_for(rows,i) for i in range(9)]
    return {'source':source,'rows':rows,'obligations':obligations,'queries':queries,'cases':cases,'matrices':matrices,'closures':closure_maps(obligations,matrices),'fibre_stats':dict(fibre_stats)}

def verify(data,context):
    require(data['schema']=='C9-original-triple-rectangle-exclusion-v1' and data['base']==BASE,'certificate identity')
    expected={'original_triple_contacts':0,'excluded_original_case_site_hypotheses':180,'general_932_exclusion':False,'no_triple_h4_branch':'OPEN','k_common_minimum_inherited':23,'new_k_bound':False,'new_Lean':False,'source_graph_controls':'not triggered'}
    require(data['conclusions']==expected,'claim boundary')
    require(data['matrices']==context['matrices'],'literal three-distinct-anchor mixed-row grid')
    predecessor=json.loads((HERE/'frozen'/PRED/'certificate.json').read_text())
    require(data['case_bindings']==predecessor['case_bindings'],'full original names/rotation/attachment bindings')
    for binding in data['case_bindings']:
        q=context['queries'][binding['query_id']];case=context['cases'][q['case_id']]
        digest=hashlib.sha256(json.dumps(case,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        require(binding['retained_frozen_case_sha256']==digest and binding['C9_original_names']==case['boundary_order'],'original full annulus bytes')
    require(len(data['traces'])==180,'missing original case/site hypothesis')
    seen=set();rounds=0;deletions=0
    for trace in data['traces']:
        key=(trace['query_id'],trace['triple_index']);require(key not in seen and key[0] in context['queries'] and key[1] in range(9),'duplicate/foreign hypothesis');seen.add(key)
        support=context['queries'][key[0]]['fixed_point'];require(trace['initial']==support,'wrong original initial support')
        closed=context['closures'][key[1]]
        for turn in trace['rounds']:
            require(turn['before']==support,'current support changed')
            expected=[]
            for row in indices(support):
                bad=[s for s,opts in enumerate(context['obligations'][row]) if all(closed[o]&~support for o in opts)]
                if bad:expected.append({'row':row,'splits':bad})
            require(turn['removals']==expected and expected,'invalid or incomplete current-premise deletion round')
            support&=~sum(1<<entry['row'] for entry in expected);rounds+=1;deletions+=len(expected)
        require(support==trace['fixed_point']==0,'nonempty source support')
        require(trace['verdict']=='original triple-contact hypothesis excluded','wrong original-source verdict')
    require(seen==set(itertools.product(context['queries'],range(9))),'incomplete20x9 original domain')
    return {'original_collars':20,'original_triple_sites_each':9,'original_case_site_hypotheses_excluded':180,'independent_NC_component_partitions':4862,'whole_Kempe_options':sum(len(opts) for r in context['obligations'] for opts in r),'three_anchor_matrices':9,'each_matrix_shape':[20,20],'deletion_rounds':rounds,'conditional_row_deletions':deletions,'complete_original_annulus':context['fibre_stats'],'no_triple_branch':'OPEN','general_932':'OPEN','new_Lean':False}

def graph_lifts(vertices,edges,fixed):
    adjacency={v:set() for v in vertices}
    for a,b in edges:adjacency[a].add(b);adjacency[b].add(a)
    require(all(fixed[a]!=fixed[b] for a,b in edges if a in fixed and b in fixed),'improper control seed')
    colors=dict(fixed);answer=[]
    def visit():
        if len(colors)==len(vertices):answer.append(tuple(colors[v] for v in vertices));return
        v=max((v for v in vertices if v not in colors),key=lambda v:(len({colors[w] for w in adjacency[v] if w in colors}),len(adjacency[v]),v))
        forbidden={colors[w] for w in adjacency[v] if w in colors}
        for color in range(4):
            if color not in forbidden:colors[v]=color;visit();del colors[v]
    visit();return answer

def full_join_control():
    """One inherited named mesh, complete sets of lifts; not an original932 G."""
    predecessor=json.loads((HERE/'frozen'/PRED/'certificate.json').read_text())
    mesh=next(m for m in predecessor['geometric_controls'] if m['id']=='one_triple_m11')
    vertices=mesh['boundary']+mesh['private_vertices'];faces=mesh['oriented_faces']
    edges={tuple(sorted((a,b))) for face in faces for a,b in zip(face,face[1:]+face[:1])}
    plus=['t0']+['c'+str(i) for i in range(1,6)]+['t'+str(i) for i in range(1,5)]+['s0']
    minus=['t0']+['c'+str(i) for i in [5,6,7,8,0]]+['t'+str(i) for i in range(5,9)]+['s1']
    require(set(plus)&set(minus)=={'t0','c5'},'actual shared edge separator')
    ep={e for e in edges if set(e)<=set(plus)};em={e for e in edges if set(e)<=set(minus)}
    triangle={tuple(sorted(e)) for e in [('c0','c1'),('c1','t0'),('t0','c0')]}
    require(ep|em|triangle==edges and set(plus)|set(minus)==set(vertices),'all attachments/crossedges retained')
    lp=graph_lifts(plus,ep,{'t0':3,'c1':1,'c5':2});lm=graph_lifts(minus,em,{'t0':3,'c5':2,'c0':0})
    direct=set(graph_lifts(vertices,edges,{'c0':0,'c1':1,'c5':2,'t0':3}));joined=set()
    for p in lp:
        pd=dict(zip(plus,p))
        for m in lm:
            md=dict(zip(minus,m));require(all(pd[v]==md[v] for v in ('t0','c5')),'literal separator mismatch')
            joined.add(tuple((pd if v in pd else md)[v] for v in vertices))
    require(direct==joined,'Cartesian full lifts differ from whole graph')
    groups=Counter(tuple(word[vertices.index('c'+str(i))] for i in range(9)) for word in direct)
    aa=context_paths(1,2);bb=context_paths(2,0)
    counts=[[groups[(0,1)+a+(2,)+b] for b in bb] for a in aa]
    for a in range(20):
        for b in range(20):
            require(counts[a][b]==sum(1 for p in lp if tuple(dict(zip(plus,p))['c'+str(i)] for i in range(2,5))==aa[a])*sum(1 for m in lm if tuple(dict(zip(minus,m))['c'+str(i)] for i in range(6,9))==bb[b]),'complete rank-one count including empty fibre')
    return {'id':mesh['id'],'complete_932_global_minimal_source':'not triggered','cell_full_lifts':[len(lp),len(lm)],'whole_full_lifts':len(direct),'all_fixed_anchor_fibres':400,'empty_fibres':sum(v==0 for line in counts for v in line),'Cartesian_join_equals_direct_whole_graph':True}

def context_paths(start,end):
    return [p for p in itertools.product(range(4),repeat=3) if all(a!=b for a,b in zip((start,)+p,p+(end,)))]

def negatives(data,context):
    mutations=[]
    bad=copy.deepcopy(data);bad['traces'].pop();mutations.append(('missing_original_case_site',bad))
    bad=copy.deepcopy(data);bad['matrices'][0]['literal_anchors']=[0,1,0];mutations.append(('two_anchor_colors_misused_as_rank1',bad))
    bad=copy.deepcopy(data);bad['matrices'][0]['row_grid'][0][0]=bad['matrices'][0]['row_grid'][0][1];mutations.append(('independently_relabelled_mixed_row',bad))
    bad=copy.deepcopy(data);bad['traces'][0]['rounds'][0]['removals'].pop();mutations.append(('omitted_current_premise_deletion',bad))
    bad=copy.deepcopy(data);bad['case_bindings'][0]['C9_original_names'].reverse();mutations.append(('original_contact_rotation_reversed',bad))
    bad=copy.deepcopy(data);bad['conclusions']['general_932_exclusion']=True;mutations.append(('no_triple_branch_overclaimed',bad))
    rejected=[]
    for name,bad in mutations:
        try:verify(bad,context)
        except (AssertionError,KeyError,ValueError):rejected.append(name)
        else:raise AssertionError('negative accepted: '+name)
    process=subprocess.run([sys.executable,'-B',str(HERE/'check.py'),'--source',str(HERE/'certificate.json.gz')],capture_output=True)
    require(process.returncode==2 and b'unrecognized arguments: --source' in process.stderr,'unsupported source proposal accepted')
    rejected.append('unsupported_named_source_rejected')
    # The independent annulus comparison must reject missing empty and nonempty fibres.
    case=copy.deepcopy(context['cases'][context['queries'][next(iter(context['queries']))]['case_id']])
    for mode in ('empty','lift'):
        bad=copy.deepcopy(case)
        if mode=='empty':next(fs for fs in bad['full_lifts_by_inner_then_outer_row'] if any(not f for f in fs)).remove([])
        else:next(f for fs in bad['full_lifts_by_inner_then_outer_row'] for f in fs if f).pop()
        try:annulus(bad,context['rows'],[tuple(p) for p in context['source']['outer_pattern_order']])
        except AssertionError:rejected.append('deleted_annulus_'+mode+'_fibre')
        else:raise AssertionError('incomplete annulus accepted')
    return rejected

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--negative',action='store_true');parser.add_argument('--check-entry-shared',action='store_true');parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json.gz');args=parser.parse_args()
    inputs=custody(args.check_entry_shared);context=prepare();data=json.loads(gzip.decompress(args.certificate.read_bytes()))
    result={'status':'PASS','custody':inputs,**verify(data,context),'full_lift_geometric_control':full_join_control()}
    if args.negative:result['negative_controls_rejected']=negatives(data,context)
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
