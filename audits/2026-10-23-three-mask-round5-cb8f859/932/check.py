#!/usr/bin/env python3
"""Independent C-first full annulus and Q-geometry replay; no producer import."""
import argparse,copy,gzip,hashlib,itertools,json,subprocess,sys
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
R4='audits/2026-10-23-three-mask-round4-cb8f859/932/'
SRC='audits/2026-10-13-c9-932-source-d521163/frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz'
SPLITS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
def require(ok,msg):
    if not ok:raise AssertionError(msg)
def norm(w):
    names={};return tuple(names.setdefault(c,len(names)) for c in w)
def bits(mask):
    while mask:
        b=mask&-mask;yield b.bit_length()-1;mask-=b
def custody(strict=False):
    m=json.loads((HERE/'INPUTS.json').read_text());require(m['base']==BASE,'BASE');entry=json.loads((HERE.parent/'BASE.json').read_text());prior={r['path']:r for r in entry['predecessors']}
    for r in m['inputs']:
        blob=(HERE/r['frozen_path']).read_bytes();require((len(blob),hashlib.sha256(blob).hexdigest())==(r['bytes'],r['sha256']),'frozen bytes/SHA')
        require((REPO/r['path']).read_bytes()==blob,'immutable live drift: '+r['path'])
        if r['path'] in prior:require((r['bytes'],r['sha256'])==(prior[r['path']]['bytes'],prior[r['path']]['sha256']),'not round5 entry bytes')
        if r['authority']=='immutable exact Git BASE':require(subprocess.check_output(['git','show',BASE+':'+r['path']],cwd=REPO)==blob,'not exact Git BASE')
    drift=[]
    for r in m['routing_background']:
        blob=(HERE/r['frozen_path']).read_bytes();require((len(blob),hashlib.sha256(blob).hexdigest())==(r['bytes'],r['sha256']),'routing snapshot')
        if (REPO/r['path']).read_bytes()!=blob:drift.append(r['path'])
    if strict:require(not drift,'live routing entry drift')
    return {'immutable_files':len(m['inputs']),'immutable_authority_drift':[],'routing_background_drift':drift,'routing_policy':'strict' if strict else 'reported separately'}
def canonical_rows():
    result=[]
    def visit(w):
        if len(w)==9:
            if w[-1]!=w[0]:result.append(tuple(w))
            return
        for c in range(min(4,max(w,default=-1)+2)):
            if not w or c!=w[-1]:visit(w+[c])
    visit([]);require(len(result)==820,'all820 proper C9 rows');return result
def whole_options(rows):
    nc=[]
    def visit(p):
        if len(p)==9:
            if any(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b] for a,b,c,d in itertools.combinations(range(9),4)):return
            nc.append((tuple(p),tuple(sum(1<<i for i in range(9) if p[i]==j) for j in range(max(p)+1))));return
        for j in range(max(p)+2):visit(p+[j])
    visit([0]);require(len(nc)==4862,'all NC partitions');index={p:i for i,p in enumerate(rows)}
    @lru_cache(None)
    def allowed(left):
        return [(p,blocks) for p,blocks in nc if all((b&left) in [0,b] for b in blocks) and all(((left>>i&1)!=(left>>((i+1)%9)&1)) or p[i]==p[(i+1)%9] for i in range(9))]
    out=[]
    for row in rows:
        entry=[]
        for pairs in SPLITS:
            side=sum(1<<i for i,c in enumerate(row) if c in pairs[0]);swap={a:b for pair in pairs for a,b in [pair,pair[::-1]]};options=set()
            for p,blocks in allowed(side):
                orbit=0
                for selected in range(1<<len(blocks)):
                    word=tuple(swap[c] if selected>>p[i]&1 else c for i,c in enumerate(row));orbit|=1<<index[norm(word)]
                options.add(orbit)
            entry.append(sorted(options))
        out.append(entry)
    return out
