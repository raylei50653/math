#!/usr/bin/env python3
"""Finite paper tables for the complete twelve-attachment nine-point disk.

Every lookup uses one unchanged opposite boundary; no Kempe exchange or
four-colour theorem oracle is used. Arbitrary-source planarity is proved in
the companion report, independently of these literal edge checks.
"""
import itertools
from functools import cache

from four_color_twelve_cut_eight_side_verification import pairs

UNIFORM = (2,) * 6
SPECS = {
    '122223': ([(0, 2), (0, 4), (2, 4)], (0, 2, 4)),
    '122232': ([(0, 2), (0, 4), (2, 4)], (0, 2, 4)),
    '122313': ([(0, 2), (2, 4), (2, 5)], (0, 2, 5)),
    '122322': ([(0, 2), (2, 5), (3, 5)], (0, 2, 5)),
    '123213': ([(0, 2), (0, 4), (2, 4)], (0, 2, 4)),
    '131313': ([(0, 3), (1, 3), (3, 5)], (0, 1, 3)),
}
TABLES = {
    '122223': {'021021': '130213230', '021023': '210231310',
               '021321': '130213230', '021323': '213201013',
               '031021': '120313320', '031023': '210231310',
               '031321': '120203312', '031323': '320201132'},
    '122232': {'021021': '130232210', '021023': '130212230',
               '021321': '130202213', '021323': '130202213',
               '031021': '120232310', '031023': '120312320',
               '031321': '120203312', '031323': '310202231'},
    '122313': {'021032': '213201013', '021202': '130323210',
               '021232': '213021013', '021302': '130213230',
               '031032': '320201132', '031202': '120313320',
               '031232': '212021013', '031302': '210231310'},
    '122322': {'021012': '210231310', '021032': '130213230',
               '021302': '130213230', '021312': '210231310',
               '031012': '120203312', '031032': '120203312',
               '031302': '210231310', '031312': '120203312'},
    '123213': {'021021': '213103021', '021023': '213101023',
               '021321': '210103321', '021323': '210131320',
               '031021': '212103031', '031023': '212301013',
               '031321': '210103321', '031323': '210131320'},
    '131313': {'010201': '121312023', '010203': '121312023',
               '010213': '121302023', '010231': '123102023',
               '013201': '120132320', '013203': '120132320',
               '013213': '121032320', '013231': '121012023'},
    '222222': {'012012': '201303321', '012013': '231301023',
               '012021': '201303321', '012023': '203101123',
               '012031': '231203031', '012032': '203101123'},
}


@cache
def reduction_spec(profile):
    if tuple(profile) == UNIFORM:
        return dict(kind='identify_opposite', identified_Y_indices=[0, 3],
                    representative='222222', normalizing_triangle=[0, 1, 2])
    options = []
    for a in (0, 2, 4):
        for sign in (1, -1):
            transformed = tuple(profile[(a + sign*i) % 6] for i in range(6))
            key = ''.join(map(str, transformed))
            if key not in SPECS:
                continue
            for b in range(6):
                if {((a + sign*x) % 6, (b + sign*y) % 6)
                    for x, y in pairs(transformed)} == set(pairs(profile)):
                    options.append((key, a, sign, b))
    key, a, sign, b = min(options, key=lambda t: (t[0], t[1], -t[2], t[3]))
    xmap = [(a + sign*i) % 6 for i in range(6)]
    ymap = [(b + sign*i) % 6 for i in range(6)]
    spokes = [{(2*i+j) % 6 for j in range(3)} for i in range(3)]
    hubmap = [6 + spokes.index({xmap[j] for j in s}) for s in spokes]
    chords, triangle = SPECS[key]
    return dict(kind='add_noncrossing_chords', representative=key,
                a=a, sign=sign, b=b, normalizing_triangle=triangle,
                representative_to_original_X=xmap + hubmap,
                representative_to_original_Y=ymap,
                added_Y_index_pairs=[(ymap[i], ymap[j]) for i, j in chords])


def reduced_boundary_accepts(profile, beta):
    if any(beta[i] == beta[(i+1) % 6] for i in range(6)):
        return False
    spec = reduction_spec(profile)
    if spec['kind'] == 'identify_opposite':
        return beta[0] == beta[3]
    return all(beta[i] != beta[j] for i, j in spec['added_Y_index_pairs'])


def paper_lift(profile, beta):
    spec = reduction_spec(profile)
    uniform = spec['kind'] == 'identify_opposite'
    transformed = tuple(beta) if uniform else tuple(
        beta[j] for j in spec['representative_to_original_Y'])
    names = [transformed[j] for j in spec['normalizing_triangle']]
    assert len(set(names)) == 3
    names += sorted(set(range(4)) - set(names))
    inverse = {c: i for i, c in enumerate(names)}
    key = ''.join(str(inverse[c]) for c in transformed)
    lift = [names[int(c)] for c in TABLES[spec['representative']][key]]
    if uniform:
        return tuple(lift)
    result = [None] * 9
    for i, original in enumerate(spec['representative_to_original_X']):
        result[original] = lift[i]
    return tuple(result)


def validate_paper_tables():
    """Check all normalized branches and every literal original edge directly."""
    edges = ([(i, (i+1) % 6) for i in range(6)]
             + [(6+i, (2*i+j) % 6) for i in range(3) for j in range(3)]
             + [(6, 7), (7, 8), (8, 6)])
    for key, table in TABLES.items():
        profile = tuple(map(int, key))
        # The representative chosen by reduction_spec need not be itself under
        # an automorphism, so enumerate this table in its own stated coordinates.
        triangle = (0, 1, 2) if profile == UNIFORM else SPECS[key][1]
        chords = [] if profile == UNIFORM else SPECS[key][0]
        expected = set()
        for beta in itertools.product(range(4), repeat=6):
            if tuple(beta[i] for i in triangle) != (0, 1, 2):
                continue
            if any(beta[i] == beta[(i+1) % 6] for i in range(6)):
                continue
            if profile == UNIFORM and beta[0] != beta[3]:
                continue
            if any(beta[i] == beta[j] for i, j in chords):
                continue
            expected.add(''.join(map(str, beta)))
        assert expected == set(table) and len(table) == (6 if profile == UNIFORM else 8)
        for b, a in table.items():
            beta, lift = tuple(map(int, b)), tuple(map(int, a))
            assert all(lift[i] != lift[j] for i, j in edges)
            assert all(lift[x] != beta[y] for x, y in pairs(profile))
    return dict(normalized_branches=sum(map(len, TABLES.values())),
                every_original_edge_and_twelve_attachments_checked=True)
