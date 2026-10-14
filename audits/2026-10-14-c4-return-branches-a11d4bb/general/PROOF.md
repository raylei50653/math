# General mask13: a sector return, with an exact stopping point

The no-rainbow return from the frozen
[r-deletion proof](../../2026-10-14-c4-c5-recursion-fdd3e22/fibre/PROOF.md)
does not presently exclude the general six-pin R. There is an arbitrary-size
refinement on the same complete fibres: the missing-colour endpoint acquires
an additional mandatory attachment, and a palette-changing return is a
bijection between two explicitly defined subsets of the **admitted** ABCB
sectors. General exclusion remains OPEN.

This argument uses the original R, its outer Jordan cycle `(z,s,r,t)`, its
actual triangle edges `zp,zq,pq`, and the common colour frame `(A,B,C,D)`.
Its failure hypotheses are precisely
[JOINT_FIBRES](../../2026-10-14-c4-mask13-joint6-fdd3e22/JOINT_FIBRES.md)
§1: mask13; ABAB universally has pq=CD; ABCD universally has pq=BD.
In particular the rainbow fibre is nonempty. All switches below use actual
maximal components in one complete colouring; no six-point Jordan boundary
or independent path witnesses are introduced.

## 1. Two additional same-colouring attachments

Retain the already proved disjoint sectors

`X={f in F(ABCB): pq=CD}`, `Y={f in F(ABCB): pq=BD}`.

Let `d(f)` be the D-coloured endpoint of pq. The old proof gives
`F(ABCB)=X disjoint-union Y`, with ABCB/BC absent.

For every `f in X`, the vertices `s,t,d(f)` lie in one BD component.
Indeed s and t already lie in one BD component. If d(f) were outside it,
switching its BD component would fix all four boundary vertices and change
pq from CD to CB. This gives a forbidden ABCB/BC full colouring. Thus

`f in X ==> s ~BD t ~BD d(f)`.

For every `g in Y`, the vertices `r,d(g)` lie in one CD component. Otherwise
switching the CD component of d(g) fixes the whole outer word and changes
pq from BD to BC, again forbidden. Thus

`g in Y ==> r ~CD d(g)`.

These refine the old attachment split. They do not connect z to r in X or
s to t in Y: the established complementary disconnections still hold.

## 2. The possible BC palette return has an exact inverse

In every ABCB colouring, the two boundary edges `sr,rt` put s,r,t in one
BC component L. Define

`X0={f in X: the C endpoint of pq is outside L}`,

`Y0={g in Y: the B endpoint of pq is outside L}`.

Switch the BC component of the C endpoint in a member of X0. Its component
misses s,r,t by definition and misses z because z=A. The boundary remains
exactly ABCB, the C endpoint becomes B, and the D endpoint is unaffected.
The image therefore lies in Y0. The same maximal component has the same
vertex set afterward. Switching the BC component of the B endpoint is the
exact inverse on **every vertex**, giving the full-fibre bijection

`X0 <--> Y0`.

The endpoint identity is retained. Thus the map restricts to a bijection
from X0 with `(p,q)=(C,D)` to Y0 with `(p,q)=(B,D)`, and likewise from
`(D,C)` to `(D,B)`. This statement in fact needs only the disk, the literal
edges and the definitions of X0/Y0; its proof does not use the source's
universal palette conditions.

If that endpoint is instead in L, its BC switch changes the boundary to
`ACBC`. Applying the single common B/C renaming restores ABCB and the
original ordered pq assignment. This case stays in its original sector.
Consequently neither case supplies a forbidden ABAB/BD or ABCD/CD lift.

Composing a free-sector switch with the previously proved r/AC and t/BD
maps can connect a subset of ABAB to a subset of ABCD, but each end has its
required palette. An injection into an admitted fibre yields no contradiction.
No assertion that X0 or Y0 is nonempty follows from mask13.

## 3. What the original no-rainbow step would need here

The frozen return lemma starts with outer ABAC and pq=BC in a different
four-pin disk. Its no-rainbow hypothesis forces z and the opposite boundary
vertex into one AD component, whose complementary BC disconnection then
permits the t return. In general R, ABAC is absent and ABCD is present.
There is therefore neither a nonempty initial ABAC/BC fibre nor the
no-rainbow premise used to force that connection.

