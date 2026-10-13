#!/usr/bin/env python3
"""Independent U4 full original-graph relation audit.

Reconstruct the marked finite domain from the three small saved archives.
Use restricted-growth boundary words and fixed-order exhaustive coloring,
without importing any producer. --check reads all inputs without writing.
"""
import argparse
from collections import Counter
from hashlib import sha256

from itertools import combinations, product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
B=frozenset(range(5))
FRAME=frozenset(tuple(sorted((i,(i+1)%5))) for i in B)
PAIRS=tuple(product(range(4),repeat=2))
def boundary_rows():
 found=[]
 def visit(prefix):
  if len(prefix)==5:
   if prefix[-1]!=prefix[0]:found.append(tuple(prefix))
   return
  for c in range(min(max(prefix,default=-1)+1,3)+1):
   if prefix and c==prefix[-1]:continue
   visit(prefix+[c])
 visit([])
 assert len(found)==10
 return tuple(found)
ROWS=boundary_rows()
def regions(verts,edges):
 todo=set(verts);result=[]
 while todo:
  queue=[min(todo)];group=set()
  for v in queue:
   if v in group:continue
   group.add(v)
   for a,b in edges:
    if a==v and b in todo and b not in group:queue.append(b)
    if b==v and a in todo and a not in group:queue.append(a)
  todo-=group;result.append(sorted(group))
 return result
def support(v,edges):
 return tuple(sorted(b for b in B if tuple(sorted((b,v))) in edges))
def independent_lifts(edges,row,ports):
 verts=set(B)|{v for e in edges for v in e}
 ns={v:[] for v in verts}
 for a,b in edges:ns[a].append(b);ns[b].append(a)
 order=sorted(verts)
 # Fixed order based on initial boundary incidence, never adaptive/MRV.
 inner=sorted(verts-B,key=lambda v:(-len(set(ns[v])&B),-len(ns[v]),v))
 assigned=dict(enumerate(row));answer={}
 def go(i):
  if i==len(inner):
   key=tuple(assigned[v] for v in ports)
   answer.setdefault(key,tuple(assigned[v] for v in order));return
  v=inner[i];forbidden={assigned[u] for u in ns[v] if u in assigned}
  for c in range(4):
   if c not in forbidden:assigned[v]=c;go(i+1)
  assigned.pop(v,None)
 go(0)
 return answer
def piece_records(edges,roots):
 inner={v for e in edges for v in e}-B-set(roots);result=[]
 for group in regions(inner,edges):
  contacts=[[v for v in group if tuple(sorted((r,v))) in edges] for r in roots]
  result.append(dict(vertices=group,root_contacts=contacts,owners=[r for r,c in zip(roots,contacts) if c],contact_order=sorted({v for c in contacts for v in c}),boundary_attachments=[list(support(v,edges)) for v in group]))
 return result
