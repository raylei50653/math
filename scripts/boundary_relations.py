#!/usr/bin/env python3
"""Exact colour relations on named ports, with nonvacuous conditional forcing.

Patterns use ONE global colour renaming, never independent input/output S4.
This module makes no assertion about planar/disk realizability of operations.
"""
from dataclasses import dataclass
from itertools import product
from typing import Iterable


def normalize(pattern):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in pattern)


@dataclass(frozen=True)
class Literal:
    left: str
    right: str
    equal: bool = True

    def text(self):
        return self.left + ('=' if self.equal else '!=') + self.right


@dataclass(frozen=True)
class Relation:
    """Each row denotes its whole global S4 orbit. Port order is significant."""
    ports: tuple[str, ...]
    patterns: frozenset[tuple[int, ...]]

    def __post_init__(self):
        if len(set(self.ports)) != len(self.ports):
            raise ValueError('Ports must have distinct names')
        if any(len(p) != len(self.ports) or normalize(p) != p or
               any(type(c) is not int or not 0 <= c < 4 for c in p) for p in self.patterns):
            raise ValueError('Rows must be globally normalized four-colour assignments')

    @classmethod
    def of(cls, ports, patterns):
        return cls(tuple(ports), frozenset(normalize(p) for p in patterns))

    def condition(self, guards: Iterable[Literal]):
        indexed = [(self.ports.index(g.left), self.ports.index(g.right), g.equal) for g in guards]
        return Relation(self.ports, frozenset(p for p in self.patterns
                                              if all((p[i] == p[j]) == eq for i, j, eq in indexed)))

    def query(self, left, right, guards=()):
        """Infeasible conditions never report either colour as forced."""
        selected = self.condition(guards)
        i, j = self.ports.index(left), self.ports.index(right)
        pair_projection = frozenset(normalize((p[i], p[j])) for p in selected.patterns)
        same = sorted(p for p in selected.patterns if p[i] == p[j])
        different = sorted(p for p in selected.patterns if p[i] != p[j])
        status = ('infeasible' if not pair_projection else 'free' if len(pair_projection) == 2
                  else 'forced_equal' if (0, 0) in pair_projection else 'forced_different')
        return dict(status=status, surviving_orbits=len(selected.patterns),
                    pair_projection=sorted(pair_projection),
                    equal_witness=same[0] if same else None,
                    different_witness=different[0] if different else None)

    def rename(self, names):
        return Relation(tuple(names.get(p, p) for p in self.ports), self.patterns)

    def reorder(self, ports):
        if len(ports) != len(self.ports) or set(ports) != set(self.ports):
            raise ValueError('Reordering must specify each existing port exactly once')
        indices = [self.ports.index(p) for p in ports]
        return Relation.of(ports, (tuple(row[i] for i in indices) for row in self.patterns))

    def meet(self, other):
        """Conjoin restrictions on the SAME named interface."""
        aligned = other.reorder(self.ports)
        return Relation(self.ports, self.patterns & aligned.patterns)

    def project(self, keep):
        """Existentially hide all other ports, after any shared constraints."""
        if len(set(keep)) != len(keep):
            raise ValueError('Projection ports must be distinct')
        indices = [self.ports.index(p) for p in keep]
        return Relation.of(keep, (tuple(row[i] for i in indices) for row in self.patterns))

    def as_dict(self):
        return dict(ports=self.ports, patterns=sorted(self.patterns), geometry='unchecked')


def c5_universe():
    return Relation.of(tuple(f'b{i}' for i in range(5)),
                       (b for b in product(range(4), repeat=5)
                        if all(b[i] != b[(i + 1) % 5] for i in range(5))))


def extra_forcings(relation):
    """All inclusion-minimal live guards forcing a diagonal EQ/NEQ beyond C5.

    Only the five diagonals are variables: the five boundary edges are NEQ
    already. The complete relation remains authoritative, not this view.
    """
    base = c5_universe().reorder(relation.ports)
    diagonals = [(f'b{i}', f'b{j}') for i in range(5) for j in range(i + 1, 5)
                 if (j - i) not in (1, 4)]
    found = []
    for target in diagonals:
        others = [pair for pair in diagonals if pair != target]
        for values in product((None, False, True), repeat=4):
            guards = tuple(Literal(*pair, eq) for pair, eq in zip(others, values) if eq is not None)
            result = relation.query(*target, guards)
            status = result['status']
            if not status.startswith('forced_') or base.query(*target, guards)['status'] == status:
                continue
            if any(relation.query(*target, guards[:i] + guards[i + 1:])['status'] == status
                   for i in range(len(guards))):
                continue
            found.append(dict(given=[g.text() for g in guards],
                              forces=Literal(*target, status == 'forced_equal').text(),
                              witness=next(p for p in (result['equal_witness'], result['different_witness'])
                                           if p is not None),
                              surviving_orbits=result['surviving_orbits']))
    return sorted(found, key=lambda r: (len(r['given']), r['given'], r['forces']))
