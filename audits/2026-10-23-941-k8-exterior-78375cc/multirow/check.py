"""Independent finite seven-row certificate checker; no source-realization claim.

No producer imports. Rebuild complete cap fibres by graph backtracking, validate
every survivor's six partitions and all lifts/subset swaps, and exhaust every
deleted state's partitions at its claimed elimination stage. Sound deletions
plus a closed final set establish the greatest necessary fixed point, without
requiring that a deletion occurred at the earliest possible iteration.
"""
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import json
import random
import sys
import time

if sys.flags.optimize:
    raise RuntimeError('Checker requires active assertions; do not use Python -O or -OO.')

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'frozen/audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/certificate.json'
BASE = '78375cc0e995c868c221605c24835d7e622f0091'
SOURCE_SHA256 = '0d53cda484f624966dcf5e46cef6933ccc4af2e542d27250258640b7906be6c8'
FULL_SCOPE = {0, 1, 2, 3}
ROWS = tuple(tuple(map(int, q)) for q in ('01012', '01023', '01201', '01203', '01213', '01231', '01232'))
PAIRS = tuple(combinations(range(4), 2))
PAIR_ORDER = (0, 5, 1, 4, 2, 3)
RINGS = (tuple(range(8)), tuple(range(8, 13)))
EDGES = tuple((c[i], c[(i + 1) % len(c)]) for c in RINGS for i in range(len(c)))


def normalize(word):
    order = list(dict.fromkeys(word))
    order.extend(c for c in range(4) if c not in order)
    mapping = tuple(order.index(c) for c in range(4))
    return tuple(mapping[c] for c in word), mapping


def encode(q, word):
    return ROWS.index(q) * 65536 + sum(c * 4 ** i for i, c in enumerate(word))


