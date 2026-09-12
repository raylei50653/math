/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.AttachmentBlock

/-! # A structural attachment budget

Every extra chord in a boundary fan consumes at least one forward triangle step.
Summing these costs gives an attachment bound from `RunOK`, without enumerating words
or assuming any theorem about planar embeddings. -/

namespace FiveBoundary.GeometryDFA
open ColorDFA

local infixl:50 " <+ " => List.Sublist

/-- Steps internal to a list, without a closing edge. -/
def internalSteps : List (Fin 3) → ℕ
  | [] => 0
  | a :: l => pathSteps a l

theorem internalSteps_le_pathSteps (a : Fin 3) (l : List (Fin 3)) :
    internalSteps l ≤ pathSteps a l := by
  cases l <;> simp [internalSteps, pathSteps]

theorem internalSteps_append (l m : List (Fin 3)) :
    internalSteps l + internalSteps m ≤ internalSteps (l ++ m) := by
  cases l with
  | nil => simp [internalSteps]
  | cons a l =>
    simp only [List.cons_append, internalSteps, pathSteps_append]
    exact Nat.add_le_add_left (internalSteps_le_pathSteps _ _) _

theorem internalSteps_flatMap {α : Type*} (f : α → List (Fin 3)) (l : List α) :
    (l.map (fun a => internalSteps (f a))).sum ≤ internalSteps (l.flatMap f) := by
  induction l with
  | nil => simp [internalSteps]
  | cons a l ih =>
    simp only [List.map_cons, List.sum_cons, List.flatMap_cons]
    exact (Nat.add_le_add_left ih _).trans (internalSteps_append _ _)

theorem internalSteps_le_stepSum (l : List (Fin 3)) : internalSteps l ≤ stepSum l := by
  cases l with
  | nil => exact le_rfl
  | cons a l =>
    simp only [internalSteps, stepSum, pathSteps_append]
    omega

theorem stp_pos {a b : Fin 3} (h : a ≠ b) : 1 ≤ stp a b := by
  revert a b; decide

/-- A fan has no repetitions, so each of its internal steps costs at least one. -/
theorem length_sub_one_le_internalSteps (l : List (Fin 3)) (h : l.Nodup) :
    l.length - 1 ≤ internalSteps l := by
  induction l with
  | nil => simp [internalSteps]
  | cons a l ih =>
    cases l with
    | nil => simp [internalSteps, pathSteps]
    | cons b l =>
      have ht := ih h.of_cons
      have hn : a ≠ b := fun he => (List.nodup_cons.mp h).1 (he ▸ List.mem_cons_self)
      have hp := stp_pos hn
      simp only [List.length_cons, internalSteps, pathSteps] at *
      omega

theorem fan_nodup (o : Bool) (s : Finset (Fin 3)) (r : Fin 3) : (fan o s r).Nodup := by
  apply List.nodup_rotate.mpr
  exact List.Nodup.map (fun _ _ h => pos_injective o h)
    (List.Nodup.filter _ (List.nodup_finRange 3))

theorem fan_length (o : Bool) (s : Finset (Fin 3)) (r : Fin 3) :
    (fan o s r).length = s.card := by
  have he : (fan o s r).toFinset = s := by ext k; simp [mem_fan]
  exact (List.toFinset_card_of_nodup (fan_nodup o s r)).symm.trans (congrArg Finset.card he)

/-- Total cost of nonempty fans beyond their first chord is bounded by winding. -/
theorem fan_excess_le_winding (w : Word) (ρ : Run) :
    ((List.finRange 5).map (fun i => (w i).card - 1)).sum ≤ winding w ρ := by
  let f := fun i => (fan ρ.1 (w i) (ρ.2 i)).map (pos ρ.1)
  have hf : ∀ i, (w i).card - 1 ≤ internalSteps (f i) := by
    intro i
    have hn : (f i).Nodup := List.Nodup.map (fun _ _ h => pos_injective ρ.1 h) (fan_nodup _ _ _)
    simpa [f, fan_length] using length_sub_one_le_internalSteps (f i) hn
  have hs : ((List.finRange 5).map (fun i => (w i).card - 1)).sum ≤
      ((List.finRange 5).map (fun i => internalSteps (f i))).sum := by
    exact List.sum_le_sum (fun i _ => hf i)
  have he : (sequence w ρ).map (fun e => pos ρ.1 e.2) = (List.finRange 5).flatMap f := by
    simp [sequence, List.map_flatMap, List.map_map, Function.comp_def, f]
  rw [winding_eq_stepSum, he]
  exact hs.trans ((internalSteps_flatMap f _).trans (internalSteps_le_stepSum _))