def single_markers():
 a=json.loads((ROOT/'artifacts/c5_triangle_branches/observations.json').read_text())['disk_templates']
 b=json.loads((ROOT/'artifacts/c5_triangle_path_reduction/observations.json').read_text())['normal_forms']
 forms=[]
 for family,archive in enumerate((a,b)):
  for origin,old in enumerate(archive):
   oldedges={tuple(sorted(e)) for e in old['edges']};tri={5,6,7};allverts={v for e in oldedges for v in e}
   for tailid,branch in enumerate(regions(allverts-B-tri,oldedges)):
    touching=[(t,x) for t in sorted(tri) for x in branch if tuple(sorted((t,x))) in oldedges]
    assert len(touching)==1
    t,start=touching[0];path=[start]
    while len(path)<len(branch):
     nxt=[v for v in branch if v not in path and tuple(sorted((path[-1],v))) in oldedges]
     assert len(nxt)==1;path.append(nxt[0])
    leaf=support(path[-1],oldedges);X=support(path[0],oldedges)
    specs=[]
    if family==0:
     for prefix,suffix in product((0,1,2),repeat=2):
      if (prefix+suffix)%2==1:continue
      kind='uniform_nonleaf';ns=[X]*(prefix+1+suffix)+[leaf]
      specs.append((kind,prefix,suffix,ns,prefix))
     # Keep historical ordering, which is irrelevant to fingerprint checking.
     specs=[next(s for s in specs if s[1:3]==ps) for ps in ((0,0),(0,2),(2,0),(2,2),(1,1))]
     specs.append(('uniform_leaf',0,0,[X,leaf],1))
    else:
     Y=support(path[1],oldedges)
     specs.append(('two_run_X',0,2,[X,Y,Y,leaf],0))
     for prefix,suffix in ((0,1),(1,0),(1,2),(2,1)):
      specs.append(('two_run_Y',prefix,suffix,[X]+[Y]*(prefix+1+suffix)+[leaf],prefix+1))
     specs.append(('two_run_leaf',0,2,[X,Y,Y,leaf],3))
    retained=sorted(allverts-B-set(path));rename={v:v for v in B}|{v:5+i for i,v in enumerate(retained)}
    for w in sorted(tri-{t}):
     for kind,prefix,suffix,attachments,offset in specs:
      newpath=list(range(5+len(retained),5+len(retained)+len(attachments)))
      edges={tuple(sorted((rename[x],rename[y]))) for x,y in oldedges if x not in path and y not in path}
      edges|={(b,v) for v,ns in zip(newpath,attachments) for b in ns}
      edges|=set(zip(newpath,newpath[1:]));edges.add(tuple(sorted((rename[t],newpath[0]))))
      roots=[newpath[offset],rename[w]];pieces=piece_records(edges,roots)
      assert len([p for p in pieces if len(p['owners'])==2])==1
      if len(pieces)>2:continue
      forms.append(dict(edges=sorted(edges),roots=roots,pieces=pieces,family=family,origin=origin,tail=tailid,kind=kind,prefix=prefix,suffix=suffix,path=newpath,marker_offset=offset,triangle_parent=rename[t]))
 assert len(forms)==316
 return forms
def marker_key(form):
 return tuple(map(tuple,form['edges'])),tuple(form['roots'])

PRIMARY=ROOT/'artifacts/c5_excess_two_nonadjacent_two_mixed_core44/observations.json'
OUT=ROOT/'artifacts/c5_excess_two_nonadjacent_two_mixed_core44/independent_audit.json'
INPUTS=(
 ROOT/'artifacts/c5_triangle_branches/observations.json',
 ROOT/'artifacts/c5_triangle_path_reduction/observations.json',
 ROOT/'artifacts/c5_two_triangle_blocks/observations.json',
 ROOT/'artifacts/c5_excess_two_nonadjacent_two_mixed_core44/control_input.json',
)
SCRIPT=Path(__file__).resolve()


def coloring_valid(edges,row,order,witness,ports=(),values=()):
    assert len(order)==len(witness) and len(set(order))==len(order)
    c=dict(zip(order,witness,strict=True))
    assert set(c)==set(B)|{v for e in edges for v in e}
    assert all(x in range(4) for x in c.values())
    assert tuple(c[b] for b in range(5))==tuple(row)
    assert all(c[a]!=c[b] for a,b in edges)
    assert tuple(c[v] for v in ports)==tuple(values)


def embedding_valid(edges,rotation):
    apex=len(rotation)-1
    augmented=edges|{(b,apex) for b in B}
    for v,neighbours in enumerate(rotation):
        assert len(neighbours)==len(set(neighbours))
        assert set(neighbours)=={b if a==v else a for a,b in augmented if v in (a,b)}
    successors={}
    for a,b in augmented:
        for u,v in ((a,b),(b,a)):
            ns=rotation[v]
            successors[u,v]=(v,ns[(ns.index(u)+1)%len(ns)])
    todo=set(successors);faces=[]
    while todo:
        start=min(todo);dart=start;face=[]
        while True:
            assert dart in todo
            todo.remove(dart);face.append(dart[0]);dart=successors[dart]
            if dart==start:break
        faces.append(face)
    assert len(rotation)-len(augmented)+len(faces)==2
    return faces


def double_markers():
    saved=json.loads(INPUTS[2].read_text())
    records=[]
    for origin,old in enumerate(saved['disk_templates']):
        edges={tuple(sorted(e)) for e in old['edges']}
        embedding_valid(edges,old['apex_rotation'])
        sigma=sum(1<<i for i,row in enumerate(ROWS) if independent_lifts(edges,row,()))
        assert sigma==old['sigma']
        if sigma!=1022:continue
        inner=sorted({v for e in edges for v in e}-B)
        assert len(inner)==6
        triangles=[set(t) for t in combinations(inner,3) if all(e in edges for e in combinations(t,2))]
        assert len(triangles)==2 and not triangles[0]&triangles[1]
        assert len([e for e in edges if e[0] in inner and e[1] in inner])==7
        for roots in combinations(inner,2):
            if roots in edges:continue
            pieces=piece_records(edges,roots)
            assert len([p for p in pieces if len(p['owners'])==2])==1
            records.append(dict(edges=sorted(edges),roots=list(roots),pieces=pieces,
                                family='double_triangle',input_origin=[2,origin]))
    assert len(records)==512
    return records


