# Independent C review of B

Reviewed `../B/PROOF.md`, the patch definitions and the complete-family
argument, and replayed `../B/check_patches.py --check ../B/patches.json`
read-only. An initial invocation omitted the required certificate argument
and exited at argparse without running any checks; the corrected replay
below completed.

The fixed-rim five-cap lift is sound: the fan root is a valid h colour,
and u has a colour missing from three fixed neighbours. The support
subset and lost two rows retain their stated local rim ordering.

The paper classification of every zero/one-inner-vertex C5 patch is
sound. The two missing three-colour rows require the stated chord
disjunctions; crossing excludes one combination. Each remaining wrong
combination blocks a one-vertex realization of the required four-colour
test because the needed unique-colour contacts lie on opposite sides
of a present chord. Presence of both fan chords partitions the disk into
triangles and makes every one-vertex extension possible.

The C6 enumeration is correctly limited to fixed named rim, no
identification and at most one interior vertex. Completing each such
simple plane graph to a triangulation on its same vertices and taking
all subgraphs is a complete search for this family. It does not establish
the stronger statement against source-conditioned exterior relations.
Read-only replay passed, including all exact certificate comparisons.

One wording correction was communicated to B: an induced rim in the
patch K does not exclude an edge between the same rim vertices drawn
in an arbitrary exterior E. The contextual construction must suppress
a duplicate if necessary. This changes no proper-colouring relation
and does not affect the finite cap proof or the operation-family result.

The original six-rim lift in C is independently necessary: the sound
pentagon fan cannot bypass the deleted original neighbour b. C's
rainbow gate is consistent with B's complete fixed-rim C6 obstruction.
No smaller completed bad source or full minimum-source realization is
asserted by this review.
