/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.EdgeMask
import Mathlib.Data.Nat.BitIndices

/-! Executable natural-number popcount and viable guard. This identifies Lean
integer operations with the finite-set specification, not Python execution. -/
namespace FiveBoundary.EdgeMask

open PrefixPartition

/-- Count the set bits using the executable binary decomposition of a natural. -/
def popcount (n : ℕ) : ℕ := n.bitIndices.length

@[simp] theorem popcount_zero : popcount 0 = 0 := rfl
@[simp] theorem popcount_even (n : ℕ) : popcount (2 * n) = popcount n := by
  simp [popcount]
@[simp] theorem popcount_odd (n : ℕ) : popcount (2 * n + 1) = popcount n + 1 := by
  simp [popcount]

theorem bitIndices_encode (M : Finset ℕ) : (encode M).bitIndices.toFinset = M := by
  ext e
  simp

/-- No fixed width or upper bound on the finite set is needed. -/
@[simp] theorem popcount_encode (M : Finset ℕ) : popcount (encode M) = M.card := by
  have h := congrArg Finset.card (bitIndices_encode M)
  simpa [List.toFinset_card_of_nodup Nat.bitIndices_nodup, popcount] using h

theorem popcount_inter (M N : Finset ℕ) :
    popcount (encode M &&& encode N) = (M ∩ N).card := by
  rw [← encode_inter, popcount_encode]

theorem popcount_shift (M : Finset ℕ) (cut : ℕ) :
    popcount (encode M >>> cut) = (suffix cut M).card := by
  rw [← encode_shifted, popcount_encode, shifted_card]

/-- An executable guard with finite loops and integer incidence masks. Numeric
attachment order is deliberately distinct from ordering by popcount. -/
def viable (k : ℕ) (touch : ℕ → ℕ) (n cut : ℕ) : Bool :=
  (List.range k).all (fun m => decide (ReducedViable.blockStart m < cut →
    4 ≤ popcount (n &&& touch m) + popcount (touch m >>> cut))) &&
  (List.range k).all (fun m => decide (m + 1 < k →
    ReducedViable.blockStart (m + 1) < cut →
    ((n >>> ReducedViable.blockStart (m + 1)) &&& 31) ≤
      ((n >>> ReducedViable.blockStart m) &&& 31)))

theorem viable_encode_iff (k : ℕ) (touch : ℕ → Finset ℕ) (P : Finset ℕ) (cut : ℕ) :
    viable k (fun m => encode (touch m)) (encode P) cut = true ↔
      ReducedViable.Viable k touch P cut := by
  simp only [viable, Bool.and_eq_true, List.all_eq_true, List.mem_range,
    decide_eq_true_eq, popcount_inter, popcount_shift, attachment_value]
  unfold ReducedViable.Viable ReducedViable.degree
  constructor
  · rintro ⟨hd, ha⟩
    exact ⟨hd, fun m hm => ha m (by omega) hm⟩
  · rintro ⟨hd, ha⟩
    exact ⟨hd, fun m _ => ha m⟩

theorem integer_viable_of_survivor (k : ℕ) (touch : ℕ → Finset ℕ) (M : Finset ℕ)
    (hM : ReducedViable.Survivor k touch M) (cut : ℕ) :
    viable k (fun m => encode (touch m))
      (encode M &&& ((1 <<< cut) - 1)) cut = true := by
  rw [← encode_prefix, viable_encode_iff]
  exact ReducedViable.viable_of_survivor k touch M hM cut

/-- Raw integer masks also agree with bounded decoding when no high bit is lost. -/
theorem viable_decode_iff (k E n cut : ℕ) (touch : ℕ → Finset ℕ)
    (hn : n < 2 ^ E) :
    viable k (fun m => encode (touch m)) n cut = true ↔
      ReducedViable.Viable k touch (decode E n) cut := by
  simpa only [encode_decode_of_lt hn] using
    viable_encode_iff k touch (decode E n) cut

/-- Connect the integer guard to the already proved graph degree/attachment bridge. -/
theorem integer_viable_of_graph {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (M : Finset ℕ) (hM : ReducedGraphBridge.Represents G M)
    (hG : ReducedGraphBridge.GraphSurvivor G) (cut : ℕ) :
    viable k (fun m => encode (ReducedGraphBridge.touch k m))
      (encode M &&& ((1 <<< cut) - 1)) cut = true :=
  integer_viable_of_survivor k (ReducedGraphBridge.touch k) M
    ((ReducedGraphBridge.survivor_iff G M hM).mpr hG) cut

/-- A rejected integer prefix cannot be the prefix of any survivor. -/
theorem integer_rejection_sound (k : ℕ) (touch : ℕ → Finset ℕ) (n cut : ℕ)
    (hn : viable k (fun m => encode (touch m)) n cut = false) :
    ¬ ∃ M, encode M &&& ((1 <<< cut) - 1) = n ∧
      ReducedViable.Survivor k touch M := by
  rintro ⟨M, rfl, hM⟩
  have := integer_viable_of_survivor k touch M hM cut
  simp [hn] at this

/-- Specialize the integer DFS correspondence to the actual integer guard. -/
theorem viable_reach_iff (k : ℕ) (touch : ℕ → Finset ℕ) (oracle : ℕ → Prop)
    (stop lo s : ℕ) (base M : Finset ℕ) (phase : ReducedDFS.Phase) :
    Reach (fun n cut => viable k (fun m => encode (touch m)) n cut = true)
      oracle stop (encode base) lo phase (encode M) s ↔
    ReducedDFS.Reach (ReducedViable.Viable k touch) (fun P => oracle (encode P))
      stop base lo phase M s := by
  rw [reach_iff]
  simp only [viable_encode_iff]

end FiveBoundary.EdgeMask