def reconstructed_domain():
    archives=[json.loads(path.read_text()) for path in INPUTS[:2]]
    for old in archives[0]['disk_templates']:
        embedding_valid(set(map(tuple,old['edges'])),old['apex_rotation'])
    for old in archives[1]['normal_forms']:
        embedding_valid(set(map(tuple,old['edges'])),old['topology']['apex_rotation'])
    singles=single_markers()
    for form in singles:
        f=form['family']
        form['input_origin']=[f,form['origin']]
        form['family']='single_triangle_uniform' if f==0 else 'single_triangle_two_run'
    forms=singles+double_markers()
    keys=[marker_key(f) for f in forms]
    assert len(keys)==len(set(keys))==828
    return {marker_key(f):f for f in forms}


def mixed11_algebra():
    avoiding=[sum(1<<i for i,(c,d) in enumerate(PAIRS) if c!=a and d!=b) for a,b in PAIRS]
    admitted,forbidden=0,set()
    for relation in range(65536):
        banned=tuple(p for p,mask in zip(PAIRS,avoiding) if not relation&mask)
        if all(sum(p[0]==a for p in banned)<=1 for a in range(4)) and all(
                sum(p[1]==b for p in banned)<=1 for b in range(4)):
            admitted+=1;forbidden.add(banned)
    assert admitted==65431 and len(forbidden)==89
    return admitted,forbidden


def d5_targets():
    indices={row:i for i,row in enumerate(ROWS)}
    def normalized(word):
        names={}
        return tuple(names.setdefault(c,len(names)) for c in word)
    result={}
    for mask in (933,941):
        orbit=set()
        for sign in (-1,1):
            for shift in range(5):
                moved=0
                for i,row in enumerate(ROWS):
                    if mask>>i&1:
                        image=normalized([row[(sign*j+shift)%5] for j in range(5)])
                        moved|=1<<indices[image]
                orbit.add(moved)
        result[str(mask)]=sorted(orbit)
    return result


