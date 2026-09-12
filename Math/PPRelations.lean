/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.GadgetRelations

/-!
Thin pp syntax and denotation over the existing gadget relation operations.

Binders are de Bruijn: `Formula.ex` hides the last index via `Fin.snoc`.
Conjunction never captures independently bound existentials by name coincidence.
This file does not assert geometry or catalog realizability.
-/
namespace FiveBoundary.PP
open Gadget (meet hide hide_shared identity)

/-- Prenex-capable pp formulas with `n` free colour (or value) positions. -/
inductive Formula (α : Type) : ℕ → Type
  | atom {n k : ℕ} (r : (Fin k → α) → Prop) (args : Fin k → Fin n) : Formula α n
  | and {n : ℕ} : Formula α n → Formula α n → Formula α n
  | ex {n : ℕ} : Formula α (n + 1) → Formula α n

/-- Assignment of `n` values. -/
abbrev Assign (α : Type) (n : ℕ) := Fin n → α

/-- View a unary predicate as a `Gadget.Rel` into `Unit`, so `meet` applies. -/
def asRel {X : Type} (p : X → Prop) : Gadget.Rel X Unit := fun x _ => p x

/-- Denotation: a predicate on assignments of the free variables. -/
def eval {α : Type} : {n : ℕ} → Formula α n → Assign α n → Prop
  | _, .atom r args, ρ => r (ρ ∘ args)
  | _, .and φ ψ, ρ => eval φ ρ ∧ eval ψ ρ
  | _, .ex φ, ρ => hide (fun ρ z => eval φ (Fin.snoc ρ z)) ρ

theorem eval_atom {α : Type} {n k : ℕ} (r : (Fin k → α) → Prop) (args : Fin k → Fin n)
    (ρ : Assign α n) : eval (.atom r args) ρ ↔ r (ρ ∘ args) :=
  Iff.rfl

/-- Conjunction is pointwise intersection. -/
theorem eval_and {α : Type} {n : ℕ} (φ ψ : Formula α n) :
    eval (φ.and ψ) = fun ρ => eval φ ρ ∧ eval ψ ρ :=
  rfl

/-- The same law as a `Gadget.meet` identity. -/
theorem eval_and_meet {α : Type} {n : ℕ} (φ ψ : Formula α n) :
    asRel (eval (φ.and ψ)) = meet (asRel (eval φ)) (asRel (eval ψ)) :=
  rfl

/-- Existential elimination is exactly `Gadget.hide` of the last variable. -/
theorem eval_ex_hide {α : Type} {n : ℕ} (φ : Formula α (n + 1)) :
    eval φ.ex = hide (fun ρ z => eval φ (Fin.snoc ρ z)) :=
  rfl

theorem eval_ex_iff {α : Type} {n : ℕ} (φ : Formula α (n + 1)) (ρ : Assign α n) :
    eval φ.ex ρ ↔ ∃ z, eval φ (Fin.snoc ρ z) :=
  Iff.rfl

/-- Independently bound existentials remain two separate `hide`s after conjunction. -/
theorem eval_and_ex {α : Type} {n : ℕ} (φ ψ : Formula α (n + 1)) :
    eval (φ.ex.and ψ.ex) =
      fun ρ => hide (fun ρ z => eval φ (Fin.snoc ρ z)) ρ ∧
               hide (fun ρ z => eval ψ (Fin.snoc ρ z)) ρ :=
  rfl

/-- A shared binder is `hide` of the pointwise `meet` (same witness). -/
theorem eval_ex_and {α : Type} {n : ℕ} (φ ψ : Formula α (n + 1)) :
    eval (φ.and ψ).ex =
      hide (meet (fun (ρ : Assign α n) z => eval φ (Fin.snoc ρ z))
                 (fun ρ z => eval ψ (Fin.snoc ρ z))) :=
  rfl

theorem eval_ex_and_hide_shared {α : Type} {n : ℕ} (φ ψ : Formula α (n + 1)) :
    eval (φ.and ψ).ex =
      hide (fun ρ z => eval φ (Fin.snoc ρ z) ∧ eval ψ (Fin.snoc ρ z)) :=
  hide_shared (fun ρ z => eval φ (Fin.snoc ρ z)) (fun ρ z => eval ψ (Fin.snoc ρ z))

/-- Shared witnesses imply independently hidden witnesses; the converse is false. -/
theorem eval_ex_and_imp_and_ex {α : Type} {n : ℕ} (φ ψ : Formula α (n + 1))
    (ρ : Assign α n) : eval (φ.and ψ).ex ρ → eval (φ.ex.and ψ.ex) ρ := by
  rintro ⟨z, hφ, hψ⟩
  exact ⟨⟨z, hφ⟩, ⟨z, hψ⟩⟩

/-- Binary atom from an existing `Gadget.Rel`. -/
def pair {n : ℕ} (i j : Fin n) : Fin 2 → Fin n := ![i, j]

