# Two-hole replacement control and independent signed-span work

This directory uses only the new exclusive audit's frozen previous audit
`frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c`. It retains the original ordered
frame `(x,y,a,b,c)`, all original exterior attachments including every additional
neighbour of n, and the complete source contract. The two-hole result below is a bounded
search control. A subsequent exact source obstruction is proved in
`ORBIT_LEMMA.md`:132 signed half-row counts cancel every surviving orbit
column and force the actual positive short-witness count to zero. That
argument excludes the named n>=6 source branch without constructing a
smaller bad. The unsuccessful replacement and numerical runs remain scoped
records and are not used for that theorem.

## Exact two-hole family

Delete the original `p,h,R` inside the induced seven-rim
`(a,b,q,L,u1,u2,n)`, and optionally replace the original r inside its six-rim
`(s,x,y,t,w,v)`. The latter is induced: the frozen core C11 is induced and the
full original x/y stars exclude all remaining nonconsecutive contacts. Each
hole is filled by a simple triangulation with zero, one, or two new interior
vertices. Every added edge is marked either equal (contract it) or unequal
(retain it). The entire extension is enumerated jointly; no marginal choices
are combined. Nonempty signatures cannot create loops on retained edges, and
the induced original rims rule out loops on original edges. The original frame
vertices remain distinct. Every exterior original edge is preserved through
the quotient, including all n attachments.

The left triangulation counts are42,330,4620; the right counts are14,84,1008.
The actual original d_a positive fibre has either left seven-word
`(0,1,2,1,0,2,1)` or `(0,1,2,1,2,0,1)`. Its right values have s=t=1,
`{x,y}={v,w}={2,3}`. Retain only relations admitting at least one such actual
restriction; preserving a specific restriction does not assert that that
restriction occurs in the source.

There are256 distinct retained left relations and82 right relations. The
completed cost is computed from actual quotient classes: on the left,
`number_of_classes - 7 - 3`; on the right, `number_of_classes - 6 - 1`.
Thus the combined strict candidates have total cost below k precisely when
the sum of these deltas is negative. There are14,656 such relation pairs.

The previous combined search excluded every left class containing both a and
u2 because it also covered n=5, where a-u2 is an original edge. This n>=6
branch has an induced seven-rim and admits those contractions. The complete
new family includes them. The earlier files `left-relations.json.gz`,
`right-contractions.json`, and `joint-supports.json` preserve the discovery
run with the inherited restriction; the `full-*` artifacts are the complete
family for the present branch.

For every one of the5951 frozen necessary-live C11 fibres, enumerate every
proper b,x,y assignment and its exact canonical five-frame row. Couple its
complete left seven-word and complete right six-word to the two local
relations. A candidate's possible negative supports are exactly the union
of these full cap assignments. No strict candidate in this family has all
three designated negative supports empty. This only limits the stated family
and sufficient zero-envelope test; it is not an arbitrary replacement theorem.

The maximal ten-row support masks on that same necessary-live set are:

| mask | number of strict relation pairs |
| --- | ---: |
| 863 | 256 |
| 1023 | 14382 |
| 943 | 4 |
| 959 | 7 |
| 1007 | 7 |

All five masks belong to the frozen K132 catalogue. Therefore applying only
the per-candidate support upper bound and membership in K132 cannot prune
this necessary-live set. These maximal masks are not asserted to occur on
one common actual source, and this observation does not decide stronger
joint count or common-geometry constraints.

Read-only exact replay is `python3 -B .../reduction/check.py`.
`full-left-relations.json.gz` retains all class lists, marked edges, faces,
full relation supports, and actual-positive restriction indices. The other
full artifacts retain the scoped negative result and complete mask histogram.
No numerical optimizer is used for these search conclusions.

## Signed-span lemma and numerical controls

`SPAN_LEMMA.md` proves independently by inclusion and exclusion that the actual
common core count vector belongs to the signed span of the1585 proper
noncrossing connectivity partitions. It also justifies the strict positive
short-witness sum z[5093]+z[5100].

`span_only.py` attempted an unbounded homogeneous optimization and returned
HiGHS status4 (solve error); it establishes nothing. The bounded independent
`span_normalized.py` run, with sum z=1, returned numerical optimum
`z[5093]+z[5100] ≈ 0.00026089523653626565`. This is a numerical diagnostic,
not a rational feasible certificate or actual source realization. It suggests
that the signed span plus the existing zero envelope alone is insufficient;
it must not be promoted to an exact theorem without a checked rational point.

`full_phase1.py` independently tests the full count cone with all ten required
positive quantities bounded below by one common variable t and sum z=1.
Its numerical output, whatever the solver status, is not an exclusion proof.
Only an independently checked exact separating identity could provide that.
