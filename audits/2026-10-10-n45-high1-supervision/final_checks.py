#!/usr/bin/env python3
"""Bind actual subprocess records and streams, including retained expected FAILs."""
import json
from review import OUT,put,sha

def main():
    commands=[]
    for f in sorted((OUT/'logs').glob('*.json')):
        record=json.loads(f.read_text());label=f.stem
        expected=2 if label.startswith('negative-') else 1 if label in ['base-historical-doc-fail','whole-docgraph'] else 0
        assert record['exit_code']==expected,(label,record['exit_code'],expected)
        record.update(label=label,expected_exit=expected)
        for stream in ['stdout','stderr']:
            rel=f'logs/{label}.{stream}.log';record[stream+'_file']=rel;record[stream+'_sha256']=sha((OUT/rel).read_bytes())
        commands.append(record)
    assert len(commands)==24
    stages={'negative-certificate':'certificate byte comparison','negative-input-index':'input validation / fixed-domain reconstruction',
            'negative-receipt':'delivery/receipt exact binding','negative-nested-receipt':'payload inventory'}
    for label,stage in stages.items():assert json.loads((OUT/f'logs/{label}.stderr.log').read_text())['stage']==stage
    for s in ['h1a','h1r','h1c']:
        assert (OUT/f'logs/{s}-normal.stdout.log').read_bytes()==(OUT/f'logs/{s}-seed17.stdout.log').read_bytes()
    for s in ['worker-envelope']:
        assert (OUT/f'logs/{s}-normal.stdout.log').read_bytes()==(OUT/f'logs/{s}-seed17.stdout.log').read_bytes()
    whole=(OUT/'logs/whole-docgraph.stderr.log').read_text()
    assert sum('duplicate' in x.lower() for x in whole.splitlines())==62
    put('checks.json',{'commands':commands,'actual_commands':len(commands),'peer_normal_seed17_stdout_byte_equal':True,
        'four_wrong_artifact_actual_stages':stages,'historical_failure_expected_exits_retained':True,
        'whole_docgraph_duplicate_ID_errors':62,'paper_proved_by_these_checks':False})
    print(json.dumps({'actual_logged_commands':len(commands),'expected_nonzero_retained':6,'remaining_expected_zero':18,
                      'all_actual_exits_match':True,'paper_check':False},sort_keys=True))
if __name__=='__main__':main()
