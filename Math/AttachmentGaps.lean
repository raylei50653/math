/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.AttachmentSaturated

/-! # Three shared junctions with empty boundary positions

Keep empty packets in place: each anchored gap is a word over the empty packet
and its unique permitted singleton. The equivalence works at any boundary length.
-/

namespace FiveBoundary.GeometryDFA
open ColorDFA

/-- Empty boundary positions are retained, rather than quotiented away. -/
def GapPackets (k : Fin 3) (T : List (List (Fin 3))) : Prop :=
  ∀ l ∈ T, l = [] ∨ l = [k]

theorem gapPackets_of_constant (T : List (List (Fin 3))) (k : Fin 3)
    (hn : ∀ l ∈ T, l.Nodup) (hc : ∀ a ∈ T.flatten, a = k) : GapPackets k T := by
  intro l hl
  by_cases he : l = []
  · exact Or.inl he
  · exact Or.inr (singleton_of_packet_constant l k (hn l hl) he
      (fun a ha => hc a (List.mem_flatten.mpr ⟨l, hl, ha⟩)))

theorem GapPackets.flatten_eq (k : Fin 3) (T : List (List (Fin 3)))
    (h : GapPackets k T) : T.flatten = List.replicate (T.count [k]) k := by
  induction T with
  | nil => simp
  | cons l T ih =>
    have ht := ih (fun l hl => h l (List.mem_cons_of_mem _ hl))
    rcases h l List.mem_cons_self with rfl | rfl <;> simp [ht, List.replicate_succ]

theorem GapPackets.inventory (k : Fin 3) (T : List (List (Fin 3)))
    (h : GapPackets k T) : T.count [] + T.count [k] = T.length := by
  induction T with
  | nil => simp
  | cons l T ih =>
    have ht := ih (fun l hl => h l (List.mem_cons_of_mem _ hl))
    rcases h l List.mem_cons_self with rfl | rfl <;> simp at * <;> omega

/-- Full cyclic normal form with empty packets allowed in each of the three gaps. -/
theorem three_junction_gaps_iff (ls : List (List (Fin 3)))
    (hA : [0, 1] ∈ ls) (hB : [1, 2] ∈ ls) (hC : [2, 0] ∈ ls)
    (hn : ∀ l ∈ ls, l.Nodup) :
    stepSum ls.flatten ≤ 3 ↔
      ∃ n U V W, ls.rotate n = [0, 1] :: (U ++ [1, 2] :: (V ++ [2, 0] :: W)) ∧
        GapPackets 1 U ∧ GapPackets 2 V ∧ GapPackets 0 W := by
  constructor
  · intro hs
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
    exact ⟨n, U, V, W, hr,
      gapPackets_of_constant U 1 (fun l hl => hn l (memls l (Or.inl hl))) hu,
      gapPackets_of_constant V 2 (fun l hl => hn l (memls l (Or.inr (Or.inl hl)))) hv,
      gapPackets_of_constant W 0 (fun l hl => hn l (memls l (Or.inr (Or.inr hl)))) hw⟩
  · rintro ⟨n, U, V, W, hr, hu, hv, hw⟩
    have he : (ls.rotate n).flatten =
        (junctionPackets (W.count [0]) (U.count [1]) (V.count [2])).flatten := by
      simp [hr, junctionPackets, List.flatten_append, hu.flatten_eq, hv.flatten_eq,
        hw.flatten_eq]
    rw [← stepSum_flatten_rotate ls n, he, junctionPackets_stepSum]

/-- In C5, exactly two boundary positions remain between the three anchors.
Their empty-packet count is preserved, so this covers the two nonsaturated
three-junction regimes as well as the saturated regime. -/
theorem NecklaceCuts.three_junction_cyclic_gaps (s : NecklaceCuts) (h : s.Valid)
    (he : s.junctionTotal = 3) :
    ∃ n U V W, s.packets.rotate n =
        [0, 1] :: (U ++ [1, 2] :: (V ++ [2, 0] :: W)) ∧
      GapPackets 1 U ∧ GapPackets 2 V ∧ GapPackets 0 W ∧
      U.length + V.length + W.length = 2 ∧
      U.count [] + V.count [] + W.count [] = s.emptyTotal := by
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
  obtain ⟨n, U, V, W, hr, hu, hv, hw⟩ :=
    (three_junction_gaps_iff s.packets hA hB hC hn).mp s.stepSum_le_three
  have hlen := congrArg List.length hr
  simp only [List.length_rotate, s.packets_length, List.length_cons,
    List.length_append] at hlen
  have hcount := congrArg (List.count []) hr
  rw [(List.rotate_perm s.packets n).count_eq] at hcount
  simp only [List.count_cons, List.count_append] at hcount
  refine ⟨n, U, V, W, hr, hu, hv, hw, by omega, ?_⟩
  simpa [NecklaceCuts.emptyTotal, Nat.add_assoc] using hcount.symm

/-- The two free boundary positions split exactly into empty positions and
the permitted singleton positions; no placement information is erased. -/
theorem NecklaceCuts.three_junction_gap_inventory (s : NecklaceCuts) (h : s.Valid)
    (he : s.junctionTotal = 3) :
    ∃ n U V W, s.packets.rotate n =
        [0, 1] :: (U ++ [1, 2] :: (V ++ [2, 0] :: W)) ∧
      GapPackets 1 U ∧ GapPackets 2 V ∧ GapPackets 0 W ∧
      U.count [] + V.count [] + W.count [] = s.emptyTotal ∧
      U.count [1] + V.count [2] + W.count [0] + s.emptyTotal = 2 := by
  obtain ⟨n, U, V, W, hr, hu, hv, hw, hl, hz⟩ := s.three_junction_cyclic_gaps h he
  have := hu.inventory
  have := hv.inventory
  have := hw.inventory
  exact ⟨n, U, V, W, hr, hu, hv, hw, hz, by omega⟩

end FiveBoundary.GeometryDFA
