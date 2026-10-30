#!/usr/bin/env python3
"""Separate the fixed six-leaf target from the published 102-ray K6 cone.

This is an exact finite calculation, not a proof that K6 contains all plane
sources.  The imported author ray declarations are checked against the original
2 MiB compressed byte-range prefix, not a fresh network download.  The authors'
complete multi-gigabyte closure certificate is not replayed here.
"""
from __future__ import annotations

import argparse
import bz2
from hashlib import sha256
import io
from itertools import permutations, product
import json
from pathlib import Path
import re
import tarfile

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'audits/2026-10-30-bernhart-universal-marking'
AUTHOR = AUDIT / 'author-k6-rays.json'
PREFIX = AUDIT / 'author-proof-archive-prefix.tar.bz2'
TARGET = ROOT / 'audits/2026-10-29-bernhart-endpoint-ray/r2-support-actions.json'
DEFAULT = AUDIT / 'k6-separation.json'
PREFIX_SHA256 = 'b47f6091ccc3de39bc133ccbdbd0ec74e9a2f4d807e71492d406cb2979bb6d64'
BLOCK_SHA256 = '6585c730eb03c66b7b944b858a316fa903124ee56f77ef7d762abf3c95fa2130'


def canonical(word):
    colors = {}
    return tuple(colors.setdefault(c, len(colors) + 1) for c in word)


def abc(word):
    return ''.join('ABC'[c - 1] for c in word)


def author_data():
    """Re-extract all 102 K6 declarations from the pinned archive byte prefix."""
    saved = json.loads(AUTHOR.read_text())
    prefix = PREFIX.read_bytes()
    assert len(prefix) == 2_097_152
    assert sha256(prefix).hexdigest() == PREFIX_SHA256
    dec = bz2.BZ2Decompressor()
    partial_tar = dec.decompress(prefix)
    assert not dec.eof  # This is deliberately only the first byte range.
    with tarfile.open(fileobj=io.BytesIO(partial_tar), mode='r:') as archive:
        first = archive.next()
        assert first.name == 'proof-corr.txt' and first.isfile()
        # The declarations are at the beginning of this 50 GB tar member.
        text = archive.extractfile(first).read(1_000_000).decode()
    declarations, rays = [], []
    for line_number, line in enumerate(text.splitlines(), 1):
        match = re.fullmatch(r'6\.(\d+): (.*)', line)
        if not match:
            continue
        counts = {}
        for term in match[2].split(' + '):
            entry = re.fullmatch(r'(?:(\d+) \* )?([ABC]{6})', term)
            assert entry is not None
            word, count = entry[2], int(entry[1] or 1)
            assert word not in counts and count > 0
            integer_word = tuple('ABC'.index(c) + 1 for c in word)
            assert canonical(integer_word) == integer_word
            assert all(integer_word.count(c) % 2 == 0 for c in (1, 2, 3))
            counts[word] = count
        declarations.append(dict(source_line=line_number, text=line))
        rays.append(dict(index=int(match[1]), canonical_counts=counts))
    assert [row['index'] for row in rays] == list(range(1, 103))
    assert [row['source_line'] for row in declarations] == list(range(52, 154))
    block = '\n'.join(row['text'] for row in declarations) + '\n'
    assert sha256(block.encode()).hexdigest() == BLOCK_SHA256
    assert saved['declarations'] == declarations and saved['rays'] == rays
    provenance = saved['provenance']
    assert provenance['downloaded_prefix_sha256'] == PREFIX_SHA256
    assert provenance['declaration_block_sha256'] == BLOCK_SHA256
    assert provenance['downloaded_prefix_bytes'] == len(prefix)
    assert provenance['requested_range'] == 'bytes=0-2097151'
    assert provenance['response_status'] == 206
    assert provenance['published_K6_ray_count'] == len(rays)
    assert provenance['archive_member'] == first.name
    assert provenance['closure_certificate_replayed'] is False
    return saved


