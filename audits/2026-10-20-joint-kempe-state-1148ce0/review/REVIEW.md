# Independent review: joint Kempe state

**PASS within the stated scope.** The six boundary partitions of one coloring,
together with its literal boundary colors, do not determine the next such state
under a boundary-rooted Kempe action. The counterexample is one genuine embedded
C5 disk, not a combination of different graphs, different color frames, or
independently feasible color-pair data.

This review owns only `review/`. It reads the frozen catalogue and the supplied
experiment/refinement artifacts, but imports no code from the experiment,
root refinement, or the project's earlier Kempe scripts.

Artifact custody has a separate limit. The experiment agent reports a transient
v1-to-v2 edit and restoration in [CUSTODY.md](../experiment/CUSTODY.md).
The independent reviewer has no pre-edit checksum establishing the original
v1 bytes, so this review does not certify that the restored v1 is byte-identical
to the first version. The current certificate's mathematics is independently
reconstructed below; the separately named transient-v2 artifacts are
reconstructions, not captured original v2 bytes. Neither reconstructed v2 file
is used by these review checkers. The frozen catalogue hash is checked directly.

## Independent literal and geometric certificate

[check_collision.py](check_collision.py) reads the frozen cell `95` with its
SHA256 pinned, adds the five original cycle edges, and independently constructs
all six maximal two-color component systems by repeated edge closure. It checks
proper full colorings, literal boundary signatures, the same action
`(1,2,root=1)`, both complete swapped components, and both target systems.
Its [certificate](collision_certificate.json) was created exclusively; `check`
reconstructs it in memory and does not write.

The full sources are `01012132` and `01012233`; the selected maximal components
are `{1,5,7}` and `{1}`. Both source signatures agree. The target words are
`02012231` and `02012233`; their `01` and `23` boundary partitions differ.
The complete fixed `01012` fibre contains exactly
`01012132`, `01012133`, and `01012233`.

The independent straight-line embedding uses the strictly convex ordered rim

```
0=(0,0), 1=(4,0), 2=(6,3), 3=(3,6), 4=(0,4).
```

Solving the interior barycentric equations with exact rational arithmetic gives

```
5=(206/71,127/71), 6=(169/71,210/71), 7=(229/71,85/71).
```

The checker verifies every barycentric equation, distinct vertices, strict
interiority, absence of nonincident segment intersections or vertices on edges,
the nine positive oriented triangular faces, the complete edge incidences,
connected path links at boundary vertices, connected cycle links at interior
vertices, and disk Euler characteristic. The positive twice-face areas are

```
(340,335,780,560,676,307,302,163,158)/71;
```

their sum is the outer polygon's twice-area `51`. Thus planarity and the
specified C5 outer boundary have an exact geometric witness, not merely a
catalogue label.

Every check run rejects ten in-memory corruptions: missing action, malformed
integer, improper source, nonmaximal component, forged boundary partition,
different root action, partial swap, coincident vertices, an outside vertex,
and reversed face orientation. These are checked through the same certificate
validator used for the positive certificate.

## Independent finite replay and refinement

[check_cross.py](check_cross.py) uses sequential vertex coloring with exact
backtracking and repeated edge closure. It compares every complete fibre and
every reported row statistic of all 132 fixed catalogue graphs with the
experiment certificate, including all empty fibres. The results agree:

| Quantity | Independently verified |
| --- | ---: |
| Fixed catalogue graphs | 132 |
| Prescribed literal boundary fibres | 1,320 |
| Empty fibres | 405 |
| Full lifts | 1,810 |
| Joint states, separately per graph | 1,280 |
| Enabled rooted actions | 27,150 |
| Ambiguous joint-state/action pairs | 1,229 |
| Graphs with a collision | 90 |

No planarity claim for all 132 representatives is derived by this cross-check;
the explicit exact embedding above is for the counterexample cell `95`.
The finite totals are properties of the saved graph representatives.

