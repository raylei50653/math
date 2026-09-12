/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.AttachmentNormalForm

/-! # Incidence signatures of attachment normal forms

Count empty boundary packets, singleton packets, and shared-junction packets.
This is geometry only. Scalar incidence regimes are distinguished from a classification
of their cyclic placements; no word enumeration or Hall witness enters these proofs. -/

namespace FiveBoundary.GeometryDFA
open ColorDFA

/-- The packet alphabet of a normal form with all attachment degrees at least two. -/
def PacketAlphabet (l : List (Fin 3)) : Prop :=
  l = [] ∨ (∃ p, l = [p]) ∨ (∃ p, l = [p, p + 1])

/-- Counting packets in the nondegenerate alphabet. -/
theorem packet_inventory (ls : List (List (Fin 3))) (h : ∀ l ∈ ls, PacketAlphabet l) :
    ls.length = ls.count [] + ls.count [0] + ls.count [1] + ls.count [2] +
      ls.count [0, 1] + ls.count [1, 2] + ls.count [2, 0] ∧
    ls.flatten.length = ls.count [0] + ls.count [1] + ls.count [2] +
      2 * (ls.count [0, 1] + ls.count [1, 2] + ls.count [2, 0]) := by
  induction ls with
  | nil => simp
  | cons l ls ih =>
    obtain ⟨hi, hj⟩ := ih (fun l hl => h l (List.mem_cons_of_mem _ hl))
    have hl := h l (by simp)
    rcases hl with rfl | ⟨p, rfl⟩ | ⟨p, rfl⟩
    · simp only [List.length_cons, List.flatten_cons, List.nil_append, List.count_cons] at *
      simp +decide at *
      omega
    · fin_cases p <;>
        simp only [List.length_cons, List.flatten_cons, List.length_append,
          List.count_cons] at * <;>
        simp +decide at * <;> omega
    · fin_cases p <;>
        simp only [List.length_cons, List.flatten_cons, List.length_append,
          List.count_cons] at * <;>
        simp +decide at * <;> omega

namespace NecklaceCuts

def singletonTotal (s : NecklaceCuts) : ℕ := ∑ k : Fin 3, s.packets.count [k]
def junctionTotal (s : NecklaceCuts) : ℕ := ∑ k : Fin 3, s.packets.count [k, k + 1]
def emptyTotal (s : NecklaceCuts) : ℕ := s.packets.count []

theorem attachmentCount_eq_total (s : NecklaceCuts) (h : s.Valid) :
    attachmentCount s.word = s.a + s.b + s.c := by
  have hc : attachmentCount s.word = s.widths.sum := by
    rw [← s.packet_lengths, s.packets_eq_ofFn]
    rw [List.ofFn_eq_map, List.map_map, ← List.ofFn_eq_map, List.sum_ofFn]
    simp only [Function.comp_def, s.packet_length_eq_card h, attachmentCount]
  exact hc.trans s.total

theorem alphabet (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) : ∀ l ∈ s.packets, PacketAlphabet l := by
  intro l hl
  rw [s.packets_eq_ofFn, List.mem_ofFn] at hl
  obtain ⟨i, rfl⟩ := hl
  exact s.packet_shape h hd i

/-- Exactly five boundary packets, and each junction packet contributes two attachments. -/
theorem inventory (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) :
    s.emptyTotal + s.singletonTotal + s.junctionTotal = 5 ∧
    s.singletonTotal + 2 * s.junctionTotal = s.a + s.b + s.c := by
  obtain ⟨hp, hc⟩ := packet_inventory s.packets (s.alphabet h hd)
  rw [s.packets_length] at hp
  rw [s.packets_flatten] at hc
  simp only [List.length_rotate, necklace, List.length_append, List.length_replicate] at hc
  simp only [singletonTotal, junctionTotal, emptyTotal, Fin.sum_univ_three]
  simp +decide at *
  omega

theorem junctionTotal_le_three (s : NecklaceCuts) : s.junctionTotal ≤ 3 := by
  have h0 := s.forward_pair_count_le_one 0
  have h1 := s.forward_pair_count_le_one 1
  have h2 := s.forward_pair_count_le_one 2
  simp only [junctionTotal, Fin.sum_univ_three]
  omega

/-- Six scalar regimes; cyclic placement is intentionally not asserted here. -/
def IncidenceRegime (s : NecklaceCuts) : Prop :=
  (s.junctionTotal = 1 ∧ s.singletonTotal = 4 ∧ s.emptyTotal = 0) ∨
  (s.junctionTotal = 2 ∧ s.singletonTotal = 2 ∧ s.emptyTotal = 1) ∨
  (s.junctionTotal = 2 ∧ s.singletonTotal = 3 ∧ s.emptyTotal = 0) ∨
  (s.junctionTotal = 3 ∧ s.singletonTotal = 0 ∧ s.emptyTotal = 2) ∨
  (s.junctionTotal = 3 ∧ s.singletonTotal = 1 ∧ s.emptyTotal = 1) ∨
  (s.junctionTotal = 3 ∧ s.singletonTotal = 2 ∧ s.emptyTotal = 0)

