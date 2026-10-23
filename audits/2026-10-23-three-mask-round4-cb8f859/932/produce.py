#!/usr/bin/env python3
"""Exclusive finite C9 folded-separator certificate producer."""
import gzip,hashlib,itertools,json
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
R3='audits/2026-10-23-three-mask-round3-cb8f859/932/'
R2='audits/2026-10-23-three-mask-round2-cb8f859/932/'
T2='audits/2026-10-13-c9-932-source-d521163/'
SOURCE=T2+'frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz'

def norm(word):
    seen={};return tuple(seen.setdefault(v,len(seen)) for v in word)

def indices(mask):
    while mask:
        bit=mask&-mask;yield bit.bit_length()-1;mask-=bit

def freeze():
    paths=[R3+p for p in ['REPORT.md','SOURCE_CONTRACT.md','paper/PROOF.md','certificate.json','INPUTS.json','VERIFICATION.json','MANIFEST.json']]
    paths += [R2+p for p in ['REPORT.md','SOURCE_CONTRACT.md','paper/PROOF.md','certificate.json.gz','INPUTS.json']]
    paths += [T2+'geometry/PROOF.md',T2+'counts/PAPER.md',T2+'SOURCE_CONTRACT.md',SOURCE]
    paths += ['audits/2026-10-23-three-mask-round4-cb8f859/'+p for p in ['BASE.json','START.md']]
    records=[]
    entry=json.loads((HERE.parent/'BASE.json').read_text());predecessors={r['path']:r for r in entry['predecessors']}
    for path in paths:
        blob=(REPO/path).read_bytes();digest=hashlib.sha256(blob).hexdigest()
        if path in predecessors:assert (len(blob),digest)==(predecessors[path]['bytes'],predecessors[path]['sha256'])
        dest=HERE/'frozen'/path;dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():assert dest.read_bytes()==blob  # Resume retained pre-certificate freeze only.
        else:
            with dest.open('xb') as f:f.write(blob)
        records.append({'path':path,'frozen_path':str(dest.relative_to(HERE)),'bytes':len(blob),'sha256':digest,
                        'authority':'immutable exact Git BASE' if path.startswith(T2) else 'immutable predecessor/round4 entry bytes'})
    routing=[]
    for r in entry['routing']:
        blob=(HERE.parent/r['snapshot']).read_bytes();dest=HERE/'frozen/routing'/r['path'];dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:f.write(blob)
        routing.append({**r,'frozen_path':str(dest.relative_to(HERE))})
    with (HERE/'INPUTS.json').open('x') as f:json.dump({'schema':'C9-folded-separator-inputs-v1','base':BASE,'inputs':records,
        'routing_background':routing,'write_boundary':str(HERE.relative_to(REPO))},f,indent=2,sort_keys=True);f.write('\n')

def grid(rows,site,equal):
    index={tuple(r):i for i,r in enumerate(rows)};end=0 if equal else 1
    group=[p for p in itertools.permutations(range(4)) if p[0]==0 and p[end]==end];paths=[]
    for length,start,finish in [(3,0,end),(4,end,0)]:
        words=[w for w in itertools.product(range(4),repeat=length) if all(a!=b for a,b in zip((start,)+w,w+(finish,)))];orbits={}
        for w in words:
            orbit=tuple(sorted({tuple(g[c] for c in w) for g in group}));orbits[orbit[0]]=orbit
        paths.append(sorted(orbits.items()))
    cells=[];coordinates={}
    for a,(u,uo) in enumerate(paths[0]):
        line=[]
        for b,(v,vo) in enumerate(paths[1]):
            options=set()
            for image in vo:
                shifted=(0,)+u+(end,)+image;word=shifted[-site:]+shifted[:-site] if site else shifted
                options.add(index[norm(word)])
            line.append(sorted(options))
            for p in options:assert p not in coordinates;coordinates[p]=(a,b)
        cells.append(line)
    return {'site':site,'anchor_mode':'equal' if equal else 'distinct','literal_anchors':[0,end],
            'whole_color_group':[list(g) for g in group],
            'left_arc_orbits':[[list(w) for w in orbit] for _,orbit in paths[0]],
            'right_arc_orbits':[[list(w) for w in orbit] for _,orbit in paths[1]],'row_options_grid':cells},coordinates

def main():
    freeze();src=json.loads(gzip.decompress((HERE/'frozen'/SOURCE).read_bytes()));rows=src['inner_pattern_order'];ob=src['kempe_obligations']
    queries=[q for q in src['queries'] if q['target']==932 and q['geometry_id']=='induced' and q['status']=='necessary_condition_residual']
    grids=[];contexts={}
    for site in range(9):
        contexts[site]=[]
        for equal in [False,True]:
            record,coordinates=grid(rows,site,equal);grids.append(record)
            contexts[site].append(([[sum(1<<p for p in opts) for opts in line] for line in record['row_options_grid']],coordinates))
    @lru_cache(None)
    def requirements(site,orbit):
        result=[]
        for cells,coordinates in contexts[site]:
            points=[coordinates[p] for p in indices(orbit) if p in coordinates]
            aa={a for a,b in points};bb={b for a,b in points}
            result.extend(cells[a][b] for a in sorted(aa) for b in sorted(bb))
        return tuple(result)
    traces=[]
    for query in queries:
        for site in range(9):
            support=query['fixed_point'];turns=[]
            while True:
                remove=[]
                for row in indices(support):
                    bad=[split for split,options in enumerate(ob[row]) if all(orbit&~support or any(not(mask&support) for mask in requirements(site,orbit)) for orbit in options)]
                    if bad:remove.append({'row':row,'failed_splits':bad})
                if not remove:break
                after=support&~sum(1<<r['row'] for r in remove)
                turns.append({'before':support,'removals':remove,'after':after});support=after
            assert support==0
            traces.append({'query_id':query['query_id'],'site':site,'original_center_multiplicities':[1,2],
                           'initial':query['fixed_point'],'rounds':turns,'fixed_point':support,
                           'verdict':'both original distance-four centre hypotheses excluded'})
        print(json.dumps({'query_id':query['query_id'],'sites_excluded':9}),flush=True)
    prior=json.loads((HERE/'frozen'/R3/'certificate.json').read_text())
    data={'schema':'C9-folded-separator-exclusion-v1','base':BASE,'case_bindings':prior['case_bindings'],'grids':grids,'traces':traces,
          'whole_option_policy':'all complete boundary orbits; every failed split rejects every option using the same before support',
          'conclusions':{'original_distance_four_centres':0,'original_case_pair_hypotheses_excluded':180,
              'original_case_pair_multiplicity_hypotheses_excluded':360,'remaining_contact_templates_each_collar':1,
              'remaining_named_zero_pair_templates':20,'new_unconditional_C9_row_deletions':0,
              'zero_pair_h4_branch':'OPEN','general_932':'OPEN','h_ge_5':'OPEN','smaller_bad':'OPEN','K_infinity':'OPEN',
              'new_Lean':False,'k_common_minimum_inherited':23,'new_k_bound':False,'source_graph_controls':'not triggered'}}
    blob=gzip.compress(json.dumps(data,sort_keys=True,separators=(',',':')).encode(),mtime=0)
    with (HERE/'certificate.json.gz').open('xb') as f:f.write(blob)
    print(json.dumps({'status':'produced exclusively','case_pair_traces':len(traces),'rounds':sum(len(t['rounds']) for t in traces),
                      'conditional_row_deletions':sum(len(r['removals']) for t in traces for r in t['rounds'])}))

if __name__=='__main__':main()
