/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.AttachmentGaps

/-! # Ordered singleton gaps at missing junctions

A shared junction fixes where the cyclic order starts. The remaining chords cannot
run backwards in that order. Lift this order to packet blocks while retaining empties.
-/
namespace FiveBoundary.GeometryDFA
open ColorDFA
local infixl:50 " <+ " => List.Sublist

def SingletonPackets (T : List (List (Fin 3))) : Prop :=
  ∀ l ∈ T, l = [] ∨ ∃ k, l = [k]

/-- If a gap contains no occurrence of its allowed position, it contains only empties. -/
theorem GapPackets.change_of_not_mem (k j : Fin 3) (T : List (List (Fin 3)))
    (h : GapPackets k T) (ha : k ∉ T.flatten) : GapPackets j T := by
  intro l hl
  rcases h l hl with he | he
  · exact Or.inl he
  · exfalso
    exact ha (List.mem_flatten.mpr ⟨l, hl, by simp [he]⟩)

/-- A linearly ordered list of singleton packets splits into its three blocks.
Empty packets remain in the displayed decomposition. -/
theorem singletonPackets_ordered_blocks (T : List (List (Fin 3))) (q : Fin 3)
    (ha : SingletonPackets T)
    (ho : T.flatten.Pairwise (fun a b => stp q a ≤ stp q b)) :
    ∃ U V W, T = U ++ V ++ W ∧ GapPackets q U ∧
      GapPackets (q + 1) V ∧ GapPackets (q + 2) W := by
  induction T with
  | nil => exact ⟨[], [], [], rfl, by simp [GapPackets], by simp [GapPackets], by simp [GapPackets]⟩
  | cons l T ih =>
    have hat : SingletonPackets T := fun l hl => ha l (List.mem_cons_of_mem _ hl)
    have hot : T.flatten.Pairwise (fun a b => stp q a ≤ stp q b) :=
      ho.sublist (by simpa only [List.flatten_cons] using (List.sublist_append_right l T.flatten))
    obtain ⟨U, V, W, ht, hu, hv, hw⟩ := ih hat hot
    rcases ha l List.mem_cons_self with rfl | ⟨k, rfl⟩
    · exact ⟨[] :: U, V, W, by simp [ht], by simpa [GapPackets] using hu, hv, hw⟩
    · have hhead : ∀ a ∈ T.flatten, stp q k ≤ stp q a := by
        change (k :: T.flatten).Pairwise (fun a b => stp q a ≤ stp q b) at ho
        exact (List.pairwise_cons.mp ho).1
      rcases fin3_trichotomy q k with hk | hk | hk
      all_goals subst k
      · exact ⟨[q] :: U, V, W, by simp [ht], by simpa [GapPackets] using hu, hv, hw⟩
      · have hnu : q ∉ U.flatten := by
          intro hm
          have := hhead q (by simp only [ht, List.flatten_append, List.mem_append]; exact Or.inl (Or.inl hm))
          have hd : stp q (q + 1) = 1 := by fin_cases q <;> decide
          simp [hd] at this
        have hu' := GapPackets.change_of_not_mem q (q + 1) U hu hnu
        refine ⟨[], [q + 1] :: (U ++ V), W, by simp [ht, List.append_assoc], by simp [GapPackets], ?_, hw⟩
        simp only [GapPackets, List.mem_cons, List.mem_append]
        intro l hl
        rcases hl with rfl | hl | hl
        · exact Or.inr rfl
        · exact hu' l hl
        · exact hv l hl
      · have hnu : q ∉ U.flatten := by
          intro hm
          have := hhead q (by simp only [ht, List.flatten_append, List.mem_append]; exact Or.inl (Or.inl hm))
          have hd : stp q (q + 2) = 2 := by fin_cases q <;> decide
          simp [hd] at this
        have hnv : q + 1 ∉ V.flatten := by
          intro hm
          have := hhead (q + 1) (by simp only [ht, List.flatten_append, List.mem_append]; exact Or.inl (Or.inr hm))
          have hd : stp q (q + 2) = 2 ∧ stp q (q + 1) = 1 := by fin_cases q <;> decide
          omega
        have hu' := GapPackets.change_of_not_mem q (q + 2) U hu hnu
        have hv' := GapPackets.change_of_not_mem (q + 1) (q + 2) V hv hnv
        refine ⟨[], [], [q + 2] :: (U ++ V ++ W), by simp [ht],
          by simp [GapPackets], by simp [GapPackets], ?_⟩
        simp only [GapPackets, List.mem_cons, List.mem_append]
        intro l hl
        rcases hl with rfl | (hl | hl) | hl
        · exact Or.inr rfl
        · exact hu' l hl
        · exact hv' l hl
        · exact hw l hl

