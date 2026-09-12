/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.AttachmentBudget
import Math.GeometryWitness

/-! # Structural reductions for the Z5 profile bound

The low-degree branch of the geometry-to-Hall bridge: if any interior vertex has at
most one attachment, only a pinned pair can reject, and all rejected unique positions
lie in the common neighbours of the other two interior vertices. `RunOK` bounds that
intersection by two. This file closes the low-degree branch; the complementary
all-degrees-at-least-two branch is closed in `GeoRejectBridge`, yielding the full
rejection-profile bound. -/

namespace FiveBoundary.Hall
open ColorDFA GeometryDFA Finset

/-- The set of rejected unique positions. -/
def rejectionSet (w : Word) : Finset (Fin 5) := univ.filter (GeoReject w)

theorem rejection_card_add_profile_card (w : Word) :
    (rejectionSet w).card + (threeProfile w).card = 5 := by
  rw [threeProfile_eq_geo, rejectionSet, card_filter_add_card_filter_not]
  simp

/-- Different classes of a three-colour C5 shape are disjoint (local position arithmetic). -/
theorem shape_positions_distinct (u a b : Fin 5)
    (ha : a = u + 1 ∨ a = u + 3) (hb : b = u + 2 ∨ b = u + 4) :
    u ≠ a ∧ u ≠ b ∧ a ≠ b := by
  revert u a b; decide +kernel

theorem seesAll_degree_ge_three (w : Word) (u : Fin 5) (k : Fin 3)
    (h : SeesAll w u k) : 3 ≤ (linksOf w k).card := by
  obtain ⟨hu, ha, hb⟩ := h
  obtain ⟨a, ha, hma⟩ : ∃ a, (a = u+1 ∨ a = u+3) ∧ a ∈ linksOf w k := by
    rcases ha with ha | ha
    · exact ⟨u+1, Or.inl rfl, ha⟩
    · exact ⟨u+3, Or.inr rfl, ha⟩
  obtain ⟨b, hb, hmb⟩ : ∃ b, (b = u+2 ∨ b = u+4) ∧ b ∈ linksOf w k := by
    rcases hb with hb | hb
    · exact ⟨u+2, Or.inl rfl, hb⟩
    · exact ⟨u+4, Or.inr rfl, hb⟩
  have hd := shape_positions_distinct u a b ha hb
  exact Finset.two_lt_card.mpr ⟨u, hu, a, hma, b, hmb, hd⟩

/-- Every two-class Hall witness needs at least two attachments at each vertex. -/
theorem hits_two_degree_ge_two (w : Word) (u : Fin 5) (k : Fin 3)
    (h : (HitsOdd w u k ∧ HitsEven w u k) ∨
      (HitsUnique w u k ∧ HitsEven w u k) ∨
      (HitsUnique w u k ∧ HitsOdd w u k)) : 2 ≤ (linksOf w k).card := by
  apply Finset.one_lt_card.mpr
  rcases h with ⟨ha, hb⟩ | ⟨hu, hb⟩ | ⟨hu, ha⟩
  · rcases ha with ha | ha <;> rcases hb with hb | hb
    · exact ⟨u+1, ha, u+2, hb, (shape_positions_distinct u _ _ (Or.inl rfl) (Or.inl rfl)).2.2⟩
    · exact ⟨u+1, ha, u+4, hb, (shape_positions_distinct u _ _ (Or.inl rfl) (Or.inr rfl)).2.2⟩
    · exact ⟨u+3, ha, u+2, hb, (shape_positions_distinct u _ _ (Or.inr rfl) (Or.inl rfl)).2.2⟩
    · exact ⟨u+3, ha, u+4, hb, (shape_positions_distinct u _ _ (Or.inr rfl) (Or.inr rfl)).2.2⟩
  · rcases hb with hb | hb
    · exact ⟨u, hu, u+2, hb, (shape_positions_distinct u (u+1) _ (Or.inl rfl) (Or.inl rfl)).2.1⟩
    · exact ⟨u, hu, u+4, hb, (shape_positions_distinct u (u+1) _ (Or.inl rfl) (Or.inr rfl)).2.1⟩
  · rcases ha with ha | ha
    · exact ⟨u, hu, u+1, ha, (shape_positions_distinct u _ (u+2) (Or.inl rfl) (Or.inl rfl)).1⟩
    · exact ⟨u, hu, u+3, ha, (shape_positions_distinct u _ (u+2) (Or.inr rfl) (Or.inl rfl)).1⟩

