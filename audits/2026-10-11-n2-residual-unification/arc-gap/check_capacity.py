#!/usr/bin/env python3
"""Read-only conditional capacity check on 63 frozen original source records."""
import hashlib
import json
import sys
from pathlib import Path

SOURCE = Path("artifacts/c5_excess_two_arc_component_slack/observations.json")
OUT = Path(__file__).with_name("capacity_controls.json")


def accepts(edges, coordinates, beta):
    adjacency = {v: [] for v in range(5)}
    adjacency.update({v: [] for v in coordinates})
    for x, y in edges:
        adjacency[x].append(y)
        adjacency[y].append(x)
    colors = dict(enumerate(beta))

    def visit(j):
        if j == len(coordinates):
            return True
        v = coordinates[j]
        forbidden = {colors[x] for x in adjacency[v] if x in colors}
        for a in range(4):
            if a not in forbidden:
                colors[v] = a
                if visit(j + 1):
                    return True
        colors.pop(v, None)
        return False

    return visit(0)


raw = SOURCE.read_bytes()
data = json.loads(raw)
pins = [tuple(p) for p in data["pin_order"]]
pin_index = {p: j for j, p in enumerate(pins)}
records = []
counts = dict(original_graphs=63, structural_graphs=0, rejected_rows=0,
              q_minimal_rows=0, orientations=0, column_equalities=0,
              target_sources=0)
for idx, source in enumerate(data["records"]):
    roots, edges, components = source["roots"], source["edges"], source["components"]
    mixed = [c for c in components if min(c["root_incidence"]) > 0]
    unary = [c for c in components if min(c["root_incidence"]) == 0]
    if sorted(roots) in edges or len(mixed) != 2:
        continue
    if any(sum(c["root_incidence"][j] > 0 for c in unary) > 1 for j in (0, 1)):
        continue
    counts["structural_graphs"] += 1
    counts["target_sources"] += source["sigma_mask"] in (933, 941, 940)
    for row in range(10):
        beta = components[0]["rows"][row]["beta"]
        if len(set(beta)) != 3:
            continue
        relations = []
        for c in components:
            cr = c["rows"][row]
            assert cr["beta"] == beta
            relations.append({pins[j] for j, f in enumerate(cr["local_full_fibres_by_pins"]) if f})
        spoke_colors = [{beta[x] for x, b in edges if x < 5 and b == root} |
                        {beta[b] for b, x in edges if b < 5 and x == root}
                        for root in roots]
        allowed = {(a, b) for a, b in pins if a not in spoke_colors[0] and b not in spoke_colors[1]}
        joint = allowed.intersection(*relations)
        assert bool(joint) == accepts(edges, source["interior_coordinates"], beta)
        if joint:
            continue
        counts["rejected_rows"] += 1
        nonframe = [e for e in edges if max(e) >= 5]
        if not all(accepts([x for x in edges if x != e], source["interior_coordinates"], beta)
                   for e in nonframe):
            continue
        counts["q_minimal_rows"] += 1
        entry = dict(source_record_index=idx, sigma_mask=source["sigma_mask"],
                     row_index=row, beta=beta, orientations=[])
        for side in (0, 1):
            m = sum(c["root_incidence"][side] for c in mixed)
            forbidden = []
            deficits = []
            for c, rel in zip(components, relations):
                if c not in unary or not c["root_incidence"][side]:
                    continue
                F = {a for a in range(4) if not any(p[side] == a for p in rel)}
                assert rel == {p for p in pins if p[side] not in F}
                assert F.isdisjoint(spoke_colors[side])
                forbidden.append(F)
                deficits.append(c["root_incidence"][side] - len(F))
            D = sum(deficits)
            E = set(range(4)) - spoke_colors[side] - set().union(*forbidden)
            other_allowed = set(range(4)) - spoke_colors[1-side]
            for c, rel in zip(components, relations):
                if c in unary and c["root_incidence"][1-side]:
                    other_allowed &= {p[1-side] for p in rel}
            assert E and other_allowed and len(E) == m - 1 + D and D in (0, 1)
            assert sum(len(f) for f in forbidden) + len(spoke_colors[side]) == 4-len(E)
            columns = []
            for b in sorted(other_allowed):
                fields = []
                ks = []
                for c, rel in zip(components, relations):
                    if c in mixed:
                        fields.append({a for a in range(4)
                                       if ((a,b) if side == 0 else (b,a)) not in rel})
                        ks.append(c["root_incidence"][side])
                V = set().union(*fields)
                assert E <= V
                delta = sum(k-len(f) for k,f in zip(ks,fields))
                overlap = sum(map(len,fields))-len(V)
                leak = len(V-E)
                assert min(D,delta,overlap,leak) >= 0 and D+delta+overlap+leak == 1
                columns.append(dict(other_pin=b, D=D, delta=delta, o=overlap, lambda_=leak))
                counts["column_equalities"] += 1
            entry["orientations"].append(dict(root=roots[side], m=m, D=D,
                                                E=sorted(E), columns=columns))
            counts["orientations"] += 1
        records.append(entry)
output = dict(input=dict(path=str(SOURCE), sha256=hashlib.sha256(raw).hexdigest()),
              scope="fixed original graphs; complete existing local fibres; independent whole-graph DFS q-minimality",
              counts=counts, records=records,
              target_source_status="not triggered; no target source exclusion evidence")
rendered = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
if "--check" in sys.argv:
    assert OUT.read_text() == rendered, "conditional capacity artifact mismatch"
else:
    with OUT.open("x") as f:
        f.write(rendered)
print(json.dumps(counts, sort_keys=True))
