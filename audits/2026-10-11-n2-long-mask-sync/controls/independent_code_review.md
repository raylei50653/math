# Independent review of the high-contact and synchrony checkers

Review scope: read-only inspection of the two bounded new checkers, their
retained artifacts and replay/corruption receipts, and the arbitrary-size
mask theorem in `../synchrony/REPORT.md`. Only this review file was written.
No broad checks, source generation, shared-document changes, or publication
were performed for this review.

**Decision:** the final reviewed checkers preserve their stated bounded
semantics and evidence boundaries. The low-contact exact-arc mask theorem
has no material gap in the reconstructed block-tree and palette argument.
One artifact-overwrite defect found during review was fixed by the owning
worker; no unresolved finding remains in the reviewed versions.

## 1. Exact reviewed versions

| File | Bytes | SHA256 |
| --- | ---: | --- |
| `../high-contact/checker.py` | 8,658 | `4e9cd458e0b9a86ccd7298d09ad1d0a4d0415c07ab7ba3cdf3068bc0c8d3dadc` |
| `../synchrony/signatures.py` | 3,059 | `a01d4cf6043e7ed8e09c72c1507994275deb38b742d9ce018bdb484c31eda34a` |
| `../synchrony/REPORT.md` | 13,531 | `b3d79698c0c08f92a69f8b2a2e5c3993641d23bde971372880c6fcc57f08ac0e` |

The parent BASE has exactly thirteen input entries. Both checkers verify
every frozen input's byte count and SHA256 before constructing their
payloads. The reviewed source artifacts have the byte counts and hashes
reported by their receipts:

* High-contact: 228,606 bytes,
  `f91d8a12bdf4b4c07c2ff64b6c345f292942668ad00af224ab4b71cdaa7326b7`.
* Synchrony: 9,026 bytes,
  `a41e0bc9afb5c20c70336321917065cbc1e37dd8998244d1f937f6562e5b03c5`.

These hashes were independently read from the current files during review.
The normal, seed17 and corruption executions were inspected through the
retained `verification.json` receipts; this review did not repeat those
already successful bounded executions.

## 2. High-contact complete-fibre semantics

`fibre_record` keeps the named original vertex order, all original region
edges, literal boundary attachments and ordered root contacts. Its DFS
assigns every original local vertex and rejects conflicts with every already
assigned neighbor. Previously unassigned neighbors are checked when their
turn arrives. The recursive assignment cleanup introduces no stale colors.
Thus the stored cells contain complete local tuples, rather than counts,
contact marginals, or independently normalized palettes.

Both named controls use disjoint boundary, root and local coordinate sets,
have no root-root edge or root-boundary spoke in their local region, and use
the proper frozen boundary table. Accordingly every ambient root-pin cell
is a valid local list problem. All ten rows and all sixteen ordered cells
are retained, including the forty empty cells in the two controls. The
selected diagonal is cell 15 in the explicit lexicographic ordered pin list.
The named rows are selected by exact beta tuple (`01212`, `01202`, `01021`),
so the artifact's numeric row ordering cannot change their labels.

The degree-four, distinct-contact and H-degree-two attachment assertions
match the two literal named graphs. The four-contact path has mask
`{0,1,3}` and contacts at its two internal cutpoints; it calibrates the
stated local counterexample and does not contradict the contact-at-leaves
lemma. The four-leaf tree has empty mask and every contact is an original
C leaf. Neither control supplies full target Sigma, criticality, target
degree-five roots, or a source rotation, and the report explicitly preserves
those limits.

`minor_control` verifies pairwise disjoint connected original bags and an
original edge for all ten bag pairs. This is the correct uncontracted K5
minor certificate obligation; it makes no coloring or Sigma claim about
the minor.

Artifact generation uses exclusive `open('xb')`; `--check` recomputes the
whole payload and compares exact bytes. `--artifact` permits retaining a
corrupt copy without changing primary evidence. The retained corruption
receipt exits 1 with `artifact mismatch`. No false full-fibre or target
source claim was found.

## 3. Synchrony signatures and resolved generation defect

`signatures.py` computes equality and inequality masks directly on the same
literal five-point boundary frame. It tests disjointness of the two actual
arc-edge ID sets, preserving their common source coordinates. The five
unordered disjoint pairs, twenty Eq/Diff unions, ten mixed-type common
escapes, two Eq/Eq covers and five Diff/Diff covers agree with the
independent signature and attachment tables in this controls directory.
The payload explicitly states that it supplies no local fibres or source
realizability; the paper report separately refers to complete local controls.

The first inspected generation path used `artifact.write_bytes(raw)` and
would overwrite retained evidence on rerun. This was reported to the root
and owning worker. The final inspected version instead uses
`with artifact.open('xb')`, at lines 65–66, and supports a separate
`--artifact` path. Its check mode compares the entire recomputed byte
payload. The retained corrupted-copy receipt exits 1 on `artifact mismatch`.
The overwrite defect is therefore resolved in the exact reviewed version.
The fix changes only the CLI write protection; the saved payload bytes and
SHA256 remain unchanged. No replacement generation or primary-artifact
mutation was requested or performed by this reviewer.

## 4. Independent reconstruction of the paper mask theorem

The theorem's premises retain complete degree-four original vertices,
distinct contacts, exact three-point support on one original two-edge arc,
the leaf-contact and ordinary-private-cycle bounds, and the H-degree-two
attachment injection. The degree-list theorem is an explicit adopted
external dependency rather than a new checker claim.

At a refused diagonal row, tight palettes give D exactly at noncontacts.
The two available literal boundary edges and attachment injection cap
H-degree-two vertices at two. The contact budget bounds every odd cycle
by four vertices, hence forces triangles. Three block-tree leaves would
require three distinct contact bridge endpoints and thus three different
boundary-edge attachments; two triangle leaves would require at least four
contacts. Therefore only two leaves remain. The additional attachment
capacity controls arbitrary bridge chains and ordinary triangles, leaving
the four stated refusing shapes with 2, 3, 5 and 6 original vertices.

I reconstructed the individual palettes:

* The contact bridge rejects exactly when its two actual edge T colors
  coincide, giving Eq.
* The all-contact path can reject only when its two leaf palettes differ
  and its original middle attachment is the arc middle point, giving Diff.
* The five-point triangle with a two-bridge tail forces the tail palettes
  to be `{D,T}`, giving Eq. The report correctly allows both all-middle
  triangle attachments and attachments entirely to the two arc endpoints.
* The six-point two-triangle shape forces the ordinary triangle palette
  `{D,T(f)}` to be disjoint from the leaf palette `T(e)`. A refused Diff row
  fixes the actual middle attachment and opposite-endpoint contacts, so
  every Diff row, and exactly those rows, satisfies the same obstruction.

Thus the exact masks are empty, Eq or Diff, rather than arbitrary subsets
of those types. The sufficiency follows from the same full degree-list
palette obstruction, while necessity follows from the block-tree case
split. The 800 finite attachment controls calibrate these shapes but are
not used to infer the unbounded case split.

The same-row source corollary retains the original unary and mixed full
lifts, the original short lift, common `(D,D)` pins, root spokes and free
isolated factors. Its seven same-type templates are explicitly necessary
templates rather than seven source realizations. General high-contact
pieces, full same-row/off-diagonal joints, full parent N2 and E-ARC2 remain
open. No material paper gap or false closure claim was found in this scope.
