/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Enumeration

/-!
# SYM: relabelling the sealed interior vertices does not change the C5 interface

This file isolates the *labelling normalisation* rule that `scripts/c5_cell_reduced.py` calls `SYM`.
Nothing here mentions degrees (`R1`), separating cycles (`R2`), `K₆ = K₅` or the catalogue: it is the
pure invariance statement that the reduction is allowed to quotient by.

Setting.  A C5 cell is a graph on `Fin n` whose first five vertices are the ordered boundary `B`.
`relabel π G` renames the vertices of `G` by `π` (the pullback `G.comap π`), and `Sigma G B` is the set
of boundary colourings of `B` that extend to a proper four-colouring of `G`.

Contents.

* `Sigma_relabel` — **the main theorem**: if `π` fixes the boundary pointwise then
  `Sigma (relabel π G) B = Sigma G B`.  So the membership question "does this boundary pattern extend
  inward?" — the single bit of the enumerator's mask — is a property of the *unlabelled* interior,
  not of the numbering.  `sigma_iff_relabel` is the per-bit form.
* the ten-bit key of §5 — the reading of one bit and its orbit invariance, with the finite orbit
  facts reused from `Math/Enumeration.lean`.

Trust.  Every theorem below is an ordinary proof (`propext` / `Classical.choice` / `Quot.sound` only),
audited in `Math/SymRelabelAudit.lean`.  The finite orbit facts reused from `Math/Enumeration.lean`
(`colorReps` coverage, disjointness, minimality) are `native_decide` there, exactly as documented for
that file.

Attachment-mask transport and existence of sorted representatives for arbitrary `k` are proved
in `Math/SymNormalForm.lean`, which imports this file. Python implementation checks remain separate.
The orbit quotient of §5 is not formalised here.
-/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false

namespace FiveBoundary.Sym

open SimpleGraph

variable {n : ℕ}

/-! ### 1. Relabelling an interior

The vertices live on `Fin n` as everywhere else in the library (`Proper`, `Sigma`).  `relabel π G` is
the graph whose `π`-preimages carry `G`'s edges; in the enumerator's coordinates it is exactly the
mask permutation `interior_perm_maps` applied to the mask of `G`. -/

/-- Rename the vertices of `G` by `π` (pullback along `π`). -/
def relabel (π : Equiv.Perm (Fin n)) (G : SimpleGraph (Fin n)) : SimpleGraph (Fin n) :=
  G.comap π

@[simp]
theorem relabel_adj (π : Equiv.Perm (Fin n)) (G : SimpleGraph (Fin n)) (u v : Fin n) :
    (relabel π G).Adj u v ↔ G.Adj (π u) (π v) :=
  Iff.rfl

theorem relabel_one (G : SimpleGraph (Fin n)) : relabel 1 G = G := by
  ext u v
  simp [relabel]

/-- Relabelling is an action, so the relabellings of a graph form a group orbit. -/
theorem relabel_mul (π σ : Equiv.Perm (Fin n)) (G : SimpleGraph (Fin n)) :
    relabel (π * σ) G = relabel σ (relabel π G) := by
  ext u v
  simp [relabel]

/-- A colouring of `relabel π G` is a colouring of `G` precomposed with `π.symm`: the pullback moves
the neighbours of `u` to the neighbours of `π u`, so the two graphs differ only by the renaming. -/
theorem proper_relabel (π : Equiv.Perm (Fin n)) (G : SimpleGraph (Fin n)) (c : Fin n → Color) :
    Proper (relabel π G) c ↔ Proper G (fun x => c (π.symm x)) := by
  constructor
  · intro hc u v huv
    have h2 : (relabel π G).Adj (π.symm u) (π.symm v) := by
      rw [relabel]
      show G.Adj (π (π.symm u)) (π (π.symm v))
      rwa [Equiv.apply_symm_apply, Equiv.apply_symm_apply]
    exact hc (π.symm u) (π.symm v) h2
  · intro hc u v huv
    have h2 : G.Adj (π u) (π v) := by
      rw [relabel] at huv
      exact huv
    simpa only [Equiv.symm_apply_apply] using hc (π u) (π v) h2

