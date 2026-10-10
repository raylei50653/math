#!/usr/bin/env python3
"""Independent finite audit: static-order coloring from frozen original edges.

No worker module imports. This checks only the supplied 23 graphs and 11 whole-U
derivatives. It neither constructs graphs nor searches a family of sources.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HOME = Path(__file__).resolve().parent
PC = HOME / 'inputs/pc'
COLORS = set(range(4))
PAIRS = list(product(range(4), repeat=2))


def encode(x):
    return (json.dumps(x, sort_keys=True, indent=2) + '\n').encode()


def load(p):
    return json.loads(p.read_text())


def expect(condition, why):
    if not condition:
        raise AssertionError(why)


def read_patterns():
    result = []
    for coloring in product(range(4), repeat=5):
        if coloring[0] or any(coloring[i] == coloring[(i+1)%5] for i in range(5)):
            continue
        if all(coloring[i] <= 1 + max(coloring[:i]) for i in range(1, 5)):
            result.append(list(coloring))
    expect(len(result) == 10, 'proper restricted-growth C5 pattern count')
    return result


PATTERNS = read_patterns()


def edges(es):
    return sorted(tuple(sorted(e)) for e in es)


def adjacency(vs, es):
    return {v: {w for a, b in es for w in ([b] if a == v else [a] if b == v else [])} for v in vs}


def components(vs, es):
    left, result = set(vs), []
    adj = adjacency(left, [e for e in es if set(e) <= left])
    while left:
        found, frontier = set(), {min(left)}
        while frontier:
            found |= frontier
            frontier = set().union(*(adj[v] for v in frontier)) - found
        left -= found
        result.append(sorted(found))
    return result


def bridge_list(vs, es):
    n = len(components(vs, es))
    return [list(e) for e in es if len(components(vs, [f for f in es if f != e])) > n]


def enumerate_colors(vs, es, pins, one=False):
    """Fixed degree order, unlike the worker's dynamic MRV solver."""
    adj = adjacency(vs, es)
    assigned = dict(pins)
    if any(assigned[a] == assigned[b] for a, b in es if a in assigned and b in assigned):
        return []
    todo = sorted(set(vs) - set(pins), key=lambda v: (-len(adj[v]), v))
    answer = []

    def visit(i):
        if i == len(todo):
            answer.append([assigned[v] for v in vs])
            return one
        v = todo[i]
        for c in range(4):
            if any(assigned.get(w) == c for w in adj[v]):
                continue
            assigned[v] = c
            stop = visit(i+1)
            del assigned[v]
            if stop:
                return True
        return False

    visit(0)
    return sorted(answer)


def legal(vs, es, pins, lift):
    expect(len(lift) == len(vs) and all(type(c) is int and c in COLORS for c in lift), 'full lift shape/colors')
    f = dict(zip(vs, lift))
    expect(all(f[v] == c for v, c in pins.items()), 'literal pins')
    expect(all(f[a] != f[b] for a, b in es), 'original-edge witness inequality')
    return f


def rotation_faces(vs, es, rot):
    adj = adjacency(vs, es)
    expect(set(rot) == {str(v) for v in vs}, 'rotation key identity')
    expect(all(len(rot[str(v)]) == len(set(rot[str(v)])) and set(rot[str(v)]) == adj[v] for v in vs), 'rotation neighbor identity')
    successor = {}
    for v in vs:
        ring = rot[str(v)]
        for i, u in enumerate(ring):
            successor[u, v] = (v, ring[(i+1) % len(ring)])
    cycles, dart_face = [], {}
    for start in sorted(successor):
        if start in dart_face:
            continue
        cycle, dart = [], start
        while dart not in dart_face:
            dart_face[dart] = len(cycles)
            cycle.append(dart[0])
            dart = successor[dart]
        expect(dart == start, 'face permutation orbit closes')
        cycles.append(cycle)
    return cycles, dart_face


