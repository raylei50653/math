#!/usr/bin/env python3
"""Independent, stdlib-only exact checker for the frozen W7 necessary cone.

No optimizer, generated solver code, or baseline Python module is imported.
The orbit family is the fixed, previously checked input, not regenerated here.
"""
import argparse
from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
import gzip
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import random
import sys
import time

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
OLD = ROOT / 'audits/2026-10-20-r6-941-j1-five-edge-417732f'
BASE = 'd5b8a8605bcbcef7aebbcf1934dad7ba255ccf02'
SHA = {
    'caps.json.gz': '01547476f7afdc88ab224d640eaef363cfe765dd29e8983ca9df7aa63fdd68a3',
    'orbits.json.gz': '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad',
}
RIM = ('a','n','u4','u3','u2','u1','L','q','c','s','v','w','t')
ROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
POS_ROWS = (0,2,3,5,7,8,9)
LABELS = ['G['+ROWS[j]+']' for j in POS_ROWS] + ['G[01232,h=a]', 'G[01232,h=b]', 'Z[44459]+Z[44466]']
SCOPE = 'strict only-R/W7 subtype under inherited J1 source contract'


class Rejected(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Rejected(message)


def packed(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def digest(obj):
    return hashlib.sha256(packed(obj)).hexdigest()


def integer(x):
    return type(x) is int


def canonical(t):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in t)


def states(n, prefix=(0,)):
    if len(prefix) == n:
        if prefix[0] != prefix[-1]:
            yield prefix
        return
    for x in range(min(max(prefix)+1, 3)+1):
        if x != prefix[-1]:
            yield from states(n, prefix+(x,))


def decode_pinned(name, raw):
    require(hashlib.sha256(raw).hexdigest() == SHA[name], 'frozen input SHA256 mismatch: '+name)
    return json.loads(gzip.decompress(raw))


def load_pinned(name):
    return decode_pinned(name, (OLD/'counting'/name).read_bytes())


@lru_cache(None)
def left_star(a, n, L, q, c, forbidden):
    boundary = dict(a=a, n=n, L=L, q=q, c=c)
    g_edges = [('b','a'),('b','c'),('b','q'),('b','p'),('p','a'),('p','q'),
               ('p','n'),('p','h'),('h','q'),('h','L'),('h','R'),('h','n')]
    b_edges = [('b','a'),('b','c'),('b','q')]
    result = {name: [] for name in ('G','Q1','J1')}
    for b,p,h,R in product(range(4), repeat=4):
        if forbidden & (1 << R):
            continue
        colors = dict(boundary, b=b, p=p, h=h, R=R)
        if all(colors[u] != colors[v] for u,v in g_edges):
            result['G'].append((b,p,h,R))
    for b,R in product(range(4), repeat=2):
        if forbidden & (1 << R):
            continue
        colors = dict(boundary, b=b, R=R)
        if not all(colors[u] != colors[v] for u,v in b_edges):
            continue
        if b == n and R == q:
            result['Q1'].append((b,R))
        if b == L and R != a:
            result['J1'].append((b,R))
    return result


@lru_cache(None)
def right_star(a,c,s,v,w,t):
    edges = [('r','s'),('r','v'),('r','w'),('r','t'),('r','x'),('r','y'),
             ('x','c'),('x','s'),('x','y'),('y','a'),('y','t')]
    boundary = dict(a=a,c=c,s=s,v=v,w=w,t=t)
    out = []
    for x,y,r in product(range(4), repeat=3):
        colors = dict(boundary,x=x,y=y,r=r)
        if all(colors[u] != colors[v] for u,v in edges):
            out.append((x,y,r))
    return out


@lru_cache(None)
def caps_for(a,n,L,q,c,s,v,w,t,forbidden):
    result = {name: [0]*10 for name in ('G','Q1','J1')}
    sectors = [0,0]
    for name, lifts in left_star(a,n,L,q,c,forbidden).items():
        for lift in lifts:
            b = lift[0]
            for x,y,r in right_star(a,c,s,v,w,t):
                row = ROWS.index(''.join(map(str, canonical((x,y,a,b,c)))))
                result[name][row] += 1
                if name == 'G' and row == 9:
                    sectors[0] += int(lift[2] == a)
                    sectors[1] += int(lift[2] == b)
    return result, sectors


def encode(t):
    out = 0
    for x in t:
        out = 4*out+x
    return out


def half_representative(t):
    # Minimum over the eight permutations preserving the unordered pair split.
    choices = []
    for swap,left,right in product((0,1), repeat=3):
        perm = [(x ^ (left if x < 2 else right)) ^ (2*swap) for x in range(4)]
        choices.append(encode(tuple(perm[x] for x in t)))
    return min(choices)


def rebuild_rowmap(all_states):
    result = {}
    for i,t in enumerate(all_states):
        representatives = set()
        for mate in (1,2,3):
            other = [x for x in (1,2,3) if x != mate]
            perm = {0:0, mate:1, other[0]:2, other[1]:3}
            row = half_representative(tuple(perm[x] for x in t))
            require(row not in result or result[row] == i, 'row map is not a function')
            result[row] = i
            representatives.add(row)
        require(len(representatives) == 3, 'state does not have exactly three half-rows')
    return result


def load_model():
    caps = load_pinned('caps.json.gz')
    orbit = load_pinned('orbits.json.gz')
    all_states = list(states(13))
    require(len(all_states) == 66430, 'C13 state count')
    require([list(t) for t in all_states] == caps['states'], 'C13 canonical enumeration')
    require(list(RIM) == caps['ordered_rim'], 'ordered original rim')
    parent = OLD / 'frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/J1/certificate.json'
    raw = parent.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == caps['parent_C10_sha256'], 'parent C10 SHA256')
    parent_live = set(json.loads(raw)['final_live'])
    ten_index = {t:i for i,t in enumerate(states(10))}
    rebuilt_capzero, rebuilt_inherited, rebuilt_zero = [], [], []
    for i,t in enumerate(all_states):
        a,n,u4,u3,u2,u1,L,q,c,s,v,w,tlast = t
        forbidden = sum(1 << x for x in set((n,u4,u3,u2,u1,L)))
        expected, sector = caps_for(a,n,L,q,c,s,v,w,tlast,forbidden)
        for name in ('G','Q1','J1'):
            require(all(caps['matrices'][name][row][i] == expected[name][row] for row in range(10)), 'full-star cap mismatch at state '+str(i))
        require(all(caps['sectors'][j][i] == sector[j] for j in range(2)), 'sector cap mismatch at state '+str(i))
        bad = any(expected['G'][j] for j in (1,4,6)) or expected['Q1'][9] or any(expected['J1'][j] for j in (4,6))
        badR = [R for R in range(4) if not (forbidden & (1 << R)) and ten_index[canonical((a,n,R,L,q,c,s,v,w,tlast))] not in parent_live]
        if bad:
            rebuilt_capzero.append(i)
        if badR:
            rebuilt_inherited.append([i,badR])
        if bad or badR:
            rebuilt_zero.append(i)
    require(rebuilt_capzero == caps['cap_zero'], 'cap zero set mismatch')
    require(rebuilt_inherited == caps['inherited_C10_zero_R_lifts'], 'inherited zero R lifts mismatch')
    require(rebuilt_zero == caps['initial_zero'], 'initial zero set mismatch')
    require(len(rebuilt_zero) == 5098 and len(rebuilt_capzero) == 2942, 'zero counts')
    initial_live = set(range(len(all_states))) - set(rebuilt_zero)
    require(sorted(initial_live) == caps['initial_live'], 'initial live set mismatch')
    rowids = rebuild_rowmap(all_states)
    require(sorted(map(list,rowids.items())) == orbit['rowids'], 'full half-row-to-state map mismatch')
    require(digest(orbit['rowids']) == orbit['rowids_sha256'], 'row map canonical digest')
    require(orbit['coefficients_per_row'] == 4 and orbit['full_half_row_size'] == 8, 'orbit multiplicity normalization must be 8Z=4sumX')
    require(len(orbit['columns']) == 307197, 'surviving column count')
    require(digest(orbit['columns']) == orbit['live_columns_sha256'], 'live columns canonical digest')
    removed = set()
    for round_ in orbit['rounds']:
        require(round_ == sorted(set(round_)), 'closure round not sorted unique')
        require(not (removed & set(round_)), 'closure removal repeated')
        removed.update(round_)
    live = initial_live - removed
    require(len(removed) == 24 and len(live) == 61308, 'support closure state counts')
    require(sorted(live) == orbit['live'], 'final live set mismatch')
    active_rows = {r for r,i in rowids.items() if i in live}
    require(len(active_rows) == 183924, 'active half-row count')
    covered = set()
    previous = None
    incidence_count = 0
    for j,col in enumerate(orbit['columns']):
        require(col and col == sorted(set(col)), 'column row IDs not sorted unique at '+str(j))
        require(previous is None or previous < col, 'columns not sorted unique')
        require(all(integer(r) and r in active_rows for r in col), 'column touches zero or unknown state at '+str(j))
        covered.update(col)
        incidence_count += len(col)
        previous = col
    require(covered == active_rows, 'final live half-row without a surviving column')
    require(incidence_count + len(active_rows) == 4448132, 'equality nnz count')
    witnesses = []
    index = {t:i for i,t in enumerate(all_states)}
    for e0,e1 in ((0,1),(1,0)):
        t = (0,1,2,1,2,1,2,3,1,2,e0,e1,2)
        witnesses.append(index[canonical(t)])
    require(witnesses == [44459,44466], 'target canonical IDs')
    require([w['canonical_id'] for w in caps['witnesses']] == witnesses, 'frozen target IDs')
    require(all(i in live for i in witnesses), 'target deleted by closure')
    positives = [caps['matrices']['G'][j] for j in POS_ROWS] + caps['sectors']
    target = [int(i in witnesses) for i in range(len(all_states))]
    positives.append(target)
    return dict(caps=caps, orbit=orbit, states=all_states, live=live,
                rows=rowids, active_rows=active_rows, positives=positives,
                witnesses=witnesses, nnz=incidence_count+len(active_rows))


