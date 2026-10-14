# Retained exploration and stopping point

The initial direct Kempe/Jordan route began from the existing ABABCBC
fibre. The available R mask13 switches return to the other allowed ABCB
sector, and the p-deletion mask14 has a nonempty rainbow fibre. No
legitimate sequence forcing an original empty fibre was proved. In
particular separate complete colourings ABABCBC and ABABCAB cannot be
treated as simultaneous assignments or assumed Kempe-connected. The
work therefore returned to actual faces and original small-cycle
geometry, without enlarging a necessary-condition closure model.

The first useful geometric observation was r-ell nonadjacency. It follows
from the original proper C5 `(y,a,p,ell,r)` if that edge were present,
using its forced interior t. This is an explicit consequence of already
adopted source geometry, and does not by itself enlarge the known class
of excluded minimum sources.

Before the stronger triple quotient in PROOF.md was noticed, the
following weaker genuine source exclusion was independently derived:
`p=5,a=5,m=5` is impossible. If these degrees hold, the original m link
is `(a,p,ell,v,t)`, and deleting x,y,p,m exposes the actual faces
`(z,s,r,t)` and `(z,q,ell,v,t)`, sharing zt. The original small-cycle
constraints make all displayed nonshared pins distinct. Contract z-r
in the first face and z-ell in the second. The independent triple
`{z,r,ell}` and strict size bound make the quotient source-colourable.
Normalize z=r=ell=A. Since t,v are distinct adjacent neighbours of m,
choose m outside their colours and A, then extend p. The R mask13
condition forces s=t=B. Thus m avoids B; if q!=B choose p=B, and if
q=B any legal p already has B in the pq palette. Both contradict the
ABAB pq condition. The separate r6 investigator derived the similarly
weaker exclusion `p=5,a=5,t=5`.

Both are subsumed by the final `p=5=>a>=6` theorem, which deletes no
additional vertex and uses only the original seven pins. They are not
listed as additional independent gains. The early local restoration
experiments are retained in [exploration-local.log](exploration-local.log)
as preliminary arithmetic, not final source certificates.

The authorized stopping condition is reached with a full arbitrary-size
exclusion of the previously open source subbranch p=5,a=5. The stronger
goal p=5 impossible has not been achieved. No larger abstract Kempe
model, higher-interface enumeration, or implication of source
realizability is introduced.