For the complete literal action graph of cell `95`, an independent unrestricted
coloring enumeration gives `264` full proper colorings and `3,960` enabled
rooted actions. All action roots remain in the original five boundary vertices
even when extra observations are retained. Moore refinement gives:

```
joint signature:       192 -> 240 -> 264 (stable)
boundary colors alone: 144 -> 192 -> 240 -> 264 (stable).
```

The joint partition exactly equals the boundary-observation partition through
one action. The stable partition consists of singleton full colorings.

Adding private contact `5` or private contact `7` to both the observed colors
and all six restricted partitions gives `264` singleton states immediately.
Adding only `6` leaves `192` states and `96` conflicting state/action pairs.
All eight subsets of `{5,6,7}` were checked and match the root certificate.
Consequently the successful one-pin observations encode the full coloring on
this fixed graph; this is not a demonstrated state compression or a general
one-pin bound.

The same literal sources are separated by the two-action word

```
(1,2,root=1), then (0,1,root=0):

01012132 -> 02012231 -> 12102230
01012233 -> 02012233 -> 12012233.
```

The first boundary outputs both equal `02012`. The second outputs are `12102`
and `12012`. This is an explicit boundary-observation failure at depth two,
not only an internal disagreement between intermediate partitions.
The independent trace and all fixed-graph refinement counts are retained in
[cross_certificate.json](cross_certificate.json).

## Theory and source-contract review

The depth-one equivalence in [theory/REPORT.md](../theory/REPORT.md) is correct
for the declared unrestricted boundary-rooted action grammar. The joint
signature determines each enabled action's changed boundary block. Conversely,
comparing each action's literal output with the original boundary recovers
exactly that block, since swapping distinct colors changes every vertex in it.
This reconstructs all six boundary partitions, including empty partitions.
Filtering out actions that leave a fixed target fibre invalidates that
reconstruction argument; the theory explicitly states this restriction.

The action-marked residual-component/attachment quotient is sufficient for
one-step mixed-pair reconstruction. Residual components must be formed after
deletion, new same-color vertices cannot have edges among themselves in a
proper coloring, and maximality of the exchanged component prohibits edges
to an opposite-color vertex outside it. The stated attachments therefore
account for all remaining new edges. The descriptor is not claimed to update
itself after a second action; this distinction is essential.

The J1 `S/M` and `I/II/III` tables match the frozen continuation and geometry
reports, including placement of the original `v,w` identities, the
three-edge W5 exception, and simultaneous same-coloring path requirements.
The six joint cells are only necessary classification indices and may be empty.
The S-layer exchange need not preserve `I/II/III`, because those are mixed
partitions for that action. Hidden-component actions remain relevant to full
Kempe reachability even when boundary colors stay fixed.

The new counterexample is not a realization of the full r6/941/J1 source
contract. Those source hypotheses are **not triggered**, and J1's two remaining
fibres stay OPEN. Neither the finite replay nor stable fixed-graph refinement
provides source exclusion, arbitrary-disk state closure, a smaller-bad
construction, a reconstruction-cost decrease, or a new Lean theorem.
The parent [REPORT.md](../REPORT.md) preserves these scope boundaries, limits
the depth/refinement numbers to cell `95`, and makes no claim that its
eight-vertex witness has minimum possible size.

## Reproduction

```
python3 -B audits/2026-10-20-joint-kempe-state-1148ce0/review/check_collision.py check
python3 -B audits/2026-10-20-joint-kempe-state-1148ce0/review/check_cross.py check
```

Both run read-only. Normal deterministic replay and `PYTHONHASHSEED=17` replay
are recorded in [verification-final.json](verification-final.json), with final
checker hashes and unchanged certificate bytes. The earlier
[verification.json](verification.json) is retained as its original run record.
Their `build` modes use exclusive creation and cannot overwrite an existing
saved certificate. No commit or push was performed.
