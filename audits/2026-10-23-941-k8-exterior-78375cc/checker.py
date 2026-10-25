#!/usr/bin/env python3
"""Independent finite-envelope replay; surviving states are NOT source models.

Uses only the frozen source JSON and the result being checked.  It does not
import explore.py.  Cap fibres are rebuilt by DFS on the actual edge list;
partitions use restricted-growth strings and components use union-find.
"""
import argparse
import copy
import hashlib
import itertools
import json
import random
import time
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "frozen/audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/certificate.json"
SOURCE_SHA256 = "0d53cda484f624966dcf5e46cef6933ccc4af2e542d27250258640b7906be6c8"
OUTER = (0, 1, 2, 3, 2)
REJECTS = {(0, 1, 0, 2, 1), (0, 1, 2, 0, 2), (0, 1, 2, 1, 2)}
PAIRS = tuple(itertools.combinations(range(4), 2))
RINGS = (tuple(range(8)), tuple(range(8, 13)))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def normalize(values):
    order = []
    result = []
    for value in values:
        if value not in order:
            order.append(value)
        result.append(order.index(value))
    return tuple(result)


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, x, y):
        x, y = self.find(x), self.find(y)
        if x != y:
            self.parent[y] = x

    def partition(self, vertices):
        result = {}
        for vertex in vertices:
            result.setdefault(self.find(vertex), []).append(vertex)
        return tuple(sorted(tuple(sorted(block)) for block in result.values()))


def canonical_partition(blocks):
    return tuple(sorted(tuple(sorted(block)) for block in blocks))


def graph_data(cap):
    vertices = cap["ordered_boundary"] + cap["ordered_inner"]
    require(len(vertices) == 15 and len(set(vertices)) == 15, "cap vertex contract")
    index = {vertex: i for i, vertex in enumerate(vertices)}
    edges = tuple(sorted(tuple(sorted((index[a], index[b]))) for a, b in cap["edges"]))
    require(len(set(edges)) == len(edges), "repeated cap edge")
    require(all(a != b for a, b in edges), "cap loop")
    require(all(tuple(sorted((i, (i + 1) % 8))) in edges for i in range(8)), "missing K8 ring edge")
    adjacency = [set() for _ in vertices]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    return vertices, edges, adjacency


def boundary_words():
    def extend(word):
        if len(word) == 8:
            if word[-1] != word[0]:
                yield tuple(word)
            return
        for color in range(min(3, max(word) + 1) + 1):
            if color != word[-1]:
                yield from extend(word + [color])
    return tuple(extend([0]))


def dfs_lifts(word, adjacency):
    coloring = list(word) + [-1] * 7
    answers = []

    def visit(remaining):
        if not remaining:
            answers.append(tuple(coloring[8:]))
            return
        vertex = max(remaining, key=lambda v: (len({coloring[w] for w in adjacency[v] if coloring[w] >= 0}), len(adjacency[v]), -v))
        next_remaining = remaining - {vertex}
        forbidden = {coloring[w] for w in adjacency[vertex] if coloring[w] >= 0}
        for color in range(4):
            if color not in forbidden:
                coloring[vertex] = color
                visit(next_remaining)
        coloring[vertex] = -1

    visit(set(range(8, 15)))
    return tuple(sorted(answers))


def verify_fibres(cap):
    _, _, adjacency = graph_data(cap)
    recorded = {}
    for fibre in cap["complete_fibres"]:
        word = tuple(fibre["word"])
        require(word not in recorded, "duplicate fibre")
        lifts = tuple(tuple(lift) for lift in fibre["full_lifts"])
        require(len(set(lifts)) == len(lifts), "duplicate full lift")
        recorded[word] = tuple(sorted(lifts))
    require(set(recorded) == set(boundary_words()), "complete boundary domain, including empty fibres")
    rebuilt = {word: dfs_lifts(word, adjacency) for word in boundary_words()}
    require(recorded == rebuilt, "full cap fibres differ from independent edge DFS")
    residual = set(map(tuple, cap["residual_accepting_words"]))
    require(len(residual) == len(cap["residual_accepting_words"]), "duplicate residual")
    require(all(rebuilt.get(word) for word in residual), "residual without a full lift")
    return rebuilt


def literal_domain(cap):
    return {tuple(p[c] for c in word) for word in cap["residual_accepting_words"] for p in itertools.permutations(range(4))}


