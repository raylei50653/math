"""Reproduce an accepted finite simple graph failing in display serialization.

The vertex value is generated programmatically to avoid JSON's same decimal
conversion limit. No solver source or interpreter setting is modified.
"""
import sys, json, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from four_color_lab import normalize_graph, solve
from four_color_constraints import solve_constraints
limit=sys.get_int_max_str_digits()
records=[]
if not limit:
    raise SystemExit('Interpreter decimal integer conversion limit is disabled; example does not apply.')
for digits in (limit,limit+1):
    vertex=10**(digits-1)
    graph={'vertices':[vertex],'edges':[]}
    normalize_graph(graph)
    for engine in (solve_constraints,solve):
        rec={'engine':engine.__name__, 'vertex_expression':f'10**{digits-1}',
             'decimal_digits':digits,'input_accepted_by_normalize_graph':True,
             'known_witness_colors':[0], 'vertices':1,'edges':0,
             'options':{'trace_limit':0}}
        try:
            r=engine(graph,trace_limit=0)
            rec.update(status=r['status'],colors=r['colors'])
        except Exception as e:
            rec.update(exception_type=type(e).__name__,error=str(e),traceback=traceback.format_exc())
        records.append(rec)
result={'python':sys.version,'int_max_str_digits':limit,'records':records,
        'classification':'API input-label serialization exception; not an incorrect four-color decision'}
print(json.dumps(result,indent=2))