def side_data(frame, roots, es, active, rels, beta):
    result = {}
    for r in roots:
        factors = [{'id': ['spoke', r, b], 'n': 1, 'F': [beta[frame.index(b)]]} for b in frame if tuple(sorted((r,b))) in es]
        factors += [{'id': ['unary', p['id']], 'n': len(p['contacts'][str(r)]), 'F': rels[p['id']]['F'][str(r)]}
                    for p in active if p['kind'] == 'unary' and r in p['owners']]
        union = set().union(*(set(t['F']) for t in factors))
        result[str(r)] = {'factors': factors, 'E': sorted(COLORS - union)}
    return result


def local_relation(frame, es, p, roots, beta):
    vs = sorted(set(frame) | set(p['vertices']))
    local_edges = [e for e in es if set(e) <= set(vs)]
    pins = dict(zip(frame, beta))
    grouped = {}
    for lift in enumerate_colors(vs, local_edges, pins):
        f = legal(vs, local_edges, pins, lift)
        key = tuple(f[v] for v in p['contact_order'])
        grouped.setdefault(key, []).append([f[v] for v in p['vertices']])
    tuples = [{'tuple': list(t), 'lifts': sorted(grouped[t])} for t in sorted(grouped)]
    fibres = []
    for pair in PAIRS:
        ids = []
        for i, t in enumerate(tuples):
            f = dict(zip(p['contact_order'], t['tuple']))
            if all(f[v] != pair[k] for k, r in enumerate(roots) for v in p['contacts'][str(r)]):
                ids.append(i)
        fibres.append({'pins': list(pair), 'tuple_indices': ids})
    forbidden = {}
    for r in p['owners']:
        ix = [p['contact_order'].index(v) for v in p['contacts'][str(r)]]
        palettes = [{t['tuple'][j] for j in ix} for t in tuples]
        forbidden[str(r)] = sorted(set.intersection(*palettes) if palettes else set())
    return {'tuples': tuples, 'fibres': fibres, 'F': forbidden}


def whole_row(frame, roots, vs, es, active, rels, beta):
    full_lifts = enumerate_colors(vs, es, dict(zip(frame,beta)))
    groups = {p: [] for p in PAIRS}
    for lift in full_lifts:
        f = legal(vs, es, dict(zip(frame,beta)), lift)
        groups[tuple(f[r] for r in roots)].append(lift)
    cells = []
    for i, pair in enumerate(PAIRS):
        cells.append({'pins': list(pair), 'tuple_indices': {p['id']: rels[p['id']]['fibres'][i]['tuple_indices'] for p in active},
                      'full_lifts': groups[pair]})
    return {'literal_beta': beta, 'root_pairs': [list(p) for p in PAIRS if groups[p]], 'all_16_fibres': cells,
            'sides': side_data(frame, roots, es, active, rels, beta)}


def target_transports():
    index = {tuple(p): i for i,p in enumerate(PATTERNS)}
    records = []
    for original in [933,941]:
        for shift in range(5):
            for reverse in [False, True]:
                perm = [(shift + (-1 if reverse else 1)*j)%5 for j in range(5)]
                row_indices = []
                for i,p in enumerate(PATTERNS):
                    if not original & (1 << i):
                        continue
                    translated = [p[j] for j in perm]
                    names = list(dict.fromkeys(translated))
                    canonical = tuple(names.index(c) for c in translated)
                    row_indices.append(index[canonical])
                records.append({'canonical_sigma': original,'whole_frame_positions': perm,'sigma': sum(1<<i for i in row_indices)})
    return sorted(records, key=lambda r:(r['canonical_sigma'],r['whole_frame_positions']))


