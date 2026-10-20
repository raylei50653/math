# Independent audit of complete-fibre transport

Authority is the parent [BASE](../BASE.md) and 1,082 SHA256-sealed frozen
inputs. This reviewer writes only in `review/`. No source graph is supplied,
no source is realized, and no commit or push is authorized.

## Existing transport: accepted within its stated scope

The original eight J1 fibres and twelve J2 fibres are full literal fibres of
one actual core F, including all private vertices and empty fibres. The
cap has a unique full lift on every listed fibre. Restricting a complete
Ji colouring and reattaching that cap are inverse operations. Thus there
is no multiplicity or palette-orbit factor missing from either sum.

The d map switches the entire actual 23 component of R, then applies the
global transposition (23) to the complete colouring of F. Both operations
preserve the 23 induced graph, and commute; the composite is its own
inverse. The cap may change its r colour on reattachment, but the original
ordered C5 colour frame is restored exactly. The J1 and J2 family III
equalities therefore hold on full fibres, including empty ones.

The q map switches the entire actual 03 component of q. At q=0 this
component meets the rim exactly at q. The 03 graph is unchanged by the
switch, so the inverse exists precisely on that stratum of the q=3
fibre. “Exactly at q” concerns the boundary intersection: the component
may contain arbitrarily many private vertices. For d=2 the complementary
stratum is precisely q connected to the colour-zero vertex of {v,w}.
The original report correctly does not identify the injection with a
surjection onto the whole q=3 fibre.

Consequently the existing formula and two-target zero equivalence are
valid under the frozen source theorem. No missing inverse, omitted empty
fibre, or change of source was found.

## Exact upstream dependency

The partition lists are consequences of the original three zero rows,
the branch assumption a_i=0, and the previously proved Ji zeros at 01202
and 01212. The frozen complete-component zero closure then restricts
the core to 1,973 possible normalized states. Every actual complementary
component partition must be noncrossing, respect boundary adjacency and
the triangulated block count, and have all component switches remain in
that possible set. This is why the frozen partition lists apply to an
arbitrary complete colouring of the actual F.

The present independent checker uses those frozen possible sets as
theorem inputs. It does not claim to prove the original zeros or source
legality anew. It independently enumerates all 16,796 noncrossing rim
partitions, reconstructs the surviving partitions for each literal
target, and checks the maps without importing any old or sibling checker
implementation.

It exactly reconstructs all 24 J1 colour-pair records, comprising 56
partitions, and all 36 J2 records, comprising 112 partitions. It also
checks all 1,082 parent input hashes.

## Independent check of the proposed orientation stratum

For every one of the eight J1 fibres, the two allowed 01|23 partitions
have a,c,n together and v,w together. Exactly one partition has the
01 component of {v,w} disjoint from a; exactly the same partition has
s and t connected in 23.

On this disjoint stratum, switching the full 01 component of v exchanges
the two orientations of (v,w), changes no other rim colour, and preserves
the stratum. Its own inverse is the same complete-component switch.
This proves the proposed restricted full-fibre bijection. On the other
partition the switch also changes a,n,c, so it is not the claimed
fixed-frame orientation map. A universal equality of the two whole
orientation fibres does not follow.

The d map preserves this stratum because it does not alter the actual
01 induced graph. No analogous compatibility of the q map with this
stratification is asserted: swapping a 03 component can change which
vertices belong to the 01 induced graph.

## Validation and limits

[check.py](check.py) and [certificate.json](certificate.json) record the
independent enumeration and all eight stratum witnesses.
[checks.json](checks.json) records successful normal and seed17 replays.
Changing the separate stratum's v-component label in the
[negative certificate](negative-certificate.json) is rejected.

The whole-source last rejection, original branch exclusion, existence
of a smaller bad source, and Lean formalization remain OPEN. Surviving
necessary partitions have no common actual private graph realization
certificate.

## Independent J2 union map and zero propagation

The subsequent [j2_transport.py](j2_transport.py) independently regenerated
all 64 allowed 01|23 partitions of the twelve J2 fibres. For each one it
switches each distinct actual 23 component meeting {s,t} exactly once.
It verifies that q and the orientation e stay fixed, d flips, and the
same boundary partition is admissible at the output. Applying the same
map twice returns the starting literal assignment.

Families I and II can interchange under the map. Their disjoint union,
for each fixed e, is paired between d=2 and d=3. Family III stays in III
and is paired separately. Since the whole 23 induced graph and rooted
components are invariant, the paper involution acts on all private
vertices and has the same inverse on complete actual colourings.
The unique cap relift restores the original fixed frame. Therefore

```
N01021(J2) = 2 * sum(the six fixed literal d=2 complete F fibre counts).
```

This identity and the resulting six-target zero equivalence are accepted
under the original a2=0 source branch. No individual fibre has been proved
empty, and no pairwise equality between I alone at the two d values is
claimed.

As a separate check, [closure.py](closure.py) independently builds three
complementary-pair obligations for each of the 2,461 canonical states,
without importing the old H-row family or a sibling model. The resulting
7,383 obligations include a redundant obligation at the two-colour state;
this is not an assertion that the old 7,382 H-row count was wrong.
The frozen 1,973-state possible set is stable. Deleting the six d=2
targets removes all twelve J2 targets in the ensuing closure.

[j2-checks.json](j2-checks.json) records normal and seed17 replays of both
independent checks, plus rejection of a tampered involution target.
The reviewer reported these results before a tool-capacity interruption;
the parent added this prose from the completed artifacts and review
message, without changing the independent programs or certificates.

## Parent review of the geometry increment

The parent checked the paper separator and pocket arguments in
[geometry/PROOF.md](../geometry/PROOF.md). In the s~t branch the a–c path
avoids v,w, the s–t crosscut has no other rim contacts, and the first
s–t-crosscut contact / last preceding a–c-path contact give the claimed
ordered private contacts in one complete colouring. The length-three
n–L exception retains the original W5 at R and its exact star.
The seven-rim patch is the union of an eight-face and a five-face disk,
overlapping in hRn and hLR; the parent clarified this overlap wording.
No source contradiction or path-length upper bound follows.
