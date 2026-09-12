#!/usr/bin/env python3
"""Translate untrusted JSON data into closed Lean inputs; the checker recomputes Sigma."""
import argparse
import hashlib
import json
import re
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', default='artifacts/boundary/bad_certificates.jsonl')
    p.add_argument('--output', default='Math/GeneratedCertificates.lean')
    p.add_argument('--namespace', default='FiveBoundary')
    p.add_argument('--split', action='store_true', help='Use proven split-interior checker')
    p.add_argument('--relation', action='store_true', help='Allow GOOD/empty exact relations; requires --split')
    a = p.parse_args()
    assert not a.relation or a.split
    assert re.fullmatch(r'FiveBoundary(?:\.[A-Za-z][A-Za-z0-9_]*)*', a.namespace)
    certificates = [json.loads(line) for line in Path(a.input).read_text().splitlines()]
    sigmas = []
    rows = []
    for c in certificates:
        digest = c.pop('sha256')
        assert hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest() == digest
        assert type(c['n']) is int and 5 <= c['n'] <= (15 if a.split else 10)
        assert c['boundary'] == list(range(5)), 'Only fixed ordered boundary supported'
        assert all(len(e)==2 and all(type(x) is int and 0 <= x < c['n'] for x in e) for e in c['edges'])
        assert all(len(b)==5 and all(type(x) is int and 0 <= x < 4 for x in b) for b in c['sigma'])
        from itertools import product
        universe = [b for b in product(range(4),repeat=5) if all(b[i]!=b[(i+1)%5] for i in range(5))]
        assert c['sigma_bits_hex'] == format(sum(1 << i for i,b in enumerate(universe) if list(b) in c['sigma']), '060x')
        s = tuple(tuple(b) for b in c['sigma'])
        if s not in sigmas:
            sigmas.append(s)
        es = '['+','.join(f'({u},{v})' for u,v in c['edges'])+']'
        if a.split:
            parts = [f'({u},{v})' for u,v in c['edges']]
            es = '[' + ',\n    '.join(','.join(parts[j:j+8])
                                     for j in range(0, len(parts), 8)) + ']'
        prefix = f'{c["n"]-5}, ' if a.split else f'{c["n"]}, by decide, '
        rows.append(f'  -- JSON SHA-256: {digest}\n'
                    f'  ⟨{prefix}{es},\n    expected{sigmas.index(s)}.toFinset⟩')
    lines = ['/-', 'Copyright (c) 2026 raylei50653. All rights reserved.',
             'Released under Apache 2.0 license as described in the file LICENSE.',
             'Authors: raylei50653', '-/',
             'import Math.SplitCertificate' if a.split else 'import Math.Certificates', '',
             '/-! Generated data. Run scripts/export_certificates.py to regenerate.',
             'Native computation is intentional; see docs/phase1.md for the trust boundary. -/',
             'set_option linter.style.nativeDecide false', 'set_option linter.style.setOption false',
             f'namespace {a.namespace}', 'set_option maxRecDepth 100000', 'set_option maxHeartbeats 0', '']
    for i,s in enumerate(sigmas):
        colors = ['!['+','.join(map(str,b))+']' for b in s]
        chunks = ',\n  '.join(','.join(colors[j:j+4]) for j in range(0,len(colors),4))
        lines.append(f'def expected{i} : List BoundaryColoring := [\n  {chunks}\n]')
    kind = 'SplitCertificate' if a.split else 'Certificate'
    checker = 'checkSplitCertificate' if a.split else 'checkCertificate'
    if a.relation:
        checker = 'checkRelationCertificate'
    sound = 'splitChecker_sound' if a.split else 'checker_sound'
    bound = 'by omega' if a.split else 'c.large'
    valid_proof = (f'theorem all_certificates_valid : certificates.all {checker} = true := by\n'
                   '  native_decide') if a.relation else (
                   f'theorem all_certificates_valid : certificates.all {checker} = true := by native_decide')
    lines += ['', f'def certificates : List {kind} := [', ',\n'.join(rows), ']', '',
              f'theorem certificate_count : certificates.length = {len(rows)} := by decide',
              valid_proof]
    if a.relation:
        lines += [
              'theorem all_certificates_exact (c : SplitCertificate) (hc : c ∈ certificates)',
              '    (b : BoundaryColoring) :',
              '    b ∈ Sigma (graphOfEdges c.edges) (firstBoundary (by omega)) ↔',
              '      b ∈ c.expected := by',
              '  exact relationChecker_exact c ((List.all_eq_true.mp all_certificates_valid) c hc) b']
    else:
        lines += [
              f'theorem all_certificates_bad (c : {kind}) (hc : c ∈ certificates) :',
              f'    BAD (graphOfEdges c.edges) (firstBoundary ({bound})) := by' if a.split else
              '    BAD (graphOfEdges c.edges) (firstBoundary c.large) := by',
              f'  exact {sound} c ((List.all_eq_true.mp all_certificates_valid) c hc)']
    lines += ['', f'end {a.namespace}', '']
    Path(a.output).write_text('\n'.join(lines))
    print(f'Exported {len(rows)} certificates, {len(sigmas)} distinct expected Sigma sets')

if __name__ == '__main__':
    main()
