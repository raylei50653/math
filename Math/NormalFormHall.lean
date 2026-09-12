/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.AttachmentNormalForm
import Math.GeometryProfile

/-! # Hall rejection as a corollary of attachment normal form

Geometry is established independently in `AttachmentNormalForm`. The first rejection
corollary eliminates both triple witnesses that use the unique boundary position.
No classification of words or normal forms is used in the proof. -/

namespace FiveBoundary.Hall
open ColorDFA GeometryDFA Finset

/-- A full three-vertex boundary fan is incompatible with all three attachment degrees
being at least two. This is a consequence of the cut-necklace normal form. -/
theorem not_all_unique_of_degrees (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hd : ∀ k, 2 ≤ (linksOf w k).card) (u : Fin 5) : ¬ ∀ k, HitsUnique w u k := by
  intro hall
  have he : w u = univ := by
    apply eq_univ_of_forall
    intro k
    exact (mem_filter.mp (hall k)).2
  have hb := runOK_fan_card_le_two_of_degrees w ρ h hd u
  rw [he] at hb
  have : (univ : Finset (Fin 3)).card = 3 := by decide
  omega

/-- **First Hall corollary of geometry normal form.** Only the pair-pinned witness and
the triple witness hitting both repeated colour classes remain. This holds for every
accepting word, including words with a low-degree interior vertex. -/
theorem geoReject_iff_pair_or_opposite (w : Word) (ρ : Run) (h : RunOK w ρ) (u : Fin 5) :
    GeoReject w u ↔
      (∃ p q, p ≠ q ∧ SeesAll w u p ∧ SeesAll w u q) ∨
      (∀ k, HitsOdd w u k ∧ HitsEven w u k) := by
  constructor
  · rintro (ha | hb | hc | hd)
    · exact Or.inl ha
    · exact Or.inr hb
    · have hdeg : ∀ k, 2 ≤ (linksOf w k).card := fun k =>
        hits_two_degree_ge_two w u k (Or.inr (Or.inl (hc k)))
      exact False.elim (not_all_unique_of_degrees w ρ h hdeg u (fun k => (hc k).1))
    · have hdeg : ∀ k, 2 ≤ (linksOf w k).card := fun k =>
        hits_two_degree_ge_two w u k (Or.inr (Or.inr (hd k)))
      exact False.elim (not_all_unique_of_degrees w ρ h hdeg u (fun k => (hd k).1))
  · rintro (ha | hb)
    · exact Or.inl ha
    · exact Or.inr (Or.inl hb)

end FiveBoundary.Hall
