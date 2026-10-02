/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.NamedRepairCore

/-! Concrete repair instances for the two original private-interior cores.
All colour relations are literal named projections. The selected mixed frame
family is explicit; no disk embedding or frame completeness is asserted. -/
namespace FiveBoundary.NamedRepair

open CommonRepair

set_option maxRecDepth 16384

/-- Full literal projections; every lift is to the same original graph. -/
def Accept (rev : Bool) (scope : Finset (Fin 8)) (b : Row) : Prop :=
  ∃ c ∈ J rev, ∀ u ∈ scope, c u = b u

def frame₁ : Finset (Fin 8) := {0,4,3,2,6}
def frame₂ (rev : Bool) : Finset (Fin 8) := {source rev,1,other rev,7,5}

def P (rev : Bool) : Set Row := {b | Accept rev frame₁ b ∧ Accept rev (frame₂ rev) b}

theorem j_subset_p (rev : Bool) : J rev ⊆ P rev :=
  fun b hb => ⟨⟨b, hb, fun _ _ => rfl⟩, ⟨b, hb, fun _ _ => rfl⟩⟩

def system (rev : Bool) : System Row Scope :=
  projectionSystem (J rev) (P rev) (j_subset_p rev) (fun s => (s.val : Set (Fin 8)))

theorem scope_count : Fintype.card Scope = 70 := by decide +kernel

def scopeA : Scope := ⟨{0,1,2,3}, by decide⟩
def scopeB (rev : Bool) : Scope := ⟨{source rev,5,6,7}, by cases rev <;> decide⟩
def scopeT : Scope := ⟨{0,2,5,6}, by decide⟩
def scopesE (rev : Bool) : Set Scope := {s | 6 ∈ s.val ∧ 7 ∈ s.val ∧ s ≠ scopeB rev}

instance (rev : Bool) (s : Scope) : Decidable (s ∈ scopesE rev) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))

def roles (rev : Bool) : Roles Scope where
  A := scopeA
  B := scopeB rev
  T := scopeT
  E := scopesE rev
  AB := by cases rev <;> decide
  AT := by decide
  BT := by cases rev <;> decide
  E_nonempty := ⟨⟨{0,1,6,7}, by decide⟩, by cases rev <;> decide⟩
  A_not_E := by cases rev <;> decide
  B_not_E := by cases rev <;> simp [scopesE]
  T_not_E := by cases rev <;> decide

/-- Necessary information read on the two selected mixed frames. -/
def PGuard (rev : Bool) (b : Row) : Prop :=
  b 0 ≠ b 1 ∧ b 1 ≠ b 2 ∧ b 2 ≠ b 3 ∧ b 3 ≠ b 4 ∧ b 0 ≠ b 4 ∧
  b 5 ≠ b (source rev) ∧ b (source rev) ≠ b 6 ∧ b 6 ≠ b (other rev) ∧
  b (other rev) ≠ b 7 ∧ b 5 ≠ b 7 ∧ N (b 0) (b 4) (b 3) (b 2) ∧
  (b (other rev) ≠ b 5 ∨ b 7 ≠ b (source rev))

theorem b_frame_guard : ∀ p s q t r : Color, BRule p s q t r → t ≠ p ∨ r ≠ s := by decide

theorem b_t_guard : ∀ p s q t r : Color, BRule p s q t r → N s t p q := by decide

theorem p_guard (rev : Bool) {b : Row} (h : b ∈ P rev) : PGuard rev b := by
  obtain ⟨⟨c, hc, ec⟩, ⟨d, hd, ed⟩⟩ := h
  have hc' := (j_iff_rule rev c).mp hc
  have hd' := (j_iff_rule rev d).mp hd
  have hg := b_frame_guard _ _ _ _ _ hd'.2
  cases rev <;>
    simp only [frame₁, frame₂, source, other, Bool.false_eq_true, ↓reduceIte,
      Finset.mem_insert, Finset.mem_singleton] at ec ed <;>
    simp only [forall_eq_or_imp] at ec ed <;>
    rcases ec with ⟨e0,e4,e3,e2,e6⟩ <;>
    rcases ed with ⟨f0,f1,f2,f7,f5⟩ <;>
    simp_all [JRule, ARule, BRule, PGuard, source, other]

