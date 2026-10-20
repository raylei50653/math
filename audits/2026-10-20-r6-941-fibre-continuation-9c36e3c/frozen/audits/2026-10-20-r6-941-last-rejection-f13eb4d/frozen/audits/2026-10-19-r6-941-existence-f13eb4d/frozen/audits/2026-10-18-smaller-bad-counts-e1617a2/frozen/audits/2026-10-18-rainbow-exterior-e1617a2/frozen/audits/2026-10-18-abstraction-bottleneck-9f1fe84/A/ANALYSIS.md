# A. Bottleneck diagnosis and a weaker certificate for preserving badness

BASE `9f1fe84f73aabfa87a33d28754633bae6bf0b707`; 2026-10-18.
This is an independent analysis and a finite catalogue certificate. No source
reduction, new source exclusion, ordinary-matching theorem, or Lean theorem is
claimed. The root frozen inputs are unchanged. Extra BASE inputs and their
SHA-256 hashes are in [INPUTS.json](INPUTS.json); the executable finite result is
[check_signed_interface.py](check_signed_interface.py).

## 1. The current bottleneck is not ordinary matching

The frozen `docs/c5_kempe_guide.md:219–237` records that the last ordinary101
Tutte obstruction was excluded at arbitrary size. Thus `P101 != empty`, and the
ordinary union `P101 union P110` is nonempty. The remaining target is an element
of that union whose **entire** complementary 2-factor is even, equivalently
`omega_e=0` or `W110+W101>0`. It is unnecessary to prove both W counts positive.
The same guide at lines 227–230 already records XOR-preserving batch-exchange
connectivity; connectivity without a good endpoint is not a new route to
positivity.

There is a real obstruction to the latest sufficient condition, not merely a
missing estimate. For a fixed actual M with exactly two complete complement
cycles, both odd, every even-complement reference R has
`D-(M intersect R)` connected. Its distinguished region is the entire graph,
so minimizing that region by changing R cannot progress. This follows from
complete-region parity, independently of cap details; see frozen
`audits/2026-10-17-r6-two-cycle-cap-3d325d7/PROOF.md:44–68`.

Two further negative controls identify the same loss of information in earlier
and current work:

* A safe switch can delete the visible seven-cycle while changing complete
  complement lengths `(7,8,5)` to `(15,5)`, preserving oddness two. See frozen
  `audits/2026-10-17-r6-seven-five-repair-5b9a7b3/A/PROOF.md:211–230`.
* Static complete boundary relation does not determine future geometric
  legality, or the lift used by the next step. Frozen
  `docs/c5_phase_b_common_lemmas.md:370–384` gives the actual same-relation
  different-disk-continuation example, the R511 five-port obstruction, and the
  intermediate-lift mismatch. These are distinct failures; preserving a larger
  collection of marginal observations does not resolve them.

Therefore the common bottleneck is **a proposed local improvement has not been
shown to lift to the actual objective on one completed source**. In matching it
is full oddness with literal edge constraints; in source replacement it is a
legal smaller graph still outside the finite catalogue; in dynamic repair it
is a composable path from one concrete lift.

## 2. Which hypotheses can be weakened

Some restrictions are structural safeguards: ordered contacts, joint fibres,
actual attachments, sealed private vertices, and one candidate graph cannot be
dropped when proving a replacement. Frozen `docs/c5_common_language.md:15–26`
and `docs/c5_phase_b_common_lemmas.md:303–389` document actual failures when
these are omitted.

Other restrictions are consequences of choosing a stronger preservation goal
than the minimal-counterexample argument needs. For a contradiction to global
minimality, the replacement need not retain the original exact Sigma, mask319,
r=6, original degrees, or the seven-cap shape. It needs to be a legitimate disk
C5 source outside K132 with strictly fewer completed interior vertices.
The authority is [no4ct handoff](frozen/docs/tasks/c5_no4ct_handoff.md), lines
92–114: minimum k is over **all** sources with `Sigma(G) notin K`, not over a
fixed mask. The support classification is a theorem about the minimum source,
not a condition that every smaller counterexample must retain.

