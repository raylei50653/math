/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Mathlib.Data.Set.Lattice
import Mathlib.Data.Finset.Card
import Aesop
import Lean.Elab.Tactic.Omega

/-! Complete-relation repair criteria. Rows and candidate indices need not be finite.
The hypotheses concern actual sets of rows, not cardinalities or marginal projections.
No graph realization, topology, or finite certificate is assumed or certified here. -/
namespace FiveBoundary.CommonRepair

universe u v
variable {Ω : Type u} {Λ : Type v}

/-- All conditions preserve the same target relation in the same row space. -/
structure System (Ω : Type u) (Λ : Type v) where
  target : Set Ω
  base : Set Ω
  accept : Λ → Set Ω
  target_base : target ⊆ base
  faithful : ∀ i, target ⊆ accept i

namespace System

variable (s : System Ω Λ)

def delta : Set Ω := s.base \ s.target

def result (H : Set Λ) : Set Ω := {x | x ∈ s.base ∧ ∀ i ∈ H, x ∈ s.accept i}

def Repairs (H : Set Λ) : Prop := s.result H = s.target

def rejectors (x : Ω) : Set Λ := {i | x ∈ s.delta ∧ x ∉ s.accept i}

def Covers (H : Set Λ) : Prop := ∀ x ∈ s.delta, ∃ i ∈ H, i ∈ s.rejectors x

def ExactWitness (Q : Set Λ) : Prop := ∃ x ∈ s.delta, s.rejectors x = Q

def MinimalRepair (H : Set Λ) : Prop :=
  s.Repairs H ∧ ∀ L ⊆ H, s.Repairs L → L = H

def MaximalFailure (H : Set Λ) : Prop :=
  ¬ s.Repairs H ∧ ∀ L, H ⊆ L → ¬ s.Repairs L → L = H

theorem target_subset_result (H : Set Λ) : s.target ⊆ s.result H :=
  fun _ hx => ⟨s.target_base hx, fun i _ => s.faithful i hx⟩

theorem repairs_iff_covers (H : Set Λ) : s.Repairs H ↔ s.Covers H := by
  classical
  constructor
  · intro h x hx
    by_contra hn
    have hresult : x ∈ s.result H := by
      refine ⟨hx.1, fun i hi => ?_⟩
      by_contra hni
      exact hn ⟨i, hi, hx, hni⟩
    exact hx.2 (h ▸ hresult)
  · intro h
    apply Set.Subset.antisymm _ (s.target_subset_result H)
    intro x hx
    by_contra hn
    obtain ⟨i, hi, _, hni⟩ := h x ⟨hx.1, hn⟩
    exact hni (hx.2 i hi)

theorem repairs_mono {H L : Set Λ} (h : s.Repairs H) (hHL : H ⊆ L) :
    s.Repairs L := by
  rw [s.repairs_iff_covers] at h ⊢
  intro x hx
  obtain ⟨i, hi, hxi⟩ := h x hx
  exact ⟨i, hHL hi, hxi⟩

theorem not_repairs_iff_residual (H : Set Λ) :
    ¬ s.Repairs H ↔ (s.result H \ s.target).Nonempty := by
  classical
  constructor
  · intro h
    by_contra hn
    apply h
    apply Set.Subset.antisymm _ (s.target_subset_result H)
    intro x hx
    by_contra hnx
    exact hn ⟨x, hx, hnx⟩
  · rintro ⟨x, hx, hnx⟩ h
    exact hnx (h ▸ hx)

theorem witness_hits {Q H : Set Λ} (hw : s.ExactWitness Q) (h : s.Repairs H) :
    ∃ i ∈ H, i ∈ Q := by
  obtain ⟨x, hx, heq⟩ := hw
  obtain ⟨i, hi, hxi⟩ := (s.repairs_iff_covers H).mp h x hx
  exact ⟨i, hi, heq ▸ hxi⟩

