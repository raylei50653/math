/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.AttachmentSignature

/-! # Cyclic normal form when all three junctions are shared

The three pair packets anchor the cyclic order. Between consecutive junctions, every
packet is a singleton of their common triangle position. This is proved structurally
from the one-turn bound, not by enumerating attachment words or packet arrangements. -/

namespace FiveBoundary.GeometryDFA
open ColorDFA
local infixl:50 " <+ " => List.Sublist

theorem stepSum_flatten_rotate_one (ls : List (List (Fin 3))) :
    stepSum (ls.rotate 1).flatten = stepSum ls.flatten := by
  cases ls with
  | nil => rfl
  | cons l ls =>
    simp only [List.rotate_cons_succ, List.rotate_zero, List.flatten_append,
      List.flatten_cons, List.flatten_nil, List.append_nil]
    rw [← List.rotate_append_length_eq l ls.flatten, stepSum_rotate]

theorem stepSum_flatten_rotate (ls : List (List (Fin 3))) (n : ℕ) :
    stepSum (ls.rotate n).flatten = stepSum ls.flatten := by
  induction n with
  | zero => simp
  | succ n ih => rw [← List.rotate_rotate, stepSum_flatten_rotate_one, ih]

/-- Three shared junctions have a forced cyclic order. -/
theorem junctions_cyclic_order (ls : List (List (Fin 3)))
    (hA : [0, 1] ∈ ls) (hB : [1, 2] ∈ ls) (hC : [2, 0] ∈ ls)
    (hs : stepSum ls.flatten ≤ 3) :
    ∃ n U V W, ls.rotate n = [0, 1] :: (U ++ [1, 2] :: (V ++ [2, 0] :: W)) := by
  obtain ⟨pre, post, he⟩ := List.append_of_mem hA
  have hrot : ls.rotate pre.length = [0, 1] :: (post ++ pre) := by
    rw [he, List.rotate_append_length_eq]; rfl
  have hb : [1, 2] ∈ post ++ pre := by
    have hm : [1, 2] ∈ ls.rotate pre.length := List.mem_rotate.mpr hB
    rw [hrot] at hm
    simpa using hm
  obtain ⟨U, T, ht⟩ := List.append_of_mem hb
  have hrot' : ls.rotate pre.length = [0, 1] :: (U ++ [1, 2] :: T) := by rw [hrot, ht]
  have hc : [2, 0] ∈ U ∨ [2, 0] ∈ T := by
    have hm : [2, 0] ∈ ls.rotate pre.length := List.mem_rotate.mpr hC
    rw [hrot'] at hm
    simpa using hm
  rcases hc with hc | hc
  · have hsub : [[0, 1], [2, 0], [1, 2]] <+ ls.rotate pre.length := by
      rw [hrot']
      apply List.Sublist.cons_cons
      exact (List.singleton_sublist.mpr hc).append
        (List.singleton_sublist.mpr (List.mem_cons_self))
    have hb := stepSum_le_of_sublist hsub.flatten
    have hbad : stepSum ([[0, 1], [2, 0], [1, 2]] : List (List (Fin 3))).flatten = 6 := by decide
    rw [hbad, stepSum_flatten_rotate] at hb
    omega
  · obtain ⟨V, W, hw⟩ := List.append_of_mem hc
    exact ⟨pre.length, U, V, W, by rw [hrot', hw]⟩

/-- Any position inserted between anchored junctions must be their common position. -/
theorem anchored_gap_position (k : Fin 3) :
    (stepSum [0, 1, k, 1, 2, 2, 0] ≤ 3 → k = 1) ∧
    (stepSum [0, 1, 1, 2, k, 2, 0] ≤ 3 → k = 2) ∧
    (stepSum [0, 1, 1, 2, 2, 0, k] ≤ 3 → k = 0) := by
  revert k; decide +kernel

/-- No position other than the common endpoint can occur in a gap between junctions. -/
theorem anchored_gaps_constant (U V W : List (Fin 3))
    (hs : stepSum ([0, 1] ++ U ++ [1, 2] ++ V ++ [2, 0] ++ W) ≤ 3) :
    (∀ k ∈ U, k = 1) ∧ (∀ k ∈ V, k = 2) ∧ (∀ k ∈ W, k = 0) := by
  refine ⟨?_, ?_, ?_⟩
  · intro k hk
    have hsub : [0, 1, k, 1, 2, 2, 0] <+ [0, 1] ++ U ++ [1, 2] ++ V ++ [2, 0] ++ W :=
      (((((List.Sublist.refl [0, 1]).append (List.singleton_sublist.mpr hk)).append
        (List.Sublist.refl [1, 2])).append (List.nil_sublist V)).append
        (List.Sublist.refl [2, 0])).append (List.nil_sublist W)
    exact (anchored_gap_position k).1 ((stepSum_le_of_sublist hsub).trans hs)
  · intro k hk
    have hsub : [0, 1, 1, 2, k, 2, 0] <+ [0, 1] ++ U ++ [1, 2] ++ V ++ [2, 0] ++ W :=
      (((((List.Sublist.refl [0, 1]).append (List.nil_sublist U)).append
        (List.Sublist.refl [1, 2])).append (List.singleton_sublist.mpr hk)).append
        (List.Sublist.refl [2, 0])).append (List.nil_sublist W)
    exact (anchored_gap_position k).2.1 ((stepSum_le_of_sublist hsub).trans hs)
  · intro k hk
    have hsub : [0, 1, 1, 2, 2, 0, k] <+ [0, 1] ++ U ++ [1, 2] ++ V ++ [2, 0] ++ W :=
      (((((List.Sublist.refl [0, 1]).append (List.nil_sublist U)).append
        (List.Sublist.refl [1, 2])).append (List.nil_sublist V)).append
        (List.Sublist.refl [2, 0])).append (List.singleton_sublist.mpr hk)
    exact (anchored_gap_position k).2.2 ((stepSum_le_of_sublist hsub).trans hs)

/-- A nonempty duplicate-free packet with one possible position is a singleton. -/
theorem singleton_of_packet_constant (l : List (Fin 3)) (k : Fin 3)
    (hn : l.Nodup) (he : l ≠ []) (hc : ∀ a ∈ l, a = k) : l = [k] := by
  cases l with
  | nil => exact False.elim (he rfl)
  | cons a l =>
    have ha := hc a (List.mem_cons_self)
    subst a
    have hempty : l = [] := by
      apply List.eq_nil_iff_forall_not_mem.mpr
      intro b hb
      have hb' := hc b (List.mem_cons_of_mem _ hb)
      exact (List.nodup_cons.mp hn).1 (hb' ▸ hb)
    rw [hempty]

/-- All-three-junction normal form, with arbitrary numbers of singleton packets. -/
theorem three_junction_normalForm (ls : List (List (Fin 3)))
    (hA : [0, 1] ∈ ls) (hB : [1, 2] ∈ ls) (hC : [2, 0] ∈ ls)
    (hs : stepSum ls.flatten ≤ 3) (hn : ∀ l ∈ ls, l.Nodup) (hne : ∀ l ∈ ls, l ≠ []) :
    ∃ n x y z, ls.rotate n =
      [0, 1] :: (List.replicate y [1] ++ [1, 2] ::
        (List.replicate z [2] ++ [2, 0] :: List.replicate x [0])) := by
  obtain ⟨n, U, V, W, hr⟩ := junctions_cyclic_order ls hA hB hC hs
  have hs' : stepSum ([0, 1] ++ U.flatten ++ [1, 2] ++ V.flatten ++ [2, 0] ++ W.flatten) ≤ 3 := by
    have hh : stepSum (ls.rotate n).flatten ≤ 3 := by rw [stepSum_flatten_rotate]; exact hs
    simpa [hr, List.flatten_append, List.append_assoc] using hh
  obtain ⟨hu, hv, hw⟩ := anchored_gaps_constant U.flatten V.flatten W.flatten hs'
  have memls : ∀ l, l ∈ U ∨ l ∈ V ∨ l ∈ W → l ∈ ls := by
    intro l hl
    apply (List.mem_rotate (n := n)).mp
    rw [hr]
    simp only [List.mem_cons, List.mem_append]
    tauto
  have constant : ∀ (T : List (List (Fin 3))) (k : Fin 3),
      (∀ l ∈ T, l ∈ ls) → (∀ a ∈ T.flatten, a = k) → T = List.replicate T.length [k] := by
    intro T k hm hc
    apply List.eq_replicate_of_mem
    intro l hl
    exact singleton_of_packet_constant l k (hn l (hm l hl)) (hne l (hm l hl))
      (fun a ha => hc a (List.mem_flatten.mpr ⟨l, hl, ha⟩))
  have hU := constant U 1 (fun l hl => memls l (Or.inl hl)) hu
  have hV := constant V 2 (fun l hl => memls l (Or.inr (Or.inl hl))) hv
  have hW := constant W 0 (fun l hl => memls l (Or.inr (Or.inr hl))) hw
  exact ⟨n, W.length, U.length, V.length, by rw [hr, hU, hV, hW]; simp⟩

/-- The packet normal form, anchored at the 0-to-1 junction. -/
def junctionPackets (x y z : ℕ) : List (List (Fin 3)) :=
  [0, 1] :: (List.replicate y [1] ++ [1, 2] ::
    (List.replicate z [2] ++ [2, 0] :: List.replicate x [0]))

theorem flatten_replicate_singleton (n : ℕ) (k : Fin 3) :
    (List.replicate n [k]).flatten = List.replicate n k := by
  induction n with
  | zero => rfl
  | succ n ih => simp [List.replicate_succ, ih]

/-- The displayed cyclic normal form makes exactly one turn for any singleton block lengths. -/
theorem junctionPackets_stepSum (x y z : ℕ) : stepSum (junctionPackets x y z).flatten = 3 := by
  simp only [junctionPackets, List.flatten_cons, List.flatten_append, flatten_replicate_singleton]
  have hneg : (-(2 : Fin 3)).val = 1 := by decide +kernel
  simp [List.cons_append, stepSum, pathSteps_append, pathSteps,
    pathSteps_replicate_self, lastOf_replicate_self, stp, hneg]

/-- The three-anchor normal form is an equivalence, not just a necessary ordering condition. -/
theorem three_junction_normalForm_iff (ls : List (List (Fin 3)))
    (hA : [0, 1] ∈ ls) (hB : [1, 2] ∈ ls) (hC : [2, 0] ∈ ls)
    (hn : ∀ l ∈ ls, l.Nodup) (hne : ∀ l ∈ ls, l ≠ []) :
    stepSum ls.flatten ≤ 3 ↔ ∃ n x y z, ls.rotate n = junctionPackets x y z := by
  constructor
  · exact fun hs => three_junction_normalForm ls hA hB hC hs hn hne
  · rintro ⟨n, x, y, z, he⟩
    rw [← stepSum_flatten_rotate ls n, he, junctionPackets_stepSum]

/-- **Saturated C5 geometry.** Every eight-attachment nondegenerate normal form is a
cyclic sequence of the three shared junctions separated by exactly two singleton packets. -/
theorem NecklaceCuts.saturated_cyclic_normalForm (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) (ha : s.a + s.b + s.c = 8) :
    ∃ n x y z, x + y + z = 2 ∧ s.packets.rotate n = junctionPackets x y z := by
  obtain ⟨he, hx, hz⟩ := (s.eight_iff_three_junctions_two_singletons h hd).mp ha
  have ha0 := s.junctions_all_one he 0
  have ha1 := s.junctions_all_one he 1
  have ha2 := s.junctions_all_one he 2
  have hA : [0, 1] ∈ s.packets := List.count_pos_iff.mp (by simp +decide at ha0; omega)
  have hB : [1, 2] ∈ s.packets := List.count_pos_iff.mp (by simp +decide at ha1; omega)
  have hC : [2, 0] ∈ s.packets := List.count_pos_iff.mp (by simp +decide at ha2; omega)
  have hn : ∀ l ∈ s.packets, l.Nodup := by
    intro l hl
    rw [s.packets_eq_ofFn, List.mem_ofFn] at hl
    obtain ⟨i, rfl⟩ := hl
    exact h i
  have hne : ∀ l ∈ s.packets, l ≠ [] := by
    intro l hl he
    subst l
    have hz' : s.packets.count [] = 0 := hz
    exact List.count_eq_zero.mp hz' hl
  obtain ⟨n, x, y, z, hnform⟩ := (three_junction_normalForm_iff s.packets hA hB hC hn hne).mp
    s.stepSum_le_three
  have hlen := congrArg List.length hnform
  simp only [List.length_rotate, s.packets_length, junctionPackets, List.length_cons,
    List.length_append, List.length_replicate] at hlen
  exact ⟨n, x, y, z, by omega, hnform⟩

/-- The saturated cyclic classification stated directly for the original attachment word. -/
theorem runOK_saturated_normalForm (w : Word) (ρ : Run) (h : RunOK w ρ)
    (hd : ∀ k, 2 ≤ (linksOf w k).card) (ha : attachmentCount w = 8) :
    ∃ s : NecklaceCuts, s.Valid ∧ s.word = w ∧
      ∃ n x y z, x + y + z = 2 ∧ s.packets.rotate n = junctionPackets x y z := by
  obtain ⟨s, hs, he⟩ := normalForm_of_runOK w ρ h
  refine ⟨s, hs, he, ?_⟩
  apply s.saturated_cyclic_normalForm hs
  · rw [he]; exact hd
  · rw [← s.attachmentCount_eq_total hs, he]; exact ha

end FiveBoundary.GeometryDFA
