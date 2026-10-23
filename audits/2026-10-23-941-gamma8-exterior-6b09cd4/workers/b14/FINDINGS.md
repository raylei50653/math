# Fixed B14 join: exact endpoint alternatives and the M-cut obstruction

Scope: the same ordinary short Type I source, original 02 type 13/36, original
03 type 4/9, wrong-side rootless component `M=K02(T)`, and the same literal
`Γ8=(r,T,sΓ,x,h,W*,e,d)`. Here `sΓ` distinguishes the Γ vertex from the B14
vertex named `s`. No source realization or general wrong-side exclusion follows.

## Authorities

- `audits/2026-10-23-941-gamma8-cells-6b09cd4/PROOF.md`, sections 1–5:
  Γ8, the 11 necessary types, complete local stars, and their actual edges.
- `audits/2026-10-23-941-p-b13-6b09cd4/PROOF.md`, sections 1–2, 6:
  the rootless complete M/N components, all their F-private vertices, and the
  Γ8 component labels. The Γ8 arguments below do not assume `j=2`.
- `audits/2026-10-23-three-mask-methods-cb8f859/941/PROOF.md`, sections 1, 4,
  and its `certificate.json` component-interface rows: literal B14, original
  complete 02 partition, the unique necessary successor after the full K flip,
  all original full fibres and full cap lifts.
- `audits/2026-10-21-w7-I-joint-2c38d1d/geometry/PROOF.md`, section 2:
  `N_F(Y) ∩ N_F(V) = {U}`. This uses the original z5 ear and full original
  stars; it is stronger than proper coloring alone.
- `audits/2026-10-21-w7-L-path-30dde27/six_degree/certificate-v2.json.gz`,
  `ordinary_C14_cases`, split `[0,3]`, `complete_specific_F_types[4 or 9]`:
  the exact original 03 and complementary 12 boundary blocks below.

Program name `HL_0` is the same literal vertex Y. All contacts listed below
are complete boundary contacts; private vertices remain present.

## Exact boundary identity alternatives

The complete original K02 contacts are `{U}`, and the complete B13 contacts
are `{V,Y,q,c}`. After the full K flip, the complete C12 boundary contacts
are `{V,U,Y,w,t}` for target 44459 and `{V,U,Y,t}` for target 44466. The
other rooted 12 block D has complete contacts `{c,s}` and `{c,s,v}`,
respectively. E can instead be rootless; if it meets B14, it equals D.
The complete Q03 component contains q.
Consequently:

| Γ role | Possible B14 identity |
| --- | --- |
| r, T, sΓ | none; the complete N/M components are rootless |
| x | none; K's only contact U lies in C, while x lies outside C |
| d | U only |
| e | V or Y only |
| h | c only |
| W* | q only |

For `j=2`, τ and ζ are F-private by the Jordan disk argument. These are
identity alternatives, not a choice to replace an original private vertex by
a freely invented boundary point. The original graph, ordered boundary,
rotation, attachments and full stars remain fixed. In particular, no equality
with the original P endpoint b or last K exit x' has been assumed.

The known qY boundary edge and `N_F(Y) ∩ N_F(V) = {U}` immediately exclude
`e=V, W*=q`: the original edge eW* would make q a second F-common neighbor
of V and Y. This applies to arbitrary Γ8 interior size and either ear side.

## Original 03 and complementary 12 tables

Each row gives all boundary blocks for the split 03|12. Different displayed
blocks are different complete components, including when their colors lie in
the same palette.

| Target | Original 03 type | All boundary blocks |
| --- | --- | --- |
| 44459 | 4 | `{a,z1,z2,z3,z4,U}`; `{V}`; `{Y,w,t}`; `{q,v}`; `{c,s}` |
| 44459 | 9 | `{a,z1,z2,z3,z4}`; `{V,Y,w,t}`; `{U}`; `{q,v}`; `{c,s}` |
| 44466 | 4 | `{a,z1,z2,z3,z4,U}`; `{V}`; `{Y,t}`; `{q,w}`; `{c,s,v}` |
| 44466 | 9 | `{a,z1,z2,z3,z4}`; `{V,Y,t}`; `{U}`; `{q,w}`; `{c,s,v}` |

Thus U and q are in distinct original 03 components in every row, while c
is in a different original 12 component from either V or Y.

For the 11 j=2 types this gives the weaker direct checks:

- `d=U, W*=q, I_d=1` is impossible, since dW* is then the original Uq edge.
- `d=U, W*=q, core=O, I_x=1` is impossible, since O has the original
  03 path `U–τ–x–q`.
- `e∈{V,Y}, h=c, I_x=I_d=0` is impossible, since the strip faces force
  the original 12 path `e–ζ–c`.

These direct checks are subsumed in part by the stronger M-flip result below;
they should not be combined as independent candidate graphs or palettes.

## Full rootless N flip excludes both ears at the U/q attachment

There is a stronger check than the core-O original03 path above. Flip 13
on the **entire original rootless N**. Its vertices remain outside the
02 palette, so the entire original 02-induced graph, complete components
and partition are unchanged. Its boundary word is unchanged, and its full
stars are in F. Thus the original 02 type is still 13 or 36 on the same
literal source; its necessary original 03 split is still one of types 4/9.
The latter may change between the two types, but both separate U and q.

