"""Exact four-colour constraints: propagate, eliminate, then write back.

No unknown vertex receives a colour during reduction.  Eliminating a variable
stores the *complete joint* frontier relation, including every possible colour
of the eliminated variable for each allowed frontier tuple.  Reverse lookup is
therefore witness reconstruction, not a search over guessed assignments.

``checks`` counts candidate attempts, relation-row filtering/membership tests,
and enabled C5 index operations.  ``max_checks`` bounds that sum; a separate 100,000-row safety ceiling
bounds cumulative generated tables and optional certificate snapshots.  Neither
limit means unsatisfiable.  Graph bookkeeping and final witness verification
are not charged as relation checks.  General variable elimination remains
exponential in frontier width.  Optional induced-C5 discovery has its own
cycle/scan-step limits; a truncated discovery only omits redundant propagators.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, islice, permutations, product


CONSTRAINT_RULES = [
    {"id": "C1", "name": "子構造限制傳播", "description": "由原子圖結構推出限制，或過濾完整關係；刪除沒有共同支援的候選色，只縮限，不填色。"},
    {"id": "C2", "name": "合併消去與記錄", "description": "合併同一點的全部關係，保存每個完整邊界色組及其所有可用內部色。"},
    {"id": "C3", "name": "反向查表寫回", "description": "全部消去成功後，依已確定的完整邊界色組查表，反向寫回合法顏色。"},
]

# Shared immutable literal-colour tables.  No quotient by colour permutations.
EDGE_ROWS = frozenset(permutations(range(4), 2))
TRIANGLE_ROWS = frozenset(permutations(range(4), 3))
K4_ROWS = frozenset(permutations(range(4), 4))
TABLE_ROW_CEILING = 100000


def substructure_catalogue():
    """Export the actual reusable templates, not graph-level cached answers."""
    from four_color_c5 import c5_catalogue
    from four_color_conflicts import conflict_catalogue

    return {
        "version": "literal-four-colour-substructures-v2",
        "palette": list(range(4)),
        "templates": [
            {"name": name, "scope": list(range(size)),
             "edges": [list(edge) for edge in combinations(range(size), 2)],
             "rows": [list(row) for row in sorted(rows)]}
            for name, size, rows in (("edge", 2, EDGE_ROWS),
                                     ("triangle", 3, TRIANGLE_ROWS),
                                     ("k4", 4, K4_ROWS))
        ] + [c5_catalogue()],
        "conflicts": conflict_catalogue(),
        "template_hits_definition": "Initial edge/triangle/K4 factors reuse immutable tables; C5 indexed reuse is counted separately by c5_queries. Neither is a cached graph solution.",
    }


@dataclass
class _Factor:
    scope: tuple
    rows: frozenset
    source_edges: frozenset
    source_vertices: frozenset
    revision: int = 0


class _WorkLimit(Exception):
    pass


def solve_constraints(graph, use_substructures=True, max_checks=1000000,
                      trace_limit=5000, record_relations=True, use_c5=False,
                      c5_max_cycles=128, c5_max_scan_steps=200000,
                      c5_scan_method="complete", use_conflicts=True,
                      c5_method="table", use_intersections=False, use_cycles=False,
                      cycle_max_cycles=128, cycle_max_scan_steps=200000):
    """Solve exactly, or return ``limit`` without asserting nonexistence.

    Recorded rows equal the join of ``input_relations`` under the explicitly
    recorded ``source_domains``.  ``source_edges`` describe original provenance;
    outside GAC context can narrow a bucket, so they alone do not specify its
    complete relation.  With ``record_relations=False``, compact record metadata
    is returned while complete witness maps remain internal for reconstruction.
    Bare-cycle support is optional and adds no factors.  Structural mode also
    exposes a redundant hub-equality factor implied by an original bipyramid;
    this can change primal adjacency and elimination order, never original edges.
    The Python API defaults to the historical table mode; the CLI chooses the
    structural mode by default when C5 inference is enabled.
    ``c5_queries`` counts attempted queries, including one partially charged
    query if the work budget interrupts its pure index calculation.
    Optional intersections additionally filter factor pairs on their complete
    shared interface (at least two variables); they do not require unique rows.
    Optional original-cycle closure feeds exact local unary supports back into
    the same fixed point.  Chords and external attachments remain factors;
    bounded cycle discovery is never a complete source-coverage claim.
    """
    from four_color_lab import graph_fingerprint, normalize_graph, verify_coloring
    from four_color_c5 import C5_ROWS, find_induced_c5, find_local_c5, query_c5
    from four_color_conflicts import KnownConflictIndex, conflict_catalogue
    from four_color_intersections import intersect_on_shared

    g = normalize_graph(graph)
    if any(type(value) is not bool for value in (use_substructures, record_relations, use_c5, use_conflicts, use_intersections, use_cycles)):
        raise ValueError("use_substructures, record_relations, use_c5, use_conflicts, use_intersections and use_cycles must be booleans")
    if c5_method not in ("structure", "table"):
        raise ValueError("c5_method must be structure or table")
    if any(type(value) is not int or value < 0
           for value in (max_checks, trace_limit, c5_max_cycles, c5_max_scan_steps,
                         cycle_max_cycles, cycle_max_scan_steps)):
        raise ValueError("limits must be nonnegative integers")
    if c5_scan_method not in ("complete", "local"):
        raise ValueError("c5_scan_method must be complete or local")
    if c5_scan_method == "local" and not use_c5:
        raise ValueError("local C5 scanning requires use_c5=True")

    vertices = g["vertices"]
    index = {vertex: position for position, vertex in enumerate(vertices)}
    finder = find_local_c5 if c5_scan_method == "local" else find_induced_c5
    c5_scan = finder(g, c5_max_cycles, c5_max_scan_steps) if use_c5 else {
        "cycles": [], "steps": 0, "complete": None, "truncated": False,
    }
    c5_cycles = [tuple(index[vertex] for vertex in cycle) for cycle in c5_scan["cycles"]]
    c5_last_domains = {}
    original_cycles, cycle_last_domains = {}, {}
    cycle_discovery_signature = None
    cycle_scan = dict(cycles=[], scan_steps=0, discoveries=0, truncated=False,
                      all_cycles_complete=False,
                      coverage="bounded fundamental cycles of active original graph and domain-induced subgraphs; not all cycles")
    adjacency = [set() for _ in vertices]
    for a, b in g["edges"]:
        adjacency[index[a]].add(index[b])
        adjacency[index[b]].add(index[a])
    domains = [set(range(4)) for _ in vertices]
    domain_edges = [set() for _ in vertices]
    domain_vertices = [set() for _ in vertices]
    colors = [-1] * len(vertices)
    for vertex, color in g["fixed"]:
        domains[index[vertex]] = {color}
        domain_vertices[index[vertex]].add(vertex)
        colors[index[vertex]] = color
    conflict_index = KnownConflictIndex(vertices, g["edges"]) if use_conflicts else None
    conflict_subgraphs = []

    # Enumerate cliques by common-neighbour intersections, never by n^4 scans.
    triangles, k4 = [], []
    for a in range(len(vertices)):
        for b in sorted(v for v in adjacency[a] if v > a):
            common = adjacency[a] & adjacency[b]
            for c in sorted(v for v in common if v > b):
                triangles.append((a, b, c))
                for d in sorted(v for v in common & adjacency[c] if v > c):
                    k4.append((a, b, c, d))
    covered_triangles = {triple for clique in k4 for triple in combinations(clique, 3)}
    selected_triangles = [triple for triple in triangles if triple not in covered_triangles] if use_substructures else []
    selected_k4 = k4 if use_substructures else []
    covered_edges = {edge for clique in selected_k4 + selected_triangles
                     for edge in combinations(clique, 2)}
    uncovered_edges = [(index[a], index[b]) for a, b in g["edges"]
                       if tuple(sorted((index[a], index[b]))) not in covered_edges]

    def original_edges(scope):
        return frozenset(tuple(sorted((vertices[a], vertices[b])))
                         for a, b in combinations(scope, 2))

    factors = [
        _Factor(tuple(scope), rows, original_edges(scope),
                frozenset(vertices[v] for v in scope))
        for scopes, rows in ((selected_k4, K4_ROWS),
                             (selected_triangles, TRIANGLE_ROWS),
                             (uncovered_edges, EDGE_ROWS))
        for scope in scopes
    ]
    template_hits = len(factors)
    self_constraints = []
    equality_pairs = set()
    if use_c5 and c5_method == "structure":
        for ring in c5_cycles:
            hubs = sorted(set.intersection(*(adjacency[v] for v in ring)) - set(ring))
            for hub in hubs[1:]:
                pair = (hubs[0], hub)
                if pair in equality_pairs:
                    continue
                equality_pairs.add(pair)
                source_edges = {tuple(sorted((vertices[ring[i]], vertices[ring[(i + 1) % 5]])))
                                for i in range(5)}
                source_edges.update(tuple(sorted((vertices[center], vertices[v])))
                                    for center in pair for v in ring)
                rows = frozenset((color, color) for color in range(4))
                selected = [vertices[v] for v in (*ring, *pair)]
                record = dict(id="c5_hub_equality", name="五環雙中心等色",
                              cycle=[vertices[v] for v in ring], boundary=[vertices[v] for v in pair],
                              vertices=selected, edges=[list(edge) for edge in sorted(source_edges)],
                              rows=[list(row) for row in sorted(rows)],
                              condition="兩個不同原頂點都鄰接同一五環的全部五點。",
                              conclusion="兩中心若異色，五環只能用剩下兩色而矛盾，所以兩中心必須同色。",
                              scope="original-subgraph", relation="equality",
                              relation_contract="exact hub projection of the bare 15-edge bipyramid; all other original constraints are retained")
                self_constraints.append(record)
                factors.append(_Factor(pair, rows, frozenset(source_edges), frozenset(selected)))
    substructures = {
        "triangles": len(triangles), "k4": len(k4), "edges": len(g["edges"]),
        "selected_triangles": len(selected_triangles), "selected_k4": len(selected_k4),
        "uncovered_edges": len(uncovered_edges), "template_hits": template_hits,
        "c5": len(c5_cycles), "c5_selected": len(c5_cycles),
        "c5_scan_complete": c5_scan["complete"], "c5_scan_steps": c5_scan["steps"],
        "c5_scan_algorithm": c5_scan.get("algorithm"),
        "c5_scan_step_unit": c5_scan.get("step_unit"),
        "c5_scan_method": c5_scan_method if use_c5 else None,
        "c5_method": c5_method if use_c5 else None,
        "known_conflicts_enabled": use_conflicts,
        "self_constraints": len(self_constraints),
        "c5_scan_coverage": c5_scan.get("coverage", "all-induced-c5" if use_c5 else None),
        "c5_local_scan_complete": c5_scan.get("local_scan_complete"),
        "c5_discovery_centers": c5_scan.get("centers", []),
        "c5_scan_truncated": c5_scan["truncated"], "c5_template_rows": len(C5_ROWS),
        "template_hits_definition": "initial edge/triangle/K4 factors reuse immutable tables; C5 lookups are counted as c5_queries; no cached graph solutions",
        "instances": {
            "triangles": [[vertices[v] for v in clique] for clique in triangles],
            "k4": [[vertices[v] for v in clique] for clique in k4],
            "selected_triangles": [[vertices[v] for v in clique] for clique in selected_triangles],
            "uncovered_edges": [[vertices[v] for v in edge] for edge in uncovered_edges],
            "c5": [list(cycle) for cycle in c5_scan["cycles"]],
            "conflicts": conflict_subgraphs,
            "self_constraints": self_constraints,
        },
    }
    stats = dict(checks=0, candidate_checks=0, relation_checks=0, prunes=0,
                 row_prunes=0, eliminations=0, writebacks=0, conflicts=0,
                 peak_scope=max((len(f.scope) for f in factors), default=0),
                 peak_frontier=0,
                 peak_rows=sum(len(f.rows) for f in factors), table_rows=0,
                 certificate_rows=0, template_hits=template_hits,
                 c5_queries=0, c5_skips=0, c5_prunes=0, c5_conflicts=0,
                 c5_index_ops=0, c5_scan_steps=c5_scan["steps"], c5_inactive_skips=0,
                 c5_structure_ops=0, conflict_checks=0, known_conflicts=0,
                 self_constraints=len(self_constraints),
                 intersection_checks=0, intersection_pairs=0, intersection_prunes=0,
                 cycle_queries=0, cycle_prunes=0, cycle_checks=0, cycle_conflicts=0,
                 cycle_scan_steps=0, cycle_skips=0, cycle_inactive_skips=0,
                 decisions=0, backtracks=0, assignments=0)
    counts = dict.fromkeys((rule["id"] for rule in CONSTRAINT_RULES), 0)
    events, records, witness_maps, eliminated = [], [], [], []
    active = set(range(len(vertices)))
    emitted = 0
    max_table_rows = min(max_checks, TABLE_ROW_CEILING)
    status = None

    def check(kind):
        if stats["checks"] >= max_checks:
            raise _WorkLimit(f"已達 {max_checks} 次候選／關係檢查上限；尚未判定。")
        stats["checks"] += 1
        stats[kind] += 1

    def emit(kind, rule=None, vertex=None, color=None, detail="", phase="reduce", **extra):
        nonlocal emitted
        emitted += 1
        if len(events) >= trace_limit:
            return
        event = dict(
            kind=kind, rule=rule, colors=colors[:],
            domains=[[colors[i]] if phase != "reduce" and colors[i] >= 0
                     else sorted(domain) for i, domain in enumerate(domains)],
            depth=len(eliminated), vertex=vertex, color=color, detail=detail,
            phase=phase, eliminated_vertices=[vertices[v] for v in eliminated],
            frontier=[], relation_rows=0,
            live_relation_rows=sum(len(f.rows) for f in factors),
            relation_preview=[], blockers=[], causal_vertices=[], causal_edges=[],
            conflict_edges=[], stats=stats.copy(), rule_counts=counts.copy(),
        )
        event.update(extra)
        events.append(event)

    def explain(factor):
        return dict(causal_vertices=sorted(factor.source_vertices),
                    causal_edges=[list(edge) for edge in sorted(factor.source_edges)])

    def record_known_conflict(witness):
        selected = [index[v] for v in witness["vertices"]]
        source_edges = {tuple(sorted(edge)) for edge in witness["edges"]}
        source_edges.update(edge for v in selected for edge in domain_edges[v])
        source_vertices = set(witness["vertices"])
        source_vertices.update(vertex for v in selected for vertex in domain_vertices[v])
        witness.update(causal_edges=[list(edge) for edge in sorted(source_edges)],
                       causal_vertices=sorted(source_vertices))
        conflict_subgraphs.append(witness)
        stats["conflicts"] += 1
        stats["known_conflicts"] += 1
        counts["C1"] += 1
        emit("conflict", "C1", detail=f"結構推出矛盾：{witness['name']}。{witness['condition']}尚未寫色。",
             frontier=witness["vertices"], conflict_edges=witness["edges"],
             conflict_shape=witness["id"], conflict_template_id=witness["id"],
             conflict_subgraph=witness, causal_edges=witness["causal_edges"],
             causal_vertices=witness["causal_vertices"], relation_rows=0)

    def propagate_known():
        """Original-edge singleton implications, then sufficient motif guards."""
        if conflict_index is None:
            return True

        def charge():
            check("relation_checks")
            stats["conflict_checks"] += 1

        changed = True
        while changed:
            witness = conflict_index.find(domains, fixed=g["fixed"], charge=charge)
            if witness is not None:
                record_known_conflict(witness)
                return False
            changed = False
            for a, b in g["edges"]:
                for u, v in ((index[a], index[b]), (index[b], index[a])):
                    if len(domains[u]) != 1 or len(domains[v]) <= 1:
                        continue
                    charge()
                    color = next(iter(domains[u]))
                    if color in domains[v]:
                        domains[v].remove(color)
                        domain_edges[v].update(domain_edges[u])
                        domain_edges[v].add(tuple(sorted((vertices[u], vertices[v]))))
                        domain_vertices[v].update(domain_vertices[u])
                        domain_vertices[v].update((vertices[u], vertices[v]))
                        stats["prunes"] += 1
                        counts["C1"] += 1
                        changed = True
                        emit("propagate", "C1", detail=f"原邊 {vertices[u]}–{vertices[v]}：點 {vertices[u]} 只剩色 {color + 1}，故另一端排除此色；尚未寫色。",
                             frontier=[vertices[u], vertices[v]],
                             causal_edges=[list(edge) for edge in sorted(domain_edges[v])],
                             causal_vertices=sorted(domain_vertices[v]))
        return True

    def contradiction(factor, detail, vertex=None):
        stats["conflicts"] += 1
        emit("conflict", vertex=vertex, detail=detail,
             conflict_edges=[list(edge) for edge in sorted(factor.source_edges)],
             frontier=[vertices[v] for v in factor.scope],
             relation_rows=0,
             conflict_shape="empty_joint_relation", **explain(factor))

    def propagate_c5():
        """Exact local support by structure or table; this pass adds no factors."""
        any_change = False

        def charge_index():
            check("relation_checks")
            stats["c5_structure_ops" if c5_method == "structure" else "c5_index_ops"] += 1

        for cycle in c5_cycles:
            if any(v not in active for v in cycle):
                stats["c5_inactive_skips"] += 1
                continue
            signature = tuple(sum(1 << color for color in domains[v]) for v in cycle)
            if c5_last_domains.get(cycle) == signature:
                stats["c5_skips"] += 1
                continue
            first_query = cycle not in c5_last_domains
            stats["c5_queries"] += 1
            # The callback charges before every operation; a limit interrupts
            # this pure query before any candidate domain can be changed.
            if c5_method == "structure":
                from four_color_cycle_structure import derive_c5
                answer = derive_c5(signature, charge=charge_index)
            else:
                answer = query_c5(signature, charge=charge_index)
            source_edges = {tuple(sorted((vertices[cycle[i]], vertices[cycle[(i + 1) % 5]])))
                            for i in range(5)}
            source_edges.update(edge for v in cycle for edge in domain_edges[v])
            source_vertices = {vertices[v] for v in cycle}
            source_vertices.update(vertex for v in cycle for vertex in domain_vertices[v])
            removed = 0
            for offset, v in enumerate(cycle):
                narrowed = {color for color in range(4) if answer["supports"][offset] & (1 << color)}
                removed += len(domains[v]) - len(narrowed)
                if narrowed != domains[v]:
                    domain_edges[v].update(source_edges)
                    domain_vertices[v].update(source_vertices)
                    domains[v] = narrowed
            stats["c5_prunes"] += removed
            stats["prunes"] += removed
            # Projecting supports is idempotent for this exact same relation;
            # cache the post-projection signature to skip the next unchanged pass.
            c5_last_domains[cycle] = tuple(answer["supports"])
            fields = dict(
                relation_kind="c5", frontier=[vertices[v] for v in cycle],
                relation_rows=answer["row_count"],
                causal_edges=[list(edge) for edge in sorted(source_edges)],
                causal_vertices=sorted(source_vertices),
                domain_masks=list(signature), supported_domain_masks=answer["supports"],
                c5_method=c5_method,
            )
            structural_rules = []
            for rule in answer.get("rules", []):
                rule = dict(rule)
                rule["vertices"] = [vertices[cycle[position]] for position in rule.get("vertices", [])]
                for key in ("vertex", "fixed_vertex"):
                    if key in rule:
                        rule[key] = vertices[cycle[rule[key]]]
                if "edge" in rule:
                    rule["edge"] = [vertices[cycle[position]] for position in rule["edge"]]
                if rule.get("id") == "cycle_path_consistency":
                    rule["anchor_vertex"] = vertices[cycle[0]]
                    rule["condition"] = f"逐一固定原環首點 {vertices[cycle[0]]} 的候選色，沿四邊路徑計數，再核對閉合邊。"
                structural_rules.append(rule)
            fields["structural_rules"] = structural_rules
            if not answer["row_count"]:
                stats["c5_conflicts"] += 1
                stats["conflicts"] += 1
                counts["C1"] += 1
                emit("conflict", "C1", detail=f"C5 {'結構推導' if c5_method == 'structure' else '查表'}得到零個共同色組；尚未寫色。",
                     conflict_edges=[list(edge) for edge in sorted(source_edges)],
                     conflict_shape="empty_c5_relation", **fields)
                return False, any_change
            if removed:
                counts["C1"] += 1
                any_change = True
            if first_query or removed:
                preview = []
                if len(events) < trace_limit:
                    if c5_method == "structure":
                        preview = [dict(boundary=list(row), colors=[]) for row in answer.get("relation_preview", [])]
                    else:
                        bits = answer["allowed_bits"]
                        while bits and len(preview) < 6:
                            lowest = bits & -bits
                            row_index = lowest.bit_length() - 1
                            preview.append(dict(boundary=list(C5_ROWS[row_index]), colors=[]))
                            bits ^= lowest
                emit("c5_structure" if c5_method == "structure" else "c5_lookup", "C1", detail=f"C5 {'沿環結構推導' if c5_method == 'structure' else '索引'}留下 {answer['row_count']} 個完整色組，刪去 {removed} 個候選色；尚未寫色。",
                     relation_preview=preview, **fields)
        return True, any_change

    def intersection_charge():
        check("relation_checks")
        stats["intersection_checks"] += 1

    def find_intersection_pairs():
        # Use shared-variable incidence instead of comparing every factor pair.
        # Even pair discovery is charged, so dense instances respect the budget.
        incidence = {}
        for position, factor in enumerate(factors):
            for vertex in factor.scope:
                incidence.setdefault(vertex, []).append(position)
        shared_counts = {}
        for vertex in sorted(incidence):
            for pair in combinations(incidence[vertex], 2):
                intersection_charge()
                shared_counts[pair] = shared_counts.get(pair, 0) + 1
        return sorted(pair for pair, size in shared_counts.items() if size >= 2)

    def propagate_intersections(pairs, seen):
        changed = False
        for left_index, right_index in pairs:
            left, right = factors[left_index], factors[right_index]
            signature = (left.revision, right.revision)
            if seen.get((left_index, right_index)) == signature:
                continue
            stats["intersection_pairs"] += 1
            answer = intersect_on_shared(left.scope, left.rows, right.scope, right.rows,
                                         charge=intersection_charge)
            left_removed = len(left.rows) - len(answer["left_rows"])
            right_removed = len(right.rows) - len(answer["right_rows"])
            if left_removed or right_removed:
                source_edges = left.source_edges | right.source_edges
                source_vertices = left.source_vertices | right.source_vertices
                for factor, kept, removed in ((left, answer["left_rows"], left_removed),
                                              (right, answer["right_rows"], right_removed)):
                    if removed:
                        factor.rows = kept
                        factor.revision += 1
                        factor.source_edges = source_edges
                        factor.source_vertices = source_vertices
                removed = left_removed + right_removed
                stats["row_prunes"] += removed
                stats["intersection_prunes"] += removed
                counts["C1"] += 1
                changed = True
                emit("intersection", "C1",
                     detail=f"共同接口整列取交集：保留 {len(answer['common_rows'])} 個共同色組，兩表共刪 {removed} 列；尚未寫色。",
                     frontier=[vertices[v] for v in answer["scope"]],
                     relation_rows=len(answer["common_rows"]),
                     relation_preview=[dict(boundary=list(row), colors=[]) for row in
                                       islice(sorted(answer["common_rows"]), 8)] if len(events) < trace_limit else [],
                     left_scope=[vertices[v] for v in left.scope],
                     right_scope=[vertices[v] for v in right.scope],
                     left_removed=left_removed, right_removed=right_removed,
                     causal_edges=[list(edge) for edge in sorted(source_edges)],
                     causal_vertices=sorted(source_vertices))
                if not answer["common_rows"]:
                    contradiction(left, "兩張完整關係在共同接口上的交集為空；沒有共同延伸。")
                    return False, changed
            seen[(left_index, right_index)] = (left.revision, right.revision)
        return True, changed

    def propagate_cycles():
        """Bounded original-cycle discovery, exact closure, then domain feedback."""
        nonlocal cycle_discovery_signature
        from four_color_cycle_propagation import find_original_cycles
        from four_color_local_information import derive_cycle

        def charge_cycle():
            check("relation_checks")
            stats["cycle_checks"] += 1

        def charge_discovery():
            charge_cycle()
            stats["cycle_scan_steps"] += 1

        selected = tuple(sorted(active))
        domain_signature = tuple(sum(1 << color for color in domains[v]) for v in selected)
        signature = (selected, domain_signature)
        if signature != cycle_discovery_signature and len(selected) >= 3:
            original_ids = {vertices[v] for v in selected}
            active_graph = dict(vertices=[vertices[v] for v in selected],
                                edges=[edge for edge in g["edges"]
                                       if edge[0] in original_ids and edge[1] in original_ids])
            cycle_scan["discoveries"] += 1
            try:
                found = find_original_cycles(
                    active_graph, domain_signature,
                    max_cycles=max(0, cycle_max_cycles - len(original_cycles)),
                    max_scan_steps=cycle_max_scan_steps, charge=charge_discovery)
            except _WorkLimit:
                cycle_scan["truncated"] = True
                cycle_scan["last_discovery_complete"] = False
                cycle_scan["last_discovery_interrupted"] = True
                cycle_scan["scan_steps"] = stats["cycle_scan_steps"]
                raise
            cycle_scan["last_discovery_interrupted"] = False
            for literal_cycle in found["cycles"]:
                cycle = tuple(index[v] for v in literal_cycle)
                if cycle not in original_cycles:
                    original_cycles[cycle] = tuple(literal_cycle)
            cycle_discovery_signature = signature
            cycle_scan["cycles"] = [list(cycle) for cycle in original_cycles.values()]
            cycle_scan["scan_steps"] = stats["cycle_scan_steps"]
            cycle_scan["truncated"] = cycle_scan["truncated"] or found["truncated"]
            cycle_scan["last_discovery_complete"] = found["complete"]
            cycle_scan["last_discovery"] = {
                key: value for key, value in found.items() if key != "cycles"}

        changed = False
        for cycle, literal_cycle in original_cycles.items():
            if any(v not in active for v in cycle):
                stats["cycle_inactive_skips"] += 1
                continue
            masks = tuple(sum(1 << color for color in domains[v]) for v in cycle)
            if cycle_last_domains.get(cycle) == masks:
                stats["cycle_skips"] += 1
                continue
            stats["cycle_queries"] += 1
            # Query is pure and charged before each DP stage.  No partial
            # result changes domains if the shared work limit interrupts it.
            answer = derive_cycle(masks, charge=charge_cycle)
            try:
                count_decimal = str(answer["row_count"])
            except ValueError as error:
                # Python bounds decimal conversion of very large integers.
                # The query is still uncommitted, so stop as an explicit
                # resource limit instead of crashing or losing exact counts.
                raise _WorkLimit("原環的精確局部計數超出十進位記錄上限；尚未判定。") from error
            source_edges = {
                tuple(sorted((vertices[cycle[i]], vertices[cycle[(i + 1) % len(cycle)]])))
                for i in range(len(cycle))}
            source_edges.update(edge for v in cycle for edge in domain_edges[v])
            source_vertices = {vertices[v] for v in cycle}
            source_vertices.update(vertex for v in cycle for vertex in domain_vertices[v])
            removed = 0
            for position, v in enumerate(cycle):
                supported = {color for color in range(4)
                             if answer["supports"][position] & (1 << color)}
                narrowed = domains[v] & supported
                removed += len(domains[v]) - len(narrowed)
                if narrowed != domains[v]:
                    domain_edges[v].update(source_edges)
                    domain_vertices[v].update(source_vertices)
                    domains[v] = narrowed
            cycle_last_domains[cycle] = tuple(answer["supports"])
            stats["cycle_prunes"] += removed
            stats["prunes"] += removed
            if removed:
                changed = True
            fields = dict(
                relation_kind="cycle", frontier=list(literal_cycle),
                cycle_length=len(cycle), relation_rows=answer["row_count"],
                relation_rows_decimal=count_decimal,
                domain_masks=list(masks), supported_domain_masks=answer["supports"],
                causal_edges=[list(edge) for edge in sorted(source_edges)],
                causal_vertices=sorted(source_vertices),
                cycle_method=answer["method"], state_capacity=answer["state_capacity"],
                cycle_contract=answer["relation_contract"])
            if not answer["row_count"]:
                stats["cycle_conflicts"] += 1
                stats["conflicts"] += 1
                counts["C1"] += 1
                emit("conflict", "C1", detail=f"原 {len(cycle)} 點環沿同一首點色無法閉合；完整局部關係為空，尚未寫色。",
                     conflict_edges=[list(edge) for edge in sorted(source_edges)],
                     conflict_shape="empty_original_cycle", **fields)
                return False, changed
            counts["C1"] += 1
            emit("cycle_query", "C1",
                 detail=f"原 {len(cycle)} 點環閉合檢查保留 {count_decimal} 個完整局部色組，刪去 {removed} 個候選色；回饋共同傳播，尚未寫色。",
                 **fields)
        return True, changed

    def propagate():
        """Domain consistency, plus optional complete shared-tuple filtering."""
        pairs, seen = None, {}
        changed = True
        while changed:
            changed = False
            if not propagate_known():
                return False
            for factor in factors:
                kept = []
                for row in factor.rows:
                    check("relation_checks")
                    if all(row[offset] in domains[v] for offset, v in enumerate(factor.scope)):
                        kept.append(row)
                removed_rows = len(factor.rows) - len(kept)
                if removed_rows:
                    # Domain restrictions may have come from outside this
                    # factor.  Carry their original-edge provenance so the
                    # displayed cause includes those earlier deductions.
                    factor.source_edges = frozenset(
                        set(factor.source_edges) |
                        {edge for v in factor.scope for edge in domain_edges[v]})
                    factor.source_vertices = frozenset(
                        set(factor.source_vertices) |
                        {vertex for v in factor.scope for vertex in domain_vertices[v]})
                    factor.rows = frozenset(kept)
                    factor.revision += 1
                    stats["row_prunes"] += removed_rows
                if not factor.rows:
                    if factor.scope:
                        v = factor.scope[0]
                        stats["prunes"] += len(domains[v])
                        domains[v] = set()
                    counts["C1"] += 1
                    contradiction(factor, "完整關係表已空：這些原邊限制與目前候選域沒有共同延伸。",
                                  vertices[factor.scope[0]] if factor.scope else None)
                    return False
                supports = [set() for _ in factor.scope]
                for row in factor.rows:
                    for offset, color in enumerate(row):
                        supports[offset].add(color)
                removed_colors = 0
                for offset, v in enumerate(factor.scope):
                    narrowed = domains[v] & supports[offset]
                    removed_colors += len(domains[v]) - len(narrowed)
                    if narrowed != domains[v]:
                        domain_edges[v].update(factor.source_edges)
                        domain_vertices[v].update(factor.source_vertices)
                    domains[v] = narrowed
                if removed_rows or removed_colors:
                    stats["prunes"] += removed_colors
                    counts["C1"] += 1
                    changed = True
                    emit("propagate", "C1", detail=f"關係表刪去 {removed_rows} 列，候選域刪去 {removed_colors} 個顏色；尚未寫色。",
                         frontier=[vertices[v] for v in factor.scope],
                         relation_rows=len(factor.rows), **explain(factor))
            if use_intersections:
                if pairs is None:
                    pairs = find_intersection_pairs()
                compatible, intersection_changed = propagate_intersections(pairs, seen)
                if not compatible:
                    return False
                changed = changed or intersection_changed
            if c5_cycles:
                compatible, c5_changed = propagate_c5()
                if not compatible:
                    return False
                changed = changed or c5_changed
            if use_cycles:
                # First settle the ordinary factors and whole-interface
                # intersections, so their new domains guide cycle discovery.
                if changed:
                    continue
                compatible, cycle_changed = propagate_cycles()
                if not compatible:
                    return False
                changed = changed or cycle_changed
        return True

    def select_vertex():
        primal = {v: set() for v in active}
        for factor in factors:
            for v in factor.scope:
                primal[v].update(w for w in factor.scope if w != v)

        def priority(v):
            neighbors = primal[v]
            missing = sum(b not in primal[a] for a, b in combinations(sorted(neighbors), 2))
            return missing, len(neighbors), v

        return min(active, key=priority)

    def snapshot_factor(factor):
        return dict(scope=[vertices[v] for v in factor.scope],
                    rows=[list(row) for row in sorted(factor.rows)],
                    source_edges=[list(edge) for edge in sorted(factor.source_edges)],
                    source_vertices=sorted(factor.source_vertices))

    emit("start", detail="先保留每點可能色，傳播並記錄完整邊界關係；全部消去成功後才反向寫色。",
         use_c5=use_c5, c5_selected=len(c5_cycles), c5_scan_complete=c5_scan["complete"],
         c5_scan_steps=c5_scan["steps"])
    for record in self_constraints:
        emit("structural_constraint", "C1", detail=record["conclusion"],
             relation_kind="c5_hub_equality", frontier=record["boundary"],
             relation_rows=4, relation_preview=[dict(boundary=row, colors=[]) for row in record["rows"]],
             structural_rules=[record], self_constraint=record,
             causal_edges=record["edges"], causal_vertices=record["vertices"], c5_method="structure")
    try:
        if not propagate():
            status = "unsatisfiable"
        while active and status is None:
            v = select_vertex()
            bucket = [factor for factor in factors if v in factor.scope]
            union_scope = sorted({v} | {w for factor in bucket for w in factor.scope})
            frontier = tuple(w for w in union_scope if w != v)
            stats["peak_scope"] = max(stats["peak_scope"], len(union_scope))
            stats["peak_frontier"] = max(stats["peak_frontier"], len(frontier))
            source_edges = frozenset(
                {edge for factor in bucket for edge in factor.source_edges} |
                {edge for w in union_scope for edge in domain_edges[w]})
            source_vertices = frozenset(
                {vertices[v]} | {w for factor in bucket for w in factor.source_vertices} |
                {vertex for w in union_scope for vertex in domain_vertices[w]})
            offsets = {w: offset for offset, w in enumerate(frontier)}
            prepared = [(factor, tuple(-1 if w == v else offsets[w] for w in factor.scope))
                        for factor in bucket]
            table = {}
            for boundary in product(*(sorted(domains[w]) for w in frontier)):
                choices = []
                for color in sorted(domains[v]):
                    check("candidate_checks")
                    valid = True
                    for factor, positions in prepared:
                        check("relation_checks")
                        row = tuple(color if offset == -1 else boundary[offset] for offset in positions)
                        if row not in factor.rows:
                            valid = False
                            break
                    if valid:
                        choices.append(color)
                if choices:
                    if stats["table_rows"] >= max_table_rows:
                        raise _WorkLimit(f"完整關係表已達 {max_table_rows} 列儲存上限；尚未判定。")
                    table[boundary] = tuple(choices)
                    stats["table_rows"] += 1

            projected = _Factor(frontier, frozenset(table), source_edges, source_vertices)
            record = dict(vertex=vertices[v], scope=[vertices[w] for w in frontier],
                          source_edges=[list(edge) for edge in sorted(source_edges)],
                          source_vertices=sorted(source_vertices), relation_rows=len(table),
                          complete=True,
                          absent_boundary="empty fibre within the recorded source_domains")
            if record_relations:
                snapshot_rows = sum(len(factor.rows) for factor in bucket) + len(table)
                if stats["certificate_rows"] + snapshot_rows > max_table_rows:
                    raise _WorkLimit(f"完整關係記錄已達 {max_table_rows} 列儲存上限；尚未判定。")
                stats["certificate_rows"] += snapshot_rows
                record["rows"] = [dict(boundary=list(boundary), colors=list(choices))
                                  for boundary, choices in table.items()]
                record["source_domains"] = [dict(vertex=vertices[w], colors=sorted(domains[w]))
                                            for w in union_scope]
                record["input_relations"] = [snapshot_factor(factor) for factor in bucket]
            records.append(record)
            if not table:
                contradiction(projected, f"消去點 {vertices[v]} 時，沒有任何完整邊界色組可以共同延伸。", vertices[v])
                status = "unsatisfiable"
                break

            witness_maps.append((v, frontier, table))
            factors = [factor for factor in factors if v not in factor.scope]
            if frontier:
                factors.append(projected)
            active.remove(v)
            eliminated.append(v)
            stats["eliminations"] += 1
            counts["C2"] += 1
            stats["peak_rows"] = max(stats["peak_rows"], sum(len(factor.rows) for factor in factors))
            preview = [dict(boundary=list(boundary), colors=list(choices))
                       for boundary, choices in islice(table.items(), 8)] if len(events) < trace_limit else []
            emit("eliminate", "C2", vertices[v],
                 detail=f"消去點 {vertices[v]}：保存 {len(table)} 個完整邊界色組及其所有可用色；尚未寫色。",
                 frontier=[vertices[w] for w in frontier], relation_preview=preview,
                 relation_rows=len(table),
                 **explain(projected))
            if not propagate():
                status = "unsatisfiable"

        if status is None:
            # All elimination succeeded.  Every lookup is guaranteed by the
            # exact projected relation used when eliminating later variables.
            for v, frontier, table in reversed(witness_maps):
                boundary = tuple(colors[w] for w in frontier)
                if any(color < 0 for color in boundary) or boundary not in table:
                    raise AssertionError("missing complete frontier witness during writeback")
                choices = table[boundary]
                if colors[v] >= 0:
                    if colors[v] not in choices:
                        raise AssertionError("fixed colour lost during reconstruction")
                    continue
                colors[v] = min(choices)
                stats["writebacks"] += 1
                stats["assignments"] += 1
                counts["C3"] += 1
                emit("writeback", "C3", vertices[v], colors[v],
                     detail=f"完整邊界色組查表成功，將點 {vertices[v]} 寫為色 {colors[v] + 1}。",
                     phase="writeback", frontier=[vertices[w] for w in frontier],
                     relation_rows=len(table),
                     relation_preview=[dict(boundary=list(boundary), colors=list(choices))])
            if not verify_coloring(g, colors):
                raise AssertionError("constraint solver produced an invalid original-graph witness")
            status = "colored"
            emit("solution", detail="全部原邊與固定色已直接核對；完整共同見證成立。", phase="done")
    except _WorkLimit as limit:
        status = "limit"
        emit("limit", detail=str(limit), phase="done")

    if status == "unsatisfiable":
        emit("end", detail="限制的完整共同關係為空；這份固定色無法延伸。" if g["fixed"] else
             "限制的完整共同關係為空；此圖不存在四色染色。", phase="done")
    cycle_scan["scan_steps"] = stats["cycle_scan_steps"]
    return dict(
        name=g.get("name", "自訂圖"), description=g.get("description", ""), graph=g,
        engine="constraints", status=status, colors=colors,
        domains=[[colors[i]] if colors[i] >= 0 else sorted(domain)
                 for i, domain in enumerate(domains)],
        events=events, stats=stats, rules=CONSTRAINT_RULES,
        rule_counts=counts, trace_truncated=emitted > len(events), event_count=emitted,
        graph_sha256=graph_fingerprint(g), use_substructures=use_substructures,
        use_c5=use_c5, c5_max_cycles=c5_max_cycles, c5_max_scan_steps=c5_max_scan_steps,
        c5_scan_method=c5_scan_method,
        c5_method=c5_method, use_conflicts=use_conflicts, use_intersections=use_intersections,
        use_cycles=use_cycles, cycle_max_cycles=cycle_max_cycles,
        cycle_max_scan_steps=cycle_max_scan_steps, cycle_scan=cycle_scan,
        conflict_catalogue=conflict_catalogue(include_rows=False),
        conflict_subgraphs=conflict_subgraphs,
        self_constraints=self_constraints,
        conflict_scan_steps=conflict_index.last_scan_steps if conflict_index else 0,
        conflict_scan_truncated=conflict_index.last_scan_truncated if conflict_index else False,
        conflict_scan_coverage="bounded sufficient motifs; no completeness claim",
        record_relations=record_relations, max_checks=max_checks, max_table_rows=max_table_rows,
        substructures=substructures, elimination_records=records,
        relation_contract="exact allowed rows of the join of input_relations under source_domains; absent boundary tuples have empty fibres; source_edges alone are provenance",
    )
