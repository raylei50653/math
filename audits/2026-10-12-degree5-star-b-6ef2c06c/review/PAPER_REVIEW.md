# Independent paper review and literal spot checks

Review scope: `paper/CONTRACT.md`, the frozen source/topology domain, and direct
literal coloring spot checks. The reviewer wrote the mathematical contract
before finite operation-coloring results were inspected. `DESIGN.json` froze
its SHA-256 as
`31c1ebb1ba5d3f99d6e4fcfaf5c3d80df776f10cedc03ca917d661243af95a28`.
The frozen contract has not been changed after that freeze.

## Paper conclusions

The CENTER bijection preserves the whole H=G-v lift, all five actual neighbor
colors, and the original common outer color frame. Its missing-color set gives
every possible center color, including an empty set. It holds without assuming
the neighbors form a cycle.

Spoke deletion and flip share exactly one D_i lift universe. The conditions
A_i (restore the old spoke) and Z_i (satisfy the new opposite diagonal) are both
evaluated on that same coloring. Every old deletion lift survives, but this
establishes only relation inclusion. For flips, preservation of every old lift
is stronger than old-to-new row coverage and still establishes only that
direction. Boundary-relation equality may use different witnesses in the two
directions; a demand for one common witness is not a necessary condition.

The quotient proof uses the literal vertex map and complete block equalities.
Pullback and descent are inverse full-lift maps between quotient colorings and
H colorings constant on each block. Boundary injectivity and absence of loops
are needed; parallel-edge simplification preserves proper coloring. Inserting
v is a separate CENTER test. One pair equality does not ensure this test.

F-SOUND and Q-SOUND prove both row inclusions with explicit choices of full
lifts. Their paper proofs do not rely on a finite trigger, minimum-source
identity, edge-criticality, deficiency, or the external saturation theorem.
Their zero finite triggers are not a failure of the proof and do not yield a
reduction in a conditional minimal outside-catalogue source.

All simultaneous equalities must be checked on the same H lift. A fixed-domain
absence of a counterexample to Q-SEPARATE-JOIN cannot replace this full-join
requirement or prove the corresponding arbitrary-relation claim.

## Independent enumeration method

For each graph used below, the reviewer fixed each of the ten stored boundary
patterns and independently enumerated `itertools.product(range(4),
repeat=number_of_remaining_vertices)`. An assignment was retained precisely
when every literal edge had differently colored ends. This did not call the
generation checker, its backtracking functions, or its relation projections.
For quotient spot checks the transformed literal graph was enumerated directly
as well as comparing equal-color H lifts. The full audit checker supplies the
replayable exhaustive record; these checks are an additional independent sample.

The row order is the frozen `controls/domain.json` order:

    0:01012  1:01021  2:01023  3:01201  4:01202
    5:01203  6:01212  7:01213  8:01231  9:01232.

## W5: deletion and flip

The source has vertices `[0,1,2,3,4,5]`, boundary `[0,1,2,3,4]`, center `v=5`,
and literal edges

    01,04,05,12,15,23,25,34,35,45.

Its frozen rotation gives `L=[0,4,3,2,1]`. Direct enumeration gives
`Sigma(G)=91`, the five three-color boundary rows 0,1,3,4,6.

Delete spoke 05. The result has `Sigma=987`, adding rows 7,8,9 and losing none.
The old row-0 lift `[0,1,0,1,2,3]` remains proper. The new row-7 lift
`[0,1,2,1,3,0]` is proper after deletion and fails the original spoke because
vertices 0 and 5 both have color 0. These are literal counterexamples to D-ANY
and D-OLD-ALL as claimed equality conditions.

Flip 05 to the opposite diagonal 14. The two original incident inner faces are
`[5,0,4]` and `[0,5,1]`; 14 is an absent diagonal of their quadrilateral.
The flip has `Sigma=721`, losing rows 1,3 and adding rows 7,9, so its relation
is incomparable with the original. The row-0 full lift `[0,1,0,1,2,3]` satisfies
both the old spoke and the new diagonal. The added row-7 full lift
`[0,1,2,1,3,0]` satisfies the new diagonal and fails the old spoke. Thus a common
successful lift does not establish full relation equality: F-ANY is refuted.

