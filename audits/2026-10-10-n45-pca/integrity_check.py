#!/usr/bin/env python3
"""Read-only PC inventory and fresh input-integrity verification."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

HOME=Path(__file__).resolve().parent
ROOT=HOME.parent.parent
PC=ROOT/'audits/2026-10-09-n45-pc'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    inputs=json.loads((HOME/'inputs.json').read_text())
    original=[]
    for item in inputs['authority_files']:
        assert digest(HOME/item['frozen'])==item['sha256'], item['frozen']
        path=PC/'source'/item['path'] if item['authority']=='BASE Git blob' else ROOT/item['path']
        assert digest(path)==item['sha256'],str(path)
        record={'path':str(path.relative_to(ROOT)),'sha256':digest(path),'bytes':path.stat().st_size,'byte_drift':False}
        if 'mtime_ns' in item:
            record['mtime_ns']=path.stat().st_mtime_ns
            record['mtime_drift']=record['mtime_ns']!=item['mtime_ns']
            assert not record['mtime_drift'],str(path)
        else:
            record['mtime_check']='BASE worker source mtime was not recorded initially; bytes checked against Git blob'
        original.append(record)
    delivery=json.loads((PC/'delivery.json').read_text())
    manifest=PC/'MANIFEST.sha256'
    assert digest(manifest)==delivery['manifest_sha256']
    inventory=[]
    for line in manifest.read_text().splitlines():
        h,relative=line.split('  ',1)
        assert digest(PC/relative)==h,relative
        inventory.append({'path':relative,'sha256':h,'bytes':(PC/relative).stat().st_size})
    assert len(inventory)==delivery['inventory_files']
    assert sum(p['bytes'] for p in inventory)==delivery['inventory_bytes']
    head=subprocess.check_output(['git','-C',str(PC/'source'),'rev-parse','HEAD'],text=True).strip()
    status=subprocess.check_output(['git','-C',str(PC/'source'),'status','--porcelain'],text=True)
    assert head==inputs['BASE'] and not status
    result={'worker_manifest_sha256':digest(manifest),'worker_inventory_files':len(inventory),'worker_inventory_bytes':sum(p['bytes'] for p in inventory),
            'worker_HEAD':head,'worker_clean':not status,'original_and_frozen_inputs':original,'byte_drift_count':0,'recorded_mtime_drift_count':0,
            'scope':'Integrity only. Reading payload bytes does not adopt paper judgments or imply general source coverage.'}
    with (HOME/'checks/read-only-after.json').open('xb') as f:
        f.write((json.dumps(result,sort_keys=True,indent=2)+'\n').encode())
    print(json.dumps({k:result[k] for k in ['worker_inventory_files','worker_inventory_bytes','worker_clean','byte_drift_count','recorded_mtime_drift_count']},sort_keys=True))


if __name__=='__main__':
    main()