def sealed_result_header(expected, caps):
    require(set(expected) == {"schema", "strong", "caps"}, "sealed result fields")
    require(expected["schema"] == "k8-exterior-literal-necessary-v2", "result schema")
    require(expected["strong"] is True, "strong annular mode required")
    distributions = [tuple(row["distribution"]) for row in expected["caps"]]
    require(len(distributions) == 4 and set(distributions) == {tuple(cap["distribution"]) for cap in caps[:4]}, "exact four representative result coverage")


def noninterlaced(blocks, ring):
    position = {vertex: i for i, vertex in enumerate(ring)}
    intersections = [set(block) & set(ring) for block in blocks]
    for i, left in enumerate(intersections):
        if len(left) < 2:
            continue
        for right in intersections[i + 1:]:
            if len(right) < 2:
                continue
            labels = [int(vertex in right) for vertex in sorted(left | right, key=position.get)]
            changes = sum(labels[j] != labels[(j + 1) % len(labels)] for j in range(len(labels)))
            if changes > 2:
                return False
    return True


@lru_cache(None)
def growth_strings(n):
    if not n:
        return ((),)
    words = [(0,)]
    for _ in range(1, n):
        words = [word + (label,) for word in words for label in range(max(word) + 2)]
    return tuple(words)


@lru_cache(None)
def exterior_options(word, pair):
    colors = word + OUTER
    active = [vertex for vertex in range(13) if colors[vertex] in pair]
    forced = UnionFind(13)
    for ring in RINGS:
        for i, a in enumerate(ring):
            b = ring[(i + 1) % len(ring)]
            if a in active and b in active:
                forced.union(a, b)
    atoms = forced.partition(active)
    result = []
    for labels in growth_strings(len(atoms)):
        merged = [[] for _ in range(max(labels, default=-1) + 1)]
        for label, atom in zip(labels, atoms):
            merged[label].extend(atom)
        partition = canonical_partition(merged)
        if all(noninterlaced(partition, ring) for ring in RINGS):
            result.append(partition)
    require(len(set(result)) == len(result), "partition enumerator duplication")
    return tuple(result)


def planar_necessary(blocks, strong):
    if not all(noninterlaced(blocks, ring) for ring in RINGS):
        return False
    if not strong:
        return True
    label_of = {vertex: label for label, block in enumerate(blocks) for vertex in block}
    through = {label for label, block in enumerate(blocks) if set(block) & set(RINGS[0]) and set(block) & set(RINGS[1])}
    if not through:
        return True
    cyclic_orders = []
    for ring in RINGS:
        for label, block in enumerate(blocks):
            contacts = sorted(ring.index(vertex) for vertex in block if vertex in ring)
            if len(contacts) < 2:
                continue
            through_contacts = [ring.index(vertex) for vertex in ring if label_of[vertex] in through - {label}]
            if through_contacts:
                containing_gaps = set()
                for position in through_contacts:
                    for gap, start in enumerate(contacts):
                        distance = (position - start) % len(ring)
                        span = (contacts[(gap + 1) % len(contacts)] - start) % len(ring)
                        if 0 < distance < span:
                            containing_gaps.add(gap)
                if len(containing_gaps) != 1:
                    return False
        labels = [label_of[vertex] for vertex in ring if label_of[vertex] in through]
        runs = [label for i, label in enumerate(labels) if label != labels[i - 1]]
        if not runs and labels:
            runs = [labels[0]]
        if len(runs) != len(through):
            return False
        start = runs.index(min(through))
        cyclic_orders.append(runs[start:] + runs[:start])
    first, second = cyclic_orders
    return first == second or first == second[:1] + second[:0:-1]


def cap_pair_blocks(word, lifts, edges, pair):
    result = set()
    for lift in lifts:
        colors = word + lift
        forest = UnionFind(15)
        for a, b in edges:
            if colors[a] in pair and colors[b] in pair:
                forest.union(a, b)
        result.add(forest.partition(vertex for vertex in range(8) if colors[vertex] in pair))
    return tuple(sorted(result))


def joined_blocks(exterior, cap_blocks):
    forest = UnionFind(13)
    active = set()
    for partition in (exterior, cap_blocks):
        for block in partition:
            active.update(block)
            for vertex in block[1:]:
                forest.union(block[0], vertex)
    return forest.partition(sorted(active))