Every neighbor of this center is an original boundary vertex. Hence W5 has no
admitted nontrivial quotient in this task. Its boundary vertices have degree
three, so W5 is a positive control for star operations, not a conditional
minimal outside-K source.

## Catalogue 95, v=6: single-pair quotient

The literal source has vertices `[0,1,2,3,4,5,6,7]`, boundary `[0,1,2,3,4]`,
`L=[0,4,3,2,5]`, and edges

    01,04,05,06,07,12,17,23,25,26,27,34,36,46,56,57.

Operation `catalogue:95:v6:quotient:01231` deletes center 6 and identifies
vertices 4 and 5, retaining boundary label 4. Its literal quotient has vertices
`[0,1,2,3,4,7]` and edges

    01,04,07,12,17,23,24,27,34,47.

Direct enumeration gives `Sigma(G)=95` and `Sigma(Q)=271`. Rows 4,6 are lost;
row 8 is gained. On row 0, the H coloring on ordered vertices
`[0,1,2,3,4,5,7]` is `[0,1,0,1,2,2,3]`. It satisfies 4=5 and has center color 3
available. This triggers Q-ANY, but the complete boundary relations differ.

On row 8, the H coloring is `[0,1,2,3,1,1,3]`, so the ordered L tuple is
`[0,1,3,2,1]`. It satisfies 4=5 and uses all four colors, leaving no center color.
It descends to quotient lift `[0,1,2,3,1,3]` on `[0,1,2,3,4,7]`; no original G
lift exists on this row. This is a literal Q-PAIR-CENTER counterexample.

For the lost rows, direct enumeration returns the original full lifts
`[0,1,2,0,2,1,3,3]` on row 4 and `[0,1,2,1,2,1,3,3]` on row 6, while the quotient
fibres are empty. Thus both directions of the incomparable outcome have direct
literal evidence, rather than only mask subtraction.

## Candidate-scoring correction and evidence version

The initial generator used the first L-ordered member of an equality block as
its pair representative for Q-SEPARATE-JOIN. The pre-result frozen contract
requires the **least actual vertex label**. These spanning constraints have the
same simultaneous conjunction, but their separate existential hypotheses need
not agree. The initial output also aggregated Q-PAIR-CENTER by operation rather
than its frozen individual-lift unit. Therefore the retained v1 certificate is
**not accepted evidence** for the frozen candidate scores. The contract and
source/operation domain were not changed to fit the results.

The corrected v2 generator uses sorted actual labels and individual equality
lifts. Its reported Q-PAIR-CENTER scores are 2,340 triggering lifts: 1,710
`triggered and holds` and 630 `counterexample`. These 630 failed lifts occur
across all 275 single-pair operations; the latter operation count must not be
misreported as a count of individual lifts or as saying every equality lift
fails. Q-SEPARATE-JOIN reports 60 triggering operation-row instances, all
`triggered and holds`, with zero counterexamples. An independent direct-product
scan using the least actual label also found no counterexample to that frozen
Q-SEPARATE-JOIN predicate. This remains fixed-domain calibration only.

The mathematical relation comparisons are unaffected by this predicate-scoring
repair. The corrected generator reports 385 deletions strictly enlarging the
relation; flips comprise 20 strict shrinkages, 5 strict enlargements, and 320
incomparable outcomes; quotients comprise 75 strict shrinkages, 10 strict
enlargements, and 205 incomparable outcomes. None of the 1,020 admitted
operations preserves all ten rows. The independent examples above confirm
specific outcomes; exhaustive acceptance belongs to the complete independent
checker and its recorded run, not to these spot checks alone.

## Custody and residual boundaries

The upstream literal catalogue and its original checker carry graph edges and
an apex-planarity result but do not supply historical source rotations. The
audit freezes a newly certified disk embedding before operation coloring, and
then preserves that same embedding through each operation. This is honest
fixed-embedding calibration; it is not verification of an unavailable old
rotation and does not quantify over all embeddings of each literal graph.

No 933/941 graph satisfying the conditional minimal-source identity was
supplied. Its source trigger remains `not triggered`. No Lean verification was
run. General reducibility and catalogue equality remain OPEN; neither a zero
trigger nor zero equality-preserving operations in these small controls changes
those boundaries.
