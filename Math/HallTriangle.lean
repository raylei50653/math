/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.GeometryDFA
import Mathlib.Combinatorics.Hall.Basic

/-! The colour side of the triangle grammar, closed by Hall's theorem.

A K3 whose three vertices all have a common free colour `d` is uncolourable exactly when two
vertices are pinned to `{d}`, or all three lists sit inside `{d, x}` for one further colour `x`.
Specialised to the automaton, a three-colour boundary pattern is rejected iff one of the two
named combinatorial witnesses exists. Nothing here depends on the 32,768-word enumeration;
the final `native_decide` theorem is only a regression guard against the automaton. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
namespace FiveBoundary.Hall
open ColorDFA GeometryDFA Finset

/-- Two distinct vertices whose only available colour is the free colour `d`. -/
def PairPinnedToFourth (avail : Fin 3 → Finset Color) (d : Color) : Prop :=
  ∃ i j, i ≠ j ∧ avail i = {d} ∧ avail j = {d}

/-- All three lists lie in `{d, x}` for a single colour `x ≠ d`. -/
def TripleRestrictedToTwo (avail : Fin 3 → Finset Color) (d : Color) : Prop :=
  ∃ x, x ≠ d ∧ ∀ i, avail i ⊆ {d, x}

instance (avail : Fin 3 → Finset Color) (d : Color) : Decidable (PairPinnedToFourth avail d) :=
  inferInstanceAs (Decidable (∃ i j, i ≠ j ∧ avail i = {d} ∧ avail j = {d}))
instance (avail : Fin 3 → Finset Color) (d : Color) : Decidable (TripleRestrictedToTwo avail d) :=
  inferInstanceAs (Decidable (∃ x, x ≠ d ∧ ∀ i, avail i ⊆ {d, x}))

theorem pinned_of_subset_singleton {s : Finset Color} {d : Color} (hd : d ∈ s)
    (h : s ⊆ {d}) : s = {d} :=
  Subset.antisymm h (singleton_subset_iff.mpr hd)

