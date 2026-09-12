/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Mathlib

/-! Generic deterministic-state lemmas for stepwise sufficiency.
No strip graph or generated Python automaton is certified by this module.
The hypotheses about colour actions and loop states must be discharged separately.
-/
namespace StepwiseState

variable {S C : Type*}

def run (step : S → C → S) (s : S) : List C → S
  | [] => s
  | c :: w => run step (step s c) w

theorem run_append (step : S → C → S) (s : S) (u v : List C) :
    run step s (u ++ v) = run step (run step s u) v := by
  induction u generalizing s with
  | nil => rfl
  | cons c u ih => exact ih (step s c)

/-- The state and continuation must be renamed by the same colour permutation. -/
theorem run_rename (step : S → C → S) (rename : Equiv.Perm C → S → S)
    (equivariant : ∀ p s c, rename p (step s c) = step (rename p s) (p c))
    (p : Equiv.Perm C) (s : S) (w : List C) :
    run step (rename p s) (w.map p) = rename p (run step s w) := by
  induction w generalizing s with
  | nil => rfl
  | cons c w ih =>
    simp only [List.map_cons, run, ← equivariant]
    exact ih (step s c)

/-- A local change of register frame after reading a colour preserves alignment.
This applies to move-to-front recency frames, as well as any other permutation.
-/
theorem register_update (step : S → C → S) (rename : Equiv.Perm C → S → S)
    (equivariant : ∀ p s c, rename p (step s c) = step (rename p s) (p c))
    (compose : ∀ p m s, rename m (rename p s) = rename (p.trans m) s)
    (p m : Equiv.Perm C) (s : S) (c : C) :
    rename m (step (rename p s) (p c)) = rename (p.trans m) (step s c) := by
  rw [← equivariant, compose]

theorem aligned_acceptance (step : S → C → S) (rename : Equiv.Perm C → S → S)
    (accept : S → Prop)
    (equivariant : ∀ p s c, rename p (step s c) = step (rename p s) (p c))
    (invariant : ∀ p s, accept (rename p s) ↔ accept s)
    (p : Equiv.Perm C) (s : S) (w : List C) :
    accept (run step (rename p s) (w.map p)) ↔ accept (run step s w) := by
  rw [run_rename step rename equivariant, invariant]

def repeatWord (u : List C) : ℕ → List C
  | 0 => []
  | k + 1 => u ++ repeatWord u k

theorem run_repeat_loop (step : S → C → S) (s : S) (u : List C)
    (loop : run step s u = s) (k : ℕ) :
    run step s (repeatWord u k) = s := by
  induction k with
  | zero => rfl
  | succ k ih => rw [repeatWord, run_append, loop, ih]

/-- A common loop can preserve a distinction across arbitrarily many copies.
The finite checker supplies the prefixes, loop, and distinguishing suffix;
this ordinary proof supplies the quantification over all repetition counts.
-/
theorem pumped_distinction (step : S → C → S) (accept : S → Prop)
    (s t : S) (u x : List C)
    (loop_s : run step s u = s) (loop_t : run step t u = t)
    (separates : ¬ (accept (run step s x) ↔ accept (run step t x))) (k : ℕ) :
    ¬ (accept (run step s (repeatWord u k ++ x)) ↔
       accept (run step t (repeatWord u k ++ x))) := by
  simpa only [run_append, run_repeat_loop step s u loop_s,
    run_repeat_loop step t u loop_t] using separates

end StepwiseState
