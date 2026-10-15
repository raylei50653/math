# Original r of degree six: the complete C5 support is 319

BASE is `676b1024715f24a0d969fba90baab21b756406e2`. The immutable
[input seal](../INPUTS.json) binds the [source geometry](../frozen/audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md),
[previous degree-six transfer](../frozen/audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md),
[previous quotient construction](../frozen/audits/2026-10-14-c4-return-branches-a11d4bb/r_high/PROOF.md),
and [no4ct source contract](../frozen/docs/tasks/c5_no4ct_handoff.md).
This is a new stronger source screen; the old transfer and integer-count
certificates remain unchanged.

Within the existing globally minimum noncatalogue C5 source contract,

\[
d_G(x)=d_G(y)=d_G(b)=4,\qquad d_G(r)=6
\quad\Longrightarrow\quad
\boxed{\Sigma(U)=319},\qquad U=R-r,
\]

in the fixed boundary order `(z,s,v,w,t)`. This excludes the two former
possibilities 271 and 314. It does not exclude the r=6 branch.

## 1. Exact source and smaller-disk contract

G minimizes the number k of interior vertices among **all** finite simple
C5 disk graphs whose complete boundary relation is outside K132; the
secondary maximum-edge choice supplies the previously proved structural
normal form. Comparison disks need not have that normal form. In particular,
the underlying disk class permits chords and does not require connectedness
or triangular inner faces. Every legitimate comparison disk with fewer than
k interior vertices has its complete relation in K132. Every one of the
132 frozen relations is nonempty. This is relative minimum-source
colourability and does not assume the general four-colour theorem.

The frozen transfer has already proved that R has total size k+1 and that
deleting the original degree-six r produces a triangular disk U with total
size k and the simple induced C5 boundary

`C=(z,s,v,w,t)`.

The original r fan is `(x,y,t,w,v,s)`. In particular, `sw` and `vt` are
nonedges: either edge would form a nonfacial triangle through r in the
four-connected T0. The inherited face `zpq` remains; its three vertices
are distinct and p,q are strictly internal to U. The same transfer proves

\[
\Sigma(U)\subseteq319,\qquad
\Sigma(U)\in K_{132},\qquad
\Sigma(U)\in\{271,314,319\}.
\]

These are complete outer relations, not summaries of selected colourings.
All marked p,q constraints and all empty fibres in the former all-r-lifts
table remain part of the underlying source contract.

## 2. Relative cofacial equality lemma with an explicit cap

Let A be a finite plane graph and let a,b be distinct nonadjacent vertices
incident with one face. Draw a new a-b arc in that face and contract the
new edge. Delete the contracted edge and suppress parallel copies of other
edges. This constructs a planar quotient Q=A/(a=b). Because ab was not an
original edge, no original edge becomes a loop. Suppression of parallel
edges changes neither proper colourability nor the exact correspondence

\[
\operatorname{Col}_4(Q)\;\longleftrightarrow\;
\{f\in\operatorname{Col}_4(A):f(a)=f(b)\}.
\]

This is a bijection on complete labelled colourings in one fixed colour
frame. The identification contracts the added arc; it does not delete any
constraint on an edge of A.

Suppose Q has N vertices and at least one edge. Choose one edge uv and one
of its incident face sides on the sphere. Within a sufficiently small
neighbourhood on that side draw a new path `u-a1-a2-a3-v`, whose three
new vertices and edge interiors avoid Q. The new path and the old edge uv
bound an empty disk. Declare that empty disk to be the exterior face. All
of Q lies on the other side, inside the resulting specified C5. The five
boundary vertices are distinct, and there are no chords between them:
each new vertex has just its two path edges and uv is a boundary edge.
Thus the result D is a finite simple legitimate C5 disk, with

\[
|V(D)|=N+3,\qquad k(D)=N+3-5=N-2.
\]

Inner cutvertices, nontriangular faces, or suppressed parallel edges in Q
do not prevent this construction. Minimum-source comparison applies to
the whole disk class; it does not require D to be a triangulation or an
edge-maximal source. If `N-2<k`, then `Sigma(D)` belongs to the nonempty
K132, so D has a complete colouring. Restriction to Q and the displayed
bijection give a complete colouring of A with a=b. No conclusion equating
the complete fibres of D with those of a catalogue representative is used.

This is the reusable statement: **a cofacial nonedge has a nonempty complete
equal-colour fibre whenever its planar quotient admits the above C5 cap
within the strict minimum-source interior budget.**

## 3. Two separate applications to U

Both pairs s,w and v,t are nonedges on U's actual exterior. Either
identification reduces the vertex count by exactly one; edge suppression
does not remove vertices. It leaves the triangle zpq intact, so the
quotient certainly has an edge. In either case the cap budget is