/-- K3 list colouring with a common free colour: Hall's condition reduces to the two witnesses. -/
theorem k3_uncolorable_iff (avail : Fin 3 → Finset Color) (d : Color) (hd : ∀ i, d ∈ avail i) :
    (¬ ∃ t : Fin 3 → Color, Function.Injective t ∧ ∀ i, t i ∈ avail i) ↔
      PairPinnedToFourth avail d ∨ TripleRestrictedToTwo avail d := by
  rw [← Finset.all_card_le_biUnion_card_iff_exists_injective, not_forall]
  constructor
  · rintro ⟨s, hs⟩
    rw [not_le] at hs
    have hmem : ∀ i ∈ s, avail i ⊆ s.biUnion avail := fun i hi => subset_biUnion_of_mem avail hi
    have hs3 : #s ≤ 3 := (card_le_univ s).trans (by simp)
    rcases Nat.lt_or_ge #s 2 with h2 | h2
    · -- at most one vertex: the free colour already gives a representative
      exfalso
      obtain ⟨i, hi⟩ : s.Nonempty := card_pos.mp (by omega)
      have : d ∈ s.biUnion avail := hmem i hi (hd i)
      have := card_pos.mpr ⟨d, this⟩
      omega
    · rcases Nat.lt_or_ge #s 3 with h3 | h3
      · -- two vertices sharing a single available colour, necessarily `d`
        left
        obtain ⟨i, j, hij, rfl⟩ := card_eq_two.mp (show #s = 2 by omega)
        have hU : ({i, j} : Finset (Fin 3)).biUnion avail ⊆ {d} := by
          have hcard : #(({i, j} : Finset (Fin 3)).biUnion avail) ≤ 1 := by
            have := card_pair hij
            omega
          have hdU : d ∈ ({i, j} : Finset (Fin 3)).biUnion avail :=
            hmem i (by simp) (hd i)
          rw [card_le_one_iff_subset_singleton] at hcard
          obtain ⟨x, hx⟩ := hcard
          have : x = d := (mem_singleton.mp (hx hdU)).symm
          rwa [this] at hx
        exact ⟨i, j, hij, pinned_of_subset_singleton (hd i) ((hmem i (by simp)).trans hU),
          pinned_of_subset_singleton (hd j) ((hmem j (by simp)).trans hU)⟩
      · -- all three vertices inside at most two colours
        have hs : s = univ := eq_univ_of_card s (by simp; omega)
        subst hs
        have hcard : #(univ.biUnion avail) ≤ 2 := by
          have := hs
          simp only [card_univ, Fintype.card_fin] at this
          omega
        have hdU : d ∈ univ.biUnion avail := hmem 0 (mem_univ _) (hd 0)
        by_cases hx : ∃ x ∈ univ.biUnion avail, x ≠ d
        · right
          obtain ⟨x, hxU, hxd⟩ := hx
          refine ⟨x, hxd, fun i => (hmem i (mem_univ _)).trans ?_⟩
          have hsub : ({d, x} : Finset Color) ⊆ univ.biUnion avail := by
            intro c hc
            simp only [mem_insert, mem_singleton] at hc
            rcases hc with rfl | rfl <;> assumption
          have hcard' : #(univ.biUnion avail) ≤ #({d, x} : Finset Color) := by
            rw [card_pair (Ne.symm hxd)]; exact hcard
          exact (eq_of_subset_of_card_le hsub hcard').symm.subset
        · left
          push Not at hx
          have hU : univ.biUnion avail ⊆ {d} := fun c hc => by simpa using hx c hc
          exact ⟨0, 1, by decide,
            pinned_of_subset_singleton (hd 0) ((hmem 0 (mem_univ _)).trans hU),
            pinned_of_subset_singleton (hd 1) ((hmem 1 (mem_univ _)).trans hU)⟩
  · rintro (⟨i, j, hij, hi, hj⟩ | ⟨x, hx, h⟩)
    · refine ⟨{i, j}, ?_⟩
      rw [not_le, biUnion_insert, singleton_biUnion, hi, hj, union_self, card_singleton,
        card_pair hij]
      norm_num
    · refine ⟨univ, ?_⟩
      rw [not_le]
      calc #(univ.biUnion avail) ≤ #({d, x} : Finset Color) :=
            card_le_card (biUnion_subset.mpr (fun i _ => h i))
        _ = 2 := card_pair (Ne.symm hx)
        _ < #(univ : Finset (Fin 3)) := by simp

/-! ### Specialisation to the colour automaton -/

/-- Available colours of interior vertex `k` after the automaton has read the boundary. -/
def availOf (w : Word) (b : BoundaryColoring) : Fin 3 → Finset Color :=
  fun k => univ \ run w b k

theorem free_colour_available (w : Word) (b : BoundaryColoring) {d : Color}
    (hd : d ∉ usedColors b) (k : Fin 3) : d ∈ availOf w b k := by
  simp only [availOf, mem_sdiff, mem_univ, true_and, run_spec, mem_image, not_exists, not_and]
  intro j _ hj
  exact hd (mem_image.mpr ⟨j, mem_univ _, hj⟩)

/-- The colour side, closed: a boundary pattern leaving a colour `d` unused is rejected by the
compiled triangle gadget iff one of the two Hall witnesses exists. -/
theorem reject_iff_hall (w : Word) (b : BoundaryColoring) {d : Color} (hd : d ∉ usedColors b) :
    ¬ Accept (run w b) ↔
      PairPinnedToFourth (availOf w b) d ∨ TripleRestrictedToTwo (availOf w b) d := by
  rw [← k3_uncolorable_iff (availOf w b) d (free_colour_available w b hd)]
  simp [Accept, availOf]

/-- Same statement against the exact boundary relation of the compiled graph. -/
theorem not_mem_sigma_iff_hall (w : Word) (b : BoundaryColoring) (hb : Proper C5 b) {d : Color}
    (hd : d ∉ usedColors b) :
    b ∉ Sigma (graphOfEdges (Gadget.triangleEdges (linksOf w))) (firstBoundary (by omega)) ↔
      PairPinnedToFourth (availOf w b) d ∨ TripleRestrictedToTwo (availOf w b) d := by
  rw [sigma_iff_accept, ← reject_iff_hall w b hd]
  simp [hb]

/-- The witnesses read directly as "seen colours": pinned ⇔ the vertex has seen every colour
other than `d`; restricted ⇔ every vertex has seen both colours outside `{d, x}`. -/
theorem pinned_iff_sees_all (w : Word) (b : BoundaryColoring) {d : Color} (k : Fin 3)
    (hd : d ∉ run w b k) : availOf w b k = {d} ↔ ∀ c, c ≠ d → c ∈ run w b k := by
  simp only [availOf]
  constructor
  · intro h c hc
    by_contra hmem
    have : c ∈ univ \ run w b k := mem_sdiff.mpr ⟨mem_univ _, hmem⟩
    rw [h, mem_singleton] at this
    exact hc this
  · intro h
    ext c
    simp only [mem_sdiff, mem_univ, true_and, mem_singleton]
    constructor
    · intro hc; by_contra hne; exact hc (h c hne)
    · rintro rfl; exact hd

theorem restricted_iff_sees_two (w : Word) (b : BoundaryColoring) (d x : Color) :
    (∀ k, availOf w b k ⊆ {d, x}) ↔ ∀ k, ∀ c, c ≠ d → c ≠ x → c ∈ run w b k := by
  simp only [availOf, subset_iff, mem_sdiff, mem_univ, true_and, mem_insert, mem_singleton]
  constructor
  · intro h k c hcd hcx
    by_contra hmem
    rcases h k hmem with rfl | rfl
    · exact hcd rfl
    · exact hcx rfl
  · intro h k c hc
    by_contra hne
    push Not at hne
    exact hc (h k c hne.1 hne.2)

/-! ### Regression guard only: the closed colour semantics agree with the automaton on every
word and every three-colour representative. Not a source of truth for the theorems above. -/

def unusedColour (b : BoundaryColoring) : Color :=
  (List.finRange 4).find? (fun c => decide (c ∉ usedColors b)) |>.getD 3

theorem regression_guard : ∀ m : Fin 32768, threeReps.all (fun b =>
    let w := wordOfMask m.val
    let d := unusedColour b
    (!acceptB (run w b)) ==
      decide (PairPinnedToFourth (availOf w b) d ∨
        TripleRestrictedToTwo (availOf w b) d)) = true := by
  native_decide

end FiveBoundary.Hall
