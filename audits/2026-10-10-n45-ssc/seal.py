#!/usr/bin/env python3
"""Exclusive-create local seal after audit results and report are complete."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

OUT = Path(__file__).resolve().parent

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def write_new(path, raw):
    with path.open('xb') as stream:
        stream.write(raw)

def main():
    links = {p.relative_to(OUT).as_posix(): str(p.readlink()) for p in OUT.rglob('*') if p.is_symlink()}
    write_new(OUT / 'SYMLINKS.json', (json.dumps(links, indent=2, sort_keys=True) + '\n').encode())
    files = {p.relative_to(OUT).as_posix(): p for p in OUT.rglob('*')
             if p.is_file() and not p.is_symlink() and p.relative_to(OUT).as_posix() not in {'MANIFEST.sha256', 'delivery.json'}
             and not p.relative_to(OUT).as_posix().startswith('seal-checks/')}
    manifest = ''.join(sha(files[name]) + '  ' + name + '\n' for name in sorted(files))
    write_new(OUT / 'MANIFEST.sha256', manifest.encode())
    receipt = {'task': 'N45-SSC', 'base': 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744',
               'sealed_utc': datetime.now(timezone.utc).isoformat(), 'judgment': 'PASS_ARTIFACT_INTEGRITY_ONLY',
               'paper_adoption': 'NOT_ADJUDICATED', 'manifest': 'MANIFEST.sha256',
               'manifest_sha256': sha(OUT / 'MANIFEST.sha256'), 'payload_regular_files': len(files),
               'symlink_count': len(links), 'symlinks': 'SYMLINKS.json',
               'exclusions': ['MANIFEST.sha256', 'delivery.json', 'seal-checks/**'],
               'exclusion_reason': 'Nonrecursive seal metadata; postseal logs have their own metadata manifest.',
               'worker_manifest_sha256': sha(OUT / 'frozen/worker/MANIFEST.sha256'),
               'worker_report_sha256': sha(OUT / 'frozen/worker/REPORT.md'),
               'postseal_checks': 'seal-checks/commands.json', 'postseal_manifest': 'seal-checks/MANIFEST.sha256',
               'shared_edits': False, 'worker_edits': False, 'new_finite_source_certificate': False,
               'ss_trigger_count': None, 'new_Lean': False, 'source_realization': False,
               'general_validator_soundness': 'NOT_TESTED', 'commit_push_pr_external_messages_subagents': False}
    write_new(OUT / 'delivery.json', (json.dumps(receipt, indent=2, sort_keys=True) + '\n').encode())
    print(json.dumps(receipt, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
