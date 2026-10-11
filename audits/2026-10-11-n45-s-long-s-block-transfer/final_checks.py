"""Final read-only content/custody checks, before exclusive delivery sealing."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode=True
import checker
import custody
import direct_enumerator
import transfer

HERE=Path(__file__).resolve().parent

def main():
    checker.authority_check()
    protected=json.loads((HERE/'logs/custody-before.stdout').read_text())
    current=custody.snapshot()
    changed=[p for p,h in protected['files'].items() if current['files'].get(p)!=h]
    assert not changed,changed
    assert current['head']==protected['head']=='f2692089ad4259808e27d9b7e882ac09505b180a'
    assert current['tracked_diff_sha256']==protected['tracked_diff_sha256']
    cert=json.loads((HERE/'certificate.json').read_text())
    assert cert==transfer.calculate(HERE/'cases.json')
    assert cert==direct_enumerator.enumerate_certificate((HERE/'cases.json').read_bytes())
    certificate_snapshot=json.loads((HERE/'logs/custody-certificate-before.stdout').read_text())
    cert_key=str((HERE/'certificate.json').relative_to(custody.ROOT))
    assert current['files'][cert_key]==certificate_snapshot['files'][cert_key]
    for pair in [('check-normal','check-seed17'),('direct-normal','direct-seed17')]:
        for stream in ['stdout','stderr']:
            assert (HERE/'logs'/f'{pair[0]}.{stream}').read_bytes()==(HERE/'logs'/f'{pair[1]}.{stream}').read_bytes()
    for name in ['negative-r','negative-empty','negative-branch','direct-negative-r','direct-negative-empty','direct-negative-branch']:
        result=json.loads((HERE/'logs'/f'{name}.result.json').read_text())
        assert result['exit_code']==1
    assert 'original vertex=r' in (HERE/'logs/negative-r.stderr').read_text()
    assert 'tuple=[0, 0],r=0,empty=True' in (HERE/'logs/negative-empty.stderr').read_text()
    assert 'original vertex l2' in (HERE/'logs/negative-branch.stderr').read_text()
    for i in [0,1]:
        assert json.loads((HERE/'logs'/f'missing-{i}.result.json').read_text())['exit_code']==128
    coverage=json.loads((HERE/'coverage.json').read_text())
    claims=json.loads((HERE/'claims.json').read_text())
    adopted=json.loads((HERE/'authority/sealed/audits/2026-10-11-n45-s-long-s-review/remaining-schedules.json').read_text())
    keys=lambda s:(s['t_s'],s['SigmaG_orbit'],tuple(s['QG']),s['beta_q'])
    assert {keys(s) for s in coverage['assigned_schedules']}=={keys(s) for s in adopted['remaining_schedules']}
    assert len(coverage['assigned_schedules'])==24
    assert sum(len(s['variants']) for s in coverage['assigned_schedules'])==38
    pin_count=0
    for schedule in coverage['assigned_schedules']:
        assert schedule['Delta']==sorted(set(schedule['QG'])-{schedule['beta_q']})
        assert not schedule['new_proved_restoration_rows'] and not schedule['new_source_minors']
        for variant in schedule['variants']:
            assert [r['literal'] for r in variant['ten_rows']]==transfer.LITERALS
            for row in variant['ten_rows']:
                assert len(row['pins'])==16
                assert [(p['r'],p['s']) for p in row['pins']]==[(a,b) for a in range(4) for b in range(4)]
                assert row['gamma_b4']==int(row['literal'][4])
                pin_count+=16
    assert pin_count==6080
    assert claims['recurrence_requires_K11_K12'] is False
    assert coverage['target_source']=={'executed':False,'trigger_count':None,'status':'not triggered'}
    assert coverage['finite_calibration']['source_lifts_computed'] is False
    assert coverage['finite_calibration']['disk_topology_verified'] is False
    assert len(claims['claims'])==7
    for claim in claims['claims']:
        assert all(k in claim for k in ['quantifier','premises','conclusion_type','dependencies','original_e','original_r_coordinate'])
        assert claim['original_e']==['r','b4'] and claim['original_r_coordinate']=='r'
    assert not any(p.name=='__pycache__' or p.suffix=='.pyc' or p.is_symlink() for p in HERE.rglob('*'))
    assert not (HERE/'delivery.json').exists(),'delivery collision'
    required=['REPORT.md','claims.json','inputs.json','coverage.json','checks.json','transfer-proof.md',
              'cases.json','certificate.json','checker.py','direct_enumerator.py','negative-plan.json',
              'negative-r-colour.json','negative-empty-cell.json','negative-missing-branch.json','local-review.md']
    assert all((HERE/p).is_file() for p in required)
    print(json.dumps({'status':'passes','adoption':'待獨立驗收','protected_files_zero_drift':len(protected['files']),
        'certificate_zero_drift':True,'assigned_schedules':24,'spoke_variants':38,'symbolic_ordered_pins':pin_count,
        'finite_assignments':sum(len(r['assignments']) for c in cert['cases'] for r in c['rows']),
        'negative_rejections':6,'new_source_exclusions':0,'no_bytecode_or_symlinks':True,
        'target_source':coverage['target_source']},ensure_ascii=False,sort_keys=True))

if __name__=='__main__':
    main()
