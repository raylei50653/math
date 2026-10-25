"""Read-only direct-graph check of the bounded replacement experiments."""
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import one_center
import two_centers

HERE = Path(__file__).resolve().parent


def graph(model, centers):
    parent=list(range(8))
    def find(v):
        while parent[v]!=v:
            v=parent[v]
        return v
    for a,b in model['equal']:
        a,b=find(a),find(b)
        parent[max(a,b)]=min(a,b)
    ports=[find(i) for i in range(8)]
    edges={tuple(sorted((ports[i],ports[(i+1)%8]))) for i in range(8)}
    edges|={tuple(sorted((ports[a],ports[b]))) for a,b in model['different']}
    neighbors=[model['neighbors']] if centers==1 else model['neighbors']
    for j,ns in enumerate(neighbors):
        edges|={(ports[v],8+j) for v in ns}
    if centers==2 and model['centers_adjacent']:
        edges.add((8,9))
    assert not any(a==b for a,b in edges),'loop in nonempty candidate'
    return ports,sorted(edges)


def direct_fibres(model, centers, words):
    ports,edges=graph(model,centers)
    fibres=[]
    for w in words:
        coloring={}
        consistent=True
        for p,c in zip(ports,w):
            if p in coloring and coloring[p]!=c:
                consistent=False
                break
            coloring[p]=c
        lifts=[]
        if consistent:
            for cs in product(range(4),repeat=centers):
                full=dict(coloring)
                full.update({8+j:c for j,c in enumerate(cs)})
                if all(full[a]!=full[b] for a,b in edges):
                    lifts.append(list(cs))
        fibres.append(lifts)
    return fibres


def validate(outputs):
    source_raw=one_center.SOURCE.read_bytes()
    source=json.loads(source_raw)
    words=[tuple(r['word']) for r in source['caps'][0]['complete_fibres']]
    digest=hashlib.sha256(source_raw).hexdigest()
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    assert inputs['base']=='78375cc0e995c868c221605c24835d7e622f0091','wrong frozen base'
    assert inputs['sha256']==digest,'frozen input hash mismatch'
    assert one_center.AUTHORITY.read_bytes()==source_raw,'authority bytes drift'
    assert len(words)==274 and len(set(words))==274
    assert len(source['caps'])==21
    reports=[]
    for centers,producer,output in zip((1,2),(one_center,two_centers),outputs):
        assert set(output)=={'schema','source','source_sha256','library','caps'},'unknown or missing contract field'
        assert output['schema']==('941-k8-one-center-v1' if centers==1 else '941-k8-two-centers-v1'),'wrong schema'
        assert len(output['caps'])==21,'missing cap'
        assert output['source_sha256']==digest,'source hash mismatch'
        assert output['source']==inputs['source'],'wrong source identity'
        catalog,counts=producer.make_catalog(words)
        assert output['library']==counts,'library counts mismatch'
        fibre_digest=hashlib.sha256()
        empty=lifts=0
        for mask,model in sorted(catalog.items()):
            full=direct_fibres(model,centers,words)
            actual=sum(1<<i for i,f in enumerate(full) if f)
            assert mask==actual,'candidate support differs from direct quotient graph'
            empty+=sum(not f for f in full)
            lifts+=sum(map(len,full))
            fibre_digest.update(json.dumps([mask,model,full],sort_keys=True,separators=(',',':')).encode())
        safe_total=0
        residual_total=0
        for original,claimed in zip(source['caps'],output['caps']):
            assert set(claimed)=={'distribution','old_residual_count','safe_candidates','new_residual'},'unknown or missing cap field'
            assert original['distribution']==claimed['distribution'],'cap order'
            support=sum(1<<i for i,r in enumerate(original['complete_fibres']) if r['full_lifts'])
            residual={tuple(w) for w in original['residual_accepting_words']}
            assert claimed['old_residual_count']==len(residual)
            expected=[]
            union=0
            for mask,model in sorted(catalog.items()):
                if mask&~support:
                    continue
                union|=mask
                expected.append(dict(**model,relation=[list(w) for i,w in enumerate(words) if mask>>i&1]))
            assert expected==claimed['safe_candidates'],'safe candidate list mismatch'
            missing=[list(w) for i,w in enumerate(words) if w in residual and not(union>>i&1)]
            assert missing==claimed['new_residual'],'residual mismatch'
            assert len(missing)==len(residual),'unexpected new exclusion must be independently reviewed'
            safe_total+=len(expected)
            residual_total+=len(missing)
        reports.append(dict(centers=centers,**counts,checked_fibres=len(catalog)*274,
            empty_fibres=empty,full_lifts=lifts,full_fibre_sha256=fibre_digest.hexdigest(),
            safe_total=safe_total,residual_total=residual_total,new_exclusions=0))
    return dict(status='PASS',source_sha256=digest,experiments=reports,
                finite_library='triggered and holds',actual_exterior_realization='not triggered',
                source_exclusion='none',K8_same_exterior='OPEN')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--one',type=Path,default=HERE/'ONE_CENTER.json')
    parser.add_argument('--two',type=Path,default=HERE/'TWO_CENTERS.json')
    args=parser.parse_args()
    result=validate([json.loads(args.one.read_text()),json.loads(args.two.read_text())])
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