K132 here means 132 distinct ordered ten-bit relations, with 24 D5 classes,
realized in the complete `k<=5` catalogue. It is neither 132 graphs with possibly
duplicate masks nor 39 masks. The frozen [catalogue](frozen/artifacts/c5_cells/cells.json)
has 132 distinct `cells` keys; [atlas](frozen/docs/c5_combinatorial_atlas.md),
lines 17–29 and 167–175, distinguishes them from arbitrary raw masks, necessary
screens, and two-sided intersections. No arbitrary-size completeness assertion
about K132 is used here: being outside it is precisely the badness predicate.

## 3. A four-query certificate, strictly weaker than exact Sigma preservation

Use the fixed ordered row list

`01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`.

The following certificate is shared by the three normalized minimum-source
supports 932, 933, and 941:

| Query | Required result on one completed candidate graph |
| --- | --- |
| 01232 | Has a full proper extension |
| 01021 | Has no full proper extension |
| 01202 | Has no full proper extension |
| 01212 | Has no full proper extension |

In bits it is `Sigma & 594 = 512`. The other six observations are free.

**Finite catalogue lemma.** None of the 132 K132 masks satisfies this condition.
Exactly 64 raw ten-bit masks satisfy it. Thus any legal disk C5 graph satisfying
the condition lies outside K132.

The checker independently examines all `3 * 1024` observation scopes, rather
than only the proposed four. For target 932 there are five minimum four-query
scopes; for 933 there are two; for 941 the displayed scope is unique. Every one
of the 176 scopes with at most three observations agrees with a catalogue mask,
for each of the three targets. All 528 countermodels are in
[signed_interface_certificate.json](signed_interface_certificate.json).
This is minimum **number of observed boundary rows**, not minimum interface
arity, minimum number of vertices, or a minimum among all conceivable invariants.

Removing any one of the four queries fails even for this common certificate:

| Removed query | One K132 countermodel satisfying the other three |
| --- | --- |
| reject 01021 | 774 |
| reject 01202 | 564 |
| reject 01212 | 960 |
| accept 01232 | 165 |

The four-query combination is not historically new. The frozen
[W5 support report](frozen/docs/c5_w5_three_color_support.md), lines 130–135,
already proves that a sound small quotient branch preserving 01232 must leak one
of the three rejected rows. The contribution here is its explicit use as a
weaker preservation target, its catalogue-wide minimality certificate, and the
following general transfer theorem. The old no-go prevents presenting the five
existing W5 quotient branches as a solution to this new target.

### 3.1 Signed contextual replacement theorem

Let G be a graph with a fixed ordered boundary B and a sealed decomposition
`G=E union P` whose overlap is exactly a named interface I. There are no extra
private identifications or cross edges. Let P' use the same named I and fresh
private vertices; put `G'=E union P'`. All data use one literal colour frame.
For a boundary row q, let `E_q` be the complete relation on I induced by E with
q pinned, and let `R_q` and `R'_q` be the corresponding complete interface
relations induced by P and P'. Shared B positions are included in the common
pinning, not independently re-coloured.

Suppose G has an accepted row a and rejected rows in a set Z. It suffices that:

1. there is an actual tuple `t in E_a intersect R_a` with `t in R'_a`;
2. for every `z in Z`,
   `E_z intersect R'_z subseteq E_z intersect R_z`.

Then G' accepts a and rejects every row in Z.

**Proof.** The tuple t has an exterior lift and a P' lift that agree on all
shared vertices; fresh private vertices and absence of extra cross edges let
them glue to a full G' colouring. For z, the original rejection says
`E_z intersect R_z=empty`; condition 2 makes the new intersection empty. Full
extension to G' would give a tuple in that intersection, a contradiction. QED.

This is a one-sided criterion: one actual accepted witness is retained, while
the three rejected queries forbid new compatible tuples. Equality of complete
piece relations is unnecessary; so is preservation of every accepted witness,
colouring counts, or the other six boundary rows. A stronger but easier local
test is `R'_z subseteq R_z` for each rejected z. The contextual inclusion above
is weaker still, because tuples impossible in the actual exterior are irrelevant.