/-- A junction fixes the linear order of all remaining chords. -/
theorem junction_tail_ordered (q : Fin 3) (T : List (Fin 3))
    (hs : stepSum ([q + 2, q] ++ T) ≤ 3) :
    T.Pairwise (fun a b => stp q a ≤ stp q b) := by
  apply List.pairwise_iff_forall_sublist.mpr
  intro a b hab
  have hh := (stepSum_le_of_sublist ((List.Sublist.refl [q + 2, q]).append hab)).trans hs
  have localOrder : ∀ q a b : Fin 3,
      stepSum [q + 2, q, a, b] ≤ 3 → stp q a ≤ stp q b := by decide +kernel
  exact localOrder q a b hh

def oneJunctionPackets (q : Fin 3) (x y z : ℕ) : List (List (Fin 3)) :=
  [q + 2, q] :: (List.replicate x [q] ++ List.replicate y [q + 1] ++ List.replicate z [q + 2])

theorem oneJunctionPackets_stepSum (q : Fin 3) (x y z : ℕ) :
    stepSum (oneJunctionPackets q x y z).flatten = 3 := by
  simp only [oneJunctionPackets, List.flatten_cons, List.flatten_append, flatten_replicate_singleton]
  have hneg : (-(2 : Fin 3)).val = 1 := by decide +kernel
  fin_cases q <;> cases x <;> cases y <;> cases z <;>
    simp [List.cons_append, stepSum, pathSteps_append, pathSteps,
      stp, hneg]

/-- The one-junction form, with arbitrary singleton block lengths and empty positions. -/
theorem one_junction_tail_iff (q : Fin 3) (T : List (List (Fin 3)))
    (ha : SingletonPackets T) :
    stepSum ([q + 2, q] :: T).flatten ≤ 3 ↔
      ∃ U V W, T = U ++ V ++ W ∧ GapPackets q U ∧
        GapPackets (q + 1) V ∧ GapPackets (q + 2) W := by
  constructor
  · intro hs
    exact singletonPackets_ordered_blocks T q ha (junction_tail_ordered q T.flatten hs)
  · rintro ⟨U, V, W, rfl, hu, hv, hw⟩
    have he : ([q + 2, q] :: (U ++ V ++ W)).flatten =
        (oneJunctionPackets q (U.count [q]) (V.count [q + 1]) (W.count [q + 2])).flatten := by
      simp [oneJunctionPackets, List.flatten_append, hu.flatten_eq, hv.flatten_eq, hw.flatten_eq]
    rw [he, oneJunctionPackets_stepSum]

/-- Exactly one shared junction can be chosen as the anchor, in any triangle labeling. -/
theorem NecklaceCuts.one_junction_counts (s : NecklaceCuts) (he : s.junctionTotal = 1) :
    ∃ q : Fin 3, ∀ p : Fin 3,
      s.packets.count [p, p + 1] = if p = q + 2 then 1 else 0 := by
  have h0 := s.forward_pair_count_le_one 0
  have h1 := s.forward_pair_count_le_one 1
  have h2 := s.forward_pair_count_le_one 2
  simp only [NecklaceCuts.junctionTotal, Fin.sum_univ_three] at he
  simp only [Fin.exists_fin_succ, Fin.forall_fin_succ]
  simp +decide at *
  omega

