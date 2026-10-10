#!/usr/bin/env python3
"""Apply the reviewed, exact five-file scoped adoption to unchanged baselines."""
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(name, data):
    with (HERE/name).open('x') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def main():
    intake = read(HERE/'intake.json')
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() == intake['BASE']
    h2r = read(HERE/'frozen/audits/2026-10-10-n45-h2r/independent-judgment.json')
    h2a = read(HERE/'frozen/audits/2026-10-10-n45-h2a/independent-judgment.json')
    h2c = read(HERE/'frozen/audits/2026-10-10-n45-h2c/independent-judgment.json')
    h3r = read(HERE/'frozen/audits/2026-10-10-n45-h3r/independent-judgment.json')
    assert len(h2r['claims']) == len(h2a['claims']) == 12
    assert h2c['paper_adjudicated'] is False
    assert sum(c['raw_verdict'] == 'gap' for c in h2r['claims']) == 1
    assert all(c['qualified_verdict'] in ['holds under stated hypotheses', 'holds with explicit qualification'] for c in h2r['claims'])
    contract_path = 'frozen/audits/2026-10-10-n45-h3a/frozen/authority/common-contract.md'
    text = (HERE/contract_path).read_text()
    kblock = text.split('## 全部 HIGH3 原來源契約\n', 1)[1].split('\n## 待核', 1)[0].strip()
    assert len(re.findall(r'^K\d+\.', kblock, re.M)) == 13
    claims = []
    for c in h2r['claims']:
        claims.append({'id': c['id'], 'raw_verdict': c['raw_verdict'],
                       'adopted_verdict': c['qualified_verdict'],
                       'complete_source_domain': 'every finite arbitrary-size G satisfying all original H1-H13',
                       'new_source_hypotheses': [],
                       'query_qualification': 'Only unused-Dgamma restoration construction: proper gamma uses exactly three colors on all B' if c['id'] == 'H2-EXCLUSION' else None,
                       'independent_proofs': ['H2A REPORT §§2-5', 'H2R REPORT §§2-6'],
                       'BASE_sections': c['BASE_sections'], 'external_trust': c['external_trust']})
    write('acceptance.json', {
        'audit_id': 'N45-HIGH23-SUPERVISION', 'BASE': intake['BASE'], 'authority': 'parent scoped adoption',
        'HIGH2': {'adopted': True, 'full_H1_H13': h2r['full_contract'], 'claims': claims,
                  'raw_all_twelve_PASS': False,
                  'raw_finding_ids': ['H2A-QDOMAIN-01', 'H2R-EXCLUSION-FOUR-COLOR-UNUSED'],
                  'parent_finding': 'parent-quantifier-finding.json',
                  'qualification_changes_source_domain': False,
                  'all_proper_gamma_retained': ['JOIN', 'RESTORE', 'F', 'PALETTE'],
                  'four_color_acceptance': 'original H2 full Sigma includes every T4 row; no unused-color construction asserted there'},
        'HIGH3': {'adopted': True, 'full_K1_K13_text': kblock,
                  'full_contract_file': contract_path, 'full_contract_sha256': sha((HERE/contract_path).read_bytes()),
                  'all_twenty_one_independent_claims_adopted_under_full_contract': True,
                  'independent_audits': ['H3A', 'H3R', 'H3G'], 'parent_proof': 'parent-high3-review.json',
                  'source_route': 'X own beta-minimal, unique s degree5, no spokes, complete C/U contacts(2,3), same-beta private full cover, |FU|>=2; BASE no-spoke exterior §§1-3,5 excludes (3,2) using original X K5',
                  'new_source_hypotheses': []},
        'coverage': {'adopted': True,
                     'exact_domain': 'canonical §1 S identity X=G-e=M, both original mixed short, all shared source hypotheses and full same-source data retained',
                     'accepted_reductions': ['S05', 'S06'],
                     'LOW': [{'u': 1, 'r_spokes': 2, 'case': 'LOW1'}, {'u': 2, 'r_spokes': 1, 'case': 'LOW2'}],
                     'HIGH': [{'u': 1, 's_spokes': 2, 'case': 'HIGH1'}, {'u': 2, 's_spokes': 1, 'case': 'HIGH2'}, {'u': 3, 's_spokes': 0, 'case': 'HIGH3'}],
                     'identity_proof': 'LOW u+t_r=3, t_r>=1 because original omitted e exists; HIGH u+t_s=3,u>=1,t_s>=0; non-unary root mixed3 implies two original spokes. All case-specific complete contracts mapped, never inherited X minimality.',
                     'independent_check': 'H2A REPORT §6 full HIGH coverage; parent original LOW1/LOW2 adoption and canonical S05/S06 plus parent-coverage.json',
                     'conclusion': 'exclude only this exact both-original-mixed-short S identity'},
        'artifact_acceptance': {'H2C': 'only named artifact/receipt/finite-tool observations, not its twelve unadjudicated paper claims',
                                'historical_stdin_helpers': 'three helpers have no retained program bytes/hash; no byte-exact replay claim',
                                'new_finite_source': False, 'source_trigger_count': None, 'new_Lean': False},
        'external_trust': {'url': 'https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf',
                           'theorems': ['Lemma 7', 'Theorem 10'],
                           'frozen_pdf_sha256': '50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea',
                           'BASE_paper_remains_external_to_Lean': True},
        'remaining_OPEN': ['S with at least one original long mixed', 'other 45/54 omission/core identities', 'original55', 'sources with no45/54 core', 'general N2/E', 'epsilon>=3', 'Lean formalization'],
        'publication': 'five current shared docs plus dated history; stop L2; no commit/push/PR',
        'preserved_FAIL': ['whole DocGraph 62 duplicate-ID errors', 'concurrent-addition outside custody exit1', 'historical missing BASE paths', 'E4 provenance FAIL', 'original failed generations/link checks'],
    })
    paths = list(intake['shared_before'])
    for path in paths:
        baseline = (HERE/'shared-before'/path).read_bytes()
        assert (ROOT/path).read_bytes() == baseline, path
    # The parent, guide/status, then direct consumers follow the recorded L0-L2 plan.
    paths = ['docs/c5_excess_two_nonadjacent_unit_core45.md', 'docs/c5_kempe_guide.md',
             'docs/STATUS.md', 'docs/c5_phase_b_common_lemmas.md', 'artifacts/c5_excess_two_e4/REPORT.md']
    diffs = []
    after = {}
    for path in paths:
        before = (HERE/'shared-before'/path).read_text()
        next_text = (HERE/'draft'/path).read_text()
        (ROOT/path).write_text(next_text)
        diffs.extend(difflib.unified_diff(before.splitlines(keepends=True), next_text.splitlines(keepends=True), fromfile='before/'+path, tofile='after/'+path))
        after[path] = {'sha256': sha((ROOT/path).read_bytes()), 'bytes': len((ROOT/path).read_bytes())}
    (HERE/'documentation.diff').write_text(''.join(diffs))
    history = ROOT/'docs/history/2026-10-10-n45-high23-adoption.md'
    with history.open('x') as f:
        f.write((HERE/'history-draft.md').read_text())
    after[history.relative_to(ROOT).as_posix()] = {'sha256': sha(history.read_bytes()), 'bytes': len(history.read_bytes())}
    unchanged = {path: {'sha256': sha((ROOT/path).read_bytes())} for path in ['README.md', 'docs/HANDOFF.md']}
    write('documentation-state.json', {'BASE': intake['BASE'], 'after': after,
                                      'reviewed_unchanged': unchanged, 'shared_before': intake['shared_before'],
                                      'propagation': 'L0 source -> L1 guide/status -> L2 direct consumers; stop L2',
                                      'old_worker_trees_refreshed': False})
    write('documentation-checks.json', {'status': 'pending actual checks; replaced by recorded executions before seal'})
    print(json.dumps({'accepted': ['HIGH2 with explicit three-color construction qualification', 'HIGH3 under complete K1-K13', 'exact S both-short five-case composition'], 'current_shared_changed': len(paths), 'history_added': 1}, ensure_ascii=False))


if __name__ == '__main__':
    main()
