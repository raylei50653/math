"""Exact four-colour constraints: propagate, eliminate, then write back.

No unknown vertex receives a colour during reduction.  Eliminating a variable
stores the *complete joint* frontier relation, including every possible colour
of the eliminated variable for each allowed frontier tuple.  Reverse lookup is
therefore witness reconstruction, not a search over guessed assignments.

``checks`` counts candidate attempts plus relation-row filtering/membership
tests.  ``max_checks`` bounds that sum; a separate 100,000-row safety ceiling
bounds cumulative generated tables and optional certificate snapshots.  Neither
limit means unsatisfiable.  Graph bookkeeping and final witness verification
are not charged as relation checks.  General variable elimination remains
exponential in frontier width.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, islice, permutations, product


CONSTRAINT_RULES = [
    {"id": "C1", "name": "子構造限制傳播", "description": "過濾完整關係表，刪除沒有共同支援的候選色；只縮限，不填色。"},
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
    return {
        "version": "literal-four-colour-cliques-v1",
        "palette": list(range(4)),
        "templates": [
            {"name": name, "scope": list(range(size)),
             "edges": [list(edge) for edge in combinations(range(size), 2)],
             "rows": [list(row) for row in sorted(rows)]}
            for name, size, rows in (("edge", 2, EDGE_ROWS),
                                     ("triangle", 3, TRIANGLE_ROWS),
                                     ("k4", 4, K4_ROWS))
        ],
        "template_hits_definition": "Each initial factor instance reuses one immutable literal-colour template; these are not cached graph solutions.",
    }


@dataclass
class _Factor:
    scope: tuple
    rows: frozenset
    source_edges: frozenset
    source_vertices: frozenset


class _WorkLimit(Exception):
    pass


def solve_constraints(graph, use_substructures=True, max_checks=1000000,
                      trace_limit=5000, record_relations=True):
    """Solve exactly, or return ``limit`` without asserting nonexistence.

    Recorded rows equal the join of ``input_relations`` under the explicitly
    recorded ``source_domains``.  ``source_edges`` describe original provenance;
    outside GAC context can narrow a bucket, so they alone do not specify its
    complete relation.  With ``record_relations=False``, compact record metadata
    is returned while complete witness maps remain internal for reconstruction.
    """
    from four_color_lab import graph_fingerprint, normalize_graph, verify_coloring

    g = normalize_graph(graph)
    if type(use_substructures) is not bool or type(record_relations) is not bool:
        raise ValueError("use_substructures and record_relations must be booleans")
    if any(type(value) is not int or value < 0 for value in (max_checks, trace_limit)):
        raise ValueError("limits must be nonnegative integers")

    vertices = g["vertices"]
    index = {vertex: position for position, vertex in enumerate(vertices)}
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
    substructures = {
        "triangles": len(triangles), "k4": len(k4), "edges": len(g["edges"]),
        "selected_triangles": len(selected_triangles), "selected_k4": len(selected_k4),
        "uncovered_edges": len(uncovered_edges), "template_hits": template_hits,
        "template_hits_definition": "initial factors reusing immutable tables; not cached graph solutions",
        "instances": {
            "triangles": [[vertices[v] for v in clique] for clique in triangles],
            "k4": [[vertices[v] for v in clique] for clique in k4],
            "selected_triangles": [[vertices[v] for v in clique] for clique in selected_triangles],
            "uncovered_edges": [[vertices[v] for v in edge] for edge in uncovered_edges],
        },
    }
    stats = dict(checks=0, candidate_checks=0, relation_checks=0, prunes=0,
                 row_prunes=0, eliminations=0, writebacks=0, conflicts=0,
                 peak_scope=max((len(f.scope) for f in factors), default=0),
                 peak_frontier=0,
                 peak_rows=sum(len(f.rows) for f in factors), table_rows=0,
                 certificate_rows=0, template_hits=template_hits,
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

    def contradiction(factor, detail, vertex=None):
        stats["conflicts"] += 1
        emit("conflict", vertex=vertex, detail=detail,
             conflict_edges=[list(edge) for edge in sorted(factor.source_edges)],
             frontier=[vertices[v] for v in factor.scope],
             relation_rows=0,
             conflict_shape="empty_joint_relation", **explain(factor))

    def propagate():
        """Generalized arc consistency; only domains and factor rows change."""
        changed = True
        while changed:
            changed = False
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

    emit("start", detail="先保留每點可能色，傳播並記錄完整邊界關係；全部消去成功後才反向寫色。")
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
    return dict(
        name=g.get("name", "自訂圖"), description=g.get("description", ""), graph=g,
        engine="constraints", status=status, colors=colors,
        domains=[[colors[i]] if colors[i] >= 0 else sorted(domain)
                 for i, domain in enumerate(domains)],
        events=events, stats=stats, rules=CONSTRAINT_RULES,
        rule_counts=counts, trace_truncated=emitted > len(events), event_count=emitted,
        graph_sha256=graph_fingerprint(g), use_substructures=use_substructures,
        record_relations=record_relations, max_checks=max_checks, max_table_rows=max_table_rows,
        substructures=substructures, elimination_records=records,
        relation_contract="exact allowed rows of the join of input_relations under source_domains; absent boundary tuples have empty fibres; source_edges alone are provenance",
    )
