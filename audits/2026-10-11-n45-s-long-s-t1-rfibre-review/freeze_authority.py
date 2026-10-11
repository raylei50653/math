#!/usr/bin/env python3
"""Freeze the directly inspected N-diagonal BASE proof and pinned Gallai PDF."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'


def main():
    requested = json.loads((HERE / 'extra-authority-pins.json').read_bytes())
    # The independently inspected E4 proof is the only extra BASE dependency.
    name = 'artifacts/c5_excess_two_e4/REPORT.md'
    raw = subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=REPO)
    blob = subprocess.check_output(['git', 'rev-parse', BASE + ':' + name], cwd=REPO, text=True).strip()
    assert raw == (REPO / name).read_bytes()
    path = HERE / 'authority' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)
    result = [{'path': name, 'frozen_path': str(path.relative_to(HERE)), 'authority': 'BASE Git blob',
               'base': BASE, 'git_blob': blob, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
               'used_scope': 'E4 original short-support N-diagonal sufficient premises, lines225-245'}]
    external = 'audits/2026-10-11-n45-s-long-s-fibre/external/gallai.pdf'
    pdf = (REPO / external).read_bytes()
    assert len(pdf) == 164927 and hashlib.sha256(pdf).hexdigest() == '50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea'
    path = HERE / 'authority/external/gallai.pdf'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(pdf)
    result.append({'path': external, 'frozen_path': str(path.relative_to(HERE)), 'authority': 'external pinned primary PDF',
                   'base': None, 'git_blob': None, 'bytes': len(pdf), 'sha256': hashlib.sha256(pdf).hexdigest(),
                   'origin_refetched': False, 'pinned_pages_inspected': [5, 6],
                   'used_theorems': ['Lemma7', 'Theorem10'], 'new_Lean_theorem': False})
    with (HERE / 'extra-authority-inputs.json').open('x') as stream:
        stream.write(json.dumps({'base': BASE, 'inputs': result, 'requested_independent_pins': requested},
                               ensure_ascii=False, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'extra_BASE_proof_frozen': 1, 'pinned_primary_PDF_frozen': 1}))


if __name__ == '__main__':
    main()
