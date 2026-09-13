/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Boundary

/-! Exact residuals for a fixed finite alphabet of pairwise-conflicting insertions.
This is an abstract grammar; no extraction from arbitrary disk patches is asserted. -/
namespace FiveBoundary.LocalWiring

variable {A : Type}

/-- Every atom is a local insertion. Conflicting pairs cannot coexist. -/
def Valid (cross : A → A → Prop) (s : Set A) : Prop :=
  ∀ a ∈ s, ∀ b ∈ s, ¬ cross a b

def forbidden (cross : A → A → Prop) (s : Set A) : Set A :=
  {b | ∃ a ∈ s, cross a b}

/-- A continuation must be internally valid and compatible with the history.
The history itself is assumed valid when using this as a live-state semantics. -/
def Continue (cross : A → A → Prop) (s t : Set A) : Prop :=
  Valid cross t ∧ ∀ b ∈ t, b ∉ forbidden cross s

theorem forbidden_union (cross : A → A → Prop) (s t : Set A) :
    forbidden cross (s ∪ t) = forbidden cross s ∪ forbidden cross t := by
  ext b
  simp only [forbidden, Set.mem_ofPred_eq, Set.mem_union]
  aesop

/-- The summary update is closed and needs no hidden history. -/
theorem update_congruent (cross : A → A → Prop) (s s' t : Set A)
    (he : forbidden cross s = forbidden cross s') :
    forbidden cross (s ∪ t) = forbidden cross (s' ∪ t) := by
  rw [forbidden_union, forbidden_union, he]

/-- Exact future equivalence: a differing bit is separated by a one-atom continuation. -/
theorem residual_exact (cross : A → A → Prop) (irr : ∀ a, ¬ cross a a)
    (s s' : Set A) :
    (∀ t, Continue cross s t ↔ Continue cross s' t) ↔
      forbidden cross s = forbidden cross s' := by
  constructor
  · intro h
    ext b
    have ht : Valid cross ({b} : Set A) := by
      intro a ha c hc
      simp only [Set.mem_singleton_iff] at ha hc
      subst a
      subst c
      exact irr b
    have hb := h {b}
    simp only [Continue, ht, true_and, Set.mem_singleton_iff,
      forall_eq] at hb
    exact not_iff_not.mp hb
  · intro he t
    simp only [Continue, he]

/-- For a symmetric conflict relation this is exactly validity of the joined support. -/
theorem continue_iff_union (cross : A → A → Prop)
    (sym : ∀ a b, cross a b → cross b a) (s t : Set A) (hs : Valid cross s) :
    Continue cross s t ↔ Valid cross (s ∪ t) := by
  simp only [Continue, Valid, forbidden, Set.mem_ofPred_eq, Set.mem_union] at *
  aesop

/-- Fixed cyclic endpoint labels; a chord has two different ordered endpoints. -/
abbrev Chord (n : ℕ) := {p : Fin n × Fin n // p.1 < p.2}

def Cross {n : ℕ} (e f : Chord n) : Prop :=
  (e.val.1 < f.val.1 ∧ f.val.1 < e.val.2 ∧ e.val.2 < f.val.2) ∨
  (f.val.1 < e.val.1 ∧ e.val.1 < f.val.2 ∧ f.val.2 < e.val.2)

theorem cross_irrefl {n : ℕ} (e : Chord n) : ¬ Cross e e := by
  simp [Cross]

theorem cross_symm {n : ℕ} (e f : Chord n) : Cross e f → Cross f e := by
  simp only [Cross]
  exact Or.symm

/-- The generic arbitrary-continuation result applies to this concrete grammar. -/
theorem chord_residual_exact {n : ℕ} (s s' : Set (Chord n)) :
    (∀ t, Continue Cross s t ↔ Continue Cross s' t) ↔
      forbidden Cross s = forbidden Cross s' :=
  residual_exact Cross cross_irrefl s s'

end FiveBoundary.LocalWiring
