# M10: the complete ten-vertex C8 inner calibration

BASE `6cafdfb02fe5892a49eee21f92aea2369a25c022`. This is a bounded
calibration after a paper classification, not an enumeration cutoff used as an
arbitrary-size proof. Let `C=(c0,...,c7)` be the original induced collar,
`I` its ten strict inner vertices, and `Q=H[I]` in the inherited embedding.

## Premises and original attachment reduction

Use the frozen original disk contracts: all bounded faces of `H` are triangles;
`d_H(c)>=4` for `c` in `C`; `d_H(x)>=5` for `x` in `I`; original internal C3
and C4 caps are empty, and C5 caps are empty or a single W5. The C3 statement
comes from the frozen deep-five-wheel report, sections 1 and 4. The old frozen
C8 proof establishes that every strict inner vertex has at most two C contacts,
which, if two, are adjacent or antipodal; the eight original C-edge third
vertices `t0,...,t7` are distinct; and at least one vertex has no C contact.

An adjacent double contact must be the original facial `t_i`. A second vertex
`x` joining `c_i,c_(i+1)` would make an occupied original triangle cap enclosing
`t_i`, prohibited by the empty C3 premise. Thus the two vertices outside the
`t_i` set are single-contact, antipodal-contact, or zero-contact vertices.

There is no antipodal-contact vertex at `m=10`. If `x` joins `c_i,c_(i+4)`, its
crosscut splits the disk into two original C6 caps. Each cap contains the four
`t_j` belonging to its four original C edges, and neither `t_j` can cross to the
other cap. Only one remaining strict vertex can have zero C contact. Hence one
cap has no such vertex. Its induced Q lobe is outerplane: all four `t_j` reach
its C arc, and `x` reaches its endpoints. Every `t_j` has Q degree at least
three within that lobe. A simple outerplane graph has two low-degree ears, and
only `x` could be one of them, a contradiction. Two antipodal-contact vertices
already exhaust the two extra vertices and contradict the existence of a
zero-contact vertex. This covers both single and repeated antipodal patterns
without inferring exclusion from a finite count.

Consequently the original C links form an actual simple cycle of length eight
or nine. If nine, the extra exposed vertex `x` has just one C contact and there
is a unique strictly deeper vertex `r`. A chord of this nine-cycle cuts off a
triangulated polygon avoiding `r`. Such a polygon has an ear away from the
adjacent chord endpoints; the complete inward Q sector at that vertex lies in
this polygon, so its Q degree is two, contradicting its required degree at
least three. There are no chords. Triangulation therefore forces W9. But `x`
then has Q degree three and H degree four, contradicting `d_H(x)>=5`.

Thus `I={t0,...,t7,r,s}`, the original collar is the standard C8-to-T8 annulus,
all its sixteen C-I edges are precisely `c_i t_i` and `c_(i+1) t_i`, and `r,s`
have no C contact.

## The three named types

Every `t_i` has Q degree at least three; `r,s` have degree at least five.

**M10-CHORD-55.** If the original T8 has a chord `t_a t_b`, both chord sides
must contain a deeper vertex: an empty side would have the forbidden low-degree
ear. Each side has exactly one of `r,s`. A center of degree at least five needs
at least five vertices on that side's rim, so each T arc has at least four
edges. Their sum is eight; both have length four. Thus `b=a+4` and each side is
exactly W5. No second T chord is possible, since distinct antipodal chords
cross. The centers are nonadjacent. There are four choices of the literal
chord endpoints with fixed original C/T labels.

**M10-EDGE-35 and M10-EDGE-44.** If T8 has no chord, the only possible strict
inner edge is `rs`. It must exist: every bounded triangular face uses a T edge
or `rs`, and without `rs` the third vertices of successive T-edge faces must
all be the same center, leaving the other center disconnected. The two faces
at `rs` have distinct original third vertices `t_a,t_b`. The r- and s-faces
form contiguous original T arcs. If the clockwise r-arc has `d` edges, then
`d_Q(r)=d+2` and `d_Q(s)=10-d`; hence `d=3,4,5`. Interchanging the otherwise
unnamed centers identifies 3 with 5. The 3/5 type has eight short-arc placements;
the 4/4 type has four unordered antipodal endpoint placements.