/-- The three units of winding bound all extra fan chords. -/
theorem runOK_fan_excess_le_three (w : Word) (ρ : Run) (h : RunOK w ρ) :
    ((List.finRange 5).map (fun i => (w i).card - 1)).sum ≤ 3 := by
  have hb := fan_excess_le_winding w ρ
  rcases h with h | h <;> omega

/-- Number of attachment edges, counted at the boundary. -/
def attachmentCount (w : Word) : ℕ := ∑ i, (w i).card

/-- Number of boundary vertices with a nonempty fan. -/
def activeCount (w : Word) : ℕ := (Finset.univ.filter (fun i => (w i).Nonempty)).card

theorem attachmentCount_eq_active_add_excess (w : Word) :
    attachmentCount w = activeCount w + ∑ i, ((w i).card - 1) := by
  simp only [attachmentCount, activeCount, Finset.card_filter]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  split_ifs with h
  · have := Finset.card_pos.mpr h; omega
  · have := Finset.not_nonempty_iff_eq_empty.mp h
    simp [this]

/-- A sharper form remembers how many boundary vertices are actually used. -/
theorem runOK_attachmentCount_le (w : Word) (ρ : Run) (h : RunOK w ρ) :
    attachmentCount w ≤ activeCount w + 3 := by
  have hb := runOK_fan_excess_le_three w ρ h
  rw [← List.ofFn_eq_map, List.sum_ofFn] at hb
  rw [attachmentCount_eq_active_add_excess]
  omega

theorem activeCount_le_five (w : Word) : activeCount w ≤ 5 :=
  (Finset.card_le_card (Finset.filter_subset _ _)).trans (by simp)

/-- No accepted triangle word has more than eight attachment edges. -/
theorem runOK_attachmentCount_le_eight (w : Word) (ρ : Run) (h : RunOK w ρ) :
    attachmentCount w ≤ 8 :=
  (runOK_attachmentCount_le w ρ h).trans (Nat.add_le_add_right (activeCount_le_five w) 3)

/-- The same edges counted at the triangle vertices. -/
theorem attachmentCount_eq_degree_sum (w : Word) :
    attachmentCount w = ∑ k, (linksOf w k).card := by
  have count : ∀ s : Finset (Fin 3), s.card = ∑ k, if k ∈ s then 1 else 0 := by
    intro s
    rw [← Finset.card_filter]
    simp
  simp only [attachmentCount, count, linksOf, Finset.card_filter]
  exact Finset.sum_comm

/-- Saturating the bound forces all boundary vertices to participate. -/
theorem runOK_eight_all_active (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hc : attachmentCount w = 8) : ∀ i, (w i).Nonempty := by
  have hb := runOK_attachmentCount_le w ρ h
  have ha := activeCount_le_five w
  have he : Finset.univ.filter (fun i => (w i).Nonempty) = Finset.univ :=
    Finset.eq_of_subset_of_card_le (Finset.filter_subset _ _) (by
      simpa [activeCount] using (show 5 ≤ activeCount w by omega))
  intro i
  have hi : i ∈ Finset.univ.filter (fun i => (w i).Nonempty) := by rw [he]; exact Finset.mem_univ i
  exact (Finset.mem_filter.mp hi).2

/-! ### Two triangle vertices cannot have three common boundary neighbours -/

/-- The two possible orders in which a fan can contain two distinct triangle vertices. -/
def pairOrder (p q : Fin 3) (b : Bool) : List (Fin 3) := if b then [p, q] else [q, p]

/-- A local fan fact (eight letters only), checked by kernel reduction. -/
theorem pairOrder_sublist_fan (o : Bool) (s : Finset (Fin 3)) (r p q : Fin 3)
    (hne : p ≠ q) (hp : p ∈ s) (hq : q ∈ s) :
    ∃ b, pairOrder (pos o p) (pos o q) b <+ (fan o s r).map (pos o) := by
  revert o s r p q; decide +kernel

