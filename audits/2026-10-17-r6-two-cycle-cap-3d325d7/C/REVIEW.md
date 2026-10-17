# C review: exact SEP geometry and the short-cycle boundary

Frozen BASE: `3d325d7197aa05815c71bedc52c1b253d736c7bb`.
The independent audit accepts the user's section 4, with the precise
same-source and local-sector meanings made explicit in [PROOF](PROOF.md).

## Accepted statements and decisive checks

| Claim | Independent check | Status |
| --- | --- | --- |
| SEP iff an actual simple S_R cycle separates the two marked primal interiors | Retained dual components are exactly embedded S_R faces, including when S_R has bridges, isolates or several components; distinct faces are separated by a simple graph cycle | ACCEPT |
| The separating cycle must pass through z and separate zm from zp | The literal path `mid(mz)-z-p-mid(pq)` avoids S_R edges, and p has S_R-degree at most one; a separating cycle can meet it only at z | ACCEPT |
| q-centred version uses zm,zq | Reflect the full source and use q's degree-one property | ACCEPT |
| Every such S_R cycle is even | All its edges have the same nonzero alpha difference in one complete chi; summing in `F_2^2` forces even length | ACCEPT |
| A p-centred separating four-cycle cannot use zq | The actual z rotation forces its other neighbour A into L_a; it lifts to original proper C5 `(a,A,B,q,b)` with both p,h strictly inside | ACCEPT |
| For p-centred c0=5 every separating S_R cycle has length at least six | The full c-sector is beta0,q; g in M excludes z beta0 at the actual mz beta0 face; four-cycles using the sole remaining zq edge are excluded | ACCEPT |
| Reflected q-centred a0=5 length bound | Full reflection transports original sectors and the same complete colouring | ACCEPT |

## Quantifiers and qualifications retained

1. M is an actual ordinary `P101` matching, and C is its complete
   nonfacial seven-component containing f. Both cap-centre positions
   are retained. No smallest-oddness premise is used.
2. R is the **whole alpha class of one complete actual all-distinct
   colouring chi**. Each edge of the witness cycle must simultaneously
   belong to `M intersect R100` for that chi. An even cycle of M* alone,
   or edgewise alpha availability across different colourings, supplies
   no witness.
3. The local rays are actual darts in the fixed original quotient
   rotation. “Opposite sides” means the two open local sectors bounded
   by the two cycle darts at z, not an independently reordered link.
4. The original C5 in the four-cycle proof need only be simple and
   proper. Its possible chords do not weaken the frozen cap theorem.
   The rotation at the boundary vertex a forces p into its bounded cap;
   the actual ph edge then forces h into that same cap. The proof also
   excludes B=m using c0>=5 and the exact m-z common-neighbour sectors.
5. The at-least-six conclusion uses c0=5 on the p side, or a0=5 on the
   q side. It is not promoted to arbitrary opposite sectors, where a
   four-cycle can lift to an original C6.
6. The criterion and these exclusions do not use the new stronger
   cap-m contact lemma; they depend only on the frozen previous cap,
   sector and original proper-C5 authorities. The two inputs can thus
   be audited independently before integration.

## Verification scope

All 13 copied root inputs matched their recorded bytes and SHA256s.
No computational enumeration is needed for the planar proofs. The
embedded face argument explicitly includes the bridge case so that no
unjustified claim that every face boundary is a simple cycle enters the
criterion. No new Lean result, source realization, matching repair,
even-complement positivity, or general SEP existence claim is made.

The independent [B cross-review](../B/CROSS_REVIEW.md) accepts this proof,
including both face/local-ray directions with disconnected S_R, the
original C4 lift's exclusion of B=m, and the bounded ab-sector argument.
No changes were requested. This file records this worker's independent
paper audit and its exact accepted boundary.
