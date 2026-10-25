"""Known sufficient obstructions, with literal original-subgraph witnesses.

Recognition uses edge structure and domain guards.  Exported full relations
are independent audit data; they are never consulted by the recognizer.
"""
from __future__ import annotations

from itertools import combinations, permutations, product


VERSION = "literal-four-colour-conflicts-v1"
_SPECS = (
    ("fixed_edge", "原邊同色", 2, "原邊兩端都只剩同一色。"),
    ("four_color_star", "四色阻擋星形", 5, "四個不同原鄰點的唯一色覆蓋四色。"),
    ("triangle_two_colors", "三角形兩色矛盾", 3, "原三角形的候選色聯集至多兩色。"),
    ("c5_two_colors", "五環兩色奇偶矛盾", 5, "原五環的候選色聯集至多兩色。"),
    ("k5", "原 K5", 5, "五個不同原頂點的十條原邊全部存在。"),
)


def conflict_catalogue(include_rows=True):
    """Return fresh audit data, including empty fibres, in one literal frame."""
    templates = []
    for identifier, name, size, condition in _SPECS:
        edges = ([(0, v) for v in range(1, 5)] if identifier == "four_color_star"
                 else [(i, (i + 1) % 5) for i in range(5)] if identifier == "c5_two_colors"
                 else list(combinations(range(size), 2)))
        item = dict(id=identifier, name=name, scope=list(range(size)),
                    edges=[list(edge) for edge in edges], condition=condition,
                    evidence="original edges plus current literal domains")
        if identifier == "four_color_star":
            item.update(center=0, boundary=[1, 2, 3, 4])
            if include_rows:
                item["rows"] = [dict(boundary=list(row), colors=sorted(set(range(4)) - set(row)))
                                for row in product(range(4), repeat=4) if len(set(row)) < 4]
                item["forbidden_rows"] = [list(row) for row in permutations(range(4))]
        elif include_rows:
            item["rows"] = [list(row) for row in product(range(4), repeat=size)
                            if all(row[a] != row[b] for a, b in edges)]
        templates.append(item)
    hub_constraint = dict(id="c5_hub_equality", name="五環雙中心等色",
                          scope=list(range(7)), boundary=[5, 6],
                          edges=[[i, (i + 1) % 5] for i in range(5)] +
                                [[i, hub] for i in range(5) for hub in (5, 6)],
                          condition="兩中心都鄰接同一奇五環的全部五點。",
                          conclusion="異色中心會把五環限制為兩色，故中心必須同色。")
    if include_rows:
        hub_constraint["rows"] = [[color, color] for color in range(4)]
    return dict(version=VERSION, palette=list(range(4)), templates=templates,
                self_constraints=[hub_constraint],
                empty_fibres="four_color_star.forbidden_rows lists all 24 empty leaf fibres",
                runtime="structural guards; exported rows are audit data only")


