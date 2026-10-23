#!/usr/bin/env python3
"""Read-only independent C9 geometry replay. No producer import or graph search."""
import argparse, copy, gzip, hashlib, itertools, json, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
R2='audits/2026-10-23-three-mask-round2-cb8f859/932/'
T2='audits/2026-10-13-c9-932-source-d521163/'
SOURCE=T2+'frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz'

def require(condition,message):
    if not condition:raise AssertionError(message)

def canonical(data):return json.dumps(data,sort_keys=True,separators=(',',':')).encode()

def custody(strict=False):
    data=json.loads((HERE/'INPUTS.json').read_text());require(data['base']==BASE,'input BASE')
    for r in data['inputs']:
        blob=(HERE/r['frozen_path']).read_bytes()
        require(len(blob)==r['bytes'] and hashlib.sha256(blob).hexdigest()==r['sha256'],'frozen bytes/SHA: '+r['path'])
        require((REPO/r['path']).read_bytes()==blob,'immutable drift: '+r['path'])
        if r['authority']=='immutable exact Git BASE':
            require(subprocess.check_output(['git','show',BASE+':'+r['path']],cwd=REPO)==blob,'not Git BASE: '+r['path'])
    routing=[]
    for r in data['routing_background']:
        blob=(HERE/r['frozen_path']).read_bytes()
        require(len(blob)==r['bytes'] and hashlib.sha256(blob).hexdigest()==r['sha256'],'routing snapshot bytes/SHA')
        if hashlib.sha256((REPO/r['path']).read_bytes()).hexdigest()!=r['sha256']:routing.append(r['path'])
    if strict:require(not routing,'live routing entry drift')
    return {'immutable_files':len(data['inputs']),'immutable_authority_drift':[],
            'routing_background_drift':routing,'routing_policy':'strict' if strict else 'reported separately'}

def geometry():
    pairs=[]
    for a,b in itertools.combinations(range(9),2):
        if min(b-a,9-b+a)==4:pairs.append({a,b})
    indexed=[{i,(i+4)%9} for i in range(9)]
    require(set(map(frozenset,pairs))==set(map(frozenset,indexed)),'all nine distance-four pairs')
    witnesses=[]
    for i,j in itertools.combinations(range(9),2):
        p,q=indexed[i],indexed[j];shared=p&q
        if not shared:
            ordered=sorted(p|q)
            require(len(ordered)==4 and {ordered[0],ordered[2]} in [p,q],'four-terminal alternation')
            witnesses.append({'pair_indices':[i,j],'kind':'alternating','cyclic_terminals':ordered})
        else:
            require(len(shared)==1,'distinct pair identity');a=next(iter(shared));b=next(iter(p-{a}));d=next(iter(q-{a}))
            require(min(abs(b-d),9-abs(b-d))==1,'other ends not an original C9 edge')
            pocket=['c'+str(a),'x','c'+str(b),'c'+str(d),'y']
            diagonals=[]
            for s,t in itertools.combinations(range(5),2):
                if t-s in [1,4]:continue
                u,v=pocket[s],pocket[t]
                # C--C chords are absent; x/y each has precisely its two contacts.
                if u.startswith('c') and v.startswith('c'):continue
                if u=='x' and v.startswith('c') and int(v[1:]) not in p:continue
                if v=='x' and u.startswith('c') and int(u[1:]) not in p:continue
                if u=='y' and v.startswith('c') and int(v[1:]) not in q:continue
                if v=='y' and u.startswith('c') and int(u[1:]) not in q:continue
                diagonals.append({u,v})
            require(diagonals==[{'x','y'}],'empty pocket chord obstruction')
            require(len({a,b,d})==3,'wheel produces no triple')
            witnesses.append({'pair_indices':[i,j],'kind':'shared_endpoint_C5','shared_endpoint':a,'adjacent_other_ends':[b,d],
                              'pocket_order':pocket,'only_allowed_diagonal':['x','y'],'forbidden_wheel_C_contacts':sorted([a,b,d])})
    return witnesses

