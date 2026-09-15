#!/usr/bin/env python3
"""Replay cut interfaces on the existing Errera transitions; no new graph search."""
import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path

from c5_edge_choices import EdgeModel, Move, ROOT
from c5_edge_states import TYPE_PAIRS
from c5_complementary_cube import encode, singleton_of

SOURCE = ROOT / 'artifacts/c5_cells/edge_choices.json'
OUT = ROOT / 'artifacts/c5_cells/cut_interfaces.json'


def partition(vertices, edges):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    unseen, parts = set(adj), []
    while unseen:
        queue = [min(unseen)]
        unseen.remove(queue[0])
        for u in queue:
            for v in sorted(adj[u] & unseen):
                unseen.remove(v)
                queue.append(v)
        parts.append(tuple(sorted(queue)))
    return tuple(parts)


def predict(interface):
    """Only the interface partition and added edges are needed here."""
    blocks = interface['blocks']
    owner = {p: i for i, b in enumerate(blocks) for p in b['ports']}
    joins = [(owner[u], owner[v]) for u, v in interface['added_ends']]
    parts = partition(range(len(blocks)), joins)
    terminals = [tuple(sorted(t for i in part for t in blocks[i]['terminals']))
                 for part in parts]
    assert all(len(ts) in (0, 2) for ts in terminals)
    return dict(pairings=sorted(ts for ts in terminals if ts),
                cycles=sum(not ts for ts in terminals))


def interfaces(model, c, action):
    """Delete cut edges first, then contract retained connected components.

    Closed components remain as blocks even when they have no interface ports.
    Internal face IDs and ordered boundary edge IDs are never renamed.
    """
    block = set(action.component)
    k = action.pair[0] ^ action.pair[1]
    old = [c[u] ^ c[v] for u, v in model.edges]
    cut = {e for e, (u, v) in enumerate(model.edges) if (u in block) != (v in block)}
    new = [t ^ k if e in cut else t for e, t in enumerate(old)]
    rows = []
    for types in TYPE_PAIRS:
        retained = [e for e, t in enumerate(old) if t in types and e not in cut]
        added = [e for e in sorted(cut) if new[e] in types]
        target_edges = retained + added
        vertices = set(range(model.dual.f)) | {
            v for e in target_edges for v in model.dual.ends[e]}
        ports = {v for e in cut for v in model.dual.ends[e]} & vertices
        parts = partition(vertices, [model.dual.ends[e] for e in retained])
        interface = dict(types=types,
            blocks=[dict(ports=sorted(set(part) & ports),
                         terminals=[v - model.dual.f for v in part if v >= model.dual.f])
                    for part in parts],
            added_ends=[model.dual.ends[e] for e in added])
        rows.append(dict(interface=interface, prediction=predict(interface),
                         retained_edges=retained, added_edges=added, retained_vertices=parts))
    return rows


def check_transition(model, c, action):
    d = model.apply(c, action)
    rows = interfaces(model, c, action)
    for row, actual in zip(rows, model.dual.systems(d)):
        assert row['prediction'] == dict(pairings=sorted(t for t, _ in actual if t),
                                         cycles=sum(not t for t, _ in actual))
    return rows


