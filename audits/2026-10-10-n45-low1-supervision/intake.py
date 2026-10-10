#!/usr/bin/env python3
"""Exact independent reviewer envelopes and complete immutable-tree snapshots."""
import json
from review import ROOT,OUT,BASE,check_manifest,sha,tree,put
def main():
    records={};summary={}
    for suffix in ['l1a','l1r','l1c']:
        rel='audits/2026-10-10-n45-'+suffix;p=ROOT/rel
        d=json.loads((p/'delivery.json').read_text());mf=d.get('manifest_file','MANIFEST.sha256')
        metadata=d.get('seal_files',d.get('receipt_bound_files'))
        assert isinstance(metadata,dict) and metadata
        assert not any(f.is_symlink() for f in p.rglob('*'))
        count=check_manifest(p,mf,lambda r:r in {mf,'delivery.json'} or r in metadata)
        assert sha((p/mf).read_bytes())==d['manifest_sha256']
        for name,digest in metadata.items():assert sha((p/name).read_bytes())==digest,name
        full=tree(p);assert len(full)==count+2+len(metadata)
        for key in ['payload_files','payload_file_count','regular_payload_files']:
            if key in d:assert d[key]==count
        record={'full_tree':full,'manifest_file':mf,'manifest_sha256':d['manifest_sha256'],
                'delivery_sha256':sha((p/'delivery.json').read_bytes()),'payload_files':count,
                'receipt_bound_metadata_files':len(metadata),'symlinks':0,
                'judgment_sha256':sha((p/'independent-judgment.json').read_bytes())}
        records[rel]=record
        summary[suffix]={k:v for k,v in record.items() if k!='full_tree'}
    put('incoming-audits.json',records)
    print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
