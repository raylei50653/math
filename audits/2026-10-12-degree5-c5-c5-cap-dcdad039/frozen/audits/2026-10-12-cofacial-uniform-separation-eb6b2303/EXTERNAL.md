# External theorem boundary

Verified against the primary paper on 2026-10-12:

- Zdenek Dvorak and Bernard Lidicky, *Coloring count cones of planar graphs*,
  arXiv:1907.04066v2 (2021 version; published in J. Graph Theory 100 (2022)).
- Primary source: https://arxiv.org/pdf/1907.04066v2
- Corollary 20, printed page 16: Conjecture 8 holds for plane near-cubic graphs
  with strictly fewer than 30 vertices. The strict bound is the theorem's
  statement; do not replace it with the less precise introductory prose.
- Section 1 explicitly permits parallel edges and loops. The normal form proved
  in this audit is a simple primal graph; its dual is interpreted in the paper's
  near-cubic category.
- Observation 3, printed page 3, identifies extension counts for a fixed primal
  boundary assignment with those for its dual edge precoloring. Four primal
  boundary assignments map to each edge precoloring; that does not multiply the
  fixed-assignment extension count.
- Section 3, Conjecture 9, printed page 9, is the equivalent inequality
  `3 * sum(a-counts) >= sum(b-counts)` for boundary degree five. The repository's
  frozen count-cone bridge identifies these with the five singleton counts and
  the five repeated-pair counts, respectively.

The cited paper's computational proof/certificates are an external dependency;
they were not reproduced in this audit. This audit does not claim that the
unbounded Conjecture 8 or Conjecture 9 has been proved, nor does it claim to have
surveyed all later literature.

## Application to this audit

For a plane near-triangulation with outer cycle length five and `k` interior
vertices, Euler gives `2*k+4` dual vertices. Thus `k <= 12` implies fewer than
30 dual vertices. The new paper argument must establish a near-triangulated
minimum counterexample **without increasing k** before using this inequality
for arbitrary disk cells. The old completion-with-hubs argument alone does not
supply this implication.

This application is a new inference from the local normal-form argument and the
cited theorem, not a theorem attributed verbatim to the cited authors.