/-- Three local necessary conditions extracted without computing any marginal table. -/
theorem accept_a (rev : Bool) {b : Row} (h : Accept rev scopeA.val b) :
    N (b 0) (b 1) (b 2) (b 3) := by
  obtain ⟨c, hc, he⟩ := h
  have hN := ((j_iff_rule rev c).mp hc).1.2.2.2.2.2.1
  simpa only [he 0 (by decide), he 1 (by decide), he 2 (by decide), he 3 (by decide)] using hN

theorem accept_b (rev : Bool) {b : Row} (h : Accept rev (scopeB rev).val b) :
    b 6 ≠ b 7 ∧ (b (source rev) ≠ b 7 ∨ b 5 = b 6) := by
  obtain ⟨c, hc, he⟩ := h
  have hB := ((j_iff_rule rev c).mp hc).2.2.2.2.2.2
  have hs := he (source rev) (by simp [scopeB])
  have hp := he 5 (by simp [scopeB])
  have hq := he 6 (by simp [scopeB])
  have hr := he 7 (by simp [scopeB])
  simpa only [hs, hp, hq, hr] using hB

theorem accept_t (rev : Bool) {b : Row} (h : Accept rev scopeT.val b) :
    N (b (source rev)) (b (other rev)) (b 5) (b 6) := by
  obtain ⟨c, hc, he⟩ := h
  have hn := b_t_guard _ _ _ _ _ ((j_iff_rule rev c).mp hc).2
  have hs := he (source rev) (by cases rev <;> decide)
  have ht := he (other rev) (by cases rev <;> decide)
  simpa only [hs, ht, he 5 (by decide), he 6 (by decide)] using hn

theorem accept_e (rev : Bool) {b : Row} {e : Scope} (he : e ∈ scopesE rev)
    (h : Accept rev e.val b) : b 6 ≠ b 7 := by
  obtain ⟨c, hc, eq⟩ := h
  have hn := ((j_iff_rule rev c).mp hc).2.2.2.2.2.2.1
  simpa only [eq 6 he.1, eq 7 he.2.1] using hn


/-- Full-J membership inside P is exactly the three missing local constraints. -/
theorem j_inside_p (rev : Bool) {b : Row} (hp : b ∈ P rev) :
    b ∈ J rev ↔ N (b 0) (b 1) (b 2) (b 3) ∧ b 6 ≠ b 7 ∧
      (b (source rev) ≠ b 7 ∨ b 5 = b 6) := by
  have hg := p_guard rev hp
  rw [j_iff_rule]
  simp only [JRule, ARule, BRule, PGuard] at *
  tauto

/-- The colour obstruction used uniformly by all fourteen E scopes. -/
theorem coverage_colors : ∀ p s q t r : Color,
    p ≠ s → s ≠ q → q ≠ t → t ≠ r → p ≠ r →
    (t ≠ p ∨ r ≠ s) → N s t p q → s ≠ r ∨ p = q := by decide

theorem cover_ab (rev : Bool) : (system rev).Covers {scopeA, scopeB rev} := by
  intro b hb
  by_contra hn
  have ha : Accept rev scopeA.val b := by
    by_contra h
    exact hn ⟨scopeA, by simp, hb, h⟩
  have hB : Accept rev (scopeB rev).val b := by
    by_contra h
    exact hn ⟨scopeB rev, by simp, hb, h⟩
  exact hb.2 ((j_inside_p rev hb.1).mpr ⟨accept_a rev ha, accept_b rev hB⟩)

theorem cover_ate (rev : Bool) (e : Scope) (he : e ∈ scopesE rev) :
    (system rev).Covers {scopeA, scopeT, e} := by
  intro b hb
  by_contra hn
  have ha : Accept rev scopeA.val b := by
    by_contra h
    exact hn ⟨scopeA, by simp, hb, h⟩
  have ht : Accept rev scopeT.val b := by
    by_contra h
    exact hn ⟨scopeT, by simp, hb, h⟩
  have hE : Accept rev e.val b := by
    by_contra h
    exact hn ⟨e, by simp, hb, h⟩
  have hg := p_guard rev hb.1
  rcases hg with ⟨_,_,_,_,_,hps,hsq,hqt,htr,hpr,_,hframe⟩
  exact hb.2 ((j_inside_p rev hb.1).mpr ⟨accept_a rev ha, accept_e rev he hE,
    coverage_colors _ _ _ _ _ hps hsq hqt htr hpr hframe (accept_t rev ht)⟩)

