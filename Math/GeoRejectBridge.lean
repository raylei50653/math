/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.NormalFormHall

/-! # From attachment normal form to the rejection profile

The normal-form fan and common-neighbour bounds suffice: a degree-two interior
vertex confines rejection to its three non-neighbours. No word enumeration or
classification into observed shapes is used.
-/
namespace FiveBoundary.Hall
open ColorDFA GeometryDFA Finset

/-- The attachment budget forces a degree-two vertex in the nondegenerate branch. -/
theorem runOK_exists_degree_two (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hd : ∀ k, 2 ≤ (linksOf w k).card) : ∃ k, (linksOf w k).card = 2 := by
  have hb := runOK_attachmentCount_le_eight w ρ h
  rw [attachmentCount_eq_degree_sum, Fin.sum_univ_three] at hb
  by_contra hn
  push Not at hn
  have h0 := hd 0
  have h1 := hd 1
  have h2 := hd 2
  have n0 := hn 0
  have n1 := hn 1
  have n2 := hn 2
  omega

/-- A degree-two vertex cannot be incident to a rejected unique position.
A pair witness there would give a forbidden three-vertex fan. -/
theorem rejectionSet_subset_compl_of_degree_two (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hd : ∀ k, 2 ≤ (linksOf w k).card) (k : Fin 3)
    (hk : (linksOf w k).card = 2) : rejectionSet w ⊆ (linksOf w k)ᶜ := by
  intro u hu
  apply mem_compl.mpr
  intro huk
  rcases (geoReject_iff_pair_or_opposite w ρ h u).mp (mem_filter.mp hu).2 with
    ⟨p, q, hpq, hp, hq⟩ | ht
  · have hpk : p ≠ k := by
      intro he; subst p
      have := seesAll_degree_ge_three w u k hp
      omega
    have hqk : q ≠ k := by
      intro he; subst q
      have := seesAll_degree_ge_three w u k hq
      omega
    apply not_all_unique_of_degrees w ρ h hd u
    intro j
    have coverAll : ∀ k p q j : Fin 3, p ≠ k → q ≠ k → p ≠ q →
        j = k ∨ j = p ∨ j = q := by decide +kernel
    have cover := coverAll k p q j hpk hqk hpq
    rcases cover with rfl | rfl | rfl
    · exact huk
    · exact hp.1
    · exact hq.1
  · have := seesAll_degree_ge_three w u k ⟨huk, ht k⟩
    omega

/-- **Geometry-to-rejection bridge:** an accepting attachment word rejects at most
three of the five unique positions. -/
theorem runOK_rejection_le_three (w : Word) (ρ : Run) (h : RunOK w ρ) :
    (rejectionSet w).card ≤ 3 := by
  by_cases hd : ∀ k, 2 ≤ (linksOf w k).card
  · obtain ⟨k, hk⟩ := runOK_exists_degree_two w ρ h hd
    have hb := card_le_card (rejectionSet_subset_compl_of_degree_two w ρ h hd k hk)
    simpa [card_compl, hk] using hb
  · push Not at hd
    obtain ⟨k, hk⟩ := hd
    exact (runOK_rejection_le_two_of_low_degree w ρ h k (by omega)).trans (by omega)

/-- Equality makes the two attachments exactly the accepted unique positions. -/
theorem rejectionSet_eq_compl_of_three (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hr : (rejectionSet w).card = 3) (k : Fin 3) (hk : (linksOf w k).card = 2) :
    rejectionSet w = (linksOf w k)ᶜ := by
  have hd := (runOK_large_rejection_degrees w ρ h (by omega)).1
  exact eq_of_subset_of_card_le (rejectionSet_subset_compl_of_degree_two w ρ h hd k hk)
    (by simp [card_compl, hk, hr])

