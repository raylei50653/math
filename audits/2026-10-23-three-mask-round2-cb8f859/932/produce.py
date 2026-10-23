#!/usr/bin/env python3
"""Exclusive-create 180 original triple-contact exclusion traces.

Fixed boundary interfaces only; no source graphs are enumerated. check.py is
independent and does not import this file or the exploratory probe.
"""
import gzip,hashlib,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
PRED='audits/2026-10-23-three-mask-methods-cb8f859/932/'
SOURCE=PRED+'frozen/audits/2026-10-13-c9-932-source-d521163/frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz'

def bits(mask):
    while mask:
        one=mask&-mask;yield one.bit_length()-1;mask-=one

def main():
    data=json.loads(gzip.decompress((HERE/'frozen'/SOURCE).read_bytes()))
    predecessor=json.loads((HERE/'frozen'/PRED/'certificate.json').read_text())
    rows=[tuple(p) for p in data['inner_pattern_order']]
    obligations=data['kempe_obligations']
    orbits={m for row in obligations for split in row for m in split}
    queries=[q for q in data['queries'] if q['target']==932 and q['geometry_id']=='induced' and q['status']=='necessary_condition_residual']
    matrices=[];traces=[]
    for site in range(9):
        coordinate={}; grid={}
        for index,word in enumerate(rows):
            p=word[site:]+word[:site]
            if len({p[0],p[1],p[5]})!=3:continue
            relabel={p[0]:0,p[1]:1,p[5]:2}
            relabel[next(c for c in range(4) if c not in relabel)]=3
            p=tuple(relabel[c] for c in p)
            a,b=p[2:5],p[6:9];coordinate[index]=(a,b);grid[a,b]=index
        left=sorted({a for a,b in grid});right=sorted({b for a,b in grid})
        matrices.append({'triple_index':site,'literal_anchors':[0,1,2],'literal_t_color':3,'left_arc_words':left,'right_arc_words':right,'row_grid':[[grid[a,b] for b in right] for a in left]})
        def close(mask):
            coords=[coordinate[j] for j in bits(mask) if j in coordinate]
            aa={a for a,b in coords};bb={b for a,b in coords}
            for a in aa:
                for b in bb:mask|=1<<grid[a,b]
            return mask
        closed={mask:close(mask) for mask in orbits}
        for query in queries:
            support=query['fixed_point'];initial=support;rounds=[]
            while True:
                removals=[]
                for row in bits(support):
                    bad=[s for s,opts in enumerate(obligations[row]) if all(closed[m]&~support for m in opts)]
                    if bad:removals.append({'row':row,'splits':bad})
                if not removals:break
                rounds.append({'before':support,'removals':removals})
                for record in removals:support&=~(1<<record['row'])
            assert support==0
            traces.append({'query_id':query['query_id'],'triple_index':site,'initial':initial,'rounds':rounds,'fixed_point':support,'verdict':'original triple-contact hypothesis excluded'})
        print(json.dumps({'site':site,'original_cases':len(queries),'excluded':20}),flush=True)
    payload={'schema':'C9-original-triple-rectangle-exclusion-v1','base':'cb8f8593e273a7426ecadd59797a6e643cc4768e','case_bindings':predecessor['case_bindings'],'matrices':matrices,'traces':traces,'conclusions':{'original_triple_contacts':0,'excluded_original_case_site_hypotheses':180,'general_932_exclusion':False,'no_triple_h4_branch':'OPEN','k_common_minimum_inherited':23,'new_k_bound':False,'new_Lean':False,'source_graph_controls':'not triggered'}}
    with (HERE/'certificate.json.gz').open('xb') as out:
        with gzip.GzipFile(fileobj=out,mode='wb',mtime=0) as stream:stream.write((json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode())

if __name__=='__main__':main()