/-- Three original words, in U=(a0,a1,a2,a3,a4,b0,b2,b4) order. -/
def witness (rev : Bool) (k : Fin 3) : Row :=
  if rev then ![![0, 1, 2, 3, 2, 1, 1, 2],
    ![0, 1, 2, 1, 2, 1, 3, 2],
    ![0, 1, 0, 1, 2, 1, 2, 2]] k
  else ![![0, 1, 2, 3, 2, 1, 1, 3],
    ![0, 1, 2, 0, 1, 1, 3, 0],
    ![0, 1, 0, 1, 2, 1, 2, 2]] k

/-- Eleven complete-U lifts per orientation from the source proof. -/
def lifts (rev : Bool) (k : Fin 3) : List Row :=
  if rev then ![[![3, 1, 2, 3, 2, 1, 1, 2],
    ![0, 3, 2, 3, 2, 1, 1, 2],
    ![0, 1, 0, 3, 2, 1, 1, 2],
    ![0, 1, 2, 0, 2, 1, 1, 2]],
    [![0, 1, 0, 1, 2, 1, 3, 2],
    ![0, 1, 2, 1, 2, 3, 3, 2],
    ![0, 1, 2, 1, 2, 1, 1, 2],
    ![1, 0, 2, 1, 2, 1, 3, 0],
    ![2, 1, 2, 1, 0, 1, 3, 0]],
    [![0, 1, 0, 1, 2, 1, 1, 2],
    ![0, 1, 0, 1, 2, 1, 2, 3]]] k
  else ![[![3, 1, 2, 3, 2, 1, 1, 3],
    ![0, 3, 2, 3, 2, 1, 1, 3],
    ![0, 1, 0, 3, 2, 1, 1, 3],
    ![0, 1, 2, 0, 2, 1, 1, 3]],
    [![2, 1, 2, 0, 1, 1, 3, 0],
    ![0, 1, 2, 0, 1, 3, 3, 0],
    ![0, 1, 2, 0, 1, 1, 1, 0],
    ![0, 2, 1, 0, 1, 1, 3, 2],
    ![0, 1, 0, 2, 1, 1, 3, 2]],
    [![0, 1, 0, 1, 2, 1, 1, 2],
    ![0, 1, 0, 1, 2, 1, 2, 3]]] k

def Bad (rev : Bool) (k : Fin 3) (s : Scope) : Prop :=
  if k = 0 then s = scopeA else if k = 1 then s = scopeB rev ∨ s = scopeT
  else 6 ∈ s.val ∧ 7 ∈ s.val
instance (rev : Bool) (k : Fin 3) (s : Scope) : Decidable (Bad rev k s) :=
  inferInstanceAs (Decidable (if k = 0 then _ else if k = 1 then _ else _))

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
-- Iterate the supplied lists, never the entire function space of possible lifts.
/-- Small finite certificate, retaining actual colours and all seventy scopes. -/
theorem lift_check : ∀ rev k,
    (lifts rev k).all (fun c => decide (JRule rev c)) = true ∧
    (∀ s : Scope, ¬ Bad rev k s →
      (lifts rev k).any (fun c => decide (∀ u ∈ s.val, c u = witness rev k u)) = true) ∧
    (lifts rev k).any (fun c => decide (∀ u ∈ frame₁, c u = witness rev k u)) = true ∧
    (lifts rev k).any (fun c => decide (∀ u ∈ frame₂ rev, c u = witness rev k u)) = true := by
  decide +kernel

theorem lift_certificate (rev : Bool) (k : Fin 3) :
    (∀ c ∈ lifts rev k, JRule rev c) ∧
    (∀ s : Scope, ¬ Bad rev k s →
      ∃ c ∈ lifts rev k, ∀ u ∈ s.val, c u = witness rev k u) ∧
    (∃ c ∈ lifts rev k, ∀ u ∈ frame₁, c u = witness rev k u) ∧
    (∃ c ∈ lifts rev k, ∀ u ∈ frame₂ rev, c u = witness rev k u) := by
  simpa only [List.all_eq_true, List.any_eq_true, decide_eq_true_eq] using lift_check rev k

