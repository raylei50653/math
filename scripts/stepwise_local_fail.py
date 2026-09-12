#!/usr/bin/env python3
"""Statistics for 'locally certified failure' (Q2 / section 6a) on the C5 test bed.

python scripts/stepwise_local_fail.py          # writes artifacts/stepwise/local_fail.json

Same scope as stepwise_sufficiency.py (87 inside patches, same family as outside with
dihedral alignment, forward-only colouring of b0..b4, legal prefixes only).  For every
dead legal prefix we ask which *state map* S already certifies death, i.e. every legal
prefix with the same S-value is dead too:

  tail_k        last k colours (normalized)
  tail_k+count  last k colours plus number of distinct colours used so far
  count         number of distinct colours only
  full          the whole prefix (always certifies)

'fixed outside'  : certification inside one glued graph (Sigma_in meet Sigma_out).
'inside only'    : the S-class is dead already for Sigma_in alone (valid for any outside).
'every outside'  : the S-class is dead in every library outside (weaker than inside only).
"""
from collections import Counter, defaultdict
import json

from stepwise_sufficiency import FAN, OUT, RING, Bits, align, dihedral, normalize, sigma_from_edges


def state_maps():
    maps = {'count': lambda p: len(set(p)), 'full': lambda p: p}
    for k in (1, 2, 3):
        maps[f'tail{k}'] = (lambda k: lambda p: normalize(p[-k:]))(k)
        maps[f'tail{k}+count'] = (lambda k: lambda p: (normalize(p[-k:]), len(set(p))))(k)
    return maps


def main():
    data = json.loads((FAN / 'states.json').read_text())
    bits = Bits([tuple(p) for p in data['pattern_order']])
    sigmas = [sigma_from_edges([tuple(e) for e in s['edges']]) for s in data['states']]
    in_masks = [bits.mask(s) for s in sigmas]
    out_masks = {(x, g): bits.mask(align(sigmas[x], g)) for x in range(len(sigmas)) for g in dihedral()}
    legal = {n: [p for p in bits.prefixes[n] if all(p[j] != p[j + 1] for j in range(n - 1))]
             for n in range(1, RING)}
    maps = state_maps()
    classes = {(n, name): defaultdict(list) for n in legal for name in maps}
    for n, ps in legal.items():
        for name, f in maps.items():
            for p in ps:
                classes[(n, name)][f(p)].append(p)

    def dead_classes(n, name, feasible):
        """S-values all of whose legal prefixes are dead under `feasible`."""
        return {v for v, ps in classes[(n, name)].items()
                if all(not bits.completion[p] & feasible for p in ps)}

    stats = Counter()
    per_prefix = Counter()
    for i, m_in in enumerate(in_masks):
        inside_dead = {(n, name): dead_classes(n, name, m_in) for n in legal for name in maps}
        every_dead = {}
        for n in legal:
            for name, f in maps.items():
                cls = set(classes[(n, name)])
                for out in out_masks.values():
                    cls &= dead_classes(n, name, m_in & out)
                    if not cls:
                        break
                every_dead[(n, name)] = cls
        for out in out_masks.values():
            feasible = m_in & out
            for n, ps in legal.items():
                dead = [p for p in ps if not bits.completion[p] & feasible]
                stats[(n, 'dead_prefixes')] += len(dead)
                stats[(n, 'legal_prefixes')] += len(ps)
                fixed_dead = {name: dead_classes(n, name, feasible) for name in maps}
                for p in dead:
                    per_prefix[(n, p, 'dead')] += 1
                    for name, f in maps.items():
                        v = f(p)
                        if v in fixed_dead[name]:
                            stats[(n, name, 'fixed_outside')] += 1
                            per_prefix[(n, p, name)] += 1
                        if v in every_dead[(n, name)]:
                            stats[(n, name, 'every_outside')] += 1
                        if v in inside_dead[(n, name)]:
                            stats[(n, name, 'inside_only')] += 1
                            per_prefix[(n, p, name + ' inside-only')] += 1
    table = {}
    for n in legal:
        table[f'depth{n}'] = dict(legal=stats[(n, 'legal_prefixes')], dead=stats[(n, 'dead_prefixes')],
                                  certified={name: {scope: stats[(n, name, scope)]
                                                    for scope in ('fixed_outside', 'every_outside', 'inside_only')}
                                             for name in maps})
    result = dict(scope='see stepwise_sufficiency.py; legal prefixes only; forward-only colouring',
                  glued_graphs=len(in_masks) * len(out_masks),
                  table=table,
                  per_prefix={f'depth{n} {p}': {k: c for (m, q, k), c in sorted(per_prefix.items()) if (m, q) == (n, p)}
                              for (n, p, _) in sorted(set((n, p, 0) for (n, p, _) in per_prefix))})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'local_fail.json').write_text(json.dumps(result, indent=1, default=repr) + '\n')
    for d, row in table.items():
        print(f"{d}: legal {row['legal']}  dead {row['dead']}")
        for name, scopes in row['certified'].items():
            pct = {s: f"{v:7d} ({100 * v / row['dead']:5.1f}%)" if row['dead'] else '-' for s, v in scopes.items()}
            print(f"   {name:12s} fixed {pct['fixed_outside']}  every {pct['every_outside']}  inside-only {pct['inside_only']}")
    print('per dead prefix (glued graphs where dead / certified by count / tail3 / tail3+count / inside-only):')
    for key, row in result['per_prefix'].items():
        print(f"   {key}: dead {row['dead']:6d}  count {row.get('count', 0):6d}  tail3 {row.get('tail3', 0):6d}"
              f"  tail3+count {row.get('tail3+count', 0):6d}  inside-only {row.get('full inside-only', 0):6d}")


if __name__ == '__main__':
    main()