/-- If adding any missing index repairs a failed complement, its residual rows
have exactly those missing indices as rejectors. -/
theorem residual_compl_eq (Q : Set Λ)
    (hadd : ∀ i ∈ Q, s.Repairs (insert i Qᶜ)) :
    s.result Qᶜ \ s.target = {x | x ∈ s.delta ∧ s.rejectors x = Q} := by
  classical
  ext x
  constructor
  · rintro ⟨hx, hnx⟩
    have hd : x ∈ s.delta := ⟨hx.1, hnx⟩
    refine ⟨hd, Set.Subset.antisymm ?_ ?_⟩
    · intro i hi
      by_contra hn
      exact hi.2 (hx.2 i hn)
    · intro i hi
      obtain ⟨j, hj, hjx⟩ := (s.repairs_iff_covers _).mp (hadd i hi) x hd
      rcases hj with rfl | hj
      · exact hjx
      · exact (hjx.2 (hx.2 j hj)).elim
  · rintro ⟨hd, heq⟩
    refine ⟨⟨hd.1, fun i hi => ?_⟩, hd.2⟩
    by_contra hn
    exact hi (heq ▸ (show i ∈ s.rejectors x from ⟨hd, hn⟩))

theorem exactWitness_of_compl (Q : Set Λ) (hfail : ¬ s.Repairs Qᶜ)
    (hadd : ∀ i ∈ Q, s.Repairs (insert i Qᶜ)) : s.ExactWitness Q := by
  obtain ⟨x, hx⟩ := (s.not_repairs_iff_residual _).mp hfail
  rw [s.residual_compl_eq Q hadd] at hx
  exact ⟨x, hx⟩

theorem maximalFailure_of_compl (Q : Set Λ) (hfail : ¬ s.Repairs Qᶜ)
    (hadd : ∀ i ∈ Q, s.Repairs (insert i Qᶜ)) : s.MaximalFailure Qᶜ := by
  classical
  refine ⟨hfail, fun L hL hn => Set.Subset.antisymm ?_ hL⟩
  intro i hi
  change i ∉ Q
  intro hiQ
  exact hn (s.repairs_mono (hadd i hiQ) (Set.insert_subset hi hL))

/-- For faithful systems, deletion-minimality and inclusion-minimality agree,
even for an infinite candidate set. -/
theorem minimalRepair_iff_deletions (H : Set Λ) :
    s.MinimalRepair H ↔ s.Repairs H ∧ ∀ i ∈ H, ¬ s.Repairs (H \ {i}) := by
  classical
  constructor
  · rintro ⟨hH, hmin⟩
    refine ⟨hH, fun i hi hd => ?_⟩
    have heq := hmin (H \ {i}) Set.sdiff_subset hd
    have : i ∈ H \ {i} := heq.symm ▸ hi
    exact this.2 rfl
  · rintro ⟨hH, hdel⟩
    refine ⟨hH, fun L hL hrep => Set.Subset.antisymm hL ?_⟩
    intro i hi
    by_contra hn
    apply hdel i hi
    apply s.repairs_mono hrep
    intro j hj
    exact ⟨hL hj, fun hji => hn (hji ▸ hj)⟩

/-- The independent degenerate branch uses no roles or nonempty witnesses. -/
theorem repairs_of_base_eq_target (h : s.base = s.target) (H : Set Λ) :
    s.Repairs H := by
  apply Set.Subset.antisymm _ (s.target_subset_result H)
  exact fun _ hx => h ▸ hx.1

theorem minimalRepair_of_base_eq_target (h : s.base = s.target) (H : Set Λ) :
    s.MinimalRepair H ↔ H = ∅ := by
  constructor
  · intro hm
    exact (hm.2 ∅ (Set.empty_subset H) (s.repairs_of_base_eq_target h ∅)).symm
  · rintro rfl
    exact ⟨s.repairs_of_base_eq_target h ∅,
      fun L hL _ => Set.Subset.antisymm hL (Set.empty_subset L)⟩

end System