class KnownConflictIndex:
    """Reuse original adjacency; bound optional cycle discovery separately."""

    def __init__(self, vertices, edges, max_scan_steps=20000):
        self.vertices = list(vertices)
        self.positions = {v: i for i, v in enumerate(vertices)}
        self.edges = sorted({tuple(sorted(edge)) for edge in edges},
                            key=lambda edge: tuple(self.positions[v] for v in edge))
        self.adjacency = {v: set() for v in vertices}
        for a, b in self.edges:
            self.adjacency[a].add(b)
            self.adjacency[b].add(a)
        self.max_scan_steps = max_scan_steps
        self.last_scan_steps = 0
        self.last_scan_truncated = False
        self._k5_checked = False
        self._k5 = None

    def find(self, domains, fixed=(), scope="current-domains", charge=None):
        if len(domains) != len(self.vertices):
            raise ValueError("domains must align with ordered vertices")
        domain = {v: set(values) for v, values in zip(self.vertices, domains)}
        if any(any(type(c) is not int or c not in range(4) for c in values)
               for values in domain.values()):
            raise ValueError("domain colours must be integers 0..3")
        self.last_scan_steps = 0
        self.last_scan_truncated = False

        def tick():
            if charge is not None:
                charge()

        def ordered(values):
            return sorted(values, key=self.positions.__getitem__)

        def certificate(identifier, selected, edges, **extra):
            _, name, _, condition = next(spec for spec in _SPECS if spec[0] == identifier)
            return dict(id=identifier, template_id=identifier, name=name,
                        vertices=list(selected), edges=[list(edge) for edge in edges],
                        domains=[dict(vertex=v, colors=sorted(domain[v])) for v in selected],
                        fixed=[list(pair) for pair in fixed], condition=condition,
                        scope=scope, empty_relation=True, relation_rows=0,
                        role_mapping=list(selected), **extra)

        for a, b in self.edges:
            tick()
            if len(domain[a]) == 1 and domain[a] == domain[b]:
                return certificate("fixed_edge", [a, b], [(a, b)])
        for center in self.vertices:
            if len(self.adjacency[center]) < 4:
                continue
            by_color = {}
            for neighbor in ordered(self.adjacency[center]):
                tick()
                if len(domain[neighbor]) == 1:
                    by_color.setdefault(next(iter(domain[neighbor])), neighbor)
            if len(by_color) == 4:
                leaves = [by_color[c] for c in range(4)]
                return certificate("four_color_star", [center, *leaves],
                                   [(center, leaf) for leaf in leaves], center=center)
        for a in self.vertices:
            for b in ordered(v for v in self.adjacency[a]
                             if self.positions[v] > self.positions[a]):
                for c in ordered(v for v in self.adjacency[a] & self.adjacency[b]
                                 if self.positions[v] > self.positions[b]):
                    tick()
                    if all(domain[v] for v in (a, b, c)) and len(domain[a] | domain[b] | domain[c]) <= 2:
                        return certificate("triangle_two_colors", [a, b, c],
                                           [(a, b), (b, c), (c, a)])

        # A two-colour odd cycle is impossible by alternation.  Only vertices
        # whose actual domains fit one common pair take part in this search.
        try:
            for pair in combinations(range(4), 2):
                eligible = {v for v in self.vertices if domain[v] and domain[v] <= set(pair)}
                if len(eligible) < 5:
                    continue
                for start in ordered(eligible):
                    def visit(path):
                        last = path[-1]
                        if len(path) == 5:
                            if start in self.adjacency[last]:
                                return path
                            return None
                        for neighbor in ordered(self.adjacency[last] & eligible):
                            if self.last_scan_steps >= self.max_scan_steps:
                                raise StopIteration
                            tick()
                            self.last_scan_steps += 1
                            if neighbor in path or self.positions[neighbor] <= self.positions[start]:
                                continue
                            result = visit(path + [neighbor])
                            if result is not None:
                                return result
                        return None
                    selected = visit([start])
                    if selected is not None:
                        return certificate("c5_two_colors", selected,
                                           [(selected[i], selected[(i + 1) % 5]) for i in range(5)],
                                           palette=list(pair))
        except StopIteration:
            self.last_scan_truncated = True

        # This structural obstruction does not depend on changing domains.
        if not self._k5_checked:
            def clique(prefix, candidates):
                if len(prefix) == 5:
                    return prefix
                if len(prefix) + len(candidates) < 5:
                    return None
                for offset, v in enumerate(candidates):
                    tick()
                    result = clique(prefix + [v], [w for w in candidates[offset + 1:]
                                                   if w in self.adjacency[v]])
                    if result is not None:
                        return result
                return None
            self._k5 = clique([], self.vertices)
            self._k5_checked = True
        if self._k5 is not None:
            return certificate("k5", self._k5, list(combinations(self._k5, 2)))
        return None


def find_known_conflict(vertices, edges, domains, fixed=(), scope="current-domains",
                        charge=None, max_scan_steps=20000):
    if type(max_scan_steps) is not int or max_scan_steps < 0:
        raise ValueError("max_scan_steps must be a nonnegative integer")
    return KnownConflictIndex(vertices, edges, max_scan_steps).find(
        domains, fixed=fixed, scope=scope, charge=charge)