/-- The boundary colouring is untouched because `π` fixes the boundary pointwise. -/
theorem boundaryColoring_relabel (π : Equiv.Perm (Fin n))
    (B : Fin 5 ↪ Fin n) (hB : ∀ i, π (B i) = B i) (c : Fin n → Color) :
    boundaryColoring B (fun x => c (π x)) = boundaryColoring B c := by
  show (fun x => c (π x)) ∘ B = c ∘ B
  have hcomp : (fun x => c (π x)) ∘ B = c ∘ (π ∘ B) := rfl
  rw [hcomp, show π ∘ B = B from funext hB]

/-! ### 2. The C5 interface of a cell is a relabelling invariant -/

/-- **SYM, main theorem.**  Relabelling vertices that are off the boundary leaves the complete
boundary colouring relation — the feasibility of every C5 boundary pattern — unchanged.  No hypothesis
on `π` beyond "fixes the boundary pointwise" is used: the interior may carry chords or any other
edges, and `n` need not be the enumerator's `5 + k`. -/
theorem Sigma_relabel {G : SimpleGraph (Fin n)} (π : Equiv.Perm (Fin n)) (B : Fin 5 ↪ Fin n)
    (hB : ∀ i, π (B i) = B i) :
    Sigma (relabel π G) B = Sigma G B := by
  have hfix : ∀ i : Fin 5, π.symm (B i) = B i := by
    intro i
    rw [show π.symm (B i) = π.symm (π (B i)) by rw [hB i]]
    exact Equiv.symm_apply_apply π (B i)
  ext b
  change (∃ c, Proper (relabel π G) c ∧ boundaryColoring B c = b) ↔
    (∃ c, Proper G c ∧ boundaryColoring B c = b)
  constructor
  · rintro ⟨c, hc, hbc⟩
    refine ⟨fun x => c (π.symm x), ?_, ?_⟩
    · exact (proper_relabel π G c).mp hc
    · rw [← hbc]
      exact boundaryColoring_relabel π.symm B hfix c
  · rintro ⟨c, hc, hbc⟩
    refine ⟨fun x => c (π x), ?_, ?_⟩
    · exact (proper_relabel π G (fun x => c (π x))).mpr (by simpa using hc)
    · rw [← hbc]
      exact boundaryColoring_relabel π B hB c

