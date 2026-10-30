#!/usr/bin/env python3
"""Complete-kernel indistinguishability; no new planar row-pruning claim.

Original-edge enumeration is independently checked by the sibling replay tool.
Every empty fibre is explicit. Full exterior problems are deliberately unequal.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess

import four_color_three_step_source_invariant as source
import ck_kempe_obstruction as kempe

ROOT = Path(__file__).resolve().parents[1]
COLORS = tuple(range(4))
BOUNDARY = tuple(range(3, 9))
PORTS = (9, 13, 11, 15)  # A,B,F,D, literal original identities


def edges_canonical(edges):
    return sorted({tuple(sorted(edge)) for edge in edges})


def exact_buckets(edges):
    factors = [dict(scope=edge, rows={r for r in product(COLORS, repeat=2) if r[0] != r[1]},
                    causes={edge}) for edge in edges]
    history = []
    for vertex in (0, 1, 2):
        bucket = [f for f in factors if vertex in f['scope']]
        factors = [f for f in factors if vertex not in f['scope']]
        scope = tuple(sorted(set().union(*(set(f['scope']) for f in bucket)) - {vertex}))
        causes = set().union(*(f['causes'] for f in bucket))
        fibres = []
        rows = set()
        for row in product(COLORS, repeat=len(scope)):
            assignment = dict(zip(scope, row))
            allowed = []
            for color in COLORS:
                assignment[vertex] = color
                if all(tuple(assignment[v] for v in f['scope']) in f['rows'] for f in bucket):
                    allowed.append(color)
            fibres.append(allowed)
            if allowed:
                rows.add(row)
        history.append(dict(eliminated_vertex=vertex, ordered_scope=scope,
                            causal_original_edges=sorted(causes), full_fibres=fibres,
                            nonempty_rows=len(rows), empty_rows=len(fibres)-len(rows)))
        factors.append(dict(scope=scope, rows=rows, causes=causes))
    remaining = [dict(ordered_scope=f['scope'], rows=sorted(f['rows']),
                      causal_original_edges=sorted(f['causes'])) for f in factors]
    return history, remaining


def direct_fibres(edges):
    fibres = {row: [] for row in product(COLORS, repeat=6)}
    for coloring in product(COLORS, repeat=9):
        if all(coloring[u] != coloring[v] for u, v in edges):
            fibres[coloring[3:]].append(coloring[:3])
    return [fibres[row] for row in fibres]


def reconstruct(history, remaining):
    """Delayed writeback against the whole remaining core problem."""
    answer = []
    for row in product(COLORS, repeat=6):
        assignment = dict(zip(BOUNDARY, row))
        lifts = [assignment] if all(tuple(assignment[v] for v in f['ordered_scope']) in
                                  set(map(tuple, f['rows'])) for f in remaining) else []
        for record in reversed(history):
            extended = []
            for assignment in lifts:
                index = 0
                for v in record['ordered_scope']:
                    index = 4 * index + assignment[v]
                extended.extend(assignment | {record['eliminated_vertex']: color}
                                for color in record['full_fibres'][index])
            lifts = extended
        answer.append(sorted(tuple(a[v] for v in (0, 1, 2)) for a in lifts))
    return answer


def projection_family(fibres):
    alive = [row for row, fibre in zip(product(COLORS, repeat=6), fibres) if fibre]
    family = []
    for size in range(7):
        for indexes in combinations(range(6), size):
            rows = sorted({tuple(row[i] for i in indexes) for row in alive})
            family.append(dict(ordered_scope=[BOUNDARY[i] for i in indexes], rows=rows))
    # All 64 projections at once, with the full relation included: generalized
    # semijoin consistency is already at its finite fixed point.
    for left in family:
        for right in family:
            overlap = sorted(set(left['ordered_scope']) & set(right['ordered_scope']))
            support = {tuple(r[right['ordered_scope'].index(v)] for v in overlap)
                       for r in right['rows']}
            assert all(tuple(r[left['ordered_scope'].index(v)] for v in overlap) in support
                       for r in left['rows'])
    return family


def outer_tensor(core_edges):
    colorings = [c for c in product(COLORS, repeat=9)
                 if all(c[u] != c[v] for u, v in core_edges)]
    indices = [[i for i, c in enumerate(colorings)
                if all(c[v] != color for v, color in zip((3, 4, 5, 6), ports))]
               for ports in product(COLORS, repeat=4)]
    assert all(indices)
    return dict(port_order=PORTS, core_colorings=colorings, full_fibre_indices=indices,
                counts=list(map(len, indices)))


def normalize(row):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in row)


def inner_circle_control(core_edges):
    """The existing partition fixed point on a genuine original C0, before z."""
    cycle = (2, 3, 4, 7, 5, 6)
    edges = [edge for edge in core_edges if 8 not in edge]
    states = kempe.patterns(6)
    accepted = 0
    for index, row in enumerate(states):
        fixed = dict(zip(cycle, row))
        if any(all((fixed | {0: a, 1: b})[u] != (fixed | {0: a, 1: b})[v]
                   for u, v in edges) for a, b in product(COLORS, repeat=2)):
            accepted |= 1 << index
    result = kempe.obstruction(6, accepted)
    assert accepted == 4969575 and result['residual_mask'] == 2075405200
    assert result['initial_obstruction_count'] == 18 and result['residual_count'] == 16
    return dict(name='PAIR-C0-D16', original_cycle=cycle, original_edges=edges,
                fixed_point=result,
                scope='Two-center inside relation on original C0 before eliminating z; '
                      'not the complete common exterior family of the 17-point sources.')


def exterior_audit(sources, fibres, tensor):
    core_rows = list(product(COLORS, repeat=6))
    word = (0, 1, 0, 1, 2, 0, 1, 2)
    summary, comparisons = {}, {}
    for item in sources:
        cycle = item['C_order']
        port_positions = [cycle.index(v) for v in PORTS]
        proper_words = [w for w in product(COLORS, repeat=8)
                        if all(w[i] != w[(i+1) % 8] for i in range(8))]
        # Exhaustive exterior contexts, indexed by all four inner attachments.
        compatible_counts = {colors: 0 for colors in product(COLORS, repeat=4)}
        for w in proper_words:
            pc = tuple(w[i] for i in port_positions)
            for colors in product(COLORS, repeat=4):
                if all(a != b for a, b in zip(colors, pc)):
                    compatible_counts[colors] += 1
            idx = 0
            for color in pc:
                idx = 4 * idx + color
            assert tensor['full_fibre_indices'][idx]
        total = nonempty = 0
        for row, fibre in zip(core_rows, fibres):
            if fibre:
                count = compatible_counts[row[:4]]
                nonempty += count
                total += count * len(fibre)
        idx = 0
        for pos in port_positions:
            idx = 4 * idx + word[pos]
        comparisons[item['name']] = len(tensor['full_fibre_indices'][idx])
        summary[item['name']] = dict(full_solution_count=total, nonempty_fibres=nonempty,
                                    complete_interface_rows=4**14,
                                    empty_fibres=4**14-nonempty)
        assert len(proper_words) == 6564
        assert len({normalize(w) for w in proper_words}) == 274
    return dict(proper_outer_words_per_source=6564, s4_patterns=274,
                accepts_all_proper_words=True, comparison_word=word,
                comparison_counts=comparisons, global_counts=summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    # Existing original source and embedding certificates, unchanged.
    old_sources = source.outer_attachment_controls()
    sources = []
    histories = []
    for key, name in [('alternating_outer_attachment_blocker', 'ALT-OUTER-17'),
                      ('planar_outer_attachment_control', 'PLANAR-TWIN-17')]:
        old = old_sources[key]
        edges = list(map(tuple, old['certificate']['original_edges']))
        histories.append(exact_buckets(edges)[0])
        sources.append(dict(name=name, vertex_order=list(range(17)), original_edges=edges,
                            C_order=old['certificate']['marked_original_cycle'],
                            original_paths=old['certificate']['private_paths'],
                            P_nonalternating=old['certificate']['P_nonalternating'],
                            networkx_planar=old['networkx_planar'],
                            embedding=old.get('embedding')))
    core_edges = [edge for edge in map(tuple, sources[0]['original_edges']) if max(edge) < 9]
    assert core_edges == [edge for edge in map(tuple, sources[1]['original_edges']) if max(edge)<9]
    history, remaining = exact_buckets(core_edges)
    assert histories[0] == histories[1] == history
    fibres = direct_fibres(core_edges)
    assert reconstruct(history, remaining) == fibres
    assert sum(map(len, fibres)) == 936 and sum(map(bool, fibres)) == 732
    controls = []
    for name, old in [('historical_adjacent9', source.historical.three_step_audit()),
                      ('historical_tree9', source.historical.independent_centers_audit())]:
        edges = edges_canonical(old['original_edges'])
        actual = direct_fibres(edges)
        assert actual == [[tuple(x) for x in f['full_internal_lifts']] for f in old['complete_fibres']]
        h, r = exact_buckets(edges)
        assert reconstruct(h, r) == actual
        controls.append(dict(name=name, vertices=list(range(9)), original_edges=edges,
                             boundary_order=BOUNDARY, full_fibres=actual,
                             solution_count=sum(map(len, actual)), nonempty_fibres=sum(map(bool, actual))))
    tensor = outer_tensor(core_edges)
    outer = exterior_audit(sources, fibres, tensor)
    assert outer['comparison_counts'] == {'ALT-OUTER-17': 291, 'PLANAR-TWIN-17': 276}
    assert outer['global_counts']['ALT-OUTER-17']['full_solution_count'] == 1924992
    assert outer['global_counts']['PLANAR-TWIN-17']['full_solution_count'] == 1913472
    witnesses = [dict(source='ALT-OUTER-17', full_coloring=(0,1,2,1,3,3,0,2,0,0,1,0,1,2,0,1,2)),
                 dict(source='PLANAR-TWIN-17', full_coloring=(0,1,2,1,2,0,3,3,0,0,1,2,1,0,0,1,2))]
    for witness in witnesses:
        for item in sources:
            c = witness['full_coloring']
            assert all(c[u] != c[v] for u, v in item['original_edges']) == (item['name'] == witness['source'])
    data = dict(colors=COLORS, elimination_order=[0,1,2], core_vertices=list(range(9)),
                labels=source.LABELS+['A','s','F','t','B','u','D','v'], core_edges=core_edges,
                kernel=dict(boundary_order=BOUNDARY, full_fibres=fibres, solution_count=936,
                            nonempty_fibres=732, empty_fibres=3364),
                history=history, core_remaining_factors=remaining,
                projection_closure=projection_family(fibres),
                outer_sources=sources, controls=controls, outer_tensor=tensor,
                outer_boolean_control=outer, global_difference_witnesses=witnesses,
                d_control=inner_circle_control(core_edges),
                claim='Full generated kernel equality; global residual problems unequal. '
                      'No new row deletion, no complete D gain, no 4CT.')
    target = args.out_dir/'results.json'
    target.write_text(json.dumps(data, sort_keys=True, separators=(',', ':'))+'\n')
    dependencies = ['scripts/four_color_three_step_relation_control.py',
                    'scripts/four_color_three_step_relation_replay.py',
                    'scripts/four_color_three_step_source_invariant.py',
                    'scripts/four_color_eight_cut_three_step_verification.py',
                    'scripts/four_color_seven_cut_verification.py']
    dependencies.append('scripts/ck_kempe_obstruction.py')
    receipt = dict(baseline=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                   sources={p:sha256((ROOT/p).read_bytes()).hexdigest() for p in dependencies},
                   outputs={'results.json':sha256(target.read_bytes()).hexdigest()},
                   evidence='Finite exact original-edge checks; paper congruence is not Lean formalized.')
    (args.out_dir/'verification.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(kernel=[936,732,3364], history=[(r['nonempty_rows'],r['empty_rows']) for r in history],
                          result_bytes=target.stat().st_size, outer=outer), sort_keys=True))


if __name__ == '__main__':
    main()
