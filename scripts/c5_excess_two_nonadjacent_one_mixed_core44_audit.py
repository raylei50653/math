#!/usr/bin/env python3
"""Independently replay the U3 mixed11 finite certificate without producer imports."""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/c5_excess_two_nonadjacent_one_mixed_core44/observations.json'
OUT = ART.with_name('independent_audit.json')
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
raw = ART.read_bytes()
data = json.loads(raw)
B = set(range(5))
FRAME = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}
counts = Counter()

def check(test, label):
    if not test:
        raise AssertionError(label)

def canon(seq):
    used = []
    out = []
    for c in seq:
        if c not in used:
            used.append(c)
        out.append(used.index(c))
    return tuple(out)

# Restricted-growth words generate one representative per common color orbit.
rows = []
def rgs(word):
    if len(word) == 5:
        if word[-1] != word[0]:
            rows.append(tuple(word))
        return
    for c in range(min(3, max(word)+1)+1):
        if c != word[-1]:
            rgs(word+[c])
rgs([0])
rows.sort()
check(len(rows) == 10 and list(map(list, rows)) == data['pattern_order'], 'canonical rows')
row_index = {r:i for i,r in enumerate(rows)}
orbits = {}
for base in (933, 941):
    orbit = set()
    for perm in ([ (s+d*i) % 5 for i in range(5)] for s in range(5) for d in (1,-1)):
        mask = 0
        for i, row in enumerate(rows):
            if base & (1 << i):
                mask |= 1 << row_index[canon(tuple(row[v] for v in perm))]
        orbit.add(mask)
    orbits[str(base)] = sorted(orbit)
check(orbits == data['target_D5_orbits'], 'D5 target orbits')
targets = set(orbits['933']) | set(orbits['941'])
diagonals = {p for p in itertools.combinations(range(5),2) if p not in FRAME}
check({tuple(x['actual_boundary_pair']) for x in data['rejected_row_pair_coverage']} == diagonals, 'pair inventory')
for entry in data['rejected_row_pair_coverage']:
    a,b = entry['actual_boundary_pair']
    check({x['target_mask'] for x in entry['target_cases']} == targets, 'mask inventory')
    for case in entry['target_cases']:
        expect = [i for i,r in enumerate(rows) if r[a] == r[b] and not (case['target_mask'] & (1<<i))]
        check(expect and expect == case['rejected_repeating_rows'], 'rejected repeated pair')
        counts['pair_mask_cases'] += 1

def edge_set(entries):
    es = {tuple(e) for e in entries}
    check(len(es) == len(entries), 'duplicate edge')
    check(all(a < b for a,b in es), 'edge order')
    return es

def validate_coloring(values, order, es, row, ports=(), port_values=()):
    check(len(values) == len(order) and len(set(order)) == len(order), 'witness order')
    f = dict(zip(order,values))
    check(set(values) <= {0,1,2,3}, 'witness colors')
    check(tuple(f[i] for i in range(5)) == row, 'literal boundary frame')
    check(all(f[a] != f[b] for a,b in es), 'original edge witness')
    check(tuple(f[v] for v in ports) == tuple(port_values), 'contact/root tuple witness')
    return f

def piece_bruteforce(vs, es, row, contacts):
    got = set()
    for colors in itertools.product(range(4), repeat=len(vs)):
        f = dict(enumerate(row))
        f.update(zip(vs,colors))
        if all(f[a] != f[b] for a,b in es):
            got.add(tuple(f[v] for v in contacts))
    return got

def graph_all_tuples(vs, es, row, ports, roots):
    adjacent = {v:set() for v in B | set(vs)}
    for a,b in es:
        adjacent[a].add(b)
        adjacent[b].add(a)
    # Static order and precomputed domains; enumerate every assignment.
    order = sorted(vs, key=lambda v:(v not in roots, -len(adjacent[v]), -v))
    domains = {v:tuple(c for c in range(4) if all(row[b] != c for b in adjacent[v] & B)) for v in vs}
    f = dict(enumerate(row))
    got = {p:set() for p in itertools.product(range(4),repeat=2)}
    full_count = 0
    def visit(pos):
        nonlocal full_count
        if pos == len(order):
            pair = tuple(f[v] for v in roots)
            got[pair].add(tuple(f[v] for v in ports))
            full_count += 1
            return
        v = order[pos]
        for c in domains[v]:
            if all(f.get(u) != c for u in adjacent[v]):
                f[v] = c
                visit(pos+1)
        f.pop(v,None)
    visit(0)
    return got,full_count