| Graph | Total vertices | Specified C5 interior count |
| --- | ---: | ---: |
| U | k | k-5 |
| Q=U/(s=w), or U/(v=t) | k-1 | not used |
| capped Q | k+2 | k-3<k |

The lemma therefore proves both

\[
\exists f\in\operatorname{Col}_4(U):f(s)=f(w),\qquad
\exists g\in\operatorname{Col}_4(U):g(v)=g(t).
\]

Each is a full colouring of the same original U. They are separately
quantified and need not coincide. In fact the sole canonical proper C5
row satisfying both equalities is ABCBC, which the old support upper
bound 319 forbids. Hence in this source these two witnesses must differ.
No simultaneous identification or combination of independent witnesses
is asserted.

## 4. Fixed ten-row screen

The checker reconstructs the following order from all `4^5=1024`
labelled assignments, retaining all 240 proper C5 assignments and taking
common S4 orbits. It independently checks first-occurrence normalization
against the minimum over all 24 colour permutations.

| Bit | Boundary `(z,s,v,w,t)` | In mask319 | s=w | v=t |
| ---: | --- | --- | --- | --- |
| 0 | ABABC | yes | yes | no |
| 1 | ABACB | yes | no | no |
| 2 | ABACD | yes | no | no |
| 3 | ABCAB | yes | no | no |
| 4 | ABCAC | yes | no | yes |
| 5 | ABCAD | yes | no | no |
| 6 | ABCBC | no | yes | yes |
| 7 | ABCBD | no | yes | no |
| 8 | ABCDB | yes | no | no |
| 9 | ABCDC | no | no | yes |

Thus s=w permits `ABABC,ABCBC,ABCBD`, and inside 319 it forces a nonempty
ABABC fibre. Similarly v=t permits `ABCAC,ABCBC,ABCDC`, and inside 319 it
forces a nonempty ABCAC fibre. Because a complete global colour
permutation transports every full colouring, the assertion holds for each
fixed representative in these two S4 orbits, including the unused fourth
colour in a three-colour boundary frame.

| Former candidate | ABABC present | ABCAC present | New source screen |
| ---: | --- | --- | --- |
| 271 | yes | no | excluded by v=t |
| 314 | no | yes | excluded by s=w |
| 319 | yes | yes | survives |

The required row-bit mask is `1+16=17`. Among the complete 132 frozen
catalogue masks contained in 319, only 319 contains both required bits.
This proves the stated conditional equality for arbitrary source size.

## 5. Certificate scope, retained evidence, and replay

[check_r6.py](check_r6.py) imports no previous checker. It verifies the
parent input seal, reconstructs the ten rows, checks the frozen transfer
upper support, checks all 132 catalogue masks, and applies the two exact
equality predicates. [r6-final.json](r6-final.json) binds the checker and frozen data.
The arbitrary-size embedding, cap, and colour-pullback argument is the
paper proof above; the finite program does not certify arbitrary plane
embeddings or re-enumerate K132.

Run from the repository root:

```sh
python3 -B audits/2026-10-14-cofacial-fibres-676b102/r6/check_r6.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-cofacial-fibres-676b102/r6/check_r6.py --check
```

[logs/final/receipts.json](logs/final/receipts.json) records default and seed17 checks
and an intentionally corrupted certificate rejection, with complete
stdout, stderr, and exit status retained. The negative control falsely
keeps 271 and must fail comparison with independent recomputation.

The initial [r6.json](r6.json), its hash-bound
[check_r6_initial.py](check_r6_initial.py), and original [receipts](logs/receipts.json)
are retained unchanged. The active checker differs only by exclusive
certificate creation (`open("x")`) and its final-certificate default. No
mathematical row changed. The final receipts also retain an expected
rejection of an attempt to overwrite the final certificate; its bytes
must remain unchanged.

The old [r6 count report](../frozen/audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/REPORT.md)
and [count certificate](../frozen/audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/counts.json)
remain valid evidence that the former explicitly listed necessary support,
switch-orbit, and common-integer-count equations are feasible for all
three masks. Those equations did not encode the two nonedge-quotient
colourability obligations. The current source exclusion adds those
geometric obligations; it does not declare the old integer models
incorrect or claim that the surviving 319 model is realizable.

The r=6 source branch, the low-p/q mask14 source problem, the other T/T0
branches, and the unbounded catalogue equality remain OPEN. This audit
does not improve the general `k>=23` or `K<=22=K<=5=K132`, construct an
actual source, rerun an external enumeration, invoke 4CT, or add a Lean
theorem.
