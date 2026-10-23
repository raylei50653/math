# Root independent review: C9 contact geometry

2026-10-23. This note records review reasoning, not a new source certificate.
The source is the globally minimal no4ct complete-932, h=4 original disk
of the T2 audit; all original C9 contacts, rotations and attachments remain.

The existing T2 geometry already classifies contact sets: distances 2 and 3
are forbidden; each allowed triple is A_i={i,i+1,i+5} modulo 9. The new
claim to review is simultaneous compatibility, not that old classification.

An independent exhaustive check of all 36 pairs A_i,A_j found a pair of
four distinct alternating terminals in every case. The paths through the
two distinct face-third vertices have disjoint interiors, which contradicts
the disk crosscut lemma. Shared unselected boundary contacts do not affect
the argument because the selected four endpoints are distinct. Thus at
most one of the nine actual face-third vertices can have its opposite contact.
An arbitrary triple-contact vertex is the actual face-third vertex of its
adjacent C9 pair, since the original C3 has empty bounded side.

For the proposed lower bounds, the important sealing checks are:

- If m=9 and there is no triple contact, the nine face-third vertices
  exhaust the interior. Every C9 vertex has exactly its two prescribed
  interior neighbors; triangulation seals an inner 9-cycle. A triangulated
  9-gon has ears, giving an original interior vertex degree four.
- If a triple exists, its three arms partition the disk into the original
  triangular face and two induced C6 cells. Each cell contains four distinct
  face-third vertices from its four original C9 edges. If these are all
  its interior vertices, they and the triple center bound a triangulated
  pentagon. At least one ear differs from the center, again giving a
  complete original degree-four star. Therefore each cell needs at least
  five strict interior vertices, so m>=11 in the triple case.

These are conditional structural lower bounds. The current inherited
k>=23 remains stronger numerically. No general 932 exclusion, new source
realization, or Lean result follows.
