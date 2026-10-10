#!/usr/bin/env python3
"""Small wrong-declaration probes on frozen legal inputs; no new graph edges."""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HOME = Path(__file__).resolve().parent
PC = HOME/'inputs/pc'


def encode(x):
    return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()


def create(path,data):
    with path.open('xb') as f:
        f.write(data)


def load(path):
    return json.loads(path.read_text())


def check(condition,reason):
    if not condition:
        raise AssertionError(reason)


def run(label,proposal):
    stdout=HOME/'logs'/f'{label}.stdout.log'; stderr=HOME/'logs'/f'{label}.stderr.log'; command=HOME/'logs'/f'{label}.command.json'
    argv=[sys.executable,'-B',str(PC/'checker.py'),'--source',str(proposal)]
    with stdout.open('xb') as out,stderr.open('xb') as err,command.open('xb') as cmd:
        start=time.monotonic()
        result=subprocess.run(argv,cwd=HOME.parent.parent,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=out,stderr=err)
        metadata={'argv':argv,'cwd':str(HOME.parent.parent),'exit_code':result.returncode,'elapsed_seconds':time.monotonic()-start,
                  'stdout':str(stdout.relative_to(HOME)),'stderr':str(stderr.relative_to(HOME)),'env':{'PYTHONDONTWRITEBYTECODE':'1'}}
        cmd.write(encode(metadata))
    check(result.returncode==2,'expected fail-closed exit2: '+label)
    check(stderr.read_bytes()==b'','unexpected stderr: '+label)
    payload=load(stdout)
    return metadata,payload


def main():
    original_path=PC/'controls-v2/NA7-0002-P1.json'
    original=load(original_path)
    graph_path=(original_path.parent/original['graph_file']).resolve()
    raw=load(graph_path)
    cert=load(PC/'certificate-final-v2.json')
    g=next(x['graph'] for x in cert['fixed_sources'] if x['graph']['id']=='NA7-0002')
    beta=g['rows'][0]['literal_beta'];lift=g['rows'][0]['all_16_fibres'][4]['full_lifts'][0]
    f=dict(zip(g['vertices'],lift))
    check(all(f[a]!=f[b] for a,b in raw['edges']),'original legal whole lift oracle')
    p=next(p for p in g['pieces'] if p['id']=='P0')
    original_tuple=[f[v] for v in p['contact_order']]
    oracle={'original_graph_sha256':sha256(graph_path.read_bytes()).hexdigest(),'original_graph':str(graph_path.relative_to(HOME)),
            'vertices':g['vertices'],'edges':raw['edges'],'literal_beta':beta,'full_legal_original_lift':lift,
            'shared_original_vertex':9,'original_root_contact_edges':[[5,9],[6,9]],'piece':'P0','contact_order':p['contact_order'],'original_contact_tuple':original_tuple}
    check(all(e in raw['edges'] for e in oracle['original_root_contact_edges']),'actual shared original contact edges')
    create(HOME/'probes/original-oracle.json',encode(oracle))
    summary=[]
    metadata,result=run('legal-fixed-missing-LP',original_path)
    check(result['source_contract']['status']=='not triggered','legal control must be missing LP')
    summary.append({'id':'legal-fixed-missing-LP','command':metadata,'source_contract':result['source_contract'],'layers':result['layers']})
    for item in load(PC/'negative-inputs-v2/index.json'):
        metadata,result=run('existing-'+item['id'],PC/item['proposal'])
        finding=result['source_contract']['finding']
        check(result['source_contract']['status']=='counterexample' and item['expected_error'] in finding,'existing negative exact reason '+item['id'])
        summary.append({'id':item['id'],'kind':'existing malformed-declaration control','command':metadata,'status':result['source_contract']['status'],'finding':finding,'original_oracle':item['oracle']})
    proposals=[]

    def proposal(label,expected,edit,graph_edit=None):
        q=deepcopy(original)
        q['graph_file']='../'+str(graph_path.relative_to(HOME))
        edit(q)
        if graph_edit:
            changed=deepcopy(raw); graph_edit(changed)
            check(changed['vertices']==raw['vertices'] and changed['edges']==raw['edges'],'probe changed graph edges/vertices')
            gp=HOME/'probes'/f'{label}-graph.json'
            create(gp,encode(changed));q['graph_file']=gp.name;q['source_sha256']=sha256(gp.read_bytes()).hexdigest()
        qp=HOME/'probes'/f'{label}.json';create(qp,encode(q))
        proposals.append({'id':label,'proposal':str(qp.relative_to(HOME)),'expected':expected,'oracle':'probes/original-oracle.json','source_edges_unchanged':True})

    proposal('missing-original-rotation','ordered_induced_C5_disk',lambda q:[p.pop('shield',None) for p in q['pieces']],lambda r:r.pop('rotation'))
    proposal('wrong-rotation-neighbor-set','rotation neighborhood differs from original edges',lambda q:None,lambda r:r['rotation']['5'].pop())
    proposal('omitted-empty-fibre','complete empty/nonempty fibres differ',lambda q:q['pieces'][0]['rows'][0]['fibres'].pop(next(i for i,f in enumerate(q['pieces'][0]['rows'][0]['fibres']) if not f['tuple_indices'])))
    proposal('omitted-complete-component','declared pieces are not all complete original H-root components',lambda q:q['pieces'].pop())
    proposal('wrong-partial-L-role','declared L has wrong original actual support',lambda q:q['roles'].update(L='P0'))
    proposal('missing-critical-edge-witness','declared critical witnesses do not cover every original nonframe edge exactly once',lambda q:q.update(critical_witnesses=[]))
    create(HOME/'probes/index.json',encode(proposals))
    for item in proposals:
        metadata,result=run('probe-'+item['id'],HOME/item['proposal'])
        status=result['source_contract']['status']
        if item['id']=='missing-original-rotation':
            check(status=='not triggered' and item['expected'] in result['source_contract']['missing_sufficient_premises'],'missing rotation must fail-closed')
            finding=result['layers']['ordered_induced_C5_disk']
        else:
            finding=result['source_contract']['finding']
            check(status=='counterexample' and item['expected'] in finding,'new negative exact reason '+item['id'])
        summary.append({'id':item['id'],'kind':'fresh wrong-declaration control on unchanged original edges/vertices','command':metadata,'status':status,'finding':finding,'oracle':'probes/original-oracle.json'})
    create(HOME/'checks/probe-results.json',encode({'checks':summary,'scope':'Six fresh declaration probes, five existing negatives, one legal missing-LP control. No mathematical source counterexamples.'}))
    print(json.dumps({'probe_checks':len(summary),'all_exit2':True,'new_probes':len(proposals),'existing_negatives':5,'legal_missing_LP':1},sort_keys=True))


if __name__=='__main__':
    main()