theorem pair_zero {n : ℕ} (i j : Fin n) : pair i j 0 = i := rfl

theorem pair_one {n : ℕ} (i j : Fin n) : pair i j 1 = j := rfl

def ofRel {α : Type} {n : ℕ} (r : Gadget.Rel α α) (i j : Fin n) : Formula α n :=
  .atom (fun v => r (v 0) (v 1)) (pair i j)

theorem eval_ofRel {α : Type} {n : ℕ} (r : Gadget.Rel α α) (i j : Fin n)
    (ρ : Assign α n) : eval (ofRel r i j) ρ ↔ r (ρ i) (ρ j) :=
  Iff.rfl

/-- Logical equality atom; not a cofacial equality wire. -/
def eq {α : Type} {n : ℕ} (i j : Fin n) : Formula α n :=
  ofRel (identity α) i j

theorem eval_eq {α : Type} {n : ℕ} (i j : Fin n) (ρ : Assign α n) :
    eval (eq i j) ρ ↔ ρ i = ρ j :=
  eval_ofRel (identity α) i j ρ

theorem eval_eq_snoc {α : Type} (i : Fin 2) (ρ : Assign α 2) (z : α) :
    eval (eq i.castSucc (2 : Fin 3)) (Fin.snoc ρ z) ↔ ρ i = z := by
  rw [eval_eq, Fin.snoc_castSucc]
  have hlast : (2 : Fin 3) = Fin.last 2 := rfl
  rw [hlast, Fin.snoc_last]

/-- `∃ z, EQ(x,z) ∧ EQ(y,z)` with free `x = 0`, `y = 1` and bound `z = 2`. -/
def sharedEQ {α : Type} : Formula α 2 :=
  (eq (0 : Fin 3) 2 |>.and (eq (1 : Fin 3) 2)).ex

/-- `(∃ z, EQ(x,z)) ∧ (∃ w, EQ(y,w))`; the two binders are distinct constructors. -/
def independentEQ {α : Type} : Formula α 2 :=
  (eq (0 : Fin 3) 2).ex |>.and (eq (1 : Fin 3) 2).ex

theorem sharedEQ_forces {α : Type} (ρ : Assign α 2) :
    eval (sharedEQ (α := α)) ρ ↔ ρ 0 = ρ 1 := by
  constructor
  · rintro ⟨z, hz⟩
    have h0 := (eval_eq_snoc 0 ρ z).mp hz.1
    have h1 := (eval_eq_snoc 1 ρ z).mp hz.2
    exact h0.trans h1.symm
  · intro h
    refine ⟨ρ 0, ?_⟩
    exact ⟨(eval_eq_snoc 0 ρ (ρ 0)).mpr rfl, (eval_eq_snoc 1 ρ (ρ 0)).mpr h.symm⟩

theorem independentEQ_holds {α : Type} (ρ : Assign α 2) :
    eval (independentEQ (α := α)) ρ :=
  ⟨⟨ρ 0, (eval_eq_snoc 0 ρ (ρ 0)).mpr rfl⟩, ⟨ρ 1, (eval_eq_snoc 1 ρ (ρ 1)).mpr rfl⟩⟩

theorem independentEQ_not_eq {α : Type} {a b : α} (hne : a ≠ b) :
    ¬ ∀ ρ : Assign α 2, eval (independentEQ (α := α)) ρ → ρ 0 = ρ 1 := by
  intro h
  let ρ : Assign α 2 := ![a, b]
  exact hne (h ρ (independentEQ_holds ρ))

/-- Shared hidden witness forces `x = y`; independent witnesses do not. -/
theorem shared_not_independent {α : Type} {a b : α} (hne : a ≠ b) :
    ∃ ρ : Assign α 2,
      eval (independentEQ (α := α)) ρ ∧ ¬ eval (sharedEQ (α := α)) ρ := by
  refine ⟨![a, b], independentEQ_holds _, ?_⟩
  intro h
  exact hne ((sharedEQ_forces _).mp h)

/-- Colour regression: `∃z. EQ(x,z)∧EQ(y,z)` vs independent existentials. -/
theorem sharedEQ_forces_color (ρ : Assign Color 2) :
    eval (sharedEQ (α := Color)) ρ ↔ ρ 0 = ρ 1 :=
  sharedEQ_forces ρ

theorem independentEQ_free_color :
    (∀ ρ : Assign Color 2, eval (independentEQ (α := Color)) ρ) ∧
    ¬ ∀ ρ : Assign Color 2, eval (independentEQ (α := Color)) ρ → ρ 0 = ρ 1 :=
  ⟨independentEQ_holds, independentEQ_not_eq Fin.zero_ne_one⟩

theorem shared_not_independent_color :
    ∃ ρ : Assign Color 2,
      eval (independentEQ (α := Color)) ρ ∧ ¬ eval (sharedEQ (α := Color)) ρ :=
  shared_not_independent Fin.zero_ne_one

end FiveBoundary.PP