/-- Named projections of one complete relation automatically give faithful
conditions. Each scope may have its own extension; no joint extension is inferred. -/
def projectionSystem {U C : Type*} (J P : Set (U → C)) (hJP : J ⊆ P)
    (scope : Λ → Set U) : System (U → C) Λ where
  target := J
  base := P
  accept i := {x | ∃ y ∈ J, ∀ u ∈ scope i, y u = x u}
  target_base := hJP
  faithful := fun _ x hx => ⟨x, hx, fun _ _ => rfl⟩

theorem mem_projection_result {U C : Type*} (J P : Set (U → C)) (hJP : J ⊆ P)
    (scope : Λ → Set U) (H : Set Λ) (x : U → C) :
    x ∈ (projectionSystem J P hJP scope).result H ↔
      x ∈ P ∧ ∀ i ∈ H, ∃ y ∈ J, ∀ u ∈ scope i, y u = x u := Iff.rfl

/-- Distinct named roles; the candidate type may contain arbitrary extra indices. -/
structure Roles (Λ : Type v) where
  A : Λ
  B : Λ
  T : Λ
  E : Set Λ
  AB : A ≠ B
  AT : A ≠ T
  BT : B ≠ T
  E_nonempty : E.Nonempty
  A_not_E : A ∉ E
  B_not_E : B ∉ E
  T_not_E : T ∉ E

namespace Roles

variable (r : Roles Λ)

def Template (H : Set Λ) : Prop :=
  (r.A ∈ H ∧ r.B ∈ H) ∨ ∃ e ∈ r.E, r.A ∈ H ∧ r.T ∈ H ∧ e ∈ H

def WitnessCoverage (s : System Ω Λ) : Prop :=
  s.ExactWitness {r.A} ∧ s.ExactWitness {r.B, r.T} ∧
  s.ExactWitness (insert r.B r.E) ∧ s.Covers {r.A, r.B} ∧
  ∀ e ∈ r.E, s.Covers {r.A, r.T, e}

theorem template_mono {H L : Set Λ} (h : r.Template H) (hHL : H ⊆ L) :
    r.Template L := by
  rcases h with ⟨ha, hb⟩ | ⟨e, he, ha, ht, hE⟩
  · exact Or.inl ⟨hHL ha, hHL hb⟩
  · exact Or.inr ⟨e, he, hHL ha, hHL ht, hHL hE⟩

theorem template_pair : r.Template {r.A, r.B} := by
  exact Or.inl ⟨by simp, by simp⟩

theorem template_triple {e : Λ} (he : e ∈ r.E) : r.Template {r.A, r.T, e} := by
  exact Or.inr ⟨e, he, by simp, by simp, by simp⟩

theorem repairs_iff_template (s : System Ω Λ) (h : r.WitnessCoverage s) (H : Set Λ) :
    s.Repairs H ↔ r.Template H := by
  classical
  obtain ⟨hA, hBT, hBE, hAB, hATE⟩ := h
  constructor
  · intro hH
    obtain ⟨a, ha, hqa⟩ := s.witness_hits hA hH
    have haH : r.A ∈ H := by simpa only [Set.mem_singleton_iff.mp hqa] using ha
    by_cases hb : r.B ∈ H
    · exact Or.inl ⟨haH, hb⟩
    · obtain ⟨t, ht, hqt⟩ := s.witness_hits hBT hH
      obtain ⟨e, he, hqe⟩ := s.witness_hits hBE hH
      have htH : r.T ∈ H := by
        simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hqt
        rcases hqt with rfl | rfl
        · exact (hb ht).elim
        · exact ht
      have heE : e ∈ r.E := by
        rcases hqe with rfl | heE
        · exact (hb he).elim
        · exact heE
      exact Or.inr ⟨e, heE, haH, htH, he⟩
  · intro hH
    rcases hH with ⟨ha, hb⟩ | ⟨e, he, ha, ht, heH⟩
    · apply s.repairs_mono ((s.repairs_iff_covers _).mpr hAB)
      simpa only [Set.insert_subset_iff, Set.singleton_subset_iff] using And.intro ha hb
    · apply s.repairs_mono ((s.repairs_iff_covers _).mpr (hATE e he))
      simpa only [Set.insert_subset_iff, Set.singleton_subset_iff] using And.intro ha ⟨ht, heH⟩

