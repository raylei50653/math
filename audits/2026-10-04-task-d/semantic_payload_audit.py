#!/usr/bin/env python3
"""Compare entire saved/rebuilt JSON, excluding only the direct input hash map."""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import sys

def differences(a, b, path='$'):
    if type(a) != type(b):
        return [dict(path=path, saved=a, rebuilt=b)]
    if isinstance(a, dict):
        result=[]
        for k in sorted(a.keys() | b.keys()):
            if k not in a or k not in b:
                result.append(dict(path=f'{path}.{k}', saved=a.get(k), rebuilt=b.get(k)))
            else: result.extend(differences(a[k], b[k], f'{path}.{k}'))
        return result
    if isinstance(a, list):
        if len(a) != len(b):
            return [dict(path=path+'.length', saved=len(a), rebuilt=len(b))]
        return [d for i,(x,y) in enumerate(zip(a,b)) for d in differences(x,y,f'{path}[{i}]')]
    return [] if a == b else [dict(path=path,saved=a,rebuilt=b)]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    root=args.repo.resolve();sys.path.insert(0,str(root/'scripts'))
    results=[]
    for name in ('c5_excess_two_mixed_core_single_spoke',
                 'c5_excess_two_mixed_core_four_spoke_singles'):
        module=importlib.import_module(name)
        raw=module.OUT.read_bytes()
        saved=json.loads(raw)
        built=module.build()
        rebuilt=json.loads(json.dumps(built,ensure_ascii=False))
        before=saved.pop('input_sha256')
        after=rebuilt.pop('input_sha256')
        all_diff=differences(before,after,'$.input_sha256')
        math_diff=differences(saved,rebuilt)
        serialized=(json.dumps(built,ensure_ascii=False,sort_keys=True,indent=1)+'\n').encode()
        result=dict(name=name,artifact=str(module.OUT.relative_to(root)),
                    artifact_sha256=hashlib.sha256(raw).hexdigest(),
                    rebuilt_bytes_sha256=hashlib.sha256(serialized).hexdigest(),
                    strict_bytes_equal=raw==serialized,
                    input_path_sets_equal=before.keys()==after.keys(),
                    direct_input_hash_differences=all_diff,
                    non_document_input_hash_differences=[d for d in all_diff if not d['path'].startswith('$.input_sha256.docs/')],
                    complete_payload_except_direct_input_hash_map_equal=not math_diff,
                    mathematical_payload_differences=math_diff,
                    saved_artifact_unchanged_after_build=raw==module.OUT.read_bytes(),
                    removed_fields=['input_sha256'])
        results.append(result)
        print(json.dumps({k:result[k] for k in ('name','strict_bytes_equal','complete_payload_except_direct_input_hash_map_equal','saved_artifact_unchanged_after_build')},sort_keys=True),flush=True)
    args.output.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    assert all(r['complete_payload_except_direct_input_hash_map_equal'] and not r['non_document_input_hash_differences'] and r['saved_artifact_unchanged_after_build'] for r in results)

if __name__=='__main__':main()
