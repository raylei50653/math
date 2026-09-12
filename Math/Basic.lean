/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Mathlib

/-!
# Starter examples

These should compile immediately if mathlib's cache is present.
Open this file in VS Code with the Lean 4 extension to see the infoview.
-/

/-- Direct lemma: addition on `ℕ` is commutative. -/
example (n m : ℕ) : n + m = m + n :=
  Nat.add_comm n m

/-- Tactic proof: a numeric identity. -/
example : 2 + 2 = 4 := by
  norm_num

/-- `2` is prime. `decide` closes finite decidable goals. -/
theorem two_prime : Nat.Prime 2 := by
  decide

/-- Squares of reals are nonnegative. -/
example (x : ℝ) : 0 ≤ x ^ 2 :=
  sq_nonneg x
