#!/usr/bin/env python3
"""Finite C5 Kempe transport index and bounded disk wiring control.

Imports only generators from c5_kempe_screen; never runs its report or 4CT screen.
New output is created exclusively; --check recomputes without writing files.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import networkx as nx

from c5_kempe_screen import PAIRS, REPS, noncrossing, normalize, partitions

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_kempe_transport/observations.json'
CATALOGUE = ROOT / 'artifacts/c5_cells/cells.json'
INDEX = {q: i for i, q in enumerate(REPS)}


def canonical_partition(p):
    return tuple(sorted(tuple(sorted(b)) for b in p))


def independent_partitions(xs):
    """Restricted-growth enumeration, independent of the imported recursion."""
    if not xs:
        return {()}
    result = set()
    for word in product(range(len(xs)), repeat=len(xs)):
        if not all(word[i] <= max(word[:i], default=-1) + 1
                   for i in range(len(xs))):
            continue
        result.add(canonical_partition(tuple(
            tuple(xs[i] for i, c in enumerate(word) if c == j)
            for j in range(max(word) + 1))))
    return result


def admissible_partitions(q, split, generator):
    left = [i for i in range(5) if q[i] in split[0]]
    right = [i for i in range(5) if q[i] in split[1]]
    result = set()
    for p in generator(left):
        for r in generator(right):
            blocks = canonical_partition(tuple(p) + tuple(r))
            if not noncrossing(blocks):
                continue
            owner = {v: j for j, b in enumerate(blocks) for v in b}
            if any(any(q[i] in pair and q[(i + 1) % 5] in pair
                       for pair in split) and owner[i] != owner[(i + 1) % 5]
                   for i in range(5)):
                continue
            result.add(blocks)
    return sorted(result)


def alternating_quadruples(left, right):
    """Certificates of four DISTINCT alternating frame contacts."""
    a, b = set(left), set(right)
    return [list(v) for v in combinations(range(5), 4)
            if ((v[0] in a and v[2] in a and v[1] in b and v[3] in b)
                or (v[0] in b and v[2] in b and v[1] in a and v[3] in a))]


def block_swap(q, pair, block):
    result = list(q)
    for v in block:
        assert q[v] in pair
        result[v] = pair[1] if q[v] == pair[0] else pair[0]
    assert all(result[i] != result[(i + 1) % 5] for i in range(5))
    return tuple(result)


def transport_tables():
    cells = json.loads(CATALOGUE.read_text())
    assert cells['pattern_order'] == [list(q) for q in REPS]
    assert cells['singleton_of_three_colour'] == {
        '0': 4, '1': 3, '3': 2, '4': 1, '6': 0}
    generator_checks = []
    for n, bell in enumerate((1, 1, 2, 5, 15, 52)):
        actual = {canonical_partition(p) for p in partitions(list(range(n)))}
        assert actual == independent_partitions(list(range(n)))
        assert len(actual) == bell
        generator_checks.append(dict(vertices=n, partitions=bell))
    tables = []
    for sigma in (933, 941):
        records, partition_rows = {}, []
        for qi, q in enumerate(REPS):
            if sigma >> qi & 1:
                continue
            for si, split in enumerate(PAIRS):
                options = admissible_partitions(q, split, partitions)
                assert options == admissible_partitions(q, split, independent_partitions)
                for pi, blocks in enumerate(options):
                    pid = f'KT{sigma}-q{qi}-s{si}-p{pi}'
                    row = dict(id=pid, q_index=qi, q=q, split=split,
                               frame_blocks=blocks, accepted_target_swap_ids=[])
                    for block in blocks:
                        pair = next(c for c in split if q[block[0]] in c)
                        literal = block_swap(q, pair, block)
                        target = INDEX[normalize(literal)]
                        if not sigma >> target & 1:
                            continue
                        rid = (f'KT{sigma}-q{qi}-c{pair[0]}{pair[1]}-B'
                               + ''.join(map(str, block)))
                        if rid not in records:
                            contexts = []
                            for a in range(5):
                                b = (a + 1) % 5
                                contexts.append(dict(
                                    a=a, b=b,
                                    frame_sides=[name for name, v in (('a', a), ('b', b))
                                                 if v in block],
                                    endpoint_colours_in_pair=[
                                        name for name, v in (('a', a), ('b', b))
                                        if q[v] in pair]))
                            records[rid] = dict(
                                id=rid, q_index=qi, q=q, colour_pair=pair,
                                frame_block=block, q_prime_literal=literal,
                                q_prime_normalized=normalize(literal), q_prime_index=target,
                                frame_side_contexts=contexts,
                                actual_root_origin='UNASSIGNED: needs same-graph root-to-chain incidence',
                                partition_ids=[])
                        records[rid]['partition_ids'].append(pid)
                        row['accepted_target_swap_ids'].append(rid)
                    partition_rows.append(row)
        pairs = []
        counts = Counter()
        coverage = {str(i): [0] * 5 for i in range(10) if not sigma >> i & 1}
        for row in partition_rows:
            rs = [records[k] for k in row['accepted_target_swap_ids']]
            for a in range(5):
                b = (a + 1) % 5
                for left in rs:
                    for right in rs:
                        if (left['id'] == right['id'] or a not in left['frame_block']
                                or b not in right['frame_block']):
                            continue
                        assert not set(left['frame_block']) & set(right['frame_block'])
                        crossing = alternating_quadruples(left['frame_block'], right['frame_block'])
                        assert not crossing  # SAME noncrossing partition, not independent choices.
                        coverage[str(row['q_index'])][a] += 1
                        counts['joint_noninterlacing_endpoint_pairs'] += 1
                        pairs.append(dict(
                            partition_id=row['id'], a=a, b=b,
                            a_frame_swap_id=left['id'], b_frame_swap_id=right['id'],
                            alternating_quadruples=crossing,
                            colour_pairs_disjoint=not set(left['colour_pair']) & set(right['colour_pair']),
                            actual_root_incidence='UNASSIGNED'))
        examples = [r for r in pairs if r['a'] == 0 and r['b'] == 1
                    and r['a_frame_swap_id'] == f'KT{sigma}-q1-c03-B0'
                    and r['b_frame_swap_id'] == f'KT{sigma}-q1-c12-B1']
        assert examples
        tables.append(dict(
            sigma=sigma, rejected_q_indices=[i for i in range(10) if not sigma >> i & 1],
            partition_rows=partition_rows, transport_records=[records[k] for k in sorted(records)],
            joint_endpoint_pairs=pairs, joint_pair_counts_by_q_and_edge=coverage,
            named_noninterlacing_table_witness=examples[0],
            summary=dict(partitions=len(partition_rows), transport_records=len(records),
                         joint_endpoint_pairs=len(pairs), alternating_joint_pairs=0,
                         q_edge_entries_with_joint_pair=sum(n > 0 for ns in coverage.values() for n in ns))))
    return dict(
        scope='Complete single-block swaps of frame noncrossing partitions for fixed labels 933/941; '
              'existential necessary index, not source realization or root linkage.',
        side_rule='frame_sides labels block contacts at a/b only. Root-origin side cannot be '
                  'inferred from q, colour pair and block. See actual incidence in control witnesses.',
        common_colour_rule='Only one S4 renaming of all positions; literal q_prime is retained. No D5 quotient.',
        partition_generator_controls=generator_checks, tables=tables)


# Bounded local control: finish the first size layer, then stop enlargement.

FRAME = tuple(range(5))
Z, W = 5, 6
TERMINALS = (0, 1, Z, W)
FRAME_EDGES = tuple(sorted((min(i, (i+1)%5), max(i,(i+1)%5)) for i in FRAME))


def lists_extension(g, p, psi):
    lists = {v: [c for c in range(4) if all(psi.get(w) != c for w in g[v] if w not in p)] for v in p}
    order = sorted(p, key=lambda v: (len(lists[v]), -g.degree(v), v))
    assigned = {}
    def visit(i):
        if i == len(order):
            return dict(assigned)
        v = order[i]
        for c in lists[v]:
            if all(assigned.get(w) != c for w in g[v] if w in assigned):
                assigned[v] = c
                found = visit(i+1)
                if found is not None:
                    return found
                del assigned[v]
        return None
    return visit(0), {str(v): lists[v] for v in sorted(p)}


def external_colourings(g, p, q):
    for cz, cw in product(range(4), repeat=2):
        psi = dict(enumerate(q)) | {Z: cz, W: cw}
        if all(psi[u] != psi[v] for u, v in g.edges() if u not in p and v not in p):
            yield psi


def full_sigma(g, p):
    rows, witnesses = [], {}
    for qi, q in enumerate(REPS):
        for psi in external_colourings(g, p, q):
            ext, _ = lists_extension(g, p, psi)
            if ext is not None:
                rows.append(qi)
                witnesses[str(qi)] = {str(v): c for v, c in sorted((psi | ext).items())}
                break
    mask = sum(1 << i for i in rows)
    ordered = sorted(q for q in product(range(4), repeat=5)
                     if all(q[i] != q[(i+1)%5] for i in FRAME)
                     and REPS.index(normalize(q)) in rows)
    return dict(mask=mask, pattern_indices=rows, representative_rows=[list(REPS[i]) for i in rows],
                complete_ordered_rows=[list(q) for q in ordered], extension_witnesses=witnesses)


def disk_embedding(g):
    # H is connected and touches all five frame vertices.  Therefore in every
    # embedding the apex is on the opposite side of the frame from H.
    a = max(g) + 1
    aug = nx.Graph(g)
    aug.add_edges_from((a, b) for b in FRAME)
    planar, emb = nx.check_planarity(aug)
    if not planar:
        return None
    data = {v: [w for w in emb.neighbors_cw_order(v) if w != a] for v in sorted(g)}
    out = nx.PlanarEmbedding()
    out.set_data(data)
    out.check_structure()
    marked, faces = set(), []
    for u in sorted(g):
        for v in data[u]:
            if (u,v) not in marked:
                faces.append(out.traverse_face(u, v, marked))
    outer = next((f for f in faces if len(f) == 5 and set(f) == set(FRAME)), None)
    assert outer is not None, data
    return dict(rotation={str(v): data[v] for v in sorted(data)}, faces=faces, outer_face=outer)


def hub_test(g, p, psi):
    ext = set(g) - set(p)
    neighbors = set().union(*(set(g[v]) - set(p) for v in p))
    palette = sorted({psi[v] for v in neighbors})
    candidates = {}
    for c in palette:
        required = {v for v in neighbors if psi[v] == c}
        optional = sorted(ext-neighbors)
        bags = []
        for bits in range(1 << len(optional)):
            bag = required | {v for j,v in enumerate(optional) if bits >> j & 1}
            if nx.is_connected(g.subgraph(bag)):
                bags.append(tuple(sorted(bag)))
        candidates[c] = sorted(bags)
    chosen = []
    def visit(i):
        if i == len(palette):
            return list(chosen)
        for bag in candidates[palette[i]]:
            s = set(bag)
            if any(s.intersection(old) for old in chosen):
                continue
            if any(not any(g.has_edge(v,w) for v in bag for w in old) for old in chosen):
                continue
            chosen.append(bag)
            found = visit(i+1)
            if found is not None:
                return found
            chosen.pop()
        return None
    found = visit(0)
    return dict(feasible=found is not None, colors=palette, neighbor_vertices=sorted(neighbors),
                connected_candidate_bags={str(c): [list(b) for b in candidates[c]] for c in palette},
                witness_bags=None if found is None else [list(b) for b in found])


def boundary_contact_order(g, p, embedding):
    # Face of G[P] using rotations restricted from the certified disk embedding.
    # Each dart from P to G-P is placed at its actual corner. For P an edge or
    # tree this is an ordinary contour walk; repeated contacts retain identity.
    rotation = {v: embedding['rotation'][str(v)] for v in g}
    if len(p) == 1:
        v = next(iter(p))
        return [[v,w] for w in rotation[v] if w not in p]
    interior = nx.PlanarEmbedding()
    interior.set_data({v: [w for w in rotation[v] if w in p] for v in p})
    marked, walks = set(), []
    for u in sorted(p):
        for v in interior.neighbors_cw_order(u):
            if (u,v) not in marked:
                walk = interior.traverse_face(u,v,marked)
                contacts=[]
                for i,cur in enumerate(walk):
                    before, after = walk[i-1], walk[(i+1)%len(walk)]
                    nbrs=rotation[cur]
                    j=(nbrs.index(before)+1)%len(nbrs)
                    while nbrs[j] != after:
                        if nbrs[j] not in p:
                            contacts.append([cur,nbrs[j]])
                        j=(j+1)%len(nbrs)
                walks.append(contacts)
    # H-P is connected, so all external attachments are in a common face of P.
    contacts = max(walks,key=len)
    assert len(contacts) == sum(len(set(g[v])-p) for v in p), (walks,p)
    return contacts


def alternating_contact_test(contacts):
    """Exact named a-root-color1-b-root-color2 incidence test on the P contour."""
    n=len(contacts)
    for begin in range(n):
        cyclic=[(begin+j)%n for j in range(n)]
        for local in combinations(range(n),4):
            indices=[cyclic[j] for j in local]
            terminals=[contacts[j][1] for j in indices]
            if terminals in ([0,Z,1,W],[0,W,1,Z]):
                return dict(incidence_indices=indices, incidences=[contacts[j] for j in indices],
                            terminal_order=terminals)
    return None


def alternating_path_test(g, p, contacts):
    # Conservative genuine alternating obstruction predicate: four actual
    # contact incidences alternating around the P face, with two vertex-disjoint
    # external paths between the opposite pairs. Save paths if one exists.
    ext = g.subgraph(set(g)-p)
    for inds in combinations(range(len(contacts)),4):
        a,b,c,d = [contacts[i][1] for i in inds]
        if len({a,b,c,d}) != 4:
            continue
        for path in nx.all_simple_paths(ext,a,c):
            remaining = ext.subgraph(set(ext)-set(path))
            if b in remaining and d in remaining and nx.has_path(remaining,b,d):
                return dict(incidence_indices=list(inds),contact_vertices=[a,b,c,d],
                            path_ac=path,path_bd=nx.shortest_path(remaining,b,d))
    return None


def kempe_swaps(g,p,psi,sigma):
    ext=g.subgraph(set(g)-p)
    result=[]
    for pair in combinations(range(4),2):
        sub=ext.subgraph(v for v in ext if psi[v] in pair)
        for chain in sorted((sorted(c) for c in nx.connected_components(sub))):
            new=dict(psi)
            for v in chain:
                new[v] = pair[1] if psi[v] == pair[0] else pair[0]
            q=tuple(new[i] for i in FRAME)
            extension,lists=lists_extension(g,p,new)
            hubs=hub_test(g,p,new)
            result.append(dict(color_pair=list(pair),vertices=chain,frame_block=sorted(set(chain)&set(FRAME)),
                               touches_neighbor=any(v in hubs['neighbor_vertices'] for v in chain),
                               roots_in_chain=sorted(set(chain)&{Z,W}),q_prime=list(q),
                               neighbor_incidences=[[v,w] for v in sorted(p) for w in sorted(g[v]) if w in chain],
                               frame_side=('both' if 0 in chain and 1 in chain else 'a' if 0 in chain else 'b' if 1 in chain else 'neither'),
                               psi_prime={str(v):c for v,c in sorted(new.items())},
                               q_prime_in_actual_sigma=REPS.index(normalize(q)) in sigma['pattern_indices'],
                               normalized_q_prime=list(normalize(q)),pattern_prime=REPS.index(normalize(q)),
                               extends=extension is not None,
                               extension=None if extension is None else {str(v):c for v,c in sorted(extension.items())},
                               hubs_feasible=hubs['feasible'],hub_witness=hubs['witness_bags'],lists=lists))
    return result


def independent_witness_checks(first):
    if first is None:
        return None
    g=nx.Graph()
    g.add_nodes_from(first['vertices'])
    g.add_edges_from(first['edges'])
    p=set(first['piece'])
    psi={int(v):c for v,c in first['psi'].items()}
    assert all(psi[u]!=psi[v] for u,v in g.edges() if u not in p and v not in p)
    inner=sorted(set(g)-set(FRAME))
    raw_assignments=0
    def brute_sigma(h, expected):
        nonlocal raw_assignments
        accepted=[]
        for qi,q in enumerate(REPS):
            found=False
            for colours in product(range(4),repeat=len(inner)):
                raw_assignments+=1
                f=dict(enumerate(q))|dict(zip(inner,colours))
                if all(f[u]!=f[v] for u,v in h.edges()):
                    found=True
            if found:
                accepted.append(qi)
        assert accepted==expected['pattern_indices']
        independent_orbit={tuple(perm[c] for c in REPS[qi]) for qi in accepted for perm in permutations(range(4))}
        assert independent_orbit==set(map(tuple,expected['complete_ordered_rows']))
        for qi,colouring in expected['extension_witnesses'].items():
            f={int(v):c for v,c in colouring.items()}
            assert tuple(f[b] for b in FRAME)==REPS[int(qi)]
            assert all(f[u]!=f[v] for u,v in h.edges())
    brute_sigma(g,first['full_sigma'])
    for deletion in first['edge_deletions']:
        deleted=nx.Graph(g)
        deleted.remove_edge(*deletion['edge'])
        brute_sigma(deleted,deletion['full_sigma'])
    # Independent hub candidate enumeration ranges over every external subset,
    # rather than only adding non-neighbors to each required color group.
    neighbors=set(first['hub_search']['neighbor_vertices'])
    external=sorted(set(g)-p)
    bags=first['hub_search']['connected_candidate_bags']
    independent={}
    for color in first['hub_search']['colors']:
        required={v for v in neighbors if psi[v]==color}
        forbidden=neighbors-required
        candidates=[]
        for bits in range(1<<len(external)):
            bag={v for i,v in enumerate(external) if bits>>i&1}
            if required<=bag and not forbidden.intersection(bag) and nx.is_connected(g.subgraph(bag)):
                candidates.append(tuple(sorted(bag)))
        independent[color]=sorted(candidates)
        assert independent[color]==list(map(tuple,bags[str(color)]))
    tuples=0
    feasible=False
    for candidate in product(*(independent[c] for c in sorted(independent))):
        tuples+=1
        if any(set(a)&set(b) for a,b in combinations(candidate,2)):
            continue
        if all(any(g.has_edge(u,v) for u in a for v in b) for a,b in combinations(candidate,2)):
            feasible=True
    assert feasible==first['hub_search']['feasible']
    contact_terminals=[w for v,w in first['piece_face_contacts']]
    assert sorted(contact_terminals)==[0,1,Z,W] # This stop witness has one contact per terminal.
    assert alternating_contact_test(first['piece_face_contacts']) is None
    return dict(bruteforce_private_colour_assignments=raw_assignments,
                relations_checked=1+len(first['edge_deletions']),complete_ordered_S4_orbits_checked=True,
                independent_all_external_subsets_hub_search=True,independent_hub_candidate_tuples=tuples,
                unique_four_terminal_contour_noninterlacing=True)


def small_control(max_p=6):
    assert nx.__version__ == '3.5'
    counts=Counter(classification_hubs=0,classification_alternating_blocker=0,classification_other=0)
    first=None
    first_found_n=None
    graph_rows=[]
    classification_rows=[]
    for pg in nx.graph_atlas_g()[1:]:
        n=len(pg)
        if n>max_p or not nx.is_connected(pg) or max(dict(pg.degree()).values())>4:
            continue
        counts['connected_P_atlas_representatives']+=1
        p=set(range(7,7+n))
        pe=sorted((u+7,v+7) for u,v in pg.edges())
        choices=[list(combinations(TERMINALS,4-pg.degree(v))) for v in range(n)]
        for wiring in product(*choices):
            counts['P_terminal_wirings']+=1
            for zm,wm in product(range(32),repeat=2):
                counts['graph_wirings_considered']+=1
                g=nx.Graph()
                g.add_nodes_from(range(7+n))
                g.add_edges_from(FRAME_EDGES)
                g.add_edge(Z,W)
                g.add_edges_from(pe)
                g.add_edges_from((v+7,t) for v,ts in enumerate(wiring) for t in ts)
                g.add_edges_from((Z,b) for b in FRAME if zm >> b & 1)
                g.add_edges_from((W,b) for b in FRAME if wm >> b & 1)
                if set(TERMINALS)&set().union(*(set(g[v]) for v in p)) != set(TERMINALS):
                    continue
                if g.degree(Z)<5 or g.degree(W)<5:
                    continue
                if any(not(set(g[b])-set(FRAME)) for b in FRAME):
                    continue
                counts['actual_root_and_full_frame_wirings']+=1
                embedding=disk_embedding(g)
                if embedding is None:
                    continue
                counts['disk_wirings']+=1
                assert all(g.degree(v)==4 for v in p)
                sigma=full_sigma(g,p)
                counts['disk_masks_'+str(sigma['mask'])]+=1
                graph_id=f'P{n}-disk-{len(graph_rows)+1:03d}'
                graph_rows.append(dict(id=graph_id,n=n,p_edges=[list(e) for e in pe],wiring=[list(ts) for ts in wiring],
                                       z_spoke_mask=zm,w_spoke_mask=wm,edges=[list(e) for e in sorted(g.edges())],
                                       full_sigma=sigma,embedding=embedding))
                for qi,q in enumerate(REPS):
                    if qi in sigma['pattern_indices']:
                        continue
                    for psi in external_colourings(g,p,q):
                        counts['rejected_external_colourings']+=1
                        extension,lists=lists_extension(g,p,psi)
                        assert extension is None
                        hubs=hub_test(g,p,psi)
                        contacts=boundary_contact_order(g,p,embedding)
                        crossing=alternating_contact_test(contacts)
                        path_control=alternating_path_test(g,p,contacts)
                        assert path_control is None, 'Alternating disjoint paths cannot inhabit one planar face'
                        kind='hubs' if hubs['feasible'] else 'alternating_blocker' if crossing else 'other'
                        classification_rows.append(dict(id=f'{graph_id}-psi-{len(classification_rows)+1:03d}',graph_id=graph_id,
                            q=list(q),pattern_index=qi,psi={str(v):c for v,c in sorted(psi.items())},classification=kind,
                            piece_face_contacts=contacts,alternating_contact_certificate=crossing,hub_search=hubs,
                            independent_disjoint_alternating_paths=path_control))
                        counts['classification_'+kind]+=1
                        assert not hubs['feasible'], 'Finite planar hub-principle counterexample'
                        if kind=='other' and first is None:
                            first_found_n=n
                            first=dict(id=f'P{n}-witness-001',vertices=list(g),edges=[list(e) for e in sorted(g.edges())],
                                       frame=list(FRAME),piece=sorted(p),roots=[Z,W],
                                       degrees={str(v):g.degree(v) for v in sorted(g)},actual_support=sorted(set().union(*(set(g[v])&set(FRAME) for v in p))),
                                       root_neighbors=sorted(set().union(*(set(g[v])&{Z,W} for v in p))),
                                       psi={str(v):c for v,c in sorted(psi.items())},q=list(q),pattern_index=qi,
                                       lists=lists,full_sigma=sigma,embedding=embedding,hub_search=hubs,
                                       piece_face_contacts=contacts,alternating_blocker=crossing,classification=kind,
                                       independent_disjoint_alternating_paths=path_control,
                                       fixed_933_941_source=sigma['mask'] in (933,941),kempe_swaps=kempe_swaps(g,p,psi,sigma),
                                       vertex_names={str(v):('a=b0' if v==0 else 'b=b1' if v==1 else 'z' if v==Z else 'w' if v==W else f'b{v}' if v in FRAME else f'p{v-7}') for v in g},
                                       epsilon=sum(g.degree(v)-4 for v in g if v not in FRAME),
                                       edge_deletions=[] )
                            for e in sorted(g.edges()):
                                if tuple(sorted(e)) in FRAME_EDGES:
                                    continue
                                deleted=nx.Graph(g)
                                deleted.remove_edge(*e)
                                deletion_sigma=full_sigma(deleted,p)
                                gained=sorted(set(deletion_sigma['pattern_indices'])-set(sigma['pattern_indices']))
                                assert gained
                                first['edge_deletions'].append(dict(edge=list(e),full_sigma=deletion_sigma,
                                    gained_pattern_indices=gained,critical=True))
                            first['sigma_edge_minimal']=all(row['critical'] for row in first['edge_deletions'])
                            first['T4_all_accepted']=set((2,5,7,8,9))<=set(sigma['pattern_indices'])
        # Stop enlargement once the required named stop witness was found.
        if first_found_n==n:
            break
    assert len(classification_rows) == counts['rejected_external_colourings']
    assert sum(counts['classification_' + kind] for kind in
               ('hubs', 'alternating_blocker', 'other')) == len(classification_rows)
    return dict(networkx_version=nx.__version__,domain=dict(max_P_vertices_requested=max_p,
                largest_P_vertices_exhausted=first_found_n or max_p,atlas_P_isomorphism_representatives=True,
                all_labeled_terminal_attachments=True,terminals=list(TERMINALS),P_full_degree=4,
                roots_adjacent=True,roots_full_degree_at_least=5,all_frame_vertices_touched=True,
                root_spoke_masks_exhausted=[0,31],inner_remainder_exactly=[Z,W],
                disk_predicate='Planarity after adding temporary apex adjacent to all C5 vertices; saved outer C5 face.',
                graph_isomorphism_quotient=False,stops_enlargement_after_first_other=True),
                classification_predicates=dict(hubs='Exact theorem-B bags: connected, disjoint, pairwise adjacent, cover N(P), monochromatic only on N(P), one bag per neighbor color.',
                alternating_blocker='Actual P-face contact incidences contain cyclic a-z-b-w or a-w-b-z; a=0,b=1,z=5,w=6 have distinct witness colors.',
                other='Neither certified predicate holds; this tests the named four-terminal cyclic interlacing type, not unspecified broader blocker definitions.'),
                counts=dict(sorted(counts.items())),disk_graph_rows=graph_rows,classification_rows=classification_rows,first_other=first,
                independent_stop_witness_checks=independent_witness_checks(first),
                summary=dict(exhausted_P_vertices=first_found_n or max_p,disk_graphs=counts['disk_wirings'],
                    rejected_colorings=counts['rejected_external_colourings'],hubs=counts['classification_hubs'],
                    alternating_blockers=counts['classification_alternating_blocker'],other=counts['classification_other'],
                    stop_witness=None if first is None else first['id'],
                    stop_witness_mask=None if first is None else first['full_sigma']['mask'],
                    fixed_source_K_counterexample=False),
                scope='Finite local calibration. A mask other than 933 or 941 is not a counterexample to fixed-source K.')



def build():
    assert nx.__version__ == '3.5', 'Use networkx==3.5 for this certificate.'
    tables = transport_tables()
    control = small_control()
    return dict(
        schema='c5-kempe-transport-v1', base_commit='ca3870f9b79684c2100480d0dc04523899666928',
        trust=dict(paper='Conditional swap observation and finite-table insufficiency only.',
                   external='Existing Theorem B dependencies are not rerun; no 4CT oracle.',
                   python='Exact finite frame index and bounded wiring/colouring/rotation certificates.',
                   lean='No new Lean theorem; lake build not run.'),
        inputs={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                for p in (CATALOGUE, ROOT / 'scripts/c5_kempe_screen.py', Path(__file__))},
        networkx_version=nx.__version__, transport=tables, control=control,
        summary=dict(tables={str(t['sigma']): t['summary'] for t in tables['tables']},
                     control=control['summary']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path, default=OUT)
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode()
    witness = result['control']['first_other']
    assert witness is not None, 'The bounded control must retain its named stop witness.'
    witness_path = args.output.parent / (witness['id'] + '.json')
    witness_payload = (json.dumps(witness, indent=2, sort_keys=True) + '\n').encode()
    if args.check:
        assert args.output.read_bytes() == payload, f'Certificate differs: {args.output}'
        assert witness_path.read_bytes() == witness_payload, f'Witness differs: {witness_path}'
    else:
        assert not args.output.exists(), f'Refusing to overwrite: {args.output}'
        assert not witness_path.exists(), f'Refusing to overwrite: {witness_path}'
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as f:
            f.write(payload)
        with witness_path.open('xb') as f:
            f.write(witness_payload)
    print(json.dumps(result['summary'], sort_keys=True))
    print('CHECK OK' if args.check else f'CREATED {args.output.relative_to(ROOT) if args.output.is_relative_to(ROOT) else args.output}')


if __name__ == '__main__':
    main()