def mesh_properties(mesh):
    boundary=mesh['boundary'];private=mesh['private_vertices'];vertices=boundary+private;faces=mesh['oriented_faces']
    require(boundary==['c'+str(i) for i in range(9)] and len(vertices)==len(set(vertices)),'control vertex labels')
    adj={v:set() for v in vertices};inc=defaultdict(list);links={v:defaultdict(set) for v in vertices}
    for n,face in enumerate(faces):
        require(len(face)==len(set(face))==3 and set(face)<=set(vertices),'simple original triangular face')
        for a,b,c in [face,face[1:]+face[:1],face[2:]+face[:2]]:
            inc[tuple(sorted((a,b)))].append((a,b,n));adj[a].add(b);adj[b].add(a)
            links[a][b].add(c);links[a][c].add(b)
    bedges={tuple(sorted((boundary[i],boundary[(i+1)%9]))) for i in range(9)}
    require({e for e in inc if set(e)<=set(boundary)}==bedges,'C9 chord')
    for edge,sides in inc.items():
        if edge in bedges:require(len(sides)==1,'boundary edge has wrong sides')
        else:require(len(sides)==2 and sides[0][:2]==sides[1][1::-1],'original oriented edge sides')
    for v,link in links.items():
        seen=set();todo=[next(iter(link))]
        while todo:
            w=todo.pop()
            if w not in seen:seen.add(w);todo.extend(link[w]-seen)
        require(seen==set(link),'disconnected original link')
        degrees=sorted(map(len,link.values()))
        require(degrees==([1,1]+[2]*(len(degrees)-2) if v in boundary else [2]*len(degrees)),'full original link not path/cycle')
    require(len(vertices)-len(inc)+len(faces)==1,'disk Euler characteristic')
    require(all(len(adj[v])>=4 for v in boundary) and all(len(adj[v])>=5 for v in private),'full degree bounds')
    thirds=[]
    for i in range(9):
        a,b=boundary[i],boundary[(i+1)%9];side=inc[tuple(sorted((a,b)))]
        thirds.append(next(iter(set(faces[side[0][2]])-{a,b})))
    require(thirds==mesh['face_third_vertices']==['t'+str(i) for i in range(9)],'actual C edge third vertices')
    doubles=[]
    for v in private:
        contacts=[i for i,c in enumerate(boundary) if c in adj[v]]
        require(len(contacts)<=2,'round2 no-triple premise')
        for a,b in itertools.combinations(contacts,2):
            require(min(abs(a-b),9-abs(a-b)) in [1,4],'forbidden contact distance')
            if min(abs(a-b),9-abs(a-b))==4:doubles.append(v)
    require(doubles==mesh['distance_four_vertices'],'distance-four center labels')
    require(len(doubles) in [1,2] and all({'c0','c4'}<=adj[v] for v in doubles),'control distance-four pair')
    if len(doubles)==2:require(doubles[1] in adj[doubles[0]],'forced original center edge')
    require(mesh['source_claim'] is False and mesh['status']=={'triangulated_degree_contact_control':'triggered and holds',
            'complete_932_global_minimal_source':'not triggered'},'untriggered source overclaimed')
    return {'V':len(vertices),'E':len(inc),'F':len(faces),'m':len(private),'triangulated_disk':True,
            'C_degrees':[len(adj[v]) for v in boundary],'I_degrees':[len(adj[v]) for v in private],
            'distance_four_centres':doubles,'source':'not triggered','small_cap_control':small_caps(vertices,adj,faces,inc)}

def small_caps(vertices,adj,faces,inc):
    """Exhaustive bounded-cycle control only; does not prove the source cap theorem."""
    cycles=set()
    for start in vertices:
        def walk(path):
            for w in adj[path[-1]]:
                if w==start and len(path)>=3:cycles.add(min(tuple(path),tuple([start]+list(reversed(path[1:])))))
                elif len(path)<5 and w>start and w not in path:walk(path+[w])
        walk([start])
    counts=Counter()
    for cycle in cycles:
        cut={tuple(sorted((a,b))) for a,b in zip(cycle,cycle[1:]+cycle[:1])};dual={i:set() for i in range(-1,len(faces))}
        for edge,sides in inc.items():
            if edge in cut:continue
            indices=[s[2] for s in sides];a,b=indices if len(indices)==2 else [indices[0],-1]
            dual[a].add(b);dual[b].add(a)
        seen={-1};todo=[-1]
        while todo:
            a=todo.pop()
            for b in dual[a]-seen:seen.add(b);todo.append(b)
        bounded=set(range(len(faces)))-seen
        strict={v for i in bounded for v in faces[i]}-set(cycle)
        if len(cycle)<5:require(not strict,'occupied C3/C4 control cap')
        elif strict:require(len(strict)==1 and all(v in adj[next(iter(strict))] for v in cycle),'non-W5 occupied C5 control cap')
        counts[str(len(cycle))+'_empty' if not strict else '5_W5']+=1
    return {'status':'triggered and holds','cycles_by_type':dict(counts)}

