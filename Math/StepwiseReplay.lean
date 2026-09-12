/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.StripGraph
import Math.StepwiseState
import Math.StepwiseGenerated

/-! Replay of the stored fan 4 / fan 5 residual classification through the verified strip
checker.  Two kinds of statement:

* `fan4_nerode_lower_bound`, `fan5_nerode_lower_bound`: the true extendability language of
  the one-row strip with fan 4 (resp. 5) has at least 55 (resp. 97) distinct right
  residuals.  Every separator endpoint is re-decided by `StripGraph.verdict`; the Python
  DFA is not trusted for this.
* `fan4_table_replay`, `fan5_table_replay`: on every boundary word of length at most 7 the
  stored minimised table agrees with the strip semantics.  This is a finite consistency
  check of the table, not a proof that it is the residual automaton.

Native computation is intentional; see docs/automata.md for the trust boundary. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
namespace StepwiseReplay
open StripGraph
open StepwiseData (fan4Live fan5Live fan4Delta fan5Delta)
set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- Exported words are lists of naturals; colours are taken modulo 4. -/
def toWord (l : List ℕ) : List (Fin 4) := l.map fun x => ⟨x % 4, Nat.mod_lt _ (by decide)⟩

def toSeps (l : List (ℕ × ℕ × List ℕ)) : List (ℕ × ℕ × List (Fin 4)) :=
  l.map fun t => (t.1, t.2.1, toWord t.2.2)

def fan4Reps : List (List (Fin 4)) := StepwiseData.fan4Reps.map toWord
def fan5Reps : List (List (Fin 4)) := StepwiseData.fan5Reps.map toWord
def fan4Seps : List (ℕ × ℕ × List (Fin 4)) := toSeps StepwiseData.fan4Seps
def fan5Seps : List (ℕ × ℕ × List (Fin 4)) := toSeps StepwiseData.fan5Seps

/-! ### Lower bounds on the number of residuals -/

theorem fan4_separated : separatesAll [4] fan4Reps fan4Seps = true := by native_decide
theorem fan5_separated : separatesAll [5] fan5Reps fan5Seps = true := by native_decide

theorem fan4_reps_length : fan4Reps.length = 55 := by decide
theorem fan5_reps_length : fan5Reps.length = 97 := by decide

theorem fan4_residuals_injective :
    Function.Injective fun q : Fin fan4Reps.length => residual [4] fan4Reps[q] :=
  residual_injective fan4_separated

theorem fan5_residuals_injective :
    Function.Injective fun q : Fin fan5Reps.length => residual [5] fan5Reps[q] :=
  residual_injective fan5_separated

theorem encard_range_residuals_ge {fans : List ℕ} {reps : List (List (Fin 4))}
    {seps : List (ℕ × ℕ × List (Fin 4))} (h : separatesAll fans reps seps = true) :
    (reps.length : ℕ∞) ≤ (Set.range (residual fans)).encard := by
  have hsub : Set.range (fun q : Fin reps.length => residual fans reps[q]) ⊆
      Set.range (residual fans) := by
    rintro _ ⟨q, rfl⟩
    exact ⟨_, rfl⟩
  calc (reps.length : ℕ∞)
      = (Set.range fun q : Fin reps.length => residual fans reps[q]).encard := by
        rw [← (Set.finite_range _).cast_ncard_eq, residual_range_ncard h]
    _ ≤ _ := Set.encard_le_encard hsub

/-- Negative control: dropping one separator or replacing one by a non-separating word
is detected. -/
example : separatesAll [4] fan4Reps (fan4Seps.drop 1) = false := by native_decide
example : separatesAll [4] fan4Reps
    (fan4Seps.map fun t => if t.1 = 0 ∧ t.2.1 = 1 then (0, 1, [1]) else t) = false := by
  native_decide

/-- The one-row fan-4 strip language has at least 55 distinct right residuals. -/
theorem fan4_nerode_lower_bound : (55 : ℕ∞) ≤ (Set.range (residual [4])).encard := by
  have := encard_range_residuals_ge fan4_separated
  rwa [fan4_reps_length] at this