def verify_long_controls(primary,counts):
    controls=primary['marked_tail_long_controls']
    expected_ids=[i for i,f in enumerate(primary['forms']) if f['family']!='double_triangle']
    assert [c['form_index'] for c in controls]==expected_ids
    records=[];contact_nonidentity=None
    for control in controls:
        fi=control['form_index'];short=primary['forms'][fi];long=control['expanded']
        short_edges=set(map(tuple,short['original_edges']))
        long_edges=set(map(tuple,long['original_edges']))
        roots=short['original_root_order'];path=short['marker']['path']
        assert long['original_root_order']==roots
        quotient_order=short['coloring_vertex_order']
        assert long['quotient_vertex_order']==quotient_order
        bags=long['branch_sets']
        assert len(bags)==len(quotient_order)
        inverse={v:q for q,bag in zip(quotient_order,bags,strict=True) for v in bag}
        assert sum(map(len,bags))==len(inverse)
        assert long['coloring_vertex_order']==sorted(inverse)
        for q,bag in zip(quotient_order,bags,strict=True):
            assert q in bag and regions(bag,long_edges)==[sorted(bag)]
            if q in B or q in roots or q in (5,6,7):assert bag==[q]
            for v in bag:assert support(v,long_edges)==support(q,short_edges)
        quotient={tuple(sorted((inverse[a],inverse[b]))) for a,b in long_edges if inverse[a]!=inverse[b]}
        assert quotient==short_edges
        assert all(sum(v in e for e in long_edges)==4 for v in set(inverse)-B)
        # Independently identify all positive segments, respecting marked roots.
        segments=[];current=[]
        for v in path:
            ns=support(v,short_edges)
            if v in roots or len(ns)==3:
                if current:segments.append(current);current=[]
            elif current and support(current[-1],short_edges)!=ns:
                segments.append(current);current=[v]
            else:current.append(v)
        if current:segments.append(current)
        assert long['positive_segments_expanded']==len(segments)
        assert {q for q,bag in zip(quotient_order,bags,strict=True) if len(bag)>1}=={s[0] for s in segments}
        assert all(len(bag) in (1,3) for bag in bags)
        expected_pieces=piece_records(long_edges,roots)
        assert len(expected_pieces)==len(long['retained_original_pieces'])
        for p,saved in zip(expected_pieces,long['retained_original_pieces'],strict=True):
            for field in ('vertices','root_contacts','owners','contact_order','boundary_attachments'):
                assert saved[field]==p[field]
            assert saved['actual_support']==sorted({b for ns in p['boundary_attachments'] for b in ns})
            assert list(map(tuple,saved['incident_edges']))==sorted(e for e in long_edges if set(e)&set(p['vertices']))
        ports=list(roots)+sorted({v for p in expected_pieces for v in p['contact_order']})
        assert long['port_order']==ports
        triangle,=[t for t in combinations(quotient_order,3) if t[0]>=5
                   and all(e in short_edges for e in combinations(t,2))]
        anchors=list(roots)+sorted(set(triangle)-set(roots))
        assert long['anchor_order']==anchors
        short_ports=short['port_order']
        lifted_port_images=[inverse[v] for v in ports]
        assert len(lifted_port_images)==len(set(lifted_port_images))
        assert set(lifted_port_images)==set(short_ports)
        coordinate_order=[lifted_port_images.index(v) for v in short_ports]
        rows=[]
        for ri,(row,saved) in enumerate(zip(ROWS,long['rows'],strict=True)):
            actual=independent_lifts(long_edges,row,ports)
            tuples=sorted(actual)
            assert list(map(tuple,saved['joint_port_tuples']))==tuples
            assert len(saved['full_coloring_witnesses'])==len(tuples)
            for values,witness in zip(tuples,saved['full_coloring_witnesses'],strict=True):
                coloring_valid(long_edges,row,sorted(inverse),witness,ports,values)
                counts['long_joint_witnesses']+=1
            pins=sorted({t[:2] for t in tuples})
            assert list(map(tuple,saved['root_pairs']))==pins
            assert pins==list(map(tuple,short['rows'][ri]['root_pairs']))
            mapped={tuple(t[i] for i in coordinate_order) for t in tuples}
            short_joint=set(map(tuple,short['rows'][ri]['joint_port_tuples']))
            contact_equal=mapped==short_joint
            counts['long_contact_joint_equalities' if contact_equal else 'long_contact_joint_differences']+=1
            if not contact_equal and contact_nonidentity is None:
                extra=sorted(mapped-short_joint);missing=sorted(short_joint-mapped)
                first=extra[0]
                actual_tuple=next(t for t in tuples if tuple(t[i] for i in coordinate_order)==first)
                contact_nonidentity=dict(form_index=fi,row_index=ri,
                    original_root_order=roots,short_port_order=short_ports,long_port_order=ports,
                    long_port_quotient_images=lifted_port_images,
                    additional_mapped_contact_tuples=extra,missing_mapped_contact_tuples=missing,
                    representative_long_joint_tuple=actual_tuple,
                    long_whole_coloring_order=sorted(inverse),
                    representative_long_whole_coloring=actual[actual_tuple],
                    scope='full actual contact joints of separate original graphs need not coincide; triangle plus root anchor joint is preserved')
            long_anchor=independent_lifts(long_edges,row,anchors)
            short_anchor=independent_lifts(short_edges,row,anchors)
            assert set(long_anchor)==set(short_anchor)
            assert list(map(tuple,saved['anchor_joint_tuples']))==sorted(long_anchor)
            assert len(saved['full_anchor_coloring_witnesses'])==len(long_anchor)
            for values,witness in zip(sorted(long_anchor),saved['full_anchor_coloring_witnesses'],strict=True):
                coloring_valid(long_edges,row,sorted(inverse),witness,anchors,values)
                counts['long_anchor_witnesses']+=1
            counts['long_anchor_joint_comparisons']+=1
            counts['long_root_pair_comparisons']+=1
            counts['long_full_contact_joint_checks']+=1
            rows.append(dict(row_index=ri,root_pairs=pins,anchor_joint_tuples=sorted(long_anchor),
                             complete_contact_joint_preserved=contact_equal,
                             complete_contact_tuples=sorted(mapped)))
        counts['long_controls']+=1
        records.append(dict(form_index=fi,rows=rows))
    assert counts['long_controls']==316
    assert counts['long_full_contact_joint_checks']==counts['long_root_pair_comparisons']==3160
    assert counts['long_anchor_joint_comparisons']==3160
    assert contact_nonidentity is not None
    assert contact_nonidentity['form_index']==4 and contact_nonidentity['row_index']==1
    assert len(contact_nonidentity['additional_mapped_contact_tuples'])==20
    assert not contact_nonidentity['missing_mapped_contact_tuples']
    return records,contact_nonidentity


