"""Exclusive certificate generation; all failure/negative outputs are retained."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True
import transfer

HERE=Path(__file__).resolve().parent

def exclusive(path,value):
    with path.open('xb') as f:
        f.write(transfer.canonical(value))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',action='store_true')
    parser.add_argument('--negatives',action='store_true')
    args=parser.parse_args()
    assert args.certificate != args.negatives
    if args.certificate:
        cert=transfer.calculate(HERE/'cases.json')
        exclusive(HERE/'certificate.json',cert)
        data=json.loads((HERE/'cases.json').read_text())
        degree=[]
        for c in data['cases']:
            degree.append({'case_id':c['id'],'expected_valid':c['expected_valid'],
              'vertices':[{'vertex':v,'deg_C':sum(v in e for e in c['original_edges']),
                           'N_B':c['boundary_attachments'][v],'s_contact':v in c['s_contacts'],
                           'full_degree':sum(v in e for e in c['original_edges'])+len(c['boundary_attachments'][v])+int(v in c['s_contacts'])}
                          for v in c['vertices']],
              'findings':transfer.degree_findings(c),'disk_topology_verified':False})
        exclusive(HERE/'degree-audit.json',{'status':'待獨立驗收','cases':degree})
        print(json.dumps({'generated':'certificate.json','sha256':hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest(),'failed_cases':cert['failed_cases']},sort_keys=True))
    else:
        cert=json.loads((HERE/'certificate.json').read_text())
        altered=copy.deepcopy(cert)
        c=altered['cases'][0]; row=c['rows'][0]
        cell=next(x for x in row['ambient_fibres'] if x['preimages'])
        i=c['vertices'].index('r'); old=cell['preimages'][0][i]
        cell['preimages'][0][i]=(old+1)%4
        exclusive(HERE/'negative-r-colour.json',altered)
        plan=[{'certificate':'negative-r-colour.json','mutation':'change one complete ambient preimage r colour',
               'case':c['case_id'],'row':row['literal'],'tuple':cell['tuple'],'r_cell':cell['r'],
               'original_vertex':'r','old_colour':old,'new_colour':cell['preimages'][0][i]}]
        altered=copy.deepcopy(cert); c=altered['cases'][0]; row=c['rows'][0]
        cell=next(x for x in row['ambient_fibres'] if not x['preimages'])
        row['ambient_fibres'].remove(cell)
        exclusive(HERE/'negative-empty-cell.json',altered)
        plan.append({'certificate':'negative-empty-cell.json','mutation':'delete one empty ambient fibre',
                     'case':c['case_id'],'row':row['literal'],'tuple':cell['tuple'],'r_cell':cell['r']})
        altered=copy.deepcopy(cert); c=next(x for x in altered['cases'] if x['case_id']=='BRIDGE_FIX6')
        i=c['vertices'].index('l2'); c['vertices'].pop(i)
        for row in c['rows']:
            all_lists=[row['assignments']]
            all_lists += [x['preimages'] for x in row['ambient_fibres']]
            all_lists += [x[k] for x in row['pins'] for k in ['preimages','restored_preimages']]
            all_lists += [x[k] for variant in row['spoke_variants'] for x in variant['pins'] for k in ['preimages','restored_preimages']]
            # JSON reload created separate vectors; avoid deleting twice if any list alias exists.
            seen=set()
            for vectors in all_lists:
                for vector in vectors:
                    if id(vector) not in seen:
                        seen.add(id(vector)); vector.pop(i)
        exclusive(HERE/'negative-missing-branch.json',altered)
        plan.append({'certificate':'negative-missing-branch.json','mutation':'omit original branch vertex and its coordinates',
                     'case':'BRIDGE_FIX6','original_vertex':'l2','original_edge':['l0','l2']})
        exclusive(HERE/'negative-plan.json',{'status':'待獨立驗收','controls':plan,
                  'scope':'transfer validator controls, no target source search'})
        print(json.dumps({'negative_certificates':[p['certificate'] for p in plan]},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except (AssertionError,ValueError,OSError) as error:
        print(str(error),file=sys.stderr)
        raise SystemExit(1)
