#!/usr/bin/env python3
"""Small, exact pp formulas over four colours; geometry is separate evidence.

python scripts/pp_relations.py examples
python scripts/pp_relations.py eval artifacts/pp_relations/r767_pair.json

Syntax is prenex existential conjunction, with explicit disjoint free/bound
names. Atom arguments may repeat. No arbitrary Python guards, negation,
disjunction, implicit variable capture, or graph-layout inference.
"""
import argparse
from dataclasses import dataclass
import hashlib
from itertools import product
import json
from pathlib import Path

from boundary_relations import Relation, normalize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/pp_relations'
SCHEMA = 'four-colour-pp-v1'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Atom:
    symbol: str
    args: tuple[str, ...]


@dataclass(frozen=True)
class Formula:
    free: tuple[str, ...]
    exists: tuple[str, ...]
    atoms: tuple[Atom, ...]

    def __post_init__(self):
        names = self.free + self.exists
        if any(not isinstance(v, str) or not v for v in names):
            raise ValueError('Variable names must be nonempty strings')
        if len(set(names)) != len(names):
            raise ValueError('Free and existential names must be distinct and disjoint')
        for atom in self.atoms:
            if not isinstance(atom, Atom) or not isinstance(atom.symbol, str):
                raise ValueError('Expected a named relation atom')
            if any(not isinstance(v, str) or v not in names for v in atom.args):
                raise ValueError('Every atom argument must be explicitly declared')

    def as_dict(self):
        return dict(schema=SCHEMA, free=list(self.free), exists=list(self.exists),
                    atoms=[dict(symbol=a.symbol, args=list(a.args)) for a in self.atoms])

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or set(data) != {'schema', 'free', 'exists', 'atoms'}:
            raise ValueError('Expected only schema/free/exists/atoms')
        if data['schema'] != SCHEMA or any(type(data[k]) is not list for k in ('free', 'exists', 'atoms')):
            raise ValueError('Invalid pp schema or variable/atom lists')
        atoms = []
        for a in data['atoms']:
            if not isinstance(a, dict) or set(a) != {'symbol', 'args'} or type(a['args']) is not list:
                raise ValueError('Expected only symbol/args in each atom')
            atoms.append(Atom(a['symbol'], tuple(a['args'])))
        return cls(tuple(data['free']), tuple(data['exists']), tuple(atoms))


@dataclass(frozen=True)
class Symbol:
    relation: Relation
    evidence: dict


def load_language(root=ROOT):
    """Read existing witnessed relations, checking recorded source byte hashes.

    Evidence is a reference to prior validation, not a fresh graph/Lean check.
    EQ is logical equality, not a claim of a cofacial equality wire.
    """
    catalog_path = root / 'artifacts/boundary_relations/library.json'
    catalog = json.loads(catalog_path.read_text())
    fan = root / 'artifacts/fan_pentagon'
    if set(catalog['source_sha256']) != {'states.json', 'summary.json', 'replay.json'}:
        raise ValueError('Unexpected catalog source set')
    for name, expected in catalog['source_sha256'].items():
        if digest(fan / name) != expected:
            raise ValueError(f'Stale catalog source: {name}')
    states = json.loads((fan / 'states.json').read_text())
    rows = {r['sigma_bits']: r for r in states['states']}
    ports = tuple(f'b{i}' for i in range(5))
    order = [tuple(p) for p in states['pattern_order']]
    language = {
        'EQ': Symbol(Relation.of(('x', 'y'), [(0, 0)]),
                     dict(kind='logical equality', geometry='no physical wire asserted')),
        'NEQ': Symbol(Relation.of(('x', 'y'), [(0, 1)]),
                      dict(kind='edge relation', geometry='no composed layout asserted')),
    }
    if len(catalog['entries']) != len(rows) or len({e['id'] for e in catalog['entries']}) != len(rows):
        raise ValueError('Duplicate or missing catalog entries')
    for entry in catalog['entries']:
        bits, raw = entry['id'], entry['relation']
        row = rows.get(bits)
        expected = [p for i, p in enumerate(order) if bits >> i & 1]
        if (row is None or tuple(raw['ports']) != ports or
                list(map(tuple, raw['patterns'])) != expected or
                entry['realization']['mask'] != row['mask'] or
                entry['realization']['source'] != 'artifacts/fan_pentagon/states.json'):
            raise ValueError(f'Catalog/witness mismatch: R{bits}')
        language[f'R{bits}'] = Symbol(
            Relation(ports, frozenset(expected)),
            dict(kind='catalog reference; not reverified geometry',
                 catalog='artifacts/boundary_relations/library.json',
                 catalog_sha256=digest(catalog_path), entry_id=bits,
                 source_sha256=catalog['source_sha256']['states.json'],
                 realization=entry['realization']))
    return language