def report():
    author = author_data()
    source = json.loads(TARGET.read_text())
    h = {tuple(row['six_word']): row['three_cap_colors'][0]
         for row in source['word_factorization']['rows']}
    assert set(h) == set(product((1, 2, 3), repeat=6))
    for row in source['word_factorization']['rows']:
        assert len(set(row['three_cap_colors'])) == 1
    parity_words = [w for w in h if all(w.count(c) % 2 == 0 for c in (1, 2, 3))]
    orbit_representatives = sorted({canonical(w) for w in parity_words})
    assert len(orbit_representatives) == 31
    for w in h:
        if w not in parity_words:
            assert h[w] == 0
        for perm in permutations((1, 2, 3)):
            assert h[tuple(perm[c - 1] for c in w)] == h[w]
    target = {abc(w): h[w] for w in orbit_representatives}
    assert sum(value > 0 for value in h.values()) == 81
    assert sum(h.values()) == 87
    forbidden = sorted(w for w, count in target.items() if count == 0)
    assert len(forbidden) == 17
    assert sum(count > 0 for count in target.values()) == 14
    rows = []
    for ray in author['rays']:
        counts = ray['canonical_counts']
        assert set(counts) <= set(target)
        witnesses = [w for w in forbidden if counts.get(w, 0) > 0]
        value = sum(counts.get(w, 0) for w in forbidden)
        assert value > 0 and witnesses
        rows.append(dict(ray_index=ray['index'], functional_value=value,
                         positive_forbidden_coordinates=[dict(word=w, count=counts[w])
                                                         for w in witnesses]))
    return dict(
        conclusion='The fixed h is outside the published cone K6 at every positive scale; general plane-source realizability remains OPEN.',
        evidence_layer='Exact finite integer replay of imported 102 ray declarations and the target; not an all-source theorem.',
        provenance=author['provenance'],
        sources_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                       for p in (AUTHOR, PREFIX, TARGET, Path(__file__))},
        target=dict(all_literal_word_coordinates=729, parity_orbit_coordinates=31,
                    positive_literal_words=81, literal_word_mass=87,
                    canonical_orbit_counts=target),
        separation=dict(functional='Sum of the 17 listed canonical orbit coordinates.',
                        functional_coordinates=forbidden, functional_target_value=0,
                        published_K6_rays=102,
                        minimum_ray_functional_value=min(row['functional_value'] for row in rows),
                        ray_witnesses=rows,
                        proof='Every nonzero nonnegative combination of the 102 rays has strictly positive functional; every positive multiple of h has value zero.'),
        external_paper_implication=dict(
            scope='Conditional on the published computer-assisted Lemma 12 and paper Lemmas 13-19, without independently replaying their full closure certificate.',
            statements=['Any actual plane six-leaf source with n a positive multiple of h is outside K6.',
                        'Lemma 13 gives a seven-pole outside K7 with at most one fewer vertex in the closed-boundary convention.',
                        'An extremal seven-pole minor has at least 28 vertices by Lemma 19.',
                        'Consequently the original six-leaf source has at least 28 cubic interior vertices.'],
            cubic_vertex_lower_bound=28,
            closure_certificate_replayed=False),
        limitations=['K6 is not asserted to contain every plane six-leaf source.',
                     'The whole 208-ray B6 cone was not enumerated or imported.',
                     'The full multi-gigabyte author closure certificate was not downloaded or replayed.',
                     'No actual target source or full counterexample is supplied.',
                     'No r2 exclusion or new forced-zero coordinate follows.'],
        outcomes=dict(target_source_existence='OPEN', universal_marked_bond_existence='OPEN',
                      r2_exclusion='OPEN', new_forced_zero_coordinates=0, new_Lean=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = json.loads(json.dumps(report(), sort_keys=True))
    if args.check:
        assert json.loads(args.check.read_text()) == result
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(published_K6_rays=102, parity_orbits=31,
                         target_zero_orbits=17, functional_target_value=0,
                         minimum_ray_functional_value=result['separation']['minimum_ray_functional_value'],
                         target_in_K6=False, full_author_closure_replayed=False,
                         target_source_existence='OPEN', new_forced_zero_coordinates=0), sort_keys=True))


if __name__ == '__main__':
    main()
