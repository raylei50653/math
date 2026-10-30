#!/usr/bin/env python3
"""Exact finite checks for the proposed Ck counting bridge (stdlib only).

Verify that independent marginal weights add no restriction to Boolean D,
and provide an integer signed-signature certificate that the standard B5
counting cone still contains the C5 support 932. No graph is realized here.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import ck_kempe_obstruction as ck


def weak_marginal_check():
    """For each stable C5 support, explicitly place all mass on one witness."""
    table = ck.obligations(5)
    stable = []
    equations = 0
    for mask in range(1, 1 << len(table)):
        if ck.failure(mask, table) is not None:
            continue
        stable.append(mask)
        for j in ck._indices(mask):
            count = j + 1  # deliberately nonuniform positive coordinates
            for split in range(3):
                choices = ck.partition_options(5, j, split)
                eligible = [orbit & mask == orbit for orbit, _ in choices]
                selected = eligible.index(True)
                weights = [count if i == selected else 0 for i in range(len(choices))]
                assert all(w == 0 or ok for w, ok in zip(weights, eligible))
                assert sum(weights) == count
                equations += 1
    assert len(stable) == 153 and 932 in stable
    return dict(nonempty_stable_supports=len(stable), marginal_equations=equations,
                arbitrary_counts="n(c)=index(c)+1; no cross-coloring weight constraints",
                supports=stable)


def matchings(vertices):
    """Every perfect noncrossing matching on the supplied ordered ports."""
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for i in range(1, len(vertices)):
        b = vertices[i]
        for rest in matchings(vertices[1:i] + vertices[i + 1:]):
            result = ((a, b),) + rest
            if not any(u < x < v < y or x < u < y < v
                       for (u, v), (x, y) in combinations(result, 2)):
                yield result


def signatures(k):
    """Partial noncrossing matchings with a sign on each pair (DL §1.2)."""
    for size in range(0, k + 1, 2):
        for vertices in combinations(range(k), size):
            for matching in matchings(vertices):
                for signs in product((-1, 1), repeat=len(matching)):
                    yield tuple((a, b, s) for (a, b), s in zip(matching, signs))


def compatible(word, pair, signature):
    ports = {j for j, color in enumerate(word) if color in pair}
    covered = {j for a, b, _ in signature for j in (a, b)}
    return (ports == covered and
            all((word[a] == word[b]) == (sign == -1)
                for a, b, sign in signature))


def integrate(word):
    boundary = [0]
    for color in word[:-1]:
        boundary.append(boundary[-1] ^ color)
    assert boundary[-1] ^ word[-1] == 0
    return tuple(boundary)


def standard_b5_certificate():
    """Construct and verify a common y(S), not independent marginal weights."""
    words = [w for w in product((1, 2, 3), repeat=5)
             if all(w.count(color) % 2 == 1 for color in (1, 2, 3))]
    sigs = tuple(signatures(5))
    assert len(words) == 60 and len(sigs) == 61 and len(set(sigs)) == 61
    counts = {word: int(len(set(integrate(word))) == 4) for word in words}
    rows = [(word, pair) for word in words for pair in combinations((1, 2, 3), 2)]
    columns = [{i for i, (word, pair) in enumerate(rows) if compatible(word, pair, s)}
               for s in sigs]
    # Keep signatures compatible only with positive rows. Every positive row
    # has exactly one such signature, so common integer weights y(S)=1 suffice.
    eligible = [(s, ids) for s, ids in zip(sigs, columns)
                if ids and all(counts[rows[i][0]] for i in ids)]
    weights = {signature: 1 for signature, _ in eligible}
    assert len(weights) == 10
    for word, pair in rows:
        actual = sum(weights.get(s, 0) for s in sigs if compatible(word, pair, s))
        assert actual == counts[word]
    support = {ck.normalize(integrate(w)) for w in words if counts[w]}
    mask = sum(1 << ck.patterns(5).index(c) for c in support)
    assert mask == 932 and len(support) == 5
    assert Counter(counts.values()) == {0: 30, 1: 30}
    assert ck.failure(mask, ck.obligations(5)) is None
    # Every nonzero weight matters: deleting it must break an equation.
    for signature, ids in eligible:
        assert ids
        i = min(ids)
        word, pair = rows[i]
        corrupted = sum(weights.get(s, 0) for s in sigs
                        if s != signature and compatible(word, pair, s))
        assert corrupted != counts[word]
    return dict(parity_words=len(words), signed_signatures=len(sigs),
                common_weight_equations=len(rows), support_mask=mask,
                support_patterns=sorted(support), positive_parity_words=sum(counts.values()),
                weights=[dict(signature=s, weight=1) for s, _ in eligible],
                deletion_negative_controls=len(weights),
                conclusion="932 belongs to standard B5; no planar realization is claimed")


def report():
    root = Path(__file__).resolve().parents[1]
    files = (Path(__file__), root / "scripts/ck_kempe_obstruction.py")
    # This edge-wise identity holds for all assignments of three edge colors;
    # it does not recover cross-split component structure after a cut.
    for color in (1, 2, 3):
        assert ((color in (2, 3)) != (color in (1, 3))) == (color in (1, 2))
    return dict(scope="Exact finite algebra and support checks; no 4CT or realizability oracle",
                weak_marginals=weak_marginal_check(),
                standard_b5=standard_b5_certificate(),
                edgewise_xor_identity=True,
                sources={str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest()
                         for p in files})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps({"weak_D_supports": result["weak_marginals"]["nonempty_stable_supports"],
                      "weak_equations": result["weak_marginals"]["marginal_equations"],
                      "standard_B5_equations": result["standard_b5"]["common_weight_equations"],
                      "standard_B5_support": result["standard_b5"]["support_mask"],
                      "common_nonzero_weights": len(result["standard_b5"]["weights"])}, indent=2))


if __name__ == "__main__":
    main()
