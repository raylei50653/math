#!/usr/bin/env python3
"""Read-only sealed supervision replay. Verifies evidence bytes, not mathematics."""
import json
import review as r

def main():
    assert r.git('rev-parse', 'HEAD').decode().strip() == r.BASE
    before = json.loads((r.OUT/'inputs-before.json').read_text())
    assert r.tree(r.WORKER) == before['worker'], 'worker bytes/mtime/symlinks changed'
    incoming = json.loads((r.OUT/'incoming-audits.json').read_text())
    for rel, item in incoming.items():
        assert r.tree(r.ROOT/rel) == item['state'], 'independent audit drift: '+rel
    after = json.loads((r.OUT/'shared-after.json').read_text())
    for rel, digest in after.items():
        assert r.sha((r.ROOT/rel).read_bytes()) == digest, 'shared adoption drift: '+rel
    for rel, item in before['existing'].items():
        if rel in after: continue
        assert r.file_state(r.ROOT/rel) == item, 'pre-existing file drift: '+rel
    delivery = json.loads((r.OUT/'delivery.json').read_text())
    n = r.manifest(r.OUT, lambda rel: rel in {'MANIFEST.sha256', 'delivery.json'})
    assert n == delivery['payload_files']
    assert r.sha((r.OUT/'MANIFEST.sha256').read_bytes()) == delivery['manifest_sha256']
    for name, digest in delivery['pinned_outputs'].items():
        assert r.sha((r.ROOT/name).read_bytes()) == digest, name
    print(json.dumps({'task': 'N45-SS-supervision', 'integrity_only': True, 'payload_files': n,
                      'worker_tree_entries': len(before['worker']), 'independent_audits': len(incoming),
                      'existing_files_preserved_except_recorded_adoption': len(before['existing'])-len(after),
                      'LP_and_SS_paper_status': delivery['mathematical_status'],
                      'general_N2_E': 'OPEN', 'next_task_started': False}, sort_keys=True))

if __name__ == '__main__': main()