/-- The three missing-index sets are the minimal sets hitting every template. -/
theorem template_compl_obstructions (Q : Set Λ)
    (hQ : Q = {r.A} ∨ Q = {r.B, r.T} ∨ Q = insert r.B r.E) :
    ¬ r.Template Qᶜ ∧ ∀ i ∈ Q, r.Template (insert i Qᶜ) := by
  classical
  have hab := r.AB
  have hat := r.AT
  have hbt := r.BT
  have haE := r.A_not_E
  have hbE := r.B_not_E
  have htE := r.T_not_E
  obtain ⟨e, he⟩ := r.E_nonempty
  rcases hQ with rfl | rfl | rfl
  all_goals
    simp only [Template, Set.mem_compl_iff, Set.mem_insert_iff, Set.mem_singleton_iff]
    aesop

theorem witnessCoverage_of_classification (s : System Ω Λ)
    (h : ∀ H, s.Repairs H ↔ r.Template H) : r.WitnessCoverage s := by
  have witness : ∀ Q, (Q = {r.A} ∨ Q = {r.B, r.T} ∨ Q = insert r.B r.E) →
      s.ExactWitness Q := by
    intro Q hQ
    obtain ⟨hfail, hadd⟩ := r.template_compl_obstructions Q hQ
    exact s.exactWitness_of_compl Q (fun hR => hfail ((h _).mp hR))
      (fun i hi => (h _).mpr (hadd i hi))
  refine ⟨witness _ (Or.inl rfl), witness _ (Or.inr (Or.inl rfl)),
    witness _ (Or.inr (Or.inr rfl)), ?_, ?_⟩
  · exact (s.repairs_iff_covers _).mp ((h _).mpr r.template_pair)
  · intro e he
    exact (s.repairs_iff_covers _).mp ((h _).mpr (r.template_triple he))

/-- The full W/C equivalence, including the necessity of exact witnesses over ALL indices. -/
theorem witnessCoverage_iff_classification (s : System Ω Λ) :
    r.WitnessCoverage s ↔ ∀ H, s.Repairs H ↔ r.Template H :=
  ⟨fun h H => r.repairs_iff_template s h H, r.witnessCoverage_of_classification s⟩

theorem minimal_template_pair {H : Set Λ} (hH : r.Template H)
    (hsub : H ⊆ {r.A, r.B}) : H = {r.A, r.B} := by
  apply Set.Subset.antisymm hsub
  rcases hH with ⟨ha, hb⟩ | ⟨e, _, _, ht, _⟩
  · simpa only [Set.insert_subset_iff, Set.singleton_subset_iff] using And.intro ha hb
  · have : r.T = r.A ∨ r.T = r.B := hsub ht
    exact (this.elim r.AT.symm r.BT.symm).elim

theorem minimal_template_triple {H : Set Λ} {e : Λ} (he : e ∈ r.E)
    (hH : r.Template H) (hsub : H ⊆ {r.A, r.T, e}) : H = {r.A, r.T, e} := by
  apply Set.Subset.antisymm hsub
  rcases hH with ⟨_, hb⟩ | ⟨f, hf, ha, ht, hfH⟩
  · have : r.B = r.A ∨ r.B = r.T ∨ r.B = e := hsub hb
    rcases this with h | h | h
    · exact (r.AB h.symm).elim
    · exact (r.BT h).elim
    · exact (r.B_not_E (h.symm ▸ he)).elim
  · have : f = r.A ∨ f = r.T ∨ f = e := hsub hfH
    have hfe : f = e := by
      rcases this with h | h | h
      · exact (r.A_not_E (h ▸ hf)).elim
      · exact (r.T_not_E (h ▸ hf)).elim
      · exact h
    subst f
    simpa only [Set.insert_subset_iff, Set.singleton_subset_iff] using And.intro ha ⟨ht, hfH⟩

