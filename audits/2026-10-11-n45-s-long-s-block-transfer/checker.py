"""Strictly read-only validation against recurrence AND independent original edges."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
import transfer
import direct_enumerator

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent

def first_difference(expected,actual,path='',vertices=None,field=None):
    if type(expected)!=type(actual):
        return f'{path}: expected {type(expected).__name__}, observed {type(actual).__name__}'
    if isinstance(expected,dict):
        if 'case_id' in expected:
            path+=' case='+expected['case_id']; vertices=expected.get('vertices',vertices)
        if 'literal' in expected:
            path+=' row='+expected['literal']
        if 'tuple' in expected and 'r' in expected:
            path+=f" ambient(tuple={expected['tuple']},r={expected['r']})"
        elif 'r' in expected and 's' in expected:
            path+=f" pin(r={expected['r']},s={expected['s']})"
        if 's_spokes' in expected:
            path+=' s_spokes='+str(expected['s_spokes'])
        for k in expected:
            if k not in actual:
                return f'{path}: missing required field {k}'
        for k in actual:
            if k not in expected:
                return f'{path}: unexpected field {k}'
        for k in expected:
            d=first_difference(expected[k],actual[k],path+'/'+k,vertices,k)
            if d:
                return d
    elif isinstance(expected,list):
        if field=='vertices' and expected!=actual:
            missing=[v for v in expected if v not in actual]
            return f'{path}: missing original vertex {missing[0]}' if missing else f'{path}: original vertex order changed'
        if field=='ambient_fibres':
            keys=lambda cell:(tuple(cell['tuple']),cell['r'])
            actual_keys={keys(x) for x in actual}
            for x in expected:
                if keys(x) not in actual_keys:
                    return f"{path}: missing ambient cell tuple={x['tuple']},r={x['r']},empty={not x['preimages']}"
        if len(expected)!=len(actual):
            return f'{path}: expected {len(expected)} entries, observed {len(actual)}'
        for i,(e,a) in enumerate(zip(expected,actual)):
            vp=f'{path}[{i}]'
            if field in ('colour_vector','assignments_vector') and vertices and i<len(vertices):
                vp+=f' original vertex={vertices[i]}'
            nextfield='colour_vector' if field in ('preimages','restored_preimages','assignments') else field
            d=first_difference(e,a,vp,vertices,nextfield)
            if d:
                return d
    elif expected!=actual:
        return f'{path}: expected {expected!r}, observed {actual!r}'
    return None

def authority_check():
    inputs=json.loads((HERE/'inputs.json').read_text())
    for entry in inputs['BASE_blobs']+inputs['sealed_audit_SHA256']:
        p=HERE/entry['frozen_path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],'frozen authority drift '+entry['path']
        if entry['authority']=='BASE Git blob':
            blob=subprocess.check_output(['git','rev-parse',inputs['base']+':'+entry['path']],cwd=ROOT,text=True).strip()
            assert blob==entry['git_blob'],'BASE Git object mismatch '+entry['path']
        else:
            assert entry['git_blob'] is None and entry['included_in_BASE_claimed'] is False

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',required=True)
    parser.add_argument('--cases',type=Path,default=HERE/'cases.json')
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=parser.parse_args()
    authority_check()
    expected=transfer.calculate(args.cases)
    direct=direct_enumerator.enumerate_certificate(args.cases.read_bytes())
    d=first_difference(expected,direct,'recurrence_vs_original_edges')
    if d:
        raise ValueError(d)
    actual=json.loads(args.certificate.read_text())
    d=first_difference(expected,actual,'certificate')
    if d:
        raise ValueError(d)
    assert args.certificate.read_bytes()==transfer.canonical(expected),'certificate canonical bytes differ'
    rows=[r for c in expected['cases'] for r in c['rows']]
    summary={
        'status':'passes','adoption':'待獨立驗收',
        'valid_cases':len(expected['cases']),'failed_declared_cases':expected['failed_cases'],
        'rows':len(rows),'assignments':sum(len(r['assignments']) for r in rows),
        'ambient_cells':sum(len(r['ambient_fibres']) for r in rows),
        'empty_ambient_cells':sum(not x['preimages'] for r in rows for x in r['ambient_fibres']),
        'ordered_pins':sum(len(r['pins']) for r in rows),
        'spoke_filtered_pin_cells':sum(len(x['pins']) for r in rows for x in r['spoke_variants']),
        'certificate_sha256':hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
        'target_source':expected['target_source']
    }
    print(json.dumps(summary,ensure_ascii=False,sort_keys=True))
    return 0

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (AssertionError,ValueError,KeyError,TypeError,IndexError) as error:
        print(json.dumps({'status':'rejected','reason':str(error)},ensure_ascii=False,sort_keys=True),file=sys.stderr)
        raise SystemExit(1)
