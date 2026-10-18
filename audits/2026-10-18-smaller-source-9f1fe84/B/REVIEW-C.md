# Independent review of C's completed fan candidates

2026-10-18, BASE `9f1fe84f73aabfa87a33d28754633bae6bf0b707`.
Reviewed the final C/PROOF.md, C/check_bridge.py and C/certificate.json.
The claims are accepted within their stated conditional source domain.

The adjacent original degree-five pair has exactly the stated two common
neighbours: another would create a third facial triangle on their common
edge. The links therefore give a genuine six-rim disk, with both deleted
vertices internal and all original boundary vertices retained. Each fan
is drawn inside that disk. Suppressing a duplicate exterior edge keeps
the same colouring constraint. The completed vertex count is exactly
k-2; no J-to-G reconstruction is being hidden in this count.

The generic mapping `(A,B,Q,N)` checks all four active-f placements:
`(a,b,q,n_a)`, `(q,b,a,ell)`, `(c,b,p,n_c)`, `(p,b,c,ell_c)`.
In particular the p,n_a case reverses the actual rim order, rather than
identifying any attachments. Under the original accepted row 01232,
A,B,Q are three distinct colours in each case. The first deleted centre
then takes the fourth, and the second takes A or B, selecting one fixed
fan. This preserves the same full original witness and the same original
outer colour frame.

The inverse gate is exact: a full candidate colouring lifts if and only
if its four original neighbours of the first centre are not rainbow.
Necessity is immediate; sufficiency assigns the second centre the fan
root colour and the first centre a missing colour. Checking the rim
edges, fan chords and original centre edge verifies every adjacency.
The formula for all lifts retains the additional possible assignments,
not merely this chosen sufficient lift.

The Kempe contact lemma is valid for a complete colouring in a genuinely
rejected original row. If the indicated component avoids both T and all
outer vertices, switching it fixes the outer row and makes N equal T.
Only N among the four rainbow pins changes, giving the contradicted lift.
The specialized anchors also check: after removing the degree-five
centre, b has neighbours a,c and the surviving p/q. In the non-b-rooted
fan, no new b edge is added. For a=c, b is isolated in its two-colour
subgraph with N. In the palette containing colours 0,1, original edge
xy makes either anchor imply both. The 01021 p-side alternative is
{y,c}, while literal reflection gives {x,a}. These are necessary contacts
in one colouring; they do not yet produce disjoint paths or a contradiction.

I separately reconstructed all three completed control disks from the
recorded edge sets and oriented faces. The independent checker
[review_bridge_control.py](review_bridge_control.py) uses flat Cartesian
products of all private colours, rather than C's recursive variable
selection. It verifies sphere rotations at every vertex, face dart
incidences, the original ordered outer C5, and Euler's identity for G,
G_a and G_b. It reproduces all ten full-fibre hashes and counts:

| Graph | Interior vertices | Complete ten-row counts | Mask |
| --- | --- | --- | --- |
| G | 7 | 5,13,8,5,1,0,1,0,8,4 | 863 |
| G_a | 5 | 0,1,1,0,1,0,1,0,1,2 | 854 |
| G_b | 5 | 1,12,11,1,0,0,0,0,11,10 | 783 |

The review also directly restricts every original accepted full colouring
to its chosen candidate, and compares every candidate's complete old
lift fibre against the complete original graph fibre with all unchanged
vertices fixed. The results are saved in
[REVIEW-C-CONTROL.json](REVIEW-C-CONTROL.json); the complete actual
assignments, including every empty row, are additionally retained in
[REVIEW-C-FULL-FIBRES.json](REVIEW-C-FULL-FIBRES.json). A common S4 action
on an entire full colouring expands the ten canonical outer rows.

Read-only replay commands:

```
python3 -B audits/2026-10-18-smaller-source-9f1fe84/C/check_bridge.py --check
python3 -B audits/2026-10-18-smaller-source-9f1fe84/B/review_bridge_control.py
```

These are actual completed smaller control graphs, but control G has
nonempty fibres in the three target rejected rows and is not the
hypothetical minimum source. The report correctly stops at a conditional
pair of smaller candidates, an accepted-witness cover, and a precise
rainbow obstruction. Neither site coverage for every source nor the
three globally empty fibres on one accepted candidate has been proved.