def verify_original_control(primary,counts):
    source=json.loads(INPUTS[3].read_text())
    saved=primary['named_original_control']
    edges=set(map(tuple,source['edges']));core=set(map(tuple,source['M_edges']))
    roots=source['roots_in_z_w_order']
    assert saved['id']==source['id']=='U4-SHORT-NEAR-1018'
    assert set(map(tuple,saved['original_edges']))==edges
    assert set(map(tuple,saved['core_edges']))==core
    assert saved['original_root_order']==roots
    assert core=={e for e in edges if 10 not in e}
    assert [sum(r in e for e in edges) for r in roots]==[5,5]
    assert all(sum(v in e for e in edges)==4 for v in {v for e in edges for v in e}-B-set(roots))
    embedding_valid(edges,source['original_apex_rotation'])
    # The primary walks faces in the opposite orientation. Verify its saved
    # faces as actual successor cycles in that orientation, without comparing
    # either canonical face starting point or order.
    rotation=source['original_apex_rotation'];darts=set()
    for face in saved['verified_apex_faces']:
        for a,b,c in zip(face,face[1:]+face[:1],face[2:]+face[:2]):
            ns=rotation[b]
            assert c==ns[(ns.index(a)-1)%len(ns)]
            assert (a,b) not in darts;darts.add((a,b))
    augmented=edges|{(b,len(rotation)-1) for b in B}
    assert darts=={(a,b) for a,b in augmented}|{(b,a) for a,b in augmented}
    masks=[];joint_records=[]
    assert len(saved['core_and_source_relations'])==2
    for graph,relation in zip((core,edges),saved['core_and_source_relations'],strict=True):
        order=sorted(B|{v for e in graph for v in e})
        ports=roots+sorted(set(order)-B-set(roots))
        assert relation['port_order']==ports and relation['coloring_vertex_order']==order
        mask=0;row_records=[]
        for ri,(row,record) in enumerate(zip(ROWS,relation['rows'],strict=True)):
            joint=independent_lifts(graph,row,ports)
            assert list(map(tuple,record['joint_port_tuples']))==sorted(joint)
            assert len(record['full_coloring_witnesses'])==len(joint)
            for values,witness in zip(sorted(joint),record['full_coloring_witnesses'],strict=True):
                coloring_valid(graph,row,order,witness,ports,values)
                counts['original_control_full_witnesses']+=1
            if joint:mask|=1<<ri
            row_records.append(dict(row_index=ri,joint_tuples=sorted(joint)))
            counts['original_control_row_relations']+=1
        masks.append(mask);joint_records.append(row_records)
    assert masks==[1022,1018] and [saved['sigma_M'],saved['sigma_G']]==masks
    assert saved['full_target_source_premise']=='not_triggered'
    assert [i for i in range(10) if bool(masks[0]>>i&1)!=bool(masks[1]>>i&1)]==[2]
    assert len(set(ROWS[2]))==4
    critical=saved['source_edge_deletion_witnesses']
    assert len(critical)==len(edges-set(FRAME))==19
    assert {tuple(c['edge']) for c in critical}==edges-set(FRAME)
    order=sorted(B|{v for e in edges for v in e})
    for record in critical:
        ri=record['newly_accepted_row_index'];edge=tuple(record['edge'])
        assert not masks[1]>>ri&1
        coloring_valid(edges-{edge},ROWS[ri],order,record['coloring'])
        counts['original_control_edge_witnesses']+=1
    provenance=[]
    for field in ('historical_report','historical_source'):
        record=source[field];path=Path(record['path'])
        current=sha256(path.read_bytes()).hexdigest() if path.exists() else None
        provenance.append(dict(input=field,recorded_sha256=record['sha256'],
                               current_sha256=current,match=current==record['sha256']))
    return dict(id=source['id'],sigma_M=1022,sigma_G=1018,source_premise='not_triggered',
                verified_original_relations=joint_records,historical_provenance=provenance)