def swap_outcomes(word, pair, blocks):
    colors = word + OUTER
    masks = [sum(1 << vertex for vertex in block) for block in blocks]
    subsets = [0]
    for mask in masks:
        subsets += [value | mask for value in subsets]
    successors = set()
    for mask in subsets:
        after = tuple(pair[1] if color == pair[0] else pair[0] if color == pair[1] else color for color in colors)
        after = tuple(after[i] if (mask >> i) & 1 else color for i, color in enumerate(colors))
        outer = after[8:]
        q = normalize(outer)
        if q in REJECTS:
            return None
        if q == OUTER:
            palette = list(dict.fromkeys(outer))
            require(len(palette) == 4, "accepted C5 must fix the whole palette")
            successors.add(tuple(palette.index(color) for color in after[:8]))
    return frozenset(successors)


def independent_table(cap, seed):
    _, edges, adjacency = graph_data(cap)
    words = sorted(literal_domain(cap))
    random.Random(seed).shuffle(words)
    table = {}
    for word in words:
        # Direct literal DFS, rather than independently normalizing either ring.
        lifts = dfs_lifts(word, adjacency)
        require(bool(lifts), "literal accepting word lost all cap lifts")
        options_by_pair = []
        for pair in PAIRS:
            local_blocks = cap_pair_blocks(word, lifts, edges, pair)
            cache = {}
            options = []
            for exterior in exterior_options(word, pair):
                successors = set()
                admissible = True
                for local in local_blocks:
                    full = joined_blocks(exterior, local)
                    if full not in cache:
                        cache[full] = swap_outcomes(word, pair, full)
                    outcome = cache[full]
                    if outcome is None:
                        admissible = False
                        break
                    successors.update(outcome)
                if admissible:
                    options.append((exterior, frozenset(successors)))
            options_by_pair.append(options)
        table[word] = options_by_pair
    return table


def check_result(cap, expected, strong, seed, excluded_records=None):
    started = time.monotonic()
    table = independent_table(cap, seed)
    require(expected["initial"] == len(table), "literal initial domain count")
    current = set(table)
    summary = []
    terminal_options = None
    for number, round_record in enumerate(expected["rounds"]):
        require(round_record["before"] == len(current), "wrong round initial count")
        recorded_stats = {tuple(row["word"]): row for row in round_record["stats"]}
        require(len(recorded_stats) == len(round_record["stats"]), "duplicate round state")
        require(set(recorded_stats) == current, "round state coverage")
        removed = set()
        terminal_options = {}
        for word in sorted(current):
            allowed = [[p for p, targets in choices if targets <= current] for choices in table[word]]
            counts = [sum(planar_necessary(a + b, strong) for a in allowed[i] for b in allowed[5 - i]) for i in range(3)]
            require(recorded_stats[word]["individual"] == [len(choices) for choices in allowed], "individual partition counts")
            require(recorded_stats[word]["complementary"] == counts, "joint complementary partition counts")
            if not all(counts):
                removed.add(word)
            else:
                terminal_options[word] = allowed
            if number == 0 and excluded_records is not None and word in excluded_records:
                record = excluded_records[word]
                require(len(record["allowed"]) == 6, "exclusion must cover all six palettes")
                for i in range(6):
                    recorded_options = list(map(canonical_partition, record["allowed"][i]))
                    require(len(recorded_options) == len(set(recorded_options)) and set(recorded_options) == set(allowed[i]), "exclusion complete exterior option list")
                for mode, label in ((False, "weak"), (True, "strong")):
                    actual = [sum(planar_necessary(a + b, mode) for a in allowed[i] for b in allowed[5 - i]) for i in range(3)]
                    require(actual == record[label], "exclusion joint planarity counts")
        require(len(round_record["removed"]) == len(set(map(tuple, round_record["removed"]))), "duplicate removal")
        require(removed == set(map(tuple, round_record["removed"])), "round removal set")
        summary.append({"before": len(current), "removed": len(removed)})
        current -= removed
        if not removed:
            require(number + 1 == len(expected["rounds"]), "spurious rounds after fixed point")
    require(summary and summary[-1]["removed"] == 0, "not a completed fixed point")
    require(current == set(map(tuple, expected["remaining"])), "remaining set")
    require(len(expected["remaining"]) == len(current), "duplicate remaining state")
    controls = {tuple(row["word"]): row["complementary_pairs"] for row in expected["necessary_controls"]}
    require(len(controls) == len(expected["necessary_controls"]) and set(controls) == current, "survivor control coverage")
    for word, triples in controls.items():
        require(len(triples) == 3, "three complementary controls required")
        for i, pair in enumerate(triples):
            require(len(pair) == 2, "complementary control arity")
            a, b = map(canonical_partition, pair)
            require(a in terminal_options[word][i] and b in terminal_options[word][5 - i], "control not admissible for all lifts")
            require(planar_necessary(a + b, strong), "nonplanar complementary control")
    removed = set(table) - current
    if excluded_records is not None:
        require(set(excluded_records) == removed, "exclusion supplement must cover exact removed set")
    excluded_canonical = sorted({normalize(word) for word in table} - {normalize(word) for word in current})
    return {"distribution": cap["distribution"], "initial_literal": len(table), "remaining_literal": len(current), "remaining_canonical": len({normalize(word) for word in current}), "excluded_whole_canonical_rows": excluded_canonical, "removed_literal_words": sorted(removed), "rounds": summary, "seconds": round(time.monotonic() - started, 3)}


