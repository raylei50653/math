#!/usr/bin/env python3
"""Whole-component maps on complete fibres; no graph realization claim."""
import argparse
import hashlib
import json
from pathlib import Path
D=Path(__file__).resolve().parent
P='audits/2026-10-20-r6-941-last-rejection-f13eb4d/'
def calculate():
    for row in json.loads((D/'INPUTS.json').read_text()):
        assert hashlib.sha256((D/'frozen'/row['path']).read_bytes()).hexdigest()==row['sha256']
    c=json.loads((D/'frozen'/P/'J1/certificate.json').read_text())
    fs=c['component_records']; us=[f['core'] for f in fs]
    def swap(u,p,root,pair):
        return [pair[1] if x==pair[0] and p[j]==p[root] else pair[0] if x==pair[1] and p[j]==p[root] else x for j,x in enumerate(u)]
    def flip23(u):return [5-x if x in (2,3) else x for x in u]
    witnesses=[]
    # d-switch: K_23(R), followed by the fixed global transposition (23).
    # Its inverse is itself, since global (23) commutes with K_23(R).
    for i,f in enumerate(fs):
        target=us[i].copy();target[6]=target[9]=5-target[6]
        for p in f['splits'][0]['partitions']:
            out=flip23(swap(us[i],p,2,(2,3)))
            assert out==target
            assert flip23(swap(out,p,2,(2,3)))==us[i]
        witnesses.append({'source':us[i],'target':target,'map':'global23 after K23(R)','partitions':len(f['splits'][0]['partitions'])})
    # q-switch is a bijection precisely onto the singleton-boundary-block stratum.
    for i in range(4):
        u=us[i];target=u.copy();target[4]=3
        j=us.index(target)
        for p in fs[i]['splits'][2]['partitions']:
            assert [k for k in range(10) if p[k]==p[4]]==[4]
            assert swap(u,p,4,(0,3))==target
        singleton=0; residual=[]
        for p in fs[j]['splits'][2]['partitions']:
            block=[k for k in range(10) if p[k]==p[4]]
            if block==[4]:
                singleton+=1;assert swap(target,p,4,(0,3))==u
            else:
                residual.append(block)
                if u[6]==2:
                    z0=7 if u[7]==0 else 8
                    assert z0 in block
        assert singleton==1 and len(residual)==2
        witnesses.append({'source':u,'target':target,'map':'K03(q)','image':'q component meets rim only at q','residual_blocks':residual})
    # J2 family III has the same d-switch, with R=2,L=3 fixed after normalization.
    j2=json.loads((D/'frozen'/P/'J2/certificate.json').read_text())
    for f in j2['forms']:
        if f['family']!=3:continue
        u=f['literal_core'];target=u.copy();target[6]=target[9]=5-target[6]
        for rec in f['pair_records'][0]['partitions']:
            p=rec['partition'];out=flip23(swap(u,p,2,(2,3)))
            assert out==target and flip23(swap(out,p,2,(2,3)))==u
        witnesses.append({'source':u,'target':target,'map':'J2 III global23 after K23(R)'})
    return {'status':'conditional full-fibre transport; last rejection OPEN','source_realized':False,'witnesses':witnesses,'J1_reduction':'N01021=4*(A01+A10)+2*(E01+E10); zero iff B01=B10=0','J2_representatives':10}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=D/'certificate.json');a=ap.parse_args()
    out=calculate()
    if a.build:
        with a.certificate.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    else:assert json.loads(a.certificate.read_text())==out
    print(json.dumps({'status':'PASS','maps':len(out['witnesses']),'last_rejection':'OPEN'}))
if __name__=='__main__':main()
