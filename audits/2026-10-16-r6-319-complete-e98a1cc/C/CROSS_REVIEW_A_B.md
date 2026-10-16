# C's independent paper review of A and B

BASE `e98a1cc1afd9a428600dcf4027d8138078c01650`.
This review uses the final A and B proofs of the present audit. It does
not assign source authority to their local controls.

## A: cofacial quotient and complete z fibres

PASS. The nonedge hypothesis for m=p is restricted to `a0>4`, with
the reflected restriction for m=q. Deleting z exposes the actual common
face before the identification is performed. The vertex count is
`k-3`, and the permitted five-cycle cap has exactly `k-5<k` interior
vertices. Only the original relative-minimality/nonempty-K132 premise
is used for colourability.

The complete quotient colouring corresponds to an entire colouring of
J-z. Its lift set is exactly the missing colours on the full original
link, including the empty set. With m=p, direct substitution in FJ gives
`{z,q}={v,w}` in each genuine lift; hence a nonempty fibre is precisely
the stated singleton. A never turns quotient nonemptiness into z-lift
nonemptiness. The empty-Az control calibrates this exact distinction.

The section-5 complete-colouring involution is sound. The original
AD component contains z,t and must contain v because its contrary
switch creates a forbidden boundary row. The Jordan crossing places
s,w in different BC components. Switching the actual s component is
an involution fixing all other boundary pins. The reverse direction
uses the corresponding forbidden ABCBC row. The pq palette statement
follows pointwise, since D does not move. The four removed rows are
already part of the frozen 22-row screen; no new source exclusion is
attributed to this replay.

## B: transition parity and its source localization

PASS. In B1 the f-containing component of `M0 xor N` is an actual
alternating cycle avoiding e,g. Its single flip gives ordinary101;
evenness is not assumed. B2 retains all paths obtained by deleting
the entire added matching from the old labelled beta/gamma cycles.
The endpoint-colour formula and the subsequent full-component sum
are correct, including when several surgeries meet one old cycle.
The transition count is even along each cyclic word, and every odd
new component contains a different transition edge. This proves the
bound without adding independent surgery counts.

B4's short-cycle classification is valid. In the actual cubic dual,
a chordless cycle of length at most five cannot have vertices on both
sides: each nonempty side needs three edges to its complement, while
only at most five unused incidences are available on the cycle.
First applying this to a triangle makes it facial, which the primal
minimum degree four excludes. A chord of a four- or five-cycle would
then create an excluded triangle. Thus the short cycles in question
are facial. A facial pentagon containing f can only be the p or q
face. The 101 bit partition excludes the endpoint with the same bit
as z, precisely as stated. A complementary five-cycle has at most
two removed-matching edges, so its odd transition count is exactly one.

C independently enumerated the entire planar control again, without
importing B's checker. For M111a with 8+8 complement there are exactly
four root-zero/alpha-one complete choices. All have t=2, one transition
on each of the new 9- and 7-cycles. M111b with 16-cycle complement has
two complete choices. Its symmetric difference to the unique ordinary
joint matching is itself a single twelve-edge alternating cycle,
with t=4: three transitions on the nine-cycle, one on the seven-cycle.
The six choices belong to two different 111 matchings. The corrected
B5 wording agrees with these exact counts.

The independent per-choice assignments, transitions, and placements
are retained in C's certificate under
`independent_transition_crosscheck`. Both A and B preserve their
explicit OPEN endpoint and the k+5 completed-source reconstruction
cost. Neither proof closes complete319.
