#!/usr/bin/env python3
"""Exclusive-create the fixed four-face/T-star calibration, not disk completions."""
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = 'audits/2026-10-23-941-gamma8-exterior-6b09cd4/certificate-v2.json'


def components(edges, colors, pair):
    todo = {v for v, c in colors.items() if c in pair}
    groups = []
    while todo:
        reached, stack = set(), [min(todo)]
        while stack:
            v = stack.pop()
            if v in reached:
                continue
            reached.add(v)
            stack.extend(b if a == v else a for a, b in edges
                         if v in (a, b) and (b if a == v else a) in todo - reached)
        todo -= reached
        groups.append(sorted(reached))
    return sorted(groups)


def main():
    prior = json.loads((HERE / 'frozen' / PREV).read_text())
    cells = prior['complete_predecessor_certificate']
    rows = []
    for cell in cells['candidates']:
        if cell['classification'] != 'local_necessary_type':
            continue
        core = cell['core']
        for side, uk, ck in itertools.product('CE', ['K2', 'N3'], ['K2', 'N3']):
            kinds = dict(u=uk, a='M2' if side == 'C' else 'N3',
                         b='N3' if side == 'C' else 'M2', c=ck)
            for ua, bc in itertools.product(range(2), repeat=2):
                if ua and not (side == 'E' and uk == 'N3' and core == 'L'):
                    continue
                if bc and not (side == 'C' and ck == 'N3' and core == 'R'):
                    continue
                names = {r: 'out_' + r for r in kinds}
                if ua:
                    names['u'] = names['a']
                if bc:
                    names['c'] = names['b']
                groups = sorted(sorted(r for r in kinds if names[r] == name)
                                for name in set(names.values()))
                # Canonical names agree with the independent partition checker.
                names = {r: 'out_' + min(g) for g in groups for r in g}
                colors = dict(cells['original_colors'])
                labels = dict(cells['original_component_labels'])
                for r, kind in kinds.items():
                    colors[names[r]], labels[names[r]] = int(kind[1]), kind[0]
                edges = {tuple(e) for e in cell['edges']}
                for role, ends in [('u', 'dr'), ('a', ['r', 'T']),
                                   ('b', ['T', 's']), ('c', 'sx')]:
                    edges.update(tuple(sorted((names[role], v))) for v in ends)
                edges.add(tuple(sorted((names['a'], names['b']))))
                orbit = []
                for m, n, k in itertools.product(range(2), repeat=3):
                    active = {x for x, bit in zip('MNK', (m, n, k)) if bit}
                    co = {v: c ^ (2 if labels[v] in active else 0) for v, c in colors.items()}
                    orbit.append(dict(action=[m, n, k], colors=co,
                        components={''.join(map(str, p)): components(edges, co, p)
                                    for p in itertools.combinations(range(4), 2)}))
                if core == 'O':
                    rule = ('x_continuation' if ck == 'N3' else
                            's_gap' if side == 'E' else
                            'd_continuation' if uk == 'N3' else 'r_gap')
                elif bc:
                    rule = 'x_continuation'
                elif ua:
                    rule = 'x_continuation' if ck == 'N3' else 's_gap'
                else:
                    rule = 'four_distinct_faces'
                rows.append(dict(id=cell['id'], core=core, T_M2_side=side, kinds=kinds,
                    partition=groups, edges=sorted(map(list, edges)), complete_prefix_orbit=orbit,
                    protected_private_bound=5 if core == 'O' else 4,
                    avoided_M2_side='E' if side == 'C' else 'C', witness_rule=rule))
    certificate = dict(schema='941-gamma8-m2-stars-v1', base=prior['base'],
        complete_predecessor_certificate=prior, prefix_rows=rows,
        paper_contract=dict(j=2, T_original_degree=5, same_original_exterior=True,
            full_M2_set_retained=True, E_may_be_rootless=True,
            protected_LR_bound=4, protected_O_bound=5,
            h_c_and_T_M2_in_E_exterior_bounds=[5, 6],
            stable_C_contact_and_rooted_E_and_T_M2_in_C_exterior_bounds=[5, 6],
            extra_separator_vertex_distinct_from_protected_set=True,
            prefix_rows_are_not_complete_stars_or_disk_completions=True),
        authority_boundaries=dict(finite_control='triggered and holds',
            original_source_control='not triggered', general_wrong_side='OPEN',
            eleven_type_exclusions=0, initial_pair_exclusions=0,
            common_k_lower_bound=23, smaller_bad=False, new_Lean=False, new_LP=False))
    with (HERE / 'certificate.json').open('x') as f:
        json.dump(certificate, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(status='CREATED', prefix_rows=len(rows),
                         orbit_states=8 * len(rows), local_palette_restrictions=48 * len(rows))))


if __name__ == '__main__':
    main()
