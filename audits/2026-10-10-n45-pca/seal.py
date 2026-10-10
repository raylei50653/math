#!/usr/bin/env python3
"""Exclusive-create the exact relative payload manifest and delivery record."""
from hashlib import sha256
import json
from pathlib import Path
import re
import stat
import subprocess

HOME=Path(__file__).resolve().parent
ROOT=HOME.parent.parent
EXCLUDE={'MANIFEST.sha256','delivery.json'}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path,value):
    with path.open('xb') as f:
        f.write((json.dumps(value,sort_keys=True,indent=2)+'\n').encode())


def payload():
    return sorted(p for p in HOME.rglob('*') if stat.S_ISREG(p.lstat().st_mode) and str(p.relative_to(HOME)) not in EXCLUDE)


def main():
    assert not (HOME/'MANIFEST.sha256').exists() and not (HOME/'delivery.json').exists(),'already sealed'
    inputs=json.loads((HOME/'inputs.json').read_text())
    for item in inputs['authority_files']:
        assert digest(HOME/item['frozen'])==item['sha256'],item['frozen']
    judgment=json.loads((HOME/'independent-judgment.json').read_text())
    assert digest(HOME/'independent-certificate.json')==judgment['finite_evidence_sha256']
    checks=json.loads((HOME/'checks.json').read_text())
    assert checks['all_expected_exits'] and len(checks['commands'])==20
    authored=[*HOME.glob('*.py'),HOME/'REPORT.md',HOME/'independent-judgment.json',HOME/'checks.json']
    whitespace=[]
    for path in authored:
        for i,line in enumerate(path.read_text().splitlines(),1):
            if line.rstrip()!=line:
                whitespace.append((str(path.relative_to(HOME)),i))
    assert not whitespace,whitespace
    links=re.findall(r'\[[^\]]+\]\(([^)]+)\)',(HOME/'REPORT.md').read_text())
    missing=[t for t in links if t not in EXCLUDE and not (HOME/t.split('#')[0]).exists()]
    assert not missing,missing
    validation={'frozen_input_hashes':len(inputs['authority_files']),'frozen_input_hash_status':'holds',
                'authored_whitespace_errors':whitespace,'report_local_links_checked':len(links),'missing_report_local_links':missing,
                'independent_certificate_sha256':digest(HOME/'independent-certificate.json'),'checks_command_count':20,
                'checks_expected_exits':'holds','scope':'Integrity/authoring checks only; no additional mathematical or generic validator claim.'}
    write(HOME/'checks/seal-validation.json',validation)
    files=payload()
    data=''.join(digest(p)+'  '+str(p.relative_to(HOME))+'\n' for p in files).encode()
    with (HOME/'MANIFEST.sha256').open('xb') as f:
        f.write(data)
    delivery={'task':'N45-PCA','BASE':inputs['BASE'],'decision':judgment['decision'],'write_scope':str(HOME.relative_to(ROOT)),
              'manifest_sha256':digest(HOME/'MANIFEST.sha256'),'judgment_sha256':digest(HOME/'independent-judgment.json'),
              'report_sha256':digest(HOME/'REPORT.md'),'independent_certificate_sha256':digest(HOME/'independent-certificate.json'),
              'inventory_files':len(files),'inventory_bytes':sum(p.stat().st_size for p in files),
              'manifest_exclusions':{'MANIFEST.sha256':'Root manifest self-reference; its digest is recorded in delivery.json',
                                     'delivery.json':'Root delivery contains manifest digest; excluded to avoid circular hashing'},
              'all_regular_payload_coverage':'exact','general_validator_soundness':'not established','source_exclusion':'not established',
              'paper_Lean':'no new claim','blocking_findings':judgment['blocking_findings'],
              'completed_command':{'argv':['python3','-B','audits/2026-10-10-n45-pca/seal.py'],'exit':0,'scope':'This delivery plus exact manifest; integrity-only'},
              'current_HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
              'current_shared_status':subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True),
              'worker_modification_commit_push_external_messages_subagents':'none'}
    write(HOME/'delivery.json',delivery)
    print(json.dumps({k:delivery[k] for k in ['manifest_sha256','judgment_sha256','report_sha256','independent_certificate_sha256','inventory_files','inventory_bytes']},sort_keys=True))


if __name__=='__main__':
    main()