def rotation_map(source, target):
    d, e = source["distribution"], target["distribution"]
    for sign in (1, -1):
        for shift in range(6):
            if any(d[i] != e[(shift + sign * i) % 6] for i in range(6)):
                continue
            mapping = {"T": "T"}
            for i in range(6):
                image = (shift + sign * i) % 6
                mapping["n" + str(i)] = "n" + str(image)
                mapping["q" + str(i)] = "q" + str((image if sign == 1 else image - 1) % 6)
                for j in range(d[i]):
                    mapping[f"w{i}_{j}"] = f"w{image}_{j if sign == 1 else d[i] - 1 - j}"
            return mapping, sign, shift
    return None


def cycle_key(face):
    return min(tuple(face[i:] + face[:i]) for i in range(len(face)))


def check_transport(source, target, source_fibres, target_fibres):
    found = rotation_map(source, target)
    require(found is not None, "no dihedral distribution map")
    mapping, sign, shift = found
    vertices_a = source["ordered_boundary"] + source["ordered_inner"]
    vertices_b = target["ordered_boundary"] + target["ordered_inner"]
    require(set(mapping) == set(vertices_a) and set(mapping.values()) == set(vertices_b), "vertex bijection")
    images = {tuple(sorted((mapping[a], mapping[b]))) for a, b in source["edges"]}
    require(images == {tuple(sorted(edge)) for edge in target["edges"]}, "transport actual edges")
    image_faces = {cycle_key([mapping[v] for v in (face if sign == 1 else list(reversed(face)))]) for face in source["oriented_actual_faces"]}
    require(image_faces == {cycle_key(face) for face in target["oriented_actual_faces"]}, "transport oriented faces")
    boundary_permutation = [target["ordered_boundary"].index(mapping[v]) for v in source["ordered_boundary"]]
    require(all((boundary_permutation[(i + 1) % 8] - boundary_permutation[i]) % 8 == sign % 8 for i in range(8)), "transport ordered K8 cycle")
    target_index = {vertex: i for i, vertex in enumerate(vertices_b)}
    relabelled = {}
    residual_image = set()
    residual_source = set(map(tuple, source["residual_accepting_words"]))
    for word, lifts in source_fibres.items():
        boundary = [-1] * 8
        for i, vertex in enumerate(source["ordered_boundary"]):
            boundary[target_index[mapping[vertex]]] = word[i]
        normalized = normalize(boundary)
        palette = list(dict.fromkeys(boundary))
        palette += sorted(set(range(4)) - set(palette))
        values = set()
        for lift in lifts:
            colored = word + lift
            target_coloring = [-1] * 15
            for i, vertex in enumerate(vertices_a):
                target_coloring[target_index[mapping[vertex]]] = palette.index(colored[i])
            values.add(tuple(target_coloring[8:]))
        require(normalized not in relabelled, "boundary transport injectivity")
        relabelled[normalized] = tuple(sorted(values))
        if word in residual_source:
            residual_image.add(normalized)
    require(relabelled == target_fibres, "transport all complete fibres including empty")
    require(residual_image == set(map(tuple, target["residual_accepting_words"])), "transport residual set")
    return {"target_distribution": target["distribution"], "sign": sign, "shift": shift, "vertex_map": mapping, "ordered_boundary_permutation": boundary_permutation, "C5_map": list(range(5)), "palette_map": list(range(4))}


