# Independent A review of integration and C1

Reviewed root `PROOF.md` and `C/PROOF.md` on 2026-10-17 against frozen
BASE `5b9a7b3190c84bc10ff99608e372a9b4be57a0f6`.

1. The six-state local table agrees with an independent enumeration of
   the four unmatched cap vertices. The discarded seventh matching has
   a complete odd5-cycle and is incompatible with the same M0.
2. The cap difference has exactly two cut edges and one internal path,
   so it belongs to exactly one actual alternating cycle. Common marked
   edges e,k never occur on the reference difference, and choosing its
   unique h-cycle is exactly the forbidden reference subbatch operation.
3. The root complete-component descent is sound. On a component of
   `D-(M intersect M0)`, flipping all difference cycles replaces the whole
   old complement by the actual even F0; common boundary matching edges
   prevent complementary edges crossing the support. Outside components
   are retained. The oddness decrease, when positive, is at least2.
4. The source centre trichotomy is exhaustive: selected marked edges
   incident with a four-degree centre cannot lie on C and must be its
   unique chord. In the active-f case the omitted f lies on the
   four-face arc and hence on the cap-crossing difference cycle H.
5. C1 is a valid direct application of R6-MARKED-SIX. Distinct primal
   endpoints of e,f imply no common dual endpoint. Removing a nonchord
   endpoint a of f from X loses one spoke and gains two cycle edges,
   making an explicit six-cut retaining e and containing f. The other
   facial cycle of the cap survives in Y, and a whole old complementary
   cycle survives in the exterior. Both sides are cyclic.
6. No whole influence boundary can be the desired e,f cut in this
   source: the centre trichotomy puts at least one mark wholly in X,
   which remains inside every influence component containing C. A new
   successful cut must split X and supply any needed outer cycle from
   the actual source. This missing implication is correctly left OPEN.

No correctness issue remains in the reviewed integration statements.
The strict-descent sufficient criterion is full influence-component
avoidance of H, not the weaker mark-safety condition Q!=H. A previously
ambiguous sentence in A/PROOF.md has been corrected to make that
distinction explicit.
