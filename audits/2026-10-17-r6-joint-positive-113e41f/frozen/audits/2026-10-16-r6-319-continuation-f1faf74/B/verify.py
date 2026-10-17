#!/usr/bin/env python3
"""Full finite pentagon interface and same-graph shortcut calibration."""
import argparse
import hashlib
import itertools
import json
import random
from collections import defaultdict
from pathlib import Path

BASE = 'f1faf743833c51ddc5efbe9e0f390b87b9f2311d'


def components(vertices, ids, edges):
    adj = {v: set() for v in vertices}
    for i in ids:
        a, b = edges[i]
        adj[a].add(b)
        adj[b].add(a)
    out, unseen = [], set(vertices)
    while unseen:
        todo, seen = [min(unseen)], set()
        while todo:
            u = todo.pop()
            if u in seen:
                continue
            seen.add(u)
            todo.extend(adj[u] - seen)
        unseen -= seen
        out.append(sorted(seen))
    return out


def matchings(vertices, edges, rng):
    at = defaultdict(list)
    for i, (a, b) in enumerate(edges):
        at[a].append((b, i))
        at[b].append((a, i))
    for row in at.values():
        rng.shuffle(row)
    out = []
    def run(left, chosen):
        if not left:
            out.append(sorted(chosen))
            return
        a = min(left)
        for b, i in at[a]:
            if b in left:
                run(left - {a, b}, chosen + [i])
    run(set(vertices), [])
    return sorted(out)


def colours(vertices, edges, rng):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    tie = {v: rng.random() for v in vertices}
    order = sorted(vertices, key=lambda v: (-len(adj[v]), tie[v]))
    out, partial = [], {}
    def run(j):
        if j == len(order):
            out.append([partial[v] for v in vertices])
            return
        a = order[j]
        forbidden = {partial[b] for b in adj[a] if b in partial}
        for c in range(4):
            if c not in forbidden:
                partial[a] = c
                run(j + 1)
        partial.pop(a, None)
    run(0)
    return sorted(out)


def ring_order(ids, edges):
    adj = defaultdict(list)
    for i in ids:
        a, b = edges[i]
        adj[a].append(b)
        adj[b].append(a)
    assert all(len(x) == 2 for x in adj.values())
    start = min(adj)
    prev, cur = start, min(adj[start])
    ring = [start]
    while cur != start:
        assert cur not in ring
        ring.append(cur)
        prev, cur = cur, next(v for v in adj[cur] if v != prev)
    assert len(ring) == len(adj)
    return ring


def local_interface():
    cyc = [(i, (i+1) % 5) for i in range(5)]
    rows = []
    for mask in range(32):
        selected = [i for i in range(5) if mask >> i & 1]
        fillings = []
        for internal in range(32):
            ids = [i for i in range(5) if internal >> i & 1]
            deg = [int(i in selected) for i in range(5)]
            for i in ids:
                a, b = cyc[i]
                deg[a] += 1
                deg[b] += 1
            if deg != [1]*5:
                continue
            comp = components(range(5), set(range(5))-set(ids), cyc)
            strands = []
            for vs in comp:
                port = sorted(set(vs)-set(selected))
                length = sum(a in vs and b in vs for j,(a,b) in enumerate(cyc) if j not in ids)
                assert len(port) in (0,2)
                strands.append({'vertices': vs, 'open_ports': port, 'length': length})
            fillings.append({'internal_matching': ids, 'complement_strands': strands})
        rows.append({'selected_ports': selected, 'fillings': fillings})
    assert sum(bool(r['fillings']) for r in rows) == 11
    assert all(len(r['fillings']) <= 1 for r in rows)
    assert sum(bool(r['fillings']) and len(r['selected_ports']) == 1 for r in rows) == 5
    assert sum(bool(r['fillings']) and len(r['selected_ports']) == 3 for r in rows) == 5
    tait = []
    for internal in itertools.product((1,2,3), repeat=5):
        if any(internal[i-1] == internal[i] for i in range(5)):
            continue
        ports = [({1,2,3}-{internal[i-1],internal[i]}).pop() for i in range(5)]
        assert sorted(ports.count(c) for c in (1,2,3)) == [1,1,3]
        alpha = [i for i,c in enumerate(internal) if c == 1]
        transitions = [i for i in alpha if ports[i] != ports[(i+1)%5]]
        assert len(transitions) == 1
        tait.append({'internal_colours': list(internal), 'port_colours': ports,
                     'alpha_ports': [i for i,c in enumerate(ports) if c == 1],
                     'sole_transition': transitions[0]})
    assert len(tait) == 30
    return {'all_32_port_fibres_including_empty': rows, 'all_30_complete_local_Tait_colourings': tait}


