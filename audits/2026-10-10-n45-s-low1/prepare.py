#!/usr/bin/env python3
"""Freeze this delivery's inputs; every output is exclusive-created here."""
from pathlib import Path
import hashlib
import io
import json
import os
import subprocess
import tarfile
import urllib.request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
COMMANDS = []


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)


def dump(path, value):
    write(path, (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode())


def run(name, argv, cwd=ROOT):
    result = subprocess.run(argv, cwd=cwd, capture_output=True, check=False)
    write(HERE / f'logs/{name}.stdout.log', result.stdout)
    write(HERE / f'logs/{name}.stderr.log', result.stderr)
    COMMANDS.append(dict(id=name, argv=argv, cwd=str(cwd), exit_code=result.returncode,
                         stdout=f'logs/{name}.stdout.log', stderr=f'logs/{name}.stderr.log'))
    if result.returncode:
        raise RuntimeError(f'{name}: exit {result.returncode}')
    return result.stdout


def digest(path):
    if path.is_symlink():
        return dict(kind='symlink', target=os.readlink(path))
    if not path.is_file():
        return dict(kind='missing')
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            hasher.update(chunk)
    return dict(kind='file', sha256=hasher.hexdigest(), bytes=path.stat().st_size)


def main():
    inventory = run('preexisting-inventory', ['git', 'ls-files', '--cached', '--others',
                                           '--exclude-standard', '-z'])
    prefix = HERE.relative_to(ROOT).as_posix() + '/'
    paths = sorted({p.decode() for p in inventory.split(b'\0') if p and not p.decode().startswith(prefix)})
    dump(HERE / 'preexisting-files.json', {p: digest(ROOT / p) for p in paths})
    run('initial-tracked-diff', ['git', 'diff', '--binary'])
    run('initial-cached-diff', ['git', 'diff', '--cached', '--binary'])

    # A complete immutable Git archive permits fresh-BASE navigation checks.
    archive = run('base-archive', ['git', 'archive', '--format=tar', BASE])
    tree = HERE / 'base-source'
    tree.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        source.extractall(tree, filter='data')
    base_inputs = [
        'docs/c5_two_spoke_three_contacts.md', 'docs/c5_degree5_interfaces.md',
        'docs/c5_weak_list_cores.md', 'docs/c5_phase_b_common_lemmas.md',
        'docs/c5_unary_shield_budget.md', 'artifacts/c5_excess_two_e3/REPORT.md',
        'artifacts/c5_excess_two_e3/nonadjacent_notes.md',
        'artifacts/c5_excess_two_e4/REPORT.md', 'artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md',
        'scripts/c5_two_spoke_three_contacts.py',
        'artifacts/c5_two_spoke_three_contacts/observations.json',
        'audits/2026-10-04-task-d4/a3/gallai-primary-source.pdf',
    ]
    records = []
    for i, path in enumerate(base_inputs):
        blob = run(f'base-blob-{i:02}', ['git', 'show', f'{BASE}:{path}'])
        oid = run(f'base-oid-{i:02}', ['git', 'rev-parse', f'{BASE}:{path}']).decode().strip()
        if blob != (tree / path).read_bytes():
            raise RuntimeError(f'archive mismatch: {path}')
        records.append(dict(path=path, git_blob=oid, sha256=hashlib.sha256(blob).hexdigest()))
    dump(HERE / 'base-inputs.json', dict(base=BASE, inputs=records,
                                       archive_sha256=hashlib.sha256(archive).hexdigest()))

    pdf = tree / 'audits/2026-10-04-task-d4/a3/gallai-primary-source.pdf'
    run('gallai-text', ['pdftotext', '-layout', str(pdf), '-'])
    url = 'https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf'
    with urllib.request.urlopen(url, timeout=30) as response:
        official = response.read()
    write(HERE / 'external/gallai-official.pdf', official)
    dump(HERE / 'external-source-check.json', dict(
        url=url, official_sha256=hashlib.sha256(official).hexdigest(),
        base_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
        byte_equal=official == pdf.read_bytes(),
        statements_read=['Lemma 7: uncolorable connected degree assignment is tight everywhere',
                         'Theorem 10: uncolorable degree assignments are precisely Gallai trees with blockwise uniform lists'],
        trust='External paper theorem; no Python or Lean proof of the characterization'))
    routing = ['docs/c5_kempe_guide.md', 'README.md']
    for path in routing:
        write(HERE / 'frozen/routing' / path, (ROOT / path).read_bytes())
    initial = json.loads((HERE / 'inputs-initial.json').read_text())
    brief = (HERE / 'frozen/routing/docs/history/2026-10-10-n45-ss-adoption.md').read_text()
    write(HERE / 'task.md', ('# N45-S-LOW1 frozen task\n\n' + brief.split('```text\n', 1)[1].split('```', 1)[0]).encode())
    dump(HERE / 'prepare-commands.json', dict(commands=COMMANDS,
                                            preexisting_files=len(paths),
                                            pins_match=all(p['matches'] for p in initial['pins'])))
    print(json.dumps(dict(preexisting_files=len(paths), base_inputs=len(records),
                          official_pdf_matches_base=official == pdf.read_bytes()), sort_keys=True))


if __name__ == '__main__':
    main()