/-- One-junction cyclic normal form, preserving all original boundary packets. -/
theorem NecklaceCuts.one_junction_cyclic_gaps (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) (he : s.junctionTotal = 1) :
    ∃ q n U V W, s.packets.rotate n = [q + 2, q] :: (U ++ V ++ W) ∧
      GapPackets q U ∧ GapPackets (q + 1) V ∧ GapPackets (q + 2) W := by
  obtain ⟨q, hq⟩ := s.one_junction_counts he
  have hanchor : s.packets.count [q + 2, q] = 1 := by
    have hh := hq (q + 2)
    have heq : q + 2 + 1 = q := by fin_cases q <;> decide
    simpa [heq] using hh
  obtain ⟨pre, post, hp⟩ := List.append_of_mem (List.count_pos_iff.mp (by omega : 0 < s.packets.count [q + 2, q]))
  have hr : s.packets.rotate pre.length = [q + 2, q] :: (post ++ pre) := by
    rw [hp, List.rotate_append_length_eq]; rfl
  have ha : SingletonPackets (post ++ pre) := by
    intro l hl
    have hm : l ∈ s.packets := List.mem_rotate.mp (by rw [hr]; exact List.mem_cons_of_mem _ hl)
    rcases s.alphabet h hd l hm with hem | hsing | ⟨p, hp⟩
    · exact Or.inl hem
    · exact Or.inr hsing
    · exfalso
      have hpos : 0 < (post ++ pre).count [p, p + 1] := List.count_pos_iff.mpr (hp ▸ hl)
      have hc := (List.rotate_perm s.packets pre.length).count_eq [p, p + 1]
      rw [hr, List.count_cons, hq p] at hc
      generalize (post ++ pre).count [p, p + 1] = c at hc hpos
      fin_cases p <;> fin_cases q <;> simp +decide at hc <;> omega
  have hs : stepSum ([q + 2, q] :: (post ++ pre)).flatten ≤ 3 := by
    rw [← hr, stepSum_flatten_rotate]; exact s.stepSum_le_three
  obtain ⟨U, V, W, ht, hu, hv, hw⟩ := (one_junction_tail_iff q (post ++ pre) ha).mp hs
  exact ⟨q, pre.length, U, V, W, by rw [hr, ht], hu, hv, hw⟩

