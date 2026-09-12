#!/usr/bin/env python3
"""Independent labeled-colouring replay of the small pp-expression layer.

python scripts/pp_relations.py examples
python scripts/check_pp_relations.py

Does not rerun gadget search or assert disk realizability / Lean soundness.
"""
from itertools import combinations, permutations, product
import json

from boundary_relations import Literal, Relation
from pp_relations import (Atom, Formula, OUT, ROOT, Symbol, digest, evaluate,
                          examples, load_language, write_json)


def expand(patterns):
    # Independent of the evaluator's normalization/membership path.
    return {tuple(perm[c] for c in p) for p in patterns for perm in permutations(range(4))}


def replay(formula, language):
    names = formula.free + formula.exists
    tables = {symbol: expand(definition.relation.patterns) for symbol, definition in language.items()}
    full, extensions = set(), set()
    for colours in product(range(4), repeat=len(names)):
        assignment = dict(zip(names, colours))
        if all(tuple(assignment[v] for v in a.args) in tables[a.symbol] for a in formula.atoms):
            full.add(colours[:len(formula.free)])
            extensions.add(colours)
    result = evaluate(formula, language)
    assert expand(result['relation']['patterns']) == full
    assert result['feasible'] == bool(full)
    assert len(result['witnesses']) == len(result['relation']['patterns'])
    for witness in result['witnesses']:
        assignment = witness['assignment']
        assert set(assignment) == set(names)
        assert tuple(assignment[v] for v in names) in extensions
        assert tuple(assignment[v] for v in formula.free) == tuple(witness['pattern'])
    rel = Relation.of(formula.free, result['relation']['patterns'])
    for i, j in combinations(range(len(formula.free)), 2):
        outcomes = {b[i] == b[j] for b in full}
        status = ('infeasible' if not outcomes else 'free' if len(outcomes) == 2
                  else 'forced_equal' if True in outcomes else 'forced_different')
        assert rel.query(formula.free[i], formula.free[j])['status'] == status
    assert result['geometry'].startswith('unchecked:')
    return result, full


def rejects(action):
    try:
        action()
    except ValueError:
        return
    raise AssertionError('Invalid formula was accepted')


def main():
    language = load_language()
    checked = 0
    counts = {}
    for name, formula in examples().items():
        stored = Formula.from_dict(json.loads((OUT / f'{name}.json').read_text()))
        assert stored == formula
        result, full = replay(stored, language)
        assert json.loads((OUT / f'{name}.result.json').read_text()) == json.loads(json.dumps(result))
        counts[name] = len(full)
        checked += 1
    assert counts == dict(r767_guard=24, r1023_guard=48, r767_pair=4,
                          r91_meet_r935=48, infeasible=0)
    guards = [Literal('b1', 'b4'), Literal('b0', 'b2', False)]
    for bits in (767, 1023):
        expected = language[f'R{bits}'].relation.condition(guards)
        actual = evaluate(examples()[f'r{bits}_guard'], language)['relation']
        assert Relation.of(actual['ports'], actual['patterns']) == expected
    expected = language['R91'].relation.meet(language['R935'].relation)
    assert expected.patterns == frozenset({(0, 1, 0, 1, 2), (0, 1, 0, 2, 1)})

    # All catalog atoms, reversed storage order, repeated variables and explicit
    # wiring rotation. This tests ports as labels, not independent S4 quotients.
    ports = tuple(f'b{i}' for i in range(5))
    cases = [Formula(ports, (), (Atom(s, ports),)) for s in language if s.startswith('R')]
    cases += [Formula(tuple(reversed(ports)), (), (Atom('R767', ports),)),
              Formula(ports, (), (Atom('R767', ports[1:] + ports[:1]),)),
              Formula(('x',), (), (Atom('NEQ', ('x', 'x')),)),
              Formula(('x',), (), (Atom('EQ', ('x', 'x')),)),
              Formula((), (), ()), Formula(('x', 'y'), (), ()),
              Formula((), ('x',), (Atom('NEQ', ('x', 'x')),)),
              Formula((), ('x',), (Atom('EQ', ('x', 'x')),)),
              Formula(('x',), ('unused',), ())]
    # A shared existential variable cannot be independently hidden per atom.
    shared = Formula(('x', 'y'), ('z',), (Atom('EQ', ('x', 'z')), Atom('EQ', ('y', 'z'))))
    separate = Formula(('x', 'y'), ('z', 'w'), (Atom('EQ', ('x', 'z')), Atom('EQ', ('y', 'w'))))
    cases += [shared, separate]
    assert len(replay(shared, language)[1]) == 4
    assert len(replay(separate, language)[1]) == 16
    # K5-xy: shared K3 consumes three colours, forcing both free ports equal.
    edges = [('a', 'b'), ('b', 'c'), ('a', 'c')] + [(v, z) for v in ('x', 'y') for z in ('a', 'b', 'c')]
    equality_gadget = Formula(('x', 'y'), ('a', 'b', 'c'), tuple(Atom('NEQ', e) for e in edges))
    cases.append(equality_gadget)
    assert replay(equality_gadget, language)[1] == {(c, c) for c in range(4)}
    # Empty and nonempty nullary relation atoms retain their truth values.
    extra = dict(language, TRUE=Symbol(Relation.of((), [()]), {}),
                 FALSE=Symbol(Relation.of((), []), {}))
    cases += [Formula((), (), (Atom('TRUE', ()),)), Formula(('x',), (), (Atom('FALSE', ()),))]
    for formula in cases:
        assert Formula.from_dict(formula.as_dict()) == formula
        replay(formula, extra)
        checked += 1
    rejects(lambda: Formula(('x',), ('x',), ()))
    rejects(lambda: Formula(('x',), (), (Atom('EQ', ('x', 'z')),)))
    rejects(lambda: evaluate(Formula(('x',), (), (Atom('EQ', ('x',)),)), language))
    rejects(lambda: evaluate(Formula(('x',), (), (Atom('UNKNOWN', ('x',)),)), language))
    rejects(lambda: Formula.from_dict(dict(examples()['r767_guard'].as_dict(), guard='arbitrary predicate')))
    rejects(lambda: evaluate(Formula(('x', 'y'), (), ()), language, max_variables=1))
    rejects(lambda: Formula.from_dict(dict(schema='four-colour-pp-v1', free=['x'], exists=[],
                                         atoms=[dict(symbol='EQ', args=['x', 'x'], negate=True)])))
    paths = [ROOT / 'scripts' / name for name in ('pp_relations.py', 'check_pp_relations.py', 'boundary_relations.py')]
    paths += [ROOT / 'artifacts/boundary_relations/library.json', ROOT / 'artifacts/fan_pentagon/states.json']
    paths += sorted(p for p in OUT.glob('*.json') if p.name != 'replay.json')
    report = dict(status='PASS', trust='computationally observed; independent labeled replay, not Lean proof',
                  formulas_checked=checked, example_labeled_counts=counts, invalid_cases_rejected=7,
                  geometry='not checked; existing atomic witnesses are references only',
                  source_sha256={str(p.relative_to(ROOT)): digest(p) for p in paths})
    write_json(OUT / 'replay.json', report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
