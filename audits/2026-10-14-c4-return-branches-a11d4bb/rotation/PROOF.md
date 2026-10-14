# Returning after a whole-source rotation

2026-10-14. This is a conditional paper consequence of the original
[return exclusion](../../2026-10-14-c4-c5-recursion-fdd3e22/fibre/PROOF.md)
and [degree-six frontier](../../2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md).
It applies to the same globally minimum noncatalogue no4ct source, with
the original cyclic boundary `(x,y,a,b,c)` and `d_G(x)=d_G(y)=d_G(b)=4`.
All degrees below refer to the original G. No new graph realization or
Lean result is asserted.

## The necessary colour hypothesis travels with the graph

Write `y_i` for the entire fixed singleton-i fibre count. For an oriented
boundary edge `b_i b_(i+1)`, the rotated construction has

`(x',y',a',b',c')=(b_i,b_(i+1),b_(i+2),b_(i+3),b_(i+4))`.

Its forbidden target requires **both** `y_i=y_(i+1)=0`. Indeed the
[complete T-colouring bijection](../../2026-10-14-c4-triangle-core-b66f592/PROOF.md)
§3 identifies its target fibre with those two singleton fibres, after
one explicit common colour permutation on each disjoint branch.
If either singleton fibre is positive, that cut already has a successful
target colouring and the failure premises of the return proof do not hold.

When those fibres vanish and the three original boundary vertices
`b_i,b_(i+1),b_(i+3)` all have degree four, the same original-edge geometry,
source minimality, cap table, joint-fibre lemma, and return switch apply
with all names rotated. Nothing in these steps requires the rotated mask
to equal the chosen canonical numerical representative. It requires the
two vanishing singleton fibres and the globally transported source.

Let `e_i` be the actual apex of `b_i b_(i+1)`. Consequently

`y_i=y_(i+1)=0, d_G(b_i)=d_G(b_(i+1))=d_G(b_(i+3))=4 => d_G(e_i)>=6`.

If `d_G(e_i)=6`, the same degree-six frontier theorem also gives
`d_G(e_(i-1)),d_G(e_(i+1))>=6`. These are literal adjacent apex vertices;
the assertion is about full original colourings, not separately feasible
row projections.

## Which rotations are actually available

The original source singleton supports are empty for 932, `{4}` for 933,
and `{2,4}` for 941. The original apex order is `(r,t,p,q,s)`.
The original `h>=3` prevents a and c from both having degree four. Thus
the additional usable orientations in this fixed branch are exactly:

| Original full relation | Additional original degree premise | Consequence |
| --- | --- | --- |
| 932 or 933 | a=4 | p>=6; if p=6 then t,q>=6 |
| 932 | c=4 | q>=6; if q=6 then p,s>=6 |
| 941 | a=4 or c=4 | No additional return exclusion follows from rotation |
| 933 | c=4 | No q exclusion follows from rotation |

For the p row use `(x',y',a',b',c')=(a,b,c,x,y)`; its apex is p and the
adjacent apex vertices are t,q. For the q row use
`(x',y',a',b',c')=(b,c,x,y,a)`; its apex is q and the adjacent apex vertices
are p,s. The ya orientation would need both a and c four-degree, already
excluded by h. The cx orientation similarly cannot add a usable case.

The [existing conditional bound G28](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md)
says that both p,q>=6 imply k>=28. Therefore in the residual k<=27 domain:

- For 932/933 with a=4: necessarily q=5 and p>=7.
- For 932 with c=4: necessarily p=5 and q>=7.

These implications neither raise the common k>=23 bound nor exclude the
remaining low-degree configurations. In particular, ignoring the positive
singleton fibre would wrongly extend the first row to 941 or the second
row to 933.

## Verification and limits

[check_rotation.py](check_rotation.py) checks all ten labelled C5 rows,
all 24 common colour permutations, and the five actual rotations for
each of the three source masks. It enumerates the fixed-triangle target
directly and independently compares it to the transported singleton
support. Its negative controls retain the positive singleton obstructions
for 941/ab and 933/bc. This is a finite check of the colour hypothesis and
label transport. The degree and disk argument is the paper consequence
above; it is not a new source enumeration.

```sh
python3 -B audits/2026-10-14-c4-return-branches-a11d4bb/rotation/check_rotation.py --check
```
