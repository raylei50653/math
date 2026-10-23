#!/usr/bin/env python3
"""Exclusive-create authority snapshots and a paper-list certificate."""
from pathlib import Path
from hashlib import sha256
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
AUTH=[
'audits/2026-10-23-941-types-wrong-side-round3-6b09cd4/REPORT.md',
'audits/2026-10-23-941-gamma8-chi-six-6b09cd4/PROOF.md',
'audits/2026-10-23-941-gamma8-rootless-stars-6b09cd4/PROOF.md',
'audits/2026-10-23-941-gamma8-six-equality-6b09cd4/PROOF.md',
'audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/PROOF.md',
'audits/2026-10-23-941-gamma8-cells-6b09cd4/PROOF.md',
'audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json',
'audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json',
'audits/2026-10-23-941-types-wrong-side-round3-6b09cd4/VERIFICATION.json']
def write(path,value):
 with path.open('x') as f:json.dump(value,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
inputs=[]
for name in AUTH:
 raw=(ROOT/name).read_bytes();out=HERE/'frozen'/name;out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():
  assert out.read_bytes()==raw,'retained frozen authority drift'
 else:
  with out.open('xb') as f:f.write(raw)
 inputs.append(dict(path=name,snapshot=str(out.relative_to(HERE)),bytes=len(raw),sha256=sha256(raw).hexdigest()))
write(HERE/'INPUTS.json',dict(schema='941-empty-resource-inputs-v1',base=BASE,authority=inputs))
rows=[
 dict(core='L',id='L0',y=['a','T','b','U','p_d'],a=['r','T','y','p_d','d'],b=['s','T','y','U','p_x'],reason='old_sealed_N'),
 dict(core='L',id='L1',y=['a','T','b','U','omega','p_d'],a=['r','T','y','p_d','d'],b=['s','T','y','U','p_x'],reason='opposite_exits_full_omega_link'),
 dict(core='R',id='R0',y=['a','T','b','p_x','U'],a=['r','T','y','U','p_d'],b=['s','T','y','p_x','x'],reason='old_sealed_N'),
 dict(core='R',id='R1',y=['a','T','b','p_x','omega','U'],a=['r','T','y','U','p_d'],b=['s','T','y','p_x','x'],reason='opposite_exits_full_omega_link'),
 dict(core='R',id='R2',y=['a','T','b','p_x','omega','p_d'],a=['r','T','y','p_d','U'],b=['s','T','y','p_x','x'],reason='same_color_common_neighbors_degree_four')]
write(HERE/'certificate.json',dict(schema='941-empty-resource-stars-v1',base=BASE,
 contract=dict(D=6,M2_empty=True,resource_size=6,extra_resource='omega',same_original_source=True,complete_original_stars=True,U_is_boundary_exception=True),
 eliminated_owners=['R02_outside_M','R13_outside_N','N1','N3'],remaining_owners=['K0','K2'],
 partial_N3_star_patterns=rows,
 K_star_envelopes=dict(K0=['r','s','a','y','b','p_d','p_x','e','h','W','frame13','chi_if_color3'],K2=['r','s','a','y','b','d','x','U','e','h','W','frame13','chi_if_color3']),
 boundaries=dict(source_realizability='not triggered',finite_control='triggered and holds',empty_M2_X7='OPEN',all_eleven_types='OPEN',general_wrong_side='OPEN',common_k=23,D_at_least_8='unchanged'))) 
print('exclusive input and certificate generation complete')