def c_first_band(rows):
    index={r:i for i,r in enumerate(rows)};group=list(itertools.permutations(range(4)));images=set()
    for c in rows:
        allowed=[tuple(a for a in range(4) if a not in [c[i],c[(i+1)%9]]) for i in range(9)]
        for q in itertools.product(*allowed):
            if any(q[i]==q[(i+1)%9] for i in range(9)):continue
            target=norm(q);permutations=[g for g in group if tuple(g[x] for x in q)==target]
            require(len(permutations)==1,'odd proper Q must use at least three colors')
            for g in permutations:images.add(tuple(g[x] for x in c+q))
    fibres=[[[] for _ in rows] for _ in rows]
    for lift in sorted(images):fibres[index[lift[9:]]][index[norm(lift[:9])]].append(list(lift))
    sparse=[{str(i):len(f) for i,f in enumerate(line) if f} for line in fibres]
    require(all(sparse),'all820 Q rows have a complete C lift')
    require(len(images)==10798 and sum(map(len,sparse))==10657,'exact complete band size')
    return fibres,sparse
def prepare():
    src=json.loads(gzip.decompress((HERE/'frozen'/SRC).read_bytes()));rows=canonical_rows();require([list(w) for w in rows]==src['inner_pattern_order'],'original row order')
    options=whole_options(rows);require(options==src['kempe_obligations'],'independent full Q-Kempe options')
    fibres,sparse=c_first_band(rows);queries={q['query_id']:q for q in src['queries'] if q['target']==932 and q['geometry_id']=='induced' and q['status']=='necessary_condition_residual'}
    require(len(queries)==20,'complete20 original collars');return {'src':src,'rows':rows,'options':options,'fibres':fibres,'sparse':sparse,'queries':queries}
def small_caps(vertices,adj,faces,inc):
    cycles=set()
    for start in vertices:
        def walk(p):
            for w in adj[p[-1]]:
                if w==start and len(p)>=3:cycles.add(min(tuple(p),tuple([start]+list(reversed(p[1:])))))
                elif len(p)<5 and w>start and w not in p:walk(p+[w])
        walk([start])
    counts=Counter()
    for cy in cycles:
        cut={tuple(sorted((a,b))) for a,b in zip(cy,cy[1:]+cy[:1])};dual={i:set() for i in range(-1,len(faces))}
        for edge,sides in inc.items():
            if edge in cut:continue
            ff=[z[2] for z in sides];a,b=ff if len(ff)==2 else [ff[0],-1];dual[a].add(b);dual[b].add(a)
        seen={-1};todo=[-1]
        while todo:
            a=todo.pop()
            for b in dual[a]-seen:seen.add(b);todo.append(b)
        inside={v for i in set(range(len(faces)))-seen for v in faces[i]}-set(cy)
        if len(cy)<5:require(not inside,'occupied original C3/C4 control cap')
        elif inside:require(len(inside)==1 and set(cy)<=adj[next(iter(inside))],'non-W5 original C5 control cap')
        counts[str(len(cy))+'_empty' if not inside else '5_W5']+=1
    return dict(counts)