/-- At equality there is a unique degree-two vertex; the other degrees are three. -/
theorem runOK_three_rejection_degrees (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hr : (rejectionSet w).card = 3) :
    ∃ k, (linksOf w k).card = 2 ∧ ∀ j, j ≠ k → (linksOf w j).card = 3 := by
  obtain ⟨hd, hb⟩ := runOK_large_rejection_degrees w ρ h (by omega)
  obtain ⟨k, hk⟩ := runOK_exists_degree_two w ρ h hd
  have hn : ∀ j, j ≠ k → 3 ≤ (linksOf w j).card := by
    intro j hj
    have hjd := hd j
    by_contra hn
    have hj2 : (linksOf w j).card = 2 := by omega
    have he : linksOf w j = linksOf w k := compl_injective
      ((rejectionSet_eq_compl_of_three w ρ h hr j hj2).symm.trans
        (rejectionSet_eq_compl_of_three w ρ h hr k hk))
    have hc := runOK_common_le_one_of_degrees w ρ h hd j k hj
    rw [he, inter_self, hk] at hc
    omega
  refine ⟨k, hk, ?_⟩
  intro j hj
  have hjd := hn j hj
  have h0 := hd 0
  have h1 := hd 1
  have h2 := hd 2
  simp only [Fin.sum_univ_three] at hb
  have hn0 := hn 0
  have hn1 := hn 1
  have hn2 := hn 2
  fin_cases k
  · have h1 := hn 1 (by decide)
    have h2 := hn 2 (by decide)
    norm_num at hk hb
    fin_cases j
    · exact (hj rfl).elim
    · change (linksOf w 1).card = 3; omega
    · change (linksOf w 2).card = 3; omega
  · have h0 := hn 0 (by decide)
    have h2 := hn 2 (by decide)
    norm_num at hk hb
    fin_cases j
    · change (linksOf w 0).card = 3; omega
    · exact (hj rfl).elim
    · change (linksOf w 2).card = 3; omega
  · have h0 := hn 0 (by decide)
    have h1 := hn 1 (by decide)
    norm_num at hk hb
    fin_cases j
    · change (linksOf w 0).card = 3; omega
    · change (linksOf w 1).card = 3; omega
    · exact (hj rfl).elim

/-- Positions at which an attachment set meets both repeated classes. -/
def oppositePositions (S : Finset (Fin 5)) : Finset (Fin 5) :=
  univ.filter (fun u => (u + 1 ∈ S ∨ u + 3 ∈ S) ∧ (u + 2 ∈ S ∨ u + 4 ∈ S))

/-- Local C5 arithmetic: a nonadjacent pair meets both classes at at most one position.
Only two boundary indices are checked, not attachment words. -/
theorem nonadjacent_opposite_le_one (a b : Fin 5)
    (hn : ¬ ∃ t : Fin 5, ({a, b} : Finset (Fin 5)) = {t, t + 1}) :
    (oppositePositions {a, b}).card ≤ 1 := by
  revert a b hn
  decide +kernel

/-- The pair witness avoids a degree-two vertex, so it lies at a shared neighbour
of the other two vertices; the triple witness lies in its opposite positions. -/
theorem rejectionSet_subset_opposite_union_common (w : Word) (ρ : Run) (h : RunOK w ρ)
    (k : Fin 3) (hk : (linksOf w k).card = 2) :
    rejectionSet w ⊆ oppositePositions (linksOf w k) ∪
      (linksOf w (k + 1) ∩ linksOf w (k + 2)) := by
  intro u hu
  rcases (geoReject_iff_pair_or_opposite w ρ h u).mp (mem_filter.mp hu).2 with
    ⟨p, q, hpq, hp, hq⟩ | ht
  · have hpk : p ≠ k := by
      intro he; subst p
      have := seesAll_degree_ge_three w u k hp
      omega
    have hqk : q ≠ k := by
      intro he; subst q
      have := seesAll_degree_ge_three w u k hq
      omega
    apply mem_union.mpr ∘ Or.inr
    rcases fin3_other_pair k p q hpk hqk hpq with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
    · exact mem_inter.mpr ⟨hp.1, hq.1⟩
    · exact mem_inter.mpr ⟨hq.1, hp.1⟩
  · exact mem_union.mpr (Or.inl (mem_filter.mpr ⟨mem_univ _, ht k⟩))