Within X, the available r/AC return goes to ABAB/CD. Within Y, the available
t/BD return goes to ABCD/BD. Section 2's extra palette switch either crosses
between admitted sectors or stays within one sector after common renaming.
To exclude general R, a further argument must force a switch sequence ending
in ABAC, ABAB with palette other than CD, or ABCD with palette other than BD,
or must use additional source geometry/minimality to rule out all remaining
component states. The present argument establishes none of these conclusions.

The complete source degrees, induced six-pin nonedges, absence of nonfacial
triangles, common-neighbour identity, original contact/rotation rules and
global minimality remain additional premises. The terminal calculation below
does not encode their arbitrary hidden vertices and does not show those
premises compatible or incompatible with target failure.

## 4. Stronger simultaneous terminal control

[check_general.py](check_general.py) starts from the refined seven pin-orbits
and the literal mandatory edges. It separately handles the only possible
optional-edge cases: neither, tp, or qs. Both optional edges together remain
excluded by the frozen source's h>=3 argument.

Each state now records **all three complementary colour-pair partitions at
once**. For a selected complementary split, the checker examines every
independent component switch. Its target must still admit a live simultaneous
state with exactly the same switched-pair and complementary-pair partition.
This is necessary: a component switch preserves both induced subgraphs for
that complementary split, not merely the pin word. Repeated pruning also
requires all future selected splits to have such targets.

The surviving labelled simultaneous states are:

| Optional edge case | Surviving states | Surviving pin orbits |
| --- | ---: | ---: |
| neither | 648 | 7 |
| tp | 240 | 5 |
| qs | 240 | 5 |

Every surviving state satisfies both attachments in §1, and the checker
replays the free/anchored BC return in §2. The ordinary seven/five/five pin
supports therefore survive this stronger necessary control.

This is still an abstraction. It guarantees only a surviving target choice
for each split with that split's exact partition signature; it does not
identify hidden graph vertices across different splits, build a graph, or
build one deterministic switch system on all complete colourings. Even a
nonempty kernel cannot certify cross-colouring graph realization. Conversely
the surviving kernel prevents this particular necessary test from proving
an exclusion; it does not prove that no stronger Kempe argument exists.

## 5. Two honest plane-disk controls and preserved failures

The checker validates oriented face incidence, Euler characteristic, every
vertex link, the exact six-pin induced skeleton and
`N(z) intersection N(r)={s,t}` of two explicit disks. Both have mask13 and
complete fixed-frame fibre counts `(2,0,7,5)`.

The eight-point disk with optional qs has no nonfacial triangles. It has one
full X0 colouring and one full Y0 colouring, and the checker records their
actual component, complete target colouring and exact inverse. This is a
nonvacuous control for §2 on one graph. The nine-point disk with neither
optional edge has empty X0/Y0 and one nonfacial triangle `(z,q,7)`; it only
controls the named skeleton/common-neighbour facts and the full fibre count.

Neither disk satisfies either of the source's universal ABAB/CD and ABCD/BD
palette rows; both also have vertices below the source's degree bounds.
Neither is a target-source realization or a counterexample to general
exclusion. Their full fibres are retained in
[general-final.json](general-final.json), including rainbow colourings. The
earlier [general.json](general.json) is retained with its historical script
hash; the final checker accepts `--certificate PATH` for explicit replay
and certificate corruption controls.

Two initial control failures are retained as
[check_general.initial-failure.log](check_general.initial-failure.log) and
[check_general.second-failure.log](check_general.second-failure.log): they
rejected, respectively, treating the nine-point disk as having all triangles
facial, and assuming its X0/Y0 fibres nonempty. Those properties are now
reported accurately rather than used as premises.

Replay:

```sh
python3 -B audits/2026-10-14-c4-return-branches-a11d4bb/general/check_general.py --check
```

Result: arbitrary-size attachment refinements and the subset full-fibre
bijection are proved; all stronger terminal controls PASS; general mask13
exclusion and arbitrary-size C5 catalogue closure remain OPEN. No external
theorem, graph enumeration, source realization, or Lean result is added.

[receipts.json](receipts.json) records default and seed17 PASS plus expected
rejection of [tampered-negative.json](tampered-negative.json), whose first
partition case falsely claims 647 surviving states instead of 648. Its
stdout/stderr and exit code are retained beside the positive replay logs.
