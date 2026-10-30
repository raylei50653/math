#!/usr/bin/env python3
"""Explicit all-local-row extensions for a capped-antiprism three-branch seed.

The tables are mathematical construction data, not a coloring lookup oracle.
Every one of the eight normalized branch choices has a six-rung base case and
an eight-rung base case. The latter has a reversible pair at rungs 3 and 4,
so repeating that pair constructs every even length >=8.
"""

from itertools import permutations

# Key: (x_(n-1), x_2, y_0) with (a,x_0,x_1)=(0,1,2).
# Value: literal X word, literal Y word, b color.
SIX_RUNG_TEMPLATES = {
    (2, 1, 0): ('121212', '030303', 1),
    (2, 1, 3): ('121212', '303030', 1),
    (2, 3, 0): ('123212', '010303', 2),
    (2, 3, 3): ('123212', '301030', 2),
    (3, 1, 0): ('121213', '030302', 1),
    (3, 1, 3): ('121213', '303020', 1),
    (3, 3, 0): ('123123', '012012', 3),
    (3, 3, 3): ('123123', '302302', 1),
}

EIGHT_RUNG_TEMPLATES = {
    (2, 1, 0): ('12121212', '03030303', 1),
    (2, 1, 3): ('12121212', '30303030', 1),
    (2, 3, 0): ('12321212', '01030303', 2),
    (2, 3, 3): ('12312312', '30230230', 1),
    (3, 1, 0): ('12121213', '03030302', 1),
    (3, 1, 3): ('12121213', '30303020', 1),
    (3, 3, 0): ('12313123', '01202012', 3),
    (3, 3, 3): ('12312123', '30230302', 1),
}


def normalized_extension(n, branch_choices):
    """Construct colors in sorted original-vertex order x,y,a,b."""
    assert n >= 6 and n % 2 == 0
    table = SIX_RUNG_TEMPLATES if n == 6 else EIGHT_RUNG_TEMPLATES
    xword, yword, bcolor = table[tuple(branch_choices)]
    xs, ys = tuple(map(int, xword)), tuple(map(int, yword))
    if n >= 8:
        # With sigma_i=(x_i,y_i), all eight templates have K(sigma_3,
        # sigma_4) AND K(sigma_4,sigma_3). Insert copies of 3,4 after 4.
        repeats = (n - 8) // 2
        xs = xs[:5] + xs[3:5] * repeats + xs[5:]
        ys = ys[:5] + ys[3:5] * repeats + ys[5:]
    return xs + ys + (0, bcolor)


def extend_initial_local_row(n, local_coloring):
    """Extend EVERY proper seed coloring, using one shared color frame.

    local_coloring is a dictionary on {a,x_(n-1),x0,x1,y0,x2}. No search,
    stored full coloring, or previous whole-source witness is consulted.
    """
    central_colors = (local_coloring[2 * n], local_coloring[0], local_coloring[1])
    assert len(set(central_colors)) == 3
    fourth, = set(range(4)) - set(central_colors)
    palette = central_colors + (fourth,)
    normalize = {color: j for j, color in enumerate(palette)}
    choices = tuple(normalize[local_coloring[v]] for v in (n - 1, 2, n))
    normalized = normalized_extension(n, choices)
    result = tuple(palette[color] for color in normalized)
    assert all(result[v] == color for v, color in local_coloring.items())
    return result


def all_constructed_initial_extensions(n):
    """Exactly 192 specified witnesses, one for each proper initial local row."""
    answer = []
    for palette in permutations(range(4)):
        for choices in SIX_RUNG_TEMPLATES:
            normalized = normalized_extension(n, choices)
            answer.append(tuple(palette[color] for color in normalized))
    assert len(answer) == len(set(answer)) == 192
    return sorted(answer)