def report():
    source = json.loads(SOURCE.read_text())
    model = EdgeModel(source['graph'])
    fixed = source['structural_cycle_loss']
    reference = tuple(fixed['source'])
    exact = Move(tuple(fixed['event']['pair']), tuple(fixed['event']['component']))
    # Retain every supplied safe history, but compare distinct witnesses once.
    candidates = defaultdict(list)
    for stage in ('one_switch_compatible', 'prefix_safe_two_switches'):
        for i, b in enumerate(source['stages'][stage]['branches']):
            c = tuple(b['coloring'])
            if c[:5] == reference[:5] and model.view(c) == model.view(reference):
                current = tuple(source['seeds'][b['origin']])
                assert model.compatible(current)
                for index in b['history']:
                    event = source['transition_table'][index]
                    assert current == tuple(event['before'])
                    current = model.apply(current, Move(tuple(event['pair']), tuple(event['component'])))
                    assert current == tuple(event['after']) and model.compatible(current)
                assert current == c
                candidates[c].append(dict(stage=stage, branch=i, origin=b['origin'], history=b['history']))
    rows = []
    for c, histories in sorted(candidates.items()):
        action, = [a for a in model.actions(c) if a.pair == (1, 2) and 0 in a.component]
        d = model.apply(c, action)
        event = model.edge_replay(c, action)
        escapes = [dict(pair=a.pair, component=a.component, target=model.apply(d, a),
                        singleton=singleton_of(model.apply(d, a)))
                   for a in model.actions(d) if singleton_of(model.apply(d, a)) in (1, 3, 4)]
        if exact not in model.actions(c):
            try:
                model.apply(c, exact)
            except ValueError:
                pass
            else:
                raise AssertionError('A stale component must be rejected.')
        rows.append(dict(source=c, histories=histories, exact_action_legal=exact in model.actions(c),
            source_relation=model.view(c), source_cycles=model.dual.state(c, True)[-1],
            action=dict(pair=action.pair, component=action.component), event=event,
            target_relation=model.view(d), target_compatible=model.compatible(d),
            immediate_escapes=escapes, interfaces=check_transition(model, c, action)))
    assert len(rows) == 4 and sum(r['exact_action_legal'] for r in rows) == 1
    assert len({tuple(r['source_cycles']) for r in rows}) == 1
    assert sum(r['target_compatible'] for r in rows) == 2
    assert all(r['event']['systems'][2]['cycle_count_before'] == 2 and
               r['event']['systems'][2]['cycle_count_after'] == 1 for r in rows)
    # Audit the new reconstruction against every previously certified transition.
    audit = []
    for event in source['transition_table']:
        c = tuple(event['before'])
        action = Move(tuple(event['pair']), tuple(event['component']))
        assert model.apply(c, action) == tuple(event['after'])
        audit.append(check_transition(model, c, action))
    # Negative control: erase retained connectivity by identifying every port.
    # This changes a real prediction and therefore cannot replace the interface.
    negative = None
    for ri, row in enumerate(rows):
        for si, system in enumerate(row['interfaces']):
            original = system['interface']
            bad = dict(original, blocks=[dict(
                ports=sorted(p for b in original['blocks'] for p in b['ports']),
                terminals=sorted(t for b in original['blocks'] for t in b['terminals']))])
            try:
                wrong = predict(bad)
            except AssertionError:
                wrong = 'invalid terminal count'
            if wrong != system['prediction']:
                negative = dict(row=ri, system=si, corrupted=bad, wrong=wrong,
                                correct=system['prediction'])
                break
        if negative is not None:
            break
    assert negative is not None
    files = [SOURCE, Path(__file__), *(ROOT / p for p in source['hashes'] if p.startswith('scripts/'))]
    result = dict(trust='Exact Python replay on existing Errera witnesses; no Lean theorem or bounded-size state claim.',
        scope='Same raw boundary and source pairing; supplied one/two-step histories safe at every intermediate state.',
        graph=source['graph'], reference=reference,
        summary=dict(witnesses=len(rows), histories=sum(len(r['histories']) for r in rows),
                     exact_action_legal=sum(r['exact_action_legal'] for r in rows),
                     compatible_targets=sum(r['target_compatible'] for r in rows),
                     audited_transitions=len(audit), audited_systems=3 * len(audit)),
        comparisons=rows, connectivity_negative_control=negative,
        audit_sha256=sha256(encode(audit).encode()).hexdigest(),
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files})
    model.dual.systems.cache_clear()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    content = encode(result) + '\n'
    if args.check:
        assert OUT.read_text() == content, 'Certificate differs; inspect before regenerating.'
    else:
        OUT.write_text(content)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
