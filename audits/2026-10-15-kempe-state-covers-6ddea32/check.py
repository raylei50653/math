#!/usr/bin/env python3
"""Read-only complete graph-colouring/cover replay and exact cover-space algebra."""
import argparse,collections,hashlib,itertools,json
from pathlib import Path
from space import PERMS,canonical,rename,layer_space
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
SOURCE='audits/2026-10-15-kempe-compatibility-6ddea32/certificate.json'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def custody():
    m=json.loads((HERE/'INPUTS.json').read_text())
    for r in m['inputs']:
        need(sha(HERE/'frozen'/r['path'])==sha(ROOT/r['path'])==r['sha256'],'input drift: '+r['path'])
    for r in m['local_graphs']:need(sha(HERE/r['path'])==r['sha256'],'graph instance drift')
    return m

def components(adj,row,pair):
    left={v for v,c in enumerate(row) if c in pair};result=[]
    while left:
        v=min(left);left.remove(v);part={v};todo=[v]
        while todo:
            for w in adj[todo.pop()]&left:left.remove(w);part.add(w);todo.append(w)
        result.append(sorted(part))
    return result

def enumerate_colours(adj,pins):
    n=len(adj);nodes=0;solutions=[];ds=[15]*n
    for v,c in zip([pins[i] for i in (0,5,6)],(0,1,2)):ds[v]=1<<c
    def search(dom):
        nonlocal nodes
        nodes+=1;changed=True
        while changed:
            changed=False
            for u in range(n):
                if dom[u].bit_count()!=1:continue
                for v in sorted(adj[u]):
                    if dom[v]&dom[u]:
                        dom[v]&=~dom[u];changed=True
                        if not dom[v]:return
        todo=[v for v in range(n) if dom[v].bit_count()>1]
        if not todo:solutions.append(tuple(d.bit_length()-1 for d in dom));return
        v=min(todo,key=lambda v:(dom[v].bit_count(),-len(adj[v]),v))
        for c in range(4):
            if dom[v]>>c&1:child=dom[:];child[v]=1<<c;search(child)
    search(ds)
    return sorted(solutions),nodes

def cover_graph(name,states,space,byid,frame,edge):
    g=json.loads((HERE/name).read_text());values=g['functions'];pins=g['pins'];n=len(values);adj=[set() for _ in range(n)]
    need(len(set(pins))==7,'pins are not distinct')
    need(len(g['edges'])==len({tuple(e) for e in g['edges']}),'duplicate edge')
    for a,b in g['edges']:need(0<=a<b<n,'invalid simple edge');adj[a].add(b);adj[b].add(a)
    need(set().union(*map(set,components(adj,[0]*n,(0,1))))==set(range(n)),'graph coverage')
    need(len(components(adj,[0]*n,(0,1)))==1,'graph disconnected')
    expected={};colour_to_state={}
    for s in states:
        i,p=frame[s['id']]
        for sheet in range(2):
            row=tuple(p[v[2*i+sheet]] for v in values)
            need(all(row[a]!=row[b] for a,b in g['edges']),'improper listed colouring')
            need(''.join('ABCD'[row[v]] for v in pins)==s['literal_row'],'pin mismatch')
            need(row not in colour_to_state,'two lifted states collapse')
            expected[s['id'],sheet]=row;colour_to_state[row]=(s['id'],sheet)
    normalized,nodes=enumerate_colours(adj,pins)
    full={tuple(p[c] for c in row) for row in normalized for p in PERMS}
    need(full==set(colour_to_state),'complete colourings differ from lifted states')
    counts=collections.Counter(sid for sid,sheet in colour_to_state.values())
    need(set(counts.values())=={2} and len(counts)==432,'not a two-sheet complete cover')
    checks=collections.Counter();hidden_max=0
    row_to_id={s['literal_row']:s['id'] for s in states}
    for (sid,sheet),row in expected.items():
        s=byid[sid]
        for j,part in enumerate(s['pairings']):
            bit=0;all_comps=[]
            for pair,blocks in zip(part['pairing'],part['terminal_parts']):
                actual=components(adj,row,pair)
                projected=[sorted(i for i,v in enumerate(pins) if v in comp) for comp in actual]
                hidden=sum(not b for b in projected);hidden_max=max(hidden_max,hidden)
                need(not hidden,'unexpected hidden component')
                need(sorted(projected)==sorted(blocks),'wrong terminal partition')
                for block in blocks:
                    comp=actual[projected.index(block)];all_comps.append((pair,comp));out=list(row)
                    for v in comp:out[v]=sum(pair)-out[v]
                    target=part['cube_targets_by_bitmask'][1<<bit]
                    voltage=(g['voltage']>>edge[sid,j,bit])&1
                    need(colour_to_state[tuple(out)]==(target,sheet^voltage),'wrong actual switch lift')
                    bit+=1;checks['individual_components_and_switches']+=1
            for mask in range(len(part['cube_targets_by_bitmask'])):
                out=list(row);target=sid;delta=0
                for bit,(pair,comp) in enumerate(all_comps):
                    if mask>>bit&1:
                        for v in comp:out[v]=sum(pair)-out[v]
                        delta^=(g['voltage']>>edge[target,j,bit])&1
                        target=byid[target]['pairings'][j]['cube_targets_by_bitmask'][1<<bit]
                need(target==part['cube_targets_by_bitmask'][mask],'wrong cube base target')
                need(colour_to_state[tuple(out)]==(target,sheet^delta),'wrong full cube lift')
                checks['whole_cube_masks']+=1
        for p in PERMS:
            image=tuple(p[c] for c in row)
            need(colour_to_state[image]==(row_to_id[rename(s['literal_row'],p)],sheet),'wrong full S4 action')
            checks['global_S4_actions']+=1
    # Shortest lifted closed walk changing the sheet at base state0.
    seen={(0,0):None};queue=collections.deque([(0,0)])
    while queue:
        sid,sheet=queue.popleft()
        if (sid,sheet)==(0,1):break
        for j,p in enumerate(byid[sid]['pairings']):
            for bit in range(sum(map(len,p['terminal_parts']))):
                target=p['cube_targets_by_bitmask'][1<<bit];delta=(g['voltage']>>edge[sid,j,bit])&1;y=(target,sheet^delta)
                if y not in seen:seen[y]=((sid,sheet),[sid,target,j,bit,delta]);queue.append(y)
    need((0,1) in seen,'monodromy is trivial');path=[];cur=(0,1)
    while seen[cur] is not None:cur,step=seen[cur];path.append(step)
    path.reverse()
    patterns=sorted({canonical(''.join('ABCD'[c] for c in r))[0] for r in itertools.product(range(4),repeat=5) if all(r[i]!=r[(i+1)%5] for i in range(5))})
    support=sorted({canonical(s['literal_row'])[0] for s in states});outer={canonical(s[:5])[0] for s in support};mask=sum(1<<patterns.index(r) for r in outer)
    need(mask==319,'outer mask changed')
    return {'graph_file':name,'sha256':sha(HERE/name),'vertices':n,'edges':len(g['edges']),'pins':pins,
      'voltage_hex':hex(g['voltage']),'normalized_search_nodes':nodes,'normalized_colourings':[list(r) for r in normalized],
      'complete_labelled_colourings':len(full),'projection_states':len(counts),'sheets':2,'hidden_components_max':hidden_max,
      'canonical_pin_support':support,'outer_mask':mask,'direct_checks':dict(checks),'monodromy_walk':path,
      'nonplanarity_certificate':{'edges':len(g['edges']),'planar_simple_bound':3*n-6},
      'planar_alternative_realization':'OPEN','full_720_state_cover':'OPEN','original_source':'not triggered'}

