#!/usr/bin/env python3
"""Exact disk rotations and face-defined shields for the finite calibration.

The public functions are ``disk_embedding(vertices, edges, frame=FRAME)`` and
``piece_shield(certificate, piece)``.  Both return JSON-serializable dictionaries.
No colouring or support-gap choice is used.  The latter deletes edges by merging
their incident faces in the dual of the inherited, labelled disk embedding.

The input graph must be connected (the bare frame is allowed).  An isolated
private vertex has no location in an abstract rotation system; a caller wishing
to retain such a vertex must provide a separate placement certificate rather
than have this helper silently discard it.
"""

from collections import defaultdict

import networkx as nx


FRAME = tuple(range(5))


def _edge(a, b):
    return (a, b) if a < b else (b, a)


def _cycle(walk):
    """Canonical cyclic start, preserving orientation and repeated vertices."""
    walk = tuple(walk)
    return min(walk[i:] + walk[:i] for i in range(len(walk)))


def _embedding(rotation):
    embedding = nx.PlanarEmbedding()
    embedding.set_data(rotation)
    return embedding


def _facial_walks(embedding):
    seen = set()
    walks = []
    for a in sorted(embedding):
        for b in sorted(embedding[a]):
            if (a, b) not in seen:
                walks.append(_cycle(embedding.traverse_face(a, b, seen)))
    return sorted(walks)


def _darts(walk):
    return list(zip(walk, walk[1:] + walk[:1]))


def disk_embedding(vertices, edges, frame=FRAME):
    """Return a deterministic labelled disk embedding with ``frame`` outside.

    Nodes are integer labels, all explicitly retained.  Frame chords are
    rejected.  An apex adjacent to the five frame vertices supplies a wheel.
    Every private connected component lies in one wheel face.  Components in
    the five apex triangles are reflected across the corresponding frame edge
    into the wheel's pentagonal face.  This last step is needed for partial
    frame supports: merely removing an apex need not make the frame facial.
    """
    nodes = tuple(sorted(vertices))
    if len(nodes) != len(set(nodes)) or any(not isinstance(v, int) for v in nodes):
        raise ValueError('vertices must be distinct integer labels')
    frame = tuple(frame)
    if len(frame) != 5 or len(set(frame)) != 5 or not set(frame) <= set(nodes):
        raise ValueError('frame must be five distinct input vertices')
    input_edges = tuple(tuple(e) for e in edges)
    if any(len(e) != 2 or e[0] == e[1] or not set(e) <= set(nodes)
           for e in input_edges):
        raise ValueError('invalid edge or edge endpoint missing from vertices')
    edgelist = tuple(sorted({_edge(*e) for e in input_edges}))
    frame_edges = {_edge(frame[i], frame[(i + 1) % 5]) for i in range(5)}
    if not frame_edges <= set(edgelist):
        raise ValueError('input does not contain the specified frame cycle')
    if {e for e in edgelist if set(e) <= set(frame)} != frame_edges:
        raise ValueError('specified frame is not induced')
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edgelist)
    if not nx.is_connected(graph):
        raise ValueError('disconnected graph: private-component location needed')

    apex = max(nodes) + 1
    augmented = nx.Graph(graph)
    augmented.add_node(apex)
    augmented.add_edges_from((apex, v) for v in frame)
    planar, raw = nx.check_planarity(augmented)
    if not planar:
        raise ValueError('graph admits no disk embedding with this frame')
    rotation = raw.get_data()
    wheel_vertices = set(frame) | {apex}
    wheel = _embedding({v: [w for w in rotation[v] if w in wheel_vertices]
                        for v in sorted(wheel_vertices)})
    # In the wheel, orient the pentagonal *inner* face backwards.  Once its
    # apex-side components are reflected inward, the outer face is frame order.
    if wheel.traverse_face(frame[0], frame[1]) == list(frame):
        rotation = {v: list(reversed(nbrs)) for v, nbrs in rotation.items()}
    wheel = _embedding({v: [w for w in rotation[v] if w in wheel_vertices]
                        for v in sorted(wheel_vertices)})
    reverse_frame = [frame[0], *reversed(frame[1:])]
    if wheel.traverse_face(frame[0], frame[-1]) != reverse_frame:
        raise AssertionError('augmented wheel does not have its pentagonal face')

    blocks = {}
    attachment_hosts = defaultdict(set)
    for i, v in enumerate(frame):
        prev, next_ = frame[(i - 1) % 5], frame[(i + 1) % 5]
        nbrs = rotation[v]
        start = nbrs.index(prev)
        nbrs = nbrs[start:] + nbrs[:start]
        j, k = nbrs.index(next_), nbrs.index(apex)
        if not 0 < j < k:
            raise AssertionError('wheel sectors do not follow the fixed order')
        inner, right, left = nbrs[1:j], nbrs[j + 1:k], nbrs[k + 1:]
        blocks[v] = (inner, right, left)
        for w in inner:
            attachment_hosts[w].add(('inner', -1))
        for w in right:
            attachment_hosts[w].add(('triangle', i))
        for w in left:
            attachment_hosts[w].add(('triangle', (i - 1) % 5))

    private = set(nodes) - set(frame)
    reflected, placements = set(), []
    for comp in sorted(nx.connected_components(graph.subgraph(private)),
                       key=lambda c: tuple(sorted(c))):
        hosts = set().union(*(attachment_hosts[v] for v in comp))
        if len(hosts) != 1:
            raise AssertionError('private component has no unique wheel face')
        host = next(iter(hosts))
        if host[0] == 'triangle':
            reflected.update(comp)
        placements.append(dict(vertices=sorted(comp), wheel_face=list(host),
                               reflected_into_disk=host[0] == 'triangle'))

    disk_rotation = {}
    for v in nodes:
        if v in private:
            nbrs = rotation[v]
            disk_rotation[v] = list(reversed(nbrs)) if v in reflected else nbrs[:]
        else:
            i = frame.index(v)
            inner, right, left = blocks[v]
            disk_rotation[v] = ([frame[(i - 1) % 5]] + list(reversed(left))
                                + inner + list(reversed(right))
                                + [frame[(i + 1) % 5]])
    disk = _embedding(disk_rotation)
    disk.check_structure()
    if disk.traverse_face(frame[0], frame[1]) != list(frame):
        raise AssertionError('frame was not made the outer facial walk')
    faces = _facial_walks(disk)
    outer = _cycle(frame)
    faces.remove(outer)
    faces = [outer] + faces
    if len(nodes) - len(edgelist) + len(faces) != 2:
        raise AssertionError('rotation system fails the connected Euler identity')
    canonical_rotation = []
    for v in nodes:
        nbrs = list(disk.neighbors_cw_order(v))
        start = nbrs.index(min(nbrs))
        canonical_rotation.append(dict(vertex=v, clockwise=nbrs[start:] + nbrs[:start]))
    return dict(vertices=list(nodes), edges=[list(e) for e in edgelist],
                frame=list(frame), outer=list(frame), outer_face_id=0,
                rotation=canonical_rotation,
                faces=[list(f) for f in faces],
                private_component_wheel_placements=placements,
                embedding_method='networkx-3.5 apex wheel, exterior-triangle '
                                 'reflection, inherited clockwise rotation')


