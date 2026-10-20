#!/usr/bin/env python3
"""Rebuild a W7/three-private-point disk and exact residual/cap controls; stdlib."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
FROZEN = AUDIT / 'frozen'
BASE = '417732fc5ef0a012829fd6712333b1c906128d3a'
SOURCE = 'audits/2026-10-20-kempe-residual-iteration-af0df80/frozen/audits/2026-10-20-multi-kempe-machines-af0df80/experiment/certificate.json'
SOURCE_SHA = 'feed98beeb5f83e29bf9c690283aff5d768d4f1e8ba0504f0422560fddeea6dc'
V = ('n','h','L','u1','u2','u3','u4','R','d2','d3','d4','k5','k6','k7')
B = ('n','h','d4','d3','d2','L','u1','u2','u3','u4')
PAIRS = tuple(combinations(range(4), 2))
WHEEL = ('n','h','L','u1','u2','u3','u4')
CELL = ('h','L','d2','d3','d4','k5','k6','k7')
CELL_FACES = ((0,1,7),(0,4,6),(0,5,6),(0,5,7),(1,2,7),
              (2,3,6),(2,5,6),(2,5,7),(3,4,6))


def encoded(v):
    return (json.dumps(v, sort_keys=True, separators=(',', ':')) + '\n').encode()


def digest(v):
    return sha256(encoded(v)).hexdigest()


def edge(a,b):
    return tuple(sorted((a,b)))


def graph():
    source = json.loads((FROZEN / SOURCE).read_text())
    assert sha256((FROZEN / SOURCE).read_bytes()).hexdigest() == SOURCE_SHA
    assert set(map(tuple, source['edges'])) == {
        edge(u,v) for f in CELL_FACES for u,v in combinations(f,2)}
    faces = [('R', WHEEL[i], WHEEL[(i+1)%7]) for i in range(7)]
    faces += [tuple(CELL[j] for j in f) for f in CELL_FACES]
    counts = Counter(edge(u,v) for f in faces for u,v in combinations(f,2))
    assert {e for e,k in counts.items() if k == 1} == {
        edge(B[i], B[(i+1)%len(B)]) for i in range(len(B))}
    assert all(k in (1,2) for k in counts.values())
    assert len(V)-len(counts)+len(faces) == 1
    # Each vertex link is one path (boundary) or one cycle (interior).
    for v in V:
        link = defaultdict(set)
        for f in faces:
            if v in f:
                x,y = [x for x in f if x != v]
                link[x].add(y); link[y].add(x)
        todo = set(link); seen = set(); stack = [min(todo)]
        while stack:
            x = stack.pop()
            if x in seen: continue
            seen.add(x); stack.extend(link[x]-seen)
        assert seen == todo
        degrees = sorted(map(len,link.values()))
        assert degrees == ([1,1]+[2]*(len(link)-2) if v in B else [2]*len(link))
    index = {v:i for i,v in enumerate(V)}
    adjacency = [set() for _ in V]
    for u,v in counts:
        adjacency[index[u]].add(index[v]); adjacency[index[v]].add(index[u])
    return faces, sorted(counts), adjacency


def enumerate_colors(adjacency, omitted=None):
    active = set(range(len(V))) - ({omitted} if omitted is not None else set())
    c = [-1]*len(V)
    result = []
    def visit(todo):
        if not todo:
            result.append(tuple(c)); return
        v = max(todo,key=lambda v:(len({c[w] for w in adjacency[v] if c[w]>=0}),len(adjacency[v]),-v))
        for k in range(4):
            if all(c[w] != k for w in adjacency[v]):
                c[v] = k; visit(todo-{v}); c[v] = -1
    visit(active)
    return tuple(sorted(result))


def components(c, pair, adjacency):
    todo = {v for v in range(len(V)) if c[v] in pair}
    out = []
    while todo:
        v = min(todo); todo.remove(v); block = {v}; stack = [v]
        while stack:
            for w in sorted(adjacency[stack.pop()] & todo):
                todo.remove(w); block.add(w); stack.append(w)
        out.append(frozenset(block))
    return tuple(out)


def swap(c, action, adjacency):
    i,j,root = action
    if c[root] not in (i,j): return None
    block = next(b for b in components(c,(i,j),adjacency) if root in b)
    return tuple((j if x == i else i) if v in block else x for v,x in enumerate(c))


def observe(c, adjacency):
    bi = tuple(V.index(v) for v in B)
    bs = set(bi)
    parts = tuple(tuple(sorted(tuple(sorted(b & bs)) for b in components(c,p,adjacency) if b & bs)) for p in PAIRS)
    return tuple(c[v] for v in bi), parts


def data():
    faces, edges, adj = graph()
    colors = enumerate_colors(adj)
    color_set = set(colors)
    obs = {c:observe(c,adj) for c in colors}
    fibres = defaultdict(set)
    for c in colors: fibres[obs[c]].add(c)
    actions = tuple((i,j,V.index(r)) for i,j in PAIRS for r in B)
    legal_edges = 0
    for c in colors:
        for a in actions:
            d = swap(c,a,adj)
            if d is None: continue
            assert d in color_set and swap(d,a,adj) == c
            legal_edges += 1
    # Independent whole-graph coloring versus delete-R and complete-star lifts.
    ri = V.index('R')
    core = enumerate_colors(adj, omitted=ri)
    lifted = set(); cap_records = []; base_counts = Counter(); completed_counts = Counter()
    for c in core:
        cap = tuple(k for k in range(4) if all(c[v] != k for v in adj[ri]))
        key = tuple(c[V.index(v)] for v in B)
        base_counts[key] += 1
        for k in cap:
            d = list(c); d[ri] = k; d = tuple(d)
            lifted.add(d); completed_counts[key] += 1
        cap_records.append((c,cap))
    assert lifted == color_set
    # Every proper literal outer rim is included, including empty full fibres.
    proper_rims = []
    def rim_visit(prefix):
        if len(prefix) == len(B):
            if prefix[-1] != prefix[0]: proper_rims.append(tuple(prefix))
            return
        for k in range(4):
            if not prefix or k != prefix[-1]: rim_visit(prefix+[k])
    rim_visit([])
    complete_rows = [(rim,base_counts[rim],completed_counts[rim]) for rim in proper_rims]
    assert sum(x[2] for x in complete_rows) == len(colors)
    # Literal local W7 colouring; the only variable coordinates are cell-private k5,k6,k7.
    fixed = {'n':1,'h':0,'L':2,'u1':1,'u2':2,'u3':1,'u4':2,'R':3,
             'd2':0,'d3':2,'d4':1}
    path_fibre = {c for c in colors if all(c[V.index(v)] == k for v,k in fixed.items())}
    seed = tuple(dict(fixed,k5=2,k6=3,k7=1)[v] for v in V)
    assert seed in path_fibre
    initial_o = obs[seed]
    initial = {c for c in path_fibre if obs[c] == initial_o}
    assert len(initial) > 1 and len({obs[c] for c in initial}) == 1
    assert fibres[initial_o] == initial
    a = (1,2,V.index('L'))
    transported = {swap(c,a,adj) for c in initial}
    branches = defaultdict(set)
    for c in transported: branches[obs[c]].add(c)
    assert len(branches) > 1 and sum(map(len,branches.values())) == len(initial)
    selected_o = obs[swap(min(initial),a,adj)]
    r1 = branches[selected_o]
    r2 = {swap(c,a,adj) for c in r1 if obs[swap(c,a,adj)] == initial_o}
    assert r2 and r2 < initial
    # Origin/current pairs, and inverse replay, are the independent reference.
    anchored = {c:swap(c,a,adj) for c in initial if obs[swap(c,a,adj)] == selected_o}
    assert set(anchored.values()) == r1 and set(anchored) == r2
    assert all(swap(current,a,adj) == origin for origin,current in anchored.items())
    third_o = next(o for o in sorted(branches) if o != selected_o)
    r3 = {swap(c,a,adj) for c in r2 if obs[swap(c,a,adj)] == third_o}
    assert not r3
    assert {swap(c,a,adj) for c in initial if obs[swap(c,a,adj)] == third_o}
    # Exact sparse integer transport: no collision, no duplicate counts.
    assert len({swap(c,a,adj) for c in initial}) == len(initial)
    assert sum(len({swap(c,a,adj) for c in initial if obs[swap(c,a,adj)] == o}) for o in branches) == len(initial)
    assert not {c for c in initial if obs[c] == selected_o}  # mask without transport is wrong.
    assert not initial <= transported  # current sets do not nest; origin sets do.
    # Replacing the carried set by its full observation fibre can resurrect an origin.
    refill_control = None
    for o,rs in sorted(branches.items()):
        extra = fibres[o]-rs
        if not extra: continue
        for bad_current in sorted(extra):
            returned = swap(bad_current,a,adj)
            if returned is not None and returned not in initial:
                refill_control = {'observation':o,'true_current':sorted(rs),
                                  'refilled_extra':bad_current,'reverse_origin':returned}
                break
        if refill_control: break
    # A stronger control searches another observation class if this initial fibre has no refill.
    if refill_control is None:
        for o,group in sorted(fibres.items()):
            for action in actions:
                targets = {swap(c,action,adj) for c in group}
                targets.discard(None)
                for d in sorted(targets):
                    rs = {e for e in targets if obs[e] == obs[d]}
                    extra = fibres[obs[d]]-rs
                    if extra:
                        e = min(extra)
                        refill_control = {'initial':sorted(group),'action':action,'observation':obs[d],
                                          'true_current':sorted(rs),'refilled_extra':e,
                                          'reverse_origin':swap(e,action,adj)}
                        break
                if refill_control: break
            if refill_control: break
    assert refill_control is not None
    # Different monitors may not borrow different full colorings.
    target_list = sorted(transported)
    mixed = None
    opts = [sorted({obs[d][1][j] for d in transported}) for j in range(6)]
    for parts in product(*opts):
        o = (obs[target_list[0]][0],parts)
        if all(obs[d] != o for d in transported):
            mixed = o; break
    assert mixed is not None
    assert all(any(obs[d][1][j] == mixed[1][j] for d in transported) for j in range(6))
    illegal = (0,3,V.index('n'))
    assert all(swap(c,illegal,adj) is None for c in initial)
    # Cap compatibility is an extra obligation: core Kempe and completed Kempe need not commute.
    incompatible = None
    for c in colors:
        base = list(c); base[ri] = -1; base = tuple(base)
        for action in actions:
            d = swap(c,action,adj)
            e = swap(base,action,adj)
            if d is None or e is None: continue
            restricted = list(d); restricted[ri] = -1; restricted = tuple(restricted)
            if restricted != e:
                incompatible = {'full_before':c,'action':action,'full_after':d,
                                'restrict_full_after':restricted,'core_after':e,
                                'old_cap_size':sum(all(base[v]!=k for v in adj[ri]) for k in range(4)),
                                'new_cap_size':sum(all(e[v]!=k for v in adj[ri]) for k in range(4))}
                if incompatible['old_cap_size'] != incompatible['new_cap_size']: break
        if incompatible and incompatible['old_cap_size'] != incompatible['new_cap_size']: break
    assert incompatible and incompatible['old_cap_size'] != incompatible['new_cap_size']
    missing_neighbor = None
    for c in core:
        for k in range(4):
            if c[V.index('u3')] == k and all(c[v] != k for v in adj[ri]-{V.index('u3')}):
                missing_neighbor = {'core':c,'false_R':k,'omitted_edge':['R','u3']}; break
        if missing_neighbor: break
    assert missing_neighbor
    # Fixed-literal selected histories do not obey the full source's global S4 symmetry.
    rim = initial_o[0]
    permuted_rim = tuple(1 if k == 0 else 0 if k == 1 else k for k in rim)
    assert completed_counts[rim] == completed_counts[permuted_rim] > 0
    selected_rim_count = sum(tuple(c[V.index(v)] for v in B) == rim for c in initial)
    selected_permuted_count = sum(tuple(c[V.index(v)] for v in B) == permuted_rim for c in initial)
    assert selected_rim_count > 0 and selected_permuted_count == 0
    # This initial selected fibre is not the entire source coloring vector or invariant under actions.
    assert any(d not in initial for d in transported)
    return {
        'base':BASE,'status':'exact general transport; finite local disk controls; J1 source exclusion OPEN',
        'graph':{'vertices':V,'ordered_boundary':B,'faces':faces,'edges':edges,
                 'source_edges_sha256':SOURCE_SHA,'scope':'local W7 glued along hL to an independently rebuilt eight-vertex disk; not a complete J1 source'},
        'full_colorings':len(colors),'full_colorings_sha256':digest(colors),
        'observation_classes':len(fibres),'fibre_size_histogram':sorted(Counter(map(len,fibres.values())).items()),
        'legal_partial_involution_checks':legal_edges,'rooted_actions':len(actions),
        'full_R_cap':{'base_colorings':len(core),'cap_records_sha256':digest(cap_records),
                      'proper_literal_boundary_rows':len(complete_rows),'empty_completed_rows':sum(x[2]==0 for x in complete_rows),
                      'complete_rows_sha256':digest(complete_rows),'whole_graph_lift_equality':True},
        'five_edge_control':{'fixed_literal_colors':fixed,'initial':sorted(initial),'action':a,
                             'initial_observation':initial_o,'first_observation':selected_o,
                             'r1':sorted(r1),'r2':sorted(r2),'third_observation':third_o,'r3':sorted(r3),
                             'origin_current_pairs':sorted(anchored.items()),
                             'branch_sizes':sorted(len(v) for v in branches.values())},
        'negative_controls':{
            'drop_middle_mask':{'exact_return':sorted(r2),'incorrect_parity_return':sorted(initial)},
            'mask_without_transport':{'incorrect_count':0,'exact_count':len(r1)},
            'refill_full_observation_fibre':refill_control,
            'mix_monitor_witnesses':{'false_joint_observation':mixed,'exact_count':0,
                                   'each_coordinate_has_some_witness':True},
            'illegal_action_as_loop':{'action':illegal,'exact_count':0,'incorrect_loop_count':len(initial)},
            'omit_complete_R_neighbor':missing_neighbor,
            'assume_cap_commutes':incompatible,
            'selected_fibre_as_full_source':{'selected_count':len(initial),'full_count':len(colors),
                                           'selected_set_preserved_by_action':False,
                                           'boundary':rim,'global_0_1_swap_boundary':permuted_rim,
                                           'whole_source_literal_counts':[completed_counts[rim],completed_counts[permuted_rim]],
                                           'selected_literal_counts':[selected_rim_count,selected_permuted_count]}},
        'scope':{'real_J1_source_realized':False,'general_fibre_bound':False,
                 'source_excluded':False,'smaller_bad':False,'new_Lean':False}}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--build',action='store_true')
    p.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args = p.parse_args()
    actual = json.loads(encoded(data()))
    if args.build:
        with args.certificate.open('xb') as f: f.write(encoded(actual))
    else:
        assert json.loads(args.certificate.read_text()) == actual, 'certificate mismatch'
    print(json.dumps({k:actual[k] for k in ('status','full_colorings','observation_classes','legal_partial_involution_checks','full_R_cap')}))

if __name__ == '__main__': main()