def audit():
    input_manifest = load(HOME/'inputs.json')
    for item in input_manifest['authority_files']:
        b = (HOME/item['frozen']).read_bytes()
        expect(sha256(b).hexdigest() == item['sha256'], 'frozen input hash: '+item['frozen'])
    cert = load(PC/'certificate-final-v2.json')
    expect(len(cert['fixed_sources']) == 23 and len({s['graph']['id'] for s in cert['fixed_sources']}) == 23, '23 distinct fixed graphs')
    targets = target_transports()
    expect(targets == sorted(cert['whole_D5_target_transports'],key=lambda r:(r['canonical_sigma'],r['whole_frame_positions'])), 'whole-frame D5 transports')
    expect(len({r['sigma'] for r in targets}) == 10, 'ten distinct target masks')
    counts = Counter()
    output = []
    for record in cert['fixed_sources']:
        old = record['graph']
        name, family = old['id'], record['family']
        raw = load(PC/'source/artifacts/c5_excess_two_e4c/controls'/f'{name}.json')
        source = load(HOME/'inputs/base'/raw['source'])
        expect(sha256((HOME/'inputs/base'/raw['source']).read_bytes()).hexdigest() == raw['source_sha256'], 'source graph bytes '+name)
        es, vs, frame, roots = edges(raw['edges']), sorted(raw['vertices']), old['frame'], old['roots']
        expect([list(e) for e in es] == source['canonical_edges'] == old['edges'], 'same original source edges '+name)
        expect(vs == old['vertices'], 'same original vertex identity')
        fe = {tuple(sorted((frame[i],frame[(i+1)%5]))) for i in range(5)}
        expect({e for e in es if set(e) <= set(frame)} == fe, 'ordered induced C5')
        adj = adjacency(vs,es)
        isolated = [v for v in vs if v not in frame and not adj[v]]
        interior = set(vs) - set(frame) - set(isolated)
        degree = all(len(adj[r]) == 5 for r in roots) and tuple(sorted(roots)) not in es and all(len(adj[v]) == 4 for v in interior-set(roots))
        expect(degree, 'original epsilon2/nonadjacent roots/degree4')
        touch = sorted(set().union(*(adj[v] for v in interior)) & set(frame))
        expect(touch == old['touch'] and isolated == old['ignored_isolated'], 'full B touch/isolated identity')
        expect(len(components(interior,es)) == 1, 'H connected')
        expect(bridge_list(sorted(interior),[e for e in es if set(e)<=interior]) == old['H_bridges'], 'original H bridges')
        face_list, faceof = rotation_faces(vs,es,raw['rotation'])
        expect(face_list == old['faces'], 'complete original rotation face inventory')
        effective = set(vs)-set(isolated)
        expect(len(effective)-len(es)+len(face_list) == 2 and len(components(effective,es)) == 1, 'connected genus-zero rotation')
        expect(sum(len(f)==5 and set(f)==set(frame) for f in face_list)==1, 'unique C5 outer face')
        actual = components(interior-set(roots),es)
        expect(actual == [p['vertices'] for p in old['pieces']], 'complete H-root components')
        rels = {}
        pieces = []
        for p in old['pieces']:
            ps = set(p['vertices'])
            contacts = {str(r): sorted(adj[r]&ps) for r in roots}
            owners = [r for r in roots if contacts[str(r)]]
            support = sorted(set().union(*(adj[v] for v in ps))&set(frame))
            one = len(components(interior-ps,es)) == 1
            internal = [e for e in es if set(e)<=ps]
            attachments = [list(e) for e in es if set(e)&ps and set(e)&set(frame)]
            expect(contacts == p['contacts'] and owners == p['owners'] and support == p['support'] and one == p['one_sided'], 'actual contacts/ownership/support/one-sided')
            expect(set(p['contact_order']) == set().union(*(set(v) for v in contacts.values())) and len(p['contact_order']) == len(set(p['contact_order'])), 'one shared coordinate')
            expect(p['shared_contacts'] == sorted(set(contacts[str(roots[0])])&set(contacts[str(roots[1])])), 'shared contact identity')
            expect(p['attachments'] == attachments and p['internal_edges'] == [list(e) for e in internal] and p['original_internal_bridges'] == bridge_list(p['vertices'],internal), 'actual attachments/internal edges/bridges')
            expect(p['incidences'] == [len(contacts[str(r)]) for r in roots], 'original incidence vector')
            kind = 'mixed' if len(owners)==2 else 'unary' if len(owners)==1 else 'root-free'
            expect(kind == p['kind'], 'original piece kind')
            if 'shield' in p:
                kept = sorted(ps|set(frame)); kept_set = set(kept)
                reduced = {str(v): [w for w in raw['rotation'][str(v)] if w in kept_set] for v in kept}
                local_faces, localface = rotation_faces(kept,[e for e in es if set(e)<=kept_set],reduced)
                occupied = set()
                for v in kept:
                    ring = raw['rotation'][str(v)]
                    for i,w in enumerate(ring):
                        if w in kept_set:
                            continue
                        back = i-1
                        while ring[back%len(ring)] not in kept_set:
                            back -= 1
                        occupied.add(localface[ring[back%len(ring)],v])
                expect(len(occupied)==1,'complement in one original piece face')
                complement = local_faces[occupied.pop()]
                boundary = {tuple(sorted((complement[i],complement[(i+1)%len(complement)]))) for i in range(len(complement))}
                shield = {'complement_face':complement,'edges':[list(e) for e in sorted(fe-boundary)],'length':len(fe-boundary)}
                expect(shield == p['shield'], 'shield from original rotation')
            rels[p['id']] = [local_relation(frame,es,p,roots,beta) for beta in PATTERNS]
            expect(rels[p['id']] == p['rows'], 'all ordered tuples/full local lifts/16 empty-inclusive fibres')
            counts['piece_rows'] += 10
            counts['piece_full_lifts'] += sum(len(t['lifts']) for row in rels[p['id']] for t in row['tuples'])
            pieces.append({'id':p['id'],'vertices':p['vertices'],'contacts':contacts,'shared_contacts':p['shared_contacts'], 'support':support,'incidences':p['incidences'],'kind':kind,'shield':p.get('shield'),'rows':rels[p['id']]})
        rows = [whole_row(frame,roots,vs,es,old['pieces'],{p['id']:rels[p['id']][i] for p in old['pieces']},beta) for i,beta in enumerate(PATTERNS)]
        expect(rows == old['rows'], 'all original whole-graph full lifts/fibres and side factors')
        sigma = sum(1<<i for i,row in enumerate(rows) if row['root_pairs'])
        expect(sigma == old['sigma'] == raw['sigma'], 'all ten rows determine original Sigma')
        gained_records = []
        for saved in old['critical_witnesses']:
            e = tuple(saved['edge'])
            expect(e in es and e not in fe, 'criticality edge original/nonframe')
            after = [f for f in es if f!=e]
            gained = []
            for i,beta in enumerate(PATTERNS):
                if rows[i]['root_pairs']:
                    continue
                witnesses = enumerate_colors(vs,after,dict(zip(frame,beta)),one=True)
                if witnesses:
                    gained.append({'index':i,'full_lift':witnesses[0]})
            expect([w['index'] for w in gained] == [w['index'] for w in saved['gained_rows']] and gained, 'all gained rows independent criticality')
            for w in saved['gained_rows']:
                legal(vs,after,dict(zip(frame,PATTERNS[w['index']])),w['full_lift'])
            gained_records.append({'edge':list(e),'gained_rows':gained})
        expect(len(gained_records)==len(es)-5,'every original nonframe critical edge covered')
        counts['nonframe_critical_edges'] += len(gained_records)
        prefix = 'N2' if family=='N2' else 'N1'
        counts[prefix+'_graphs'] += 1
        counts[prefix+'_original_16pin_fibres'] += 160
        geometry_holds = []
        for u in old['pieces']:
            if u['kind'] != 'unary' or sum(u['incidences']) != 1:
                continue
            for l in old['pieces']:
                for s in old['pieces']:
                    if l['id']==s['id'] or l['kind']!='mixed' or s['kind']!='mixed':
                        continue
                    supports = [set(t['support']) for t in [u,l,s]]
                    shieldsets = [set(map(tuple,t.get('shield',{}).get('edges',[]))) for t in [u,l,s]]
                    triples = [{frame[(j+k)%5] for k in range(3)} for j in range(5)]
                    good = len(old['pieces'])==3 and all(t['one_sided'] for t in [u,l,s]) and not any(supports[1]<=set(e) for e in fe) and supports[2] in [set(e) for e in fe] and supports[0] in triples and supports[1] in triples and list(map(len,shieldsets))==[2,2,1] and len(set.union(*shieldsets))==5
                    if good:
                        geometry_holds.append([u['id'],l['id'],s['id']])
        expect(bool(geometry_holds) == (record['LP_geometry']['status']=='triggered and holds'), 'LP necessary geometry')
        if prefix == 'N2':
            counts['N2_LP_geometry_triggered'] += bool(geometry_holds)
            counts['N2_target_sigma_triggered'] += sigma in {t['sigma'] for t in targets}
            counts['N2_full_B_touch'] += set(touch)==set(frame)
        derivatives = []
        for saved in record['whole_U_omissions']:
            p = next(p for p in old['pieces'] if p['id']==saved['piece'])
            r,s = saved['r'],saved['s']
            xv = [v for v in vs if v not in p['vertices']]
            xe = [e for e in es if set(e)<=set(xv)]
            expect(xv == saved['vertices_X'] and [list(e) for e in xe] == saved['edges_X'], 'exact whole original U omission')
            active = [t for t in old['pieces'] if t['id'] != p['id']]
            xrows = [whole_row(frame,roots,xv,xe,active,{t['id']:rels[t['id']][i] for t in active},beta) for i,beta in enumerate(PATTERNS)]
            expect(xrows == saved['rows_X'], 'all X full lifts/fibres')
            xsigma = sum(1<<i for i,row in enumerate(xrows) if row['root_pairs'])
            expect(xsigma==saved['sigma_X'],'X complete Sigma')
            contact = tuple(sorted((r,p['contacts'][str(r)][0])))
            expect(list(contact)==saved['contact_edge'],'original sole U contact')
            cut_edges = [e for e in es if e!=contact]
            forcing, beta_cores = [], []
            for i,beta in enumerate(PATTERNS):
                pins = dict(zip(frame,beta))
                cuts = enumerate_colors(vs,cut_edges,pins)
                expect(cuts == saved['contact_deleted_rows'][i]['all_full_lifts'],'contact deletion preserves its own full vertex/lift graph')
                pairs = sorted({tuple(dict(zip(vs,lift))[root] for root in roots) for lift in cuts})
                expect([list(t) for t in pairs]==xrows[i]['root_pairs'],'whole U/contact deletion root-pair equality')
                if xrows[i]['root_pairs'] and not rows[i]['root_pairs']:
                    palette = sorted({t['tuple'][0] for t in rels[p['id']][i]['tuples']})
                    projection = sorted({pair[roots.index(r)] for pair in xrows[i]['root_pairs']})
                    expect(len(palette)==1 and palette==projection,'Delta singleton forcing')
                    forcing.append({'index':i,'contact_palette':palette,'all_X_r_projection':projection})
                rejected = not xrows[i]['root_pairs']
                xa = adjacency(xv,xe)
                witnesses = []
                if rejected:
                    for e in xe:
                        if e in fe:
                            continue
                        lift = enumerate_colors(xv,[f for f in xe if f!=e],pins,one=True)
                        witnesses.append({'edge':list(e),'full_lift':lift[0] if lift else None})
                minimal = rejected and len(xa[r])==4 and len(xa[s])==5 and all(w['full_lift'] is not None for w in witnesses)
                oldcheck = saved['all_ten_literal_beta_core_checks'][i]
                expect(minimal == (oldcheck['layers']['rejecting_beta_minimal_45_54_core']['status']=='triggered and holds'),'same-beta minimal45/54')
                for w in oldcheck['retained_edge_beta_witnesses']:
                    if w['full_lift'] is not None:
                        legal(xv,[f for f in xe if list(f)!=w['edge']],pins,w['full_lift'])
                columns=[]
                er=set(xrows[i]['sides'][str(r)]['E']); ess=set(xrows[i]['sides'][str(s)]['E'])
                if minimal and ess and all(rels[t['id']][i]['tuples'] for t in active):
                    factors=xrows[i]['sides'][str(r)]['factors']; fsets=[set(f['F']) for f in factors]
                    for b in sorted(ess):
                        cols=[]
                        for t in active:
                            if t['kind']!='mixed':
                                continue
                            bad=[]
                            for c in range(4):
                                pair=(c,b) if roots[0]==r else (b,c)
                                if not rels[t['id']][i]['fibres'][PAIRS.index(pair)]['tuple_indices']:
                                    bad.append(c)
                            cols.append({'piece':t['id'],'k':len(t['contacts'][str(r)]),'forbidden':bad})
                        union=set().union(*(set(t['forbidden']) for t in cols))
                        terms=[sum(f['n']-len(f['F']) for f in factors),sum(map(len,fsets))-len(set().union(*fsets)),sum(t['k']-len(t['forbidden']) for t in cols),sum(len(t['forbidden']) for t in cols)-len(union),len(union-er)]
                        expect(terms==[0]*5 and union==er,'zero slack complete original mixed column partition')
                        columns.append({'b':b,'columns':cols,'E_r_X':sorted(er),'D_O_delta_o_lambda':terms})
                expect(columns == [{k:c[k] for k in ['b','columns','E_r_X','D_O_delta_o_lambda']} for c in oldcheck['zero_slack_columns']],'saved every zero-slack column')
                counts[prefix+'_rejecting_beta_minimal_occurrences'] += minimal
                beta_cores.append({'index':i,'literal_beta':beta,'rejecting_minimal_45_54':minimal,'retained_edge_beta_witnesses':witnesses,'zero_slack_columns':columns})
            expect(forcing==[{k:f[k] for k in ['index','contact_palette','all_X_r_projection']} for f in saved['new_gamma_singleton_forcing']],'all Delta original singleton identities')
            delta=[i for i in range(10) if xsigma&(1<<i) and not sigma&(1<<i)]
            expect(delta==saved['Delta'],'complete Delta')
            counts[prefix+'_whole_U_omissions'] += 1
            counts[prefix+'_X_16pin_fibres'] += 160
            counts[prefix+'_Delta_gamma_instances'] += len(forcing)
            derivatives.append({'piece':p['id'],'r':r,'s':s,'vertices_X':xv,'edges_X':[list(e) for e in xe],'sigma_X':xsigma,'rows_X':xrows,'Delta':delta,'singleton_forcing':forcing,'all_beta_core_checks':beta_cores})
        output.append({'family':family,'id':name,'vertices':vs,'edges':[list(e) for e in es],'frame':frame,'roots':roots,'faces':face_list,'touch':touch,'sigma':sigma,'pieces':pieces,'rows':rows,'critical_witnesses':gained_records,'LP_geometry_holds':geometry_holds,'whole_U_omissions':derivatives})
    expect(counts['N2_graphs']==19 and counts['N2_whole_U_omissions']==7 and counts['N1_graphs']==4 and counts['N1_whole_U_omissions']==4,'separate fixed N2/N1 domains')
    expect(counts['N2_LP_geometry_triggered']==counts['N2_target_sigma_triggered']==counts['N2_rejecting_beta_minimal_occurrences']==0,'zero N2 triggers, never an exclusion')
    return {'task':'N45-PCA','BASE':input_manifest['BASE'],'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'inputs_sha256':sha256((HOME/'inputs.json').read_bytes()).hexdigest(),'counts':dict(sorted(counts.items())),
            'whole_D5_target_transports':targets,'fixed_sources':output,'scope':'Independent recomputation of fixed finite controls only; no general validator soundness, paper, Lean or source exclusion claim.'}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--generate',action='store_true'); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
    expect(args.generate != args.check,'choose exactly one mode')
    path=HOME/'independent-certificate.json'
    if args.generate:
        with path.open('xb') as f:
            result=audit(); f.write(encode(result))
    else:
        result=audit(); expect(path.read_bytes()==encode(result),'independent byte replay')
    print(json.dumps({'result':'holds','counts':result['counts'],'certificate_sha256':sha256(path.read_bytes()).hexdigest()},sort_keys=True))


if __name__=='__main__':
    main()