def self_tests():
    tests = []
    def record(name, assertion):
        require(assertion, "self-test: " + name)
        tests.append(name)
    record("alternating_contacts_rejected", not noninterlaced(((0, 2), (1, 3)), RINGS[0]))
    record("nested_contacts_retained", noninterlaced(((0, 3), (1, 2)), RINGS[0]))
    # X,A,X,B on K8, with both A and B through to C5: a pocket obstruction.
    pocket = ((0, 2), (1, 8), (3, 9), (4,), (5,), (6,), (7,), (10,), (11,), (12,))
    record("annular_pocket_not_just_ring_crossing", planar_necessary(pocket, False) and not planar_necessary(pocket, True))
    # Three-point through order cannot distinguish reversal, but four can.
    order = ((0, 8), (1, 10), (2, 9), (3, 11), (4,), (5,), (6,), (7,), (12,))
    record("incompatible_four_through_order", planar_necessary(order, False) and not planar_necessary(order, True))
    direct = ((0, 8), (1, 9), (2, 10), (3, 11), (4,), (5,), (6,), (7,), (12,))
    record("compatible_four_through_order", planar_necessary(direct, True))
    # A free C5 color-3 endpoint under 03 gives canonical 01202.
    word = (0, 1, 2, 3, 0, 1, 2, 3)
    active = tuple((i,) for i, color in enumerate(word + OUTER) if color in (0, 3))
    record("reject_row_visible_from_subset_swap", swap_outcomes(word, (0, 3), active) is None)
    relative = (3, 2, 3, 0, 1, 0, 2, 1)
    for pair in PAIRS:
        block = tuple(i for i, color in enumerate(relative + OUTER) if color in pair)
        record("global_palette_from_C5_" + "".join(map(str, pair)), swap_outcomes(relative, pair, (block,)) == frozenset({relative}))
    # A real cap-1 fibre: one exterior partition passes one lift and fails the
    # other.  Existentially selecting a cap lift would therefore be unsound.
    word = (0, 1, 0, 1, 0, 1, 2, 1)
    exterior = ((0, 2, 8), (4, 11))
    pass_local, fail_local = ((0,), (2, 4)), ((0, 2), (4,))
    record("one_exterior_must_work_for_every_lift", swap_outcomes(word, (0, 3), joined_blocks(exterior, pass_local)) is not None and swap_outcomes(word, (0, 3), joined_blocks(exterior, fail_local)) is None)
    return tests