def sparse_vector(data, key, allowed, signed=False):
    require(key in data and type(data[key]) is list, 'missing sparse vector '+key)
    result = {}
    previous = -1
    for rec in data[key]:
        require(type(rec) is list and len(rec) == 2, 'invalid sparse entry in '+key)
        i,value = rec
        require(integer(i) and i in allowed, 'unknown or forbidden coordinate in '+key)
        require(integer(value) and value != 0 and (signed or value > 0), 'noninteger, zero, or negative coefficient in '+key)
        require(i > previous, 'unsorted or duplicate coordinates in '+key)
        result[i] = value
        previous = i
    return result


def check_certificate(model, data):
    require(type(data) is dict, 'certificate must be an object')
    if 'base' in data:
        require(data['base'] == BASE, 'certificate BASE mismatch')
    if 'input_sha256' in data:
        require(data['input_sha256'] == SHA, 'certificate input digest mismatch')
    kind = data.get('kind','primal')
    require(kind in ('primal','dual'), 'unknown certificate kind')
    if kind == 'primal':
        z = sparse_vector(data,'z',model['live'])
        x = sparse_vector(data,'x',range(len(model['orbit']['columns'])))
        totals = defaultdict(int)
        for j,value in x.items():
            for row in model['orbit']['columns'][j]:
                totals[row] += value
        for row in sorted(model['active_rows']):
            require(2*z.get(model['rows'][row],0) == totals.get(row,0), 'orbit equality fails at half-row '+str(row))
        quantities = [sum(P[i]*value for i,value in z.items()) for P in model['positives']]
        require(all(value > 0 for value in quantities), 'joint strict positivity fails: '+str(quantities))
        return dict(status='PASS',certificate='exact integer primal',nonzero_z=len(z),
                    nonzero_x=len(x),max_z=max(z.values()),max_x=max(x.values()),
                    positive_quantities=dict(zip(LABELS,quantities)),
                    checked_equalities=len(model['active_rows']),source_excluded=False,
                    source_exclusion_scope=SCOPE,general_J1_excluded=False,general_five_edge_excluded=False,
                    source_realized=False,necessary_cone='FEASIBLE')
    y = sparse_vector(data,'y',model['active_rows'],signed=True)
    lam = data.get('lambda')
    require(type(lam) is list and len(lam) == 10 and all(integer(x) and x >= 0 for x in lam), 'lambda must be ten nonnegative integers')
    require(sum(lam) > 0, 'dual must use at least one mandatory positive quantity')
    state_totals = defaultdict(int)
    for row,value in y.items():
        state_totals[model['rows'][row]] += 2*value
    min_z_slack = None
    for i in sorted(model['live']):
        rhs = sum(lam[j]*model['positives'][j][i] for j in range(10))
        slack = state_totals.get(i,0)-rhs
        require(slack >= 0, 'dual Z inequality fails at state '+str(i))
        min_z_slack = slack if min_z_slack is None else min(min_z_slack,slack)
    max_column_pairing = None
    for j,col in enumerate(model['orbit']['columns']):
        pairing = sum(y.get(row,0) for row in col)
        require(pairing <= 0, 'dual X inequality fails at column '+str(j))
        max_column_pairing = pairing if max_column_pairing is None else max(max_column_pairing,pairing)
    return dict(status='PASS',certificate='exact integer dual',nonzero_y=len(y),
                lambda_=dict(zip(LABELS,lam)),min_z_slack=min_z_slack,
                max_column_pairing=max_column_pairing,source_excluded=True,
                source_exclusion_scope=SCOPE,general_J1_excluded=False,general_five_edge_excluded=False,
                source_realized=False,necessary_cone='INFEASIBLE')