def diamond_control():
    es=[(0,1),(0,2),(1,2),(1,3),(2,3)];adj=[set() for _ in range(4)]
    for a,b in es:adj[a].add(b);adj[b].add(a)
    rows=[r for r in itertools.product(range(4),repeat=4) if all(r[a]!=r[b] for a,b in es)]
    fibres=collections.defaultdict(list)
    for r in rows:fibres[r[:3]].append(r)
    need(len(rows)==48 and len(fibres)==24 and {len(v) for v in fibres.values()}=={2},'diamond cover count')
    for row in rows:
        hs={pair:sum(not(set(comp)&{0,1,2}) for comp in components(adj,row,pair)) for pair in itertools.combinations(range(4),2)}
        htotal=[hs[p[0]]+hs[p[1]] for p in [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]]
        need(sum(2**h for h in htotal)-2==2,'diamond hidden bound')
    return {'edges':[list(e) for e in es],'pins':[0,1,2],'complete_colourings':48,'base_states':24,'sheets':2,
      'section_obstruction':{'base_pin_row':'ABC','pair':'AD','visible_component':[0],'hidden_component':[3]},
      'hidden_cube_bound':2,'graph':'connected planar diamond'}

def build():
    m=custody();source=json.loads((HERE/'frozen'/SOURCE).read_text());spaces=[];layer0=None
    for layer in range(5):
        states=[s for s in source['states'] if s['layer']==layer];data=layer_space(states);spaces.append(data[0])
        if layer==0:layer0=(states,*data)
    totals={'edge_orbits':sum(len(s['edge_orbits']) for s in spaces),'square_rank':sum(s['square_rank'] for s in spaces),
      'cover_dimension':sum(s['cover_dimension'] for s in spaces),'gauge_rank':sum(s['gauge_rank'] for s in spaces),
      'quotient_dimension':sum(s['quotient_dimension'] for s in spaces),'zero_product_quotient_dimension':sum(s['zero_product_quotient_dimension'] for s in spaces)}
    need(totals=={'edge_orbits':184,'square_rank':42,'cover_dimension':142,'gauge_rank':25,'quotient_dimension':117,'zero_product_quotient_dimension':13},'cover space dimensions')
    return {'schema':'kempe-state-cover-v1','base':m['base'],'spaces':spaces,'cover_space_totals':totals,
      'graphs':[cover_graph(name,*layer0) for name in ['graph-75.json','graph-121.json']],
      'diamond_control':diamond_control(),'full_720_cover':'OPEN','planar_realization':'OPEN','complete_319_source_exclusion':'OPEN','general_claim':'OPEN','new_Lean':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--certificate',default=str(HERE/'certificate.json'));a=p.parse_args();result=build()
    if a.write:
        with Path(a.certificate).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    else:need(json.loads(Path(a.certificate).read_text())==result,'certificate mismatch')
    print(json.dumps({'status':'PASS','cover_space':result['cover_space_totals'],'graphs':[{k:g[k] for k in ['graph_file','vertices','edges','complete_labelled_colourings','projection_states','sheets','hidden_components_max','outer_mask']} for g in result['graphs']]},sort_keys=True))
