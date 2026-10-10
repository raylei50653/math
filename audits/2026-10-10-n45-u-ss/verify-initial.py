#!/usr/bin/env python3
"""Read-only delivery/input verifier. This does not verify the paper theorem."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
BASE='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
EXCLUDED={'MANIFEST.sha256','delivery.json'}
def sha(data):return hashlib.sha256(data).hexdigest()
def git(args):
    p=subprocess.run(['git',*args],cwd=ROOT,capture_output=True)
    if p.returncode:raise RuntimeError(f'git command failed: {args!r}, exit {p.returncode}')
    return p.stdout

def main():
    head=git(['rev-parse','HEAD']).decode().strip()
    assert head==BASE, 'HEAD drifted from BASE'
    inputs=json.loads((OUT/'inputs.json').read_text())
    records=inputs['inputs']+json.loads((OUT/'inputs-additional.json').read_text())
    current=0;base=0;missing=[]
    for r in records:
        if 'frozen' not in r:
            missing.append(r['path']);continue
        data=(OUT/r['frozen']).read_bytes()
        assert sha(data)==r['sha256'],f'frozen drift: {r["frozen"]}'
        if 'expected_sha256' in r:
            assert r['sha256']==r['expected_sha256'] and r['pin_match'], 'pin mismatch'
        if r['layer']=='BASE-git-blob':
            assert git(['show',BASE+':'+r['path']])==data, f'BASE blob mismatch: {r["path"]}'
            assert git(['rev-parse',BASE+':'+r['path']]).decode().strip()==r['git_blob']
            assert (OUT/'base-source'/r['path']).read_bytes()==data, 'BASE archive mismatch'
            base+=1
        else:
            assert (ROOT/r['path']).read_bytes()==data, f'original input drift: {r["path"]}'
            current+=1
    shared=json.loads((OUT/'shared-before.json').read_text())
    for rel,digest in shared.items():
        assert (ROOT/rel).is_file() and sha((ROOT/rel).read_bytes())==digest, f'shared drift: {rel}'
    for cmd,name in [(['diff','--binary'],'initial-diff'),(['diff','--cached','--binary'],'initial-cached-diff')]:
        assert git(cmd)==(OUT/f'logs/{name}.stdout.log').read_bytes(), 'tracked diff changed'
    initial=git(['ls-files','--cached','--others','--exclude-standard','-z']).split(b'\0')
    outside=set()
    for raw in initial:
        if not raw:continue
        rel=raw.decode();p=ROOT/rel
        if p.is_file() and not p.is_relative_to(OUT):outside.add(rel)
    assert outside==set(shared), 'shared file inventory changed outside own output'
    claims=json.loads((OUT/'claims.json').read_text())
    all_ids={c['id'] for c in claims['claims']}
    expected={'N45-SS-COST','N45-SS-UNTOP','N45-SS-U3','N45-SS-U2','N45-SS-X-CORE','N45-SS-COMPONENT',
              'N45-SS-SPOKES','N45-SS-T0','N45-SS-T1','N45-SS-T2','N45-SS-EXCLUSION'}
    assert all_ids==expected and len(claims['claims'])==len(expected),'claim inventory mismatch'
    required={'quantifier','sufficient_premises','dependencies','paper_argument','evidence_layer','coverage','uncovered','finding','status'}
    for c in claims['claims']:
        assert required<=set(c),'incomplete claim metadata'
        assert all(p in c['sufficient_premises'] for p in claims['source_contract']),'source premise missing'
        for d in c['dependencies']:
            if d.startswith('N45-SS-'):assert d in all_ids,'missing internal claim dependency'
    # Only own authored top-level text: frozen reports intentionally retain their historical relative links.
    report=(OUT/'REPORT.md').read_text()
    local_links=0
    for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',report):
        if re.match(r'^[a-z][a-z0-9+.-]*:',dest):continue
        dest=dest.split('#',1)[0]
        if not dest:continue
        assert (OUT/dest).exists(), f'own REPORT link missing: {dest}'
        local_links+=1
    authored=[]
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.suffix in {'.md','.json','.py','.txt'}:
            raw=p.read_bytes()
            assert raw.endswith(b'\n'), f'missing final newline: {p.name}'
            if p.name!='gallai-primary.txt':
                assert all(line==line.rstrip() for line in raw.splitlines()),f'trailing whitespace: {p.name}'
            if p.suffix=='.json':json.loads(raw)
            if p.suffix=='.py':compile(raw,str(p),'exec')
            authored.append(p.name)
    manifest_checked=False;manifest_count=0
    if (OUT/'MANIFEST.sha256').exists():
        entries={}
        for line in (OUT/'MANIFEST.sha256').read_text().splitlines():
            digest,rel=line.split('  ',1)
            assert rel not in entries and re.fullmatch(r'[0-9a-f]{64}',digest)
            entries[rel]=digest
        actual={str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file() and str(p.relative_to(OUT)) not in EXCLUDED}
        assert actual==set(entries),'sealed manifest inventory mismatch'
        for rel,digest in entries.items():assert sha((OUT/rel).read_bytes())==digest,f'manifest mismatch: {rel}'
        delivery=json.loads((OUT/'delivery.json').read_text())
        assert delivery['manifest_sha256']==sha((OUT/'MANIFEST.sha256').read_bytes()),'delivery manifest hash mismatch'
        assert delivery['payload_file_count']==len(entries),'delivery count mismatch'
        manifest_checked=True;manifest_count=len(entries)
    print(json.dumps({'task':'N45-U-SS','scope':'Input/Git/artifact checks only; no mathematical theorem or finite source solver',
          'head':head,'current_snapshots_verified':current,'base_blobs_verified':base,'probe_missing_not_dependencies':missing,
          'shared_existing_files_unchanged':len(shared),'shared_file_inventory_unchanged':True,
          'claims_with_required_metadata':len(all_ids),'own_report_local_links':local_links,'authored_top_level_text_checked':authored,
          'sealed_manifest_checked':manifest_checked,'sealed_payload_file_count':manifest_count},indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print(str(e),file=sys.stderr)
        raise SystemExit(1)