def mesh_control(mesh):
    C=mesh['C'];Q=mesh['Q'];deep=mesh['deep_vertices'];vertices=C+Q+deep;faces=mesh['oriented_faces'];adj={v:set() for v in vertices};inc=defaultdict(list);links={v:defaultdict(set) for v in vertices}
    require(len(vertices)==len(set(vertices))==23 and len(Q)==12 and len(deep)==2,'named noninduced control domain')
    for i,f in enumerate(faces):
        require(len(set(f))==3 and set(f)<=set(vertices),'simple original face')
        for a,b,c in [f,f[1:]+f[:1],f[2:]+f[:2]]:
            adj[a].add(b);adj[b].add(a);inc[tuple(sorted((a,b)))].append((a,b,i));links[a][b].add(c);links[a][c].add(b)
    boundary={tuple(sorted((a,b))) for a,b in zip(C,C[1:]+C[:1])}
    require({e for e in inc if set(e)<=set(C)}==boundary,'original C chord')
    for e,sides in inc.items():require((len(sides)==1 if e in boundary else len(sides)==2 and sides[0][:2]==sides[1][1::-1]),'original oriented side')
    for v,l in links.items():
        seen=set();todo=[next(iter(l))]
        while todo:
            w=todo.pop()
            if w not in seen:seen.add(w);todo.extend(l[w]-seen)
        require(seen==set(l),'full link connected');degrees=sorted(map(len,l.values()))
        require(degrees==([1,1]+[2]*(len(degrees)-2) if v in C else [2]*len(degrees)),'full original link path/cycle')
    require(len(vertices)-len(inc)+len(faces)==1,'disk Euler')
    require(all(len(adj[v])>=4 for v in C) and all(len(adj[v])>=5 for v in Q+deep),'full original degree')
    contacts={v:[i for i,c in enumerate(C) if c in adj[v]] for v in Q+deep}
    for i in range(9):require(contacts['t'+str(i)]==sorted([i,(i+1)%9]),'original face-third contacts')
    require(contacts['z0a']==contacts['z0b']==[0] and contacts['z4']==[4] and all(not contacts[v] for v in deep),'all single and deep contacts')
    qedges={tuple(sorted((a,b))) for a,b in zip(Q,Q[1:]+Q[:1])};chords={e for e in inc if set(e)<=set(Q)}-qedges
    require(chords==set(map(tuple,mesh['Q_chords'])) and len(chords)==3,'complete original Q chords')
    for a,b in chords:require(min(min(abs(i-j),9-abs(i-j)) for i in contacts[a] for j in contacts[b])>=3,'near-owner Q chord survived')
    jfaces=[f for f in faces if set(f)<=set(Q+deep)];jinc=defaultdict(list)
    for i,f in enumerate(jfaces):
        for a,b in zip(f,f[1:]+f[:1]):jinc[tuple(sorted((a,b)))].append(i)
    side_deep_counts=[]
    for chord in sorted(chords):
        dual={i:set() for i in range(len(jfaces))}
        for edge,ff in jinc.items():
            if edge!=chord and len(ff)==2:dual[ff[0]].add(ff[1]);dual[ff[1]].add(ff[0])
        unseen=set(dual);parts=[]
        while unseen:
            todo=[next(iter(unseen))];seen=set()
            while todo:
                v=todo.pop()
                if v not in seen:seen.add(v);todo.extend(dual[v]-seen)
            unseen-=seen;parts.append(seen)
        counts=sorted(len({v for i in p for v in jfaces[i]}&set(deep)) for p in parts)
        require(len(counts)==2 and min(counts)>=1,'chord side loses all deep points');side_deep_counts.append(counts)
    require(mesh['source_control']=='not triggered' and mesh['source_realized'] is False and mesh['induced_Q_inference']=='counterexample','source control status')
    return {'status':'counterexample','meaning':'Q need not be induced under all retained local degree/contact/cap conditions',
            'source':'not triggered','H_vertices':23,'s':3,'Q_length':12,'deep_vertices':2,'Q_chords':sorted(chords),
            'small_caps':small_caps(vertices,adj,faces,inc),'deep_counts_on_each_chord_side':side_deep_counts}