| Named type | Literal placements | Deeper edge/chord | Degrees of r,s |
| --- | ---: | --- | --- |
| M10-CHORD-55 | 4 | `t_a t_(a+4)`, no `rs` | 5,5 |
| M10-EDGE-35 | 8 | `rs`, no T chord | 5,7 |
| M10-EDGE-44 | 4 | `rs`, no T chord | 6,6 |

This proves completeness before any coloring computation. Labels for `r,s`
are chosen deterministically from each indicated clockwise arc; no original C
or T label is rotated or discarded. `check.py` constructs exactly these 16
named graphs and checks their complete oriented triangulated disks, vertex
links, degree/contact requirements, and every original C3/C4/C5 cap using a
face-dual flood with the literal cycle edges as the barrier.

## Complete fixed-frame transfer and certificate

For every proper literal T row `tau` in `{0,1,2,3}^8`, `F_Q(tau)` is the complete
set of Q colorings extending precisely that row, including the empty set.
For a proper C row `gamma`, the actual attachment formula is

\[
 F_H(\gamma)=\{\gamma\Vert\lambda:\lambda\in F_Q(\tau),\quad
 \lambda(t_i)\notin\{\gamma(c_i),\gamma(c_{i+1})\}\ (0\le i<8)\}.
\]

The union runs over every literal proper `tau`, with no independent color
normalization. Each whole H lift retains all eighteen original colors.

For each original B-C collar `A_e`, the next transfer is the full same-row join

\[
 F_G(\beta)=\{\beta\Vert\gamma\Vert\lambda:
 (\beta,\gamma)\in\operatorname{Col}_4(A_e),\quad
 \gamma\Vert\lambda\in F_H(\gamma)\}.
\]

`check.py` reconstructs all eight B-C collars and compares their actual named
edges and oriented faces against the frozen previous literal certificate.
The 128 resulting G graphs are saved with the actual `a_i,y_(i,j)` names and
oriented faces; `original_C_names[i]` specifies the identity `c_i` in each
original collar. The eight contracts are the frozen `c15/c18-933` and
`c04/c07/c15/c18/c20/c30-941`, each with its original e vector and target.

The certificate preserves every one of the 6564 literal proper T rows per Q,
including empty rows. C has 274 proper rows up to one common global color
permutation: the alternating two-color row has orbit size 12 and each other
row has orbit size 24, giving `12+273*24=6564`. Every stored C fibre uses the
fixed representative colors throughout C,T,r,s. To obtain another literal C
row, one single permutation acts on the whole H lift; permutations of colors
unused on C preserve the complete representative fibre, so the deterministic
completion used by the checker loses no lift.

`certificate.json.gz` contains all graphs, original oriented faces, all complete
Q/H/G lifts, all row orders, and all counts. Direct search in each whole graph
is compared lexicographically with the layered full join, not only with its
support or count. Empty Q and C fibres are part of that equality.

| Check | Complete result |
| --- | ---: |
| H graphs | 16 |
| Fixed-frame C fibres | 4384 |
| Empty C fibres | 1500 |
| Whole H lifts | 7408 |
| Original B-C source controls | 128 |
| Fixed-frame B fibres | 1280 |
| Whole G lifts | 75936 |
| Complete Sigma | 1023 in all 128 controls |

Thus none of the sixteen `m=10` H configurations can yield the asserted
complete source relation 933 or 941 in any of the eight contracts. Combined
with the frozen `m=9` exclusion and the paper size bound, this establishes
`h=3 => m>=11 => k(G)>=19` for those original sources. It gives no unrestricted
h>=4 bound or arbitrary-size contract closure. Actual 933/941 sources remain
`not triggered`; the exclusion follows from complete classification and
complete fibres, not from zero discovered sources. No new Lean theorem is
claimed.

Verification commands are

```bash
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/calibration/check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-peeling-6cafdfb/calibration/check.py --check
```

The four negative controls remove a required whole G lift, alter a literal H
edge, remove an empty Q row, and remove an empty C row. All must be rejected by
the same complete-certificate comparison as normal validation. `--check` is
read-only; only `--write` creates the deterministic gzip certificate and
`RESULTS.json`.
