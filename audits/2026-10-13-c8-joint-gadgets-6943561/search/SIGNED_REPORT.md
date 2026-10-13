# Boundary-chord equality and difference caps

Every boundary chord of each frozen triangulated C8 cap is independently
labelled `Eq` or `Diff`; all C8 edges, private edges, and spokes retain `Diff`.
The `Eq` chords are simultaneously contracted. A signature is admitted exactly
when its equality classes collapse no C8 edge and no `Diff` chord. The chords
are embedded without crossings, so these contractions are simultaneous planar
operations. Applying them to the source side requires the frozen induced-C8
contract, to ensure no unrecorded source edge becomes a loop.

If `d` boundary vertices are saved by contraction and the cap has `h` private
vertices, the resulting joint graph uses `k+h-d` vertices. Here `h<=5`, so every
admitted signature lies within the `k+5` colourability budget. Each compatible
row is still a literal full row on the same eight named original vertices;
quotient classes never replace those names in the certificate.

The complete signed-chord grammar built on the 334,512 frozen caps contains:

| Private vertices | Valid signed caps, with duplicates |
| ---: | ---: |
| 0 | 156 |
| 1 | 975 |
| 2 | 6,639 |
| 3 | 44,578 |
| 4 | 312,018 |
| 5 | 2,235,092 |
| Total | 2,599,458 |

All 16 named boundary identifications and eight residual queries give
332,730,624 tests. **No signed cap rejects any upper support.** Minimum
intersection sizes, already attained with no private vertex, are:

| Query | Minimum |
| --- | ---: |
| c04-941, c07-941 | 2 |
| c15-933, c18-933 | 1 |
| c15-941, c20-941 | 3 |
| c18-941, c30-941 | 2 |

Singleton intersections force precisely these original literal rows:

* `c15-933`: indices `19, 33, 188, 249`.
* `c18-933`: indices `44, 67, 157, 188`.

The zero-private-vertex subfamily already forces all of them. The adjacent
private-vertex extensions introduce no additional singleton-forced row.
These are separate nonempty-fibre obligations on the same unknown source;
they do not assert that one colouring satisfies different signatures at once.

An initial support-only discovery run in this new search directory was
superseded by the present full-fibre certificate before sealing. Its output is
not treated as a separately retained certificate. The final producer uses
exclusive creation for certificate files; replay uses `--check`.

[SIGNED_RESULTS.json](SIGNED_RESULTS.json) provides raw hashes, per-size
statistics, exact scope, and encodings. Full fibres are retained as follows:

1. Ignore all boundary chords while enumerating each graph's 274 literal
   private-colouring fibres.
2. Store the resulting fibre counts and all private tuples in
   `signed_data/hN.counts.u16le.gz` and `signed_data/hN.tuples.u16le.gz`, using
   the [pure-cap encoding](RESULTS.json).
3. Store one equality signature byte per graph and row in
   `signed_data/hN.signatures.u8.gz`. Its bit `j` says that the endpoints of the
   `j`th lexicographically ordered boundary chord have equal colours.
4. The full fibre of an admitted signature is exactly that stored raw fibre
   when the signature byte agrees, and the empty fibre otherwise.

This lossless partition represents 712,251,492 signed fibres, of which
643,620,314 are empty, and all 204,250,566 private lifts. It neither combines
marginals nor drops empty fibres. The compressed signed data occupy about
69 MiB. [Eight named witnesses](signed_witnesses.json.gz) record explicit
Eq/Diff edges, contraction classes, the vertex savings, and all 274 full fibres
for the singleton incidences. The [witness checker](signed_witnesses.py) tests
them directly in their actual query names and rejects corrupted lifts/names.

```bash
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-joint-gadgets-6943561/search/signed_run.py --check
python3 -B audits/2026-10-13-c8-joint-gadgets-6943561/search/signed_witnesses.py --check
```

The parent audit's independent signed checker enumerates private assignments
first, computes compatible boundary-row bitsets, reconstructs equality closure
without the producer's DSU, and compares every raw count, tuple, signature,
full support, and aggregate. Its receipts are in the parent review package.

This is the complete stated signed-chord grammar on the frozen `h<=5` caps.
It is **not** a complete enumeration of all gadgets with net cost `h-d<=5`:
larger caps financed by boundary identifications, equality paths through
private vertices, and restrictions on other faces remain outside this search.
All eight necessary-support residuals and their actual source realizability
remain OPEN. No four-colour theorem is assumed and no Lean theorem is added.
