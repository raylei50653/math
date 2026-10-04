#!/usr/bin/env python3
"""ER: generate disk graphs from connected plane H maps and ordered face spokes.

No ES script is imported or read. plantri 5.8 supplies connected simple plane
maps; this module inserts a named induced C5 around each chosen face. JSON is
created exclusively or recomputed byte-for-byte by --check. No FCT oracle.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from math import factorial
from multiprocessing import Pool
from pathlib import Path
import subprocess
import sys
from time import perf_counter

from c5_excess_two_independent_coloring import (FRAME_EDGES, T4_MASK,
    SINGLETON_INDICES, compile_graph, find_extension, sigma_mask,
    sigma_mask_with_witnesses, deletion_profile, direct_product_sigma, REPS)
from c5_excess_two_independent_canonical import canonical

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_independent_search'
ES = ROOT / 'artifacts/c5_excess_two_finite_search'
KINDS = ('NA', 'AD', 'D6')
FRAME = frozenset(FRAME_EDGES)

def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'),
                       ensure_ascii=False) + '\n').encode()

def save(path, value, check):
    data = encoded(value)
    if check:
        if path.read_bytes() != data:
            raise RuntimeError(f'byte mismatch: {path}')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as f:
            f.write(data)

def q_positions(mask):
    return tuple(i for i, row in enumerate(SINGLETON_INDICES)
                 if not (mask >> row) & 1)

def q_shape(q):
    return ','.join(map(str, min(tuple(sorted((a + sign*v) % 5 for v in q))
                                for a in range(5) for sign in (-1, 1))))

def c_q(q):
    return 1 if len(q) == 5 else len(q) - sum(i in q and (i+1)%5 in q for i in range(5))

def map_faces(rotation):
    """Every oriented face walk, including repeated cut vertices/bridges."""
    unused = {(u,v) for u,row in enumerate(rotation) for v in row}
    faces = []
    while unused:
        start = min(unused)
        edge = start
        face = []
        while True:
            u,v = edge
            unused.remove(edge)
            face.append(u)
            row = rotation[v]
            edge = (v, row[(row.index(u) + 1) % len(row)])
            if edge == start:
                break
        faces.append(tuple(face))
    m = sum(map(len, rotation))//2
    assert len(rotation) - m + len(faces) == 2
    return faces

def corner_allocations(face, needs):
    """Allocate each vertex's prescribed spokes among its face occurrences."""
    remaining = list(needs)
    later = [Counter(face[i+1:]) for i in range(len(face))]
    counts = [0] * len(face)
    def rec(i):
        if i == len(face):
            if not any(remaining):
                yield tuple(v for v,c in zip(face,counts) for _ in range(c))
            return
        v = face[i]
        choices = (remaining[v],) if not later[i][v] else range(remaining[v]+1)
        for c in choices:
            counts[i] = c
            remaining[v] -= c
            yield from rec(i+1)
            remaining[v] += c
    yield from rec(0)

def spoke_supports(sequence, k):
    """Noncrossing spoke endpoints have cyclically monotone boundary labels.

    Each corner allocation is also rotated at every spoke occurrence. Thus the
    first label may be pinned to 0 (C5 rotation) without losing a graph orbit.
    Four touched frame vertices are necessary for a T4-accepting nonempty Q.
    """
    support = [0]*k
    s = len(sequence)
    if not s:
        return
    def rec(i, lower, touched):
        if i == s:
            if touched.bit_count() >= 4:
                yield tuple(support)
            return
        v = sequence[i]
        labels = (0,) if i == 0 else range(lower,5)
        for b in labels:
            bit = 1 << b
            if support[v] & bit:
                continue
            new_touched = touched | bit
            if new_touched.bit_count() + s-i-1 < 4:
                continue
            support[v] |= bit
            yield from rec(i+1, b, new_touched)
            support[v] ^= bit
    yield from rec(0,0,0)

# Local singleton clashes are a necessary failure of the same pinned T4 CSP.
ALLOWED = tuple(tuple(sum(1<<c for c in range(4)
                     if all(c != p[b] for b in range(5) if mask>>b&1))
                  for mask in range(32)) for p in REPS)

def screen_supports(h_edges, supports):
    for row in (2,5,7,8,9):
        domains = [ALLOWED[row][s] for s in supports]
        for u,v in h_edges:
            a,b = domains[u],domains[v]
            if a == b and a.bit_count() == 1:
                return False
    return True