def evaluate(formula, language, *, max_variables=10):
    """Enumerate globally normalized assignments, then existentially project.

    Every language relation denotes full S4 orbits. Each output row retains a
    satisfying assignment of ALL formula variables (not internal gadget nodes).
    The explicit size cap raises an error; evaluation is never partial.
    """
    names = formula.free + formula.exists
    if len(names) > max_variables:
        raise ValueError(f'Exact evaluator limited to {max_variables} variables')
    indexed = []
    for atom in formula.atoms:
        if atom.symbol not in language:
            raise ValueError(f'Unknown relation symbol: {atom.symbol}')
        rel = language[atom.symbol].relation
        if len(atom.args) != len(rel.ports):
            raise ValueError(f'Arity mismatch for {atom.symbol}')
        indexed.append((tuple(names.index(v) for v in atom.args), rel.patterns))
    witnesses = {}
    for values in product(range(4), repeat=len(names)):
        if normalize(values) != values:
            continue
        if all(normalize(tuple(values[i] for i in indices)) in patterns for indices, patterns in indexed):
            boundary = values[:len(formula.free)]
            witnesses.setdefault(boundary, dict(zip(names, values)))
    result = Relation(formula.free, frozenset(witnesses))
    return dict(formula=formula.as_dict(), relation=result.as_dict(),
                feasible=bool(result.patterns),
                witnesses=[dict(pattern=p, assignment=witnesses[p]) for p in sorted(witnesses)],
                atoms=[dict(index=i, symbol=a.symbol, args=a.args,
                            evidence=language[a.symbol].evidence) for i, a in enumerate(formula.atoms)],
                geometry='unchecked: atom evidence does not certify this composition',
                trust='computationally evaluated; not proved in Lean')


def examples():
    ports = tuple(f'b{i}' for i in range(5))
    guards = (Atom('EQ', ('b1', 'b4')), Atom('NEQ', ('b0', 'b2')))
    guarded = (Atom('R767', ports),) + guards
    return {
        'r767_guard': Formula(ports, (), guarded),
        'r1023_guard': Formula(ports, (), (Atom('R1023', ports),) + guards),
        'r767_pair': Formula(('b0', 'b3'), ('b1', 'b2', 'b4'), guarded),
        'r91_meet_r935': Formula(ports, (), (Atom('R91', ports), Atom('R935', ports))),
        'infeasible': Formula(ports, (), (Atom('R767', ports), Atom('EQ', ('b0', 'b1')))),
    }


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('examples')
    cmd = sub.add_parser('eval')
    cmd.add_argument('formula', type=Path)
    cmd.add_argument('--pair', nargs=2, metavar=('LEFT', 'RIGHT'))
    args = parser.parse_args()
    try:
        language = load_language()
        if args.command == 'examples':
            for name, formula in examples().items():
                write_json(OUT / f'{name}.json', formula.as_dict())
                write_json(OUT / f'{name}.result.json', evaluate(formula, language))
            print(f'Wrote {len(examples())} formulas and results to {OUT}')
        else:
            result = evaluate(Formula.from_dict(json.loads(args.formula.read_text())), language)
            if args.pair:
                row = result['relation']
                result['pair_query'] = Relation.of(row['ports'], row['patterns']).query(*args.pair)
            print(json.dumps(result, indent=2, sort_keys=True))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
