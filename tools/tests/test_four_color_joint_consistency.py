"""Independent exact-support checks for bounded multi-factor consistency."""
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_joint_consistency import joint_supports
import four_color_constraints as constraints


def enumerate_supports(factors, domains):
    scope = sorted({v for columns, _ in factors for v in columns})
    supports = [set() for _ in factors]
    values = {v: set() for v in scope}
    count = 0
    for row in product(*(sorted(domains[v]) for v in scope)):
        assignment = dict(zip(scope, row))
        if all(tuple(assignment[v] for v in columns) in rows for columns, rows in factors):
            count += 1
            for i, (columns, _) in enumerate(factors):
                supports[i].add(tuple(assignment[v] for v in columns))
            for v in scope:
                values[v].add(assignment[v])
    return count, supports, values


def initial_factors(graph, options):
    """Inspect a real pre-elimination fixed point without editing the solver."""
    state = {}

    class InitialCaptured(Exception):
        pass

    def returned(frame, event, answer):
        if event == "return":
            live = frame.f_back.f_locals
            state.update(factors=[(f.scope, f.rows) for f in live["factors"]],
                         domains=deepcopy(live["domains"]), stats=deepcopy(live["stats"]),
                         consistent=answer)
            raise InitialCaptured
        return returned

    def called(frame, event, arg):
        if (event == "call" and frame.f_code.co_name == "propagate"
                and frame.f_globals.get("__name__") == constraints.__name__):
            return returned
        return None

    previous = sys.gettrace()
    sys.settrace(called)
    try:
        constraints.solve_constraints(graph, **options)
    except InitialCaptured:
        pass
    finally:
        sys.settrace(previous)
    return state


def original_solutions(graph):
    neighbors = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        neighbors[u].add(v)
        neighbors[v].add(u)
    assignment = dict(graph.get("fixed", []))

    def visit():
        if len(assignment) == len(neighbors):
            yield assignment.copy()
            return
        choices = {v: set(range(4)) - {assignment[w] for w in neighbors[v] if w in assignment}
                   for v in neighbors if v not in assignment}
        v = min(choices, key=lambda v: (len(choices[v]), -len(neighbors[v]), v))
        for color in sorted(choices[v]):
            assignment[v] = color
            yield from visit()
        assignment.pop(v, None)

    if not any(u in assignment and v in assignment and assignment[u] == assignment[v]
               for u, v in graph["edges"]):
        yield from visit()


