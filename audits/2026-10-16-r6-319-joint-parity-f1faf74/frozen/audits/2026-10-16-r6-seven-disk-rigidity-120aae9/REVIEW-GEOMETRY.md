# Independent review of the five-odd-interior exclusion

Research BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`.
Reviewer: the matching/exterior branch, independent of both geometry
proof authors. Reviewed the complete [GEOMETRY](GEOMETRY.md) and
[RIGIDITY](RIGIDITY.md) paper arguments, the preceding seven-disk
GEOMETRY G1--G6, and the exact original-sector theorem C2 (including
C2.3) in the unchanged joint-zero C proof. No source or prior input
was modified during this review.

Verdict: **PASS, with the stated source-conditional scope**. The paper
proof excludes the entire stratum with exactly five odd complete-degree
interior vertices, irrespective of the number of even interior vertices.
Together with the adopted theorem, it gives I>=6 and |C|>=17. It does
not prove ordinary101 nonemptiness, all-source exclusion, a reduction,
Tait positivity or a Lean theorem.

## Checks of the logical steps

1. The equality case is forced, not assumed. With I=5 the inherited
   Delta identity and m-sector lower bound require all seven t values
   odd and Delta=2(1-epsilon). The m contribution uses all excess when
   m is absent; Delta=0 when it is present. Every non-m vertex therefore
   attains its exact parity-sensitive minimum. No bound on the total
   number of even interior vertices enters this argument.

2. A boundary m has degree eight and original degrees six/seven. The
   sector containing C has even original degree by its face-word
   equation, hence degree six and t_m=1. A boundary z cannot have t_z=3:
   that would leave only two exterior faces, while the two distinct mz
   faces and zpq are all exterior. For zpq, no tacit assumption on f's
   position is needed: if it were in C, all three T0 vertices would be
   on Q, and the prohibition of R-side Q chords would force a triangle
   in the simple seven-cycle. Thus zpq is outside R unconditionally.

3. Interior curvature is exactly five because every odd interior degree
   is five and every even interior degree is six. The disk identity
   gives sum t=13. Combined with the named-vertex bounds, precisely
   three ordinary boundary vertices have t=3. Their complete degree
   equals their R degree, leaving exactly one actual exterior triangular
   face. Consecutive centres would demand incompatible exterior faces
   on their common Q edge. The three ears therefore attach simultaneously
   to the same disk and leave a simple Q4. This is recognition in the
   unchanged embedding; it is not a replacement source.

4. Each ear is a zero face. Its two old Q edges meet an ordinary centre,
   hence neither is pq; the exact monochromatic-edge identity forces
   the opposite face to be zero. The possible exception at a boundary
   pq is consequently handled explicitly. No ear can be an f endpoint,
   and the earlier outside face zpq remains outside after filling.

5. The inducedness arguments are sound, including forced ears.
   RIGIDITY gives the shorter check: a chord would make the exterior
   exactly two actual triangles, with no exterior vertex. All six
   distinct T0 vertices remain on or outside Q4, so six vertices would
   have to occupy four boundary positions. GEOMETRY independently
   counts the remaining X faces; if two were filled, the two remaining
   faces belong to different induced forced pairs and cannot be the
   adjacent faces of a two-triangle disk. Neither argument assumes all
   original boundary chords were absent.

6. The four forced-ear cases are exhaustive. The e face mvw cannot be
   an ordinary-centred ear; only the other vw face can occur. Both mz
   faces cannot be ears because their two original two-edge Q arcs
   would close a four-cycle within Q. In the one-g case, mz alpha puts
   the other m ray in L_t; exact C2.3 forces the other z ray into L_c.
   The actual z interval through alpha in L_a then crosses zpq while
   avoiding mz beta. The beta case reverses those two sector labels.
   These are precisely the crossed alternatives of C2.3, rather than
   the weaker claim that a C4 merely meets a hub. The no-ear, e-only,
   and both-ear cases follow from the same exact sector statement or
   inducedness. Each yields a contradiction in the same original J.

## Evidence and scope boundaries

The new source exclusion is a paper result using the adopted exact
source geometry, global degree minima and original sectors. A synthetic
local factor-critical patch is not a globally minimum source, and its
existence is compatible with this theorem: the missing obligation is a
completion to the specified common exterior and equality conditions.
The finite patch checker supplements the paper proof but cannot establish
its arbitrary-size quantifier. Existing Lean build success similarly
does not formalize this new argument.

The matching interface keeps every ordinary lift and empty fibre. The
new I>=6 conclusion neither changes the same D-C nor implies that its
surviving interfaces are unrealizable. Any final report must continue to
state ordinary101, even-complement joint positivity and general source
exclusion as OPEN. No repair was needed to the reviewed final proof.

## Canonical proof cross-check

The initial canonical PROOF sections 1--7 were also checked against both
accepted geometry routes and MATCHING M1--M6. Its same-source quantifier
fixes one arbitrary maximum-cardinality 101 barrier throughout; no
separate exterior witnesses are combined. Its exterior101 empty-fibre
argument counts all s+1 singleton vertices against at most s S vertices.
Its even exterior-path theorem retains repeated-endpoint zero paths.
The 140 count is correctly restricted to eligible interior signatures
for an even111 join, with componentwise xor equations and actual
exterior support still required. The 420 ordinary-signature bound and
all full matching lifts and empty fibres are retained. No correction
was needed to those matching statements.

A subsequently proposed strengthening, in matching_EQUALITY.md, is an
original argument of this reviewer and is therefore NOT independently
approved by this review. It must receive review by another branch
before being adopted into the canonical theorem. It attempts to exclude
all I+B=12 cases by the same three-ear contradiction.