def build():
    raw=PRIMARY.read_bytes()
    primary=json.loads(raw)
    assert primary['schema']==1
    assert tuple(map(tuple,primary['pattern_order']))==ROWS
    assert tuple(primary['normalized_rejected_row'])==ROWS[0]
    assert tuple(map(tuple,primary['root_pin_order']))==PAIRS
    orbits=d5_targets()
    assert primary['target_D5_orbits']==orbits
    targets=sorted({m for orbit in orbits.values() for m in orbit})
    expected=reconstructed_domain()
    counts=Counter()
    family_counts=Counter()
    records=[]
    for fi,form in enumerate(primary['forms']):
        edges={tuple(sorted(e)) for e in form['original_edges']}
        roots=tuple(form['original_root_order'])
        key=(tuple(sorted(edges)),roots)
        assert key in expected,'unexpected marker fingerprint'
        inherited=expected.pop(key)
        assert form['family']==inherited['family']
        assert form['input_origin']==inherited['input_origin']
        if form['family']=='double_triangle':
            assert form['marker']=={}
        else:
            fields=('tail','kind','prefix','suffix','path','marker_offset','triangle_parent')
            assert form['marker']=={field:inherited[field] for field in fields}
        order=sorted(B|{v for e in edges for v in e})
        assert form['coloring_vertex_order']==order
        assert set(FRAME)<=edges and sorted(e for e in edges if set(e)<=B)==sorted(FRAME)
        assert roots[0]!=roots[1] and tuple(sorted(roots)) not in edges
        assert all(sum(v in e for e in edges)==4 for v in set(order)-B)
        expected_pieces=piece_records(edges,roots)
        assert len(expected_pieces)==len(form['retained_original_pieces'])
        for p,old in zip(expected_pieces,form['retained_original_pieces'],strict=True):
            for field in ('vertices','root_contacts','owners','contact_order','boundary_attachments'):
                assert old[field]==p[field],(fi,field)
            support=sorted({b for ns in p['boundary_attachments'] for b in ns})
            assert old['actual_support']==support
            assert list(map(tuple,old['incident_edges']))==sorted(e for e in edges if set(e)&set(p['vertices']))
        assert sum(len(p['owners'])==2 for p in expected_pieces)==1
        assert sum(len(p['owners'])==1 for p in expected_pieces)<=1
        ports=list(roots)+sorted({v for p in expected_pieces for v in p['contact_order']})
        assert form['port_order']==ports
        critical={tuple(e['edge']):e['coloring'] for e in form['q_critical_witnesses']}
        assert len(critical)==len(form['q_critical_witnesses'])
        assert set(critical)==edges-set(FRAME)
        for e,witness in critical.items():
            coloring_valid(edges-{e},ROWS[0],order,witness)
            counts['q_edge_witnesses']+=1
        assert len(form['rows'])==10
        ks=[];joint_rows=[];collisions=[]
        for ri,(row,saved) in enumerate(zip(ROWS,form['rows'],strict=True)):
            actual=independent_lifts(edges,row,ports)
            values=sorted(actual)
            assert list(map(tuple,saved['joint_port_tuples']))==values
            assert len(saved['full_coloring_witnesses'])==len(values)
            for values_,witness in zip(values,saved['full_coloring_witnesses'],strict=True):
                coloring_valid(edges,row,order,witness,ports,values_)
                counts['joint_witnesses']+=1
            pairs=sorted({values_[:2] for values_ in values})
            assert list(map(tuple,saved['root_pairs']))==pairs
            fibres=[[i for i,t in enumerate(values) if t[:2]==pin] for pin in PAIRS]
            assert saved['root_fibres_by_pin_order']==fibres
            counts['nonempty_fibres']+=sum(bool(f) for f in fibres)
            counts['empty_fibres']+=sum(not f for f in fibres)
            if ri==0:assert not pairs
            else:
                first=next(((a,b) for a,b in combinations(pairs,2)
                            if a[0]==b[0] or a[1]==b[1]),None)
                if len(set(row))==3:
                    assert first is not None
                    saved_collision=tuple(map(tuple,saved['three_color_capacity_collision']))
                    assert len(saved_collision)==2 and saved_collision[0]!=saved_collision[1]
                    assert saved_collision[0][0]==saved_collision[1][0] or saved_collision[0][1]==saved_collision[1][1]
                    assert set(saved_collision)<=set(pairs)
                    counts['all_nonq_three_color_collision_rows']+=1
                if first is None:
                    assert len(set(row))==4
                    counts['four_color_rows_without_collision']+=1
                    joint_rows.append(values);ks.append(pairs)
                    counts['full_joint_row_checks']+=1
                    continue
                witness_indices=[next(i for i,t in enumerate(values) if t[:2]==pin) for pin in first]
                collisions.append(dict(row_index=ri,collision_pairs=first,
                    complete_port_tuple_indices=witness_indices,
                    full_coloring_witnesses=[actual[values[i]] for i in witness_indices]))
                counts['all_nonq_collision_rows']+=1
            joint_rows.append(values);ks.append(pairs);counts['full_joint_row_checks']+=1
        tests=form['target_comparisons']
        assert len(tests)==10 and [t['target_mask'] for t in tests]==targets
        checked=[]
        for test in tests:
            target=test['target_mask'];ri=test['row_index']
            if target&1:
                assert test['exclusion']=='target_accepts_empty_core_row'
                assert ri==0 and not ks[ri]
                counts['accepted_empty_exclusions']+=1
            else:
                assert test['exclusion']=='mixed11_same_coordinate_capacity'
                assert not target>>ri&1 and ri!=0
                pair=tuple(map(tuple,test['collision_pairs']))
                assert len(pair)==2 and pair[0]!=pair[1]
                assert pair[0][0]==pair[1][0] or pair[0][1]==pair[1][1]
                assert set(pair)<=set(ks[ri])
                ci=test['collision_joint_indices']
                assert len(ci)==2 and all(joint_rows[ri][i][:2]==p for i,p in zip(ci,pair,strict=True))
                counts['capacity_exclusions']+=1
            counts['target_comparisons']+=1
            checked.append(dict(target_mask=target,row_index=ri,exclusion=test['exclusion']))
        family_counts[form['family']]+=1
        counts['marked_cores']+=1
        records.append(dict(form_id=fi,original_root_order=roots,collisions=collisions,
                            verified_targets=checked))
    assert not expected,'primary omitted expected marker fingerprints'
    assert counts['marked_cores']==828 and counts['full_joint_row_checks']==8280
    assert counts['target_comparisons']==8280 and counts['accepted_empty_exclusions']==2484
    assert counts['capacity_exclusions']==5796 and counts['all_nonq_collision_rows']==7400
    assert counts['all_nonq_three_color_collision_rows']==3312
    assert counts['four_color_rows_without_collision']==52
    assert counts['empty_fibres']+counts['nonempty_fibres']==132480
    for key in ('marked_cores','full_joint_row_checks','target_comparisons','accepted_empty_exclusions','capacity_exclusions'):
        assert primary['summary'][key]==counts[key]
    long_records,contact_nonidentity=verify_long_controls(primary,counts)
    original_control=verify_original_control(primary,counts)
    for key in ('long_controls','long_root_pair_comparisons'):
        assert primary['summary'][key]==counts[key]
    admitted,forbidden=mixed11_algebra()
    for form in primary['forms']:
        for ri,row in enumerate(form['rows'][1:],1):
            if len(set(ROWS[ri]))==4:
                continue
            k=set(map(tuple,row['root_pairs']))
            assert not any(k<=set(f) for f in forbidden)
    counts['algebra_relations']=65536
    counts['capacity_admitted_relations']=admitted
    counts['mixed11_forbidden_domain']=len(forbidden)
    for name,digest in primary['source_sha256'].items():
        assert sha256((ROOT/name).read_bytes()).hexdigest()==digest
    sources={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest()
             for p in INPUTS+(PRIMARY,SCRIPT)}
    assert PRIMARY.read_bytes()==raw
    return dict(schema=1,scope='independent U4 marked-domain and complete same-source relation audit',
        pattern_order=ROWS,target_D5_orbits=orbits,source_sha256=sources,
        family_counts=dict(sorted(family_counts.items())),summary=dict(sorted(counts.items())),
        form_audits=records,long_control_audits=long_records,
        mapped_contact_nonidentity_control=contact_nonidentity,
        named_original_control_audit=original_control,
        trust_boundary='inherits arbitrary-size classification and parity coverage; finite audit is not source realization or new Lean proof')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    payload=build()
    encoded=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n'
    if args.check:
        assert OUT.read_text()==encoded,'independent audit differs; preserve inputs'
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(encoded)
    print(json.dumps(dict(status='checked' if args.check else 'written',**payload['summary']),sort_keys=True))


if __name__=='__main__':
    main()
