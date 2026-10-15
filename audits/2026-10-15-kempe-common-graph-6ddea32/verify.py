#!/usr/bin/env python3
"""Independent finite proof replay. Does not import check.py or search."""
import argparse,hashlib,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(path):
    manifest=json.loads((HERE/'INPUTS.json').read_text())
    for item in manifest['inputs']:
        for p in (HERE/'frozen'/item['path'],ROOT/item['path']):
            require(sha(p)==item['sha256'],'authority drift')
    source_path=HERE/'frozen/audits/2026-10-15-kempe-compatibility-6ddea32/certificate.json'
    source=json.loads(source_path.read_text());certificate=json.loads(Path(path).read_text())
    require(certificate['input_sha256']==sha(source_path),'input binding')
    states={s['id']:s for s in source['states'] if s['layer']==0}
    require(len(states)==432,'wrong layer size')
    keys=set();frames={}
    for sid,s in states.items():
        ordering=''.join(dict.fromkeys(s['literal_row']))
        ordering+=''.join(c for c in 'ABCD' if c not in ordering)
        normalized=''.join('ABCD'[ordering.index(c)] for c in s['literal_row'])
        frames[sid]=(normalized,ordering);keys.add(normalized)
    keys=sorted(keys);require(keys==certificate['canonical_rows'],'canonical variables')
    frames={sid:(keys.index(k),frame) for sid,(k,frame) in frames.items()}
    relation={}
    for sid,s in states.items():
        u,frame=frames[sid]
        for part in s['pairings']:
            bit=0
            for pair,blocks in zip(part['pairing'],part['terminal_parts']):
                palette={ 'ABCD'[c] for c in pair }
                for block in blocks:
                    v,target_frame=frames[part['cube_targets_by_bitmask'][2**bit]];bit+=1
                    key=tuple(sorted((u,v)));allowed=relation.setdefault(key,set(itertools.product(range(4),repeat=2)))
                    for a,b in list(allowed):
                        left,right=(a,b) if u<=v else (b,a)
                        before,after=frame[left],target_frame[right]
                        if before!=after and {before,after}!=palette:allowed.remove((a,b))
    saved={tuple(r['variables']):{tuple(p) for p in r['allowed']} for r in certificate['binary_constraints']}
    require(len(saved)==len(certificate['binary_constraints']) and saved==relation,'binary relation mismatch')
    leaves=[];node_count=0
    def replay(node,domains):
        nonlocal node_count
        node_count+=1
        for var,value,other in node['remove']:
            require(value in domains[var],'duplicate or unauthorized elimination')
            key=tuple(sorted((var,other)));require(key in relation,'missing constraint')
            allowed=relation[key]
            if var==other:supported=(value,value) in allowed
            elif var<other:supported=any((value,b) in allowed for b in domains[other])
            else:supported=any((b,value) in allowed for b in domains[other])
            require(not supported,'elimination has a surviving support')
            domains[var].remove(value)
        if 'empty' in node:
            require(set(node)=={'remove','empty'} and not domains[node['empty']],'false contradiction')
            return
        require(all(domains),'unreported empty domain')
        if 'solution' in node:
            require(set(node)=={'remove','solution'},'solution node fields')
            v=node['solution'];require(len(v)==18,'solution length')
            require(all(domains[i]=={a} for i,a in enumerate(v)),'leaf is not fixed')
            require(all((v[i],v[j]) in allowed for (i,j),allowed in relation.items()),'invalid leaf')
            leaves.append(v);return
        require(set(node)=={'remove','branch','children'},'branch node fields')
        i=node['branch'];children=node['children'];require(len(domains[i])>1,'nonbranching variable')
        require([child['value'] for child in children]==sorted(domains[i]),'branch does not cover all values')
        for child in children:
            require(set(child)=={'value','node'},'child fields')
            ds=[set(d) for d in domains];ds[i]={child['value']};replay(child['node'],ds)
    replay(certificate['enumeration']['tree'],[set(range(4)) for k in keys])
    require(node_count==certificate['enumeration']['nodes'],'search node count')
    values=sorted(leaves)
    require(values==certificate['weak_functions'] and len(values)==25,'incomplete colour-function list')
    functions=[{sid:frame[v[i]] for sid,(i,frame) in frames.items()} for v in values]
    edges=[[a,b] for a in range(len(functions)) for b in range(a+1,len(functions))
           if not any(functions[a][sid]==functions[b][sid] for sid in states)]
    require(edges==certificate['maximal_type_edges'] and len(edges)==41,'maximal common-edge graph')
    pins=[next(i for i,f in enumerate(functions) if all(f[sid]==s['literal_row'][pin] for sid,s in states.items())) for pin in range(7)]
    require(pins==certificate['pin_types'],'pin type image')
    def disconnects(fs,es,ps):
        result=[]
        for sid,s in states.items():
            for j,part in enumerate(s['pairings']):
                for pair,blocks in zip(part['pairing'],part['terminal_parts']):
                    active={i for i,f in enumerate(fs) if 'ABCD'.index(f[sid]) in pair}
                    active_edges=[(a,b) for a,b in es if a in active and b in active]
                    for block in blocks:
                        reach={ps[block[0]]};previous=None
                        while previous!=reach:
                            previous=set(reach)
                            for a,b in active_edges:
                                if a in reach:reach.add(b)
                                if b in reach:reach.add(a)
                        if any(ps[p] not in reach for p in block):
                            result.append({'state':sid,'row':s['literal_row'],'pairing_index':j,
                              'colour_pair':pair,'pin_block':block,'reached_types':sorted(reach)})
        return result
    bad=disconnects(functions,edges,pins)
    require(bad==certificate['failed_blocks'] and len(bad)==1056,'failed-block certificate')
    require(bad[0]==certificate['first_obstruction'],'first obstruction')
    strict=[]
    for i,f in enumerate(functions):
        accepted=True
        for sid,s in states.items():
            for part in s['pairings']:
                vectors=[]
                for colour_pair,blocks in zip(part['pairing'],part['terminal_parts']):
                    for block in blocks:vectors.append(colour_pair)
                bits=[b for b in range(len(vectors)) if f[part['cube_targets_by_bitmask'][2**b]]!=f[sid]]
                if len(bits)!=1:accepted=False;break
                b=bits[0];palette=vectors[b]
                if 'ABCD'.index(f[sid]) not in palette:accepted=False;break
                swapped='ABCD'[sum(palette)-'ABCD'.index(f[sid])]
                expected=[swapped if mask&2**b else f[sid] for mask in range(len(part['cube_targets_by_bitmask']))]
                if expected!=[f[t] for t in part['cube_targets_by_bitmask']]:accepted=False;break
            if not accepted:break
        if accepted:strict.append(i)
    saved=certificate['strict_refinement'];require(strict==saved['weak_type_indices'] and len(strict)==13,'strict cube functions')
    sf=[functions[i] for i in strict]
    se=[[a,b] for a,b in itertools.combinations(range(len(strict)),2) if all(sf[a][sid]!=sf[b][sid] for sid in states)]
    sp=[strict.index(p) for p in pins]
    require(se==saved['maximal_type_edges'] and len(se)==18,'strict maximal edges')
    require(sp==saved['pin_types'],'strict pin image')
    require(disconnects(sf,se,sp)==saved['failed_blocks'],'strict failed blocks')
    require(certificate['hidden_state_covers']==certificate['all_22_row_graph_realizability']==certificate['general_claim']=='OPEN','scope upgraded')
    print(json.dumps({'status':'PASS','independent_replay':True,'proof_tree_nodes':node_count,'all_weak_functions':25,'maximal_edges':41,'failed_blocks':len(bad),'first_reached_types':bad[0]['reached_types']},sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',default=str(HERE/'certificate.json'));args=p.parse_args();run(args.certificate)