def root_choices(kind, rotation, face_vertices):
    k = len(rotation)
    degrees = tuple(map(len,rotation))
    if kind == 'D6':
        for root in range(k):
            prescribed = [4]*k
            prescribed[root] = 6
            needs = tuple(p-d for p,d in zip(prescribed,degrees))
            if all(0 <= s <= 3 for s in needs) and all(not s or v in face_vertices for v,s in enumerate(needs)):
                yield (root,), needs
    else:
        for roots in combinations(range(k),2):
            adjacent = roots[1] in rotation[roots[0]]
            if adjacent != (kind == 'AD'):
                continue
            prescribed = [4]*k
            for v in roots:
                prescribed[v] = 5
            needs = tuple(p-d for p,d in zip(prescribed,degrees))
            if all(0 <= s <= 3 for s in needs) and all(not s or v in face_vertices for v,s in enumerate(needs)):
                yield roots,needs

def map_worker(task):
    k,line = task
    n,text = line.strip().split(' ',1)
    assert int(n) == k
    rotation = tuple(tuple(ord(c)-ord('a') for c in row) for row in text.split(','))
    h_edges = tuple((u,v) for u,row in enumerate(rotation) for v in row if u<v)
    result = {kind:{} for kind in KINDS}
    stats = Counter(maps=1)
    all_faces = map_faces(rotation)
    for face in all_faces:
        face_vertices = frozenset(face)
        if any(len(row) < 4 and v not in face_vertices for v,row in enumerate(rotation)):
            continue
        for kind in KINDS:
            for roots,needs in root_choices(kind,rotation,face_vertices):
                if sum(needs) < 4:
                    continue
                stats[kind+'_root_faces'] += 1
                private_order = roots + tuple(v for v in range(k) if v not in roots)
                remap = {v:5+i for i,v in enumerate(private_order)}
                base = FRAME_EDGES + tuple((min(remap[u],remap[v]),max(remap[u],remap[v])) for u,v in h_edges)
                seen = set()
                sequences = set(corner_allocations(face,needs))
                for seq in sorted(sequences):
                    cyclic = sorted({seq[i:]+seq[:i] for i in range(len(seq))})
                    for sequence in cyclic:
                        for supports in spoke_supports(sequence,k):
                            if supports in seen:
                                continue
                            seen.add(supports)
                            stats[kind+'_attachments'] += 1
                            if not screen_supports(h_edges,supports):
                                continue
                            edges = tuple(sorted(base + tuple((b,remap[v]) for v,s in enumerate(supports) for b in range(5) if s>>b&1)))
                            graph = compile_graph(edges,5+k)
                            if any(find_extension(graph,row) is None for row in (2,5,7,8,9)):
                                continue
                            stats[kind+'_t4_candidates'] += 1
                            mask = T4_MASK
                            for row in SINGLETON_INDICES:
                                if find_extension(graph,row) is not None:
                                    mask |= 1 << row
                            if mask == 1023:
                                continue
                            key = canonical(kind,k,edges)
                            result[kind][key.code] = key.edges
                            stats[kind+'_q_candidates'] += 1
    return result,dict(stats)

def plantri_binary():
    vendor = OUT/'vendor'
    source = vendor/'plantri.c'
    expected = '3f70de5a3cacc78b2ed25b6a257588da94a518d8ae1dae74bcd0bf259cea07e8'
    if sha256(source.read_bytes()).hexdigest() != expected:
        raise RuntimeError('plantri source SHA mismatch')
    scratch = ROOT/'scratch/er'
    scratch.mkdir(parents=True, exist_ok=True)
    binary = scratch/'plantri'
    subprocess.run(['cc','-O3','-o',str(binary),str(source)],check=True)
    return binary

def enumerate_layer(k,jobs,binary):
    result = {kind:{} for kind in KINDS}
    stats = Counter()
    # e_H>=k follows from disk Euler and epsilon2; s>=4 from T4,Q.
    command = [str(binary),'-pc1m1',f'-e{k}:{2*k-1}','-a',str(k)]
    if k < 3:
        return result,dict(stats),command
    p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    def tasks():
        for line in p.stdout:
            yield k,line
    started = perf_counter()
    with Pool(jobs) as pool:
        for partial,counters in pool.imap_unordered(map_worker,tasks(),chunksize=8):
            for kind in KINDS:
                result[kind].update(partial[kind])
            stats.update(counters)
            if stats['maps'] % 10000 == 0:
                print(f'k={k} maps={stats["maps"]} q_orbits='+str({t:len(result[t]) for t in KINDS})+f' elapsed={perf_counter()-started:.1f}s',flush=True)
    stderr = p.stderr.read()
    if p.wait():
        raise RuntimeError(stderr)
    print(stderr.strip(),flush=True)
    return result,dict(sorted(stats.items())),command