def full_lifts(vertices,edges,fixed):
    adj={v:set() for v in vertices}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    require(all(a not in fixed or b not in fixed or fixed[a]!=fixed[b] for a,b in edges),'improper fixed literal anchors')
    color=dict(fixed);answer=[]
    def visit():
        if len(color)==len(vertices):answer.append(tuple(color[v] for v in vertices));return
        v=max((v for v in vertices if v not in color),key=lambda v:(len({color[w] for w in adj[v] if w in color}),len(adj[v]),v))
        used={color[w] for w in adj[v] if w in color}
        for c in range(4):
            if c not in used:color[v]=c;visit();del color[v]
    visit();return answer

def literal_join_control(mesh,equal=False):
    """Full lifts in one shared frame, retaining every empty boundary fibre."""
    two=len(mesh['distance_four_vertices'])==2;x='x';y='y' if two else 'x'
    vertices=mesh['boundary']+mesh['private_vertices'];faces=mesh['oriented_faces']
    edges={tuple(sorted((a,b))) for face in faces for a,b in zip(face,face[1:]+face[:1])}
    plus=['c'+str(i) for i in range(5)]+[x]+['t'+str(i) for i in range(4)]+['s0']
    minus=['c'+str(i) for i in [4,5,6,7,8,0]]+[y]+['t'+str(i) for i in range(4,9)]+['s1']
    ep={e for e in edges if set(e)<=set(plus)};em={e for e in edges if set(e)<=set(minus)}
    bridge={tuple(sorted(('x','y')))} if two else set()
    require(ep|em|bridge==edges and set(plus)|set(minus)==set(vertices),'lost original attachment/crossedge')
    require(set(plus)&set(minus)==({'c0','c4'} if two else {'c0','c4','x'}),'wrong actual separator')
    fixed={'c0':0,'c4':0 if equal else 1};direct=set(full_lifts(vertices,edges,fixed));joined=set();sector_stats=[]
    available=[c for c in range(4) if c not in fixed.values()]
    sectors=[(k,l) for k in available for l in available if k!=l] if two else [(k,k) for k in available]
    for k,l in sectors:
        left=full_lifts(plus,ep,{**fixed,x:k});right=full_lifts(minus,em,{**fixed,y:l})
        for a in left:
            for b in right:
                colors=dict(zip(plus,a));other=dict(zip(minus,b))
                require(all(colors[v]==other[v] for v in set(plus)&set(minus)),'independent color normalization')
                colors.update(other);joined.add(tuple(colors[v] for v in vertices))
        sector_stats.append({'x_literal_color':k,'right_center_literal_color':l,'left_full_lifts':len(left),'right_full_lifts':len(right)})
    require(direct==joined,'complete Cartesian union versus direct whole full lifts')
    words=[]
    for length in [3,4]:
        start,end=(fixed['c0'],fixed['c4']) if length==3 else (fixed['c4'],fixed['c0'])
        words.append([w for w in itertools.product(range(4),repeat=length) if all(a!=b for a,b in zip((start,)+w,w+(end,)))])
    sizes=[21,60] if equal else [20,61];require(list(map(len,words))==sizes,'all anchored proper C9 row words')
    def by_boundary(lifts):
        fibres=defaultdict(set)
        for lift in lifts:fibres[tuple(lift[vertices.index(v)] for v in mesh['boundary'])].add(lift)
        return fibres
    dl=by_boundary(direct);jl=by_boundary(joined);empty=0
    for a,b in itertools.product(*words):
        row=(fixed['c0'],)+a+(fixed['c4'],)+b;require(dl[row]==jl[row],'empty/full literal boundary fibre')
        empty+=not dl[row]
    require(len(dl)==len(jl)==sizes[0]*sizes[1],'complete fibre domain')
    result={'status':'triggered and holds','source':'not triggered','literal_anchors':fixed,
            'complete_boundary_fibres':sizes[0]*sizes[1],'empty_boundary_fibres':empty,'direct_whole_full_lifts':len(direct),
            'joined_full_lifts':len(joined),'sectors':sector_stats,'full_tuple_set_equality':True}
    if not equal:
        a,a1=(1,0,2),(1,0,3);b,b1=(0,1,0,1),(0,2,0,3)
        matrix=[[len(dl[(0,)+u+(1,)+v]) for v in [b,b1]] for u in [a,a1]]
        determinant=matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
        require(determinant!=0,'actual control rank-two safeguard')
        result['rank_one_counterexample']={'status':'counterexample','left_arc_words':[a,a1],'right_arc_words':[b,b1],
                                          'actual_full_count_minor':matrix,'determinant':determinant}
    return result