/-- Cell coordinates: `Fin (5 + k)`, boundary `firstBoundary`, interior vertices the private ones.
This is the exact situation of `c5_cell_enumerator.py`, where the interior universe is
`{5, …, 4+k}` and only interior vertices are permuted. -/
theorem Sigma_relabel_interior {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (π : Equiv.Perm (Fin (5 + k)))
    (hB : ∀ i : Fin 5, π (Fin.castLE (Nat.le_add_right 5 k) i)
      = Fin.castLE (Nat.le_add_right 5 k) i) :
    Sigma (relabel π G) (firstBoundary (Nat.le_add_right 5 k))
      = Sigma G (firstBoundary (Nat.le_add_right 5 k)) :=
  Sigma_relabel π (firstBoundary (Nat.le_add_right 5 k)) hB

/-- Feasibility of one boundary pattern is a relabelling invariant: the per-bit statement, in the form
the enumerator uses it (test one representative, read off one bit). -/
theorem sigma_iff_relabel {G : SimpleGraph (Fin n)} (π : Equiv.Perm (Fin n)) (B : Fin 5 ↪ Fin n)
    (hB : ∀ i, π (B i) = B i) (b : BoundaryColoring) :
    b ∈ Sigma (relabel π G) B ↔ b ∈ Sigma G B := by
  rw [Sigma_relabel π B hB]

/-- Any two boundary-fixing relabellings of one graph have the same interface: the cell's `Sigma`,
hence its ten-bit key, is determined by its unlabelled interior. -/
theorem Sigma_relabel_eq {G : SimpleGraph (Fin n)} (π σ : Equiv.Perm (Fin n)) (B : Fin 5 ↪ Fin n)
    (hπ : ∀ i, π (B i) = B i) (hσ : ∀ i, σ (B i) = B i) :
    Sigma (relabel π G) B = Sigma (relabel σ G) B := by
  rw [Sigma_relabel π B hπ, Sigma_relabel σ B hσ]

/-! ### 3. The attachment masks (formalised in `Math/SymNormalForm.lean`)

`SYM` in `c5_cell_reduced.py` reads the five-bit boundary-attachment mask of each private vertex and
keeps only graphs whose masks are non-increasing.  Two facts make that cut a pure labelling
normalisation:

* *transport*: relabelling moves the mask of a private vertex to the relabelled vertex, so the mask
  multiset is a relabelling invariant (sortedness of the indexed tuple is not);
* *existence*: every graph has such a relabelling — sort the private vertices by mask.

The importing module proves `attMask_relabel`, `attMask_relabel_interior`, and
`exists_sorted_relabel`, including preservation of `Sigma`, for every `k`.
`scripts/c5_sym_check.py` separately checks numeric mask order against production.
The SYM cut intersects every orbit; it is not an orbit union. Neither transport nor sorting
is needed by any theorem in this file. -/

/-! ### 5. The ten-bit key (specification; orbit machinery verified in Python)

The enumerator's `bits` is a ten-bit encoding of `Sigma`, one bit per `S₄` orbit of proper boundary
colourings, in the published `pattern_order`.  Formalising the encoding needs the orbit quotient:

* `OrbitEq b b'` iff a global recolouring carries `b` to `b'`; `Enumeration.colorOrbit` is the orbit as
  a `Finset`, and `colorReps` is the published list of ten representatives;
* the bit `j` is `1` exactly when the orbit of the tested boundary colouring is realized, i.e.
  `bit j b = 1 ↔ ∃ b' ∈ Sigma G B, OrbitEq b b'` — the reading stated in
  `docs/c5_cell_enumerator.md` §0.2;
* consequently the key depends only on the orbit, so testing the representative is lossless.

`Enumeration.lean` already proves, by `native_decide`, that the ten published patterns are distinct
(`color_reps_count`), cover all proper boundary colourings (`color_orbits_cover`) and are the
`S₄`-least element of their orbit (`color_reps_minimal`) — those are the finite facts the encoding
rests on.  The quotient-level statements above are audited computationally in
`scripts/c5_sym_check.py` and `scripts/c5_sigma_bridge.py` (whose `--orbit-sample` mode checks
`S₄`-orbit invariance of feasibility) and are recorded in `docs/c5_cell_enumerator.md` §0 and §8. -/

/-- The ten published orbit representatives, in the order shared by `pattern_order` in `cells.json`,
`REPS` in the enumerator and both relation libraries. -/
def patternOrder : List BoundaryColoring :=
  [![0,1,0,1,2], ![0,1,0,2,1], ![0,1,0,2,3], ![0,1,2,0,1], ![0,1,2,0,2],
   ![0,1,2,0,3], ![0,1,2,1,2], ![0,1,2,1,3], ![0,1,2,3,1], ![0,1,2,3,2]]

/-- The published list has exactly ten members, so it indexes the ten bits. -/
theorem patternOrder_length : patternOrder.length = 10 := by native_decide

/-- The published list is the library's `colorReps` as a set: the same ten representatives. -/
theorem patternOrder_toFinset : patternOrder.toFinset = colorReps := by native_decide

/-! ### 6. Summary of the SYM chain

**Proved here:** `Sigma_relabel` / `sigma_iff_relabel` / `Sigma_relabel_eq` — the ten-bit mask of a
cell is unchanged by relabelling its private vertices, i.e. feasibility per boundary pattern is a
property of the unlabelled interior.  That is the SYM equivalence itself, and it is what makes the
ten-bit key a function of the unlabelled graph.

**Proved in the importing `Math/SymNormalForm.lean`:** attachment-mask transport and existence
of a non-increasing representative (§3). The Python coordinate bridge and the orbit quotient
behind the ten-bit key (§5) retain their separate computational trust boundaries.

Nothing in this file mentions `R1`, `R2`, `K₆ = K₅` or the catalogue. -/

end FiveBoundary.Sym
