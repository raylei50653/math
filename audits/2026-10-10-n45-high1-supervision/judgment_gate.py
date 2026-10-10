#!/usr/bin/env python3
"""Check explicit review scope and custody; semantic conclusions are human paper review."""
import json
from review import BASE,ROOT,OUT,WORKER,contract,file_state,git,put,sha

def main():
    claims=json.loads((WORKER/'claims.json').read_text())['claims'];ids=[c['id'] for c in claims]
    reports={}
    for suffix in ['h1a','h1r','h1c']:
        path=ROOT/f'audits/2026-10-10-n45-{suffix}/independent-judgment.json'
        j=json.loads(path.read_text());assert j['BASE']==BASE and j['general_N2_E']=='OPEN' if suffix!='h1r' else j['BASE']==BASE and j['broader_scope']['general_N2_E']=='OPEN'
        assert j['new_Lean'] is False
        if suffix=='h1c':
            assert j['decision']=='accepted_artifact_integrity_only' and j['findings']==[]
            assert j['paper_mathematics']=='not adjudicated' and j['worker_paper_claim_ids']==ids
        else:
            assert [c['id'] for c in j['claims']]==ids and j['blocking_findings']==[]
            assert j['nonblocking_findings']==[]
            if suffix=='h1a':assert j['full_source_contract']==contract() and j['new_assumptions']==[]
            for c in j['claims']:
                assert c['machine_proved'] is False and c['new_Lean'] is False
                assert c['quantifier'] and c['dependencies'] and c['conclusion']
                if suffix=='h1a':
                    assert c['full_source_contract']==contract() and c['additional_premises']==[]
                    assert c['verdict']=='holds'
                else:
                    assert [h['id'] for h in c['full_source_contract']]==['H'+str(i) for i in range(1,14)]
                    assert c['full_source_contract']==j['claims'][0]['full_source_contract']
                    assert c['verdict']=='accepted within full H1-H13 paper scope'
                    assert c['gap'] is None and c['new_sufficient_premises']==[]
        reports[suffix]={'decision':j['decision'],'judgment_sha256':sha(path.read_bytes()),
                         'paper_contract_alignment':'H1A verbatim; H1R thirteen paraphrases independently aligned by supervisor; not a semantic theorem check'}
    before=json.loads((OUT/'inputs-before.json').read_text())
    assert git('rev-parse','HEAD').decode().strip()==BASE
    assert git('diff','--cached','--binary')==(OUT/'cached-before.diff').read_bytes()
    for rel,state in before['existing'].items():
        f=ROOT/rel;now=file_state(f) if f.exists() or f.is_symlink() else {'kind':'missing'}
        assert now==state,rel
    for s in ['h1a','h1r','h1c']:
        assert (OUT/f'logs/{s}-normal.stdout.log').read_bytes()==(OUT/f'logs/{s}-seed17.stdout.log').read_bytes()
    put('judgment-gate.json',{'ten_claim_ids':ids,'full_source_contract':contract(),'reviewer_reports':reports,
                            'pre_adoption_existing_files_unchanged':True,'actual_six_peer_replays_exit_zero':True,
                            'paper_proved_by_this_tool':False})
    print(json.dumps({'structured_scope_gate':'holds','paper_reviews':2,'artifact_only_review':1,
                      'claims':10,'source_premises':13,'pre_adoption_file_identity':'holds','theorem_check':False},sort_keys=True))
if __name__=='__main__':main()
