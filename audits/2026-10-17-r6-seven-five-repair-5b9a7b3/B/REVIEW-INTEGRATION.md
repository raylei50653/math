# B independent review of the integrated paper result

Reviewed 2026-10-17 against frozen BASE
`5b9a7b3190c84bc10ff99608e372a9b4be57a0f6`.
Scope: root `PROOF.md`, `A/PROOF.md`, and `C/PROOF.md` as read after
their first complete drafts. This is a mathematical cross-review, not a
claim that any full original source was instantiated.

## 1. Six-state cap table and actual one-path decomposition

**Accepted.** The integrated six-row table agrees with B's complete
32-row reconstruction and all 15 local matchings. The omitted seventh
size-three matching (`S=456,N={01,23}`) is correctly retained in B's
certificate and excluded from an even endpoint because it leaves a
closed pentagon. The six remaining cap paths have lengths six in five
cases, and two with a separate even quadrilateral in one case.

The two changed spokes belong to `M△M0`. The unique cap difference
path connects them; an internal alternating cycle cannot exist with only
one old internal matching edge. Therefore precisely one actual global
difference cycle meets X. Every other difference cycle is completely
exterior. This is valid for arbitrary exterior size.

The table concerns `H-N`, with all seven cap vertices retained. The root
column heading about cutting the two ports should be read as cutting
their interface to the exterior, not deleting those vertices. Replacing
that heading by “五割內的完整 M0 補圖片段” would make this unambiguous.

## 2. Complete centre trichotomy and mark identity

**Accepted.** If the degree-four centre is v or w, its incident primal
mark vw has dual edge on its facial quadrilateral, hence is either on
C or the shared chord. The matching condition excludes C, forcing the
chord to be e and the other centre to be the other v/w endpoint. The
same reasoning gives chord f for a p/q centre in direction110. A p/q
centre in direction101 places f on the quadrilateral boundary, and A3
forces the other centre to be an ordinary degree-five vertex. These
cases are exhaustive.

In the active-f case, f is one of 01,12,23 and is in M0. The complete
local relation gives exactly B4's three states. In each state f is on
the unique cap difference path; therefore `Q=H` is necessary. The two
chord cases retain the chord in M0 and have only the three one-edge
local difference paths. The distinction between this fixed reference
decomposition and general batches that can flip both f,g is preserved.

C's stronger exterior-placement observations also check: a spoke mark
pq in a chord-e cap would give a primal triangle containing v or w
together with p,q, violating the cross nonedges. A spoke mz in that
cap would similarly violate zv,zw. In a chord-f cap, the same argument
places e outside, and the omitted g cannot be any matching spoke.

## 3. The explicit cyclic-six cut

**Accepted.** In the active-f cap, select a nonchord endpoint a of f
on the quadrilateral arc, and suppose e is a spoke. Primal vw and pq
have four different endpoints, so they cannot lie in one triangular
face. Consequently the dual edges e,f have no common endpoint; e is
not the spoke at a. For the explicitly named set `Y=X\{a}`, cubic
degree and the absence of a chord at a give

`|δ_D(Y)|=5-1+2=6`, `e,f∈δ_D(Y)`.

The pentagon on the other side of the chord avoids a and stays inside
Y. The complete old exterior F cycles stay inside `V(D)\Y`; at least
one exists because the cubic graph cannot have seven vertices and no
old F edge crosses the five-spoke cut. Thus both sides contain actual
cycles and the adopted R6-MARKED-SIX theorem applies. This is the
requested kind of explicit cut argument for precisely this mark
placement. It does not assume the unproved general implication from
blocked repair to a small cut.

## 4. Exact whole-component exchange and strict global descent

**Accepted.** Set `L=D-(M∩M0)=F∪F0`. An L-component W contains every
whole F and F0 cycle meeting it, every whole difference cycle meeting
it, and has boundary contained in the common matching. Flipping all
difference components in W changes the complementary restriction there
to F0 and changes nothing outside W. No complementary edge crosses
the boundary. Therefore

`odd(D-M_W)=odd(F)-odd(F[W])`.

If W avoids the unique blocked difference cycle H, the actual batch
retains the joint identity. A positive odd-component count in W is even:
W is a union of whole even F0 cycles and thus has even order. The
strict decrease is consequently at least two. Every joint oddness
minimum has all its odd components in the single W_H. This proves the
announced `W_C≠W_H` arbitrary-size exclusion and leaves `W_C=W_H`
unresolved. In particular `Q≠H` alone supplies only safe marks.

A's complete surgery also checks: removal of actual `M0\M` edges
retains a fixed set of labelled old complementary paths; adding actual
`M\M0` edges reconstructs every new whole complementary cycle. With
the cap separated out, the exact change is `o_new-o_ext-1`. Vertex
parity gives `o_new≡o_ext+1 (mod 2)`, so strict descent is equivalent
to `o_new≤o_ext-1`. Hence merely touching even exterior old cycles
cannot yield strict descent. The independent plane control is properly
scoped away from source realizability and joint minimality.

One wording correction was requested from A: its phrase “stronger than
the sufficient condition Q != H” should explicitly say that Q!=H is
sufficient for mark safety only, not for strict descent. The integrated
root proof already states the correct distinction.

## 5. Scope accepted

The integrated result correctly claims a conditional all-size descent,
the exact local relation, and one actual mark-placement exclusion. It
does not claim complete three-spoke repair, disappearance of every
nonfacial seven-defect at a joint minimum, source realization, joint
positivity, complete319 exclusion, or a new Lean theorem. Whole
influence-component boundaries cannot trigger the requested marked cut
by themselves because the cap contains at least one whole e/f edge.
Any remaining cut argument must split the cap and verify both cyclic
sides afresh.

B's own verification is complete: normal and seed17 replay have
identical stdout and certificate SHA256
`5396d6485bbdfc5718f8bc33df1be5293627eee8efcad034da2320be4613a765`;
missing-empty-row and changed-complete-fragment corruptions are rejected;
exclusive-create overwrite is rejected; all 11 frozen inputs match
their sealed hashes and Git BASE bytes. See `VERIFICATION.json`.
