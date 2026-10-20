import importlib.util,json
from pathlib import Path
p=Path('audits/2026-10-20-r6-941-j1-c11-1148ce0/review')
spec=importlib.util.spec_from_file_location('publication_dual',p/'dual_check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
for name in ('drop-active-halfrow','excess-witness-weight','omit-zero-halfrows','uncancelled-signed-span','flip-live-multiplier','drop-positive-witness','omit-orbit-slack'):
 try:m.verify(p/f'dual-negative-{name}.json')
 except AssertionError as exc:print(json.dumps({'negative_control':name,'rejected':True,'reason':str(exc)}),flush=True)
 else:raise AssertionError(('accepted corrupt certificate',name))
print(json.dumps({'status':'PASS all 7 independent corruptions rejected'}),flush=True)