/-- The one-row fan-5 strip language has at least 97 distinct right residuals. -/
theorem fan5_nerode_lower_bound : (97 : ℕ∞) ≤ (Set.range (residual [5])).encard := by
  have := encard_range_residuals_ge fan5_separated
  rwa [fan5_reps_length] at this

/-! ### Finite replay of the stored tables -/

def tableStep (delta : List (List ℕ)) (s : ℕ) (c : Fin 4) : ℕ := (delta.getD s []).getD c.val 0
def tableLive (live : List Bool) (s : ℕ) : Bool := live.getD s false

/-- All boundary words of exactly length `n`. -/
def wordsOfLength : ℕ → List (List (Fin 4))
  | 0 => [[]]
  | n + 1 => (wordsOfLength n).flatMap fun w => (List.finRange 4).map fun c => c :: w

theorem mem_wordsOfLength {n : ℕ} {w : List (Fin 4)} : w ∈ wordsOfLength n ↔ w.length = n := by
  induction n generalizing w with
  | zero => simp [wordsOfLength]
  | succ n ih =>
    simp only [wordsOfLength, List.mem_flatMap, List.mem_map, List.mem_finRange, true_and]
    constructor
    · rintro ⟨u, hu, c, rfl⟩
      simp [ih.mp hu]
    · intro h
      cases w with
      | nil => simp at h
      | cons c u => exact ⟨u, ih.mpr (by simpa using h), c, rfl⟩

def wordsUpTo (n : ℕ) : List (List (Fin 4)) := (List.range (n + 1)).flatMap wordsOfLength

theorem mem_wordsUpTo {n : ℕ} {w : List (Fin 4)} : w ∈ wordsUpTo n ↔ w.length ≤ n := by
  simp only [wordsUpTo, List.mem_flatMap, List.mem_range, mem_wordsOfLength]
  constructor
  · rintro ⟨k, hk, rfl⟩; omega
  · intro h; exact ⟨w.length, by omega, rfl⟩

def tableAgrees (fans : List ℕ) (delta : List (List ℕ)) (live : List Bool) (n : ℕ) : Bool :=
  (wordsUpTo n).all fun w =>
    verdict fans w == some (tableLive live (StepwiseState.run (tableStep delta) 0 w))

theorem fan4_table_replay : tableAgrees [4] fan4Delta fan4Live 7 = true := by native_decide
theorem fan5_table_replay : tableAgrees [5] fan5Delta fan5Live 7 = true := by native_decide

/-- Negative control: reviving the dead class breaks the replay. -/
example : tableAgrees [5] fan5Delta (fan5Live.set 5 true) 7 = false := by native_decide

theorem extendable_iff_table {fans : List ℕ} {delta : List (List ℕ)} {live : List Bool} {n : ℕ}
    (h : tableAgrees fans delta live n = true) (w : List (Fin 4)) (hw : w.length ≤ n) :
    Extendable fans w ↔ tableLive live (StepwiseState.run (tableStep delta) 0 w) = true := by
  have := (List.all_eq_true.mp h) w (mem_wordsUpTo.mpr hw)
  exact verdict_iff (beq_iff_eq.mp this)

/-- On every word of length ≤ 7, the stored fan-5 table's liveness is the strip semantics. -/
theorem fan5_extendable_iff (w : List (Fin 4)) (hw : w.length ≤ 7) :
    Extendable [5] w ↔ tableLive fan5Live (StepwiseState.run (tableStep fan5Delta) 0 w) = true :=
  extendable_iff_table fan5_table_replay w hw

theorem fan4_extendable_iff (w : List (Fin 4)) (hw : w.length ≤ 7) :
    Extendable [4] w ↔ tableLive fan4Live (StepwiseState.run (tableStep fan4Delta) 0 w) = true :=
  extendable_iff_table fan4_table_replay w hw

end StepwiseReplay