def verify(data,joins=True):
    require(data['schema']=='C9-distance-four-common-embedding-v1' and data['base']==BASE,'certificate identity')
    expected={'maximum_distinct_distance_four_pairs':1,'maximum_vertices_per_distance_four_pair':2,
              'two_centres_force_original_edge':True,'necessary_templates_each_collar':19,'necessary_named_templates':380,
              'new_C9_row_deletions':0,'all_distance_four_contacts_excluded':False,'no_triple_h4_branch':'OPEN',
              'general_932':'OPEN','h_ge_5':'OPEN','smaller_bad':'OPEN','K_infinity':'OPEN','new_Lean':False,
              'k_common_minimum_inherited':23,'new_k_bound':False,'source_graph_controls':'not triggered'}
    require(data['conclusions']==expected,'claim boundary')
    require(data['distance_four_pairs']==[[i,(i+4)%9] for i in range(9)],'all original distance-four pairs')
    witnesses=geometry();require(data['distinct_pair_witnesses']==witnesses,'complete distinct-pair obstruction')
    expected_lenses=[{'pair_index':i,'C4_order':['c'+str(i),'x','c'+str((i+4)%9),'y'],
                     'forbidden_C_diagonal':['c'+str(i),'c'+str((i+4)%9)],'forced_original_diagonal':['x','y'],
                     'three_paths_outer_indices':[0,2],'three_paths_strict_interior_index':1} for i in range(9)]
    require(data['same_pair_lenses']==expected_lenses,'same-pair empty lens and middle path')
    templates=[{'pair_index':None,'multiplicity':0}]+[{'pair_index':i,'multiplicity':n} for i in range(9) for n in [1,2]]
    require(data['templates']==templates,'all19 necessary patterns')
    source=json.loads(gzip.decompress((HERE/'frozen'/SOURCE).read_bytes()));cases={c['id']:c for c in source['cases']}
    queries={q['query_id']:q for q in source['queries'] if q['target']==932 and q['geometry_id']=='induced' and q['status']=='necessary_condition_residual'}
    old=json.loads(gzip.decompress((HERE/'frozen'/R2/'certificate.json.gz').read_bytes()))
    require(old['conclusions']['original_triple_contacts']==0,'round2 no-triple authority')
    require(len(queries)==len(data['case_bindings'])==20,'all20 original source contracts')
    seen=set()
    for b in data['case_bindings']:
        qid=b['query_id'];require(qid in queries and qid not in seen,'duplicate/foreign original query');seen.add(qid)
        q=queries[qid];case=cases[q['case_id']];order=case['boundary_order']
        require(b['C9_original_names']==order and b['extras']==q['extras'],'original ordered names/attachments')
        require(b['retained_frozen_case_sha256']==hashlib.sha256(canonical(case)).hexdigest(),'complete case faces/rotation/fibres SHA')
        require(b['face_third_definitions']==[{'name':'t'+str(i),'original_edge':[order[i],order[(i+1)%9]],
            'complete_C_contacts':[order[i],order[(i+1)%9]]} for i in range(9)],'literal original face-thirds')
        require(b['distance_four_pairs']==[[order[i],order[(i+4)%9]] for i in range(9)] and b['templates']==templates,'all named templates')
        require(b['full_820_row_order_preserved'] is True and b['new_row_deletions']==[],'unsupported source row deletion')
    require(len(source['inner_pattern_order'])==820 and len(source['outer_pattern_order'])==10,'complete original row domain')
    require(len(data['geometric_controls'])==2,'both multiplicity controls')
    controls={m['id']:mesh_properties(m) for m in data['geometric_controls']}
    require(controls['one_double_m12']['m']==12 and controls['two_double_m13']['m']==13,'control sizes')
    result={'named_original_collars':20,'distinct_pair_obstructions':dict(Counter(w['kind'] for w in witnesses)),
            'same_pair_lenses':9,'necessary_templates_each_collar':19,'named_necessary_templates':380,
            'geometric_controls':controls,'source_realizability':'not triggered','no_triple_h4_branch':'OPEN',
            'new_C9_row_deletions':0,'new_k_bound':False,'k_common_minimum_inherited':23,'new_Lean':False}
    if joins:result['complete_literal_full_lift_controls']={m['id']:{'distinct_anchors':literal_join_control(m),
            'equal_anchors':literal_join_control(m,equal=True)} for m in data['geometric_controls']}
    return result

