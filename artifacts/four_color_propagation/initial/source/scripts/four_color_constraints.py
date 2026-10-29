"""Exact four-colour constraints: propagate, eliminate, then write back.

No unknown vertex receives a colour during reduction.  Eliminating a variable
stores the *complete joint* frontier relation, including every possible colour
of the eliminated variable for each allowed frontier tuple.  Reverse lookup is
therefore witness reconstruction, not a search over guessed assignments.
Internal reconstruction fibres use four-bit masks; public records still expose
every literal colour in sorted lists.  No boundary tuple or colour is dropped.

``checks`` counts candidate attempts, relation-row filtering/membership tests,
and enabled C5 index operations.  ``max_checks`` bounds that sum; a separate row
budget bounds cumulative generated tables and optional certificate snapshots.
It defaults to ``min(max_checks, 1000000)``; explicit ``max_table_rows`` can use
more memory without increasing the work budget.  Neither
limit means unsatisfiable.  Graph bookkeeping and final witness verification
are not charged as relation checks.  General variable elimination remains
exponential in frontier width.  Optional induced-C5 discovery has its own
cycle/scan-step limits; a truncated discovery only omits redundant propagators.
The optional prefix bucket method counts each attempted prefix extension as a
candidate check and rejects it as soon as a complete input factor fails.  It
preserves the same full join, fibres, original provenance and atomic records.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, islice, permutations, product
from math import prod


CONSTRAINT_RULES = [
    {"id": "C1", "name": "子構造限制傳播", "description": "由原子圖結構推出限制，或過濾完整關係；刪除沒有共同支援的候選色，只縮限，不填色。"},
    {"id": "C2", "name": "合併消去與記錄", "description": "合併同一點的全部關係，保存每個完整邊界色組及其所有可用內部色。"},
    {"id": "C3", "name": "反向查表寫回", "description": "全部消去成功後，依已確定的完整邊界色組查表，反向寫回合法顏色。"},
]

# Shared immutable literal-colour tables.  No quotient by colour permutations.
EDGE_ROWS = frozenset(permutations(range(4), 2))
TRIANGLE_ROWS = frozenset(permutations(range(4), 3))
K4_ROWS = frozenset(permutations(range(4), 4))
TABLE_ROW_CEILING = 1_000_000


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


def _fiber_colors(mask):
    """Decode a lossless four-colour fibre for the public evidence/trace."""
    return [color for color in range(4) if mask & (1 << color)]


def solve_constraints(graph, use_substructures=True, max_checks=1000000,
                      trace_limit=5000, record_relations=True, use_c5=False,
                      c5_max_cycles=128, c5_max_scan_steps=200000,
                      c5_scan_method="complete", use_conflicts=True,
                      c5_method="table", use_intersections=False, use_cycles=False,
                      cycle_max_cycles=128, cycle_max_scan_steps=200000,
                      use_cycle_contexts=False, cycle_context_max_contexts=128,
                      cycle_context_max_scan_steps=200000,
                      cycle_context_search="neighbours", use_joint_constraints=False,
                      joint_max_matches=128, joint_max_scan_steps=200000,
                      max_table_rows=None, use_interface_cache=False,
                      interface_cache_max_rows=1000000, bucket_method="anchor",
                      use_joint_consistency=False, joint_consistency_max_checks=200000,
                      partition_strategy="none", partition_block_size=12,
                      propagation_method="scan"):
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
    Optional cycle contexts preserve a common original exterior variable while
    closing a cycle, then feed complete binary/ternary projections to intersections.
    They require both intersections and cycles, and never commit a case colour.
    The historical ``neighbours`` search finds fully spoked cycles only.
    ``partial`` searches the active original graph minus the context vertex,
    permitting cycles with partial spokes; only actual spokes constrain them.
    Both searches are bounded, optional, and leave all original factors intact.
    Optional joint constraints automatically match the registered nine-point
    original-edge pattern and install its complete three-point equality factor
    before any elimination. Discovery is charged and bounded; omitted matches
    leave the original exact solver intact. No colour is chosen by the factor.
    ``max_table_rows=None`` uses min(max_checks, 1_000_000) rows. An explicit
    nonnegative integer independently bounds generated rows and complete
    certificate snapshots, without changing ``max_checks`` or omitting rows.
    ``use_interface_cache`` retains complete shared-interface row-group indexes
    in RAM for reuse across different factor pairs. Its independent row-reference
    budget evicts optional indexes rather than limiting the exact solver.
    ``bucket_method="anchor"`` preserves the historical complete-candidate
    enumeration.  ``"prefix"`` checks each input factor once all its variables
    are present in the current prefix, pruning only prefixes with no possible
    extension.  It counts actual prefix extensions in ``candidate_checks``
    (or one complete candidate when there are no free coordinates).  Both
    methods retain all joint fibres and provenance, leave live colours unwritten,
    and commit an elimination record only after its entire join is complete.
    Optional joint consistency first closes three-colour double-triangle
    equalities and palette exclusions on temporary equality classes. Later it
    joins incident factors and projects their common support without elimination.
    Hard joins can use one certified common colour-permutation group, restoring
    every literal support row before committing. Small joins avoid that overhead.
    This may cover the entire graph; it is charged joint computation, not a
    general bounded-width propagation guarantee. ``joint_consistency_max_checks``
    bounds the combined optional join work across this solve. An incomplete query
    commits nothing; when this extra allowance is exhausted, ordinary exact
    elimination continues. The main work budget remains authoritative.
    Optional partition schedules retain every live factor. Static partitions
    eliminate interiors before separators. Dynamic adaptive/information work
    regions use current scopes, domains and table sizes with a min-fill/width
    guard; message mode prioritizes estimated join work without that guard.
    Planning is included in runtime, outside the relation-check counter.
    """
    from four_color_lab import graph_fingerprint, normalize_graph, verify_coloring
    from four_color_partition import partition_plan, InformationScheduler, DYNAMIC_STRATEGIES
    from four_color_serialization import int_text
    from four_color_c5 import C5_ROWS, find_induced_c5, find_local_c5, query_c5
    from four_color_conflicts import KnownConflictIndex, conflict_catalogue
    from four_color_intersections import SharedInterfaceIndex, intersect_on_shared

    g = normalize_graph(graph)
    if any(type(value) is not bool for value in (use_substructures, record_relations, use_c5, use_conflicts, use_intersections, use_cycles, use_cycle_contexts, use_joint_constraints, use_interface_cache, use_joint_consistency)):
        raise ValueError("constraint feature flags must be booleans")
    if type(bucket_method) is not str or bucket_method not in ("anchor", "prefix"):
        raise ValueError("bucket_method must be anchor or prefix")
    if type(propagation_method) is not str or propagation_method not in ("scan", "delta"):
        raise ValueError("propagation_method must be scan or delta")
    if propagation_method == "delta" and not use_intersections:
        raise ValueError("delta propagation requires use_intersections=True")
    if use_interface_cache and not use_intersections:
        raise ValueError("interface cache requires use_intersections=True")
    if use_cycle_contexts and not (use_intersections and use_cycles):
        raise ValueError("cycle contexts require use_intersections=True and use_cycles=True")
    if cycle_context_search not in ("neighbours", "partial"):
        raise ValueError("cycle_context_search must be neighbours or partial")
    if cycle_context_search != "neighbours" and not use_cycle_contexts:
        raise ValueError("partial cycle-context search requires use_cycle_contexts=True")
    if c5_method not in ("structure", "table"):
        raise ValueError("c5_method must be structure or table")
    if any(type(value) is not int or value < 0
           for value in (max_checks, trace_limit, c5_max_cycles, c5_max_scan_steps,
                         cycle_max_cycles, cycle_max_scan_steps,
                         cycle_context_max_contexts, cycle_context_max_scan_steps,
                         joint_max_matches, joint_max_scan_steps, interface_cache_max_rows,
                         joint_consistency_max_checks)):
        raise ValueError("limits must be nonnegative integers")
    if max_table_rows is not None and (type(max_table_rows) is not int or max_table_rows < 0):
        raise ValueError("max_table_rows must be a nonnegative integer or None")
    if c5_scan_method not in ("complete", "local"):
        raise ValueError("c5_scan_method must be complete or local")
    if c5_scan_method == "local" and not use_c5:
        raise ValueError("local C5 scanning requires use_c5=True")

    plan = partition_plan(g, partition_strategy, partition_block_size)
    group_rank = {v: rank for rank, group in enumerate(plan["groups"]) for v in group}
    vertices = g["vertices"]
    scheduler = InformationScheduler(plan, vertices) if partition_strategy in DYNAMIC_STRATEGIES else None
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
    cycle_contexts, cycle_context_last_domains, context_interface_factors = {}, {}, {}
    factor_last_domains = {}
    joint_consistency_seen = {}
    triangle_equality_signature = None
    intersection_index = SharedInterfaceIndex(
        cache_max_rows=interface_cache_max_rows if use_interface_cache else 0,
        monotone_updates=propagation_method == "delta")
    cycle_context_discovery_signature = None
    cycle_context_scan = dict(contexts=[], scan_steps=0, discoveries=0,
                              truncated=False, all_contexts_complete=False,
                              coverage=("bounded original cycles in active original neighbour-induced subgraphs; not all contexts"
                                        if cycle_context_search == "neighbours" else
                                        "bounded original cycles in the active original graph minus each context vertex; partial actual spokes; not all contexts"))
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
    joint_scan = dict(constraints=[], scan_steps=0, complete=None, truncated=False,
                      interrupted=False,
                      coverage="bounded injective matches of the registered nine-point original-edge pattern only")
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
                 intersection_cache_hits=0, factor_cache_hits=0,
                 propagation_pair_visits=0, propagation_queue_pushes=0,
                 propagation_support_reuses=0,
                 interface_cache_hits=0, interface_cache_builds=0,
                 interface_cache_rows=0, interface_cache_peak_rows=0,
                 interface_cache_entries=0, interface_cache_evictions=0,
                 interface_cover_index_builds=0, interface_cover_index_factors=0,
                 cycle_queries=0, cycle_prunes=0, cycle_checks=0, cycle_conflicts=0,
                 cycle_scan_steps=0, cycle_skips=0, cycle_inactive_skips=0,
                 cycle_context_queries=0, cycle_context_prunes=0,
                 cycle_context_checks=0, cycle_context_conflicts=0,
                 cycle_context_rows=0, cycle_context_factors=0,
                 cycle_context_row_prunes=0, cycle_context_scan_steps=0,
                 cycle_context_redundant_interfaces=0,
                 cycle_context_skips=0, cycle_context_inactive_skips=0,
                 joint_scan_steps=0, joint_checks=0, joint_matches=0,
                 joint_factors=0, joint_rows=0,
                 decisions=0, backtracks=0, assignments=0)
    counts = dict.fromkeys((rule["id"] for rule in CONSTRAINT_RULES), 0)
    if use_joint_consistency:
        stats.update(joint_consistency_checks=0, joint_consistency_queries=0,
                     joint_consistency_incomplete=0, joint_consistency_cache_hits=0,
                     joint_consistency_row_prunes=0, joint_consistency_prunes=0,
                     joint_consistency_peak_scope=0, joint_support_checks=0,
                     joint_symmetry_checks=0, joint_normalized_queries=0,
                     joint_restarted_checks=0,
                     triangle_equality_checks=0, triangle_equality_queries=0,
                     triangle_equality_incomplete=0, triangle_equality_cache_hits=0,
                     triangle_equality_prunes=0, triangle_equality_merges=0)
    events, records, witness_maps, eliminated = [], [], [], []
    active = set(range(len(vertices)))
    emitted = 0
    if max_table_rows is None:
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

    def install_joint_constraints():
        """Discover original-edge occurrences, then commit complete factors."""
        from four_color_joint_patterns import find_joint_constraints

        def charge_scan():
            check("relation_checks")
            stats["joint_checks"] += 1
            stats["joint_scan_steps"] += 1

        try:
            found = find_joint_constraints(
                g, max_matches=joint_max_matches,
                max_scan_steps=joint_max_scan_steps, charge=charge_scan)
        except _WorkLimit:
            joint_scan.update(complete=False, truncated=True, interrupted=True,
                              scan_steps=stats["joint_scan_steps"])
            raise
        joint_scan.update(found, interrupted=False)
        stats["joint_matches"] = len(found["constraints"])
        for constraint in found["constraints"]:
            scope = tuple(index[v] for v in constraint["frontier"])
            rows = set()
            for row in constraint["rows"]:
                check("relation_checks")
                stats["joint_checks"] += 1
                rows.add(tuple(row))
            if (stats["table_rows"] + stats["cycle_context_rows"]
                    + stats["joint_rows"] + len(rows) > max_table_rows):
                raise _WorkLimit(f"完整關係表已達 {max_table_rows} 列儲存上限；尚未判定。")
            record = dict(
                constraint, name="九點構型三點等色", boundary=constraint["frontier"],
                vertices=constraint["source_vertices"], edges=constraint["source_edges"],
                condition="九個互異原頂點的21條必要原邊全部存在。",
                conclusion=f"同一原九點構型推出 {'、'.join(map(int_text, constraint['frontier']))} 三點同色；共同字面色尚未選定。",
                scope="original-subgraph", relation="equality",
                relation_contract=constraint["contract"])
            factors.append(_Factor(scope, frozenset(rows),
                                   frozenset(tuple(edge) for edge in record["source_edges"]),
                                   frozenset(record["source_vertices"])))
            self_constraints.append(record)
            stats["joint_factors"] += 1
            stats["joint_rows"] += len(rows)
            stats["self_constraints"] = len(self_constraints)
            substructures["self_constraints"] = len(self_constraints)
            stats["peak_scope"] = max(stats["peak_scope"], len(scope))
            stats["peak_rows"] = max(stats["peak_rows"], sum(len(f.rows) for f in factors))
            counts["C1"] += 1
            emit("structural_constraint", "C1", detail=record["conclusion"],
                 relation_kind="joint_constraint", frontier=record["frontier"],
                 rows=record["rows"], relation_rows=len(rows),
                 relation_preview=[dict(boundary=row, colors=[]) for row in record["rows"]],
                 structural_rules=[record], self_constraint=record,
                 causal_edges=record["edges"], causal_vertices=record["vertices"])

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
                        emit("propagate", "C1", detail=f"原邊 {int_text(vertices[u])}–{int_text(vertices[v])}：點 {int_text(vertices[u])} 只剩色 {color + 1}，故另一端排除此色；尚未寫色。",
                             frontier=[vertices[u], vertices[v]],
                             causal_edges=[list(edge) for edge in sorted(domain_edges[v])],
                             causal_vertices=sorted(domain_vertices[v]))
        return True

    def contradiction(factor, detail, vertex=None, **extra):
        stats["conflicts"] += 1
        emit("conflict", vertex=vertex, detail=detail,
             conflict_edges=[list(edge) for edge in sorted(factor.source_edges)],
             frontier=[vertices[v] for v in factor.scope],
             relation_rows=0,
             conflict_shape="empty_joint_relation", **explain(factor), **extra)

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
                    rule["condition"] = f"逐一固定原環首點 {int_text(vertices[cycle[0]])} 的候選色，沿四邊路徑計數，再核對閉合邊。"
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

    def refresh_interface_cache_stats():
        for key, value in intersection_index.delta_stats.items():
            stats[f"propagation_{key}"] = value
        if propagation_method == "delta":
            stats["intersection_cache_hits"] = intersection_index.skipped_pair_queries
        if not use_interface_cache:
            return
        for key, value in intersection_index.cache_stats.items():
            stats[f"interface_cache_{key}"] = value
        stats["intersection_cache_hits"] = intersection_index.skipped_pair_queries

    def propagate_intersections():
        changed = False
        # The index retains live factor identities and completed revision
        # signatures across eliminations; list positions are not cache keys.
        intersection_index.sync(factors, charge=intersection_charge)
        refresh_interface_cache_stats()
        pairs = (intersection_index.pending_pairs() if use_interface_cache or propagation_method == "delta"
                 else intersection_index.pairs())
        for left, right in pairs:
            if not use_interface_cache and propagation_method == "scan" and intersection_index.seen(left, right):
                stats["intersection_cache_hits"] += 1
                continue
            stats["intersection_pairs"] += 1
            if use_interface_cache or propagation_method == "delta":
                answer = intersection_index.intersect(left, right, charge=intersection_charge)
                refresh_interface_cache_stats()
            else:
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
            intersection_index.mark_seen(left, right, support_count=len(answer["common_rows"]))
            refresh_interface_cache_stats()
        refresh_interface_cache_stats()
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

    def propagate_cycle_contexts():
        """Close an original cycle with one common condition, then export interfaces."""
        nonlocal cycle_context_discovery_signature
        from four_color_cycle_propagation import find_original_cycles
        from four_color_cycle_contexts import derive_cycle_context

        def charge_context():
            check("relation_checks")
            stats["cycle_context_checks"] += 1

        def charge_scan():
            charge_context()
            stats["cycle_context_scan_steps"] += 1

        covering_incidence = None

        def add_covering_factor(position, factor):
            charge_context()
            for vertex in factor.scope:
                covering_incidence.setdefault(vertex, set()).add(position)
            stats["interface_cover_index_factors"] += 1

        def covering_factors(scope):
            nonlocal covering_incidence
            if not use_interface_cache:
                return factors
            if covering_incidence is None:
                covering_incidence = {}
                stats["interface_cover_index_builds"] += 1
                for position, factor in enumerate(factors):
                    add_covering_factor(position, factor)
            candidates = None
            for vertex in scope:
                charge_context()
                positions = covering_incidence.get(vertex, set())
                candidates = set(positions) if candidates is None else candidates & positions
                if not candidates:
                    return ()
            return (factors[position] for position in sorted(candidates))

        selected = tuple(sorted(active))
        masks = tuple(sum(1 << color for color in domain) for domain in domains)
        signature = (selected, tuple(masks[v] for v in selected))
        if signature != cycle_context_discovery_signature:
            cycle_context_scan["discoveries"] += 1
            complete, scans = True, []
            try:
                for hub in selected:
                    charge_scan()
                    local_vertices = tuple(sorted(
                        adjacency[hub] & active if cycle_context_search == "neighbours"
                        else active - {hub}))
                    if len(local_vertices) < 3:
                        continue
                    remaining = cycle_context_max_contexts - len(cycle_contexts)
                    if remaining <= 0:
                        complete = False
                        break
                    local_ids = {vertices[v] for v in local_vertices}
                    local_graph = dict(
                        vertices=[vertices[v] for v in local_vertices],
                        edges=[edge for edge in g["edges"]
                               if edge[0] in local_ids and edge[1] in local_ids])
                    found = find_original_cycles(
                        local_graph, tuple(masks[v] for v in local_vertices),
                        max_cycles=remaining, max_scan_steps=cycle_context_max_scan_steps,
                        charge=charge_scan)
                    for literal_cycle in found["cycles"]:
                        cycle = tuple(index[v] for v in literal_cycle)
                        cycle_contexts.setdefault((hub, cycle), tuple(literal_cycle))
                    complete = complete and found["complete"]
                    scans.append(dict(context_vertex=vertices[hub],
                                      cycles=len(found["cycles"]),
                                      scan_steps=found["scan_steps"],
                                      complete=found["complete"],
                                      truncated=found["truncated"]))
            except _WorkLimit:
                cycle_context_scan.update(truncated=True, last_discovery_complete=False,
                                          last_discovery_interrupted=True,
                                          scan_steps=stats["cycle_context_scan_steps"])
                raise
            cycle_context_discovery_signature = signature
            cycle_context_scan.update(
                contexts=[dict(context_vertex=vertices[hub], cycle=list(cycle))
                          for (hub, _), cycle in cycle_contexts.items()],
                scan_steps=stats["cycle_context_scan_steps"],
                truncated=cycle_context_scan["truncated"] or not complete,
                last_discovery_complete=complete, last_discovery_interrupted=False,
                last_discovery=scans)

        changed = False
        for (hub, cycle), literal_cycle in cycle_contexts.items():
            scope = (hub, *cycle)
            if any(v not in active for v in scope):
                stats["cycle_context_inactive_skips"] += 1
                continue
            current_masks = tuple(sum(1 << color for color in domain) for domain in domains)
            local_signature = tuple(current_masks[v] for v in scope)
            if cycle_context_last_domains.get((hub, cycle)) == local_signature:
                stats["cycle_context_skips"] += 1
                continue
            stats["cycle_context_queries"] += 1
            answer = derive_cycle_context(
                g, literal_cycle, vertices[hub], current_masks, charge=charge_context)
            try:
                count_decimal = str(answer["row_count"])
                cases = [dict(case, row_count_decimal=str(case["row_count"]))
                         for case in answer["cases"]]
            except ValueError as error:
                raise _WorkLimit("條件原環的精確計數超出十進位記錄上限；尚未判定。") from error

            source_edges = {tuple(sorted(edge)) for edge in
                            answer["cycle_edges"] + answer["context_edges"]}
            source_edges.update(edge for v in scope for edge in domain_edges[v])
            source_vertices = {vertices[v] for v in scope}
            source_vertices.update(vertex for v in scope for vertex in domain_vertices[v])
            supported_masks = (answer["context_support_mask"], *answer["cycle_supports"])
            narrowed = [{color for color in domains[v] if mask & (1 << color)}
                        for v, mask in zip(scope, supported_masks)]

            # Stage every interface update and storage/budget check before changing
            # any domains or factors.  Interrupted queries are not partial cases.
            plans, added_rows, removed_rows, redundant = [], 0, 0, 0
            planned_domains = dict(zip(scope, narrowed))
            if answer["row_count"]:
                for pair in (answer["pair_relations"] + answer["cycle_edge_relations"]
                             + answer["context_edge_relations"]):
                    pair_scope = tuple(index[v] for v in pair["scope"])
                    previous = context_interface_factors.get(pair_scope)
                    kept = set()
                    for row in pair["rows"]:
                        charge_context()
                        row = tuple(row)
                        if previous is None or row in previous.rows:
                            kept.add(row)
                    rows = frozenset(kept)
                    if previous is None:
                        # Do not add a new interface already implied by one
                        # live factor after the staged unary restrictions.
                        # The witness factor, not another staged interface,
                        # supplies this implication; exact later elimination
                        # preserves it even when that object disappears.
                        implied = False
                        for factor in covering_factors(pair_scope):
                            charge_context()
                            if not set(pair_scope).issubset(factor.scope):
                                continue
                            offsets = tuple(factor.scope.index(v) for v in pair_scope)
                            implied = True
                            for row in sorted(factor.rows):
                                charge_context()
                                if any(color not in planned_domains.get(v, domains[v])
                                       for v, color in zip(factor.scope, row)):
                                    continue
                                if tuple(row[offset] for offset in offsets) not in rows:
                                    implied = False
                                    break
                            if implied:
                                break
                        if implied:
                            redundant += 1
                            continue
                        added_rows += len(rows)
                    else:
                        removed_rows += len(previous.rows) - len(rows)
                    plans.append((pair_scope, previous, rows))
                if stats["table_rows"] + stats["cycle_context_rows"] + stats["joint_rows"] + added_rows > max_table_rows:
                    raise _WorkLimit(f"完整關係表已達 {max_table_rows} 列儲存上限；尚未判定。")
                if covering_incidence is not None:
                    # Charge every planned index insertion before any domain
                    # or factor update; an interrupted query stays atomic.
                    for _, previous, _ in plans:
                        if previous is None:
                            charge_context()

            removed = sum(len(domains[v]) - len(domain)
                          for v, domain in zip(scope, narrowed))
            for v, domain in zip(scope, narrowed):
                if domain != domains[v]:
                    domain_edges[v].update(source_edges)
                    domain_vertices[v].update(source_vertices)
                    domains[v] = domain
            new_factors = 0
            for pair_scope, previous, rows in plans:
                if previous is None:
                    factor = _Factor(pair_scope, rows, frozenset(source_edges),
                                     frozenset(source_vertices))
                    factors.append(factor)
                    if covering_incidence is not None:
                        for vertex in factor.scope:
                            covering_incidence.setdefault(vertex, set()).add(len(factors) - 1)
                        stats["interface_cover_index_factors"] += 1
                    context_interface_factors[pair_scope] = factor
                    new_factors += 1
                elif rows != previous.rows:
                    previous.rows = rows
                    previous.revision += 1
                    previous.source_edges = previous.source_edges | frozenset(source_edges)
                    previous.source_vertices = previous.source_vertices | frozenset(source_vertices)
            cycle_context_last_domains[(hub, cycle)] = tuple(supported_masks)
            stats["cycle_context_prunes"] += removed
            stats["prunes"] += removed
            stats["cycle_context_row_prunes"] += removed_rows
            stats["row_prunes"] += removed_rows
            stats["cycle_context_rows"] += added_rows
            stats["cycle_context_factors"] += new_factors
            stats["cycle_context_redundant_interfaces"] += redundant
            stats["peak_rows"] = max(stats["peak_rows"], sum(len(f.rows) for f in factors))
            changed = changed or bool(removed or removed_rows or new_factors)
            fields = dict(
                relation_kind="cycle_context", context_vertex=vertices[hub],
                cycle_vertices=list(literal_cycle), cycle_length=len(cycle),
                frontier=[vertices[v] for v in scope], relation_rows=answer["row_count"],
                relation_rows_decimal=count_decimal, domain_masks=list(local_signature),
                supported_domain_masks=list(supported_masks), context_cases=cases,
                pair_relations=answer["pair_relations"],
                cycle_edge_relations=answer["cycle_edge_relations"],
                context_edge_relations=answer["context_edge_relations"],
                context_factors_added=new_factors,
                context_rows_added=added_rows, context_rows_removed=removed_rows,
                context_interfaces_redundant=redundant,
                causal_edges=[list(edge) for edge in sorted(source_edges)],
                causal_vertices=sorted(source_vertices), cycle_method=answer["method"],
                cycle_contract=answer["relation_contract"])
            counts["C1"] += 1
            if not answer["row_count"]:
                stats["cycle_context_conflicts"] += 1
                stats["conflicts"] += 1
                emit("conflict", "C1",
                     detail=f"保留共同點 {int_text(vertices[hub])} 的每個候選色後，原 {len(cycle)} 點環皆無法閉合；完整局部關係為空，尚未寫色。",
                     conflict_shape="empty_cycle_context",
                     conflict_edges=[list(edge) for edge in sorted(source_edges)], **fields)
                return False, changed
            emit("cycle_context", "C1",
                 detail=f"共同點 {int_text(vertices[hub])} 與原 {len(cycle)} 點環保留 {count_decimal} 個完整局部色組；導出 {len(plans)} 份完整二／三元接口投影，交回接口交集，尚未寫色。",
                 **fields)
        return True, changed

    def propagate_triangle_equalities():
        """Close small three-colour rules on temporary equality classes."""
        nonlocal triangle_equality_signature
        from four_color_triangle_equalities import derive_triangle_equalities

        remaining = joint_consistency_max_checks - stats["joint_consistency_checks"]
        if remaining <= 0:
            return True, False
        ordered = tuple(sorted(active))
        signature = (ordered, tuple(tuple(sorted(domains[v])) for v in ordered))
        if signature == triangle_equality_signature:
            stats["triangle_equality_cache_hits"] += 1
            return True, False
        literal_vertices = [vertices[v] for v in ordered]
        literal_set = set(literal_vertices)
        literal_edges = [edge for edge in g["edges"] if all(v in literal_set for v in edge)]

        def charge():
            check("relation_checks")
            stats["joint_consistency_checks"] += 1
            stats["triangle_equality_checks"] += 1

        stats["triangle_equality_queries"] += 1
        answer = derive_triangle_equalities(
            literal_vertices, literal_edges, {vertices[v]: domains[v] for v in ordered},
            max_checks=remaining, charge=charge)
        triangle_equality_signature = signature
        if not answer["complete"]:
            stats["triangle_equality_incomplete"] += 1
            stats["joint_consistency_incomplete"] += 1
            return True, False
        merges = sum(step["kind"] == "three_color_double_triangle"
                     for step in answer["proof_steps"])
        stats["triangle_equality_merges"] += merges
        if not answer["proof_steps"] and answer["consistent"]:
            return True, False
        source_edges = frozenset(
            {tuple(sorted(edge)) for edge in answer["source_edges"]} |
            {edge for v in ordered for edge in domain_edges[v]})
        source_vertices = frozenset(literal_vertices) | frozenset(
            vertex for v in ordered for vertex in domain_vertices[v])
        if not answer["consistent"]:
            counts["C1"] += 1
            contradiction(
                _Factor(ordered, frozenset(), source_edges, source_vertices),
                "三色三角的等色類合併與鄰色排除推出原邊矛盾；未枚舉全圖色組、未寫色。",
                propagation_kind="triangle_equalities", structural_proof=answer["proof_steps"],
                equality_classes=[list(group) for group in answer["classes"]],
                structural_conflict=answer["conflict"], structural_query_checks=answer["checks"])
            return False, False
        prunes = 0
        for v in ordered:
            supported = set(answer["domains"][vertices[v]])
            if supported != domains[v]:
                prunes += len(domains[v]) - len(supported)
                domains[v] = supported
                domain_edges[v].update(source_edges)
                domain_vertices[v].update(source_vertices)
        if prunes:
            stats["prunes"] += prunes
            stats["triangle_equality_prunes"] += prunes
            counts["C1"] += 1
            emit("triangle_equalities", "C1",
                 detail=f"三色三角等色類推理刪去 {prunes} 個候選色；未改原圖、未寫色。",
                 structural_proof=answer["proof_steps"],
                 equality_classes=[list(group) for group in answer["classes"]],
                 structural_query_checks=answer["checks"],
                 causal_vertices=sorted(source_vertices),
                 causal_edges=[list(edge) for edge in sorted(source_edges)])
        return True, bool(prunes)

    def propagate_joint_consistency():
        """Project complete incident-factor joins; never commit partial support."""
        from four_color_joint_consistency import joint_supports

        def charge():
            check("relation_checks")
            stats["joint_consistency_checks"] += 1
            stats["joint_support_checks"] += 1

        for retired in set(joint_consistency_seen) - active:
            del joint_consistency_seen[retired]
        for center in sorted(active):
            remaining = joint_consistency_max_checks - stats["joint_consistency_checks"]
            if remaining <= 0:
                # No future query can use these retained factor identities.
                joint_consistency_seen.clear()
                return True, False
            bucket = tuple(factor for factor in factors if center in factor.scope)
            if len(bucket) < 2:
                continue
            scope = tuple(sorted({v for factor in bucket for v in factor.scope}))

            def signature():
                return (tuple((id(factor), factor.revision) for factor in bucket),
                        tuple(tuple(sorted(domains[v])) for v in scope))

            previous = joint_consistency_seen.get(center)
            if previous is not None and previous[1] == signature():
                # Strong references prevent retired factor ids being reused.
                stats["joint_consistency_cache_hits"] += 1
                continue
            stats["joint_consistency_queries"] += 1
            stats["joint_consistency_peak_scope"] = max(
                stats["joint_consistency_peak_scope"], len(scope))
            answer = joint_supports(
                [(factor.scope, factor.rows) for factor in bucket], domains,
                max_checks=remaining,
                max_support_rows=max_table_rows, charge=charge)
            stats["joint_symmetry_checks"] += answer["symmetry_checks"]
            stats["joint_restarted_checks"] += answer["restarted_checks"]
            stats["joint_normalized_queries"] += answer["symmetry_group_size"] > 1
            joint_consistency_seen[center] = (bucket, signature())
            if not answer["complete"]:
                stats["joint_consistency_incomplete"] += 1
                continue
            source_edges = frozenset(
                {edge for factor in bucket for edge in factor.source_edges} |
                {edge for v in scope for edge in domain_edges[v]})
            source_vertices = frozenset(
                {vertex for factor in bucket for vertex in factor.source_vertices} |
                {vertices[v] for v in scope} |
                {vertex for v in scope for vertex in domain_vertices[v]})
            if not answer["consistent"]:
                counts["C1"] += 1
                contradiction(
                    _Factor(scope, frozenset(), source_edges, source_vertices),
                    f"點 {int_text(vertices[center])} 的相交關係合併後為空；"
                    f"本次共同檢查涵蓋 {len(scope)} 點，未消元、未寫色。",
                    vertices[center], propagation_kind="joint_consistency",
                    joint_scope_size=len(scope), joint_query_checks=answer["checks"])
                return False, False
            row_prunes = color_prunes = 0
            for factor, supported in zip(bucket, answer["rows"]):
                if factor.rows != supported:
                    row_prunes += len(factor.rows) - len(supported)
                    factor.rows = supported
                    factor.revision += 1
                    factor.source_edges = source_edges
                    factor.source_vertices = source_vertices
            for v in scope:
                supported = set(answer["domains"][v])
                if domains[v] != supported:
                    color_prunes += len(domains[v]) - len(supported)
                    domains[v] = supported
                    domain_edges[v].update(source_edges)
                    domain_vertices[v].update(source_vertices)
            # Projection onto every input is idempotent for this completed join.
            joint_consistency_seen[center] = (bucket, signature())
            if row_prunes or color_prunes:
                stats["row_prunes"] += row_prunes
                stats["prunes"] += color_prunes
                stats["joint_consistency_row_prunes"] += row_prunes
                stats["joint_consistency_prunes"] += color_prunes
                counts["C1"] += 1
                emit("joint_consistency", "C1", vertices[center],
                     detail=f"完整合併 {len(scope)} 點的相交關係後，刪去 "
                            f"{row_prunes} 列及 {color_prunes} 個候選色；未消元、未寫色。",
                     frontier=[vertices[v] for v in scope],
                     joint_scope_size=len(scope), joint_query_checks=answer["checks"],
                     relation_rows=answer["support_rows"],
                     causal_vertices=sorted(source_vertices),
                     causal_edges=[list(edge) for edge in sorted(source_edges)])
                return True, True
        return True, False

    def propagate():
        """Domain consistency, plus optional complete shared-tuple filtering."""
        # Keep strong references until retired entries are removed, so a
        # recycled Python id can never match a different factor's cached state.
        live_ids = {id(factor) for factor in factors}
        for identity in set(factor_last_domains) - live_ids:
            del factor_last_domains[identity]
        changed = True
        while changed:
            changed = False
            if not propagate_known():
                return False
            for factor in factors:
                signature = (factor.revision,
                             tuple(tuple(sorted(domains[v])) for v in factor.scope))
                previous = factor_last_domains.get(id(factor))
                if previous is not None and previous[0] is factor and previous[1] == signature:
                    stats["factor_cache_hits"] += 1
                    continue
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
                # Unary support projection is idempotent on this exact table.
                # Cache only after the complete filter and all support updates.
                factor_last_domains[id(factor)] = (
                    factor, (factor.revision,
                             tuple(tuple(sorted(domains[v])) for v in factor.scope)))
            if use_intersections:
                compatible, intersection_changed = propagate_intersections()
                if not compatible:
                    return False
                changed = changed or intersection_changed
            if c5_cycles:
                compatible, c5_changed = propagate_c5()
                if not compatible:
                    return False
                changed = changed or c5_changed
            if use_joint_consistency:
                if changed:
                    continue
                compatible, equality_changed = propagate_triangle_equalities()
                if not compatible:
                    return False
                if equality_changed:
                    changed = True
                    continue
            if use_cycles:
                # First settle the ordinary factors and whole-interface
                # intersections, so their new domains guide cycle discovery.
                if changed:
                    continue
                compatible, cycle_changed = propagate_cycles()
                if not compatible:
                    return False
                changed = changed or cycle_changed
            if use_cycle_contexts:
                if changed:
                    continue
                compatible, context_changed = propagate_cycle_contexts()
                if not compatible:
                    return False
                if context_changed:
                    # The next indexed sync discovers new pairs while keeping
                    # completed signatures of unchanged, surviving factors.
                    changed = True
            if use_joint_consistency:
                if changed:
                    continue
                compatible, joint_changed = propagate_joint_consistency()
                if not compatible:
                    return False
                changed = changed or joint_changed
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

        if scheduler is not None:
            return scheduler.select(primal, {v: priority(v) for v in active}, factors, domains)
        candidates = active
        if partition_strategy != "none":
            first = min(group_rank[vertices[v]] for v in active)
            candidates = (v for v in active if group_rank[vertices[v]] == first)
        return min(candidates, key=priority)

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
        if use_joint_constraints:
            install_joint_constraints()
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
            # Every satisfying bucket assignment restricts to exactly one row
            # of any chosen input factor.  Start with the sparsest complete
            # factor and enumerate only its uncovered frontier coordinates.
            # This is the same full join, without testing assignments already
            # excluded by that factor.  No live vertex is assigned a colour.
            anchor = min(bucket, key=lambda factor: len(factor.rows) * prod(
                len(domains[w]) for w in frontier if w not in factor.scope)) if bucket else None
            prepared = [(factor, tuple(-1 if w == v else offsets[w] for w in factor.scope))
                        for factor in bucket if factor is not anchor]

            def bucket_candidates():
                if anchor is None:
                    for boundary in product(*(sorted(domains[w]) for w in frontier)):
                        for color in sorted(domains[v]):
                            check("candidate_checks")
                            yield boundary, color
                    return
                free = tuple(w for w in frontier if w not in anchor.scope)
                if bucket_method == "anchor":
                    anchor_offsets = {w: offset for offset, w in enumerate(anchor.scope)}
                    for row in sorted(anchor.rows):
                        check("relation_checks")
                        if any(color not in domains[w] for w, color in zip(anchor.scope, row)):
                            continue
                        for extension in product(*(sorted(domains[w]) for w in free)):
                            check("candidate_checks")
                            assignment = dict(zip(free, extension))
                            assignment.update(zip(anchor.scope, row))
                            yield tuple(assignment[w] for w in frontier), row[anchor_offsets[v]]
                    return

                # A factor becomes decidable when its last free coordinate is
                # present.  A failed complete tuple rejects every extension of
                # that prefix; accepted prefixes still visit every later colour.
                free_positions = {w: depth + 1 for depth, w in enumerate(free)}
                ready = [[] for _ in range(len(free) + 1)]
                for factor, _ in prepared:
                    depth = max((free_positions.get(w, 0) for w in factor.scope), default=0)
                    ready[depth].append(factor)
                values = [tuple(sorted(domains[w])) for w in free]

                def accepted(depth, assignment):
                    for factor in ready[depth]:
                        check("relation_checks")
                        if tuple(assignment[w] for w in factor.scope) not in factor.rows:
                            return False
                    return True

                for row in sorted(anchor.rows):
                    check("relation_checks")
                    if any(color not in domains[w] for w, color in zip(anchor.scope, row)):
                        continue
                    assignment = dict(zip(anchor.scope, row))
                    if not accepted(0, assignment):
                        continue
                    if not free:
                        check("candidate_checks")
                        yield tuple(assignment[w] for w in frontier), assignment[v]
                        continue
                    # Iterative depth-first extension has no recursion limit.
                    choices = [0] * len(free)
                    depth = 0
                    while depth >= 0:
                        if choices[depth] == len(values[depth]):
                            choices[depth] = 0
                            assignment.pop(free[depth], None)
                            depth -= 1
                            continue
                        color = values[depth][choices[depth]]
                        choices[depth] += 1
                        check("candidate_checks")
                        assignment[free[depth]] = color
                        if not accepted(depth + 1, assignment):
                            continue
                        if depth + 1 == len(free):
                            yield tuple(assignment[w] for w in frontier), assignment[v]
                        else:
                            depth += 1

            table = {}
            for boundary, color in bucket_candidates():
                valid = True
                if bucket_method == "anchor":
                    for factor, positions in prepared:
                        check("relation_checks")
                        row = tuple(color if offset == -1 else boundary[offset] for offset in positions)
                        if row not in factor.rows:
                            valid = False
                            break
                if valid:
                    if boundary in table:
                        table[boundary] |= 1 << color
                        continue
                    if stats["table_rows"] + stats["cycle_context_rows"] + stats["joint_rows"] >= max_table_rows:
                        raise _WorkLimit(f"完整關係表已達 {max_table_rows} 列儲存上限；尚未判定。")
                    table[boundary] = 1 << color
                    stats["table_rows"] += 1
            # All four possible colours fit in one integer, just as a single
            # chosen witness would, while preserving the complete fibre.
            table = dict(sorted(table.items()))

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
                record["rows"] = [dict(boundary=list(boundary), colors=_fiber_colors(mask))
                                  for boundary, mask in table.items()]
                record["source_domains"] = [dict(vertex=vertices[w], colors=sorted(domains[w]))
                                            for w in union_scope]
                record["input_relations"] = [snapshot_factor(factor) for factor in bucket]
            records.append(record)
            if not table:
                contradiction(projected, f"消去點 {int_text(vertices[v])} 時，沒有任何完整邊界色組可以共同延伸。", vertices[v])
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
            preview = [dict(boundary=list(boundary), colors=_fiber_colors(mask))
                       for boundary, mask in islice(table.items(), 8)] if len(events) < trace_limit else []
            emit("eliminate", "C2", vertices[v],
                 detail=f"消去點 {int_text(vertices[v])}：保存 {len(table)} 個完整邊界色組及其所有可用色；尚未寫色。",
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
                choices = _fiber_colors(table[boundary])
                if colors[v] >= 0:
                    if colors[v] not in choices:
                        raise AssertionError("fixed colour lost during reconstruction")
                    continue
                colors[v] = min(choices)
                stats["writebacks"] += 1
                stats["assignments"] += 1
                counts["C3"] += 1
                emit("writeback", "C3", vertices[v], colors[v],
                     detail=f"完整邊界色組查表成功，將點 {int_text(vertices[v])} 寫為色 {colors[v] + 1}。",
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

    refresh_interface_cache_stats()
    if status == "unsatisfiable":
        emit("end", detail="限制的完整共同關係為空；這份固定色無法延伸。" if g["fixed"] else
             "限制的完整共同關係為空；此圖不存在四色染色。", phase="done")
    cycle_scan["scan_steps"] = stats["cycle_scan_steps"]
    cycle_context_scan["scan_steps"] = stats["cycle_context_scan_steps"]
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
        use_interface_cache=use_interface_cache, interface_cache_max_rows=interface_cache_max_rows,
        use_cycles=use_cycles, cycle_max_cycles=cycle_max_cycles,
        cycle_max_scan_steps=cycle_max_scan_steps, cycle_scan=cycle_scan,
        use_cycle_contexts=use_cycle_contexts,
        cycle_context_max_contexts=cycle_context_max_contexts,
        cycle_context_max_scan_steps=cycle_context_max_scan_steps,
        cycle_context_search=cycle_context_search,
        cycle_context_scan=cycle_context_scan,
        use_joint_constraints=use_joint_constraints, joint_max_matches=joint_max_matches,
        use_joint_consistency=use_joint_consistency,
        joint_consistency_max_checks=joint_consistency_max_checks,
        joint_max_scan_steps=joint_max_scan_steps, joint_scan=joint_scan,
        conflict_catalogue=conflict_catalogue(include_rows=False),
        conflict_subgraphs=conflict_subgraphs,
        self_constraints=self_constraints,
        conflict_scan_steps=conflict_index.last_scan_steps if conflict_index else 0,
        conflict_scan_truncated=conflict_index.last_scan_truncated if conflict_index else False,
        conflict_scan_coverage="bounded sufficient motifs; no completeness claim",
        record_relations=record_relations, max_checks=max_checks, max_table_rows=max_table_rows,
        bucket_method=bucket_method,
        propagation_method=propagation_method,
        partition_plan=plan,
        substructures=substructures, elimination_records=records,
        relation_contract="exact allowed rows of the join of input_relations under source_domains; absent boundary tuples have empty fibres; source_edges alone are provenance",
    )
