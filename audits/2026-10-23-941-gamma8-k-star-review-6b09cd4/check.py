#!/usr/bin/env python3
"""Independent wheel/collar review; source coverage is the paper proof."""
import argparse
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
CAPS = 'audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json'


def require(test, message):
    if not test:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def cyclic(row):
    return min(tuple(row[i:] + row[:i]) for i in range(len(row)))


def custody():
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    require(manifest['base'] == BASE, 'BASE')
    for row in manifest['authority']:
        for path in [ROOT / row['path'], HERE / row['snapshot']]:
            data = path.read_bytes()
            require(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], 'authority drift: ' + str(path))
    return dict(authority_files=len(manifest['authority']), drift=0)


def reconstruct(seed):
    # Generate the full graph from central spokes and the two triangulated strips.
    ns = ['n' + str(i) for i in range(6)]
    qs = ['q' + str(i) for i in range(6)]
    faces = []
    for i in range(6):
        j, p = (i + 1) % 6, (i - 1) % 6
        faces.extend([['T', ns[i], ns[j]], [ns[j], ns[i], qs[i]], [ns[i], qs[p], qs[i]]])
    edges = {edge(a, b) for f in faces for a, b in zip(f, f[1:] + f[:1])}
    vertices = {'T', *ns, *qs}
    require(len(vertices) == 13 and len(edges) == 30 and len(faces) == 18, 'wheel cap sizes')
    directed = {}
    for f in faces:
        for a, b in zip(f, f[1:] + f[:1]):
            directed[a, b] = directed.get((a, b), 0) + 1
    require(max(directed.values()) == 1, 'repeated face incidence')
    boundary = {(a, b) for a, b in directed if (b, a) not in directed}
    require(boundary == {(qs[i], qs[(i + 1) % 6]) for i in range(6)}, 'same oriented outer boundary')
    for v in ['T', *ns]:
        neighbors = {b if a == v else a for a, b in edges if v in (a, b)}
        want = set(ns) if v == 'T' else {'T', ns[(ns.index(v) - 1) % 6], ns[(ns.index(v) + 1) % 6], qs[(ns.index(v) - 1) % 6], qs[ns.index(v)]}
        require(neighbors == want, 'complete private star: ' + v)
        lk_edges = {edge(*[x for x in f if x != v]) for f in faces if v in f}
        require(len(lk_edges) == len(neighbors), 'private full cyclic star')
        require(all(sum(x in e for e in lk_edges) == 2 for x in neighbors), 'private link not cycle')
    # No source K point may touch a nonconsecutive pair of T-link vertices:
    # n_i-T-n_j-k would be an induced original C4.
    possible_contacts = [tuple(s) for n in range(7) for s in itertools.combinations(range(6), n)
                         if all((b-a) % 6 in {1, 5} for a, b in itertools.combinations(s, 2))]
    require(len(possible_contacts) == 13 and max(map(len, possible_contacts)) == 2, 'C4 contact classification')
    extra_contacts = [s for s in possible_contacts if len(s) < 2]  # adjacent pair fixes k=q_i by original C3 face
    require(len(extra_contacts) == 7, 'extra K contact at most singleton')
    # Inserting the sole extra point in at most one outer path gives a 6/7 closed walk.
    parity = []
    randomizer = random.Random(seed)
    placements = [None, *range(6)]
    randomizer.shuffle(placements)
    for insertion in placements:
        word = []
        for i in range(6):
            word.append(qs[i])
            if insertion == i:
                word.append('w')
        proper = []
        for colors in itertools.product([0, 2], repeat=len(word)):
            if all(colors[i] != colors[(i + 1) % len(word)] for i in range(len(word))):
                proper.append(colors)
        require(len(proper) == (2 if insertion is None else 0), 'bipartite closed collar parity')
        parity.append(dict(insertion=insertion, length=len(word), proper_colorings=len(proper)))
    # Compare every edge and every consistently oriented face, rather than supports.
    caps = json.loads((HERE / 'frozen' / CAPS).read_text())['caps']
    mappings = {'L': ['zeta', 'x', 'p_x', 'U', 'p_d', 'd'], 'R': ['d', 'zeta', 'x', 'p_x', 'U', 'p_d']}
    n_image = ['r', 'tau', 's', 'b', 'y', 'a']
    isomorphisms = []
    for cap in caps:
        mapping = dict(T='T', **dict(zip(ns, n_image)), **dict(zip(qs, mappings[cap['core']])))
        mapped_edges = {edge(mapping[a], mapping[b]) for a, b in edges}
        mapped_faces = {cyclic([mapping[x] for x in f]) for f in faces}
        old_faces = {cyclic(f) for f in cap['oriented_actual_faces']}
        reverse_faces = {cyclic(list(reversed(f))) for f in cap['oriented_actual_faces']}
        require(mapped_edges == {edge(*e) for e in cap['edges']}, 'complete cap edges isomorphism')
        require(mapped_faces in [old_faces, reverse_faces], 'common face orientation isomorphism')
        require(len(set(mapping.values())) == 13, 'literal cap mapping injectivity')
        isomorphisms.append(dict(core=cap['core'], q_image=mappings[cap['core']], edge_count=len(mapped_edges), oriented_faces=len(mapped_faces)))
    return dict(vertices=sorted(vertices), edges=[list(e) for e in sorted(edges)],
                oriented_faces=sorted(faces), K_contact_sets=[list(s) for s in possible_contacts],
                extra_K_contact_sets=[list(s) for s in extra_contacts],
                parity=sorted(parity, key=lambda r: -1 if r['insertion'] is None else r['insertion']),
                old_cap_isomorphisms=isomorphisms)


