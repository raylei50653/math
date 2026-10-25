"""Lossless compact indexing for the seven-row witness certificates."""
from pathlib import Path
import argparse
import gzip
import hashlib
import json

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'frozen/audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/certificate.json'


def encode_partition(p):
    return tuple(sorted(sum(1<<v for v in b) for b in p))


def compact(raw):
    partitions=sorted({encode_partition(p) for c in raw['necessary_controls'] for pair in c['choices'] for p in pair})
    lookup={p:i for i,p in enumerate(partitions)}
    choices=sorted({tuple(lookup[encode_partition(p)] for pair in c['choices'] for p in pair)
                    for c in raw['necessary_controls']})
    choice_lookup={c:i for i,c in enumerate(choices)}
    out={k:v for k,v in raw.items() if k!='necessary_controls'}
    out.update(schema='941-k8-seven-row-compact-v1',base='78375cc0e995c868c221605c24835d7e622f0091',
               strong=True,source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
               partition_catalogue=partitions,choice_catalogue=choices,
               necessary_controls=[[c['state'],choice_lookup[tuple(lookup[encode_partition(p)] for pair in c['choices'] for p in pair)]]
                                   for c in raw['necessary_controls']])
    for c,encoded in zip(raw['necessary_controls'],out['necessary_controls']):
        assert c['state']==encoded[0]
        recovered=[partitions[i] for i in choices[encoded[1]]]
        assert recovered==[encode_partition(p) for pair in c['choices'] for p in pair]
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('indices',nargs='+',type=int);args=parser.parse_args()
    for i in args.indices:
        raw_path=HERE/f'CAP_{i}.json'
        raw=json.loads(raw_path.read_text() if raw_path.exists() else gzip.decompress(raw_path.with_suffix('.json.gz').read_bytes()))
        out=compact(raw)
        with (HERE/f'CAP_{i}_COMPACT.json').open('x') as f:
            json.dump(out,f,sort_keys=True,separators=(',',':'));f.write('\n')
        print(i,'partitions',len(out['partition_catalogue']),'choices',len(out['choice_catalogue']),
              'states',len(out['remaining']),flush=True)


if __name__=='__main__':
    main()
