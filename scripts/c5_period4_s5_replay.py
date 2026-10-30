#!/usr/bin/env python3
"""Independent stdlib replay of period-four witnesses and full-O buffers.

No imports from the search, source-control, Kempe, or buffer producers.  The
original sphere is checked as a combinatorial oriented surface before any
colouring claim is checked.  Complete Kempe classes are explored modulo one
common S4 action, with all components of all six pairs retained.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audits/2026-10-30-c5-period4-s5"
OLD = ROOT / "audits/2026-10-29-kempe-realizability/source/controls.json"
PAIRS = ((0, 3), (1, 3), (1, 2), (0, 2), (0, 3))
ROOT_POSITIONS = (2, 4, 1, 3, 0)
BOUNDARIES = ((0, 1, 0, 2, 3), (0, 1, 3, 2, 3), (0, 1, 3, 2, 1),
              (0, 2, 3, 2, 1), (0, 2, 3, 0, 1), (3, 2, 3, 0, 1))
ALIGN = (2, 3, 1, 0)


def edge(a, b):
    return tuple(sorted((a, b)))


def parts(adj, allowed):
    unseen, answer = set(allowed), []
    while unseen:
        first = min(unseen)
        unseen.remove(first)
        todo = [first]
        for a in todo:
            for b in sorted(adj[a] & unseen):
                unseen.remove(b)
                todo.append(b)
        answer.append(tuple(sorted(todo)))
    return sorted(answer)


def canonical(colors):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in colors)


def cyclic_equal(a, b):
    return len(a) == len(b) and any(a == b[k:] + b[:k] for k in range(len(b)))


def topology(w):
    n = w["n"]
    edges = [edge(*e) for e in w["original_edges"]]
    assert len(set(edges)) == len(edges) == 3 * n - 6
    assert all(0 <= a < b < n for a, b in edges)
    adj = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    assert len(parts(adj, range(n))) == 1
    faces = [tuple(f) for f in w["sphere_faces"]]
    assert len(faces) == 2 * n - 4
    assert len({tuple(sorted(f)) for f in faces}) == len(faces)
    owners, arcs, next_link = defaultdict(list), set(), defaultdict(dict)
    for j, f in enumerate(faces):
        assert len(f) == len(set(f)) == 3
        for i in range(3):
            a, b, c = f[i], f[(i + 1) % 3], f[(i + 2) % 3]
            assert (a, b) not in arcs
            arcs.add((a, b))
            owners[edge(a, b)].append(j)
            assert c not in next_link[a]
            next_link[a][c] = b
    assert set(owners) == set(edges)
    assert all(len(js) == 2 for js in owners.values())
    assert all((b, a) in arcs for a, b in arcs)
    # A single cyclic link at each vertex rules out pinched pseudo-surfaces.
    rotation = {}
    for v in range(n):
        assert set(next_link[v]) == adj[v] == set(next_link[v].values())
        start, cycle = min(adj[v]), []
        a = start
        while a not in cycle:
            cycle.append(a)
            a = next_link[v][a]
        assert a == start and set(cycle) == adj[v]
        rotation[v] = cycle
    supplied = w.get("rotation")
    if supplied is not None:
        supplied = {int(v): list(row) for v, row in
                    (supplied.items() if isinstance(supplied, dict) else enumerate(supplied))}
        assert set(supplied) == set(range(n))
        orientations = [{s for s in (1, -1)
                         if cyclic_equal(supplied[v], rotation[v][::s])}
                        for v in range(n)]
        assert set.intersection(*orientations), "Rotation and oriented faces differ"
    center, boundary = w["center"], w["boundary"]
    assert len(boundary) == len(set(boundary)) == 5
    assert set(boundary) == adj[center]
    assert cyclic_equal(boundary, rotation[center]) or cyclic_equal(boundary, rotation[center][::-1])
    assert all(edge(boundary[i], boundary[(i + 1) % 5]) in owners for i in range(5))
    assert sum(a in boundary and b in boundary for a, b in edges) == 5
    # Enumerate every simple 3/4/5-cycle with a unique first vertex/direction.
    cycles = []
    for first in range(n):
        def visit(path):
            last = path[-1]
            if len(path) >= 3 and first in adj[last] and path[1] < last:
                cut = {edge(path[i], path[(i + 1) % len(path)]) for i in range(len(path))}
                dual = {j: set() for j in range(len(faces))}
                for e, (a, b) in owners.items():
                    if e not in cut:
                        dual[a].add(b)
                        dual[b].add(a)
                regions = parts(dual, dual)
                assert len(regions) == 2
                sides = sorted((sorted({x for j in region for x in faces[j]} - set(path))
                                for region in regions), key=lambda row: (len(row), row))
                assert set(sides[0]).isdisjoint(sides[1])
                assert set(sides[0]) | set(sides[1]) == set(range(n)) - set(path)
                cycles.append(dict(cycle=path, sides=sides))
            if len(path) < 5:
                for x in sorted(adj[last]):
                    if x > first and x not in path:
                        visit(path + [x])
        visit([first])
    bad34 = [r for r in cycles if len(r["cycle"]) < 5 and r["sides"][0]]
    bad5 = [r for r in cycles if len(r["cycle"]) == 5 and len(r["sides"][0]) > 1]
    third = []
    for i in range(5):
        a, b = boundary[i], boundary[(i + 1) % 5]
        candidates = [next(x for x in faces[j] if x not in (a, b)) for j in owners[edge(a, b)]]
        assert center in candidates and len(candidates) == 2
        third.append(next(x for x in candidates if x != center))
    return adj, dict(vertices=n, edges=len(edges), faces=len(faces),
        degrees=[len(adj[v]) for v in range(n)], rotation=rotation,
        all_short_cycle_sides=cycles, separating_34=bad34, separating_5_violations=bad5,
        S34=not bad34, S5=not bad5,
        G_str=min(map(len, adj.values())) >= 5 and not bad34 and not bad5,
        five_original_exterior_third_vertices=third)


def actual_moves(w, adj):
    exterior = w["exterior_vertices"]
    assert set(exterior) == set(adj) - {w["center"]}
    assert len(exterior) == len(set(exterior))
    position = {v: j for j, v in enumerate(exterior)}
    bpos = [position[v] for v in w["boundary"]]
    oadj = {v: adj[v] - {w["center"]} for v in exterior}
    expected_edges = {edge(a, b) for a in exterior for b in oadj[a]}
    assert expected_edges == {edge(*e) for e in w["exterior_edges"]}
    cycle = [tuple(c) for c in w["cycle"]]
    assert len(cycle) == len(set(cycle)) == 4
    assert len(w["rounds"]) == 4
    snapshots, rounds, histories = [], [], {v: [] for v in exterior}
    for r, (source, row) in enumerate(zip(cycle, w["rounds"])):
        assert source == tuple(row["source_colors"])
        assert len(source) == len(exterior) and set(source) <= set(range(4))
        assert tuple(source[p] for p in bpos) == BOUNDARIES[0]
        c, colors = source, [source]
        moves = []
        assert len(row["moves"]) == 5
        for t, (pair, root_pos, stored) in enumerate(zip(PAIRS, ROOT_POSITIONS, row["moves"])):
            root = w["boundary"][root_pos]
            assert tuple(stored["pair"]) == pair and stored["root"] == root
            assert all(c[position[a]] != c[position[b]] for a, b in expected_edges)
            comps = parts(oadj, [v for v in exterior if c[position[v]] in pair])
            comp = next(p for p in comps if root in p)
            assert list(comp) == sorted(stored["component"])
            assert set(comp) & set(w["boundary"]) == {root}
            changed = tuple(sum(pair) - color if v in comp else color for v, color in zip(exterior, c))
            assert changed == tuple(stored["colors"])
            assert tuple(changed[p] for p in bpos) == BOUNDARIES[t + 1]
            assert all(changed[position[a]] != changed[position[b]] for a, b in expected_edges)
            moves.append(dict(pair=pair, root=root, component=comp, colors=changed))
            c = changed
            colors.append(c)
        normalized = tuple(ALIGN[color] for color in c)
        assert normalized == tuple(row["normalized_colors"]) == cycle[(r + 1) % 4]
        rounds.append(dict(source_colors=source, moves=moves, normalized_colors=normalized,
                           changed_vertices=[v for v in exterior if source[position[v]] != normalized[position[v]]]))
        for t, c in enumerate(colors):
            snapshots.append(dict(round=r, time=t, colors=c))
            for v in exterior:
                histories[v].append(c[position[v]])
    return oadj, position, snapshots, rounds, histories


def buffer_replay(w, adj, position, snapshots, rounds):
    boundary, exterior = w["boundary"], w["exterior_vertices"]
    distance = {v: 0 for v in boundary}
    queue = list(boundary)
    for v in queue:
        for x in sorted(adj[v]):
            if x not in distance:
                distance[x] = distance[v] + 1
                queue.append(x)
    assert set(distance) == set(exterior)
    answer = []
    for radius in (1, 2):
        kept = {v for v in exterior if distance[v] <= radius}
        remote = set(exterior) - kept
        interface = {v for v in exterior if distance[v] == radius}
        assert all(v in interface for v in kept for x in adj[v] & remote)
        records, rejoin_count = [], 0
        for snap in snapshots:
            colors = snap["colors"]
            pair_rows = []
            for pair in combinations(range(4), 2):
                active = {v for v in exterior if colors[position[v]] in pair}
                full = parts(adj, active)
                local = parts(adj, active & kept)
                far = parts(adj, active & remote)
                # Each remote original component becomes one auxiliary star.
                stars = [dict(component=comp,
                              attachments=sorted(set().union(*(adj[v] for v in comp)) & active & kept))
                         for comp in far]
                aux = {v: adj[v] & active & kept for v in active & kept}
                for j, star in enumerate(stars):
                    key = w["n"] + j
                    assert set(star["attachments"]) <= interface
                    aux[key] = set(star["attachments"])
                    for v in star["attachments"]:
                        aux[v].add(key)
                composed = sorted(tuple(v for v in comp if v in kept)
                                  for comp in parts(aux, aux) if set(comp) & kept)
                projection = sorted(tuple(v for v in comp if v in kept)
                                    for comp in full if set(comp) & kept)
                assert composed == projection
                rejoins = [dict(full_component=comp,
                                kept_pieces=[piece for piece in local if set(piece) <= set(comp)])
                           for comp in full
                           if sum(set(piece) <= set(comp) for piece in local) >= 2]
                rejoin_count += len(rejoins)
                pair_rows.append(dict(pair=pair, full_components=full,
                    local_kept_components=local, remote_stars=stars,
                    full_component_projection=projection, actual_remote_rejoins=rejoins))
            records.append(dict(round=snap["round"], time=snap["time"], colors=colors,
                                all_six_pairs=pair_rows))
        changes = []
        for r, row in enumerate(rounds):
            before, after = row["source_colors"], row["normalized_colors"]
            changes.append(dict(round=r, boundary_returns=True,
                changed_buffer_vertices=sorted(v for v in kept if before[position[v]] != after[position[v]]),
                changed_remote_vertices=sorted(v for v in remote if before[position[v]] != after[position[v]])))
        orbit = [row["source_colors"] for row in rounds]
        multi_changes = [dict(round=r, iterates=k,
            changed_buffer_vertices=sorted(v for v in kept if orbit[r][position[v]] != orbit[(r + k) % 4][position[v]]),
            changed_remote_vertices=sorted(v for v in remote if orbit[r][position[v]] != orbit[(r + k) % 4][position[v]]))
            for k in (1, 2, 3, 4) for r in range(4)]
        projected_period = min(k for k in (1, 2, 4) if all(
            orbit[r][position[v]] == orbit[(r + k) % 4][position[v]]
            for r in range(4) for v in kept))
        answer.append(dict(radius=radius, distance_from="original ordered B in full O",
            kept_vertices=sorted(kept), interface_order=sorted(interface), remote_vertices=sorted(remote),
            interface_is_assumed_cycle=False, snapshots=records, one_round_changes=changes,
            all_normalized_iterate_changes=multi_changes,
            projected_orbit_period=projected_period,
            actual_remote_rejoin_records=rejoin_count,
            full_O_component_gluing_verified=True))
    return dict(distance_layers={d: sorted(v for v in exterior if distance[v] == d)
                                 for d in range(max(distance.values()) + 1)}, buffers=answer)


def full_class(w, adj, position):
    exterior = w["exterior_vertices"]
    bpos = [position[v] for v in w["boundary"]]
    start = canonical(w["cycle"][0])
    states, ids, previous, via, actions = [start], {start: 0}, [None], [None], []
    action_count, extending = 0, []
    # The C5 boundary uses >=3 colours; global S4 acts freely.  A transposition
    # of all colour names is realizable by swapping all its actual components.
    # Consequently quotient reachability lifts to the whole literal class.
    for source, c in enumerate(states):
        assert len(set(c[p] for p in bpos)) >= 3
        if len(set(c[p] for p in bpos)) == 3:
            extending.append(source)
        source_actions = []
        for pair in combinations(range(4), 2):
            for comp in parts(adj, [v for v in exterior if c[position[v]] in pair]):
                raw = tuple(sum(pair) - color if v in comp else color for v, color in zip(exterior, c))
                target = canonical(raw)
                k = ids.get(target)
                action = dict(pair=pair, component=comp)
                if k is None:
                    k = len(states)
                    ids[target] = k
                    states.append(target)
                    previous.append(source)
                    via.append(action)
                source_actions.append(dict(target=k, **action))
                action_count += 1
        actions.append(source_actions)
    escape = []
    if extending:
        q = extending[0]
        while previous[q] is not None:
            escape.append(dict(source=previous[q], target=q, **via[q]))
            q = previous[q]
        escape.reverse()
    return dict(normalized_states=states, all_actual_component_actions=actions,
        normalized_size=len(states), literal_size=24 * len(states),
        action_count=action_count, all_six_pairs_all_components_complete=True,
        extending_state_ids=extending, blocked=not extending,
        escape_quotient_route=escape,
        quotient_contract="One common global S4 permutation only. All 24 literal lifts per state; whole literal class recovered because every global permutation is Kempe-reachable.")


def rigid_five_cycle_tests(w, geo, position, rounds):
    """Replay the S5 one-vertex-side rigidity implication for c versus H²c."""
    center = w["center"]
    orbit = [row["source_colors"] for row in rounds]
    rows = []
    for item in geo["all_short_cycle_sides"]:
        cycle = item["cycle"]
        if len(cycle) != 5 or center in cycle:
            continue
        center_side = next(side for side in item["sides"] if center in side)
        if len(center_side) < 2:
            continue
        other_side = next(side for side in item["sides"] if center not in side)
        for r in range(4):
            c, d = orbit[r], orbit[(r + 2) % 4]
            if any(c[position[v]] != d[position[v]] for v in cycle):
                continue
            defect = [v for v in other_side if c[position[v]] != d[position[v]]]
            if geo["G_str"]:
                assert len(other_side) <= 1 and not defect
            rows.append(dict(round=r, compared_iterates=2, cycle=cycle,
                center_side=center_side, opposite_side=other_side,
                stable_boundary=True, opposite_side_changed_vertices=defect,
                G_str_premise_met=geo["G_str"], rigidity_conclusion_holds=not defect,
                countercontrol_to_dropping_S5=bool(defect)))
    return dict(lemma="In G_str, a stable C5 boundary with >=2 vertices on the center side forces the opposite-side full coloring to agree. No assertion that such a cycle exists.",
        same_source_comparisons=rows,
        stable_cycles_with_opposite_defect=sum(bool(row["opposite_side_changed_vertices"]) for row in rows))


def check_face_histories(path):
    """Independent bit-choice enumeration of the five original face domains."""
    stored = json.loads(path.read_text())["history_relaxation"]
    one = []
    for start in range(4):
        for bits in product((0, 1), repeat=5):
            row = [start]
            for bit, pair in zip(bits, PAIRS):
                old = row[-1]
                if bit and old not in pair:
                    break
                row.append(sum(pair) - old if bit else old)
            else:
                one.append(tuple(row))
    assert len(one) == len(set(one)) == 28
    one.sort()
    boundary_words = list(zip(*BOUNDARIES))
    domains = [[word for word in one if all(x != y and x != z for x, y, z in
                zip(word, boundary_words[i], boundary_words[(i + 1) % 5]))] for i in range(5)]
    expected_domains = [dict(edge=[i, (i + 1) % 5],
        words=[dict(history=list(word), normalized_successor=ALIGN[word[-1]]) for word in domain])
        for i, domain in enumerate(domains)]
    assert stored["one_round_domains"] == expected_domains
    assert all(len(domain) == 2 for domain in domains)
    four = []
    for domain in domains:
        entries = []
        for first in domain:
            word, history = first, []
            for _ in range(4):
                history.extend(word)
                word = next(candidate for candidate in domain if candidate[0] == ALIGN[word[-1]])
            assert word == first
            entries.append(history)
        four.append(entries)
    assert stored["four_round_domains"] == four
    closed = []
    def extend(start, old, history, rounds):
        if rounds == 4:
            if old == start:
                closed.append(history)
            return
        for word in one:
            if word[0] == old:
                extend(start, ALIGN[word[-1]], history + list(word), rounds + 1)
    for start in range(4):
        extend(start, start, [], 0)
    closed.sort()
    assert len(closed) == stored["four_round_pointwise_history_count"] == 2090
    assert sha256(json.dumps(closed, separators=(",", ":")).encode()).hexdigest() == stored["four_round_history_sha256"]
    phases, rims = [], []
    for phase in product((0, 1), repeat=5):
        selected = [four[i][phase[i]] for i in range(5)]
        compatible = lambda a, b: all(x != y for x, y in zip(a, b))
        edges = [[a, b] for a, b in combinations(range(5), 2) if compatible(selected[a], selected[b])]
        equalities = [[a, b] for a, b in combinations(range(5), 2) if selected[a] == selected[b]]
        rim = all(list(edge(i, (i + 1) % 5)) in edges for i in range(5))
        caps = [j for j, word in enumerate(closed) if all(compatible(word, other) for other in selected)]
        phases.append(dict(phase=list(phase), compatible_original_w_edges=edges,
            possible_history_equalities=equalities, complete_rim=rim,
            compatible_cap_history_ids=caps, initial_w_colors=[h[0] for h in selected],
            normalized_round_start_w_colors=[[h[6 * r] for h in selected] for r in range(4)]))
        if all(compatible(domains[i][phase[i]], domains[(i + 1) % 5][phase[(i + 1) % 5]]) for i in range(5)):
            by_time = [[domains[i][phase[i]][t] for i in range(5)] for t in range(6)]
            rims.append(dict(phase=list(phase), w_colors_by_time=by_time,
                times_using_four_colors=[t for t, colors in enumerate(by_time) if len(set(colors)) == 4]))
    assert stored["phase_assignments"] == phases
    assert stored["one_round_complete_rim"] == rims
    assert len(rims) == 2 and all(row["times_using_four_colors"] for row in rims)
    assert not any(row["possible_history_equalities"] for row in phases)
    return dict(status="INDEPENDENT FINITE HISTORY CHECK OK", one_round_words=28,
        original_face_domains=[len(d) for d in domains], closed_four_round_words=2090,
        complete_five_face_phase_assignments=len(phases), possible_attachment_coincidences=0,
        complete_rim_phases=[row["phase"] for row in phases if row["complete_rim"]],
        complete_rim_compatible_cap_histories=sum(len(row["compatible_cap_history_ids"]) for row in phases if row["complete_rim"]),
        source_scope="Pointwise history relaxation; actual complete components checked separately.")


def old_errera():
    c = json.loads(OLD.read_text())["controls"][0]
    lookup = {row["source"]: row for row in c["H_returns"]}
    cycle = c["H_cycles"][0]
    states = c["normalized_colorings"]
    return dict(name="ERRERA-negative-control", n=17,
        original_edges=c["original_edges"], sphere_faces=c["sphere_faces"],
        center=c["deleted_vertex"], boundary=c["boundary"],
        exterior_vertices=list(range(16)), exterior_edges=c["exterior_edges"],
        cycle=[states[j] for j in cycle],
        rounds=[dict(source_colors=states[j],
                     moves=[dict(pair=m["pair"], root=m["root"], component=m["component"],
                                 colors=m["coloring"]) for m in lookup[j]["moves"]],
                     normalized_colors=states[lookup[j]["target"]]) for j in cycle])


def inspect(w):
    adj, geo = topology(w)
    oadj, position, snapshots, rounds, histories = actual_moves(w, adj)
    klass = full_class(w, oadj, position)
    buffers = buffer_replay(w, oadj, position, snapshots, rounds)
    third = geo["five_original_exterior_third_vertices"]
    return dict(name=w["name"], topology=geo, original_boundary=w["boundary"],
        period=4, least_period=4, full_O_twenty_actual_exchanges_verified=True,
        normalization_applied_to_every_original_exterior_vertex=True,
        rounds=rounds, complete_24_time_histories=histories,
        original_face_third_histories=[dict(boundary_edge=[w["boundary"][j], w["boundary"][(j + 1) % 5]],
            original_third_vertex=v, history=histories[v]) for j, v in enumerate(third)],
        stable_five_cycle_rigidity=rigid_five_cycle_tests(w, geo, position, rounds),
        full_kempe_component=klass, **buffers)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=AUDIT / "search-witnesses.json")
    parser.add_argument("--output", type=Path, default=AUDIT / "replay-certificate.json")
    parser.add_argument("--face-input", type=Path, default=AUDIT / "face-certificate.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    witnesses = [old_errera()]
    inputs = [OLD]
    if args.input.exists():
        witnesses.extend(json.loads(args.input.read_text())["witnesses"])
        inputs.append(args.input)
    face_check = None
    if args.face_input.exists():
        face_check = check_face_histories(args.face_input)
        inputs.append(args.face_input)
    result = dict(schema="independent-period4-s5-replay-v1",
        producer_imports=False, inputs={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        independent_common_face_history_check=face_check,
        witnesses=[inspect(w) for w in witnesses],
        evidence="Exact finite replay and original-surface checks; no exhaustive graph census, no Lean theorem.")
    errera = result["witnesses"][0]
    assert not errera["topology"]["S5"] and not errera["full_kempe_component"]["blocked"]
    assert all(b["actual_remote_rejoin_records"] for b in errera["buffers"])
    assert all(row["changed_buffer_vertices"] for b in errera["buffers"] for row in b["one_round_changes"])
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.check:
        assert args.output.read_text() == encoded, "Replay certificate differs"
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(json.dumps(dict(status="INDEPENDENT CHECK OK", witnesses=[dict(name=w["name"],
        G_str=w["topology"]["G_str"], S5=w["topology"]["S5"], period=w["period"],
        class_states=w["full_kempe_component"]["normalized_size"], blocked=w["full_kempe_component"]["blocked"],
        buffer_rejoins=[b["actual_remote_rejoin_records"] for b in w["buffers"]]) for w in result["witnesses"]]), sort_keys=True))


if __name__ == "__main__":
    main()
