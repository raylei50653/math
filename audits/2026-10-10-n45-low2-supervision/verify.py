#!/usr/bin/env python3
"""Read-only independent custody and adoption-scope checks, not a theorem prover."""
import argparse,json,sys
from pathlib import Path
from review import BASE,OUT,ROOT,WORKER,check_manifest,file_state,git,sha,tree,worker
SEAL_FILES={'seal-checks/payload-before.json','seal-checks/payload-after.json',
            'seal-checks/commands.json','seal-checks/corrupted-manifest.sha256',
            *{f'seal-checks/{name}.{stream}.log' for name in ['normal','seed17','corrupted']
               for stream in ['stdout','stderr']}}
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
        require(not any(f.is_symlink() for f in OUT.rglob('*')),'root symlinks unexpected')
        actual={str(f.relative_to(OUT)) for f in OUT.rglob('*') if f.is_file()
                and str(f.relative_to(OUT)) not in {'MANIFEST.sha256','delivery.json'}|SEAL_FILES}
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
        require(accepted['decision']=='accepted_LOW2_and_scoped_LOW_composition','unexpected adoption decision')
        require(accepted['full_source_contract']==claims['full_source_contract'],'source contract drift')
        require(accepted['accepted_claim_ids']==[c['id'] for c in claims['claims']],'claim coverage differs')
        require(accepted['finite_source_controls']=='not performed; no LOW2 trigger count','source layer drift')
        require(accepted['new_Lean'] is False and accepted['general_N2_E']=='OPEN','scope overclaim')
        require(accepted['LOW_composition']['decision']=='accepted_authority_section1_S_SHORT_U_LOW_only','composition scope differs')
        require(set(adoption['changed_existing'])==set(accepted['adopted_shared_sha256']) and len(adoption['changed_existing'])==5,'shared adoption inventory differs')
        require(set(adoption['new_shared'])=={'docs/history/2026-10-10-n45-low2-adoption.md'},'new shared scope differs')
        for rel,digest in accepted['adopted_shared_sha256'].items():
            require(sha((ROOT/rel).read_bytes())==digest,'adopted shared digest differs: '+rel)
        a=json.loads((ROOT/'audits/2026-10-10-n45-l2a/independent-judgment.json').read_text())
        require(accepted['LOW_composition']['independent_verdict']==a['composition'],'independent composition verdict differs')
        pins=read('high1-task-pins.json')
        require(pins['status']=='prepared; not launched' and len(pins['pins'])==9,'HIGH1 task scope differs')
        history=(ROOT/'docs/history/2026-10-10-n45-low2-adoption.md').read_text()
        for pin in pins['pins']:
            require(sha((ROOT/pin['path']).read_bytes())==pin['sha256'],'HIGH1 pin differs: '+pin['path'])
            require(pin['path']+'\n  SHA256 '+pin['sha256'] in history,'HIGH1 history pin differs: '+pin['path'])
        initial=read('initial-strict-replays.json')['records']
        require(initial['normal']['exit_code']==initial['seed17']['exit_code']==0,'initial strict exit differs')
        require(initial['normal']['output']==initial['seed17']['output'],'initial strict outputs differ')
        require(initial['corrupted']['exit_code']==2 and 'manifest digest differs' in initial['corrupted']['output'],'initial negative stage differs')
        require(initial['bad_receipt']['exit_code']==2 and 'delivery receipt binding differs' in initial['bad_receipt']['output'],'initial receipt negative differs')
        checks=read('checks.json')['commands']
        for c in checks:require(c['exit_code']==c['expected_exit'],'logged command unexpected exit: '+c['label'])
        if not args.payload_only:
            d=read('delivery.json')
            require(d['manifest_sha256']==sha((OUT/'MANIFEST.sha256').read_bytes()),'root manifest receipt differs')
            names={str(f.relative_to(OUT)) for f in (OUT/'seal-checks').rglob('*') if f.is_file()}
            require(names==set(d['seal_files'])==SEAL_FILES,'root receipt metadata inventory differs')
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
                          'paper_proved_by_tool':False,'finite_LOW2_source_controls':'not performed'},sort_keys=True))
    except (OSError,ValueError,KeyError,AssertionError) as error:
        print('integrity rejection: '+str(error),file=sys.stderr);raise SystemExit(2)
if __name__=='__main__':main()
