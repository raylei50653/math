from pathlib import Path
import importlib.util,json
D=Path(__file__).resolve().parent
J=D.parent/'frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d'
P=J/'frozen/audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
spec=importlib.util.spec_from_file_location('m',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=json.loads((J/'J1/certificate.json').read_text()); states=[t for t in m.growth(10,four=True) if m.proper(t)]; K=m.kempe(10,states)
fs=c['component_records'];live=set(c['final_live'])
print('loaded',len(live),flush=True)
for f in fs:
 i=f['core_id']; out,rounds=m.close(K,live-{i});remain=[z['core'] for z in fs if z['core_id'] in out]
 print('delete',f['core'],'=>',len(out),len(rounds),'remaining',remain,flush=True)
c2=json.loads((J/'J2/certificate.json').read_text());fs2=c2['forms'];live2=set(c2['live'])
for f in fs2:
 i=f['core_index'];out,rounds=m.close(K,live2-{i});deleted=[z['literal_core'] for z in fs2 if z['core_index'] not in out]
 print('J2 delete',f['family'],f['literal_core'],'=>',len(out),len(rounds),'deletes',deleted,flush=True)
for f in fs2:
 keep={z['core_index'] for z in fs2 if z['family']==f['family']==3 and z['literal_core'][7:9]==f['literal_core'][7:9]} if f['family']==3 else {f['core_index']}
 target_ids={z['core_index'] for z in fs2};out,rounds=m.close(K,live2-(target_ids-keep))
 print('J2 only',f['family'],f['literal_core'],'=>',len(out),len(rounds),'survives',keep<=set(out),flush=True)
