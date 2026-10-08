#!/usr/bin/env python3
"""Recheck accepted source hashes and the preserved sidecar after publication."""
import hashlib
import json
from pathlib import Path
import subprocess

folder = Path(__file__).resolve().parent
repo = Path('/home/ray/developer/ai/math')
FINAL = '1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf'
def load(path):
    return json.loads(path.read_bytes())
def metadata(path):
    raw = path.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def git(*args):
    return subprocess.check_output(['git','-C',str(repo),*args]).decode().strip()
assert git('rev-parse','HEAD') == FINAL
assert not git('status','--porcelain','--untracked-files=no')
assert subprocess.run(['git','-C',str(repo),'diff','--cached','--quiet']).returncode == 0
manifest = repo/'audits/2026-10-07-m4-local/DELIVERY.json'
delivery = load(manifest)
for entry in delivery['files']:
    assert metadata(repo/entry['path']) == {key:entry[key] for key in ('bytes','sha256')},entry['path']
seal = metadata(manifest)
assert seal == {'bytes':118904,'sha256':'0ee59a603a366808cc8fdfb52b32586403028fd72395a80785991584408d49fa'}
original = load(repo/'audits/2026-10-07-m4-local/original-bundles.json')['files']
for entry in original:
    assert metadata(repo/entry['path']) == {key:entry[key] for key in ('bytes','sha256')},entry['path']
source = load(repo/'audits/2026-10-07-m4-supervisor/acceptance/final-receipt/review/source-comparison.json')
lean = source['lean_source_config_generated_products']
for entry in lean:
    assert metadata(repo/entry['path']) == entry['tested'] == entry['m3'],entry['path']
before = load(folder/'commands/supervisor-snapshot/stdout.log')
after = [{'path':str(p.relative_to(repo)),**metadata(p)} for p in sorted((repo/'audits/2026-10-07-m4-supervisor').rglob('*'))
         if p.is_file() and '__pycache__' not in p.parts]
assert before == after,'supervisor sidecar changed'
assert (repo/'scratch').is_dir()
result = {'status':'PASS','head':FINAL,'tree':git('rev-parse','HEAD^{tree}'),
          'delivery_entries_without_seal':len(delivery['files']),'seal':seal,
          'original_bundle_files_unchanged':len(original),'lean_source_config_products_unchanged':len(lean),
          'supervisor_sidecar_files_unchanged':len(after),'scratch_retained':True,
          'tracked_and_staging_clean':True,'new_commit':False,'full_source_preflight':'integrity/source-integrity.json'}
(folder/'final-integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
