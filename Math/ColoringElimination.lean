/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Mathlib.Data.Fin.Tuple.Basic
import Mathlib.Data.Set.Defs

/-!
# Exact relation elimination and compatible reconstruction

This file formalizes the relation semantics of the finite-graph coloring solver.
Elimination retains every boundary assignment with a nonempty complete fibre.
The solution equivalence records the entire fibre, rather than independent
coordinate supports. Recursive elimination on `Fin n` is specialized to original
edge and fixed-color constraints. No planarity or Four Color Theorem is assumed.

The theorems concern mathematical relations. They do not verify the Python
implementation, propagation heuristics, resource budgets, or running time.
-/

namespace ColoringElimination

universe u v w

variable {C : Type u} {X : Type v} {Y : Type w}

/-- Literal assignments on two disjoint vertex sets in a shared color frame. -/
def join (x : X → C) (y : Y → C) : X ⊕ Y → C := Sum.elim x y

/-- A complete relation on assignments to the given vertex set. -/
abbrev Relation (V : Type v) (C : Type u) := (V → C) → Prop

/-- The complete set of internal assignments compatible with one boundary row. -/
def Fibre (R : Relation (X ⊕ Y) C) (y : Y → C) :=
  { x : X → C // R (join x y) }

/-- Exact existential projection. Absent rows have an empty fibre. -/
def eliminate (R : Relation (X ⊕ Y) C) : Relation Y C :=
  fun y => ∃ x : X → C, R (join x y)

theorem eliminate_iff_nonempty_fibre (R : Relation (X ⊕ Y) C) (y : Y → C) :
    eliminate R y ↔ Nonempty (Fibre R y) := by
  constructor
  · rintro ⟨x, hx⟩
    exact ⟨⟨x, hx⟩⟩
  · rintro ⟨⟨x, hx⟩⟩
    exact ⟨x, hx⟩

/-- Restricting and rejoining a complete assignment preserves its literal colors. -/
@[simp] theorem join_restrict (s : X ⊕ Y → C) :
    join (fun x => s (.inl x)) (fun y => s (.inr y)) = s := by
  funext v
  cases v <;> rfl

/-- Every full solution is exactly one boundary row together with one full fibre member. -/
def solutionEquiv (R : Relation (X ⊕ Y) C) :
    { s : X ⊕ Y → C // R s } ≃ (Σ y : Y → C, Fibre R y) where
  toFun s := ⟨fun y => s.1 (.inr y),
    ⟨fun x => s.1 (.inl x), by simpa using s.2⟩⟩
  invFun p := ⟨join p.2.1 p.1, p.2.2⟩
  left_inv s := by
    apply Subtype.ext
    exact join_restrict s.1
  right_inv p := by
    cases p with
    | mk y x => rfl

/-- A stored fibre member reconstructs a solution over that same boundary row. -/
theorem reconstruct (R : Relation (X ⊕ Y) C) (y : Y → C) (x : Fibre R y) :
    R (join x.1 y) := x.2

theorem satisfiable_iff_eliminate (R : Relation (X ⊕ Y) C) :
    (∃ s, R s) ↔ ∃ y, eliminate R y := by
  constructor
  · rintro ⟨s, hs⟩
    refine ⟨fun y => s (.inr y), fun x => s (.inl x), ?_⟩
    simpa using hs
  · rintro ⟨y, x, hx⟩
    exact ⟨join x y, hx⟩

/-- The rest of the factors can be kept outside a bucket only when they do not
depend on the eliminated variables. The same `y` is used by both parts. -/
theorem eliminate_bucket_iff (B : (X → C) → (Y → C) → Prop)
    (Q : (Y → C) → Prop) (y : Y → C) :
    eliminate (fun s => B (fun x => s (.inl x)) (fun z => s (.inr z)) ∧
      Q (fun z => s (.inr z))) y ↔ Q y ∧ ∃ x, B x y := by
  change (∃ x, B x y ∧ Q y) ↔ Q y ∧ ∃ x, B x y
  constructor
  · rintro ⟨x, hB, hQ⟩
    exact ⟨hQ, x, hB⟩
  · rintro ⟨hQ, x, hB⟩
    exact ⟨x, hB, hQ⟩

/-- A sound propagation pass must preserve every solution, not just satisfiability. -/
theorem eliminate_congr {R R' : Relation (X ⊕ Y) C}
    (h : ∀ s, R s ↔ R' s) (y : Y → C) :
    eliminate R y ↔ eliminate R' y := by
  constructor <;> rintro ⟨x, hx⟩
  · exact ⟨x, (h _).mp hx⟩
  · exact ⟨x, (h _).mpr hx⟩

/-- Successively eliminate each coordinate, including the final zero-arity relation.
This is a proposition-valued semantics, rather than an executable search routine. -/
def reduceAll : (n : Nat) → Relation (Fin n) C → Prop
  | 0, R => R Fin.elim0
  | n + 1, R => reduceAll n (fun tail => ∃ color, R (Fin.cons color tail))

/-- Any finite number of exact coordinate eliminations preserves existence. -/
theorem reduceAll_iff_exists (n : Nat) (R : Relation (Fin n) C) :
    reduceAll n R ↔ ∃ s, R s := by
  induction n with
  | zero =>
    constructor
    · intro h
      exact ⟨Fin.elim0, h⟩
    · rintro ⟨s, hs⟩
      have hEq : s = Fin.elim0 := by
        funext i
        exact Fin.elim0 i
      simpa [reduceAll, hEq] using hs
  | succ n ih =>
    rw [reduceAll, ih]
    constructor
    · rintro ⟨tail, color, h⟩
      exact ⟨Fin.cons color tail, h⟩
    · rintro ⟨s, hs⟩
      refine ⟨Fin.tail s, s 0, ?_⟩
      simpa only [Fin.cons_self_tail] using hs

/-- The exact original-edge/fixed-color semantics. Undirected finite simple graphs
are a specialization of the arbitrary adjacency relation used here. -/
def FourColoring {V : Type v} (adj : V → V → Prop) (fixed : V → Option (Fin 4))
    (s : V → Fin 4) : Prop :=
  (∀ a b, adj a b → s a ≠ s b) ∧
  (∀ v color, fixed v = some color → s v = color)

/-- Exact elimination succeeds precisely when one common complete four-color
assignment satisfies all original edges and every supplied fixed color. -/
theorem reduceAll_fourColoring_iff (n : Nat) (adj : Fin n → Fin n → Prop)
    (fixed : Fin n → Option (Fin 4)) :
    reduceAll n (FourColoring adj fixed) ↔ ∃ s, FourColoring adj fixed s :=
  reduceAll_iff_exists n (FourColoring adj fixed)

end ColoringElimination