/-- Two shared junctions force a constant gap and then two ordered singleton blocks. -/
theorem two_junction_tail_iff (q : Fin 3) (U T : List (List (Fin 3)))
    (ha : SingletonPackets U) (hb : SingletonPackets T) :
    stepSum ([q + 2, q] :: (U ++ [q, q + 1] :: T)).flatten ≤ 3 ↔
      GapPackets q U ∧ ∃ V W, T = V ++ W ∧ GapPackets (q + 1) V ∧ GapPackets (q + 2) W := by
  constructor
  · intro hs
    have ho := junction_tail_ordered q (U.flatten ++ [q, q + 1] ++ T.flatten)
      (by simpa [List.flatten_append, List.append_assoc] using hs)
    have hu : ∀ a ∈ U.flatten, a = q := by
      intro a ha
      have hsub : [a, q] <+ U.flatten ++ [q, q + 1] ++ T.flatten :=
        ((List.singleton_sublist.mpr ha).append (List.singleton_sublist.mpr (by simp))).append (List.nil_sublist _)
      have hle := List.pairwise_iff_forall_sublist.mp ho hsub
      have localEq : ∀ q a : Fin 3, stp q a ≤ stp q q → a = q := by decide +kernel
      exact localEq q a hle
    have hgu : GapPackets q U := gapPackets_of_constant U q (by
      intro l hl
      rcases ha l hl with rfl | ⟨k, rfl⟩ <;> simp) hu
    have hot : T.flatten.Pairwise (fun a b => stp q a ≤ stp q b) :=
      ho.sublist (List.sublist_append_right _ _)
    obtain ⟨V0, V, W, ht, hv0, hv, hw⟩ := singletonPackets_ordered_blocks T q hb hot
    have hnq : q ∉ T.flatten := by
      intro hq
      have hsub : [q + 1, q] <+ U.flatten ++ [q, q + 1] ++ T.flatten :=
        ((List.nil_sublist _).append (List.singleton_sublist.mpr (by simp))).append (List.singleton_sublist.mpr hq)
      have hle := List.pairwise_iff_forall_sublist.mp ho hsub
      have localNe : ∀ q : Fin 3, ¬ stp q (q + 1) ≤ stp q q := by decide +kernel
      exact localNe q hle
    have hv0' : GapPackets (q + 1) V0 := GapPackets.change_of_not_mem q (q + 1) V0 hv0 (by
      intro hm
      apply hnq
      simp only [ht, List.flatten_append, List.mem_append]
      exact Or.inl (Or.inl hm))
    refine ⟨hgu, V0 ++ V, W, ht, ?_, hw⟩
    intro l hl
    rcases List.mem_append.mp hl with hl | hl
    · exact hv0' l hl
    · exact hv l hl
  · rintro ⟨hu, V, W, rfl, hv, hw⟩
    have he : ([q + 2, q] :: (U ++ [q, q + 1] :: (V ++ W))).flatten =
        (oneJunctionPackets q (U.count [q] + 1) (V.count [q + 1] + 1) (W.count [q + 2])).flatten := by
      have commute (k : Fin 3) (n : ℕ) (L : List (Fin 3)) :
          List.replicate n k ++ k :: L = k :: (List.replicate n k ++ L) := by
        induction n with
        | zero => rfl
        | succ n ih => simpa [List.replicate_succ] using congrArg (List.cons k) ih
      simp [oneJunctionPackets, List.flatten_append, hu.flatten_eq, hv.flatten_eq, hw.flatten_eq,
        List.replicate_succ, List.append_assoc, commute]
    rw [he, oneJunctionPackets_stepSum]

theorem NecklaceCuts.two_junction_counts (s : NecklaceCuts) (he : s.junctionTotal = 2) :
    ∃ q : Fin 3, ∀ p : Fin 3,
      s.packets.count [p, p + 1] = if p = q + 1 then 0 else 1 := by
  have h0 := s.forward_pair_count_le_one 0
  have h1 := s.forward_pair_count_le_one 1
  have h2 := s.forward_pair_count_le_one 2
  simp only [NecklaceCuts.junctionTotal, Fin.sum_univ_three] at he
  simp only [Fin.exists_fin_succ, Fin.forall_fin_succ]
  simp +decide at *
  omega

