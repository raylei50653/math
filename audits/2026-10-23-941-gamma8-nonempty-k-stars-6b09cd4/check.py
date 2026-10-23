#!/usr/bin/env python3
"""Reconstruct necessary complete N stars; do not complete the original source."""
import argparse
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import random
from models import reconstruct,refinements,k_interfaces,PREV

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'

def require(ok,why):
    if not ok:raise ValueError(why)

def custody():
    data=json.loads((HERE/'INPUTS.json').read_text())
    require(data['base']==BASE and len(data['inputs'])==8,'input domain/BASE changed')
    for row in data['inputs']:
        raw=(HERE/row['snapshot']).read_bytes()
        require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']),'frozen authority changed: '+row['path'])
        require(raw==(ROOT/row['path']).read_bytes(),'live authority changed: '+row['path'])
    return dict(immutable_inputs=8,immutable_drift=0)

@lru_cache(None)
def expected():
    rows=reconstruct()
    rejects=refinements(rows)
    interfaces=k_interfaces(rows,rejects)
    require(len(rows)==563 and len(rejects)==83 and len(interfaces)==480,'necessary-star domain mismatch')
    require(Counter(r['reason'] for r in rejects)=={'omega-known-C-E-12-path':44,'K02-bichromatic-original-C4':39},'explicit source rejections changed')
    return dict(schema='941-gamma8-nonempty-k-stars-v1',base=BASE,
        paper_domain=dict(j=2,resource_count=7,M2_nonempty=True,
            omega_types=['K0','K2'],complete_M=['T','m'],degree_T=5,degree_m=5,
            same_original_G_F=True,original_rotation=True,literal_phi_psi=True,
            full_components=True,all_empty_fibres_and_full_lifts_preserved=True),
        relaxed_complete_N_star_rows=rows,
        rejected_relaxed_rows=rejects,
        necessary_complete_N_star_row_ids=[i for i in range(len(rows)) if i not in {r['row'] for r in rejects}],
        complete_K_star_interfaces=interfaces,
        conclusion=dict(relaxed_star_rows=563,necessary_star_rows=480,
            necessary_K0_rows=300,necessary_K2_rows=180,
            K0_d_equals_U_rows=120,K2_forces_m_C_and_d_not_U=True,
            stars_are_undirected_cyclic_representatives=True,
            common_oriented_faces_required=True,
            K_star_external_13_tails_must_be_retained=True,
            no_previous_60_or_16_table_inherited_by_literal_identity=True),
        preserved_complete_predecessor_certificate=json.loads((HERE/'frozen'/PREV).read_text()),
        authority_boundaries=dict(finite_control='triggered and holds',source_realizability='not triggered',
            eleven_type_exclusions=0,full_exterior_disk='OPEN',general_wrong_side='OPEN',
            common_k_lower_bound=23,new_Lean=False,new_LP=False,smaller_bad=False))

def validate(cert,seed=0):
    ref=expected()
    keys=list(ref);random.Random(seed).shuffle(keys)
    require(set(cert)==set(ref),'certificate key domain changed')
    for key in keys:require(cert[key]==ref[key],'certificate mismatch: '+key)
    return dict(status='PASS',relaxed_complete_N_star_rows=563,
        refined_complete_N_star_rows=480,K0_rows=300,K2_rows=180,
        d_equals_U_rows=120,wrong_C_E_rows_rejected=44,bichromatic_C4_rows_rejected=39,
        complete_K_star_interfaces=480,predecessor_fibres_and_full_lifts_preserved=True,
        source_realizability='not triggered',eleven_type_exclusions=0)

def negatives(cert):
    controls=[
        ('delete_N_star',lambda c:c['relaxed_complete_N_star_rows'].pop()),
        ('delete_full_n_contact',lambda c:c['relaxed_complete_N_star_rows'][0]['full_links']['n'].pop()),
        ('forget_original_face_edge',lambda c:c['relaxed_complete_N_star_rows'][0]['edges'].pop()),
        ('drop_d_U_alias',lambda c:c['conclusion'].update(K0_d_equals_U_rows=0)),
        ('restore_wrong_C_E_omega',lambda c:c['rejected_relaxed_rows'].pop()),
        ('lose_complete_K_connectivity',lambda c:c['complete_K_star_interfaces'][0]['K_connected_requirements'].pop()),
        ('ban_external_K_13_contacts',lambda c:c['complete_K_star_interfaces'][0]['exit_and_omega_partial_stars'][0].update(other_original_neighbors_may_include_Z_external_13=False)),
        ('claim_whole_U_cyclic_star',lambda c:c['complete_K_star_interfaces'][0].update(U_original_full_cyclic_link_not_claimed=False)),
        ('delete_empty_fibres',lambda c:c['paper_domain'].update(all_empty_fibres_and_full_lifts_preserved=False)),
        ('claim_literal_old_cap',lambda c:c['conclusion'].update(no_previous_60_or_16_table_inherited_by_literal_identity=False)),
        ('claim_source',lambda c:c['authority_boundaries'].update(source_realizability='triggered and holds')),
        ('claim_eleven_type_exclusion',lambda c:c['authority_boundaries'].update(eleven_type_exclusions=1))]
    rejected=[]
    for name,mutate in controls:
        bad=deepcopy(cert);mutate(bad)
        try:validate(bad)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise ValueError('negative accepted: '+name)
    return dict(negative_controls_rejected=rejected,count=len(rejected))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--negative',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=parser.parse_args();cert=json.loads(args.certificate.read_text())
    out=dict(custody=custody(),validation=validate(cert,args.seed))
    if args.negative:out['negative']=negatives(cert)
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