def piece_shield(certificate, piece):
    """Compute the literal face-defined shield of a connected one-sided piece.

    ``F_P`` is found by dual merging across every edge absent from
    ``K_P = B union G[P] union E(P,B)``.  All surviving boundary walks of that
    same region are returned; this also handles K_P with several components.
    """
    nodes, frame = set(certificate['vertices']), tuple(certificate['frame'])
    p = set(piece)
    if not p or not p <= nodes - set(frame):
        raise ValueError('piece must be a nonempty subset of private vertices')
    edges = {_edge(*e) for e in certificate['edges']}
    graph = nx.Graph()
    graph.add_nodes_from(sorted(nodes))
    graph.add_edges_from(sorted(edges))
    if not nx.is_connected(graph.subgraph(p)):
        raise ValueError('piece is not connected')
    rest = nodes - set(frame) - p
    if not rest or not nx.is_connected(graph.subgraph(rest)):
        raise ValueError('piece is not one-sided')
    rotation = {r['vertex']: r['clockwise'] for r in certificate['rotation']}
    faces = [tuple(f) for f in certificate['faces']]
    dart_face = {d: i for i, f in enumerate(faces) for d in _darts(f)}
    if len(dart_face) != 2 * len(edges):
        raise AssertionError('certificate faces do not partition graph darts')
    parent = list(range(len(faces)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        i, j = find(i), find(j)
        parent[max(i, j)] = min(i, j)

    frame_edges = {_edge(frame[i], frame[(i + 1) % 5]) for i in range(5)}
    k_nodes = set(frame) | p
    k_edges = {e for e in edges if e in frame_edges or
               set(e) <= k_nodes and set(e) & p}
    deleted = sorted(edges - k_edges)
    for a, b in deleted:
        union(dart_face[a, b], dart_face[b, a])
    rest_regions = {find(dart_face[v, w]) for v in rest for w in graph[v]}
    if len(rest_regions) != 1:
        raise AssertionError('connected H-P does not occupy one K_P face')
    region = next(iter(rest_regions))
    if region == find(certificate['outer_face_id']):
        raise AssertionError('rest-containing region is not an inner face')
    merged_faces = [i for i in range(len(faces)) if find(i) == region]
    k_rotation = {v: [w for w in rotation[v] if _edge(v, w) in k_edges]
                  for v in sorted(k_nodes)}
    k_embedding = _embedding(k_rotation)
    boundary = []
    for walk in _facial_walks(k_embedding):
        groups = {find(dart_face[d]) for d in _darts(walk)}
        if len(groups) != 1:
            raise AssertionError('inherited K_P walk crosses merged face regions')
        if region in groups:
            boundary.append(list(walk))
    # An isolated point of K_P is a degenerate boundary component.  Its
    # position is inherited through its original incident graph faces.
    for v in sorted(k_nodes):
        if not k_rotation[v]:
            groups = {find(dart_face[v, w]) for w in graph[v]}
            if len(groups) != 1:
                raise AssertionError('isolated K_P vertex has ambiguous region')
            if region in groups:
                boundary.append([v])
    boundary.sort()
    on_face = {e for e in frame_edges
               if any(find(dart_face[d]) == region for d in (e, e[::-1]))}
    support = {w for v in p for w in graph[v] if w in frame}
    shield = frame_edges - on_face
    return dict(piece=sorted(p), rest=sorted(rest), support=sorted(support),
                k_vertices=sorted(k_nodes), k_edges=[list(e) for e in sorted(k_edges)],
                deleted_edges=[list(e) for e in deleted],
                rest_containing_original_face_ids=merged_faces,
                rest_containing_face_boundary_walks=boundary,
                frame_edges_on_rest_face=[list(e) for e in sorted(on_face)],
                shield_edges=[list(e) for e in sorted(shield)],
                shield_vertices=sorted({v for e in shield for v in e}),
                shield_length=len(shield),
                method='dual face merges across deleted edges in the saved '
                       'labelled disk rotation')