def decode(sid):
    assert isinstance(sid, int) and 0 <= sid < len(ROWS) * 65536, ('bad state', sid)
    return ROWS[sid // 65536], tuple((sid // 4 ** i) % 4 for i in range(8))


def canonical_partition(blocks):
    return tuple(sorted(tuple(sorted(b)) for b in blocks))


def components(vertices, edges):
    adjacent = {v: set() for v in vertices}
    for a, b in edges:
        if a in adjacent and b in adjacent:
            adjacent[a].add(b)
            adjacent[b].add(a)
    answer = []
    unseen = set(adjacent)
    while unseen:
        todo = [min(unseen)]
        block = set(todo)
        unseen.difference_update(todo)
        while todo:
            v = todo.pop()
            fresh = adjacent[v] & unseen
            unseen.difference_update(fresh)
            block.update(fresh)
            todo.extend(fresh)
        answer.append(block)
    return canonical_partition(answer)


def joined(left, right):
    vertices = set().union(*(set(b) for b in left + right)) if left or right else set()
    edges = [(b[0], v) for b in left + right for v in b[1:]]
    return components(vertices, edges)


def noncrossing(part, circle):
    index = {v: i for i, v in enumerate(circle)}
    portions = [sorted(index[v] for v in b if v in index) for b in part]
    for a, b in combinations(portions, 2):
        for x, y in combinations(a, 2):
            if any(x < z < y for z in b) and any(z < x or z > y for z in b):
                return False
    return True


@lru_cache(None)
def annular(part):
    if not all(noncrossing(part, circle) for circle in RINGS):
        return False
    through = {i for i, b in enumerate(part) if any(v < 8 for v in b) and any(v >= 8 for v in b)}
    if not through:
        return True
    label = {v: i for i, b in enumerate(part) for v in b}
    orders = []
    for circle in RINGS:
        for i, block in enumerate(part):
            places = [j for j, v in enumerate(circle) if v in block]
            if len(places) < 2:
                continue
            occupied_gaps = set()
            for j, v in enumerate(circle):
                if label.get(v) not in through - {i}:
                    continue
                predecessors = [p for p in places if p < j]
                occupied_gaps.add(max(predecessors) if predecessors else max(places))
            if len(occupied_gaps) > 1:
                return False
        seq = [label[v] for v in circle if label.get(v) in through]
        compressed = [seq[i] for i in range(len(seq)) if seq[i] != seq[i - 1]]
        if not compressed:
            compressed = seq[:1]
        if len(compressed) != len(through) or len(set(compressed)) != len(through):
            return False
        orders.append(compressed)
    a, b = orders
    for other in (b, b[::-1]):
        for offset in range(len(other)):
            if a == other[offset:] + other[:offset]:
                return True
    return False


def verify_cap(cap):
    vertices = cap['ordered_boundary'] + cap['ordered_inner']
    assert len(vertices) == len(set(vertices)) == 15
    where = {v: i for i, v in enumerate(vertices)}
    edges = tuple((where[a], where[b]) for a, b in cap['edges'])
    adjacent = [set() for _ in vertices]
    for a, b in edges:
        adjacent[a].add(b)
        adjacent[b].add(a)
    expected_words = {normalize(w)[0] for w in product(range(4), repeat=8)
                      if all(w[i] != w[(i + 1) % 8] for i in range(8))}
    fibres = {}
    for fibre in cap['complete_fibres']:
        word = tuple(fibre['word'])
        assert word not in fibres
        coloring = list(word) + [-1] * 7
        solutions = []

        def search():
            pending = [v for v in range(8, 15) if coloring[v] < 0]
            if not pending:
                solutions.append(tuple(coloring[8:]))
                return
            options = {v: set(range(4)) - {coloring[u] for u in adjacent[v] if coloring[u] >= 0}
                       for v in pending}
            v = min(pending, key=lambda x: (len(options[x]), -len(adjacent[x]), x))
            for c in sorted(options[v]):
                coloring[v] = c
                search()
            coloring[v] = -1

        if all(coloring[a] != coloring[b] for a, b in edges if a < 8 and b < 8):
            search()
        declared = [tuple(lift) for lift in fibre['full_lifts']]
        assert len(set(declared)) == len(declared)
        assert sorted(solutions) == sorted(declared), ('incomplete full fibre', word)
        fibres[word] = tuple(solutions)
    assert set(fibres) == expected_words and len(fibres) == 274
    return edges, fibres


def initial_states(cap, fibres):
    palette_permutations = tuple(permutations(range(4)))
    support = {tuple(p[c] for c in w) for w, lifts in fibres.items() if lifts for p in palette_permutations}
    residual = {tuple(p[c] for c in w) for w in cap['residual_accepting_words'] for p in palette_permutations}
    assert residual <= support
    return {encode(q, w) for q in ROWS for w in (residual if q == ROWS[-1] else support)}


@lru_cache(None)
def exterior_catalog(active):
    forced = components(active, EDGES)
    output = []

    def enumerate_blocks(at, blocks):
        if at == len(forced):
            part = canonical_partition(blocks)
            if all(noncrossing(part, circle) for circle in RINGS):
                output.append(part)
            return
        new = set(forced[at])
        for i in range(len(blocks)):
            previous = blocks[i]
            blocks[i] = previous | new
            enumerate_blocks(at + 1, blocks)
            blocks[i] = previous
        enumerate_blocks(at + 1, blocks + [new])

    enumerate_blocks(0, [])
    assert len(set(output)) == len(output)
    return tuple(output)


def validate_partition(part, colors, pair):
    flat = [v for b in part for v in b]
    assert all(b for b in part) and len(flat) == len(set(flat))
    assert set(flat) == {v for v, c in enumerate(colors) if c in pair}
    label = {v: i for i, b in enumerate(part) for v in b}
    assert all(label[a] == label[b] for a, b in EDGES if a in label and b in label)
    assert all(noncrossing(part, circle) for circle in RINGS)


def read_controls(certificate):
    if 'partition_catalogue' not in certificate:
        answer = {}
        for item in certificate['necessary_controls']:
            assert item['state'] not in answer
            groups = item['choices']
            assert len(groups) == 3 and all(len(g) == 2 for g in groups)
            answer[item['state']] = tuple(canonical_partition(p) for g in groups for p in g)
        return answer
    catalogue = []
    for masks in certificate['partition_catalogue']:
        assert all(isinstance(m, int) and 0 < m < (1 << 13) for m in masks)
        assert sum(masks) == sum(1 << v for v in range(13) if any(m >> v & 1 for m in masks))
        catalogue.append(canonical_partition(tuple(v for v in range(13) if m >> v & 1) for m in masks))
    choices = certificate['choice_catalogue']
    assert all(len(c) == 6 and all(isinstance(i, int) and 0 <= i < len(catalogue) for i in c) for c in choices)
    answer = {}
    for sid, ci in certificate['necessary_controls']:
        assert sid not in answer and isinstance(ci, int) and 0 <= ci < len(choices)
        answer[sid] = tuple(catalogue[i] for i in choices[ci])
    return answer


def check(certificate, source, seed=None):
    assert set(certificate) == {'schema', 'source_sha256', 'base', 'strong', 'index', 'distribution',
                                'initial', 'rounds', 'remaining', 'necessary_controls',
                                'partition_catalogue', 'choice_catalogue'}, 'unexpected compact certificate fields'
    assert certificate['schema'] == '941-k8-seven-row-compact-v1'
    assert certificate['source_sha256'] == SOURCE_SHA256 and certificate['base'] == BASE
    assert certificate['strong'] is True
    assert certificate['index'] in FULL_SCOPE
    cap = source['caps'][certificate['index']]
    assert certificate['distribution'] == cap['distribution']
    edges, fibres = verify_cap(cap)
    initial = initial_states(cap, fibres)
    assert len(initial) == certificate['initial']
    final = set(certificate['remaining'])
    assert len(final) == len(certificate['remaining']) and final <= initial
    controls = read_controls(certificate)
    assert set(controls) == final, 'survivor controls do not match complete final state set'

    @lru_cache(None)
    def local_signatures(canonical_word, canonical_pair):
        signatures = set()
        for lift in fibres[canonical_word]:
            colors = canonical_word + lift
            active = [v for v, c in enumerate(colors) if c in canonical_pair]
            part = components(active, edges)
            signatures.add(canonical_partition(tuple(v for v in b if v < 8) for b in part if any(v < 8 for v in b)))
        return tuple(signatures)

    @lru_cache(None)
    def swap_outcomes(q, word, pair, part):
        canonical_word, mapping = normalize(word)
        canonical_pair = tuple(sorted(mapping[c] for c in pair))
        results = set()
        for local in local_signatures(canonical_word, canonical_pair):
            full = joined(part, local)
            for selected in product((False, True), repeat=len(full)):
                changed = set().union(*(set(block) for yes, block in zip(selected, full) if yes))
                new = tuple(c ^ (pair[0] ^ pair[1]) if i in changed else c for i, c in enumerate(word + q))
                nq, palette = normalize(new[8:])
                if nq not in ROWS:
                    return None
                results.add(encode(nq, tuple(palette[c] for c in new[:8])))
        return frozenset(results)

    def allowed(sid, pair_index, current):
        q, word = decode(sid)
        pair = PAIRS[pair_index]
        active = tuple(v for v, c in enumerate(word + q) if c in pair)
        result = []
        for part in exterior_catalog(active):
            targets = swap_outcomes(q, word, pair, part)
            if targets is not None and targets <= current:
                result.append(part)
        return result

    current = set(initial)
    deleted = 0
    for step, round_data in enumerate(certificate['rounds']):
        before = [sum(s // 65536 == i for s in current) for i in range(7)]
        assert before == round_data['before']
        removed = round_data['removed']
        assert len(removed) == len(set(removed)) and set(removed) <= current
        assert [sum(s // 65536 == i for s in removed) for i in range(7)] == round_data['removed_counts']
        for sid in removed:
            impossible = False
            for i in range(3):
                first, second = allowed(sid, i, current), allowed(sid, 5 - i, current)
                if not any(annular(canonical_partition(a + b)) for a in first for b in second):
                    impossible = True
                    break
            assert impossible, ('unsound deletion', step, sid)
        current.difference_update(removed)
        deleted += len(removed)
    assert current == final and certificate['rounds'][-1]['removed'] == [], 'incomplete state accounting or unstabilized final set'

    order = sorted(final)
    if seed is not None:
        random.Random(seed).shuffle(order)
    palette_checks = 0
    for count, sid in enumerate(order, 1):
        q, word = decode(sid)
        chosen = controls[sid]
        for offset in range(0, 6, 2):
            assert annular(canonical_partition(chosen[offset] + chosen[offset + 1])), ('nonplanar control', sid, offset)
        for pi, part in zip(PAIR_ORDER, chosen):
            validate_partition(part, word + q, PAIRS[pi])
            targets = swap_outcomes(q, word, PAIRS[pi], part)
            assert targets is not None and targets <= final, ('unsafe survivor partition', sid, pi)
            palette_checks += 1
        if count % 5000 == 0:
            print('checked survivors', count, '/', len(final), flush=True)
    return dict(index=certificate['index'], initial=len(initial), remaining=len(final),
                remaining_by_row=[sum(s // 65536 == i for s in final) for i in range(7)],
                validated_deletions=deleted, survivor_palette_checks=palette_checks,
                complete_fibres=len(fibres), complete_lifts=sum(map(len, fibres.values())),
                source_realization=False, status='CAP_PASS')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('certificates', nargs='*', type=Path)
    parser.add_argument('--seed', type=int)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not args.certificates:
        args.certificates = [HERE / f'CAP_{i}_COMPACT.json' for i in sorted(FULL_SCOPE)]
    raw = SOURCE.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == SOURCE_SHA256
    frozen_inputs = json.loads((HERE.parent / 'INPUTS.json').read_text())
    assert frozen_inputs['base'] == BASE
    source_entry = next(item for item in frozen_inputs['inputs']
                        if item['snapshot'] == str(SOURCE.relative_to(HERE.parent)))
    assert source_entry['sha256'] == digest and source_entry['bytes'] == len(raw)
    source = json.loads(raw)
    reports = []
    start = time.monotonic()
    for path in args.certificates:
        certificate = json.loads(path.read_text())
        assert certificate.get('source_sha256', digest) == digest
        report = check(certificate, source, args.seed)
        reports.append(report)
        print(json.dumps(report, sort_keys=True), flush=True)
    scope = {r['index'] for r in reports}
    assert len(scope) == len(reports), 'duplicate representative certificates'
    status = 'PASS' if scope == FULL_SCOPE else 'PARTIAL_PASS'
    result = dict(schema='941-k8-seven-row-independent-check-v1', source_sha256=digest,
                  base=BASE, strong=True, status=status, checked_indices=sorted(scope),
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  certificates=reports, seed=args.seed, seconds=round(time.monotonic() - start, 3))
    if args.output:
        with args.output.open('x') as f:
            json.dump(result, f, indent=2, sort_keys=True)
            f.write('\n')
    print(json.dumps(dict(status=status, files=len(reports), seconds=result['seconds'])), flush=True)


if __name__ == '__main__':
    main()
