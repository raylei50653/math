#!/usr/bin/env python3
"""Read recorded provenance hashes in the certificates actually replayed."""
import argparse
import hashlib
import json
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--replays',type=Path,nargs='+',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();root=args.repo.resolve()
    names=sorted({r['name'] for p in args.replays for r in json.loads(p.read_text())})
    results=[]
    for name in names:
        path=root/'artifacts'/name/'observations.json'
        raw=path.read_bytes();data=json.loads(raw);inputs={}
        fields=[]
        for key in ('input_sha256','inputs_sha256','source_sha256'):
            if isinstance(data.get(key),dict):
                fields.append(key);inputs.update(data[key])
        if isinstance(data.get('script_sha256'),str):
            fields.append('script_sha256');inputs[f'scripts/{name}.py']=data['script_sha256']
        records=[]
        for rel,recorded in sorted(inputs.items()):
            file=root/rel
            current=hashlib.sha256(file.read_bytes()).hexdigest() if file.is_file() else None
            records.append(dict(path=rel,recorded_sha256=recorded,current_sha256=current,
                               equal=recorded==current,
                               classification='document_provenance' if rel.startswith('docs/') else 'non_document_input'))
        results.append(dict(artifact=str(path.relative_to(root)),artifact_sha256=hashlib.sha256(raw).hexdigest(),size=len(raw),
                            hash_map_fields=fields,input_count=len(inputs),inputs=records,
                            drift=[r for r in records if not r['equal']]))
    args.output.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(certificate_count=len(results),declared_input_hashes=sum(r['input_count'] for r in results),
                         hash_drift_count=sum(len(r['drift']) for r in results),
                         non_document_drift_count=sum(d['classification']!='document_provenance' for r in results for d in r['drift'])),sort_keys=True))

if __name__=='__main__':main()