def reconstruct(graph, rng):
    pv = graph['J_vertices']
    pe = [tuple(e) for e in graph['J_edges']]
    faces = graph['J_faces']
    at = defaultdict(list)
    for fi, face in enumerate(faces):
        for a,b in zip(face, face[1:]+face[:1]):
            at[tuple(sorted((a,b)))].append(fi)
    assert set(at) == set(pe)
    assert all(len(v)==2 for v in at.values())
    de = [tuple(sorted(at[e])) for e in pe]
    dv = list(range(len(faces)))
    all_ids = set(range(len(de)))
    assert all(sum(v in e for e in de) == 3 for v in dv)
    pms = matchings(dv,de,rng)
    pmset = {tuple(m) for m in pms}
    cols = colours(pv,pe,rng)
    pi = {v:i for i,v in enumerate(pv)}
    differences = [[c[pi[a]] ^ c[pi[b]] for a,b in pe] for c in cols]
    fibres = defaultdict(list)
    for ci,row in enumerate(differences):
        fibres[tuple(i for i,c in enumerate(row) if c==1)].append(ci)
    rows, even = [], []
    for matching in pms:
        cs = components(dv,all_ids-set(matching),de)
        omega = sum(len(c)%2 for c in cs)
        fibre = fibres[tuple(matching)]
        assert len(fibre) == (4*2**len(cs) if omega==0 else 0)
        if omega == 0:
            even.append(matching)
        rows.append({'matching':matching,'complement_cycles':cs,'oddness':omega,
                     'complete_fixed_alpha_colour_fibre':fibre})
    assert set(fibres) == pmset
    # Every primal degree-five vertex supplies its literal dual facial pentagon.
    pentagons = []
    for u in pv:
        ids = {i for i,(a,b) in enumerate(pe) if u in (a,b)}
        if len(ids) != 5:
            continue
        ring = ring_order(ids,de)
        cut = {i for i,(a,b) in enumerate(de) if (a in ring) != (b in ring)}
        assert len(cut)==5
        assert all(sum(v in de[i] for i in cut)==1 for v in ring)
        pentagons.append((u,ids,ring,cut))
    shortcuts, cap_counts = [], defaultdict(int)
    for m0 in even:
        old = set(m0)
        for n in pms:
            delta = old ^ set(n)
            if not delta:
                continue
            used = {v for i in delta for v in de[i]}
            if len(components(used,delta,de)) != 1:
                continue
            for u,internal,ring,cut in pentagons:
                if not cut <= set(n):
                    continue
                k = len(cut & old)
                assert k in (1,3)
                cap_counts[k] += 1
                assert delta & cut == cut-old
                assert delta & internal == old & internal
                if k==3:
                    assert len(old & internal)==1
                    continue
                assert len(old & internal)==2
                port0 = next(iter(cut & old))
                v0 = next(v for v in ring if v in de[port0])
                j = ring.index(v0)
                r = ring[j:]+ring[:j]
                a1 = next(i for i in internal if set(de[i])=={r[1],r[2]})
                a2 = next(i for i in internal if set(de[i])=={r[3],r[4]})
                chord = next(i for i in internal if set(de[i])=={r[2],r[3]})
                assert {a1,a2} == old & internal
                rest = delta-{a1,a2}
                parts = components(used,rest,de)
                arc_vertices = next(vs for vs in parts if r[2] in vs)
                assert r[3] in arc_vertices and r[1] not in arc_vertices and r[4] not in arc_vertices
                arc = {i for i in rest if de[i][0] in arc_vertices}
                qprime = (delta-arc)|{chord}
                assert len(qprime)<len(delta)
                assert tuple(sorted(old ^ qprime)) in pmset
                qpv = {v for i in qprime for v in de[i]}
                assert len(components(qpv,qprime,de)) == 1
                # Every root edge outside the dropped arc is retained by the shortcut.
                roots = sorted((delta & old)-internal)
                retained = sorted(set(roots)-arc)
                assert set(retained) <= qprime
                shortcuts.append({'M0':m0,'endpoint':n,'cap_centre':u,'pentagon_order':r,
                                  'Q':sorted(delta),'discarded_external_arc':sorted(arc),
                                  'literal_shortcut_edge':chord,'shorter_Q':sorted(qprime),
                                  'eligible_root_edges':roots,'retained_root_edges':retained})
    return {'name':graph['name'],'source':'not triggered','primal_edges':graph['J_edges'],
            'dual_edges':[list(e) for e in de],'all_complete_J_colourings':cols,
            'all_matching_rows':rows,'single_Q_odd_pentagon_cases':
            [{'M0_selected_ports':k,'checks':v} for k,v in sorted(cap_counts.items())],
            'all_one_port_shortcuts':shortcuts}


