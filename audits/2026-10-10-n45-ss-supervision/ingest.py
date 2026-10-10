#!/usr/bin/env python3
"""Independent exact manifests and full-tree binding of sealed peer audits."""
import json
import review as r

def main():
    records = {}
    findings = []
    supplementary = []
    judgments = {
        'ssa': 'b29a4cb7917831849e02491bfa28446c2e9e49c3d6110278b3f7efc95fa9e4ab',
        'ssg': '8d595a693b85b57263fbe7ec10208130d839dee28eb2c82abc5fab7e906f6caa',
        'ssc': '15cbd8c657d070a92d0c6506903f4b48c430ce43eee1ce542654cdce7171101b'}
    for name, digest in judgments.items():
        rel = 'audits/2026-10-10-n45-'+name
        p = r.ROOT/rel
        d = json.loads((p/'delivery.json').read_text())
        def exclude(x):
            if x in {'MANIFEST.sha256', 'delivery.json'}: return True
            if name == 'ssg': return 'seal-checks' in x.split('/')
            return name == 'ssc' and x.startswith('seal-checks/')
        n = r.manifest(p, exclude)
        assert n == d.get('payload_file_count', d.get('payload_regular_files'))
        assert r.sha((p/'MANIFEST.sha256').read_bytes()) == d['manifest_sha256']
        assert r.sha((p/'independent-judgment.json').read_bytes()) == digest
        meta = r.manifest(p/'seal-checks', lambda x: x == 'MANIFEST.sha256') if name in {'ssg','ssc'} else None
        if name == 'ssg':
            prefix = 'frozen/current/audits/2026-10-10-n45-u-ss/seal-checks/'
            extra = sorted(str(f.relative_to(p)) for f in p.rglob('*') if f.is_file()
                           and 'seal-checks' in f.relative_to(p).parts and not str(f.relative_to(p)).startswith('seal-checks/'))
            assert len(extra) == 5 and all(x.startswith(prefix) for x in extra)
            for x in extra:
                raw = (p/x).read_bytes()
                assert raw == (r.WORKER/'seal-checks'/x.removeprefix(prefix)).read_bytes()
                supplementary.append(r.sha(raw)+'  '+rel+'/'+x+'\n')
            findings.append({'id': 'SS-SUP-PACK-01', 'original_top_level_exclusion_inventory_probe_exit': 1,
              'issue': 'SSG manifest excludes every seal-checks path component, wider than receipt top-level seal-checks/**',
              'extra_excluded_files': extra, 'count': 5, 'paper_block': False,
              'disposition': 'Original bytes preserved; all five match worker sealed metadata and are bound by supervisory supplemental manifest and full-tree snapshot.'})
        records[rel] = {'payload_files': n, 'metadata_files': meta, 'judgment_sha256': digest,
          'report_sha256': r.sha((p/'REPORT.md').read_bytes()),
          'receipt_sha256': r.sha((p/'delivery.json').read_bytes()), 'state': r.tree(p)}
    assert r.tree(r.WORKER) == json.loads((r.OUT/'inputs-before.json').read_text())['worker']
    r.put('inventory-findings.json', findings)
    with (r.OUT/'ssg-supplement.sha256').open('x') as f: f.write(''.join(supplementary))
    r.put('incoming-audits.json', records)
    print(json.dumps({k: {a:b for a,b in v.items() if a != 'state'} for k,v in records.items()}, sort_keys=True))

if __name__ == '__main__': main()
