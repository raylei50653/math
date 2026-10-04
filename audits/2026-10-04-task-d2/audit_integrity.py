#!/usr/bin/env python3
"""Compare D2 baseline bytes and declared hashes without refreshing artifacts."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import subprocess


def digest(path):
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            hasher.update(block)
    return hasher.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root, snapshot, out = args.repo.resolve(), args.snapshot.resolve(), args.output.resolve()
    baseline = json.loads((out/'baseline.json').read_text())
    successor_path=out/'successor_baseline_final.json'
    if not successor_path.exists(): successor_path=out/'successor_baseline.json'
    successor = json.loads(successor_path.read_text()) if successor_path.exists() else {'new_files': {}}
    changes = []
    current_digests = {}
    for rel, previous in baseline['files'].items():
        path = root/rel
        current = digest(path) if path.is_file() else None
        current_digests[rel] = current
        if current != previous['sha256']:
            changes.append(dict(path=rel, before_sha256=previous['sha256'], after_sha256=current))
    protected = [rel for rel in baseline['files'] if rel != 'artifacts/MANIFEST.json' and rel.startswith(('artifacts/', 'scripts/', 'tools/', 'docs/history/', 'audits/2026-10-04-task-d/'))]
    protected_changes = [r for r in changes if r['path'] in protected]
    successor_changes = []
    for rel, previous in successor['new_files'].items():
        # New report prose may gain its author's validation; freeze mathematical inputs.
        if not rel.startswith(('artifacts/', 'scripts/')):
            continue
        current=digest(root/rel) if (root/rel).is_file() else None
        if current != previous['sha256']:
            successor_changes.append(dict(path=rel,before_sha256=previous['sha256'],after_sha256=current))
    old_manifest=json.loads((snapshot/'artifacts/MANIFEST.json').read_text())
    current_manifest=json.loads((root/'artifacts/MANIFEST.json').read_text())
    manifest_changed_existing_files=[p for p,v in old_manifest['files'].items() if current_manifest['files'].get(p)!=v]
    manifest_added_files=sorted(set(current_manifest['files'])-set(old_manifest['files']))
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    integrity = dict(head_before=baseline['head'], head_after=head,
                     head_unchanged=head==baseline['head'], baseline_file_count=len(baseline['files']),
                     protected_file_count=len(protected), protected_changes=protected_changes,
                     all_original_artifact_bytes_preserved=not any(r['path'].startswith('artifacts/') and r['path']!='artifacts/MANIFEST.json' for r in changes),
                     old_d_audit_bytes_preserved=not any(r['path'].startswith('audits/2026-10-04-task-d/') for r in changes),
                     successor_mathematical_input_changes=successor_changes,
                     manifest_changed_existing_files=manifest_changed_existing_files,
                     manifest_added_files=manifest_added_files,
                     changed_baseline_files=changes)
    (out/'integrity_results.json').write_text(json.dumps(integrity, indent=2, ensure_ascii=False)+'\n')
    patch = []
    for change in changes:
        rel=change['path']
        if rel.endswith('.md') and (snapshot/rel).exists():
            patch.extend(difflib.unified_diff((snapshot/rel).read_text().splitlines(True),
                         (root/rel).read_text().splitlines(True), fromfile='before-d2/'+rel, tofile='after-d2/'+rel))
    (out/'integration_doc_changes.diff').write_text(''.join(patch))
    d_baseline=json.loads((root/'audits/2026-10-04-task-d/baseline.json').read_text())
    document_changes=[]
    for rel, previous in baseline['files'].items():
        if not rel.endswith('.md') or not (rel.startswith('docs/') or rel=='README.md'):
            continue
        cutoff=d_baseline['files'].get(rel,{}).get('sha256')
        current=current_digests[rel]
        if current!=previous['sha256'] or (cutoff is not None and current!=cutoff):
            document_changes.append(dict(path=rel,d_cutoff_sha256=cutoff,
                d2_before_sha256=previous['sha256'],d2_after_sha256=current,
                present_at_d_cutoff=cutoff is not None,
                changed_since_d_cutoff=cutoff is not None and current!=cutoff,
                changed_during_d2=current!=previous['sha256']))
    document_result=dict(scope='Existing README/docs Markdown bytes at the D cutoff and D2 initial baseline; separate from declared certificate hashes',
        document_changes=document_changes,changed_during_d2_count=sum(r['changed_during_d2'] for r in document_changes),
        changed_d_existing_documents_count=sum(r['changed_since_d_cutoff'] for r in document_changes))
    (out/'document_hash_changes.json').write_text(json.dumps(document_result,indent=2,ensure_ascii=False)+'\n')
    old=json.loads((root/'audits/2026-10-04-task-d/input_hash_audit.json').read_text())
    records=[]
    for cert in old:
        for entry in cert['inputs']:
            rel=entry['path']; current=digest(root/rel) if (root/rel).is_file() else None
            records.append(dict(artifact=cert['artifact'], path=rel,
                recorded_sha256=entry['recorded_sha256'], d_cutoff_sha256=entry['current_sha256'],
                d2_before_sha256=baseline['files'].get(rel,{}).get('sha256'), d2_after_sha256=current,
                differs_from_recorded=current!=entry['recorded_sha256'],
                changed_since_d_cutoff=current!=entry['current_sha256'],
                changed_during_d2=current!=baseline['files'].get(rel,{}).get('sha256'),
                classification=entry['classification']))
    new_names=('c5_excess_two_mixed_core_four_spoke_mixed12',
                 'c5_excess_two_mixed_core_four_spoke_mixed22', 'c5_mixed_p3_common_endpoint',
                 'c5_excess_two_mixed_core_four_spoke_mixed12_01_12',
                 'c5_excess_two_mixed_core_four_spoke_mixed22_short_face', 'c5_mixed_p3_one_color_ternary_unary')
    for name in new_names:
        rel_artifact='artifacts/'+name+'/observations.json'
        data=json.loads((root/rel_artifact).read_text())
        hashes={}
        for key in ('input_sha256','inputs_sha256','source_sha256'):
            if isinstance(data.get(key),dict): hashes.update(data[key])
        for rel, recorded in hashes.items():
            current=digest(root/rel) if (root/rel).is_file() else None
            records.append(dict(artifact=rel_artifact,path=rel,recorded_sha256=recorded,
                d2_before_sha256=baseline['files'].get(rel,successor['new_files'].get(rel,{})).get('sha256'),d2_after_sha256=current,
                differs_from_recorded=current!=recorded,
                new_path_since_initial_snapshot=rel not in baseline['files'],
                changed_during_d2=current!=baseline['files'].get(rel,successor['new_files'].get(rel,{})).get('sha256'),
                classification='document_provenance' if rel.startswith('docs/') else 'non_document_input'))
    drift=[r for r in records if r['differs_from_recorded']]
    hash_result=dict(scope='Original D 22 certificates plus A/B/C and A2/B2/C2 direct hash maps; not all repository certificates',
        certificate_count=len(old)+len(new_names),declared_hash_count=len(records),
        recorded_hash_drift_count=len(drift),non_document_drift_count=sum(r['classification']!='document_provenance' for r in drift),
        newly_drifted_d_hashes_since_cutoff=sum(r.get('changed_since_d_cutoff',False) and r['differs_from_recorded'] for r in records),
        input_hash_changes_during_d2=sum(r['changed_during_d2'] for r in records),
        records=records,drift=drift)
    (out/'input_hash_audit.json').write_text(json.dumps(hash_result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in integrity.items() if k!='changed_baseline_files'},ensure_ascii=False))
    print(json.dumps({k:v for k,v in hash_result.items() if k not in ('records','drift')},ensure_ascii=False))
    assert not protected_changes and not successor_changes and not manifest_changed_existing_files and integrity['head_unchanged']
    assert hash_result['non_document_drift_count']==0


if __name__ == '__main__':
    main()
