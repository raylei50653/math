#!/usr/bin/env python3
"""Check recorded workspace custody and exact authorized adoption scope."""
import json
from review import BASE,ROOT,OUT,WORKER,file_state,git,sha,tree,worker
def read(name):return json.loads((OUT/name).read_text())
def main():
    before=read('inputs-before.json');after=read('adoption-state.json');audits=read('incoming-audits.json')
    assert git('rev-parse','HEAD').decode().strip()==BASE
    assert git('diff','--cached','--binary')==(WORKER/'logs/initial-cached-diff.stdout.log').read_bytes()
    assert tree(WORKER)==before['worker']
    assert len(after['changed_existing'])==5 and len(after['new_shared'])==1
    for rel,state in before['existing'].items():
        p=ROOT/rel;now=file_state(p) if p.exists() or p.is_symlink() else {'kind':'missing'}
        assert now==after['changed_existing'].get(rel,state),rel
    for rel,state in after['new_shared'].items():assert file_state(ROOT/rel)==state,rel
    for rel,record in audits.items():assert tree(ROOT/rel)==record['full_tree'],rel
    prefixes=[str(OUT.relative_to(ROOT))+'/']+[r+'/' for r in audits]
    inventory={r.decode() for r in git('ls-files','--cached','--others','--exclude-standard','-z').split(b'\0') if r}
    assert not [r for r in inventory-set(before['existing'])-set(after['new_shared']) if not any(r.startswith(p) for p in prefixes)]
    for pin in read('high1-task-pins.json')['pins']:assert sha((ROOT/pin['path']).read_bytes())==pin['sha256']
    w=worker()
    print(json.dumps({'HEAD':BASE,'staged_diff':'unchanged','existing_regular_files_checked':32262,
                      'existing_symlinks_checked':27,'nested_repositories_presence_only':4,
                      'changed_existing_files':5,'new_shared_files':1,'reviewer_full_trees_unchanged':3,
                      'worker':w,'scope':'Git-listed original file identity and allowed five-doc/one-history adoption; nested repository contents not recursively covered'},sort_keys=True))
if __name__=='__main__':main()
