#!/usr/bin/env python3
"""Read-only finite compatibility review of the all-k template theorem.

The arbitrary-k authority is the paper proof in REPORT.md.  This independent
stdlib checker reconstructs k <= 6 templates, reads the frozen literal column
supports, and compares their exact Fourier support with the word criterion.
It does not run an LP, enumerate original disks, or infer nonnegative lifts.
"""
from collections import defaultdict
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
OLD = ROOT / "audits/2026-10-21-w7-reuse-d5b8a86"


def partitions(n):
    """All set partitions, independently filtered for circular crossings."""
    if n == 0:
        yield ()
        return

    def visit(word, largest):
        if len(word) == n:
            yield tuple(word)
            return
        for label in range(largest + 2):
            yield from visit(word + [label], max(largest, label))

    yield from visit([0], 0)


def noncrossing(word):
    n = len(word)
    return not any(word[a] == word[c] and word[b] == word[d]
                   and word[a] != word[b]
                   for a in range(n) for b in range(a + 1, n)
                   for c in range(b + 1, n) for d in range(c + 1, n))


def complementary_partition(even_word):
    """Even-block forests and the odd contacts of their complementary faces.

    A face is identified by its sides of all noncrossing forest chords.
    Every block is connected by chords between its successive even contacts.
    """
    k = len(even_word)
    even_blocks = [[2*i for i, label in enumerate(even_word) if label == block]
                   for block in range(max(even_word) + 1)]
    chords = [(a, b) for block in even_blocks for a, b in zip(block, block[1:])]
    odd_faces = defaultdict(list)
    for odd in range(1, 2*k, 2):
        odd_faces[tuple(a < odd < b for a, b in chords)].append(odd)
    blocks = sorted(even_blocks + list(odd_faces.values()), key=min)
    word = [None] * (2*k)
    for label, block in enumerate(blocks):
        for i in block:
            word[i] = label
    assert noncrossing(word)
    assert len(blocks) == k + 1
    assert all(all(i % 2 == block[0] % 2 for i in block) for block in blocks)
    return tuple(word)


def xor_span(basis):
    span = [0]
    for vector in basis:
        span += [x ^ vector for x in span]
    assert len(span) == len(set(span))
    return tuple(sorted(span))


def cosets(subgroup, n):
    seen = set()
    answer = []
    for point in range(n):
        if point not in seen:
            support = tuple(sorted(point ^ h for h in subgroup))
            answer.append(support)
            seen.update(support)
    assert len(seen) == n
    return answer


def reconstructed_columns(k, rng):
    even_partitions = [p for p in partitions(k) if noncrossing(p)]
    rng.shuffle(even_partitions)
    columns = []
    full_partitions = []
    for p in even_partitions:
        word = complementary_partition(p)
        full_partitions.append(word)
        anchors = {word[0], word[1]}
        basis = [sum(1 << (i - 2) for i in range(2, 2*k) if word[i] == block)
                 for block in range(k + 1) if block not in anchors]
        assert len(basis) == k - 1
        columns.extend(cosets(xor_span(basis), 1 << (2*k - 2)))
    assert len(even_partitions) == math.comb(2*k, k) // (k + 1)
    assert len(set(full_partitions)) == len(even_partitions)
    assert len(columns) == len(set(columns))
    return sorted(columns), len(even_partitions)


def exact_support_from_columns(raw_columns, k, rng):
    """No partition generator or proposed rank formula is used here."""
    n = 1 << (2*k - 2)
    columns = list(raw_columns)
    rng.shuffle(columns)
    groups = defaultdict(set)
    for col in columns:
        assert col == tuple(sorted(set(col)))
        assert len(col) == 1 << (k - 1)
        subgroup = tuple(sorted(point ^ col[0] for point in col))
        groups[subgroup].add(col)
    allowed = set()
    for subgroup, family in groups.items():
        elements = set(subgroup)
        assert 0 in elements
        assert all(a ^ b in elements for a in subgroup for b in subgroup)
        assert family == set(cosets(subgroup, n))
        allowed.update(a for a in range(n)
                       if all((a & h).bit_count() % 2 == 0 for h in subgroup))
    return allowed, groups


def completed_bits(a, k):
    bits = [0, 0] + [(a >> (i - 2)) & 1 for i in range(2, 2*k)]
    bits[0] = sum(bits[2::2]) % 2
    bits[1] = sum(bits[3::2]) % 2
    return bits


def reduced_word(bits):
    stack = []
    for i, selected in enumerate(bits):
        if selected:
            palette = i % 2
            if stack and stack[-1] == palette:
                stack.pop()
            else:
                stack.append(palette)
    return tuple(stack)


def return_count(k):
    """Direct polynomial-sized path recurrence, independent of Fourier data."""
    counts = {0: 1}
    for i in range(2*k):
        next_counts = defaultdict(int)
        for point, count in counts.items():
            next_counts[point] += count
            step = 1 if (point + i) % 2 == 0 else -1
            next_counts[point + step] += count
        counts = dict(next_counts)
    return counts.get(0, 0)