shield_keys=set()
for cert in data['budget']['ordered_two_two_shields']:
    es = edge_set(cert['core_edges'])
    aug = edge_set(cert['augmented_edges'])
    check(aug == es | {tuple(sorted((b,cert['exterior_apex']))) for b in B}, 'apex augmentation')
    orders = cert['unary_shield_vertex_order']
    shield_keys.add(tuple(map(tuple,orders)))
    shield_es = [set(tuple(sorted(p)) for p in zip(o,o[1:])) for o in orders]
    check(all(len(o)==3 and all((o[i+1]-o[i])%5 == 1 for i in (0,1)) for o in orders), 'shield arc')
    check(not (shield_es[0] & shield_es[1]), 'shield disjoint')
    check([sorted(x) for x in shield_es] == [list(map(tuple,x)) for x in cert['unary_shield_edges']], 'saved shield edges')
    check(cert['actual_unary_support'] == [sorted(o) for o in orders], 'shield support')
    usable = sorted(B - {o[1] for o in orders})
    check(usable == cert['common_spoke_vertices'], 'usable points')
    model = cert['subdivision']
    left,right = model['branch_partition']
    check(model['model'] == 'K3,3' and len(left)==len(right)==3 and not set(left)&set(right), 'K33 model')
    pairs = set()
    inner = set()
    for path in model['paths']:
        check(path[0] in left and path[-1] in right and len(path)==len(set(path)), 'K33 endpoints')
        check(all(tuple(sorted(e)) in aug for e in zip(path,path[1:])), 'K33 original edges')
        mids=set(path[1:-1])
        check(not mids & (set(left)|set(right)|inner), 'K33 disjoint path interiors')
        inner |= mids
        pairs.add((path[0],path[-1]))
    check(pairs == set(itertools.product(left,right)) and len(model['paths'])==9, 'K33 edge coverage')
    counts['K33_certificates'] += 1
arcs=[tuple((s+i)%5 for i in range(3)) for s in range(5)]
expect_shields={(a,b) for a,b in itertools.product(arcs,repeat=2)
                if not ({tuple(sorted(p)) for p in zip(a,a[1:])} & {tuple(sorted(p)) for p in zip(b,b[1:])})}
check(shield_keys == expect_shields and len(shield_keys)==10,'complete ordered shield domain')
capacities=[]
for k in range(1,5):
    for kind in ('spoke','unit_unary'):
        t=4-k
        possible=(t>=1) if kind=='spoke' else (k==1)
        retained=1+(k if kind=='spoke' else 0)
        capacities.append({'unary_capacity':k,'original_spokes':t,'omitted_unit':kind,
            'capacity_one_omission_possible':possible,'retained_internal_degree':retained,
            'admitted_by_paper_core_maximum_degree_three':possible and retained<=3})
check(capacities==data['budget']['capacity_rows'],'capacity table arithmetic')
counts['capacity_rows']=len(capacities)
double=data['budget']['double_triangle_control']
des=edge_set(double['interior_edges'])
check(des=={(5,7),(5,8),(7,8),(6,9),(6,10),(9,10),(5,6)},'double triangle exact control')
check(double['internal_degrees']=={str(v):sum(v in e for e in des) for v in range(5,11)},'double triangle degrees')
check(double['degree_three_vertices']==[5,6] and double['direct_bridge']==[5,6] and double['bridge_endpoints_adjacent'],'direct bridge metadata')

slack_keys = set()
for rec in data['duplicate_neighbor_list_slack']['records']:
    d = rec['internal_degree']; col = rec['repeated_boundary_neighbor_color']; pins = tuple(rec['root_pins'])
    ext = [col,col] + list(pins)
    avail = sorted(set(range(4))-set(ext))
    check(len(ext)+d==4 and rec['external_neighbor_colors']==ext, 'slack neighbor count')
    check(rec['available_colors']==avail and len(avail)-d==rec['list_slack'] and len(avail)>d, 'slack arithmetic')
    slack_keys.add((d,col,pins)); counts['slack_records'] += 1