def negative_controls(model, cert):
    tests = {}
    candidates = []
    if cert.get('kind','primal') == 'primal':
        bad = deepcopy(cert); bad['z'][0][1] += 1
        candidates.append(('one_z_integer_changed',bad))
        bad = deepcopy(cert); bad['x'][0][1] += 1
        candidates.append(('one_x_integer_changed',bad))
        bad = deepcopy(cert); bad['z'] = [r for r in bad['z'] if r[0] not in model['witnesses']]
        candidates.append(('all_target_z_removed',bad))
        bad = deepcopy(cert); bad['z'][0][1] = -1
        candidates.append(('negative_coordinate',bad))
        bad = deepcopy(cert); bad['z'][0][1] = 1.0
        candidates.append(('float_coordinate',bad))
        bad = deepcopy(cert); bad['z'].insert(0,bad['z'][0][:])
        candidates.append(('duplicate_coordinate',bad))
    else:
        bad = deepcopy(cert); bad['lambda'] = [0]*10
        candidates.append(('zero_dual_lambda',bad))
        bad = deepcopy(cert); bad['lambda'][0] = -1
        candidates.append(('negative_dual_lambda',bad))
        bad = deepcopy(cert)
        row = min(model['active_rows'])
        magnitude = 1 + sum(abs(v) for _,v in bad['y'])
        vals = dict(bad['y']); vals[row] = -magnitude
        bad['y'] = [list(r) for r in sorted(vals.items()) if r[1]]
        candidates.append(('violated_z_side',bad))
        bad = deepcopy(cert)
        row = model['orbit']['columns'][0][0]
        magnitude = 1 + sum(abs(v) for _,v in bad['y'])
        vals = dict(bad['y']); vals[row] = magnitude
        bad['y'] = [list(r) for r in sorted(vals.items()) if r[1]]
        candidates.append(('violated_column_side',bad))
    for name,bad in candidates:
        try:
            check_certificate(model,bad)
        except Rejected as exc:
            tests[name] = dict(status='REJECTED',reason=str(exc))
        else:
            raise Rejected('negative control unexpectedly passed: '+name)
    return tests