def main():
    parser=argparse.ArgumentParser()
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output',type=Path)
    mode.add_argument('--check',type=Path)
    parser.add_argument('--seed',type=int,default=0)
    args=parser.parse_args()
    inp=Path(__file__).with_name('input_controls.json')
    rng=random.Random(args.seed)
    result={'BASE':BASE,'authority':'source not triggered; exact local interface and finite controls',
            'input_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
            'pentagon_interface':local_interface(),
            'controls':[reconstruct(g,rng) for g in json.loads(inp.read_text())]}
    # A fixed, disjoint-mark negative calibration: a shortest legal Q may
    # still create an odd pentagon, and its only local shortcut removes f.
    control = next(g for g in result['controls'] if g['name']=='flipped_icosahedral_return')
    m0 = {2,5,9,10,15,19,20,26,28,29}
    q = {0,7,9,10,14,15,16,18,19,20,22,24,28,29}
    e,f,g = 2,20,5
    assert len(set(control['primal_edges'][e]+control['primal_edges'][f]+control['primal_edges'][g]))==6
    feasible=[]
    for row in control['all_matching_rows']:
        d=m0 ^ set(row['matching'])
        if f not in d or d & {e,g}:
            continue
        vs={v for i in d for v in control['dual_edges'][i]}
        if len(components(vs,d,control['dual_edges']))==1:
            feasible.append(d)
    assert q in feasible and min(map(len,feasible))==len(q)==14
    trace=next(s for s in control['all_one_port_shortcuts']
               if set(s['M0'])==m0 and set(s['Q'])==q and s['cap_centre']==9)
    assert f in trace['discarded_external_arc'] and f not in trace['shorter_Q']
    endpoint=next(r for r in control['all_matching_rows'] if set(r['matching'])==m0 ^ q)
    assert endpoint['oddness']==2 and not endpoint['complete_fixed_alpha_colour_fibre']
    result['shortest_Q_negative_calibration']={
        'control':control['name'],'marks':[e,f,g], 'M0':sorted(m0),'Q':sorted(q),
        'minimum_legal_Q_length':14,'all_legal_single_Qs':[sorted(x) for x in sorted(feasible,key=sorted)],
        'odd_endpoint':endpoint,'pentagon_shortcut':trace,
        'scope':'a shortest legal Q can have oddness two; this is not a source counterexample'}
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result,stream,sort_keys=True,indent=2)
            stream.write('\n')
    elif json.loads(args.check.read_text())!=result:
        raise SystemExit('FAIL: candidate differs from independent complete reconstruction')
    print(json.dumps({'status':'PASS','local_port_fibres':32,'nonempty_port_fibres':11,
                      'complete_local_Tait_rows':30,'controls':[
                          {'name':c['name'],'PMs':len(c['all_matching_rows']),
                           'complete_J_colourings':len(c['all_complete_J_colourings']),
                           'cap_cases':c['single_Q_odd_pentagon_cases'],
                           'shortcuts':len(c['all_one_port_shortcuts'])} for c in result['controls']]}))


if __name__=='__main__':
    main()
