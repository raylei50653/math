#!/usr/bin/env python3
"""Independent fixed S/U incremental audit. Stdlib only; never imports workers.

Original edges are authoritative. Bit-domain propagation enumerates all colorings.
Saved relations/certificates are comparison data, not solver inputs. No graph search.
--generate exclusive-creates, --check only reads; no supervisor decisions consumed.
"""
import argparse,hashlib,itertools,json,subprocess
from collections import Counter,deque
from pathlib import Path
HOME=Path(__file__).resolve().parent
ROOT=HOME.parent.parent
SOURCE=HOME/'base-source'
BASE='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
B=set(range(5));COL=set(range(4));PAIRS=list(itertools.product(range(4),repeat=2))
FRAME={(0,1),(1,2),(2,3),(3,4),(0,4)}
PATTERNS=json.loads((SOURCE/'artifacts/c5_cells/cells.json').read_text())['pattern_order']
QINDEX=[6,4,3,1,0]

def need(ok,message):
    if not ok:raise ValueError(message)
def enc(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def adjacency(vs,es):
    a={v:set() for v in vs}
    for u,v in es:a[u].add(v);a[v].add(u)
    return a

def enumerate_colors(vs,es,pins):
    """Bit-domain singleton propagation then enumerate complete assignments."""
    pos={v:i for i,v in enumerate(vs)};neighbors=[[] for v in vs]
    for u,v in es:neighbors[pos[u]].append(pos[v]);neighbors[pos[v]].append(pos[u])
    domains=[15]*len(vs)
    for v,c in pins.items():domains[pos[v]]=1<<c
    result=[]
    def search(d):
        queue=deque(i for i,x in enumerate(d) if x.bit_count()==1);done=set()
        while queue:
            i=queue.popleft()
            if i in done:continue
            done.add(i)
            for j in neighbors[i]:
                if not d[j]&d[i]:continue
                d[j]&=~d[i]
                if not d[j]:return
                if d[j].bit_count()==1:queue.append(j)
        choices=[i for i,x in enumerate(d) if x.bit_count()>1]
        if not choices:
            result.append([x.bit_length()-1 for x in d]);return
        i=min(choices,key=lambda j:(d[j].bit_count(),-len(neighbors[j]),vs[j]))
        for c in range(4):
            if d[i]&(1<<c):
                nxt=d.copy();nxt[i]=1<<c;search(nxt)
    search(domains)
    return sorted(result)

def legal(vs,es,pins,lift):
    need(lift is not None and len(lift)==len(vs),'missing/mis-sized full lift')
    f=dict(zip(vs,lift));need(all(x in COL for x in lift),'invalid color')
    need(all(f[u]!=f[v] for u,v in es),'improper full lift')
    need(all(f[v]==c for v,c in pins.items()),'literal pins drift')
    return f

def components(subset,a):
    remaining=set(subset);out=[]
    while remaining:
        todo=[min(remaining)];found=set()
        while todo:
            v=todo.pop()
            if v in found:continue
            found.add(v);todo.extend(a[v]&remaining-found)
        out.append(sorted(found));remaining-=found
    return out

def bridges(vs,es):
    n=len(components(vs,adjacency(vs,es)))
    return [list(e) for e in es if len(components(vs,adjacency(vs,[f for f in es if f!=e])))>n]

def face_walk(vs,es,rotation):
    a=adjacency(vs,es);need(set(rotation)==set(vs),'rotation keys')
    for v in vs:need(len(rotation[v])==len(set(rotation[v])) and set(rotation[v])==a[v],'rotation neighbors')
    unseen={d for u,v in es for d in [(u,v),(v,u)]};faces=[];face_of={}
    while unseen:
        start=min(unseen);d=start;face=[]
        while True:
            need(d in unseen,'repeated dart');unseen.remove(d);face_of[d]=len(faces)
            u,v=d;face.append(u);ring=rotation[v];d=(v,ring[(ring.index(u)+1)%len(ring)])
            if d==start:break
        faces.append(face)
    need(len(vs)-len(es)+len(faces)==2,'sphere Euler')
    outer=[f for f in faces if len(f)==5 and set(f)==B];need(len(outer)==1,'unique induced C5 face')
    return faces,face_of

def structure(raw):
    vs=sorted(raw['vertices']);es=sorted(tuple(sorted(e)) for e in raw['edges']);a=adjacency(vs,es)
    need(len(es)==len(set(es)) and all(u!=v for u,v in es),'simple graph')
    need({e for e in es if set(e)<=B}==FRAME,'induced ordered C5')
    roots=sorted(v for v in vs if v not in B and len(a[v])==5)
    need(len(roots)==2 and tuple(roots) not in es,'chi0 two roots')
    need(all(len(a[v])==4 for v in set(vs)-B-set(roots)),'original degree4')
    need(len(components(vs,a))==1,'connected G')
    rot={int(k):v for k,v in raw['rotation'].items()};faces,_=face_walk(vs,es,rot)
    pieces=[]
    for i,pv in enumerate(components(set(vs)-B-set(roots),a)):
        ps=set(pv);contacts={str(r):sorted(a[r]&ps) for r in roots};owners=[r for r in roots if contacts[str(r)]]
        order=sorted(set().union(*(set(c) for c in contacts.values())))
        inner=[e for e in es if set(e)<=ps];attachments=[e for e in es if set(e)&ps and set(e)&B]
        support=sorted(B & set().union(*(a[v] for v in pv)))
        one=len(components(set(vs)-B-ps,a))==1
        p={'id':f'P{i}','vertices':pv,'contacts':contacts,'owners':owners,'contact_order':order,
           'shared_contacts':sorted(set(contacts[str(roots[0])])&set(contacts[str(roots[1])])),
           'support':support,'attachments':list(map(list,attachments)),'internal_edges':list(map(list,inner)),
           'incidences':[len(contacts[str(r)]) for r in roots], 'kind':'mixed' if len(owners)==2 else 'unary',
           'one_sided':one,'original_internal_bridges':bridges(pv,inner)}
        need(bool(owners),'root-free piece outside scope')
        if one:
            kv=sorted(B|ps);ke=[e for e in es if set(e)<=set(kv)];kr={v:[w for w in rot[v] if w in kv] for v in kv}
            kfaces,faceof=face_walk(kv,ke,kr);occupied=set()
            for v in kv:
                ring=rot[v]
                for j,w in enumerate(ring):
                    if w in kv:continue
                    predecessor=(j-1)%len(ring)
                    while ring[predecessor] not in kv:predecessor=(predecessor-1)%len(ring)
                    occupied.add(faceof[(ring[predecessor],v)])
            need(len(occupied)==1,'one-sided complement in multiple faces')
            cf=kfaces[next(iter(occupied))];boundary={tuple(sorted((cf[j],cf[(j+1)%len(cf)]))) for j in range(len(cf))}
            shield=sorted(FRAME-boundary);p['shield']={'complement_face':cf,'edges':list(map(list,shield)),'length':len(shield)}
        pieces.append(p)
    return {'id':raw['id'],'vertices':vs,'edges':list(map(list,es)),'roots':roots,'rotation':raw['rotation'],'faces':faces,
            'pieces':pieces,'m':sum(p['kind']=='mixed' for p in pieces),
            'touch':sorted(B & set().union(*(a[v] for v in set(vs)-B))),
            'H_bridges':bridges(sorted(set(vs)-B),[e for e in es if not set(e)&B])}

def local(g,p,i):
    pv=p['vertices'];vs=sorted(B|set(pv));es=[e for e in g['edges'] if set(e)<=set(vs)]
    allcolors=enumerate_colors(vs,es,dict(enumerate(PATTERNS[i])));need(bool(allcolors),'local relation empty')
    groups={}
    for lift in allcolors:
        f=dict(zip(vs,lift));t=tuple(f[x] for x in p['contact_order']);groups.setdefault(t,[]).append([f[x] for x in pv])
    tuples=[{'tuple':list(t),'full_piece_lifts':sorted(groups[t])} for t in sorted(groups)]
    fibres=[]
    for pair in PAIRS:
        pins=dict(zip(g['roots'],pair));ix=[j for j,t in enumerate(tuples) if all(t['tuple'][p['contact_order'].index(x)]!=pins[r] for r in g['roots'] for x in p['contacts'][str(r)])]
        fibres.append({'pins':list(pair),'tuple_indices':ix})
    F={str(r):[c for c in range(4) if all(any(t['tuple'][p['contact_order'].index(x)]==c for x in p['contacts'][str(r)]) for t in tuples)] for r in p['owners']}
    need(all(len(F[str(r)])<=len(p['contacts'][str(r)]) for r in p['owners']),'local contact deficit')
    return {'index':i,'tuples':tuples,'fibres':fibres,'F':F}

def evaluate(g,vs,es,active,i,cut_spoke=None):
    roots=g['roots'];beta=PATTERNS[i];pins=dict(enumerate(beta))
    solutions=enumerate_colors(vs,es,pins);groups={}
    for lift in solutions:
        f=dict(zip(vs,lift));pair=tuple(f[r] for r in roots);groups.setdefault(pair,[]).append(lift)
    factors={};E={}
    for r in roots:
        fs=[{'name':f'spoke:{r}:{b}','n':1,'F':[beta[b]]} for b in sorted(B) if sorted((r,b)) in es]
        fs += [{'name':p['id'],'n':len(p['contacts'][str(r)]),'F':p['rows'][i]['F'][str(r)]} for p in active if p['kind']=='unary' and r in p['owners']]
        factors[str(r)]=fs;E[str(r)]=sorted(COL-set().union(*(set(f['F']) for f in fs)))
    cells=[]
    for pair in PAIRS:
        a,b=pair;selected={p['id']:p['rows'][i]['fibres'][4*a+b]['tuple_indices'] for p in active}
        joined=a in E[str(roots[0])] and b in E[str(roots[1])] and all(selected.values())
        need(bool(joined)==bool(groups.get(pair)),'complete join / independent direct mismatch')
        cells.append({'pins':list(pair),'tuple_indices':selected,'full_graph_lift':groups[pair][0] if pair in groups else None,'full_lift_count':len(groups.get(pair,[]))})
    accepted=[list(pair) for pair in PAIRS if pair in groups];capacity=[]
    # Match U's count convention: one unavailable record for an accepted join.
    if accepted:capacity.append({'status':'not triggered','missing':['rejecting complete join']})
    else:
        for r,s in (roots,roots[::-1]):
            if not E[str(s)]:capacity.append({'r':r,'s':s,'status':'not triggered','missing':['E_s nonempty']});continue
            for b in E[str(s)]:
                columns=[]
                for p in active:
                    if p['kind']!='mixed':continue
                    bad=[a for a in range(4) if not p['rows'][i]['fibres'][4*a+b if r==roots[0] else 4*b+a]['tuple_indices']]
                    k=len(p['contacts'][str(r)]);need(len(bad)<=k,'column contact bound')
                    columns.append({'piece':p['id'],'k':k,'G':bad})
                union=set().union(*(set(c['G']) for c in columns));own=set(E[str(r)])
                need(own<=union,'rejected join exact cover')
                terms=[sum(f['n']-len(f['F']) for f in factors[str(r)]),sum(len(f['F']) for f in factors[str(r)])-(4-len(own)),sum(c['k']-len(c['G']) for c in columns),sum(len(c['G']) for c in columns)-len(union),len(union-own)]
                degree=sum(r in e for e in es);need(all(t>=0 for t in terms) and sum(terms)==degree-4,'five-term capacity')
                capacity.append({'r':r,'s':s,'b':b,'columns':columns,'D_O_delta_o_lambda':terms,'rhs':degree-4,'status':'triggered and holds'})
    return {'index':i,'factors':factors,'E':E,'root_pairs':accepted,'all_16_fibres':cells,'capacity':capacity}

def compare_evaluation(computed,saved,vs,es,roots,is_u=True):
    need(computed['root_pairs']==saved['root_pairs'],'root pairs differ from worker')
    cells=saved['all_16_fibres'] if is_u else saved['pairs']
    for c,s in zip(computed['all_16_fibres'],cells,strict=True):
        pair=c['pins'];need(pair==s['pins'],'root-pair order drift')
        pin=dict(enumerate(PATTERNS[computed['index']]))|dict(zip(roots,pair))
        if is_u:
            need(c['tuple_indices']==s['tuple_indices'],'complete selected tuple indices')
            need((c['full_graph_lift'] is None)==(s['full_graph_lift'] is None),'full graph empty fibre')
            if s['full_graph_lift'] is not None:legal(vs,es,pin,s['full_graph_lift'])
        else:
            for k in ('joint_lift','direct_lift'):
                need((c['full_graph_lift'] is None)==(s[k] is None),'J empty fibre')
                if s[k] is not None:legal(vs,es,pin,s[k])
    if is_u:
        need(computed['factors']==saved['factors'] and computed['E']==saved['E'],'side factors/E')
        need(computed['capacity']==saved['capacity'],'capacity column terms and triggering')
    else:
        for r in roots:
            fs=computed['factors'][str(r)];ss=saved['sides'][str(r)]
            need(computed['E'][str(r)]==ss['E'],'J available colors')
            expected=[{'id':['spoke',r,int(f['name'].split(':')[-1])] if f['name'].startswith('spoke:') else ['unary',f['name']],'F':f['F']} for f in fs]
            need(expected==ss['factors'],'J original side identities')
        actual=[x for x in computed['capacity'] if x['status']=='triggered and holds'];old=[x for x in saved['capacity'] if x['status']=='triggered and holds']
        need(len(actual)==len(old),'J triggered capacity count')
        for c,d in zip(actual,old,strict=True):
            need(all(c[k]==d[k] for k in ('r','s','b','rhs')),'J capacity column identity')
            need(c['D_O_delta_o_lambda']==[d[k] for k in ('D_u','O_u','delta','o','lambda')],'J five terms')
            need(c['columns']==[{'piece':x['piece'],'k':x['k'],'G':x['G_C_b']} for x in d['columns']],'J mixed column')
        # Independently verify each J missing-premise direction.
        for d in saved['capacity']:
            if d['status']=='not triggered':
                missing=[]
                if computed['root_pairs']:missing.append('complete join rejects beta')
                if not computed['E'][str(d['s'])]:missing.append('E_s nonempty')
                need(missing==d['missing'],'J not-triggered premises')

def orbit_audit(saved):
    result=[]
    for c,kr,ks,mask in itertools.product(range(4),range(1,4),range(1,4),range(8)):
        perms=[dict(zip(range(4),p)) for p in itertools.permutations(range(4)) if p[c]==c]
        seeds=[(c,next(x for x in COL if x!=c)),(next(x for x in COL if x!=c),c),tuple(x for x in sorted(COL) if x!=c)[:2]]
        orbits=[{(p[a],p[b]) for p in perms} for a,b in seeds]
        need(sorted(map(len,orbits))==[3,3,6] and len(set().union(*orbits))==12,'S3 generated orbit partition')
        forbidden=set().union(*(orbits[k] for k in range(3) if mask&(1<<k)))
        cols=[sum(b==j for a,b in forbidden) for j in range(4)];rows=[sum(a==j for a,b in forbidden) for j in range(4)]
        valid=all(v<=kr for v in cols) and all(v<=ks for v in rows)
        if valid and kr+ks<=3:need(not forbidden,'low incidence universal relation')
        x={'c':c,'k_r':kr,'k_s':ks,'orbit_mask':mask,'forbidden_pairs':[list(p) for p in sorted(forbidden)],'column_sizes':cols,'row_sizes':rows,'status':'triggered and holds' if valid else 'not triggered','missing_premises':[] if valid else ['contact bound'],'universal':not forbidden}
        result.append(x)
    need(result==saved,'S orbit payload mismatch')
    return result

def abstract_audit(saved):
    configs=[('ABSTRACT-S-SIDE-BLOCK',[0,1],[2],[[(0,2)],[(1,2)]],[1,1],[1,1],[[2],[3]],[[0],[1],[3]],2),
             ('ABSTRACT-S-JOINT-BLOCK',[0,1],[2],[[(0,2)],[(1,2)]],[1,1],[1,1],[[2],[3]],[[0],[1],[3]],0),
             ('ABSTRACT-S-SINGLETON22-LONG-RESIDUAL',[1,2,3],[1,2],[[(a,b) for a,b in PAIRS if a and b and a!=b],[(1,1),(2,2)]],[2,1],[2,1],[[0]],[[0],[3]],1)]
    out=[]
    for conf,m in zip(configs,saved,strict=True):
        name,er,es,bad,kr,ks,fr,fs,c=conf;er=set(er);es=set(es);bad=list(map(set,bad))
        need(m['id']==name and m['E_r_X']==sorted(er) and m['E_s']==sorted(es),'abstract domains')
        need(m['k_r']==kr and m['k_s']==ks and m['side_factors_X']==fr and m['side_factors_s']==fs and m['spoke_colour']==c,'abstract fixed inputs')
        need(COL-set().union(*map(set,fr))==er and COL-set().union(*map(set,fs))==es,'abstract side domains')
        need(sum(map(len,fr))+sum(kr)==4 and sum(map(len,fs))+sum(ks)==5,'abstract original incidence')
        for f,k,l,key in zip(bad,kr,ks,('A_P','A_Q'),strict=True):
            need(m[key]==[list(p) for p in PAIRS if p not in f],'abstract all16 incl empties')
            need(all(sum(y==b for a,y in f)<=k for b in COL) and all(sum(x==a for x,b in f)<=l for a in COL),'abstract contact bounds')
        columns=[]
        for b in sorted(es):
            C=[{a for a in COL if (a,b) in f} for f in bad];V=set().union(*C)
            terms=[sum(map(len,fr))-len(set().union(*map(set,fr))),0,sum(k-len(x) for k,x in zip(kr,C)),sum(map(len,C))-len(V),len(V-er)]
            need(terms==[0]*5 and V==er,'abstract zero slack every column')
            original=er-{c};O=sum(map(len,fr))+1-len(set().union(*map(set,fr))|{c});leak=len(V-original)
            blocker=next((i for i,x in enumerate(C) if c in x),None)
            need((O,leak)==((0,1) if c in er else (1,0)),'spoke blocker two cases')
            record={'b':b,'G_P':sorted(C[0]),'G_Q':sorted(C[1]),'derivative_slacks':[0]*5,'original_O':O,'original_lambda':leak,'mixed_blocker':blocker};columns.append(record)
        need(columns==m['columns'],'abstract column payload')
        need(m['source_graph'] is None and m['full_lifts'] is None,'abstract no source lifts')
        need(set(m['missing_source_premises'])=={'named disk graph','complete component lifts','Sigma 933/941','Sigma-criticality','beta-minimality'},'missing graph/source prerequisites')
        out.append({'id':name,'all_16_pairs':[{'pins':list(p),'P_nonempty':p not in bad[0],'Q_nonempty':p not in bad[1],'join_nonempty':p[0] in er and p[1] in es and all(p not in f for f in bad)} for p in PAIRS],'columns':columns,'source_status':'not triggered','missing_source_premises':m['missing_source_premises']})
    return out

def mask_tables(s,u):
    source_tables=[];target=[]
    for sigma in (933,941):
        q=[i for i,bit in enumerate(QINDEX) if not sigma&(1<<bit)]
        allowed=[]
        for mask in range(32):
            subset=[i for i in range(5) if mask&(1<<i)]
            if set(subset)<=set(q) and (len(subset)<=1 or (len(subset)==2 and (subset[1]-subset[0])%5 in (1,4))):allowed.append(subset)
        allowed.sort(key=lambda x:(len(x),x));source_tables.append({'sigma_G':sigma,'Q_G_singleton_positions':q,'E2_permitted_Q_X':allowed,'scope':'necessary mask identities; not source realization'})
        for beta in q:
            choices=[x for x in allowed if beta in x];forced=sorted(set(q)-set().union(*map(set,choices)))
            target.append({'sigma_G':sigma,'beta_singleton_position':beta,'possible_Q_X':choices,'forced_new_rejections_removed_from_G':forced})
    need(source_tables==s,'933/941 full necessary Q tables')
    need(target==u,'seven target Q(X) rows incl 933 q2')
    return source_tables,target

def audit():
    manifest=read(HOME/'inputs.json');need(subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()==BASE,'HEAD drift')
    for f in manifest['authority_files']:
        p=SOURCE/f['path'];blob=subprocess.check_output(['git','-C',str(ROOT),'show',BASE+':'+f['path']]);need(p.read_bytes()==blob and digest(p)==f['sha256'],'BASE authority drift')
    S=read(ROOT/'audits/2026-10-09-n45-s/certificate.json');U=read(ROOT/'audits/2026-10-09-n45-u/certificate-final.json');J=read(ROOT/'audits/2026-10-09-n45-j/results/certificate.json')
    sg={x['id']:x for x in S['fixed_graph_inventory']};ug={x['id']:x for x in U['graphs']};jg={x['id']:x for x in J['N2']+J['N1_separate']}
    counts=Counter();graphs=[];spokes=[];inventory=[]
    fixed_n1={'NA8-0003','NA8-0007','NA8-0009','NA8-0010'}
    for path in sorted((SOURCE/'artifacts/c5_excess_two_e4c/controls').glob('*.json')):
        raw=read(path);g=structure(raw);inventory.append({'id':g['id'],'m':g['m']})
        need(g['m']==raw['m'],'saved inventory m from original edges')
        if g['m']!=2 and g['id'] not in fixed_n1:continue
        name=g['id'];saved=ug[name];js=jg[name];vs=g['vertices'];es=g['edges'];roots=g['roots'];a=adjacency(vs,es)
        need(name in sg if g['m']==2 else name not in sg,'N2/N1 domain separation')
        need(vs==saved['vertices'] and es==saved['edges'] and roots==saved['root_order'],'original named graph')
        need(g['rotation']==saved['rotation'] and g['faces']==saved['faces'] and g['H_bridges']==saved['original_H_bridges'],'original rotation/faces/H bridges')
        for p,old,orig,jp in zip(g['pieces'],saved['pieces'],raw['pieces'],js['pieces'],strict=True):
            for key in p:
                if key=='shared_contacts':need(p[key]==jp[key],'J shared identity');continue
                need(p[key]==old[key],'U original piece '+key)
            for key in ('vertices','contacts','owners','support','contact_order','incidences','kind'):need(p[key]==orig[key],'BASE original piece '+key)
            need(p['original_internal_bridges']==jp['original_bridges'],'J original piece bridges')
            if p['one_sided']:need(p['shield']['edges']==jp['original_shield_edges'],'J original shield edges')
            p['rows']=[local(g,p,i) for i in range(10)]
            for row,ur,br,jr in zip(p['rows'],old['rows'],orig['rows'],[r[p['id']] for r in js['relations']],strict=True):
                need(row==ur,'U complete tuples/fibres/F/full lifts')
                projected={'tuples':[{'tuple':t['tuple'],'lifts':t['full_piece_lifts']} for t in row['tuples']],'fibres':row['fibres']}
                need(projected==jr and projected['tuples']==br['tuples'] and projected['fibres']==br['fibres'],'J/BASE full relations')
                counts['piece_relations']+=1;counts['local_root_pin_fibres']+=16;counts['local_empty_fibres']+=sum(not f['tuple_indices'] for f in row['fibres']);counts['full_piece_lifts']+=sum(len(t['full_piece_lifts']) for t in row['tuples']);counts['distinct_contact_tuples']+=len(row['tuples'])
                if p['kind']=='unary' and sum(p['incidences'])==1:counts['unit_F_empty_rows' if not row['F'][str(p['owners'][0])] else 'unit_F_singleton_rows']+=1
        joins=[evaluate(g,vs,es,g['pieces'],i) for i in range(10)]
        sigma=sum(1<<i for i,row in enumerate(joins) if row['root_pairs']);need(sigma==raw['sigma']==saved['sigma']==js['original']['sigma'],'complete Sigma')
        for row,ur,jr in zip(joins,saved['joins'],js['original']['rows'],strict=True):compare_evaluation(row,ur,vs,es,roots);compare_evaluation(row,jr,vs,es,roots,False)
        if g['m']==2:
            ss=sg[name];need(ss['vertices']==vs and ss['edges']==es and ss['roots']==roots and ss['rotation']==g['rotation'],'S named source metadata')
            need(ss['original_pieces']==[{k:p[k] for k in ('vertices','contacts','owners','support')} for p in g['pieces']],'S original piece ownership')
            need(ss['sigma']==sigma,'S full Sigma')
            for i,lift in enumerate(ss['row_full_lifts']):
                need((lift is None)==(not joins[i]['root_pairs']),'S original row emptiness')
                if lift is not None:legal(vs,es,dict(enumerate(PATTERNS[i])),lift);counts['S_full_lifts_validated']+=1
            actual_spokes=[]
            for r in roots:
                for edge in es:
                    if r not in edge or not set(edge)&B:continue
                    xes=[e for e in es if e!=edge]
                    for i,row in enumerate(joins):
                        if row['root_pairs']:continue
                        derivative=evaluate(g,vs,xes,g['pieces'],i)
                        need(bool(derivative['root_pairs']),'unexpected rejecting S derivative')
                        b=next(v for v in edge if v in B);need(all(pair[roots.index(r)]==PATTERNS[i][b] for pair in derivative['root_pairs']),'all deleted spoke lifts forced equal')
                        sj=next(d for d in js['unit_derivatives'] if d['derivative']['kind']=='spoke' and d['derivative']['edge']==edge)
                        compare_evaluation(derivative,sj['rows'][i],vs,xes,roots,False)
                        oq=next(q for q in ss['spoke_queries'] if q['edge']==edge and q['index']==i)
                        f=legal(vs,xes,dict(enumerate(PATTERNS[i])),oq['full_lift']);need(f[r]==PATTERNS[i][b],'S saved forced equal')
                        need(oq['status']=='not triggered' and oq['missing_premises']==['G-spoke rejects this beta'],'S missing rejection')
                        actual_spokes.append((edge,i));spokes.append({'id':name,'edge':edge,'root':r,'row':derivative,'source_status':'not triggered','missing':['derivative rejects original beta']});counts['S_full_lifts_validated']+=1
                        counts['S_spoke_nonempty_pins']+=len(derivative['root_pairs']);counts['S_spoke_empty_pins']+=16-len(derivative['root_pairs'])
            need(len(actual_spokes)==len(ss['spoke_queries']),'S spoke×rejected-row exact domain')
        derivatives=[]
        for p in g['pieces']:
            if p['kind']!='unary' or sum(p['incidences'])!=1:continue
            r=p['owners'][0];x=p['contacts'][str(r)][0];contact=sorted((r,x));xvs=[v for v in vs if v not in p['vertices']];xes=[e for e in es if set(e)<=set(xvs)];ces=[e for e in es if e!=contact];active=[t for t in g['pieces'] if t['id']!=p['id']]
            du=next(d for d in saved['unit_derivatives'] if d['piece']==p['id']);dj=next(d for d in js['unit_derivatives'] if d['derivative'].get('piece')==p['id'])
            need(xvs==du['vertices_X']==dj['vertices'] and xes==du['edges_X']==dj['edges'],'whole original U omitted')
            xjoins=[];palettes=[];placements=[]
            for i in range(10):
                row=evaluate(g,xvs,xes,active,i);compare_evaluation(row,du['joins_X'][i],xvs,xes,roots);compare_evaluation(row,dj['rows'][i],xvs,xes,roots,False)
                cutsol=enumerate_colors(vs,ces,dict(enumerate(PATTERNS[i])));cg={}
                for lift in cutsol:
                    f=dict(zip(vs,lift));cg.setdefault(tuple(f[t] for t in roots),[]).append(lift)
                need(row['root_pairs']==[list(pair) for pair in PAIRS if pair in cg],'whole U deletion / contact deletion exact root pairs')
                for cell,old in zip(row['all_16_fibres'],du['joins_X'][i]['all_16_fibres'],strict=True):
                    pair=cell['pins'];lift=old['contact_edge_deleted_full_lift'];need((lift is None)==(tuple(pair) not in cg),'contact deletion empty fibre')
                    if lift is not None:legal(vs,ces,dict(enumerate(PATTERNS[i]))|dict(zip(roots,pair)),lift);counts['U_contact_lifts_validated']+=1
                    cell['contact_edge_deleted_full_lift']=cg[tuple(pair)][0] if tuple(pair) in cg else None
                new=bool(row['root_pairs']) and not bool(joins[i]['root_pairs'])
                palette=sorted({t['tuple'][0] for t in p['rows'][i]['tuples']});projection=sorted({pair[roots.index(r)] for pair in row['root_pairs']})
                if new:need(len(palette)==1 and palette==projection,'new accepted gamma singleton contact / root projection');palettes.append({'index':i,'contact_palette':palette,'X_root_projection':projection,'status':'triggered and holds'});counts['new_gamma_palette_instances']+=1
                if not row['root_pairs']:
                    Fu=set(p['rows'][i]['F'][str(r)]);Er=set(row['E'][str(r)]);placement='D' if not Fu else ('lambda' if Fu<=Er else 'O')
                    for c in row['capacity']:
                        if c.get('r')!=r or c['status']!='triggered and holds':continue
                        original=next(v for v in joins[i]['capacity'] if v.get('r')==r and v.get('b')==c['b']);need(c['D_O_delta_o_lambda']==[0]*5,'X degree4 all five zero')
                        wanted={'D':[1,0,0,0,0],'O':[0,1,0,0,0],'lambda':[0,0,0,0,1]}[placement];need(original['D_O_delta_o_lambda']==wanted,'U D/O/lambda restored original budget')
                        placements.append({'index':i,'r':r,'s':next(t for t in roots if t!=r),'b':c['b'],'F_U':sorted(Fu),'E_r_X':sorted(Er),'placement':placement,'X':c['D_O_delta_o_lambda'],'G':original['D_O_delta_o_lambda']})
                counts['X_nonempty_pins']+=len(row['root_pairs']);counts['X_empty_pins']+=16-len(row['root_pairs']);xjoins.append(row)
            xsigma=sum(1<<i for i,row in enumerate(xjoins) if row['root_pairs']);need(xsigma==du['sigma_X'],'X Sigma');need(placements==du['capacity_placements'],'U placement payload')
            need([i for i in range(10) if xjoins[i]['root_pairs'] and not joins[i]['root_pairs']]==du['new_rows'],'U exact gained rows')
            for minimal in du['minimal_rows']:
                need(not xjoins[minimal['index']]['root_pairs'],'minimal row rejects')
                for d in minimal['edge_deletion_lifts']:
                    legal(xvs,[e for e in xes if e!=d['edge']],dict(enumerate(PATTERNS[minimal['index']])),d['full_graph_lift'])
                counts['N1_minimal_rows' if g['m']==1 else 'N2_minimal_rows']+=1
            derivatives.append({'piece':p['id'],'vertices_X':xvs,'edges_X':xes,'contact_edge':contact,'vertices_contact_deleted':vs,'edges_contact_deleted':ces,'sigma_X':xsigma,'joins_X':xjoins,'new_gamma_palettes':palettes,'capacity_placements':placements})
            counts['unit_derivatives']+=1;counts['capacity_placement_instances']+=len(placements)
            for v in placements:counts['placement_'+v['placement']]+=1
        need(len(derivatives)==len(saved['unit_derivatives']),'U exact unit derivative inventory')
        low=[p['id'] for p in g['pieces'] if p['kind']=='mixed' and sum(p['incidences'])<=3 and p['one_sided'] and g['touch']==sorted(B)]
        need(low==saved['low_incidence_support_claim_instances'],'small incidence trigger premises');need(all(len(p['support'])>=2 for p in g['pieces'] if p['id'] in low),'small incidence necessary support')
        counts['low_incidence_support_instances']+=len(low)
        # Independent strict criticality on the same fixed graph; preserve full gains.
        need(len(saved['edge_deletions'])==len(es)-len(FRAME),'original edgecut inventory')
        for old in saved['edge_deletions']:
            ces=[e for e in es if e!=old['edge']];gains=[];csigma=0
            for i in range(10):
                fs=enumerate_colors(vs,ces,dict(enumerate(PATTERNS[i])))
                if fs:csigma|=1<<i
                if fs and not joins[i]['root_pairs']:gains.append(i)
            need(csigma==old['sigma'] and gains==[v['index'] for v in old['new_rows']] and gains,'fixed graph strict Sigma-criticality')
            for row in old['new_rows']:legal(vs,ces,dict(enumerate(PATTERNS[row['index']])),row['full_graph_lift']);counts['critical_edgecut_full_lifts_validated']+=1
            counts['critical_edge_deletions']+=1
        for w in saved['piece_rejection_witnesses']:
            p=next(t for t in g['pieces'] if t['id']==w['piece']);i=w['index'];need(not joins[i]['root_pairs'],'critical-contact witness row rejects original')
            contact=w['edge'];need(any(r in contact and x in contact for r in p['owners'] for x in p['contacts'][str(r)]),'actual original contact witness')
            f=legal(vs,[e for e in es if e!=contact],dict(enumerate(PATTERNS[i])),w['full_edge_deleted_lift']);need(f[contact[0]]==f[contact[1]],'contact witness equality')
            tight={str(v):sorted(COL-{f[x] for x in a[v]-set(p['vertices'])}) for v in p['vertices']};need(tight==w['tight_lists'],'original tight lists')
            need(all(len(tight[str(v)])==len(a[v]&set(p['vertices'])) for v in p['vertices']),'tight degree equality')
            path=w['path_to_frame_avoiding_piece'];need(path and path[0] in p['owners'] and path[-1] in B and not set(path)&set(p['vertices']) and all(sorted(e) in es for e in zip(path,path[1:])),'original outside path avoids piece')
            need(w['outside_lift']==[[v,f[v]] for v in vs if v not in p['vertices']],'outside original lift')
            counts['piece_critical_contact_witnesses']+=1
        g.update({'sigma':sigma,'joins':joins,'unit_derivatives':derivatives,'low_incidence_support_instances':low,'source_status':'not triggered','missing_source_premises':['complete Sigma=933/941','N2 rejecting 45/54 unit derivative'] if g['m']==2 else ['N2 (one mixed only)','complete Sigma=933/941']})
        graphs.append(g);counts['graphs']+=1;counts['N2_graphs' if g['m']==2 else 'N1_graphs']+=1
        counts['original_nonempty_pins']+=sum(len(row['root_pairs']) for row in joins);counts['original_empty_pins']+=sum(16-len(row['root_pairs']) for row in joins)
        for label,rows in [('G',joins)]+[('X',d['joins_X']) for d in derivatives]:
            for row in rows:
                for c in row['capacity']:counts['capacity_'+label+'_'+c['status']]+=1
    need(len(inventory)==54 and counts['N2_graphs']==19 and counts['N1_graphs']==4,'fixed domain 19+4')
    need(set(ug)=={g['id'] for g in graphs} and set(sg)=={g['id'] for g in graphs if g['m']==2},'worker exact domains')
    need(len(spokes)==47,'47 S original spoke rejection queries')
    orbits=orbit_audit(S['singleton_orbit_table']);abstract=abstract_audit(S['abstract_capacity_controls']);masks,target=mask_tables(S['cross_row_masks'],U['e4_u_exact_target_mask_table'])
    scalar=[{'m_r':r,'m_s':s,'E_r_X_size':r,'E_s_size_lower_bound':s-1,'both_short_necessary_count_pass':r+s<=5} for r,s in itertools.product(range(2,5),range(2,6))]
    need(scalar==S['both_short_incidence_counts'],'12 incidence scalars')
    palette=[]
    for mask in range(1,16):
        T=[c for c in range(4) if mask&(1<<c)];F=[c for c in range(4) if not any(t!=c for t in T)];palette.append({'T_contact':T,'F_U':F})
    palette.sort(key=lambda x:(len(x['T_contact']),x['T_contact']));need(palette==U['unit_contact_palette_algebra_15'],'15 nonempty palettes')
    for k,v in U['counts'].items():
        if k in counts:need(counts[k]==v,'U independently recomputed count '+k)
    counts.update({'original_root_pair_queries':len(graphs)*160,'derivative_root_pair_queries':counts['unit_derivatives']*160,'contact_edge_deleted_root_pair_queries':counts['unit_derivatives']*160,'S_full_sigma_rows':190,'S_full_sigma_root_pair_queries':3040,'S_spoke_rejection_rows':len(spokes),'S_spoke_root_pair_queries':len(spokes)*16,'singleton_candidates':len(orbits),'singleton_contact_bound_holds':sum(x['status']=='triggered and holds' for x in orbits),'singleton_contact_bound_not_triggered':sum(x['status']=='not triggered' for x in orbits),'abstract_models':len(abstract),'abstract_capacity_columns':sum(len(m['columns']) for m in abstract),'target_source_triggered':0,'source_counterexamples':0})
    return {'task':'N45-SU-J','BASE':BASE,'inputs_sha256':digest(HOME/'inputs.json'),'checker_sha256':digest(Path(__file__)),'independent_of_supervisor_reviews':True,'inventory_54_m_from_edges':inventory,'singleton_orbit_table':orbits,'abstract_capacity_controls':abstract,'both_short_incidence_counts':scalar,'S_cross_row_masks':masks,'U_exact_target_mask_table':target,'U_nonempty_contact_palettes':palette,'graphs':graphs,'S_spoke_rejected_row_derivatives':spokes,'counts':dict(sorted(counts.items())),'coverage':{'graph_source_prerequisites':'not triggered for all 19 N2','low_incidence_abstract_contact_bound':'triggered and holds (92); not triggered (196)','always_singleton_F_overclaim':{'status':'counterexample','count':counts['unit_F_empty_rows'],'scope':'finite control of stronger interface statement only'},'N2_degree4_rejecting_derivative':'not triggered','D_O_placement_controls':'not triggered','N1_lambda_controls':'triggered and holds (4); separate from N2','paper':'not checked','source_realization':'not checked','Lean':'not checked'}}

def main():
    p=argparse.ArgumentParser(description=__doc__);m=p.add_mutually_exclusive_group(required=True);m.add_argument('--generate',action='store_true');m.add_argument('--check',action='store_true');a=p.parse_args()
    payload=enc(audit());target=HOME/'certificate.json'
    if a.generate:
        with target.open('xb') as f:f.write(payload)
    else:need(target.read_bytes()==payload,'independent certificate byte mismatch')
    print(json.dumps({'mode':'exclusive-create' if a.generate else 'read-only replay','sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload),'counts':json.loads(payload)['counts']},sort_keys=True))
if __name__=='__main__':main()