/-- All inclusion-minimal repairs, with no discarded or normalized indices. -/
theorem minimalRepair_iff (s : System Ω Λ) (h : r.WitnessCoverage s) (H : Set Λ) :
    s.MinimalRepair H ↔ H = {r.A, r.B} ∨ ∃ e ∈ r.E, H = {r.A, r.T, e} := by
  have hc := r.repairs_iff_template s h
  constructor
  · rintro ⟨hH, hmin⟩
    rcases (hc H).mp hH with ⟨ha, hb⟩ | ⟨e, he, ha, ht, heH⟩
    · exact Or.inl (hmin {r.A, r.B}
        (Set.insert_subset_iff.mpr ⟨ha, Set.singleton_subset_iff.mpr hb⟩)
        ((hc _).mpr r.template_pair)).symm
    · exact Or.inr ⟨e, he,
        (hmin {r.A, r.T, e}
          (Set.insert_subset_iff.mpr ⟨ha,
            Set.insert_subset_iff.mpr ⟨ht, Set.singleton_subset_iff.mpr heH⟩⟩)
          ((hc _).mpr (r.template_triple he))).symm⟩
  · rintro (rfl | ⟨e, he, rfl⟩)
    · exact ⟨(hc _).mpr r.template_pair,
        fun L hL hrep => r.minimal_template_pair ((hc L).mp hrep) hL⟩
    · exact ⟨(hc _).mpr (r.template_triple he),
        fun L hL hrep => r.minimal_template_triple he ((hc L).mp hrep) hL⟩

/-- A is the only condition present in every repair. -/
theorem forced_iff (s : System Ω Λ) (h : r.WitnessCoverage s) (i : Λ) :
    (∀ H, s.Repairs H → i ∈ H) ↔ i = r.A := by
  have hc := r.repairs_iff_template s h
  constructor
  · intro hf
    have hi : i = r.A ∨ i = r.B := hf _ ((hc _).mpr r.template_pair)
    rcases hi with hi | rfl
    · exact hi
    · obtain ⟨e, he⟩ := r.E_nonempty
      have hb : r.B = r.A ∨ r.B = r.T ∨ r.B = e :=
        hf _ ((hc _).mpr (r.template_triple he))
      rcases hb with hb | hb | hb
      · exact hb
      · exact (r.BT hb).elim
      · exact (r.B_not_E (hb.symm ▸ he)).elim
  · rintro rfl H hH
    rcases (hc H).mp hH with ⟨ha, _⟩ | ⟨_, _, ha, _, _⟩ <;> exact ha

theorem maximalFailure_iff (s : System Ω Λ) (h : r.WitnessCoverage s) (H : Set Λ) :
    s.MaximalFailure H ↔
      H = ({r.A} : Set Λ)ᶜ ∨ H = ({r.B, r.T} : Set Λ)ᶜ ∨ H = (insert r.B r.E)ᶜ := by
  classical
  have hc := r.repairs_iff_template s h
  have hm : ∀ Q, (Q = {r.A} ∨ Q = {r.B, r.T} ∨ Q = insert r.B r.E) →
      s.MaximalFailure Qᶜ := by
    intro Q hQ
    obtain ⟨hfail, hadd⟩ := r.template_compl_obstructions Q hQ
    exact s.maximalFailure_of_compl Q (fun hR => hfail ((hc _).mp hR))
      (fun i hi => (hc _).mpr (hadd i hi))
  constructor
  · rintro ⟨hfail, hmax⟩
    have hn : ¬ r.Template H := fun ht => hfail ((hc H).mpr ht)
    by_cases ha : r.A ∈ H
    · have hb : r.B ∉ H := fun hb => hn (Or.inl ⟨ha, hb⟩)
      by_cases ht : r.T ∈ H
      · right; right
        apply (hmax _ ?_ (hm _ (Or.inr (Or.inr rfl))).1).symm
        intro i hi hQi
        rcases hQi with rfl | he
        · exact hb hi
        · exact hn (Or.inr ⟨i, he, ha, ht, hi⟩)
      · right; left
        apply (hmax _ ?_ (hm _ (Or.inr (Or.inl rfl))).1).symm
        intro i hi hQi
        rcases hQi with rfl | rfl
        · exact hb hi
        · exact ht hi
    · left
      apply (hmax _ ?_ (hm _ (Or.inl rfl)).1).symm
      intro i hi hQi
      exact ha (Set.mem_singleton_iff.mp hQi ▸ hi)
  · rintro (rfl | rfl | rfl)
    · exact hm _ (Or.inl rfl)
    · exact hm _ (Or.inr (Or.inl rfl))
    · exact hm _ (Or.inr (Or.inr rfl))

