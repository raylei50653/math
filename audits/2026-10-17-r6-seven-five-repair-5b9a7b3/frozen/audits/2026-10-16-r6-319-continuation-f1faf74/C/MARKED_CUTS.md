# C addendum: a cyclic five-cut crosses at most one marked edge

BASE `f1faf743833c51ddc5efbe9e0f390b87b9f2311d`, same source and all literal
names as [PROOF.md](PROOF.md). This addendum uses the three original BASE
proofs separately sealed in `../ADDITIONAL_INPUTS.json`; the original
BASE manifest and earlier worker certificate remain unchanged.

**Theorem C3.** Every actual cyclic five-edge cut of `D=J*` contains at
most one of the three specified dual edges `e=vw*`, `f=pq*`, `g=mz*`.
In fact no J five-cycle contains both e,f or both e,g; a J five-cycle
containing f,g always has a noncyclic dual side.

This is an arbitrary-size restriction on the full source, using the old
exact common-neighbour lemmas. It applies beyond cuts chosen from a
particular Tutte barrier or matching defect. It does not force existence
of any cut and does not prove an even-complement matching.

## 1. Exact identities on the same completed source

The frozen six-pin proof, section 3, gives

`N_U(z) intersect N_U(v)={s}`,
`N_U(z) intersect N_U(w)={t}`.                         (1)

Its proof retains the actual r fan and the original a/c collar. Thus after
the legal s=t quotient these become exactly

`N_J(z) intersect N_J(v)={m}`,
`N_J(z) intersect N_J(w)={m}`.                         (2)

No old common neighbour is hidden or duplicated in (2). For any retained
vertex other than m,z the quotient retains all relevant adjacencies;
m is the image of the one permitted original neighbour.

Write `a0=d_G(a)`, `c0=d_G(c)`. If `mq` is absent, equivalently c0>=5,
the very same original graph also has the exact formula

`N_J(m) intersect N_J(q)`
`  = {z} union ({j_c} if c0=5) union ({p} if a0=4)`.   (3)

Here j_c, when present, is the **actual unique middle vertex** of the
original c fan `(s,j_c,q)`; it is adjacent to z in J. It is not p,q,m,z.
The reflected formula, valid when mp is absent, is

`N_J(m) intersect N_J(p)`
`  = {z} union ({j_a} if a0=5) union ({q} if c0=4)`.   (4)

These follow by taking the union of the original s/q and t/q common
neighbours (and their reflection). Parallel-edge suppression changes no
set member. In (3), the original consecutive s/q formula gives z and
possibly j_c, while the original nonconsecutive t/q formula gives z and
possibly p. Their derivations are in the newly frozen six-pin proof,
sections 3.2--3.3; the nonconsecutive proof uses the original low-p/q
result `q=5 => c0>=6` (and its reflection), separately frozen as well.
The a/c degree sum is at least eleven, so the two optional members in
(3), or in (4), cannot occur together. The proofs below do not depend
on dropping either optional member.

## 2. Excluding each marked pair

The four old cross nonedges `pv,pw,qv,qw` exclude a five-cycle containing
both e and f: the two connecting portions between the disjoint marked
edges each have length at least two, making total length at least six.

Suppose a five-cycle contains e=vw and g=mz. It has exactly the vertices
m,z,v,w,A, where A is a fifth distinct vertex. Since zv and zw are
nonedges, its two connecting portions between vw and mz must have lengths
one and two. The direct connection is mv or mw; the length-two connection
joins z to the other endpoint through A. Thus A is a common neighbour of
z and v or w, different from m, contrary to (2). Hence there is no such
five-cycle at all. This strengthens the general ear statement in the
main proof, which is vacuous for this pair in a full source.

Finally suppose a cyclic five-cut contains f=pq and g=mz. Its primal
five-cycle has a `zpq` triangular ear whose induced C4 core retains mz,
by the existence argument at the end of main proof section 3. No
uniqueness of ears is required. Up to p/q reflection, write the five-cycle
and selected core as

`Q=(m,z,p,q,A)`, `C=(m,z,q,A)`.

The fifth vertex A is distinct from m,z,p,q. The induced core requires
mq and zA to be absent, and its two actual edges mA,qA put
`A in N_J(m) intersect N_J(q)`. Apply exact identity (3). It cannot be
z or p, since those already occur on Q. The only other possible member
is j_c, but its retained z edge would be a forbidden core chord zA.
Thus no A exists. The reflected orientation uses (4) and excludes j_a
by the same actual z edge. Consequently no cyclic five-cut contains f,g.
The three pairwise exclusions prove C3. QED.

## 3. Source authority, replay and remaining endpoint

The new conclusion restricts **one actual source graph**, with all seven
U pins, ordered rotation and attachments unchanged. It does not form a
new complete relation from different feasible witnesses. Every complete
private-colouring fibre, including the empty ones, and every original r
lift retain the old universal obligation. The checker here is purely
geometric/algebraic and makes no new projection or colouring claim.

[check_marked_cuts.py](check_marked_cuts.py) verifies all additional frozen
hashes and records the finite elimination of every optional-member case
of (3),(4), retaining both j and opposite-endpoint possibilities. It also
enumerates all five-vertex simple graphs allowed by the e/f and e/g
local skeletons to check those two elementary cycle exclusions. That
finite calculation calibrates the set/edge deductions; the original
common-neighbour and planar ear proofs supply the arbitrary-size
source authority. `marked-cuts-certificate.json` binds this addendum,
checker and all additional inputs. Default and seed17 pass; a corrupted
optional j chord and an overwrite attempt must be rejected. Receipts
are in `MARKED_CUTS_VERIFICATION.json`.

Actual minimum sources supplied: zero, **not triggered**. In particular
C3 does not repair a long odd complement, exclude the surviving mixed
sectors in C1, or turn the ordinary101 witness into an even endpoint.
`W110+W101>0`, complete319, and the general theorem remain OPEN. The
completed source still has k+5 vertices; there is no smaller-bad-source
argument, external theorem, 4CT use, Lean theorem, commit or push here.