class JointConsistencyTests(unittest.TestCase):
    def assert_exact(self, factors, domains):
        before = deepcopy((factors, domains))
        count, rows, values = enumerate_supports(factors, domains)
        answer = joint_supports(factors, domains, max_checks=1_000_000)
        self.assertTrue(answer["complete"])
        self.assertEqual(answer["consistent"], bool(count))
        self.assertEqual(answer["rows"], rows)
        self.assertEqual(answer["domains"], values)
        self.assertEqual((factors, domains), before)
        return answer

    def test_random_complete_factor_networks_against_cartesian_oracle(self):
        rng = random.Random(20261026)
        for index in range(120):
            vertices = rng.sample(range(-12, 20), rng.randrange(1, 6))
            domains = {v: {c for c in range(4) if rng.random() < .75} for v in vertices}
            factors = []
            for _ in range(rng.randrange(0, 7)):
                scope = tuple(rng.sample(vertices, rng.randrange(min(3, len(vertices)) + 1)))
                rows = frozenset(row for row in product(range(4), repeat=len(scope))
                                 if rng.random() < .6)
                factors.append((scope, rows))
            with self.subTest(index=index):
                self.assert_exact(factors, domains)

    def test_empty_scopes_domains_and_disconnected_components(self):
        for factors, domains in [([], {}), ([((), {()})], {}), ([((), set())], {}),
                                  ([((8,), {(0,), (1,)})], {8: set()}),
                                  ([((9,), {(0,), (1,)}), ((-3,), {(2,), (3,)})],
                                   {9: {0, 1}, -3: {2, 3}})]:
            self.assert_exact(factors, domains)

    def test_saturation_is_exact_support_without_claiming_solution_count(self):
        factors = [((v,), frozenset((c,) for c in range(4))) for v in (9, 20)]
        answer = self.assert_exact(factors, {9: set(range(4)), 20: set(range(4))})
        self.assertTrue(answer["all_supports_saturated"])
        self.assertFalse(answer["enumeration_complete"])
        self.assertLess(answer["assignments"], 16)

    def test_limits_expose_no_partial_support_and_do_not_mutate_inputs(self):
        factors = [((0, 1), frozenset(product(range(4), repeat=2))),
                   ((1, 2), frozenset(product(range(4), repeat=2)))]
        domains = {v: set(range(4)) for v in range(3)}
        before = deepcopy((factors, domains))
        for options in [dict(max_checks=0), dict(max_checks=17), dict(max_support_rows=1)]:
            answer = joint_supports(factors, domains, **options)
            self.assertFalse(answer["complete"])
            self.assertIsNone(answer["consistent"])
            self.assertIsNone(answer["rows"])
            self.assertIsNone(answer["domains"])
            self.assertEqual((factors, domains), before)

        class MainBudgetLimit(Exception):
            pass

        ticks = 0

        def charge():
            nonlocal ticks
            ticks += 1
            if ticks == 17:
                raise MainBudgetLimit

        with self.assertRaises(MainBudgetLimit):
            joint_supports(factors, domains, charge=charge)
        self.assertEqual((factors, domains), before)

    def test_external_charge_matches_counted_checks(self):
        ticks = []
        answer = joint_supports([((0,), {(1,)})], {0: {0, 1}}, charge=lambda: ticks.append(1))
        self.assertEqual(answer["checks"], len(ticks))
        self.assertTrue(answer["complete"])

    def test_iterative_join_exceeds_python_recursion_depth(self):
        size = sys.getrecursionlimit() + 10
        answer = joint_supports([((v,), {(0,)}) for v in range(size)],
                                [{0} for _ in range(size)], max_checks=10 * size,
                                max_support_rows=size)
        self.assertTrue(answer["complete"])
        self.assertTrue(answer["consistent"])
        self.assertEqual(answer["assignments"], 1)

    def test_fourteen_vertex_fixed_gap_and_every_bare_solution(self):
        inputs = json.loads((ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f/"
                             "propagation/inputs.json").read_text())
        graph = inputs["graph"]
        fixed = initial_factors(graph, inputs["options"])
        self.assertTrue(fixed["consistent"])
        bucket = [factor for factor in fixed["factors"] if 0 in factor[0]]
        answer = joint_supports(bucket, fixed["domains"])
        self.assertTrue(answer["complete"])
        self.assertFalse(answer["consistent"])
        self.assertEqual(answer["scope"], tuple(range(14)))
        self.assertEqual(list(original_solutions(graph)), [])

        bare_graph = dict(graph, fixed=[])
        solutions = list(original_solutions(bare_graph))
        self.assertEqual(len(solutions), 624)
        bare = initial_factors(bare_graph, inputs["options"])
        bucket = [factor for factor in bare["factors"] if 0 in factor[0]]
        answer = joint_supports(bucket, bare["domains"], max_checks=1_000_000)
        self.assertTrue(answer["complete"])
        self.assertTrue(answer["consistent"])
        observed_pair = None
        for (scope, _), rows in zip(bucket, answer["rows"]):
            if 9 in scope and 11 in scope:
                observed_pair = {(row[scope.index(9)], row[scope.index(11)]) for row in rows}
        self.assertEqual(observed_pair, {(a, b) for a in range(4) for b in range(4) if a != b})
        for coloring in solutions:
            for (scope, _), rows in zip(bucket, answer["rows"]):
                self.assertIn(tuple(coloring[v] for v in scope), rows)
            for v, domain in answer["domains"].items():
                self.assertIn(coloring[v], domain)

    def test_malformed_limits_and_scopes_are_rejected(self):
        for options in [dict(max_checks=-1), dict(max_checks=True),
                        dict(max_support_rows=-1), dict(charge=3)]:
            with self.assertRaises(ValueError):
                joint_supports([], {}, **options)
        with self.assertRaises(ValueError):
            joint_supports([((0, 0), {(0, 0)})], {0: {0}})
        with self.assertRaises(ValueError):
            joint_supports([((0,), {(4,)})], {0: {0}})


if __name__ == "__main__":
    unittest.main()
