"""Reviewer transfer reconstruction by literal 4^8 assignments, no producer imports."""
import itertools


def canonical(row):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in row)


def transfer(query, patterns, outer_patterns):
    lookup = {tuple(p): i for i, p in enumerate(patterns)}
    literal = [(row, lookup[canonical(row)])
               for row in itertools.product(range(4), repeat=8)
               if all(row[i] != row[(i+1) % 8] for i in range(8))]
    assert len(literal) == 6564
    answer = []
    for outer in outer_patterns:
        counts = [0] * len(patterns)
        boundary = {f'b{i}': value for i, value in enumerate(outer)}
        for row, index in literal:
            assignment = dict(boundary)
            assignment.update(zip(query['boundary_order'], row))
            if all(assignment[x] != assignment[y] for x, y in query['collar_edges']):
                counts[index] += 1
        answer.append(counts)
    return answer