def certificate(kind,k,edges,strict=True):
    can = canonical(kind,k,edges)
    mask,witnesses = sigma_mask_with_witnesses(can.edges,5+k)
    q = q_positions(mask)
    deletions = deletion_profile(can.edges,5+k,with_witnesses=True)
    ds = []
    critical = True
    for edge,(dm,ws) in sorted(deletions.items()):
        assert dm & mask == mask
        added = dm & ~mask
        critical &= bool(added)
        ds.append({'edge':edge,'sigma_mask':dm,'new_indices':[i for i in range(10) if added>>i&1],
                   'witnesses':{str(i):w for i,w in sorted(ws.items()) if added>>i&1}})
    # Named augmented rotation is a certificate only; generation never calls planarity.
    import networkx as nx
    g = nx.Graph()
    g.add_nodes_from(range(6+k))
    g.add_edges_from(can.edges)
    g.add_edges_from((i,5+k) for i in range(5))
    planar,embedding = nx.check_planarity(g)
    degrees = tuple(sum(v in edge for edge in can.edges) for v in range(5,5+k))
    expected = tuple(6 if kind == 'D6' and i == 0 else 5 if kind != 'D6' and i < 2 else 4 for i in range(k))
    h = g.subgraph(range(5,5+k))
    domain = {'induced_C5':frozenset(e for e in can.edges if e[1]<5) == FRAME,
              'disk':planar,'prescribed_degrees':degrees == expected,
              'spokes_at_most_three':all(sum(u<5 for u in g[v])<=3 for v in range(5,5+k)),
              'H_connected':nx.is_connected(h),
              'root_adjacency':kind == 'D6' or g.has_edge(5,6) == (kind == 'AD'),
              'T4':mask&T4_MASK == T4_MASK,'Q_nonempty':bool(q)}
    if strict:
        assert all(domain.values()),domain
    return {'code':can.code,'canonical_edges':can.edges,'orbit_size':can.orbit_size,
            'stabilizer_size':can.stabilizer_size,'sigma_mask':mask,'Q':q,'c_Q':c_q(q),
            'Q_plus_cQ':len(q)+c_q(q),'critical':critical,'accepted_colourings':witnesses,
            'deletion_sigmas':ds,'domain':domain,
            'augmented_rotation':{str(v):tuple(embedding.neighbors_cw_order(v)) for v in sorted(g)} if planar else None}

def comparison(kind,k,orbits):
    path = ES/f'{kind}_k{k}_validate.json'
    if not path.exists():
        raise RuntimeError(f'missing ES reference {path}')
    source = json.loads(path.read_bytes())
    es_q = {canonical(kind,k,row['canonical_edges']).code for row in source['q_orbits']}
    es_crit = {canonical(kind,k,row['canonical_edges']).code for row in source['crit_orbits']}
    ours_q = {row['code'] for row in orbits}
    ours_crit = {row['code'] for row in orbits if row['critical']}
    ours_rows = {row['code']:row for row in orbits}
    payload_details = {}
    for row in source['q_orbits']:
        can = canonical(kind,k,row['canonical_edges'])
        if can.code not in ours_rows:
            continue
        moved_mask = 0
        for index,p in enumerate(REPS):
            if not row['sigma_mask'] >> index & 1:
                continue
            moved = [0]*5
            for old in range(5):
                moved[can.permutation[old]] = p[old]
            names = {}
            normalized = tuple(names.setdefault(c,len(names)) for c in moved)
            moved_mask |= 1 << REPS.index(normalized)
        expected = {'sigma_mask':moved_mask,
                    'Q':tuple(sorted(can.permutation[v] for v in row['Q'])),
                    'orbit_size':row['orbit_size'],
                    'stabilizer_size':row['stabilizer_size'],
                    'critical':row['critical']}
        actual = {key:ours_rows[can.code][key] for key in expected}
        if actual != expected:
            payload_details[can.code] = {'er':actual,'es_transported':expected}
    histogram = Counter()
    for row in orbits:
        histogram[q_shape(row['Q'])] += row['orbit_size']
    counts = {'q':sum(row['orbit_size'] for row in orbits),
              'crit':sum(row['orbit_size'] for row in orbits if row['critical'])}
    mismatches = {'q_only_er':sorted(ours_q-es_q),'q_only_es':sorted(es_q-ours_q),
                  'crit_only_er':sorted(ours_crit-es_crit),'crit_only_es':sorted(es_crit-ours_crit),
                  'payload_disagreements':sorted(payload_details)}
    agree = (not any(mismatches.values()) and
             counts == {key:source['counts'][key] for key in ('q','crit')} and
             dict(histogram) == source['q_shape_labelled'])
    return {'consistent':agree,'es_source':str(path.relative_to(ROOT)),
            'es_sha256':sha256(path.read_bytes()).hexdigest(),
            'er_counts':counts,'es_counts':{key:source['counts'][key] for key in ('q','crit')},
            'er_q_orbits':len(ours_q),'es_q_orbits':len(es_q),
            'er_crit_orbits':len(ours_crit),'es_crit_orbits':len(es_crit),
            'er_q_shape_labelled':dict(sorted(histogram.items())),
            'es_q_shape_labelled':source['q_shape_labelled'],'differences':mismatches,
            'payload_details':payload_details}