theorem witness_not_j : ∀ rev k, ¬ JRule rev (witness rev k) := by decide

theorem witness_in_p (rev : Bool) (k : Fin 3) : witness rev k ∈ P rev := by
  obtain ⟨hc, _, ⟨c, hcL, ec⟩, ⟨d, hdL, ed⟩⟩ := lift_certificate rev k
  exact ⟨⟨c, (j_iff_rule rev c).mpr (hc c hcL), ec⟩,
    ⟨d, (j_iff_rule rev d).mpr (hc d hdL), ed⟩⟩

theorem witness_accept_iff (rev : Bool) (k : Fin 3) (s : Scope) :
    Accept rev s.val (witness rev k) ↔ ¬ Bad rev k s := by
  constructor
  · intro h bad
    fin_cases k
    · change s = scopeA at bad
      subst s
      have hn := accept_a rev h
      cases rev <;> exact absurd hn (by decide)
    · change s = scopeB rev ∨ s = scopeT at bad
      rcases bad with rfl | rfl
      · have hn := (accept_b rev h).2
        cases rev <;> exact absurd hn (by decide)
      · have hn := accept_t rev h
        cases rev <;> exact absurd hn (by decide)
    · change 6 ∈ s.val ∧ 7 ∈ s.val at bad
      obtain ⟨c, hc, eq⟩ := h
      have hn := ((j_iff_rule rev c).mp hc).2.2.2.2.2.2.1
      rw [eq 6 bad.1, eq 7 bad.2] at hn
      cases rev <;> exact absurd hn (by decide)
  · intro hn
    obtain ⟨c, hc, eq⟩ := (lift_certificate rev k).2.1 s hn
    exact ⟨c, (j_iff_rule rev c).mpr ((lift_certificate rev k).1 c hc), eq⟩


/-- The exact rejector set is relative to all four-element named scopes. -/
theorem witness_rejectors (rev : Bool) (k : Fin 3) :
    (system rev).rejectors (witness rev k) = {s | Bad rev k s} := by
  have hd : witness rev k ∈ (system rev).delta :=
    ⟨witness_in_p rev k, fun h => witness_not_j rev k ((j_iff_rule rev _).mp h)⟩
  ext s
  change (witness rev k ∈ (system rev).delta ∧
    ¬ Accept rev s.val (witness rev k)) ↔ Bad rev k s
  rw [witness_accept_iff]
  tauto

theorem witness_coverage (rev : Bool) : (roles rev).WitnessCoverage (system rev) := by
  have hw (k : Fin 3) : (system rev).ExactWitness {s | Bad rev k s} :=
    ⟨witness rev k,
      ⟨witness_in_p rev k, fun h => witness_not_j rev k ((j_iff_rule rev _).mp h)⟩,
      witness_rejectors rev k⟩
  refine ⟨?_, ?_, ?_, cover_ab rev, fun e he => cover_ate rev e he⟩
  · simpa [Bad, roles] using hw 0
  · have eq : {s | Bad rev 1 s} = {scopeB rev, scopeT} := by
      ext s
      simp [Bad]
    simpa only [roles, eq] using hw 1
  · have eq : {s | Bad rev 2 s} = insert (scopeB rev) (scopesE rev) := by
      ext s
      simp only [Bad, show (2 : Fin 3) ≠ 0 from by decide,
        show (2 : Fin 3) ≠ 1 from by decide, ↓reduceIte, Set.mem_ofPred_eq,
        Set.mem_insert_iff, scopesE]
      have hb : 6 ∈ (scopeB rev).val ∧ 7 ∈ (scopeB rev).val := by simp [scopeB]
      by_cases hs : s = scopeB rev <;> simp_all
    simpa only [roles, eq] using hw 2

theorem repairs_iff (rev : Bool) (H : Set Scope) :
    (system rev).Repairs H ↔
      (scopeA ∈ H ∧ scopeB rev ∈ H) ∨
      ∃ e ∈ scopesE rev, scopeA ∈ H ∧ scopeT ∈ H ∧ e ∈ H :=
  (roles rev).repairs_iff_template (system rev) (witness_coverage rev) H

