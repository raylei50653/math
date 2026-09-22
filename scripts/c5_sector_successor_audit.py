#!/usr/bin/env python3
"""Replay all saved closure obligations and audit one conditional edge ban."""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROSS = ROOT / 'artifacts/c5_sector_cross_row/observations.json'
BAN = ROOT / 'artifacts/c5_sector_empty_terminal/observations.json'
OUT = ROOT / 'artifacts/c5_sector_successor_audit/observations.json'
PAIRS = tuple(combinations(range(4), 2))


def freeze(value):
    return tuple(map(freeze, value)) if isinstance(value, list) else value


def normalize(row):
    order = list(dict.fromkeys(row))
    order += [c for c in range(4) if c not in order]
    mapping = {c: i for i, c in enumerate(order)}
    return tuple(mapping[c] for c in row), mapping


def actions(row, parts):
    for j, pair in enumerate(PAIRS):
        for bits in product((0, 1), repeat=len(parts[j])):
            selected = {v for cc, bit in zip(parts[j], bits) if bit for v in cc}
            # Explicit membership guards both directions of the swap.
            raw = tuple((pair[1] if c == pair[0] else pair[0]) if v in selected else c
                        for v, c in enumerate(row))
            target, mapping = normalize(raw)
            k = PAIRS.index(tuple(sorted(mapping[c] for c in pair)))
            yield dict(pair=pair, bits=bits, selected_frame=sorted(selected), raw_row=raw,
                       mapping=mapping, requirement=(target, k, parts[j], parts[5-j]))


def global_state(row, parts, pair):
    trans = {c: pair[1] if c == pair[0] else pair[0] if c == pair[1] else c
             for c in range(4)}
    target, mapping = normalize(tuple(trans[c] for c in row))
    target_parts = [None] * 6
    for j, old_pair in enumerate(PAIRS):
        k = PAIRS.index(tuple(sorted(mapping[trans[c]] for c in old_pair)))
        target_parts[k] = parts[j]
    return target, tuple(target_parts)


def build():
    saved = json.loads(CROSS.read_text())
    abstract = saved['abstract']
    states = [(freeze(s['row']), freeze(s['partitions'])) for s in abstract['states']]
    ids = {s: i for i, s in enumerate(states)}
    assert len(ids) == len(states) == 670
    acts = [list(actions(*s)) for s in states]
    exact = [[ids[global_state(*s, pair)] for pair in PAIRS] for s in states]
    index = {}
    for i, (row, parts) in enumerate(states):
        for j in range(6):
            index.setdefault((row, j, parts[j], parts[5-j]), set()).add(i)
    candidates = [[index.get(a['requirement'], set()) for a in aa] for aa in acts]

    # Replay the recorded eliminations only; do not run a new fixed-point loop.
    alive = set(range(len(states)))
    for round_ in abstract['deletion_rounds']:
        dead = {r['state'] for r in round_}
        assert len(dead) == len(round_) and dead <= alive
        for r in round_:
            i = r['state']
            if r['missing_action'] is not None:
                assert not candidates[i][r['missing_action']] & alive
            if r['missing_global'] is not None:
                assert exact[i][r['missing_global']] not in alive
            assert r['missing_action'] is not None or r['missing_global'] is not None
        alive -= dead
    witnesses = {r['state']: r for r in abstract['closed_successors']}
    assert set(witnesses) == alive and len(alive) == abstract['final_states'] == 603
    original_checks = 0
    for i, record in witnesses.items():
        assert len(record['successors']) == len(candidates[i])
        for options, target in zip(candidates[i], record['successors']):
            assert target in options & alive
            original_checks += 1
        assert record['global_successors'] == exact[i]
        assert set(exact[i]) <= alive

    source, action, forbidden = 397, 2, 330
    selected = acts[source][action]
    assert selected['pair'] == (0, 1) and selected['selected_frame'] == [0, 1, 2]
    assert selected['raw_row'] == (1, 0, 1, 2, 1)
    options = candidates[source][action]
    survivors = options & alive
    assert sorted(survivors) == [330, 331, 332, 333, 335, 337, 338, 339, 340, 342]
    records = []
    for i in sorted(options):
        row, parts = states[i]
        # Pull normalized color-pair indices back to raw post-swap colors.
        raw_parts = [parts[PAIRS.index(tuple(sorted(selected['mapping'][c] for c in pair)))]
                     for pair in PAIRS]
        def linked(pair, a, b):
            return any(a in cc and b in cc for cc in raw_parts[PAIRS.index(pair)])
        flags = dict(new02_1_to_3=linked((0, 2), 1, 3),
                     new12_0_separate_4=not linked((1, 2), 0, 4),
                     new13_0_separate_4=not linked((1, 3), 0, 4),
                     new13_2_separate_4=not linked((1, 3), 2, 4))
        records.append(dict(state=i, alive=i in alive, normalized_row=row,
                            normalized_partitions=parts, raw_partitions=raw_parts,
                            prerequisite_flags=flags))
    assert [r['state'] for r in records if r['alive'] and
            all(r['prerequisite_flags'].values())] == [330]
    replacement = min(survivors - {forbidden})
    assert replacement == 331 and witnesses[source]['successors'][action] == forbidden
    # Full witness audit after just the conditional (397, action 2, 330) ban.
    after_checks = 0
    for i, record in witnesses.items():
        for a, target in enumerate(record['successors']):
            if (i, a) == (source, action):
                target = replacement
            assert target in candidates[i][a] & alive
            assert (i, a, target) != (source, action, forbidden)
            after_checks += 1
        assert set(exact[i]) <= alive
    assert after_checks == original_checks
    # The complementary action has the same abstract requirement, but is a
    # different maximal component. Unframed components prevent identifying
    # the two actual swaps without an extra argument.
    assert acts[source][1]['requirement'] == selected['requirement']
    assert acts[source][1]['selected_frame'] == [4]

    ban = json.loads(BAN.read_text())
    inputs = {CROSS, BAN, Path(__file__).resolve()}
    for upstream in (saved, ban):
        for name, digest in upstream['input_sha256'].items():
            assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
            inputs.add(ROOT / name)
    return dict(schema=1,
                scope='Fixed 670-profile catalogue, single conditional transition ban; abstract witnesses are not graph realizations.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                              for p in sorted(inputs)},
                selected_action=selected, candidates=records,
                witness_override=dict(source=source, action=action,
                                      old_target=forbidden, new_target=replacement),
                complementary_action=dict(action=1, selected_frame=[4],
                                          same_abstract_requirement=True,
                                          actual_swap_equivalence_proved=False),
                summary=dict(initial_profiles=670, saved_deletions_replayed=670-len(alive),
                             inherited_profiles=len(alive), all_candidates=len(options),
                             alive_candidates=len(survivors), remaining_candidates=len(survivors)-1,
                             checked_existential_obligations_before=original_checks,
                             checked_existential_obligations_after=after_checks,
                             checked_global_obligations=6*len(alive), profile_deletions=0,
                             fixed_point_loop_rerun=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
