#!/usr/bin/env python3
"""Check recorded independent scope/coverage decisions, not mathematical truth."""
import json
from review import BASE, ROOT, OUT, WORKER, file_state, sha, tree

def read(p): return json.loads(p.read_text())
def main():
    w=read(WORKER/'claims.json'); ids=[c['id'] for c in w['claims']]
    assert ids==['LOW2-CORE','LOW2-COMP','LOW2-JOIN','LOW2-F','LOW2-MAP','LOW2-EXCLUSION']
    for name,verdict in [('l2a','holds_under_full_LOW2_source_contract'),
                         ('l2r','accepted_with_full_stated_LOW2_contract')]:
        j=read(ROOT/f'audits/2026-10-10-n45-{name}/independent-judgment.json')
        assert j['BASE']==BASE and [c['id'] for c in j['claims']]==ids
        assert not j['findings']
        for original,review in zip(w['claims'],j['claims']):
            assert review['verdict']==verdict
            assert review['source_contract']==w['full_source_contract']
            assert review['quantifier']==original['quantifier']
            assert review['dependencies']==original['dependencies']
            assert review['external_dependencies']==original['external_dependencies']
            assert review['additional_premises']==[] and review['machine_proved'] is False
    a=read(ROOT/'audits/2026-10-10-n45-l2a/independent-judgment.json')
    comp=a['composition']
    assert comp['decision']=='holds_given_accepted_LOW1_and_full_LOW2_exclusion'
    assert comp['uncovered_cases']==[] and comp['additional_premises']==[]
    assert [(c['original_U_incidence'],c['original_r_spokes'],c['original_s_spokes'])
            for c in comp['case_mapping']]==[(1,2,2),(2,1,2)]
    c=read(ROOT/'audits/2026-10-10-n45-l2c/independent-judgment.json')
    assert c['tool_verdict']=='ACCEPT_SCOPED_ARTIFACT_INTEGRITY' and not c['blocking_findings']
    for n in ('l2a','l2r','l2c'):
        assert (OUT/f'logs/{n}-normal.stdout.log').read_bytes()==(OUT/f'logs/{n}-seed17.stdout.log').read_bytes()
        for phase in ('normal','seed17'):
            assert read(OUT/f'logs/{n}-{phase}.json')['exit_code']==0
    initial=read(WORKER/'inputs-initial.json')
    for item in initial['pins']:
        assert sha((ROOT/item['path']).read_bytes())==item['expected']
    before=read(OUT/'inputs-before.json')
    assert tree(WORKER)==before['worker']
    for rel,state in before['existing'].items():
        p=ROOT/rel
        now=file_state(p) if p.exists() or p.is_symlink() else {'kind':'missing'}
        assert now==state,rel
    print(json.dumps({'recorded_scope_gate':'holds','LOW2_claims':ids,
                      'LOW_composition':'authority section1 exact S-SHORT-U-LOW only',
                      'independent_receipt_replay_pairs':3,'pre_adoption_current_pins':8,
                      'pre_existing_entries_unchanged':len(before['existing']),
                      'mathematics_proved_by_this_script':False},sort_keys=True))
if __name__=='__main__':main()
