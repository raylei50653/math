#!/usr/bin/env python3
"""Read-only frozen-input integrity and relation calibration, not a paper proof."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from calibration import semantic_calibration

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
LOGS = {f'receipt/{name}.{stream}.log' for name in ('normal','seed17') for stream in ('stdout','stderr')}
EXCLUDED = {'MANIFEST.sha256','delivery.json','receipt.json'} | LOGS
IDS = ['LOW2-CORE','LOW2-COMP','LOW2-JOIN','LOW2-F','LOW2-MAP','LOW2-EXCLUSION']

def require(value,message):
    if not value:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def manifest(directory, filename, excluded):
    actual = set()
    for path in directory.rglob('*'):
        relative = path.relative_to(directory).as_posix()
        require(not path.is_symlink(), 'unexpected symlink: '+relative)
        if path.is_file() and relative not in excluded:
            actual.add(relative)
    entries = {}
    for line in (directory/filename).read_text().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
        require(match is not None,'manifest syntax differs')
        digest,relative = match.groups()
        require(not Path(relative).is_absolute() and '..' not in Path(relative).parts,'manifest unsafe path')
        require(relative not in entries,'manifest duplicate path')
        entries[relative] = digest
    require(set(entries)==actual,'manifest exact payload inventory differs')
    for relative,digest in entries.items():
        require(sha(directory/relative)==digest,'manifest digest differs: '+relative)
    return len(entries)

def frozen_worker():
    directory = HERE/'frozen/worker'
    inputs = read(HERE/'inputs.json')
    catalog = {item['path']:item['sha256'] for item in inputs['worker_files']}
    actual = {p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file()}
    require(actual==set(catalog),'frozen worker inventory differs')
    for relative,digest in catalog.items():
        require(sha(directory/relative)==digest,'frozen worker digest differs')
    delivery = read(directory/'delivery.json')
    probes = ('bad-digest','missing-nested-delivery','duplicate-path','unsafe-path','missing-payload','bad-receipt')
    runs = ('normal','seed17')+probes
    metadata = {f'receipt/{name}.{stream}.log' for name in runs for stream in ('stdout','stderr')}
    excluded = {'MANIFEST.sha256','delivery.json','receipt.json'}|metadata
    require(set(delivery['excluded_exact_paths'])==excluded,'worker exclusion paths differ')
    count = manifest(directory,'MANIFEST.sha256',excluded)
    require(count==66,'worker payload count differs')
    require(sha(directory/'MANIFEST.sha256')==delivery['manifest_sha256'],'worker manifest binding differs')
    require(sha(directory/'receipt.json')==delivery['receipt_sha256'],'worker receipt binding differs')
    receipt = read(directory/'receipt.json')
    require(set(receipt['metadata'])==metadata,'worker receipt log inventory differs')
    for relative,digest in receipt['metadata'].items():
        require(sha(directory/relative)==digest,'worker receipt log digest differs')
    require([r['name'] for r in receipt['commands']]==list(runs),'worker command inventory differs')
    for run in receipt['commands']:
        require(run['exit_code']==run['expected_exit'],'worker recorded exit differs')
        require(run['expected_exit']==(2 if run['name'] in probes else 0),'worker expected exit differs')
        require(run['control_classification']=='triggered and holds','worker tool classification differs')
        if run['name'] in probes:
            require(run['rejection_stage'] in (directory/run['stderr']).read_text(),'worker rejection stage differs')
    require((directory/'receipt/normal.stdout.log').read_bytes()==(directory/'receipt/seed17.stdout.log').read_bytes(),'worker seeded replay differs')
    require(receipt['payload_before']==receipt['payload_after']==delivery['manifest_sha256'],'worker read-only identity differs')
    require(len(inputs['current_pins_initial'])==8,'pin inventory differs')
    for pin in inputs['current_pins_initial']:
        require(pin['matches'] and pin['actual']==pin['expected'],'initial pin differs')
        require(sha(directory/'frozen/current'/pin['path'])==pin['expected'],'frozen pin differs')
    for item in inputs['BASE_inputs']:
        blob = subprocess.check_output(['git','show',BASE+':'+item['path']],cwd=ROOT)
        require(hashlib.sha256(blob).hexdigest()==item['sha256'],'BASE hash differs')
        require(blob==(directory/'frozen/BASE'/item['path']).read_bytes(),'frozen BASE bytes differ')
        obj = subprocess.check_output(['git','rev-parse',BASE+':'+item['path']],cwd=ROOT,text=True).strip()
        require(obj==item['git_blob'],'BASE object differs')
    return len(catalog)

def judgment():
    paper = read(HERE/'independent-judgment.json')
    original = read(HERE/'frozen/worker/claims.json')
    require(paper['BASE']==original['BASE']==BASE,'judgment BASE differs')
    require(paper['full_source_contract']==original['full_source_contract'],'judgment contract differs')
    require(len(paper['full_source_contract'])==12,'incomplete full source contract')
    require([c['id'] for c in paper['claims']]==IDS,'claim inventory differs')
    for claim,source in zip(paper['claims'],original['claims']):
        require(claim['source_contract']==paper['full_source_contract'],'claim missing full contract')
        require(claim['dependencies']==source['dependencies'],'claim dependencies differ')
        require(claim['external_dependencies']==source['external_dependencies'],'external trust differs')
        require(claim['quantifier']==source['quantifier'],'claim quantifier differs')
        require(claim['additional_premises']==[] and not claim['machine_proved'],'additional premise or evidence layer differs')
        require(claim['verdict']=='accepted_with_full_stated_LOW2_contract','verdict differs')
    require(paper['source_control_evaluation']=='not established; not executed; no trigger count','source coverage differs')
    recomputed = semantic_calibration()
    expected = json.dumps(recomputed,sort_keys=True,indent=2)+'\n'
    require((HERE/'calibration.json').read_text()==expected,'relation calibration bytes differ')
    return recomputed['all_ambient_root_contact_fibres_checked']

def authored():
    names = ['REPORT.md','prepare.py','calibration.py','verify.py','seal.py','inputs.json','independent-judgment.json','calibration.json']
    for relative in names:
        data = (HERE/relative).read_text()
        require(data.endswith('\n'),'authored text lacks newline')
        require(all(line==line.rstrip(' \t') for line in data.splitlines()),'authored trailing whitespace')
    text = re.sub(r'(`+).*?\1','',(HERE/'REPORT.md').read_text())
    for relative in re.findall(r'\]\(([^\s)]+)\)',text):
        if '://' in relative:
            continue
        target = relative.split('#',1)[0]
        if target in EXCLUDED and not (HERE/target).exists():
            continue
        require((HERE/target).exists(),'authored report link missing: '+relative)

def outer_receipt():
    delivery = read(HERE/'delivery.json')
    require(set(delivery['excluded_exact_paths'])==EXCLUDED,'outer exclusion paths differ')
    require(sha(HERE/'MANIFEST.sha256')==delivery['manifest_sha256'],'outer manifest binding differs')
    require(sha(HERE/'receipt.json')==delivery['receipt_sha256'],'outer receipt binding differs')
    receipt = read(HERE/'receipt.json')
    require(set(receipt['metadata'])==LOGS,'outer receipt exact log inventory differs')
    for relative,digest in receipt['metadata'].items():
        require(sha(HERE/relative)==digest,'outer receipt log digest differs')
    require([r['name'] for r in receipt['commands']]==['normal','seed17'],'outer command inventory differs')
    for run in receipt['commands']:
        require(run['exit_code']==0,'outer actual command exit differs')
        require(run['payload_before']==run['payload_after']==delivery['manifest_sha256'],'outer payload changed')
    require((HERE/'receipt/normal.stdout.log').read_bytes()==(HERE/'receipt/seed17.stdout.log').read_bytes(),'outer seeded stdout differs')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--payload-only',action='store_true',help='During receipt preparation, omit only this audit outer metadata checks')
    args = parser.parse_args()
    try:
        count = manifest(HERE,'MANIFEST.sha256',EXCLUDED)
        worker_count = frozen_worker()
        fibres = judgment()
        authored()
        if not args.payload_only:
            outer_receipt()
        print(json.dumps({'status':'frozen_integrity_and_relation_calibration_hold','payload_files':count,
                          'worker_frozen_files':worker_count,'worker_payload_files':66,'BASE_blobs':4,
                          'frozen_initial_pins':8,'paper_claims':6,'calibration_ambient_fibres':fibres,
                          'outer_receipt_checked':not args.payload_only,'paper_proved_by_this_tool':False,
                          'source_controls':'not established; not executed; no trigger count'},sort_keys=True))
    except (OSError,ValueError,KeyError,AssertionError,subprocess.CalledProcessError) as error:
        print('integrity rejection: '+str(error),file=sys.stderr)
        return 2
    return 0

if __name__=='__main__':
    sys.exit(main())
