#!/usr/bin/env python3
"""Full original-embedding boundary certificate for two-return differences.

The inputs are complete original sources and literal colourings. Attachment
sets, midpoint contours and their projected original closed walks are distinct
objects. No bound or simplicity is imposed on an interface.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'audits/2026-10-30-c5-d2-separation'


def edge(a, b):
    return tuple(sorted((a, b)))


def parts(adj, vertices):
    unseen, result = set(vertices), []
    while unseen:
        first = min(unseen)
        unseen.remove(first)
        todo = [first]
        for a in todo:
            for b in sorted(adj[a] & unseen):
                unseen.remove(b)
                todo.append(b)
        result.append(sorted(todo))
    return sorted(result)


def cycles(adj, allowed, maximum=None):
    allowed = set(allowed)
    maximum = len(allowed) if maximum is None else maximum
    result = []
    for first in sorted(allowed):
        def visit(path):
            if len(path) >= 3 and first in adj[path[-1]] and path[1] < path[-1]:
                result.append(path)
            if len(path) < maximum:
                for v in sorted(adj[path[-1]] & allowed):
                    if v > first and v not in path:
                        visit(path + [v])
        visit([first])
    return result


def sides(control, cycle):
    faces = control['sphere_faces']
    owners = defaultdict(list)
    for j, f in enumerate(faces):
        for i in range(3):
            owners[edge(f[i], f[(i + 1) % 3])].append(j)
    cut = {edge(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))}
    dual = {j: set() for j in range(len(faces))}
    for e, (a, b) in owners.items():
        if e not in cut:
            dual[a].add(b)
            dual[b].add(a)
    regions = parts(dual, dual)
    assert len(regions) == 2
    answer = [sorted({x for j in region for x in faces[j]} - set(cycle)) for region in regions]
    assert not set(answer[0]) & set(answer[1])
    assert set(answer[0]) | set(answer[1]) == set(range(control['n'])) - set(cycle)
    return sorted(answer, key=lambda a: (len(a), a))


def cycle_record(control, cycle, difference):
    ss = sides(control, cycle)
    center = control['center']
    assert center not in cycle
    near = next(s for s in ss if center in s)
    far = next(s for s in ss if center not in s)
    fixed = not set(cycle) & set(difference)
    return dict(cycle=cycle, sides=ss, center_side=near, opposite_side=far,
                fixed=fixed, contains_difference_opposite=bool(set(far) & set(difference)),
                rigidity_trigger=len(cycle) == 5 and len(near) >= 2 and fixed)


def compress_cyclic(trace):
    out = []
    for a in trace:
        if not out or a != out[-1]:
            out.append(a)
    if len(out) > 1 and out[-1] == out[0]:
        out.pop()
    return out


def contours(control, q):
    q = set(q)
    transition = {}
    for j, f in enumerate(control['sphere_faces']):
        if len(set(f) & q) in (1, 2):
            incoming = next((f[i], f[(i + 1) % 3]) for i in range(3)
                            if f[i] in q and f[(i + 1) % 3] not in q)
            outgoing = next((f[(i + 1) % 3], f[i]) for i in range(3)
                            if f[i] not in q and f[(i + 1) % 3] in q)
            assert incoming not in transition
            transition[incoming] = (outgoing, j)
    assert set(transition) == {x for x, _ in transition.values()}
    unseen, answer = set(transition), []
    while unseen:
        first, darts, face_ids, trace = min(unseen), [], [], []
        current = first
        while current in unseen:
            unseen.remove(current)
            darts.append(list(current))
            trace.append(current[1])
            current, face_id = transition[current]
            face_ids.append(face_id)
        assert current == first
        walk = compress_cyclic(trace)
        simple = len(walk) >= 3 and len(set(walk)) == len(walk)
        row = dict(crossing_darts=darts, face_ids=face_ids, external_trace=trace,
                   compressed_closed_walk=walk, is_original_simple_cycle=simple)
        if simple:
            row['sides'] = sides(control, walk)
        answer.append(row)
    return answer


def collar(control, adj):
    b, v, faces = control['boundary'], control['center'], control['sphere_faces']
    third = []
    for i, x in enumerate(b):
        y = b[(i + 1) % 5]
        third.append(next(next(z for z in f if z not in (x, y)) for f in faces
                          if x in f and y in f and v not in f))
    fans = []
    for i, x in enumerate(b):
        rotation = control['rotation'][x]
        left, right = third[(i - 1) % 5], third[i]
        candidates = []
        for sign in (-1, 1):
            path = [left]
            while path[-1] != right:
                path.append(rotation[(rotation.index(path[-1]) + sign) % len(rotation)])
            if not set(path) & (set(b) | {v}):
                candidates.append(path)
        assert len(candidates) == 1
        path = candidates[0]
        assert all(path[j + 1] in adj[path[j]] for j in range(len(path) - 1))
        fans.append(dict(boundary_vertex=x, vertices=path, internal_vertices=path[1:-1],
                         gap=right not in adj[left], degree=len(adj[x])))
    walk = [x for fan in fans for x in fan['vertices'][:-1]]
    return dict(third_vertices=third, fans=fans, walk=walk,
                is_original_simple_cycle=len(walk) >= 3 and len(set(walk)) == len(walk))


def facing_boundary(control, adj, q, attachment_cycles):
    """Face of the original induced v-component after deleting only Q."""
    region = next(p for p in parts(adj, set(adj) - set(q)) if control['center'] in p)
    rotation = {v: [x for x in control['rotation'][v] if x in region] for v in region}
    a, b, c = control['sphere_faces'][0]
    original = control['rotation'][b]
    orientation = -1 if original[(original.index(a) - 1) % len(original)] == c else 1
    assert all(control['rotation'][f[1]][(control['rotation'][f[1]].index(f[0]) + orientation)
               % len(control['rotation'][f[1]])] == f[2] for f in control['sphere_faces'])
    unseen = {(v, x) for v in region for x in rotation[v]}
    face_walks = []
    while unseen:
        first = current = min(unseen)
        walk = []
        while current in unseen:
            unseen.remove(current)
            a, b = current
            walk.append(a)
            row = rotation[b]
            current = (b, row[(row.index(a) + orientation) % len(row)])
        assert current == first
        face_walks.append(walk)
    # The Q-facing original triangle on every boundary dart has third in Q.
    third = {(f[i], f[(i + 1) % 3]): f[(i + 2) % 3]
             for f in control['sphere_faces'] for i in range(3)}
    candidates = [w for w in face_walks if all(third[(w[i], w[(i + 1) % len(w)])] in q
                                              for i in range(len(w)))]
    assert len(candidates) == 1
    walk = candidates[0]
    walk_edges = {edge(walk[i], walk[(i + 1) % len(walk)]) for i in range(len(walk))}
    separators = [row for row in attachment_cycles if set(q) <= set(row['opposite_side'])
                  and all(edge(row['cycle'][i], row['cycle'][(i + 1) % len(row['cycle'])]) in walk_edges
                          for i in range(len(row['cycle'])))]
    assert separators
    selected = min(separators, key=lambda row: (len(row['cycle']), row['cycle']))
    b = control['boundary']
    assert not walk_edges & {edge(b[i], b[(i + 1) % 5]) for i in range(5)}
    if control['premise_flags']['S5']:
        assert len(selected['cycle']) >= 6
    return dict(v_component_after_deleting_Q=region,
                induced_rotation_rows=[dict(vertex=v, rotation=rotation[v]) for v in region],
                Q_facing_face_boundary_closed_walk=walk,
                Q_facing_original_third_vertices=[third[(walk[i], walk[(i + 1) % len(walk)])] for i in range(len(walk))],
                selected_original_separator=selected)


def gluing(control, oadj, keep):
    vertices = set(oadj)
    far = vertices - keep
    pos = {v: i for i, v in enumerate(control['exterior_vertices'])}
    records = []
    for r, row in enumerate(control['rounds']):
        snapshots = [row['source_colors']] + [m['colors'] for m in row['moves']]
        for t, c in enumerate(snapshots):
            pairs = []
            for pair in combinations(range(4), 2):
                active = {v for v in vertices if c[pos[v]] in pair}
                full = parts(oadj, active)
                local = parts(oadj, active & keep)
                remote = parts(oadj, active & far)
                stars = [dict(component=p, attachments=sorted(set().union(*(oadj[v] for v in p)) & active & keep))
                         for p in remote]
                aux = {v: oadj[v] & active & keep for v in active & keep}
                for j, star in enumerate(stars):
                    key = control['n'] + j
                    aux[key] = set(star['attachments'])
                    for v in star['attachments']:
                        aux[v].add(key)
                composed = sorted(sorted(set(p) & keep) for p in parts(aux, aux) if set(p) & keep)
                projection = sorted(sorted(set(p) & keep) for p in full if set(p) & keep)
                assert composed == projection
                pairs.append(dict(pair=list(pair), full_components=full, local_components=local,
                                  remote_stars=stars, full_projection=projection,
                                  recomposed_projection=composed))
            records.append(dict(round=r, time=t, colors=c, all_six_pairs=pairs))
    return dict(kept_vertices=sorted(keep), remote_vertices=sorted(far),
                interface=sorted(v for v in keep if oadj[v] & far), snapshots=records)


def inspect(control):
    adj = {i: set(row) for i, row in enumerate(control['rotation'])}
    v, ext = control['center'], control['exterior_vertices']
    oadj = {x: adj[x] - {v} for x in ext}
    col = collar(control, adj)
    comparison_rows, gluing_rows, gluing_ids = [], [], {}
    for comparison in control['comparisons']:
        c, d = comparison['c'], comparison['d']
        difference = sorted(x for x, a, b in zip(ext, c, d) if a != b)
        assert difference and not set(difference) & (set(control['boundary']) | set(col['third_vertices']))
        components = []
        for q in parts(oadj, difference):
            attachment = sorted(set().union(*(adj[x] for x in q)) - set(q))
            assert not set(attachment) & set(difference) and v not in attachment
            traces = contours(control, q)
            assert {x for row in traces for x in row['external_trace']} == set(attachment)
            keep = frozenset(q + attachment)
            if keep not in gluing_ids:
                gluing_ids[keep] = len(gluing_rows)
                gluing_rows.append(gluing(control, oadj, set(keep)))
            component = dict(vertices=q, attachments=attachment, attachment_count=len(attachment),
                original_neighbor_rows=[dict(vertex=x, neighbors=sorted(adj[x]), rotation=control['rotation'][x]) for x in q],
                incident_original_face_ids=[j for j, f in enumerate(control['sphere_faces']) if set(f) & set(q)],
                contours=traces, all_attachment_simple_cycles=[cycle_record(control, cc, difference) for cc in cycles(adj, attachment)],
                gluing_record_id=gluing_ids[keep])
            component['v_facing_boundary'] = facing_boundary(control, adj, q, component['all_attachment_simple_cycles'])
            if control['premise_flags']['S5']:
                assert len(attachment) >= 6
            components.append(component)
        fixed5 = [cycle_record(control, cc, difference) for cc in cycles(adj, set(ext) - set(difference), 5) if len(cc) == 5]
        violations = [row for row in fixed5 if row['rigidity_trigger'] and row['contains_difference_opposite']]
        if control['premise_flags']['S5']:
            assert not violations
        comparison_rows.append(dict(source_iterate=comparison['source_iterate'], target_iterate=comparison['target_iterate'],
            difference_vertices=difference, components=components, fixed_five_cycles=fixed5,
            rigidity_violations=violations,
            collar_fixed=not bool(set(col['walk']) & set(difference))))
    return dict(name=control['name'], collar=col, comparisons=comparison_rows,
                full_O_gluing_records=gluing_rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=AUDIT / 'controls.json')
    parser.add_argument('--output', type=Path, default=AUDIT / 'separation-certificate.json')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    result = dict(schema='c5-d2-original-boundary-v1',
        source_sha256=sha256(args.input.read_bytes()).hexdigest(),
        producer_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        controls=[inspect(c) for c in data['controls']],
        scope='Legal S5 two-return prefix and Errera S5-negative period4. No legal fully blocked period4 witness.')
    encoded = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert args.output.read_text() == encoded
    else:
        args.output.write_text(encoded)
    print(json.dumps(dict(status='OK', controls=[dict(name=c['name'], collar=c['collar']['walk'],
        comparisons=[dict(D=r['difference_vertices'], attachment_counts=[q['attachment_count'] for q in r['components']],
                          contours=[q['contours'] for q in r['components']], violations=len(r['rigidity_violations'])) for r in c['comparisons']]) for c in result['controls']]), sort_keys=True))


if __name__ == '__main__':
    main()
