/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Boundary

/-! Generic full boundary relations. Pair relations are derived projections;
there is deliberately no reconstruction of a full relation from pair data.
No operation here asserts geometric composability. -/
namespace FiveBoundary.BoundaryRelations

abbrev BoundaryRel (k : ℕ) := Finset (BoundaryAssignment k)

def pairProjection {k : ℕ} (r : BoundaryRel k) (i j : Fin k) : Finset (Color × Color) :=
  r.image (fun b => (b i, b j))

def condition {k : ℕ} (r : BoundaryRel k) (guard : BoundaryAssignment k → Prop)
    [DecidablePred guard] : BoundaryRel k := r.filter guard

def Forces {k : ℕ} (r : BoundaryRel k) (i j : Fin k) (predicate : Color × Color → Prop) : Prop :=
  (pairProjection r i j).Nonempty ∧ ∀ p ∈ pairProjection r i j, predicate p

def ForcesEq {k : ℕ} (r : BoundaryRel k) (i j : Fin k) : Prop :=
  Forces r i j (fun p => p.1 = p.2)

def ForcesNeq {k : ℕ} (r : BoundaryRel k) (i j : Fin k) : Prop :=
  Forces r i j (fun p => p.1 ≠ p.2)

theorem mem_pairProjection {k : ℕ} (r : BoundaryRel k) (i j : Fin k) (p : Color × Color) :
    p ∈ pairProjection r i j ↔ ∃ b ∈ r, (b i, b j) = p := by
  simp [pairProjection]

theorem forces_iff {k : ℕ} (r : BoundaryRel k) (i j : Fin k)
    (predicate : Color × Color → Prop) :
    Forces r i j predicate ↔ r.Nonempty ∧ ∀ b ∈ r, predicate (b i, b j) := by
  simp [Forces, pairProjection]

/-- Guard satisfiability is part of forcing, so an inconsistent assumption
cannot force both equality and inequality by vacuity. -/
theorem conditional_forces_iff {k : ℕ} (r : BoundaryRel k) (i j : Fin k)
    (guard : BoundaryAssignment k → Prop) [DecidablePred guard]
    (predicate : Color × Color → Prop) :
    Forces (condition r guard) i j predicate ↔
      (∃ b ∈ r, guard b) ∧ ∀ b ∈ r, guard b → predicate (b i, b j) := by
  rw [forces_iff]
  simp [condition, Finset.Nonempty]

theorem empty_not_forces {k : ℕ} (i j : Fin k) (predicate : Color × Color → Prop) :
    ¬ Forces (∅ : BoundaryRel k) i j predicate := by
  simp [forces_iff]

theorem condition_inter {k : ℕ} (r s : BoundaryRel k)
    (guard : BoundaryAssignment k → Prop) [DecidablePred guard] :
    condition (r ∩ s) guard = condition r guard ∩ condition s guard := by
  ext b
  simp [condition, and_assoc, and_left_comm, and_comm]

/-- Projection can lose shared-witness correlation. Only this inclusion is
valid in general; intersect full relations BEFORE projecting. -/
theorem pairProjection_inter_subset {k : ℕ} (r s : BoundaryRel k) (i j : Fin k) :
    pairProjection (r ∩ s) i j ⊆ pairProjection r i j ∩ pairProjection s i j := by
  intro p hp
  obtain ⟨b, hb, rfl⟩ := (mem_pairProjection _ _ _ _).mp hp
  exact Finset.mem_inter.mpr
    ⟨(mem_pairProjection _ _ _ _).mpr ⟨b, (Finset.mem_inter.mp hb).1, rfl⟩,
     (mem_pairProjection _ _ _ _).mpr ⟨b, (Finset.mem_inter.mp hb).2, rfl⟩⟩

end FiveBoundary.BoundaryRelations