def malformed_controls(model):
    tests = {}
    candidates = [
        ('zero_primal', {'z': [], 'x': []}),
        ('zero_dual', {'kind': 'dual', 'y': [], 'lambda': [0]*10}),
        ('noninteger_dual', {'kind': 'dual', 'y': [], 'lambda': [1.0]+[0]*9}),
        ('unknown_kind', {'kind': 'unsupported', 'z': [], 'x': []}),
        ('wrong_base', {'base': '0'*40, 'z': [], 'x': []}),
        ('wrong_input_hash', {'input_sha256': {}, 'z': [], 'x': []}),
        ('coordinate_of_zero_fibre', {'z': [[min(set(range(66430))-model['live']),1]], 'x': []}),
        ('out_of_range_column', {'z': [], 'x': [[len(model['orbit']['columns']),1]]}),
    ]
    for name,bad in candidates:
        try:
            check_certificate(model,bad)
        except Rejected as exc:
            tests[name] = dict(status='REJECTED',reason=str(exc))
        else:
            raise Rejected('malformed control unexpectedly passed: '+name)
    return tests


def model_controls(model):
    tests = {}
    mutations = [
        ('one_cap_integer_changed', 'caps.json.gz', lambda o: o['matrices']['G'][0].__setitem__(0,o['matrices']['G'][0][0]+1)),
        ('one_column_row_integer_changed', 'orbits.json.gz', lambda o: o['columns'][0].__setitem__(0,o['columns'][0][0]+1)),
        ('orbit_entry_multiplicity_4_to_5', 'orbits.json.gz', lambda o: o.__setitem__('coefficients_per_row',5)),
        ('one_column_removed', 'orbits.json.gz', lambda o: o['columns'].pop()),
    ]
    for name,source,mutate in mutations:
        altered = deepcopy(model['caps' if source.startswith('caps') else 'orbit'])
        mutate(altered)
        raw = gzip.compress(packed(altered)+b'\n',mtime=0)
        try:
            decode_pinned(source,raw)
        except Rejected as exc:
            tests[name] = dict(status='REJECTED',reason=str(exc),altered_sha256=hashlib.sha256(raw).hexdigest())
        else:
            raise Rejected('model mutation unexpectedly passed: '+name)
    return tests


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--certificate',type=Path)
    ap.add_argument('--controls',action='store_true')
    ap.add_argument('--malformed-controls',action='store_true')
    ap.add_argument('--model-controls',action='store_true')
    ap.add_argument('--seed',type=int)
    ap.add_argument('--output',type=Path)
    args = ap.parse_args()
    started = time.monotonic()
    try:
        model = load_model()
        report = dict(status='PASS',base=BASE,input_sha256=SHA,
                      states=len(model['states']),initial_zero=5098,support_closure_zero=24,
                      live_states=len(model['live']),half_rows=len(model['rows']),
                      active_half_rows=len(model['active_rows']),columns=len(model['orbit']['columns']),
                      equality_nnz=model['nnz'],positive_labels=LABELS,
                      source_exclusion_scope=SCOPE,general_J1_excluded=False,general_five_edge_excluded=False,
                      cap_matrices_rebuilt_from_original_edges=True,
                      half_rows_rebuilt_from_palette_symmetries=True,
                      full_orbit_family_regenerated=False)
        if args.seed is not None:
            # Change all certificate summation traversal orders without changing IDs.
            rng = random.Random(args.seed)
            order = list(model['rows'].items()); rng.shuffle(order)
            model['rows'] = dict(order)
            col_order = model['orbit']['columns']
            for col in col_order:
                rng.shuffle(col)
            report['permutation_seed'] = args.seed
        if args.certificate:
            cert_raw = args.certificate.read_bytes()
            cert = json.loads(cert_raw)
            report['certificate_sha256'] = hashlib.sha256(cert_raw).hexdigest()
            report['result'] = check_certificate(model,cert)
            if args.controls:
                report['negative_controls'] = negative_controls(model,cert)
        else:
            require(not args.controls, '--controls requires --certificate')
        if args.malformed_controls:
            report['malformed_controls'] = malformed_controls(model)
        if args.model_controls:
            report['model_controls'] = model_controls(model)
        report['seconds'] = round(time.monotonic()-started,6)
    except (Rejected,KeyError,IndexError,TypeError,ValueError,OSError) as exc:
        report = dict(status='FAIL',reason=str(exc),seconds=round(time.monotonic()-started,6))
    raw = json.dumps(report,sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.write_text(raw)
    print(raw,end='')
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
