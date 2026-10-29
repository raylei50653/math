/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.ColoringElimination
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Finset.Image

/-!
# Exact finite-domain projection through bounded factor subfamilies

For one eliminated variable with finite domain `C`, failure of a common witness
is witnessed by at most `Fintype.card C` factors. Consequently the existential
projection of a conjunction equals the conjunction of all projections of such
bounded subfamilies. Every subfamily is evaluated on the same boundary row.

The empty subfamily is included, making the statement valid even for an empty
color type or an empty factor index type. The complete reconstruction fibre is
still the intersection of all original factor supports, not a collection of
independently chosen witnesses for the subfamilies.

These are relation theorems, with no planarity, Python-refinement, running-time,
or uniform arity bound for an entire elimination sequence asserted.
-/

namespace ColoringBoundedProjection

universe u v w

variable {C : Type u} [Fintype C] {I : Type v} {Y : Type w}

/-- A failed common witness has an obstruction of at most one factor per color.
The factor index type need not itself be finite. -/
theorem exists_small_obstruction (P : I → C → Prop)
    (h : ¬ ∃ c : C, ∀ i : I, P i c) :
    ∃ s : Finset I, s.card ≤ Fintype.card C ∧
      ¬ ∃ c : C, ∀ i ∈ s, P i c := by
  classical
  have hblocked : ∀ c : C, ∃ i : I, ¬ P i c := by
    simpa only [not_exists, not_forall] using h
  choose f hf using hblocked
  refine ⟨Finset.univ.image f, ?_, ?_⟩
  · calc
      (Finset.univ.image f).card ≤ (Finset.univ : Finset C).card :=
        Finset.card_image_le
      _ = Fintype.card C := Finset.card_univ
  · rintro ⟨c, hc⟩
    exact hf c (hc (f c) (Finset.mem_image.mpr ⟨c, Finset.mem_univ c, rfl⟩))

/-- Exact projection is the conjunction of all bounded subfamily projections.
The witnesses for different subfamilies may differ; finite-domain obstruction
extraction nevertheless guarantees a witness common to all original factors. -/
theorem exists_forall_iff_bounded_subfamilies (P : I → C → Prop) :
    (∃ c : C, ∀ i : I, P i c) ↔
      ∀ s : Finset I, s.card ≤ Fintype.card C →
        ∃ c : C, ∀ i ∈ s, P i c := by
  constructor
  · rintro ⟨c, hc⟩ s _
    exact ⟨c, fun i _ => hc i⟩
  · intro hs
    by_contra h
    obtain ⟨s, hcard, hbad⟩ := exists_small_obstruction P h
    exact hbad (hs s hcard)

/-- The complete historical fibre at one literal, shared boundary row. -/
def completeFibre (P : I → C → Y → Prop) (y : Y) : Set C :=
  {c | ∀ i : I, P i c y}

omit [Fintype C] in
/-- Membership still checks all original factors on that same boundary row. -/
theorem mem_completeFibre (P : I → C → Y → Prop) (y : Y) (c : C) :
    c ∈ completeFibre P y ↔ ∀ i : I, P i c y := Iff.rfl

/-- The bounded factor representation has exactly the nonempty complete fibres. -/
theorem completeFibre_nonempty_iff (P : I → C → Y → Prop) (y : Y) :
    (completeFibre P y).Nonempty ↔
      ∀ s : Finset I, s.card ≤ Fintype.card C →
        ∃ c : C, ∀ i ∈ s, P i c y :=
  exists_forall_iff_bounded_subfamilies (fun i c => P i c y)

/-- A full relation factors through one boundary row and its complete fibre.
Thus the bounded projection can be paired with this fibre without losing any
original solution or adding a spurious one. -/
theorem relation_iff_bounded_projection_and_fibre
    (P : I → C → Y → Prop) (y : Y) (c : C) :
    (∀ i : I, P i c y) ↔
      (∀ s : Finset I, s.card ≤ Fintype.card C →
        ∃ a : C, ∀ i ∈ s, P i a y) ∧ c ∈ completeFibre P y := by
  constructor
  · intro hc
    exact ⟨(exists_forall_iff_bounded_subfamilies (fun i a => P i a y)).mp
      ⟨c, hc⟩, hc⟩
  · exact fun h => h.2

/-- Four literal colors need all subfamilies of at most four factors. -/
theorem fourColor_projection_iff (P : I → Fin 4 → Y → Prop) (y : Y) :
    (∃ c : Fin 4, ∀ i : I, P i c y) ↔
      ∀ s : Finset I, s.card ≤ 4 →
        ∃ c : Fin 4, ∀ i ∈ s, P i c y := by
  simpa only [Fintype.card_fin] using
    (exists_forall_iff_bounded_subfamilies (fun i c => P i c y))

omit [Fintype C] in
/-- Restrict the witness universe to the colors supported by one anchor factor.
If that support has `r` colors, it suffices to check the anchor together with
every at-most-`r` subfamily of the other factors. The anchor support is for the
same fixed boundary row as all predicates in `P`. -/
theorem exists_anchor_iff_bounded_subfamilies (A : C → Prop)
    [Fintype {c : C // A c}] (P : I → C → Prop) :
    (∃ c : C, A c ∧ ∀ i : I, P i c) ↔
      ∀ s : Finset I, s.card ≤ Fintype.card {c : C // A c} →
        ∃ c : C, A c ∧ ∀ i ∈ s, P i c := by
  constructor
  · rintro ⟨c, hA, hP⟩ s _
    exact ⟨c, hA, fun i _ => hP i⟩
  · intro hs
    have hrestricted : ∀ s : Finset I,
        s.card ≤ Fintype.card {c : C // A c} →
          ∃ c : {c : C // A c}, ∀ i ∈ s, P i c.1 := by
      intro s hcard
      obtain ⟨c, hA, hP⟩ := hs s hcard
      exact ⟨⟨c, hA⟩, hP⟩
    obtain ⟨c, hP⟩ :=
      (exists_forall_iff_bounded_subfamilies (fun i (c : {c : C // A c}) => P i c.1)).mpr
        hrestricted
    exact ⟨c.1, c.2, hP⟩

/-- The domain-cardinality bound is sharp: omitting each color once gives no
common witness, while every strictly smaller subfamily still has a witness.
The statement also handles `q = 0` without a nonemptiness assumption. -/
theorem finite_domain_bound_tight (q : Nat) :
    (¬ ∃ c : Fin q, ∀ i : Fin q, c ≠ i) ∧
      ∀ s : Finset (Fin q), s.card < q →
        ∃ c : Fin q, ∀ i ∈ s, c ≠ i := by
  classical
  constructor
  · rintro ⟨c, hc⟩
    exact hc c rfl
  · intro s hcard
    have hlt : s.card < (Finset.univ : Finset (Fin q)).card := by
      simpa only [Finset.card_univ, Fintype.card_fin] using hcard
    obtain ⟨c, _, hc⟩ := Finset.exists_mem_notMem_of_card_lt_card hlt
    exact ⟨c, fun i hi hci => hc (hci.symm ▸ hi)⟩

end ColoringBoundedProjection
