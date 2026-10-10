#!/usr/bin/env python3
"""Read-only independent custody and adoption-scope checks, not a theorem prover."""
import argparse,json,sys
from pathlib import Path
from review import BASE,OUT,ROOT,WORKER,check_manifest,file_state,git,sha,tree,worker
def read(name):return json.loads((OUT/name).read_text())
def require(cond,message):
    if not cond:raise ValueError(message)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--payload-only',action='store_true')
    p.add_argument('--manifest',type=Path,default=OUT/'MANIFEST.sha256')
    args=p.parse_args()
    try:
        # Read any supplied manifest without importing worker or reviewer code.
        records={}
        for line in args.manifest.read_text().splitlines():
            digest,rel=line.split('  ',1)
            require(len(digest)==64 and all(c in '0123456789abcdef' for c in digest),'bad digest syntax')
            require(rel not in records and not Path(rel).is_absolute() and '..' not in Path(rel).parts,'unsafe/duplicate path')
            records[rel]=digest
        actual={str(f.relative_to(OUT)) for f in OUT.rglob('*') if f.is_file() and not f.is_symlink()
                and str(f.relative_to(OUT)) not in {'MANIFEST.sha256','delivery.json'}
                and not str(f.relative_to(OUT)).startswith('seal-checks/')}
        require(actual==set(records),'root payload inventory differs')
        for rel,digest in records.items():require(sha((OUT/rel).read_bytes())==digest,'manifest digest differs: '+rel)
        require(git('rev-parse','HEAD').decode().strip()==BASE,'HEAD changed')
        before=read('inputs-before.json');adoption=read('adoption-state.json')
        require(tree(WORKER)==before['worker'],'worker full-tree identity changed')
        require(git('diff','--cached','--binary')==(WORKER/'logs/initial-cached-diff.stdout.log').read_bytes(),'staged diff changed')
        regular=links=directories=0
        for rel,state in before['existing'].items():
            f=ROOT/rel;expected=adoption['changed_existing'].get(rel,state)
            now=file_state(f) if f.exists() or f.is_symlink() else {'kind':'missing'}
            require(now==expected,'existing-file state differs: '+rel)
            regular+=state['kind']=='file';links+=state['kind']=='symlink';directories+=state['kind']=='directory'
        for rel,state in adoption['new_shared'].items():require(file_state(ROOT/rel)==state,'new shared file differs: '+rel)
        audits=read('incoming-audits.json')
        for rel,record in audits.items():require(tree(ROOT/rel)==record['full_tree'],'reviewer full-tree identity differs: '+rel)
        now_inventory={raw.decode() for raw in git('ls-files','--cached','--others','--exclude-standard','-z').split(b'\0') if raw}
        prefixes=[str(OUT.relative_to(ROOT))+'/']+[r+'/' for r in audits]
        unexpected=[r for r in now_inventory-set(before['existing'])-set(adoption['new_shared']) if not any(r.startswith(prefix) for prefix in prefixes)]
        require(not unexpected,'unexpected new workspace inventory: '+str(sorted(unexpected)))
        accepted=read('acceptance.json');claims=json.loads((WORKER/'claims.json').read_text())
        require(accepted['decision']=='accepted_scoped_LOW1_only','unexpected adoption decision')
        require(accepted['full_source_contract']==claims['full_source_contract'],'source contract drift')
        require(accepted['accepted_claim_ids']==[c['id'] for c in claims['claims']],'claim coverage differs')
        require(accepted['finite_source_controls']=='not performed; no LOW1 trigger count','source layer drift')
        require(accepted['new_Lean'] is False and accepted['general_N2_E']=='OPEN','scope overclaim')
        initial=read('initial-strict-replays.json')['records']
        require(initial['normal']['exit_code']==initial['seed17']['exit_code']==0,'initial strict exit differs')
        require(initial['normal']['output']==initial['seed17']['output'],'initial strict outputs differ')
        require(initial['corrupted']['exit_code']==2 and 'manifest digest differs' in initial['corrupted']['output'],'initial negative stage differs')
        checks=read('checks.json')['commands']
        for c in checks:require(c['exit_code']==c['expected_exit'],'logged command unexpected exit: '+c['label'])
        if not args.payload_only:
            d=read('delivery.json')
            require(d['manifest_sha256']==sha((OUT/'MANIFEST.sha256').read_bytes()),'root manifest receipt differs')
            names={str(f.relative_to(OUT)) for f in (OUT/'seal-checks').rglob('*') if f.is_file()}
            require(names==set(d['seal_files']),'root receipt metadata inventory differs')
            for rel,digest in d['seal_files'].items():require(sha((OUT/rel).read_bytes())==digest,'root receipt digest differs: '+rel)
            commands=read('seal-checks/commands.json')
            require(all(c['exit_code']==c['expected_exit'] for c in commands['commands']),'root seal exit differs')
            require(commands['normal_seed17_stdout_byte_equal'] and commands['negative_digest_rejected'],'root seal replay/negative differs')
            require(read('seal-checks/payload-before.json')==read('seal-checks/payload-after.json'),'root readonly seal changed payload')
        w=worker()
        print(json.dumps({'status':'scoped_adoption_artifact_integrity_holds','root_payload_files':len(records),
                          'worker':w,'independent_audits':len(audits),'existing_regular_files_checked':regular,
                          'existing_symlinks_checked':links,'nested_repository_directories_presence_only':directories,
                          'changed_existing_files':len(adoption['changed_existing']),'new_shared_files':len(adoption['new_shared']),
                          'paper_proved_by_tool':False,'finite_LOW1_source_controls':'not performed'},sort_keys=True))
    except (OSError,ValueError,KeyError,AssertionError) as error:
        print('integrity rejection: '+str(error),file=sys.stderr);raise SystemExit(2)
if __name__=='__main__':main()