/-- A vertex of degree at most one excludes every triple Hall witness. -/
theorem geoReject_low_degree (w : Word) (u : Fin 5) (k : Fin 3)
    (hk : (linksOf w k).card ≤ 1) :
    GeoReject w u ↔ ∃ p q, p ≠ q ∧ SeesAll w u p ∧ SeesAll w u q := by
  constructor
  · rintro (h | h | h | h)
    · exact h
    · have := hits_two_degree_ge_two w u k (Or.inl (h k)); omega
    · have := hits_two_degree_ge_two w u k (Or.inr (Or.inl (h k))); omega
    · have := hits_two_degree_ge_two w u k (Or.inr (Or.inr (h k))); omega
  · exact Or.inl

theorem fin3_other_pair (k p q : Fin 3) (hp : p ≠ k) (hq : q ≠ k) (hpq : p ≠ q) :
    (p = k+1 ∧ q = k+2) ∨ (p = k+2 ∧ q = k+1) := by
  revert k p q; decide +kernel

/-- Rejected unique positions are shared neighbours of the remaining pair. -/
theorem rejectionSet_subset_common_of_low_degree (w : Word) (k : Fin 3)
    (hk : (linksOf w k).card ≤ 1) :
    rejectionSet w ⊆ linksOf w (k+1) ∩ linksOf w (k+2) := by
  intro u hu
  obtain ⟨p, q, hpq, hp, hq⟩ := (geoReject_low_degree w u k hk).mp (mem_filter.mp hu).2
  have hpk : p ≠ k := by intro he; subst p; have := seesAll_degree_ge_three w u k hp; omega
  have hqk : q ≠ k := by intro he; subst q; have := seesAll_degree_ge_three w u k hq; omega
  rcases fin3_other_pair k p q hpk hqk hpq with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · exact mem_inter.mpr ⟨hp.1, hq.1⟩
  · exact mem_inter.mpr ⟨hq.1, hp.1⟩

/-- **Low-degree branch of the bridge.** At most two positions can be rejected. -/
theorem runOK_rejection_le_two_of_low_degree (w : Word) (ρ : Run) (h : RunOK w ρ)
    (k : Fin 3) (hk : (linksOf w k).card ≤ 1) : (rejectionSet w).card ≤ 2 := by
  apply (card_le_card (rejectionSet_subset_common_of_low_degree w k hk)).trans
  exact runOK_common_card_le_two w ρ h (k+1) (k+2) (by
    have hn : ∀ k : Fin 3, k+1 ≠ k+2 := by decide
    exact hn k)

/-- A rejection set of size at least three forces the remaining degree branch. -/
theorem runOK_large_rejection_degrees (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hr : 3 ≤ (rejectionSet w).card) :
    (∀ k, 2 ≤ (linksOf w k).card) ∧ (∑ k, (linksOf w k).card) ≤ 8 := by
  refine ⟨?_, ?_⟩
  · intro k
    by_contra hk
    have := runOK_rejection_le_two_of_low_degree w ρ h k (by omega)
    omega
  · rw [← attachmentCount_eq_degree_sum]
    exact runOK_attachmentCount_le_eight w ρ h

/-- The low-degree branch accepts at least three of the five three-colour orbits. -/
theorem runOK_profile_ge_three_of_low_degree (w : Word) (ρ : Run) (h : RunOK w ρ)
    (k : Fin 3) (hk : (linksOf w k).card ≤ 1) : 3 ≤ (threeProfile w).card := by
  have := runOK_rejection_le_two_of_low_degree w ρ h k hk
  have := rejection_card_add_profile_card w
  omega

/-- The four possible degree multisets after the structural reduction. -/
def SmallDegreeCases (d : Fin 3 → ℕ) : Prop :=
  (∀ k, d k = 2) ∨
  (∃ k, d k = 3 ∧ ∀ j, j ≠ k → d j = 2) ∨
  (∃ k, d k = 4 ∧ ∀ j, j ≠ k → d j = 2) ∨
  (∃ k, d k = 2 ∧ ∀ j, j ≠ k → d j = 3)

/-- Arithmetic only: no attachment-word enumeration. -/
theorem smallDegreeCases_of_budget (d : Fin 3 → ℕ) (hlo : ∀ k, 2 ≤ d k)
    (hhi : (∑ k, d k) ≤ 8) : SmallDegreeCases d := by
  have h0 := hlo 0
  have h1 := hlo 1
  have h2 := hlo 2
  simp only [Fin.sum_univ_three] at hhi
  simp [SmallDegreeCases, Fin.forall_fin_succ, Fin.exists_fin_succ]
  omega

/-- All unclosed cases have degree multiset (2,2,2), (2,2,3), (2,2,4), or (2,3,3). -/
theorem runOK_large_rejection_cases (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hr : 3 ≤ (rejectionSet w).card) : SmallDegreeCases (fun k => (linksOf w k).card) := by
  obtain ⟨hlo, hhi⟩ := runOK_large_rejection_degrees w ρ h hr
  exact smallDegreeCases_of_budget _ hlo hhi

end FiveBoundary.Hall