def verify(certificate, actual):
    require(certificate['schema'] == '941-k-star-independent-review-v1' and certificate['base'] == BASE, 'certificate identity')
    require(certificate['reconstruction'] == actual, 'independent complete reconstruction')
    require(certificate['contract'] == dict(same_G_F=True, literal_phi_psi=True,
            complete_R_wheel=True, K_vertices_at_most=7, arbitrary_spectators=True,
            U_is_original_G_inner=True, U_F_link_not_closed=True), 'source contract')
    require(certificate['authority'] == dict(finite_control='triggered and holds',
            actual_source='not triggered', source_coverage='paper REVIEW sections 1-3',
            empty_M2_D6_Z6='excluded_by_conditional_sealed_cap_theorem',
            all_eleven_types='OPEN', general_wrong_side='OPEN', common_k=23,
            new_Lean=False, new_matching=False), 'authority boundary')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    ap.add_argument('--negative', action='store_true')
    args = ap.parse_args()
    frozen = custody()
    actual = reconstruct(args.seed)
    certificate = json.loads(args.certificate.read_text())
    verify(certificate, actual)
    rejected = []
    if args.negative:
        mutations = [
            ('drop_actual_face', lambda c: c['reconstruction']['oriented_faces'].pop()),
            ('add_T_link_chord', lambda c: c['reconstruction']['edges'].append(['n0', 'n3'])),
            ('give_extra_K_two_N_contacts', lambda c: c['reconstruction']['extra_K_contact_sets'].append([0, 1])),
            ('invent_odd_bipartite_collar', lambda c: c['reconstruction']['parity'][1].update(proper_colorings=2)),
            ('collapse_distinct_actual_contacts', lambda c: c['reconstruction']['old_cap_isomorphisms'][0]['q_image'].__setitem__(0, 'U')),
            ('promote_finite_to_actual_source', lambda c: c['authority'].update(actual_source='triggered and holds')),
            ('close_U_boundary_star', lambda c: c['contract'].update(U_F_link_not_closed=False)),
        ]
        for label, mutate in mutations:
            bad = copy.deepcopy(certificate)
            mutate(bad)
            try:
                verify(bad, actual)
            except ValueError:
                rejected.append(label)
            else:
                raise ValueError('negative accepted: ' + label)
    print(json.dumps(dict(status='PASS', seed=args.seed, custody=frozen,
        complete_cap=dict(vertices=13, edges=30, oriented_faces=18, private_full_stars=7),
        old_cap_isomorphisms=2, extra_K_contact_options=7,
        collar_parity_cases=7, odd_collar_survivors=0,
        source_realizability='not triggered', negative_rejected=rejected), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
