/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Mathlib.Data.Finset.Filter
import Mathlib.Data.Finset.Lattice.Basic

/-!+# Unique ownership in a prefix-split subset search

Edge indices are natural numbers. A task fixes all indices below `p` and adds
only indices at least `p`. This proves the finite-set partition, not correctness
of a Python scheduler, pruning predicate, graph mutation, or colouring tables.
-/

namespace FiveBoundary.PrefixPartition

def prefixPart (p : ℕ) (M : Finset ℕ) : Finset ℕ := M.filter (· < p)

def suffix (p : ℕ) (M : Finset ℕ) : Finset ℕ := M.filter (p ≤ ·)

/-- A task labelled `A` can produce exactly unions of its fixed prefix and a suffix. -/
def Owns (p : ℕ) (A M : Finset ℕ) : Prop :=
  (∀ e ∈ A, e < p) ∧ ∃ S : Finset ℕ, (∀ e ∈ S, p ≤ e) ∧ M = A ∪ S

theorem reconstruct (p : ℕ) (M : Finset ℕ) : prefixPart p M ∪ suffix p M = M := by
  ext e
  simp only [prefixPart, suffix, Finset.mem_union, Finset.mem_filter]
  constructor
  · rintro (⟨he, _⟩ | ⟨he, _⟩) <;> exact he
  · intro he
    by_cases h : e < p
    · exact Or.inl ⟨he, h⟩
    · exact Or.inr ⟨he, Nat.le_of_not_gt h⟩

theorem prefix_union (p : ℕ) (A S : Finset ℕ)
    (hA : ∀ e ∈ A, e < p) (hS : ∀ e ∈ S, p ≤ e) :
    prefixPart p (A ∪ S) = A := by
  ext e
  simp only [prefixPart, Finset.mem_filter, Finset.mem_union]
  constructor
  · rintro ⟨ha | hs, he⟩
    · exact ha
    · exact False.elim (Nat.not_lt_of_ge (hS e hs) he)
  · intro ha
    exact ⟨Or.inl ha, hA e ha⟩

theorem owns_iff (p : ℕ) (A M : Finset ℕ) : Owns p A M ↔ A = prefixPart p M := by
  constructor
  · rintro ⟨hA, S, hS, rfl⟩
    exact (prefix_union p A S hA hS).symm
  · rintro rfl
    refine ⟨?_, suffix p M, ?_, (reconstruct p M).symm⟩
    · intro e he
      exact (Finset.mem_filter.mp he).2
    · intro e he
      exact (Finset.mem_filter.mp he).2

/-- Each target has exactly one possible task label, including the empty target. -/
theorem unique_owner (p : ℕ) (M : Finset ℕ) : ∃! A, Owns p A M := by
  refine ⟨prefixPart p M, (owns_iff p _ _).mpr rfl, ?_⟩
  intro A hA
  exact (owns_iff p A M).mp hA

/-- Distinct labels cannot produce the same target. -/
theorem owners_equal {p : ℕ} {A B M : Finset ℕ}
    (hA : Owns p A M) (hB : Owns p B M) : A = B := by
  exact ((owns_iff p A M).mp hA).trans ((owns_iff p B M).mp hB).symm

/-- After pruning the task labels, coverage is exactly retention of the target's prefix.
The caller must establish this membership from the pruning predicate's soundness. -/
theorem covered_iff (p : ℕ) (tasks : Finset (Finset ℕ)) (M : Finset ℕ) :
    (∃ A ∈ tasks, Owns p A M) ↔ prefixPart p M ∈ tasks := by
  simp only [owns_iff]
  constructor
  · rintro ⟨A, hA, rfl⟩
    exact hA
  · intro h
    exact ⟨prefixPart p M, h, rfl⟩

/-- If all target indices are below the cut, its owner is the target itself.
At `p = E` this is the direct-record branch; workers must not record it again. -/
theorem owner_at_end (p : ℕ) (M : Finset ℕ) (hM : ∀ e ∈ M, e < p) :
    prefixPart p M = M := by
  exact Finset.filter_true_of_mem hM

end FiveBoundary.PrefixPartition