/-- **Structural incidence classification.** The six regimes follow by arithmetic from
three blocks, three possible shared junctions, and five boundary positions. -/
theorem incidenceRegime (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) : s.IncidenceRegime := by
  obtain ⟨hp, hc⟩ := s.inventory h hd
  obtain ⟨ha, hb, hc'⟩ := s.degrees h
  have h0 := hd (pos s.orientation 0)
  have h1 := hd (pos s.orientation 1)
  have h2 := hd (pos s.orientation 2)
  have he := s.junctionTotal_le_three
  unfold IncidenceRegime
  omega

/-- Eight attachments exactly saturate all three shared junctions and leave two singletons. -/
theorem eight_iff_three_junctions_two_singletons (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) :
    s.a + s.b + s.c = 8 ↔
      s.junctionTotal = 3 ∧ s.singletonTotal = 2 ∧ s.emptyTotal = 0 := by
  have := s.inventory h hd
  have := s.junctionTotal_le_three
  omega

theorem junctions_all_one (s : NecklaceCuts) (he : s.junctionTotal = 3) :
    ∀ k : Fin 3, s.packets.count [k, k + 1] = 1 := by
  have h0 := s.forward_pair_count_le_one 0
  have h1 := s.forward_pair_count_le_one 1
  have h2 := s.forward_pair_count_le_one 2
  simp only [junctionTotal, Fin.sum_univ_three] at he
  intro k
  fin_cases k <;> simp +decide at * <;> omega

/-- With all three junctions shared, every block already has its two endpoint attachments. -/
theorem degree_eq_singletons_add_two (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) (he : s.junctionTotal = 3) (k : Fin 3) :
    (linksOf s.word (pos s.orientation k)).card = s.packets.count [k] + 2 := by
  rw [s.degree_eq_singletons_add_junctions h hd]
  have h1 := s.junctions_all_one he k
  have h2 := s.junctions_all_one he (k + 2)
  rw [fin3_add_two_add_one] at h2
  omega

/-- Distributing two singleton packets among three blocks has two possible shapes. -/
theorem two_singletons_cases (x : Fin 3 → ℕ) (hx : (∑ k, x k) = 2) :
    (∃ k, x k = 2 ∧ ∀ j, j ≠ k → x j = 0) ∨
    (∃ k, x k = 0 ∧ ∀ j, j ≠ k → x j = 1) := by
  simp only [Fin.sum_univ_three] at hx
  simp [Fin.exists_fin_succ, Fin.forall_fin_succ]
  omega

/-- The two saturated geometric types: two singletons in one block, or one in each of two blocks. -/
theorem saturated_singleton_cases (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) (ha : s.a + s.b + s.c = 8) :
    (∃ k, s.packets.count [k] = 2 ∧ ∀ j, j ≠ k → s.packets.count [j] = 0) ∨
    (∃ k, s.packets.count [k] = 0 ∧ ∀ j, j ≠ k → s.packets.count [j] = 1) := by
  have hx := ((s.eight_iff_three_junctions_two_singletons h hd).mp ha).2.1
  exact two_singletons_cases _ hx

/-- Saturation turns the two singleton allocations into the degree types (4,2,2) or (2,3,3). -/
theorem saturated_degree_cases (s : NecklaceCuts) (h : s.Valid)
    (hd : ∀ k, 2 ≤ (linksOf s.word k).card) (ha : s.a + s.b + s.c = 8) :
    (∃ k, (linksOf s.word (pos s.orientation k)).card = 4 ∧
      ∀ j, j ≠ k → (linksOf s.word (pos s.orientation j)).card = 2) ∨
    (∃ k, (linksOf s.word (pos s.orientation k)).card = 2 ∧
      ∀ j, j ≠ k → (linksOf s.word (pos s.orientation j)).card = 3) := by
  have he := ((s.eight_iff_three_junctions_two_singletons h hd).mp ha).1
  rcases s.saturated_singleton_cases h hd ha with ⟨k, hk, hj⟩ | ⟨k, hk, hj⟩
  · refine Or.inl ⟨k, ?_, ?_⟩
    · rw [s.degree_eq_singletons_add_two h hd he, hk]
    · intro j hjk
      rw [s.degree_eq_singletons_add_two h hd he, hj j hjk]
  · refine Or.inr ⟨k, ?_, ?_⟩
    · rw [s.degree_eq_singletons_add_two h hd he, hk]
    · intro j hjk
      rw [s.degree_eq_singletons_add_two h hd he, hj j hjk]

end NecklaceCuts
end FiveBoundary.GeometryDFA
