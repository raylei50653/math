/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.SymRelabel
import Mathlib.Data.Fin.Tuple.Sort

/-!+# Sorted attachment representatives for every finite C5 cell

This is a graph-level SYM existence theorem, independent of Python and of planarity.
The permutation is a pullback: new interior index `m` reads old index `σ m`.
Sortedness is not invariant under arbitrary relabelling; existence of a sorted
representative is the property needed for lossless normalisation.
-/

namespace FiveBoundary.Sym

/-- Five attachment bits, with boundary index `i` carrying weight `2^i`. -/
noncomputable def attMask (G : SimpleGraph (Fin n)) (B : Fin 5 ↪ Fin n)
    (v : Fin n) : ℕ := by
  classical
  exact ∑ i : Fin 5, if G.Adj (B i) v then 2 ^ i.val else 0

theorem attMask_relabel (G : SimpleGraph (Fin n)) (π : Equiv.Perm (Fin n))
    (B : Fin 5 ↪ Fin n) (hB : ∀ i, π (B i) = B i) (v : Fin n) :
    attMask (relabel π G) B v = attMask G B (π v) := by
  classical
  simp only [attMask, relabel_adj, hB]

/-- Extend a permutation of the private indices, fixing the five boundary vertices. -/
def interiorPerm {k : ℕ} (σ : Equiv.Perm (Fin k)) : Equiv.Perm (Fin (5 + k)) :=
  finSumFinEquiv.symm.trans ((Equiv.sumCongr (Equiv.refl (Fin 5)) σ).trans
    finSumFinEquiv)

@[simp] theorem interiorPerm_boundary {k : ℕ} (σ : Equiv.Perm (Fin k)) (i : Fin 5) :
    interiorPerm σ (firstBoundary (Nat.le_add_right 5 k) i) =
      firstBoundary (Nat.le_add_right 5 k) i := by
  change interiorPerm σ (Fin.castAdd k i) = Fin.castAdd k i
  simp [interiorPerm]

@[simp] theorem interiorPerm_private {k : ℕ} (σ : Equiv.Perm (Fin k)) (m : Fin k) :
    interiorPerm σ (Fin.natAdd 5 m) = Fin.natAdd 5 (σ m) := by
  simp [interiorPerm]

/-- SYM uses numeric mask order, not the number of attached boundary vertices. -/
def SortedAttachments {k : ℕ} (G : SimpleGraph (Fin (5 + k))) : Prop :=
  Antitone (fun m : Fin k =>
    attMask G (firstBoundary (Nat.le_add_right 5 k)) (Fin.natAdd 5 m))

theorem attMask_relabel_interior {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (σ : Equiv.Perm (Fin k)) (m : Fin k) :
    attMask (relabel (interiorPerm σ) G) (firstBoundary (Nat.le_add_right 5 k))
      (Fin.natAdd 5 m) =
    attMask G (firstBoundary (Nat.le_add_right 5 k)) (Fin.natAdd 5 (σ m)) := by
  rw [attMask_relabel G (interiorPerm σ) _ (interiorPerm_boundary σ),
    interiorPerm_private]

/-- Every cell, for arbitrary `k` including zero and tied masks, has a sorted
boundary-fixing relabelling with exactly the same complete colouring relation. -/
theorem exists_sorted_relabel {k : ℕ} (G : SimpleGraph (Fin (5 + k))) :
    ∃ σ : Equiv.Perm (Fin k),
      SortedAttachments (relabel (interiorPerm σ) G) ∧
      Sigma (relabel (interiorPerm σ) G) (firstBoundary (Nat.le_add_right 5 k)) =
        Sigma G (firstBoundary (Nat.le_add_right 5 k)) := by
  let f : Fin k → ℕᵒᵈ := fun m =>
    attMask G (firstBoundary (Nat.le_add_right 5 k)) (Fin.natAdd 5 m)
  refine ⟨Tuple.sort f, ?_, Sigma_relabel _ _ (interiorPerm_boundary _)⟩
  intro i j hij
  simp only [attMask_relabel_interior]
  exact Tuple.monotone_sort f hij

end FiveBoundary.Sym