theorem minimal_repairs_iff (rev : Bool) (H : Set Scope) :
    (system rev).MinimalRepair H ↔ H = {scopeA, scopeB rev} ∨
      ∃ e ∈ scopesE rev, H = {scopeA, scopeT, e} :=
  (roles rev).minimalRepair_iff (system rev) (witness_coverage rev) H

theorem unique_minimum_pair (rev : Bool) (H : Finset Scope) :
    (system rev).Repairs (H : Set Scope) ∧ H.card ≤ 2 ↔ H = {scopeA, scopeB rev} :=
  (roles rev).repair_card_le_two_iff (system rev) (witness_coverage rev) H

theorem forced_scope_iff (rev : Bool) (s : Scope) :
    (∀ H, (system rev).Repairs H → s ∈ H) ↔ s = scopeA :=
  (roles rev).forced_iff (system rev) (witness_coverage rev) s

def minimalRepairs (rev : Bool) : Finset (Finset Scope) :=
  insert {scopeA, scopeB rev}
    ((Finset.univ.filter (fun e => e ∈ scopesE rev)).image (fun e => {scopeA, scopeT, e}))

theorem minimal_repairs_mem (rev : Bool) (H : Finset Scope) :
    (system rev).MinimalRepair (H : Set Scope) ↔ H ∈ minimalRepairs rev := by
  rw [minimal_repairs_iff]
  have hp : ((H : Set Scope) = {scopeA, scopeB rev}) ↔ H = {scopeA, scopeB rev} := by
    exact_mod_cast (Iff.rfl : H = {scopeA, scopeB rev} ↔ H = {scopeA, scopeB rev})
  have ht (e : Scope) : ((H : Set Scope) = {scopeA, scopeT, e}) ↔
      H = {scopeA, scopeT, e} := by
    rw [← Finset.coe_inj]
    simp only [Finset.coe_insert, Finset.coe_singleton]
  simp only [hp, ht, minimalRepairs, Finset.mem_insert, Finset.mem_image,
    Finset.mem_filter, Finset.mem_univ, true_and]
  simp only [eq_comm]

theorem fifteen_minimal_repairs : ∀ rev, (minimalRepairs rev).card = 15 := by decide


/-- Every scope of arity at most three lies in a four-scope other than A. -/
theorem small_scope_extension : ∀ s : Finset (Fin 8), s.card ≤ 3 →
    ∃ t : Scope, s ⊆ t.val ∧ t ≠ scopeA := by decide +kernel

theorem witness_accepts_small (rev : Bool) (s : Finset (Fin 8)) (hs : s.card ≤ 3) :
    Accept rev s (witness rev 0) := by
  obtain ⟨t, hst, ht⟩ := small_scope_extension s hs
  have ha := (witness_accept_iff rev 0 t).mpr ht
  obtain ⟨c, hc, eq⟩ := ha
  exact ⟨c, hc, fun u hu => eq u (hst hu)⟩

/-- No conjunction of literal projections of arity at most three repairs P. -/
theorem no_small_projection_repair (rev : Bool) {Λ : Type*}
    (scope : Λ → Finset (Fin 8)) (hs : ∀ i, (scope i).card ≤ 3) (H : Set Λ) :
    ¬ (projectionSystem (J rev) (P rev) (j_subset_p rev)
      (fun i => (scope i : Set (Fin 8)))).Repairs H := by
  intro h
  have hw : witness rev 0 ∈
      (projectionSystem (J rev) (P rev) (j_subset_p rev)
        (fun i => (scope i : Set (Fin 8)))).result H :=
    ⟨witness_in_p rev 0, fun i _ => witness_accepts_small rev (scope i) (hs i)⟩
  change _ = J rev at h
  have hj : witness rev 0 ∈ J rev := h ▸ hw
  exact witness_not_j rev 0 ((j_iff_rule rev _).mp hj)

/-- A pair of four-point projections does repair P, complementing the lower bound. -/
theorem four_point_repair (rev : Bool) : (system rev).Repairs {scopeA, scopeB rev} :=
  ((system rev).repairs_iff_covers _).mpr (cover_ab rev)

end FiveBoundary.NamedRepair