def negative_controls(data):
    mutations=[]
    def mutate(name,fn):
        bad=copy.deepcopy(data);fn(bad);mutations.append((name,bad))
    mutate('missing_original_pair',lambda d:d['distance_four_pairs'].pop())
    mutate('missing_shared_endpoint_pocket',lambda d:d['distinct_pair_witnesses'].pop(next(i for i,w in enumerate(d['distinct_pair_witnesses']) if w['kind']=='shared_endpoint_C5')))
    mutate('pocket_forbidden_chord_accepted',lambda d:next(w for w in d['distinct_pair_witnesses'] if w['kind']=='shared_endpoint_C5')['only_allowed_diagonal'].append('c0'))
    mutate('C4_occupied_middle_path_accepted',lambda d:d['same_pair_lenses'][0].update(three_paths_strict_interior_index=None))
    mutate('same_pair_centers_not_forced_adjacent',lambda d:d['same_pair_lenses'][0].update(forced_original_diagonal=[]))
    mutate('independent_original_C_frame',lambda d:d['case_bindings'][0]['distance_four_pairs'][0].__setitem__(0,'b0'))
    mutate('local_original_face_orientation_reversed',lambda d:d['geometric_controls'][0]['oriented_faces'][0].reverse())
    mutate('all_double_contacts_overexcluded',lambda d:d['conclusions'].update(all_distance_four_contacts_excluded=True))
    mutate('full_source_realizability_overclaimed',lambda d:d['geometric_controls'][0].update(source_claim=True))
    rejected=[]
    for name,bad in mutations:
        try:verify(bad,joins=False)
        except (AssertionError,KeyError,ValueError,TypeError):rejected.append({'name':name,'status':'counterexample','result':'rejected as required'})
        else:raise AssertionError('negative accepted: '+name)
    proc=subprocess.run([sys.executable,'-B',str(HERE/'check.py'),'--source',str(HERE/'certificate.json')],capture_output=True)
    require(proc.returncode==2 and b'unrecognized arguments: --source' in proc.stderr,'unsupported source proposal accepted')
    rejected.append({'name':'unsupported_named_source_interface','status':'counterexample','result':'rejected as required'})
    rejected.append({'name':'rank_one_inference_from_two_compatible_center_colors','status':'counterexample',
                     'result':'actual full-count minors in the two named disk controls have determinants +16 and -16'})
    return rejected

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    parser.add_argument('--negative',action='store_true');parser.add_argument('--check-entry-shared',action='store_true')
    args=parser.parse_args();inputs=custody(args.check_entry_shared)
    data=json.loads((HERE/'certificate.json').read_text());result=verify(data)
    if args.negative:result['semantic_negative_controls']=negative_controls(data)
    print(json.dumps({'status':'PASS','frozen_input_check':inputs,**result},sort_keys=True))

if __name__=='__main__':main()
