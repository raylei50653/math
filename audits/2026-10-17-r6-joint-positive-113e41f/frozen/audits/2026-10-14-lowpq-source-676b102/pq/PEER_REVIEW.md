# Independent review of the r6 collar lemma and adoption summary

Reviewed the present [r6 proof](../r6/PROOF.md), its direct original
[r6 transfer](../../2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md)
and [source geometry](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md),
and the parent [report](../REPORT.md). This review is limited to the
requested cycle geometry, reflection, arbitrary-j aliases, and faithful
adoption of the low-p theorem. No further source model was explored.

**Result: no blocking mathematical or scope error found.**

Reviewed content SHA-256:

- `r6/PROOF.md`: `53f2deec25dc35797027554c69a21157bef154df9ab3c831b291a26bfd79163e`
- `REPORT.md`: `030e6712300555761ba7a91a0c4499b5bfa2df4ce9300013b0a561159b42bbe6`

## 1. Arbitrary original a-neighbour j

The lemma quantifies over original inner neighbours j of a with j!=t.
Being inner already excludes every original boundary vertex, including
y and a. The original apex contact theorem excludes j=r and j=s:
r's boundary contacts are exactly x,y, and s's are exactly c,x.
The actual r fan makes v,w distinct original inner neighbours of r,
different from s,t. If either were adjacent to a, its image would be
an additional common neighbour of z and r in R, contradicting
`N_R(z) intersect N_R(r)={s,t}`. Therefore j is neither v nor w.

Both cycles `(r,y,a,j,v)` and `(r,y,a,j,w)` consequently have five
distinct original vertices. They differ from the original B because
they contain r. The proof is valid for j=p as well as every extra
original inner neighbour of a; it does not silently assume j is a
new pin different from p. The c-side aliases follow by the same literal
reflection. No unintended j degree hypothesis is present.

## 2. The bounded sides of the two cycles

The original boundary edge ya has its exterior side outside G. Thus
the bounded cycle side is the internal side at ya. The original
y-neighbour order `(a,t,r,x)` places the triangular face ytr on this
bounded side of the edge yr. Following this same side of yr to r
fixes the sector unambiguously; it is not independently chosen at r.

For C_v the bounded r-sector runs from y to v through t,w in the
actual fan `(x,y,t,w,v,s)`. Both t and w are off the cycle by the
alias exclusions above, so both are strictly inside. A proper original
C5 cannot contain these two vertices under the adopted small-cap
theorem. This proves jv is absent.

For C_w the corresponding bounded r-sector runs from y to w through
t. Hence t is strictly inside. The small-cap theorem gives a singleton
W5 centre t, with its entire original neighbourhood the five cycle
vertices. In particular its original degree would be five, contradicting
the established r=6=>t>=6. This proves jw is absent. No appeal to a
boundary marginal, quotient face, or colouring witness is hidden in
either argument. Possible extra cycle chords do not evade the
small-cap theorem.

## 3. Reflection and precise exceptions

The full permutation `(x,y),(a,c),(p,q),(s,t),(v,w)` sends the r fan to
its reversed cyclic order. It sends C_v to `(r,x,c,j',w)`, whose bounded
sector contains s,v, and C_w to `(r,x,c,j',v)`, whose bounded sector
contains s. Therefore the reflected pair excludes j'w directly and
j'v by the contradiction s=5 versus s>=6, exactly as stated.

The exceptions t and s are necessary: tw and sv are mandatory fan
edges. The lemma deliberately says nothing about a vertex that is
not an original a/c neighbour, in particular it does not exclude
ell-v or ell-w. In the low-p specialization am is a literal original
link edge, and the existing p=5=>a>=5 theorem excludes m=t. Thus the
specialization to m-v,m-w is valid. The corresponding q-link n statement
has the same scope.

## 4. Accuracy of the parent report

The report accurately states the main new theorem p=5=>a>=6 and its
reflection q=5=>c>=6 under the fixed original x,y,b-degree-four source
contract. Its derivation uses the independent class {z,r,ell}, the
actual two-face embedded tree, the k-4 strict cap budget, and every
legal p lift on one complete D colouring. It restores the two original
designated faces and records both possible xy orders.

The report correctly distinguishes separately existing ABABCBC and
ABABCAB full fibres from a single colouring satisfying both assignments.
It also labels ell-r nonadjacency as an explicit consequence of old
source geometry, counts the weaker a=5,m=5 and a=5,t=5 work only as
contained checks, and preserves the OPEN states p5a>=6, r6p5, r6q5,
mask319, the higher-r branches, and general T/T0. It does not turn the
new degree bound into p,q>=6 or a general k>=28 theorem.

The claimed local 4^7/full-lift counts agree with the independently
replayed pq certificate. Its account of paper reasoning, finite
arithmetic, and existing Lean-library build keeps the evidence layers
separate. No edits to the reviewed files were necessary.