/-- The full residual equalities identify all possible exact witnesses, not just
one arbitrarily chosen representative from each residual. -/
theorem obstruction_residual_eq (s : System Ω Λ) (h : r.WitnessCoverage s) (Q : Set Λ)
    (hQ : Q = {r.A} ∨ Q = {r.B, r.T} ∨ Q = insert r.B r.E) :
    s.result Qᶜ \ s.target = {x | x ∈ s.delta ∧ s.rejectors x = Q} := by
  apply s.residual_compl_eq
  intro i hi
  exact (r.repairs_iff_template s h _).mpr ((r.template_compl_obstructions Q hQ).2 i hi)

theorem repair_card_ge_two (s : System Ω Λ) (h : r.WitnessCoverage s)
    (H : Finset Λ) (hH : s.Repairs (H : Set Λ)) : 2 ≤ H.card := by
  classical
  rcases (r.repairs_iff_template s h _).mp hH with ⟨ha, hb⟩ | ⟨_, _, ha, ht, _⟩
  · have hs : ({r.A, r.B} : Finset Λ) ⊆ H :=
      Finset.insert_subset_iff.mpr ⟨ha, Finset.singleton_subset_iff.mpr hb⟩
    simpa [r.AB] using Finset.card_le_card hs
  · have hs : ({r.A, r.T} : Finset Λ) ⊆ H :=
      Finset.insert_subset_iff.mpr ⟨ha, Finset.singleton_subset_iff.mpr ht⟩
    simpa [r.AT] using Finset.card_le_card hs

/-- The unique repair with at most two conditions is the named pair {A,B}. -/
theorem repair_card_le_two_iff [DecidableEq Λ] (s : System Ω Λ)
    (h : r.WitnessCoverage s) (H : Finset Λ) :
    s.Repairs (H : Set Λ) ∧ H.card ≤ 2 ↔ H = {r.A, r.B} := by
  constructor
  · rintro ⟨hH, hcard⟩
    rcases (r.repairs_iff_template s h _).mp hH with ⟨ha, hb⟩ | ⟨e, he, ha, ht, heH⟩
    · have hs : ({r.A, r.B} : Finset Λ) ⊆ H :=
        Finset.insert_subset_iff.mpr ⟨ha, Finset.singleton_subset_iff.mpr hb⟩
      apply (Finset.eq_of_subset_of_card_le hs ?_).symm
      simpa [r.AB] using hcard
    · have hs : ({r.A, r.T, e} : Finset Λ) ⊆ H :=
        Finset.insert_subset_iff.mpr ⟨ha,
          Finset.insert_subset_iff.mpr ⟨ht, Finset.singleton_subset_iff.mpr heH⟩⟩
      have hae : r.A ≠ e := fun heq => r.A_not_E (heq.symm ▸ he)
      have hte : r.T ≠ e := fun heq => r.T_not_E (heq.symm ▸ he)
      have hthree : 3 ≤ H.card := by
        simpa [r.AT, hae, hte] using Finset.card_le_card hs
      omega
  · rintro rfl
    refine ⟨(r.repairs_iff_template s h _).mpr ?_, ?_⟩
    · exact Or.inl ⟨by simp, by simp⟩
    · simp [r.AB]

end Roles
end FiveBoundary.CommonRepair