expect_slack = {(d,c,p) for d in range(3) for c in range(4) for p in itertools.product(range(4),repeat=2-d)}
check(slack_keys == expect_slack and len(slack_keys)==84, 'slack record coverage')

graph_keys=set()
for gi,g in enumerate(data['actual_graph_controls']):
    es = edge_set(g['edges']); vs=g['interior_order']; roots=g['original_root_order']; ports=g['joint_port_order']
    check(FRAME <= es and (5,6) not in es, 'frame/nonadjacency')
    check(roots==[5,6] and g['full_coloring_vertex_order']==sorted(B|set(vs)), 'root/full orders')
    check(all(sum(v in e for e in es)==(5 if v in roots else 4) for v in vs), 'full degrees')
    check(g['original_root_spokes']==[sorted(b for b in B if tuple(sorted((b,r))) in es) for r in roots], 'actual root spokes')
    pieces=g['pieces']
    graph_keys.add((g['c_path_length'],g['side_kind'],g['roots_exchanged']))
    check(len(g['rows'])==10,'all graph rows')
    check(g['high_spoke_root']==(6 if g['roots_exchanged'] else 5) and
          g['triangle_root']==(5 if g['roots_exchanged'] else 6),'root exchange metadata')
    check(set().union(*(set(p['vertices']) for p in pieces)) == set(vs)-set(roots), 'piece vertex inventory')
    check(sum(len(p['vertices']) for p in pieces)==len(vs)-2, 'piece disjointness')
    check(ports == roots+sorted(set().union(*(set(p['ordered_distinct_contacts']) for p in pieces))), 'joint port order')
    for piece in pieces:
        pvs=set(piece['vertices'])
        pes=edge_set(piece['piece_edges']); inc=edge_set(piece['root_incidence_edges'])
        check(pes=={e for e in es if set(e)<=B|pvs}, 'exact original piece edges')
        check(inc=={e for e in es if set(e)&pvs and set(e)&set(roots)}, 'exact original incidence edges')
        contacts=[sorted(v for v in pvs if tuple(sorted((v,r))) in es) for r in roots]
        check(contacts==piece['root_contacts'], 'actual contacts')
        check(piece['ownership']==[r for r,c in zip(roots,contacts) if c], 'actual owner')
        check(piece['ordered_distinct_contacts']==sorted(set().union(*map(set,contacts))), 'distinct contact order')
        attachments=[{'vertex':v,'boundary_neighbors':sorted(b for b in B if tuple(sorted((v,b))) in es)} for v in piece['vertices']]
        check(attachments==piece['boundary_attachments'], 'actual attachments')
        check(piece['actual_support']==sorted(set().union(*(set(a['boundary_neighbors']) for a in attachments))), 'actual support')
    check(pieces[0]['id']=='U_z' and pieces[0]['ownership']==[g['high_spoke_root']] and len(pieces[0]['root_incidence_edges'])==1,'unary z owner/capacity')
    check(pieces[1]['id']=='U_w' and pieces[1]['ownership']==[g['triangle_root']] and len(pieces[1]['root_incidence_edges'])==2,'unary w owner/capacity')
    mixed=pieces[2]
    check(mixed['id']=='C' and mixed['ownership']==roots and list(map(len,mixed['root_contacts']))==[1,1],'mixed11 inventory')
    check(len(mixed['vertices'])==g['c_path_length'] and mixed['actual_support']==[2,4],'mixed path/support inventory')
    check({e for e in es if set(e)<=set(mixed['vertices'])}=={tuple(sorted(e)) for e in zip(mixed['vertices'],mixed['vertices'][1:])},'actual path edges')
    check(all(a['boundary_neighbors']==[2,4] for a in mixed['boundary_attachments']),'all mixed attachments')
    sigma=0
    for ri,rowrec in enumerate(g['rows']):
        row=rows[ri]
        check(rowrec['row_index']==ri and tuple(rowrec['boundary_row'])==row, 'row identity')
        saved_pieces=rowrec['piece_relations']
        check(len(saved_pieces)==3, 'three piece relations')
        witness_maps=[]
        for piece,saved in zip(pieces,saved_pieces):
            check(saved['piece_id']==piece['id'] and saved['contact_order']==piece['ordered_distinct_contacts'], 'piece relation identity')
            check(saved['witness_vertex_order']==sorted(B|set(piece['vertices'])), 'piece witness order')
            tuples=list(map(tuple,saved['tuples'])); witnesses=saved['full_piece_witnesses']
            check(len(tuples)==len(witnesses) and tuples==sorted(set(tuples)), 'piece tuple inventory')
            check(set(tuples)==piece_bruteforce(piece['vertices'],edge_set(piece['piece_edges']),row,saved['contact_order']), 'independent whole-piece relation')
            maps=[]
            for tup,witness in zip(tuples,witnesses):
                maps.append(validate_coloring(witness,saved['witness_vertex_order'],edge_set(piece['piece_edges']),row,saved['contact_order'],tup))
                counts['piece_witnesses']+=1
            witness_maps.append(maps); counts['piece_relations']+=1
        independent,assignment_count=graph_all_tuples(vs,es,row,ports,roots)
        counts['enumerated_full_graph_colorings']+=assignment_count
        fibres=rowrec['all_sixteen_root_fibres']
        check(len(fibres)==16 and {tuple(f['root_pair']) for f in fibres}==set(independent), 'all 16 fibre inventory')
        accepted=[]
        for fibre in fibres:
            pair=tuple(fibre['root_pair']); tuples=list(map(tuple,fibre['joint_tuples'])); refs=fibre['joint_tuple_piece_witness_indices']
            check(tuples==sorted(set(tuples)) and len(tuples)==len(refs), 'joint tuple/index inventory')
            check(set(tuples)==independent[pair], 'exact independent pinned fibre')
            for tup,indices in zip(tuples,refs):
                check(len(indices)==3, 'three piece references')
                lift=dict(enumerate(row)); lift.update(zip(roots,pair))
                for pi,index in enumerate(indices):
                    check(0<=index<len(witness_maps[pi]), 'piece witness index')
                    for v,c in witness_maps[pi][index].items():
                        check(v not in lift or lift[v]==c, 'shared literal color frame')
                        lift[v]=c
                validate_coloring([lift[v] for v in g['full_coloring_vertex_order']],g['full_coloring_vertex_order'],es,row,ports,tup)
                counts['joint_tuple_composites']+=1
            witness=fibre['full_graph_witness']
            check((witness is not None)==bool(independent[pair]), 'fullgraph witness/empty fibre')
            if witness is not None:
                validate_coloring(witness,g['full_coloring_vertex_order'],es,row,roots,pair)
                counts['full_graph_witnesses']+=1
                counts['nonempty_fibres']+=1
                accepted.append(pair)
            else:
                counts['empty_fibres']+=1
            counts['pinned_fibres']+=1
        check(sorted(accepted)==list(map(tuple,rowrec['accepted_root_pairs'])), 'accepted root pairs')
        check(rowrec['accepted']==bool(accepted), 'row accepted flag')
        check(rowrec['repeated_mixed_attachment_color']==(row[2]==row[4]), 'repeat flag')
        if row[2]==row[4]:
            check(accepted, 'repeated endpoint row accepts')
            counts['repeating_endpoint_rows']+=1
        if accepted:
            sigma |= 1<<ri
        counts['graph_rows']+=1
    check(sigma==g['sigma'] and sigma not in targets, 'full sigma')
    counts['graphs']+=1
check(graph_keys==set(itertools.product(range(1,5),('bare_sides','long_z_unary','long_w_unary'),(False,True))) and len(graph_keys)==24,'complete 24 graph inventory')

for path,expected in data['source_sha256'].items():
    check(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected, 'source hash '+path)
    counts['source_hashes']+=1
check(ART.read_bytes()==raw, 'artifact byte drift')
out={'status':'PASS','artifact_bytes':len(raw),'artifact_sha256':hashlib.sha256(raw).hexdigest(),
     'counts':dict(sorted(counts.items())), 'sigma_histogram':dict(sorted(Counter(g['sigma'] for g in data['actual_graph_controls']).items())),
     'scope':'Independent canonical-pattern/orbit, literal original-edge witness, exact fullpiece/joint-fibre, K33-edge and slack checks. No primary import; no arbitrary-size theorem, disk/source-realizability or criticality certification.'}
encoded = json.dumps(out,sort_keys=True,indent=2)+'\n'
if args.check:
    check(OUT.read_text()==encoded, 'independent audit certificate differs')
else:
    OUT.write_text(encoded)
print(json.dumps(out,sort_keys=True))