/-- Both two-junction regimes have this cyclic order, with empty positions retained. -/
theorem NecklaceCuts.two_junction_cyclic_gaps (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) (he : s.junctionTotal = 2) :
    ∃ q n U V W, s.packets.rotate n = [q + 2, q] :: (U ++ [q, q + 1] :: (V ++ W)) ∧
      GapPackets q U ∧ GapPackets (q + 1) V ∧ GapPackets (q + 2) W := by
  obtain ⟨q, hq⟩ := s.two_junction_counts he
  have hA : s.packets.count [q + 2, q] = 1 := by
    have hh := hq (q + 2)
    fin_cases q <;> simpa using hh
  have hB : s.packets.count [q, q + 1] = 1 := by
    have hh := hq q
    fin_cases q <;> simpa using hh
  obtain ⟨pre, post, hp⟩ := List.append_of_mem (List.count_pos_iff.mp (by omega : 0 < s.packets.count [q + 2, q]))
  have hr : s.packets.rotate pre.length = [q + 2, q] :: (post ++ pre) := by
    rw [hp, List.rotate_append_length_eq]; rfl
  have hb : [q, q + 1] ∈ post ++ pre := by
    have hm : [q, q + 1] ∈ s.packets.rotate pre.length :=
      List.mem_rotate.mpr (List.count_pos_iff.mp (by omega : 0 < s.packets.count [q, q + 1]))
    rw [hr] at hm
    fin_cases q <;> simpa using hm
  obtain ⟨U, T, ht⟩ := List.append_of_mem hb
  have hr' : s.packets.rotate pre.length = [q + 2, q] :: (U ++ [q, q + 1] :: T) := by rw [hr, ht]
  have ha : ∀ l, l ∈ U ∨ l ∈ T → l = [] ∨ ∃ k, l = [k] := by
    intro l hl
    have hm : l ∈ s.packets := List.mem_rotate.mp (by
      rw [hr']; simp only [List.mem_cons, List.mem_append]; tauto)
    rcases s.alphabet h hd l hm with hem | hsing | ⟨p, hp⟩
    · exact Or.inl hem
    · exact Or.inr hsing
    · exfalso
      have hpos : 0 < U.count [p, p + 1] + T.count [p, p + 1] := by
        rcases hl with hl | hl
        · have := List.count_pos_iff.mpr (hp ▸ hl); omega
        · have := List.count_pos_iff.mpr (hp ▸ hl); omega
      have hc := (List.rotate_perm s.packets pre.length).count_eq [p, p + 1]
      rw [hr', List.count_cons, List.count_append, List.count_cons, hq p] at hc
      generalize U.count [p, p + 1] = c at hc hpos
      generalize T.count [p, p + 1] = d at hc hpos
      fin_cases p <;> fin_cases q <;> simp +decide at hc <;> omega
  have hs : stepSum ([q + 2, q] :: (U ++ [q, q + 1] :: T)).flatten ≤ 3 := by
    rw [← hr', stepSum_flatten_rotate]; exact s.stepSum_le_three
  obtain ⟨hu, V, W, hT, hv, hw⟩ :=
    (two_junction_tail_iff q U T (fun l hl => ha l (Or.inl hl)) (fun l hl => ha l (Or.inr hl))).mp hs
  exact ⟨q, pre.length, U, V, W, by rw [hr', hT], hu, hv, hw⟩

/-- Counting chords after a packet rotation preserves each attachment degree. -/
theorem NecklaceCuts.degree_eq_rotated_count (s : NecklaceCuts) (h : s.Valid) (n : ℕ) (k : Fin 3) :
    (linksOf s.word (pos s.orientation k)).card = (s.packets.rotate n).flatten.count k := by
  rw [s.degree_eq_count h]
  exact ((List.rotate_perm s.packets n).flatten.count_eq k).symm

/-- The unique one-junction C5 shape, up to boundary rotation and triangle labeling. -/
theorem NecklaceCuts.one_junction_normalForm (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) (he : s.junctionTotal = 1) :
    ∃ q n, s.packets.rotate n = oneJunctionPackets q 1 2 1 := by
  obtain ⟨q, n, U, V, W, hr, hu, hv, hw⟩ := s.one_junction_cyclic_gaps h hd he
  have hlen := congrArg List.length hr
  simp only [List.length_rotate, s.packets_length, List.length_cons, List.length_append] at hlen
  have h0 := hd (pos s.orientation q)
  have h1 := hd (pos s.orientation (q + 1))
  have h2 := hd (pos s.orientation (q + 2))
  rw [s.degree_eq_rotated_count h n, hr] at h0 h1 h2
  simp only [List.flatten_cons, List.flatten_append, hu.flatten_eq, hv.flatten_eq, hw.flatten_eq] at h0 h1 h2
  have hc : U.count [q] = 1 ∧ V.count [q + 1] = 2 ∧ W.count [q + 2] = 1 ∧
      U.count [] = 0 ∧ V.count [] = 0 ∧ W.count [] = 0 := by
    have hi0 := hu.inventory
    have hi1 := hv.inventory
    have hi2 := hw.inventory
    fin_cases q <;>
      simp +decide only [List.count_cons, List.count_nil, List.count_append, List.count_replicate,
        Fin.reduceAdd, Fin.reduceEq, beq_iff_eq, ite_true, ite_false,
        Nat.add_zero, Nat.zero_add] at h0 h1 h2 hi0 hi1 hi2 ⊢ <;> omega
  have exactGap : ∀ (k : Fin 3) (T : List (List (Fin 3))),
      GapPackets k T → T.count [] = 0 → T = List.replicate (T.count [k]) [k] := by
    intro k T ht hz
    have hh : ∀ l ∈ T, l = [k] := by
      intro l hl
      rcases ht l hl with hl' | hl'
      · exact False.elim (List.count_eq_zero.mp hz (hl' ▸ hl))
      · exact hl'
    have ht' := List.eq_replicate_of_mem hh
    have hn := ht.inventory
    rw [hz, Nat.zero_add] at hn
    exact ht'.trans (congrArg (fun m => List.replicate m [k]) hn.symm)
  refine ⟨q, n, ?_⟩
  rw [hr, exactGap q U hu hc.2.2.2.1, exactGap (q + 1) V hv hc.2.2.2.2.1,
    exactGap (q + 2) W hw hc.2.2.2.2.2, hc.1, hc.2.1, hc.2.2.1]
  rfl

/-- C5 inventory and degree bounds for the two-junction normal form.
The two outer singleton blocks are nonempty; all empty positions remain recorded. -/
theorem NecklaceCuts.two_junction_gap_inventory (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) (he : s.junctionTotal = 2) :
    ∃ q n U V W, s.packets.rotate n = [q + 2, q] :: (U ++ [q, q + 1] :: (V ++ W)) ∧
      GapPackets q U ∧ GapPackets (q + 1) V ∧ GapPackets (q + 2) W ∧
      U.length + V.length + W.length = 3 ∧
      U.count [] + V.count [] + W.count [] = s.emptyTotal ∧
      1 ≤ V.count [q + 1] ∧ 1 ≤ W.count [q + 2] ∧
      U.count [q] + V.count [q + 1] + W.count [q + 2] + s.emptyTotal = 3 := by
  obtain ⟨q, n, U, V, W, hr, hu, hv, hw⟩ := s.two_junction_cyclic_gaps h hd he
  have hlen := congrArg List.length hr
  simp only [List.length_rotate, s.packets_length, List.length_cons, List.length_append] at hlen
  have hz : U.count [] + V.count [] + W.count [] = s.emptyTotal := by
    have hc := (List.rotate_perm s.packets n).count_eq []
    rw [hr] at hc
    simpa [NecklaceCuts.emptyTotal, Nat.add_assoc] using hc
  have h1 := hd (pos s.orientation (q + 1))
  have h2 := hd (pos s.orientation (q + 2))
  rw [s.degree_eq_rotated_count h n, hr] at h1 h2
  simp only [List.flatten_cons, List.flatten_append, hu.flatten_eq, hv.flatten_eq, hw.flatten_eq] at h1 h2
  have hb : 1 ≤ V.count [q + 1] ∧ 1 ≤ W.count [q + 2] := by
    fin_cases q <;>
      simp +decide only [List.count_cons, List.count_nil, List.count_append, List.count_replicate,
        Fin.reduceAdd, Fin.reduceEq, beq_iff_eq, ite_true, ite_false,
        Nat.add_zero, Nat.zero_add] at h1 h2 ⊢ <;> omega
  have hi0 := hu.inventory
  have hi1 := hv.inventory
  have hi2 := hw.inventory
  exact ⟨q, n, U, V, W, hr, hu, hv, hw, by omega, hz, hb.1, hb.2, by omega⟩

end FiveBoundary.GeometryDFA