def assert_same_columns(actual, expected):
    if sorted(actual) != sorted(expected):
        raise ValueError("literal template columns differ")


def review(seed):
    manifest = json.loads((AUDIT / "BASE.json").read_text())
    assert manifest["base"] == "30f2d19275657393b7354ed75eca31439d8ee12b"
    required = [OLD / "templates/templates.json.gz", OLD / "fourier/ranks.json"]
    frozen = {entry["path"]: entry for entry in manifest["inputs"]}
    hashes = {}
    for path in required:
        relative = str(path.relative_to(ROOT))
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == frozen[relative]["sha256"]
        assert len(data) == frozen[relative]["bytes"]
        hashes[relative] = digest
    raw = json.loads(gzip.decompress(required[0].read_bytes()))
    previous = json.loads(required[1].read_text())["templates"]
    rng = random.Random(seed)
    results = []
    saved = {}
    for k in range(1, 7):
        columns = [tuple(col) for col in raw[str(k)]]
        rebuilt, partition_count = reconstructed_columns(k, rng)
        assert_same_columns(columns, rebuilt)
        allowed, groups = exact_support_from_columns(columns, k, rng)
        predicted = {a for a in range(1 << (2*k - 2))
                     if not reduced_word(completed_bits(a, k))}
        assert allowed == predicted
        assert allowed == set(previous[k - 1]["allowed_frequencies"])
        rank = len(allowed)
        assert rank == return_count(k) == math.comb(2*k - 1, k - 1)
        assert len(groups) == partition_count
        results.append(dict(k=k, rows=1 << (2*k - 2), columns=len(columns),
                            complete_coset_families=len(groups),
                            exact_rank=rank,
                            literal_template_reconstruction=True,
                            frequency_by_frequency_word_equivalence=True))
        saved[k] = (columns, rebuilt, allowed, groups)

    columns, rebuilt, allowed, groups = saved[2]
    # Palette-even totals alone admit E O E O; its forced pairs cross.
    bad_frequency = 3
    bits = completed_bits(bad_frequency, 2)
    assert bits == [1, 1, 1, 1]
    assert all(sum(bits[p::2]) % 2 == 0 for p in (0, 1))
    assert reduced_word(bits) == (0, 1, 0, 1)
    assert bad_frequency not in allowed

    # A complete coset family from only one subgroup has rank two, not three.
    one_subgroup = min(groups)
    one_family = list(groups[one_subgroup])
    incomplete_support, _ = exact_support_from_columns(one_family, 2, rng)
    assert len(incomplete_support) == 2 < math.comb(3, 1)

    # Preserve the column size while replacing a legitimate k=2 edge by a
    # diagonal.  Literal reconstruction must reject it.
    mutated = list(columns)
    replacement = None
    for i, col in enumerate(columns):
        for old_point in col:
            for new_point in range(4):
                candidate = tuple(sorted((set(col) - {old_point}) | {new_point}))
                if len(candidate) == len(col) and candidate not in set(rebuilt):
                    replacement = (i, col, candidate)
                    break
            if replacement:
                break
        if replacement:
            break
    assert replacement is not None
    index, original, changed = replacement
    mutated[index] = changed
    rejected = False
    try:
        assert_same_columns(mutated, rebuilt)
    except ValueError:
        rejected = True
    assert rejected

    return dict(
        status="PASS; all-k paper theorem, finite compatibility only; no cone verdict",
        mathematical_base=manifest["mathematical_base"],
        audit_base=manifest["base"],
        arbitrary_k_authority="REPORT.md self-contained paper proof; not a Lean theorem",
        inputs_sha256=hashes,
        templates=results,
        negative_controls=dict(
            palette_even_crossing_word=dict(k=2, frequency=bad_frequency,
                completed_bits=bits, excluded_by_frozen_columns=True),
            incomplete_subgroup_family=dict(k=2, columns=len(one_family),
                exact_rank=len(incomplete_support), full_template_rank=3,
                full_rank_formula_rejected=True),
            size_preserving_column_corruption=dict(k=2,
                original=list(original), changed=list(changed), rejected=True)),
        limitations=["Walsh character reconstruction uses signed column sums",
                     "No nonnegative-cone characterization or shared-Z gluing",
                     "No original-source realization or exclusion",
                     "No large LP, new original-disk enumeration, or Lean change"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path,
                        help="exclusive-create a result inside this template directory")
    args = parser.parse_args()
    result = review(args.seed)
    if args.output:
        dest = args.output.resolve()
        if dest.parent != HERE:
            raise ValueError("output must be directly inside template/")
        with dest.open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    else:
        assert result == json.loads((HERE / "result.json").read_text())
    print(json.dumps(dict(status=result["status"], seed=args.seed,
                          exact_ranks=[row["exact_rank"] for row in result["templates"]],
                          negative_controls="3 passed"), indent=2))


if __name__ == "__main__":
    main()