/-- Three fans containing the same distinct pair force at least two turns.
This is a six-chord local fact, independent of the attachment word. -/
theorem three_pairs_stepSum (p q : Fin 3) (hne : p ≠ q) (a b c : Bool) :
    6 ≤ stepSum (pairOrder p q a ++ pairOrder p q b ++ pairOrder p q c) := by
  revert p q a b c; decide +kernel

/-- Sorting three distinct boundary positions; only the order of C5 is involved. -/
theorem three_positions_order (i j k : Fin 5) (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k) :
    [i, j, k] <+ List.finRange 5 ∨ [i, k, j] <+ List.finRange 5 ∨
    [j, i, k] <+ List.finRange 5 ∨ [j, k, i] <+ List.finRange 5 ∨
    [k, i, j] <+ List.finRange 5 ∨ [k, j, i] <+ List.finRange 5 := by
  revert i j k; decide +kernel

theorem no_three_common_ordered (w : Word) (ρ : Run) (h : RunOK w ρ)
    (p q : Fin 3) (hne : p ≠ q) (i j k : Fin 5)
    (hord : [i, j, k] <+ List.finRange 5)
    (hi : p ∈ w i ∧ q ∈ w i) (hj : p ∈ w j ∧ q ∈ w j)
    (hk : p ∈ w k ∧ q ∈ w k) : False := by
  obtain ⟨a, ha⟩ := pairOrder_sublist_fan ρ.1 (w i) (ρ.2 i) p q hne hi.1 hi.2
  obtain ⟨b, hb⟩ := pairOrder_sublist_fan ρ.1 (w j) (ρ.2 j) p q hne hj.1 hj.2
  obtain ⟨c, hc⟩ := pairOrder_sublist_fan ρ.1 (w k) (ρ.2 k) p q hne hk.1 hk.2
  let f := fun i => (fan ρ.1 (w i) (ρ.2 i)).map (pos ρ.1)
  have hs : pairOrder (pos ρ.1 p) (pos ρ.1 q) a ++
      pairOrder (pos ρ.1 p) (pos ρ.1 q) b ++ pairOrder (pos ρ.1 p) (pos ρ.1 q) c <+
      (List.finRange 5).flatMap f := by
    apply List.Sublist.trans _ (flatMap_sublist_of_sublist f hord)
    simpa [List.append_assoc, f] using (ha.append hb).append hc
  have he : (sequence w ρ).map (fun e => pos ρ.1 e.2) = (List.finRange 5).flatMap f := by
    simp [sequence, List.map_flatMap, List.map_map, Function.comp_def, f]
  have hl := (three_pairs_stepSum (pos ρ.1 p) (pos ρ.1 q)
    (fun he => hne (pos_injective _ he)) a b c).trans (stepSum_le_of_sublist hs)
  rw [← he, ← winding_eq_stepSum] at hl
  rcases h with h | h <;> omega

/-- The sharp common-neighbour bound is two, not one. -/
theorem runOK_common_card_le_two (w : Word) (ρ : Run) (h : RunOK w ρ)
    (p q : Fin 3) (hne : p ≠ q) : ((linksOf w p) ∩ (linksOf w q)).card ≤ 2 := by
  by_contra hc
  obtain ⟨i, hi, j, hj, k, hk, hij, hik, hjk⟩ := Finset.two_lt_card.mp (by omega :
    2 < ((linksOf w p) ∩ (linksOf w q)).card)
  simp only [Finset.mem_inter, linksOf, Finset.mem_filter, Finset.mem_univ, true_and] at hi hj hk
  rcases three_positions_order i j k hij hik hjk with ho | ho | ho | ho | ho | ho
  · exact no_three_common_ordered w ρ h p q hne i j k ho hi hj hk
  · exact no_three_common_ordered w ρ h p q hne i k j ho hi hk hj
  · exact no_three_common_ordered w ρ h p q hne j i k ho hj hi hk
  · exact no_three_common_ordered w ρ h p q hne j k i ho hj hk hi
  · exact no_three_common_ordered w ρ h p q hne k i j ho hk hi hj
  · exact no_three_common_ordered w ρ h p q hne k j i ho hk hj hi

end FiveBoundary.GeometryDFA