def negative_controls(caps, rebuilt):
    rejected = []
    def expect_failure(name, action):
        try:
            action()
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError("negative control escaped: " + name)

    changed = copy.deepcopy(caps[0])
    empty = next(i for i, row in enumerate(changed["complete_fibres"]) if not row["full_lifts"])
    del changed["complete_fibres"][empty]
    expect_failure("omit_empty_fibre", lambda: verify_fibres(changed))
    changed = copy.deepcopy(caps[0])
    nonempty = next(row for row in changed["complete_fibres"] if row["full_lifts"])
    nonempty["full_lifts"].pop()
    expect_failure("omit_full_lift", lambda: verify_fibres(changed))
    changed = copy.deepcopy(caps[0])
    changed["edges"].pop(next(i for i, edge in enumerate(changed["edges"]) if set(edge) == {"q5", "w0_0"}))
    expect_failure("omit_original_ring_edge", lambda: verify_fibres(changed))
    changed = copy.deepcopy(caps[6])
    changed["residual_accepting_words"].pop()
    expect_failure("transport_different_residual", lambda: check_transport(caps[0], changed, rebuilt[0], rebuilt[6]))
    changed = copy.deepcopy(caps[6])
    changed["oriented_actual_faces"][0].reverse()
    expect_failure("transport_wrong_rotation", lambda: check_transport(caps[0], changed, rebuilt[0], rebuilt[6]))
    changed = copy.deepcopy(rebuilt[6])
    word = next(word for word, lifts in changed.items() if lifts)
    changed[word] = changed[word][1:]
    expect_failure("transport_partial_fibre", lambda: check_transport(caps[0], caps[6], rebuilt[0], changed))
    header = {"schema": "k8-exterior-literal-necessary-v2", "strong": True, "caps": [{"distribution": cap["distribution"]} for cap in caps[:4]]}
    changed = copy.deepcopy(header)
    changed["caps"].pop()
    expect_failure("omit_representative_cap", lambda: sealed_result_header(changed, caps))
    changed = copy.deepcopy(header)
    changed["caps"][-1] = changed["caps"][0]
    expect_failure("duplicate_representative_cap", lambda: sealed_result_header(changed, caps))
    changed = copy.deepcopy(header)
    changed["strong"] = False
    expect_failure("downgrade_annular_mode", lambda: sealed_result_header(changed, caps))
    changed = copy.deepcopy(header)
    changed["schema"] = "canonical-port-only-unsealed"
    expect_failure("change_relative_palette_schema", lambda: sealed_result_header(changed, caps))
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=HERE / "EXPLORATION-literal-strong-four.json")
    parser.add_argument("--indices", nargs="*", type=int)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--transport-only", action="store_true")
    parser.add_argument("--exclusions", type=Path, default=HERE / "EXCLUDED-24.json")
    args = parser.parse_args()
    checker_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if args.indices is not None:
        require(bool(args.indices) and len(args.indices) == len(set(args.indices)) and set(args.indices) <= set(range(4)), "indices must be a nonempty unique subset of four representatives")
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "frozen source SHA256")
    source = json.loads(raw)
    caps = source["caps"]
    rebuilt = [verify_fibres(cap) for cap in caps]
    transports = []
    for index, cap in enumerate(caps):
        representative = next(i for i in range(4) if rotation_map(caps[i], cap) is not None)
        row = check_transport(caps[representative], cap, rebuilt[representative], rebuilt[index])
        row.update({"representative_index": representative, "target_index": index})
        transports.append(row)
    results = []
    certificate_sha256 = None
    if not args.transport_only:
        certificate_raw = args.certificate.read_bytes()
        certificate_sha256 = hashlib.sha256(certificate_raw).hexdigest()
        expected = json.loads(certificate_raw)
        sealed_result_header(expected, caps)
        seen = set()
        for row in expected["caps"]:
            index = next(i for i, cap in enumerate(caps) if cap["distribution"] == row["distribution"])
            require(index not in seen, "duplicate result cap")
            seen.add(index)
            if args.indices is not None and index not in args.indices:
                continue
            exclusions = None
            if index == 2 and args.exclusions.exists():
                exclusion_rows = json.loads(args.exclusions.read_text())
                exclusions = {tuple(item["word"]): item for item in exclusion_rows}
                require(len(exclusions) == len(exclusion_rows), "duplicate supplementary exclusion")
            result = check_result(caps[index], row, expected["strong"], args.seed, exclusions)
            results.append(result)
            print(json.dumps({"checked": result}), flush=True)
        if args.indices is not None:
            require(set(args.indices) <= seen, "requested cap missing from result")
        require(bool(results), "no result cap checked")
    all_caps = []
    for transport in transports:
        index = transport["target_index"]
        rep = transport["representative_index"]
        result = next((row for row in results if row["distribution"] == caps[rep]["distribution"]), None)
        if result is None:
            continue
        removed = set()
        for word in result["removed_literal_words"]:
            target_word = [-1] * 8
            for position, image in enumerate(transport["ordered_boundary_permutation"]):
                target_word[image] = word[position]
            removed.add(tuple(target_word))
        domain = literal_domain(caps[index])
        require(removed <= domain, "transported exclusion outside target residual")
        surviving_canonical = {normalize(word) for word in domain - removed}
        all_caps.append({"index": index, "distribution": caps[index]["distribution"], "representative_index": rep, "initial_canonical": len(caps[index]["residual_accepting_words"]), "remaining_canonical": len(surviving_canonical), "excluded_whole_canonical_rows": sorted({normalize(word) for word in domain} - surviving_canonical), "removed_literal_count": len(removed)})
    status = "TRANSPORT_ONLY_PASS" if args.transport_only else "PARTIAL_PASS" if args.indices is not None and set(args.indices) != set(range(4)) else "PASS"
    if status == "PASS":
        require(len(results) == 4 and len(all_caps) == 21, "full envelope and transport coverage")
    print(json.dumps({"status": status, "source_sha256": SOURCE_SHA256, "checker_sha256": checker_sha256, "certificate_sha256": certificate_sha256, "strong_annular_mode": None if args.transport_only else True, "seed": args.seed, "cap_fibres_rebuilt": len(rebuilt), "fibre_records_per_cap": [len(fibres) for fibres in rebuilt], "empty_fibres_per_cap": [sum(not lifts for lifts in fibres.values()) for fibres in rebuilt], "semantic_controls": self_tests(), "negative_controls_rejected": negative_controls(caps, rebuilt), "checked_envelopes": results, "all_caps_transported_results": all_caps, "canonical_totals": {"initial": sum(row["initial_canonical"] for row in all_caps), "remaining": sum(row["remaining_canonical"] for row in all_caps)}, "dihedral_transports": transports, "authority": "necessary finite envelope only; no source-realizability claim"}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