def control_payload():
    from c5_excess_two_independent_coloring import self_test
    from c5_excess_two_independent_canonical import self_check
    coloring = self_test()
    coloring.pop('seconds')
    sources = ['scripts/c5_excess_two_independent_search.py',
               'scripts/c5_excess_two_independent_coloring.py',
               'scripts/c5_excess_two_independent_canonical.py',
               'scripts/c5_excess_two_independent_brute.py',
               'scripts/c5_kempe_screen.py',
               'artifacts/c5_excess_two_independent_search/vendor/plantri.c',
               'artifacts/c5_excess_two_independent_search/vendor/plantri-guide.txt']
    return {'schema':'c5-er-controls-v1','baseline':'d00aba4e10ea2d05ab216fedd94f5a166b2777ad',
            'coloring':coloring,'canonical':self_check(),
            'source_sha256':{p:sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}}

def certificate_worker(task):
    return certificate(*task)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-k',type=int,default=9)
    parser.add_argument('--min-k',type=int,default=3)
    parser.add_argument('--jobs',type=int,default=8)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--no-brute',action='store_true',help='Only for timing exploratory higher layers')
    parser.add_argument('--controls-only',action='store_true')
    args = parser.parse_args()
    if not 1 <= args.jobs <= 8:
        parser.error('jobs must be 1..8')
    if args.controls_only or args.min_k == 3:
        save(OUT/'controls.json',control_payload(),args.check)
        if args.controls_only:
            return 0
    binary = plantri_binary()
    timings = []
    any_failure = False
    for k in range(args.min_k,args.max_k+1):
        started = perf_counter()
        found,stats,command = enumerate_layer(k,args.jobs,binary)
        for kind in KINDS:
            tasks = [(kind,k,edges) for code,edges in sorted(found[kind].items())]
            if tasks:
                with Pool(args.jobs) as pool:
                    certs = pool.map(certificate_worker,tasks,chunksize=8)
            else:
                certs = []
            comp = comparison(kind,k,certs)
            brute = None
            b = None
            if k <= 5 and not args.no_brute:
                from c5_excess_two_independent_brute import brute_layer
                b = brute_layer(kind,k)
                bh = Counter()
                orbit_bh = Counter()
                for row in b['Q_shape_distribution']:
                    q = tuple(v for v in range(5) if row['canonical_mask'] >> v & 1)
                    bh[q_shape(q)] += row['count']
                for row in b['q_orbits']:
                    orbit_bh[q_shape(row['Q'])] += row['orbit_size']
                brute = {'counts':b['counts'],'crit_codes':b['crit_codes'],
                         'q_codes':sorted(row['code'] for row in b['q_orbits']),
                         'q_shape_labelled':dict(sorted(bh.items())),
                         'Q_shape_distribution':b['Q_shape_distribution'],
                         'consistent':set(b['crit_codes']) == {r['code'] for r in certs if r['critical']}
                              and set(row['code'] for row in b['q_orbits']) == {r['code'] for r in certs}
                              and b['counts']['q'] == comp['er_counts']['q']
                              and b['counts']['crit'] == comp['er_counts']['crit']
                              and dict(bh) == comp['er_q_shape_labelled']
                              and dict(bh) == dict(orbit_bh)}
                bc = {row['code']:row for row in b['q_orbits']}
                oc = {row['code']:row for row in certs}
                affected = set(bc)^set(oc)
                for code in set(bc)&set(oc):
                    if any(bc[code][key] != oc[code][key] for key in
                           ('sigma_mask','orbit_size','stabilizer_size')) or bc[code]['crit'] != oc[code]['critical'] or tuple(bc[code]['Q']) != tuple(oc[code]['Q']):
                        affected.add(code)
                if not brute['consistent'] and not affected:
                    affected = set(bc)|set(oc)
                brute['affected_codes'] = sorted(affected)
                brute['consistent'] &= not affected
            chunks = []
            chunk_rows = []
            chunk_bytes = 0
            def flush_chunk():
                nonlocal chunk_rows, chunk_bytes
                if not chunk_rows:
                    return
                path = OUT/f'{kind}_k{k}/q_orbits/chunk_{len(chunks)+1:04d}.json'
                value = {'type':kind,'k':k,'q_orbits':chunk_rows}
                save(path,value,args.check)
                chunks.append({'path':str(path.relative_to(ROOT)),
                               'sha256':sha256(encoded(value)).hexdigest(),
                               'orbits':len(chunk_rows)})
                chunk_rows = []
                chunk_bytes = 0
            summaries = []
            for row in certs:
                size = len(encoded(row))
                if chunk_rows and chunk_bytes + size > 750_000:
                    flush_chunk()
                summaries.append({key:row[key] for key in
                                  ('code','orbit_size','stabilizer_size','sigma_mask','Q','critical')}
                                 | {'chunk':len(chunks)+1})
                chunk_rows.append(row)
                chunk_bytes += size
            flush_chunk()
            data = {'schema':'c5-er-v1','type':kind,'k':k,'generator':'plantri5.8 plane H + ordered face spokes',
                    'T4_mask':T4_MASK,'singleton_indices':SINGLETON_INDICES,
                    'plantri_source_sha256':sha256((OUT/'vendor/plantri.c').read_bytes()).hexdigest(),
                    'generation_stats':stats,'q_orbits':summaries,'q_orbit_chunks':chunks,
                    'comparison':comp,'brute_reference':brute}
            save(OUT/f'{kind}_k{k}.json',data,args.check)
            for i,row in enumerate(r for r in certs if r['critical']):
                save(OUT/f'{kind}_k{k}/crit_orbits/orbit_{i+1:04d}.json',row,args.check)
            failed = not comp['consistent'] or (brute is not None and not brute['consistent'])
            counterexamples = [r for r in certs if r['critical'] and r['Q_plus_cQ'] > 4]
            print(f'{kind} k={k} q={comp["er_counts"]["q"]} crit={comp["er_counts"]["crit"]} crit_orbits={comp["er_crit_orbits"]} consistent={comp["consistent"]} brute={None if brute is None else brute["consistent"]}',flush=True)
            if failed or counterexamples:
                # Save every discrepancy with all graph edges/masks/deletions.
                rows = {r['code']:r for r in certs}
                esdata = json.loads((ES/f'{kind}_k{k}_validate.json').read_bytes())
                for r in esdata['q_orbits'] + esdata['crit_orbits']:
                    key = canonical(kind,k,r['canonical_edges'])
                    rows.setdefault(key.code,certificate(kind,k,key.edges,strict=False))
                evidence = []
                differing = set().union(*(set(v) for v in comp['differences'].values()))
                differing.update(r['code'] for r in counterexamples)
                if brute is not None:
                    differing.update(brute['affected_codes'])
                    for r in b['q_orbits']:
                        if r['code'] in differing:
                            rows.setdefault(r['code'],certificate(kind,k,r['canonical_edges'],strict=False))
                if not comp['consistent'] and not differing:
                    differing.update(rows)
                for code in sorted(differing):
                    row = rows[code]
                    mask,ws = direct_product_sigma(row['canonical_edges'],5+k,max_inner=9)
                    third_deletions = []
                    for edge in row['canonical_edges']:
                        if tuple(edge) not in FRAME:
                            dm,dw = direct_product_sigma([e for e in row['canonical_edges'] if e != edge],5+k,max_inner=9)
                            third_deletions.append({'edge':edge,'mask':dm,'witnesses':dw})
                    evidence.append({'certificate':row,'third_method_mask':mask,'third_method_witnesses':ws,
                                     'third_method_critical':all(d['mask'] != mask for d in third_deletions),
                                     'third_method_deletions':third_deletions})
                save(OUT/f'STOP_{kind}_k{k}.json',{'comparison':comp,'brute_reference':brute,
                                               'counterexamples':counterexamples,'evidence':evidence},args.check)
                any_failure = True
                break
        timings.append({'k':k,'wall_seconds':perf_counter()-started})
        if any_failure:
            break
    if not args.check:
        save(OUT/f'timing_{args.min_k}_{args.max_k}.json',{'jobs':args.jobs,'layers':timings},False)
    return 1 if any_failure else 0

if __name__ == '__main__':
    raise SystemExit(main())