The relations used to prove the theorem must nevertheless be full joint
relations on I, with empty fibres, actual attachments, and all shared identities.
Testing acceptance of each contact separately or substituting a different P'
for each query does not meet the theorem. Different boundary queries naturally
have different colourings; their common object is the **same candidate graph**,
not one colouring that simultaneously has four different boundary values.

### 3.2 Strict smaller-bad-source corollary

Let G be the actual global k-minimum source outside K132, normalized to one of
932, 933, 941. If a construction produces a legitimate disk C5 graph G' satisfying
the four-query certificate and `k(G')<k(G)`, the finite catalogue lemma makes
G' a smaller source outside K132, contradicting minimality.

The new graph may leave the r=6 subclass and need not have Sigma equal to G.
Its legal disk boundary, finite/simple graph conditions, specified ordered rows,
and strict **completed-source** size must be proved. Where a construction uses
a partial quotient with q vertices and restoration cost c, it must show
`k(G') <= q+c < k(G)`. An apparent saving before restoring hubs or the boundary
is insufficient. The current r6 chain explicitly still restores the old bound
`k+5`; see frozen `docs/c5_kempe_guide.md:225–237`. This audit constructs no G'.

This yields a sharper next obligation than “find an equivalent smaller
representative”: find a legal smaller candidate retaining one actual 01232
lift and preventing new complete lifts for the three rejected rows. Geometry
and completed cost remain essential, but six row equalities and all colouring
count equalities can be removed from the replacement specification.

## 4. A matching/repair abstraction should also be one-sided

Phase B's full action bisimulation is sufficient for every future observation,
but stronger than necessary for an existence proof. Let X be actual states of
one source, S abstract states, and `L(s) subseteq X` their permitted concrete
lifts. An abstract proof strategy suffices if every chosen abstract step
`s -> t` can be realized from **each current lift** in L(s) by an allowed finite
concrete path ending in L(t), and abstract success is sound for all terminal
lifts. Induction along the chosen path gives one composable concrete success
path. No reverse matching of unused concrete steps is needed.

If finite termination is claimed, add a well-founded rank that decreases along
the abstract strategy. For source reductions the rank must include completed
size and reconstruction costs. For same-D matching repair there is zero graph
reconstruction cost, but the terminal assertion remains full even complement
and literal `e in M, f xor g = 1`; visible disappearance of a cap is not success.

This is only a general transfer lemma until the actual source supplies L and
the step-lifting guarantee. Declaring every reachable state a summary, or
requiring every bottom SCC to contain a good state, merely restates existence.
The useful new work must supply a smaller, checkable interface and prove this
one-sided lifting from geometry. In the current branch, arbitrary-boundary
pairings/parities plus marked constraints are promising for that purpose;
their realization and defect descent cannot be inferred from local marginals.

## 5. Priority, scope, and verification

The recommended proof target is the signed contextual reduction of §3, or a
same-source matching repair validated by the complete parity interface. These
are distinct exits. A theorem about finite response compression does not itself
construct a smaller disk, and a matching interface does not by itself supply
an even endpoint. Keep both source obligations visible.

The four-query certificate expands the admissible replacement signatures from
one fixed mask to 64 raw masks. This is a concrete specification relaxation,
not a claim of 64 new realizable graph classes or a statistical coverage rate.
Its unrestricted source obligation is larger than another special seven-cap
lemma: a successful construction could leave the current r6/mask319 class and
still contradict the original global minimum. The existing W5 quotient no-go
means a larger region, different candidate family, or direct matching success
is needed.

Executed successfully:

```sh
python3 -B audits/2026-10-18-abstraction-bottleneck-9f1fe84/A/check_signed_interface.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-18-abstraction-bottleneck-9f1fe84/A/check_signed_interface.py
```

Both check the frozen input hashes, exact row order, 132 distinct masks, all
3072 target/scope comparisons, 528 at-most-three-query negative controls, and
the 64-mask cylinder. Catalogue generation, witness colouring enumeration,
source realization, and Lean are not rerun. No new graph exclusion is claimed.