/-- Equality forces the degree-two attachments to be adjacent on the original C5. -/
theorem runOK_three_rejection_adjacent (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hr : (rejectionSet w).card = 3) (k : Fin 3) (hk : (linksOf w k).card = 2) :
    ∃ t : Fin 5, linksOf w k = {t, t + 1} := by
  have hd := (runOK_large_rejection_degrees w ρ h (by omega)).1
  obtain ⟨a, b, _, hab⟩ := card_eq_two.mp hk
  by_contra hn
  have ho : (oppositePositions (linksOf w k)).card ≤ 1 := by
    rw [hab]
    apply nonadjacent_opposite_le_one
    simpa only [hab] using hn
  have hc := runOK_common_le_one_of_degrees w ρ h hd (k + 1) (k + 2) (by
    have hh : ∀ k : Fin 3, k + 1 ≠ k + 2 := by decide +kernel
    exact hh k)
  have hb := (card_le_card (rejectionSet_subset_opposite_union_common w ρ h k hk)).trans
    (card_union_le _ _)
  omega

/-- **Equality case of the bridge.** Three rejections form a cyclic three-interval,
and the degree multiset is (2,3,3). -/
theorem runOK_three_rejection_structure (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hr : (rejectionSet w).card = 3) :
    ∃ (k : Fin 3) (t : Fin 5),
      linksOf w k = {t, t + 1} ∧
      (∀ j, j ≠ k → (linksOf w j).card = 3) ∧
      rejectionSet w = {t + 2, t + 3, t + 4} := by
  obtain ⟨k, hk, hd⟩ := runOK_three_rejection_degrees w ρ h hr
  obtain ⟨t, ht⟩ := runOK_three_rejection_adjacent w ρ h hr k hk
  refine ⟨k, t, ht, hd, ?_⟩
  rw [rejectionSet_eq_compl_of_three w ρ h hr k hk, ht]
  have hc : ∀ t : Fin 5, ({t, t + 1} : Finset (Fin 5))ᶜ = {t + 2, t + 3, t + 4} := by
    decide +kernel
  exact hc t

/-- Colour semantics transfers the structural bound to at least two accepted orbits. -/
theorem runOK_profile_ge_two (w : Word) (ρ : Run) (h : RunOK w ρ) :
    2 ≤ (threeProfile w).card := by
  have := runOK_rejection_le_three w ρ h
  have := rejection_card_add_profile_card w
  omega

/-- The smallest accepted profile is an adjacent pair, in the original boundary labels. -/
theorem runOK_two_profile_adjacent (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hp : (threeProfile w).card = 2) : ∃ t : Fin 5, threeProfile w = {t, t + 1} := by
  have hr : (rejectionSet w).card = 3 := by
    have := rejection_card_add_profile_card w
    omega
  obtain ⟨k, hk, _⟩ := runOK_three_rejection_degrees w ρ h hr
  obtain ⟨t, ht⟩ := runOK_three_rejection_adjacent w ρ h hr k hk
  refine ⟨t, ?_⟩
  have he : threeProfile w = (rejectionSet w)ᶜ := by
    ext u
    simp [threeProfile_eq_geo, rejectionSet]
  rw [he, rejectionSet_eq_compl_of_three w ρ h hr k hk, compl_compl, ht]

/-- The normal-form statement of the bridge. -/
theorem normalForm_rejection_bound (w : Word) (h : AttachmentNormalForm w) :
    (rejectionSet w).card ≤ 3 ∧
      ((rejectionSet w).card = 3 → ∃ t : Fin 5,
        rejectionSet w = {t, t + 1, t + 2}) := by
  obtain ⟨ρ, hρ⟩ := (annulusAccept_iff_normalForm w).mpr h
  refine ⟨runOK_rejection_le_three w ρ hρ, ?_⟩
  intro hr
  obtain ⟨k, t, _, _, ht⟩ := runOK_three_rejection_structure w ρ hρ hr
  refine ⟨t + 2, ?_⟩
  simpa only [add_assoc, show (2 : Fin 5) + 1 = 3 from rfl,
    show (2 : Fin 5) + 2 = 4 from rfl] using ht

end FiveBoundary.Hall
