import ast, gzip, hashlib, json, os, pathlib, stat, subprocess, time
repo = pathlib.Path('/home/ray/developer/ai/math')
out = pathlib.Path('/tmp/math-m4-remote-integrity')
started = time.monotonic()
command = {'argv':['python3','inline full-source/original-inventory audit'], 'cwd':str(repo), 'scope':'read-only; write fresh audit records under /tmp/math-m4-remote-integrity only'}
def meta(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576), b''): h.update(chunk)
    return {'bytes':path.stat().st_size,'sha256':h.hexdigest()}
def read(path): return json.loads(path.read_bytes())
def git(*args): return subprocess.check_output(['git','-C',str(repo),*args]).decode().strip()
head_before = git('rev-parse','HEAD')
status_before = git('status','--porcelain','--untracked-files=no')
assert head_before == '1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf'
assert not status_before
snap = json.loads(gzip.decompress((repo/'audits/2026-10-07-m3-fresh-checkout/sources-before.json.gz').read_bytes()))
receipt_dir = repo/'audits/2026-10-07-m4-supervisor/acceptance/final-receipt'
accepted_inventory = json.loads(gzip.decompress((receipt_dir/'review/tested-sources.json.gz').read_bytes()))
accepted_by_path = {e['path']:e for e in accepted_inventory}
assert len(accepted_by_path) == len(accepted_inventory)
all_records, changes, modes, symlinks = [], [], [], []
for rel, old in sorted(snap['entries'].items()):
    path = repo / rel
    if old['kind'] == 'symlink':
        assert path.is_symlink() and os.readlink(path) == old['target'],rel
        symlinks.append({'path':rel,'target':old['target'],'same_as_m3':True})
        continue
    current = meta(path)
    expected = {k:old[k] for k in ['bytes','sha256']}
    assert accepted_by_path[rel]['m3'] == expected,rel
    assert accepted_by_path[rel]['tested'] == current,rel
    entry = {'path':rel,'m3':expected,'current':current,'same_as_m3':expected==current,'same_as_accepted_final':True}
    all_records.append(entry)
    if expected != current: changes.append(entry)
    mode = oct(stat.S_IMODE(path.stat().st_mode))
    if mode != old['mode']: modes.append({'path':rel,'m3':old['mode'],'current':mode,'byte_equal':expected==current})
assert set(accepted_by_path) == {e['path'] for e in all_records}
assert {e['path'] for e in changes} == {'docs/STATUS.md','docs/c5_kempe_guide.md'}
lean = [e for e in all_records if e['path'].startswith('Math/') or e['path'] in {'Math.lean','lakefile.toml','lake-manifest.json','lean-toolchain','scripts/export_excess_two_certificates.py'}]
assert len(lean)==109 and all(e['same_as_m3'] for e in lean)
raw = (json.dumps({'file_records':all_records,'symlinks':symlinks},indent=2,sort_keys=True)+'\n').encode()
compressed = gzip.compress(raw,mtime=0)
(out/'full-source-current.json.gz').write_bytes(compressed)
assert gzip.decompress(compressed)==raw
original = read(repo/'audits/2026-10-07-m4-local/original-bundles.json')['files']
orig_by_path = {e['path']:e for e in original}
assert len(original)==len(orig_by_path)==328
original_groups=[]
actual_union=set()
for rel, name, count in [('audits/2026-10-07-m2-u1-audit','DELIVERY.json',40),('audits/2026-10-07-m3-fresh-checkout','BUNDLE_INVENTORY.json',264),('audits/2026-10-07-merge-supervision','SUPERVISION_INVENTORY.json',21)]:
    folder=repo/rel
    inventory=read(folder/name)['files']
    if isinstance(inventory,dict): inventory=[{'path':p,**v} for p,v in inventory.items()]
    assert len(inventory)==count
    expected={e['path'] for e in inventory}|{name}
    actual={p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    assert actual==expected,(rel,'file set drift')
    for e in inventory: assert meta(folder/e['path'])=={k:e[k] for k in ['bytes','sha256']},e['path']
    for p in actual:
        full_rel=rel+'/'+p
        actual_union.add(full_rel)
        assert meta(repo/full_rel)=={k:orig_by_path[full_rel][k] for k in ['bytes','sha256']},full_rel
    original_groups.append({'path':rel,'entries_without_manifest':count,'files_including_manifest':len(actual),'bytes_without_manifest':sum(e['bytes'] for e in inventory),'manifest':meta(folder/name),'exact_file_set':True,'zero_byte_drift':True})
assert actual_union==set(orig_by_path)
commands=list((repo/'audits/2026-10-07-m3-fresh-checkout/commands').glob('*.json'))
logs=[]
for p in sorted(commands):
    c=read(p)
    for e in c['logs']:
        full=repo/'audits/2026-10-07-m3-fresh-checkout'/e['path']
        assert meta(full)=={k:e[k] for k in ['bytes','sha256']},str(full)
        logs.append({'command_record':p.relative_to(repo).as_posix(),'path':full.relative_to(repo).as_posix(),**meta(full)})
lean_commands={name:read(repo/'audits/2026-10-07-m3-fresh-checkout/commands'/f'{name}.json') for name in ['lean-build','lean-axioms']}
assert all(c['exit_code']==0 for c in lean_commands.values())
assert git('rev-parse','HEAD')==head_before
assert not git('status','--porcelain','--untracked-files=no')
result={'status':'PASS','exact_final_sha':head_before,'exact_final_tree':git('rev-parse','HEAD^{tree}'),'m3_snapshot_entries':len(snap['entries']),'m3_file_entries':len(all_records),'m3_symlink_entries':len(symlinks),'bytes_checked':sum(e['current']['bytes'] for e in all_records),'source_bytes_equal_to_accepted_final':True,'byte_changes_since_m3':changes,'all_other_m3_source_bytes_equal':True,'mode_changes_since_m3':modes,'lean_source_config_products_same_as_m3':109,'original_bundles':original_groups,'original_bundles_files_same_bytes':328,'m3_original_command_records':len(commands),'m3_original_logs_hash_verified':len(logs),'original_lean_commands':lean_commands,'tracked_tree_clean_before_and_after':True,'lean_build_rerun':False,'lean_axiom_process_rerun':False,'seconds':time.monotonic()-started,'full_inventory':'full-source-current.json.gz','full_inventory_gzip':meta(out/'full-source-current.json.gz')}
(out/'source-integrity.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
(out/'m3-original-log-hashes.json').write_text(json.dumps(logs,indent=2,sort_keys=True)+'\n')
command.update({'exit_code':0,'seconds':result['seconds']})
(out/'source-integrity.command.json').write_text(json.dumps(command,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'byte_changes_since_m3','mode_changes_since_m3','original_lean_commands'}},ensure_ascii=False))
print('byte_changes_since_m3='+json.dumps([e['path'] for e in changes]))
print('mode_changes_since_m3='+json.dumps(modes))