If `d=U, W*=q, I_x=1`, the actual path `d–r–T–sΓ–x–W*` becomes a literal
03 path with colors `(0,3,0,3,0,3)` after this N flip. This joins U to q,
contradicting both admissible 03 splits. As already noted, `I_d=1` directly
gives the forbidden Uq edge even before the flip. Therefore:

**U/q ear lemma.** If `d=U` and `W*=q`, neither xW* nor dW* exists as an
original edge. This holds for arbitrary Γ8 interior size, not just j=2,
and excludes either side of either ear. It uses the same complete N and the
same literal boundary, not an arbitrary independent 03 partition.

For j=2 it leaves the three zero-ear L/R/O local types at either of the
otherwise possible endpoint patterns `(d,e,h,W*)=(U,private,private,q)`
and `(U,Y,private,q)`. It does not assert that either can be realized.

## Full rootless M flip and literal endpoint exclusions

Flip 02 on the **entire original M**, then flip the same entire original K;
call the resulting F coloring χ. M and K are disjoint complete original 02
components, so the flips commute. The first flip preserves the entire
02-induced graph, every complete 02 component and its boundary contacts.
M is rootless, so the literal B14 word is unchanged by this first flip.
Every M vertex is F-private with its complete original star in F; the flip
therefore preserves the original attachments and produces another full
witness on the same F. The fixed boundary-indexed cap relations, complete
fibres and full lifts remain the same relations on the same graph. This
does not assert that swapping this fixed M vertex set defines a proper or
bijective operator on every other coloring in those relations. This is a
proper coloring of the same F, not a replacement disk or independently
selected palette witness.

The full K action still changes the B14 word only at U, from 0 to 2. The
same necessary successor calculation therefore applies to χ. In particular,
no χ12 component can contain both c and any of U,V,Y. This conclusion needs
neither an assertion that the original C/E paths survive the M flip nor an
assertion that the original 03 type itself is unchanged.

On the actual Γ8 edges, however, χ has the literal 12 path

`e1 – d2 – r1 – T2 – sΓ1 – x2 – h1`.

Only T of these seven Γ vertices lies in M, and d,x lie in K. It follows:

**Endpoint lemma.** For arbitrary Γ8 interior size and every ear status,

1. `d=U` and `h=c` cannot hold together;
2. `e∈{V,Y}` and `h=c` cannot hold together.

In particular, if the selected first P/S intersection h is the original
boundary endpoint c, then both d and e must be F-private. This includes
W*=q; it does not exclude W*=q, h=c with d,e private. For the 11 j=2 types
these endpoint exclusions are uniform in L/R/O and in all inner-ear choices.
They do not exclude any one unlabelled local ten-point type outright.

## The retained original C/E paths give a forced separator

There is a useful stronger formulation of the same proof. In the original
ψ12 graph let

- C0 be the component of `C − M2` containing the original path `e–d–r`;
- E0 be the component of `E − M2` containing the original path `sΓ–x–h`;
- `M2={v∈M:φ(v)=2}`.

These paths do survive deletion: their two original0 vertices are in K,
and their original1 vertices are outside the 02 component M. In χ, inserted
T2 joins C0 to E0. Therefore C0 cannot meet an original C boundary contact
while E0 meets an original E boundary contact. Such a pair of boundary
contacts would lie in the same χ12 component, contrary to the unique
necessary successor.

If `h=c`, every ψ12 path in C from `{r,d,e}` to the complete C boundary
contacts must meet M2. If `d=U` or `e∈{V,Y}`, every ψ12 path in E from
`{sΓ,x,h}` to the complete E boundary contacts must meet M2. These are
actual vertex-separator obligations on the same original graph. They permit
arbitrarily many M2 vertices and make no claim that T's one exterior 2
neighbor, when T has degree five, is by itself a separator.

The Γ8 interior and exterior, all other rootless components, possible
multiple P/S intersections, `h≠b`, `x≠x'`, full original stars, and all empty
fibres remain unrestricted. General wrong-side, source realization, and
the eventual 941 exclusion remain OPEN.

## Counting only these literal endpoint filters

There are initially `2×3×2×2=24` endpoint alternatives for `(d,e,h,W*)`.
The endpoint lemma, the q/V common-neighbor prohibition and the U/q ear
lemma leave the following necessary pattern counts:

| W* identity | h identity | Other endpoint restrictions | Pattern count |
| --- | --- | --- | --- |
| private | private | d private/U, e private/V/Y | 6 |
| private | c | d,e both private | 1 |
| q | private | d private/U, e private/Y | 4 |
| q | c | d,e both private | 1 |

The two patterns with d=U,W*=q retain only the three zero-ear types.
The other ten patterns retain all eleven at this level, for `10×11+2×3=116`
necessary attachment/type rows per original complete contract. This is a
finite endpoint filter, not 116 realized sources or a complete treatment of
Γ-exterior stars. In particular every one of the eleven local types remains
when its four endpoint roles are all private.