def variable_control(rec,rows):
    s=rec['s_by_C'];Q=[]
    for i in range(9):Q+=['t'+str(i)]+['z'+str((i+1)%9)+'_'+str(j+1) for j in range(s[(i+1)%9])]
    require(Q==rec['Q_order'] and len(rec['literal_Q'])==len(Q),'original variable Q order')
    word=rec['literal_Q'];require(all(word[i]!=word[(i+1)%len(Q)] for i in range(len(Q))),'proper literal variable Q')
    colors=dict(zip(Q,word));allowed=[]
    for i in range(9):
        link=['t'+str((i-1)%9)]+['z'+str(i)+'_'+str(j+1) for j in range(s[i])]+['t'+str(i)]
        allowed.append({c for c in range(4) if all(c!=colors[v] for v in link)})
    group=list(itertools.permutations(range(4)));literal_C=sorted({tuple(g[c] for c in row) for row in rows for g in group})
    lifts=[list(c)+word for c in literal_C if all(c[i] in allowed[i] for i in range(9))]
    require(lifts==rec['complete_C_plus_Q_full_lifts'],'variable single-contact complete literal full lifts')
    matrix=[[int(i==j) for j in range(4)] for i in range(4)]
    for a in allowed:
        factor=[[int(i in a and i!=j) for j in range(4)] for i in range(4)]
        matrix=[[sum(matrix[i][k]*factor[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
    trace=sum(matrix[i][i] for i in range(4));require(trace==len(lifts),'variable allowed-color transfer trace')
    if s==[1]+[0]*8:require(not lifts and rec['status']=='counterexample','empty-band proper Q guard')
    else:require(lifts and rec['status']=='triggered and holds','nonempty variable band calibration')
    return {'status':rec['status'],'s':sum(s),'Q_length':len(Q),'complete_C_lifts':trace,'all_literal_full_tuples_equal':True}
def verify(data,ctx):
    require(data['schema']=='C9-zero-single-annulus-exclusion-v1' and data['base']==BASE,'certificate identity')
    expected={'single_contact_total_minimum':1,'original_deep_vertices_minimum':2,'Q_chord_minimum_C_contact_distance':3,
              's0_original_collars_excluded':20,'Q_induced_claimed':False,'new_common_k_bound':False,'k_common_minimum_inherited':23,
              'general_932':'OPEN','zero_pair_h4_s_ge_1':'OPEN','smaller_bad':'OPEN','h_ge_5':'OPEN','K_infinity':'OPEN','new_Lean':False,
              'source_graph_controls':'not triggered','new_unconditional_C9_row_deletions':0}
    require(data['conclusions']==expected,'claim boundary');require(data['C_generic_order']==['c'+str(i) for i in range(9)] and data['Q_s0_order']==['t'+str(i) for i in range(9)],'ordered common contacts')
    require(data['s0_annulus_oriented_faces']==[['c'+str(i),'c'+str((i+1)%9),'t'+str(i)] for i in range(9)]+[['c'+str(i),'t'+str(i),'t'+str((i-1)%9)] for i in range(9)],'original s0 annulus faces')
    require(data['complete_s0_Q_then_C_row_fibres']==ctx['fibres'] and data['s0_sparse_Q_to_C_counts']==ctx['sparse'],'C-first all empty/full fibres and counts')
    prior=json.loads(gzip.decompress((HERE/'frozen'/R4/'certificate.json.gz').read_bytes()));require(data['case_bindings']==prior['case_bindings'],'all original collar identities')
    cases={c['id']:c for c in ctx['src']['cases']}
    for binding in data['case_bindings']:
        case=cases[ctx['queries'][binding['query_id']]['case_id']]
        sha=hashlib.sha256(json.dumps(case,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        require(binding['retained_frozen_case_sha256']==sha and binding['C9_original_names']==case['boundary_order'],'full original attachments/faces/rotation/fibres SHA')
    require(len(data['s0_traces'])==20,'all20 s0 hypotheses');seen=set();deletions=rounds=0;initial_counts=[]
    for trace in data['s0_traces']:
        qid=trace['query_id'];require(qid in ctx['queries'] and qid not in seen,'original query coverage');seen.add(qid);q=ctx['queries'][qid];support=q['fixed_point']
        require(trace['C_necessary_support']==support,'original C support')
        initial=sum(1<<i for i,row in enumerate(ctx['sparse']) if all(support>>int(j)&1 for j in row));require(trace['Q_initial']==initial and initial,'universal all-C-lift pullback')
        current=initial;initial_counts.append(current.bit_count())
        for turn in trace['rounds']:
            require(turn['before']==current,'same batch before support');remove=[]
            for p in bits(current):
                failed=[j for j,options in enumerate(ctx['options'][p]) if all(orbit&~current for orbit in options)]
                if failed:remove.append({'row':p,'failed_splits':failed})
            require(turn['removals']==remove and remove,'all complete whole-orbit failures');current&=~sum(1<<r['row'] for r in remove)
            require(turn['after']==current,'same batch after support');rounds+=1;deletions+=len(remove)
        require(trace['Q_final']==current==0,'s0 source hypothesis survived')
    types=[{'name':'T'+str(i),'C_contacts':[i,(i+1)%9]} for i in range(9)]+[{'name':'Z'+str(i),'C_contacts':[i]} for i in range(9)];require(data['contact_types']==types,'all original contact types')
    pairs=[]
    for a,b in itertools.combinations_with_replacement(range(18),2):
        if a==b and a<9:continue
        sep=min(min(abs(i-j),9-abs(i-j)) for i in types[a]['C_contacts'] for j in types[b]['C_contacts'])
        pairs.append({'endpoint_types':[a,b],'minimum_C_contact_distance':sep,'if_original_Q_chord_allowed_by_local_test':sep>=3})
    require(data['contact_type_pairs']==pairs,'all contact-type chord tests')
    require(len(data['variable_single_annulus_controls'])==2,'variable full-fibre controls')
    return {'s0_original_collars_excluded':20,'synchronous_batches':rounds,'conditional_Q_row_deletions':deletions,'Q_initial_sizes':dict(Counter(initial_counts)),
            'independent_NC_partitions':4862,'independent_complete_Kempe_options':sum(len(x) for r in ctx['options'] for x in r),
            'complete_s0_band_fibres':820*820,'empty_s0_band_fibres':820*820-10657,'nonzero_s0_band_entries':10657,'complete_s0_band_full_lifts':10798,
            'Q_rows_without_C_lift':0,'contact_type_pairs':len(pairs),'allowed_chord_type_pairs':sum(r['if_original_Q_chord_allowed_by_local_test'] for r in pairs),
            'noninduced_control':mesh_control(data['noninduced_Q_control']),
            'variable_single_controls':[variable_control(r,ctx['rows']) for r in data['variable_single_annulus_controls']],
            'single_contact_total_minimum':1,'deep_vertices_minimum':2,'source_realizability':'not triggered','remaining_s_ge_1':'OPEN','k_common_minimum_inherited':23,'new_common_k_bound':False}
def negatives(data,ctx):
    tests=[('drop_one_full_C_lift',lambda d:next(f for line in d['complete_s0_Q_then_C_row_fibres'] for f in line if f).pop()),
           ('omit_empty_fibre_domain',lambda d:d['complete_s0_Q_then_C_row_fibres'][0].pop()),
           ('existential_instead_of_all_lifts',lambda d:d['s0_traces'][0].update(Q_initial=1)),
           ('wrong_current_batch',lambda d:d['s0_traces'][0]['rounds'][0].update(before=0)),
           ('missing_original_collar',lambda d:d['s0_traces'].pop()),
           ('forget_whole_split',lambda d:d['s0_traces'][0]['rounds'][0]['removals'][0]['failed_splits'].pop()),
           ('invent_induced_Q',lambda d:d['conclusions'].update(Q_induced_claimed=True)),
           ('keep_only_one_deep_vertex',lambda d:d['conclusions'].update(original_deep_vertices_minimum=1)),
           ('erase_actual_Q_chord',lambda d:d['noninduced_Q_control']['Q_chords'].pop()),
           ('reverse_original_face_locally',lambda d:d['noninduced_Q_control']['oriented_faces'][0].reverse()),
           ('erase_empty_band_guard',lambda d:d['variable_single_annulus_controls'][0].update(status='triggered and holds')),
           ('promote_source_control',lambda d:d['conclusions'].update(source_graph_controls='triggered and holds'))]
    out=[]
    for name,mutate in tests:
        bad=copy.deepcopy(data);mutate(bad)
        try:verify(bad,ctx)
        except (AssertionError,ValueError,KeyError,IndexError,TypeError):out.append({'name':name,'status':'counterexample','result':'rejected as required'})
        else:raise AssertionError('negative accepted: '+name)
    p=subprocess.run([sys.executable,'-B',str(HERE/'check.py'),'--source',str(HERE/'certificate.json.gz')],capture_output=True)
    require(p.returncode==2 and b'unrecognized arguments: --source' in p.stderr,'unsupported source proposal');out.append({'name':'unsupported_named_source','status':'counterexample','result':'rejected as required'})
    return out
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--negative',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--check-entry-shared',action='store_true');args=p.parse_args()
    inputs=custody(args.check_entry_shared);ctx=prepare();data=json.loads(gzip.decompress((HERE/'certificate.json.gz').read_bytes()));result=verify(data,ctx)
    if args.negative:result['semantic_negative_controls']=negatives(data,ctx)
    print(json.dumps({'status':'PASS','frozen_input_check':inputs,**result},sort_keys=True))
if __name__=='__main__':main()
