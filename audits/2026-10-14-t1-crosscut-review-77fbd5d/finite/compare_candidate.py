#!/usr/bin/env python3
"""Compare reconstructed essentials with the subsequently supplied archive.

Reads candidate data only. Neither candidate producer nor verifier is imported.
The candidate's 32 additional BRIDGE cases are outside this comparison.
"""
from pathlib import Path
import gzip
import hashlib
import json


def run():
    here = Path(__file__).resolve().parent
    candidate = here.parent/'candidate-original/t1_broad_probe'
    with gzip.open(here/'certificate.json.gz','rt') as stream:
        rebuilt = json.load(stream)
    index = {(case['pair'],case['query']):case for case in rebuilt['cases']}
    results = []
    for pair in range(4):
        source_path = candidate/f'twohole_PINCH_{pair}.json'
        lift_path = candidate/f'independent_full_lifts_PINCH_{pair}.jsonl.gz'
        source = json.loads(source_path.read_text())
        assert source['rows'] == rebuilt['C6_rows']
        with gzip.open(lift_path,'rt') as stream:
            candidate_lifts = [json.loads(line) for line in stream]
        assert len(source['records']) == len(candidate_lifts) == 8
        for claimed,fibres in zip(source['records'],candidate_lifts):
            case = index[(pair,claimed['query'])]
            assert claimed['kind'] == 'PINCH'
            assert not claimed['incomplete'] and claimed['excluded']
            for field in ('pair','query','collar','target','vertices','edges','interfaces','matrix'):
                assert claimed[field] == case[field], (case['name'],field)
            assert claimed['shell_lift_counts'] == case['full_lift_counts']
            assert claimed['intersections'] == case['rectangle_count']
            assert sorted(claimed['rectangles']) == sorted(case['rectangles'])
            assert len({tuple(row) for row in claimed['rectangles']}) == len(case['rectangles'])
            assert fibres['interfaces'] == case['interfaces']
            assert fibres['vertices'] == case['vertices']
            assert set(fibres['fibres_by_B']) == set(rebuilt['B_rows'])
            for beta,lifts in zip(rebuilt['B_rows'],case['full_lifts']):
                assert sorted(fibres['fibres_by_B'][beta]) == lifts, (case['name'],beta)
                assert len(set(lifts)) == len(lifts)
            results.append(dict(name=case['name'],rectangle_count=case['rectangle_count'],
                                literal_lifts=case['total_full_lifts'],match=True))
    assert len(results) == 32
    report = dict(status='PASS',scope='32 essential PINCH-labeled single-x shells',
                  source='independent reconstruction completed before inspecting candidate output data',
                  candidate_algorithms_read_or_imported=False,
                  checks=['original named graph and interface equality','all 31 x 31 matrix entries including zeros',
                          'all maximal rectangles and all six certificate columns',
                          'every literal shell lift for each fixed original B row'],
                  certificate_sha256=hashlib.sha256((here/'certificate.json.gz').read_bytes()).hexdigest(),
                  counts=dict(cases=32,rectangles=sum(r['rectangle_count'] for r in results),
                              literal_lifts=sum(r['literal_lifts'] for r in results)),cases=results)
    (here/'candidate_comparison.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(report['counts'],sort_keys=True))
    print('Candidate essential data comparison PASS')


if __name__ == '__main__':
    run()
