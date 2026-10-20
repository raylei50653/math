# C. Fixed controls for larger cuts and complete component charges

BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.
The independent computation reads the frozen previous C checker and four
complete controls. It writes only this `C/` directory. The authoritative
certificate is [`certificate.json.gz`](certificate.json.gz), replayed by
[`check.py`](check.py). These are fixed weak plane controls, never original
minimum R6 sources. Source realizability remains `not triggered`.

## 1. What the four frozen controls actually test

None of the three literal controls has both safe facial repairs blocked.
Each admits the immediate `(5,6)` four-cycle switch, with no attached
subtree and a degree-four safe rim. That rim degree cannot occur in the
original source. The nonliteral weak no-repair control has an exterior
blocker on `(4,5)` and a successful `(5,6)` walk which changes g, so the
second walk is not joint admissible.

All 160 complete perfect matchings of these controls are replayed. Every
original rotation, literal mark, complete complement circle and empty
marked matching fibre is retained.

## 2. Three targeted extensions

Three controls are obtained by inserting a small fixed set of vertices and
specified cap/exterior chords into existing O circles. There is no scan over
possible sources or unbounded search over embeddings.

| New control | Safe `(4,5)` failure | Safe `(5,6)` failure | PM | even101 | even110 |
| --- | --- | --- | --- | --- | --- |
| `literal_both_outside_blocked` | exterior chord | exterior chord | 56 | 5 | 1 |
| `literal_parity_and_outside_blocked` | one even skipped arc | exterior chord | 27 | 3 | 0 |
| `literal_both_parity_blocked` | one even skipped arc | one even skipped arc | 32 | 3 | 0 |

In each of these complete fixed graphs, **no singleton primal cut gives any
joint even repair**. The minimum number of flipped primal vertices, modulo
complement, is exactly two. The following are actual same-graph witnesses:

| Control | Full matching row | Primal pair | Original degrees | Actual M-alternating boundary | Full new complement |
| --- | --- | --- | --- | --- | --- |
| exterior/exterior | 40 | `{6,9}` | `5,3` | `(5,6,13,14,12,11)` | one 22-cycle |
| parity/exterior | 20 | `{6,10}` | `5,3` | `(5,6,15,16,14,13)` | one 20-cycle |
| parity/parity | 23 | `{6,11}` | `6,4` | `(5,6,17,18,15,16,14,13)` | one 22-cycle |

The vertex numbers in the primal-pair column are the face indices of the
fixed original dual rotation. The boundary cycles use original D vertex
numbers. All three pairs avoid e,f,g and give N101.

In the first two rows neither selected vertex has a legal singleton
matching flip. Their blocker counts are `(1,1)`. The last row has counts
`(0,2)`: its safe singleton is legal but leaves two complete odd cycles.
The two-face switch absorbs its odd three-degree child component into the
other selected vertex's new component.

The selected partner degrees `3,3,4` violate the original source's partner
degree restriction. Every new control has triangular dual faces. In
addition, `literal_both_outside_blocked` and frozen
`literal_safe_cap_disappearance` each have two pairs of parallel primal
edges; the certificate records these explicitly. They are not simple
four-connected source triangulations. The first new control has ten
labelled e-normalized Tait rows with all three marked colours distinct;
the other two have none. Neither fact promotes any control to a source.

## 3. A local 5/5/5 obstruction already occurs

In `literal_both_outside_blocked`, the two safe rims are primal vertices
`A=5,B=6`; their outer common triangle has third vertex `tau=8`.
All three original degrees equal five. The complete original tree is
`T={7,8,9,12}`. Removing tau leaves

* `{7,12}`, original degree sum 13, charge one;
* `{9}`, original degree sum 3, charge one.

The actual pairs `{5,8}` and `{6,8}` pass their full rotation tests and
preserve all marks. They produce matching rows 34 and 37, respectively.
Their **complete** complement lengths are `19+3` and `11+11`, so both
retain two odd circles. Each leaves precisely the opposite odd T branch
untouched. The alternative pair `{6,9}` above repairs the same graph.

This is a finite calibration of the coupled 5/5/5 odd/odd branch in
[B §7](../B/PROOF.md#7-a-coupled-degree-five-configuration-has-one-exact-parity-blocker).
It does not realize the full source premises: other vertices have too
small a degree and the original primal graph has parallel edges.

## 4. Exact graph-level checker

For each complete perfect matching N, the checker reconstructs the unique
primal cut `X` modulo complement with `N=M triangle delta(X)*`.
It separately enumerates **all** primal subsets with vertex 0 fixed
outside X, computes the cut in the original graph, and checks the degree
at every dual vertex. Invalid subsets create degree-three vertices; every
valid subset maps bijectively to one of the independently enumerated
complete perfect matchings.

For each complete row, the checker also reconstructs every complete
component of `P_N=(V(J),N*)`, retaining original degrees, component
vertices, degree sums and charges. The complete complement circles define
a region tree. For each individual circle, its recorded length parity
equals the total original degree charge on either full shore of the
corresponding tree edge. Thus every one of the 275 rows satisfies the
exact equivalence

`all complete complement circles even`

`iff every complete P_N component has even original degree sum`.

This test includes outer and nested circles. A global even sum alone
would pass every row and has no repair authority.

The checker also independently tests all nine eligible literal
safe-rim/T-neighbour pairs in the seven fixed controls. Actual bad
corners, the shared triangle positions, every residual component of
`T-tau` and `U0-rho`, and its actual touched/untouched adjacency are
retained. Whenever the pair is admissible, the untouched-component
criterion agrees with the complete complement result. This checks the
algebraic mechanism of [A](../A/PROOF.md); it does not trigger its source
degree or simplicity premises.

Complete replay totals:

* 7 fixed controls and 275 complete perfect matchings;
* 16,384 primal cut subsets modulo complement, including every rejection;
* 224 five-spoke mask fibres and 56 marked matching fibres, including empties;
* 9 actual safe adjacent-pair tests with full residual components.

The cut fibre array uses index `k` for
`X={i+1 : bit i of k is 1}`; `null` is an invalid cut, and an integer is
the unique complete matching row. All entries are serialized, rather than
replacing rejected cuts with a count.

## 5. Validation and storage

[`VERIFICATION.json`](VERIFICATION.json) records successful normal and
`PYTHONHASHSEED=17` replays. Nine negative checks reject:

* a missing empty spoke fibre;
* an omitted complete outer odd circle;
* an omitted untouched odd component;
* a changed component charge;
* a changed full-shore charge;
* an invented admissible cut fibre;
* a changed literal mark;
* a falsely promoted source-realizability authority;
* an attempt to overwrite an existing certificate.

Certificates and mutants use deterministic gzip with `mtime=0`. The
authoritative compressed certificate is 45,597 bytes; its exact
uncompressed bytes and SHA256 are recorded in the verification receipt.
The pre-enrichment initial certificate is preserved byte-for-byte as
`certificate-initial.json.gz`; its large plain duplicate was removed.
All certificate writes are exclusive creation. The checker reads either
plain JSON or gzip and never changes its input.

No Lean theorem, universal repair, source exclusion, smaller bad source,
or joint positivity is established by these controls. This directory
contains no commit or push action.
