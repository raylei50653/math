# B cross-review of C: ACCEPT

Frozen BASE: `3d325d7197aa05815c71bedc52c1b253d736c7bb`.
Independently reviewed [C/PROOF.md](../C/PROOF.md) and
[C/REVIEW.md](../C/REVIEW.md) against the frozen sector classification,
actual previous cap geometry and original proper-C5 cap theorem.

## Exact criterion

The face/dual correspondence applies to the full spanning S_R,
including disconnected components, bridges and isolated vertices. Each
missing primal edge pq or mz has its interior in one open face; its
two dual endpoint faces are connected by its retained dual edge.
The f-containing C and the full g edge thus determine precisely those
two S_R faces. Distinct faces of a finite sphere graph are separated
by at least one simple graph cycle; repeated boundary vertices and
bridges do not require its whole face boundary to be simple.

The path `mid(mz)-z-p-mid(pq)` contains no S_R edge, and a simple S_R
cycle cannot use p because p has P-degree one. A separator therefore
meets the path only at z. The two specified rays being in opposite
local sectors is necessary and sufficient: the rest of the path
avoids the circle, so its endpoints lie on the local sides containing
those rays. The same reasoning applies with q as the low centre.
Thus both directions of the local criterion are valid, without an
assumption that S_R is connected.

All common edges have one actual alpha difference in a single complete
chi. Summing around the witness cycle forces even length. This does
not assert simultaneous realizability for arbitrary edges of M*.

## Four-cycle and degree-five conclusions

For a p-centred separating C4 containing zq, the fixed z rotation puts
its other z-neighbour A strictly within the a-sector before p. Both
centres are excluded from the cycle by their degree-one property.
The only additional quotient-vertex concern is B=m; the exact sector
intersection then forces q=beta0 and c0=4, contrary to the retained
cap bound c0>=5. All other A,B,q vertices and the AB,Bq edges lift
literally. The original cycle `(a,A,B,q,b)` is therefore simple and
proper. At its boundary edge ab, the bounded original cap is the
sector containing p; the actual edge ph forces h into that cap too.
The proper-C5 theorem permits at most one interior vertex and gives
the stated contradiction. Its no-chord premise is not needed.

When c0=5, the complete c-sector consists only of beta0,q. The actual
face `mz beta0`, already matched at g, excludes `z beta0` from M*.
The remaining separating dart is zq, so the C4 exclusion and evenness
give length at least six. Reflection transports the full same source
to the q-centred a0=5 conclusion. General opposite sectors may lift
to original C6, so no unrestricted length-six claim is justified.

## Scope

ACCEPT the exact z-cycle criterion, common-colour evenness, stated
zq/zp C4 exclusions, and precisely the c0=5/a0=5 short-cycle bounds.
No defect found requiring a mathematical change. These statements
construct neither an actual separating reference nor an alternating
matching repair. In B's two-total-cycle subcase, S_R is necessarily a
forest for every even reference, so C's criterion is necessarily
untriggered there; the two audits agree.

No finite source realization, new Lean theorem, positivity result or
complete319 exclusion follows. Source realizability remains
`not triggered`; the matching repair and global endpoints stay OPEN.
